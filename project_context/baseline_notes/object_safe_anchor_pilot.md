# Object-Safe Anchor Pilot

> Date: 2026-05-02
> Scope: `Object-Safe Early Anchor` pilot on COCO-CHAIR using the existing fixed `first_logit` setup as the base.
> Boundary:
> - no regular rerun
> - no fixed first-logit rerun
> - no prompt change
> - no evaluator change
> - no `The effect`
> - no parameter sweep
> - no full run if the `1000` pilot is unhealthy

## 1. Why Object-Safe Anchor

The object-level mechanism analysis suggested a specific failure mode in fixed `first_logit / early-anchor`:

- it removes many high-frequency over-mentioned hallucinated objects
- but it also introduces some plausible-but-absent indoor / kitchen / furniture nouns
- introduced hallucinations tend to have stronger anchor support
- they are more likely to be pushed upward by the fixed later-step anchor formula

So this pilot tested a minimal method change:

- keep the same early-anchor decoding skeleton
- but reduce positive anchor boost on object noun tokens

The goal was:

- preserve the useful later-step anchor effect
- while reducing anchor-driven promotion of plausible absent object nouns

## 2. Method Definition

Base method:

- the current fixed later-step `first_logit` adaptation
- same:
  - `gamma = 0.3`
  - `lambda = 0.05`
  - `cd_beta = 0.1`
  - prompt
  - greedy decoding
  - `max_new_tokens = 64`
  - no first-token modification
  - no `The effect`

New rule:

- if a token belongs to the object noun vocabulary
- and its early-anchor adjustment is positive
- then scale only that positive adjustment by:
  - `object_positive_scale = 0.25`

Formally:

- baseline:
  - `adjustment = weight_t * first_anchor_logits`
- object-safe:
  - if token is object-token and `adjustment > 0`
    - `adjustment := 0.25 * adjustment`
  - else keep the original adjustment

Everything else stays unchanged.

## 3. Object Vocabulary Source

Object vocabulary source:

- official CHAIR synonym list used by the current evaluator:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/resources/chair/data/synonyms.txt`

Implementation details:

- vocabulary terms come from the official CHAIR object synonym entries
- matching is done at `token-id` level
- each official object term is tokenized with the current LLaVA tokenizer
- all token ids appearing in those tokenized object terms are added to the object-token-id set

Multi-token objects:

- phrases like `dining table`, `cell phone`, `sports ball` are handled by adding all token ids appearing in the tokenized phrase
- this is therefore a token-id-level pilot approximation, not a phrase-level context disambiguator

Important boundary:

- the method does **not** use image GT
- it uses only a general object noun / synonym vocabulary

## 4. Remote Implementation

New remote scripts:

- main caption script:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/coco_caption_object_safe_anchor.py`
- resumable wrapper:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/coco_caption_object_safe_resumable.py`

Logic test:

- a minimal red-green logic test was run on remote to verify:
  - positive object-token anchor boost is scaled
  - negative boost is preserved
  - non-object-token boost is preserved

## 5. 1000-Image Pilot Result

Remote output:

- captions:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/coco_chair/object_safe_anchor_caption_1000.json`
- eval json:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/coco_chair_object_safe_anchor_eval_1000.json`
- metrics csv:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/object_safe_anchor_1000_metrics.csv`
- metrics markdown:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/object_safe_anchor_1000_metrics.md`

Main metrics:

| Method | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Object Count | s/sample |
|---|---:|---:|---:|---:|---:|---:|---:|
| regular | 1000 | 0.2090 | 0.0657 | 49.6580 | 4522 | 297 | 1.3092 |
| fixed first_logit | 1000 | 0.1610 | 0.0509 | 50.9190 | 4717 | 240 | 1.3110 |
| object_safe_anchor | 1000 | 0.1620 | 0.0530 | 51.3090 | 4228 | 224 | 1.3206 |

Direct comparison vs fixed `first_logit`:

- `CHAIRs`:
  - `0.1610 -> 0.1620`
  - slightly worse
- `CHAIRi`:
  - `0.0509 -> 0.0530`
  - worse
- `Hallucinated Object Count`:
  - `240 -> 224`
  - better in raw count
- `Object Mentions`:
  - `4717 -> 4228`
  - `-489`
- `Avg Caption Length`:
  - `50.9190 -> 51.3090`
  - `+0.3900`

## 6. Behavior Analysis vs Fixed First-Logit

Image-level behavior:

- changed caption count:
  - `955 / 1000`
- first word changed count:
  - `0 / 1000`
- empty caption count:
  - `0`
- improved images:
  - `72`
- worsened images:
  - `70`
- stable images:
  - `858`

Object-level movement vs fixed `first_logit`:

- total removed hallucination events:
  - `116`
- total introduced hallucination events:
  - `100`
- net hallucinated object count delta:
  - `-16`

Top reduced hallucinations vs fixed `first_logit`:

- `dining table`: `15`
- `person`: `11`
- `chair`: `11`
- `car`: `7`
- `bench`: `5`
- `spoon`: `5`

Top newly introduced hallucinations vs fixed `first_logit`:

- `car`: `12`
- `dining table`: `11`
- `microwave`: `7`
- `chair`: `6`
- `couch`: `6`
- `bench`: `5`

## 7. Does It Beat Fixed First-Logit?

Current answer:

- no

Why:

- it does reduce raw hallucinated object count slightly
- but it does **not** improve `CHAIRs`
- and it makes `CHAIRi` worse

Most importantly, the gain comes with a substantial drop in object mentions:

- object mentions delta vs fixed `first_logit`:
  - `-489`
- correct object mentions delta vs fixed `first_logit`:
  - `-473`

So the method is not simply filtering introduced hallucinations cleanly.

It is also suppressing many correct object mentions.

## 8. Is The Gain Coming From Shorter Captions?

Current answer:

- no

Evidence:

- average caption length increases by `+0.3900` vs fixed `first_logit`
- first word changed count remains `0`

So this is not a caption-shortening artifact.

## 9. Main Failure Mode

The pilot suggests that this object-safe rule is too blunt in its current form.

What it appears to do:

- it weakens positive anchor push on object-token ids
- that does suppress some introduced hallucinations
- but it also suppresses many correct object mentions

So the current token-id-level rule is not yet object-safe in the useful sense.

It is closer to:

- generic object-token dampening

than to:

- selective protection against anchor-driven hallucinated objects

## 10. Full Run Decision

Current decision:

- do **not** continue to full `40504`

Reason:

- the `1000` pilot does not beat fixed `first_logit`
- `CHAIRs` is slightly worse
- `CHAIRi` is worse
- object mentions drop substantially
- correct object mentions also drop substantially

So the pilot fails the intended health gate for automatic expansion.

## 11. Whether To Continue This Method

Current answer:

- not in this exact fixed form

What remains useful:

- the mechanism hypothesis was directionally reasonable
- the result still reinforces that introduced hallucinations are tied to object-token-level anchor effects

What does **not** look good:

- a flat token-id-level downscaling of all positive object-token boosts

If the line is revisited later, it should likely become:

- more local
- more context-sensitive
- less equivalent to global object suppression

## 12. Caveats

1. This is a `1000`-image pilot only.
2. Object matching is token-id-level, not phrase-level contextual parsing.
3. No image GT is used, by design.
4. The pilot is informative even though negative:
   - it shows that naively shrinking positive anchor boost on all object-token ids is too coarse.
