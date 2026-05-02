# Attention-Gated Early Anchor

> Date: 2026-05-02
> Scope: `Attention-Gated Early Anchor` pilot on COCO-CHAIR as a stricter successor to fixed `first_logit / early-anchor`.
> Boundary:
> - no regular rerun
> - no fixed first-logit rerun
> - no prompt change
> - no evaluator change
> - no `The effect`
> - no parameter sweep
> - no classifier
> - no full run unless the `1000` pilot beats or meaningfully improves on fixed `first_logit`

## 1. Why Attention-Gated Early Anchor

The current mechanism picture suggested a more selective variant than flat `Object-Safe`.

Known facts before this pilot:

- fixed `first_logit / early-anchor` improves full COCO-CHAIR vs regular
- introduced hallucinations often have strong anchor support
- correct object mentions usually have stronger middle-layer image attention
- flat `Object-Safe` reduced some hallucinations, but also suppressed many correct object mentions

So this pilot tested a narrower rule:

- keep fixed `first_logit` as the default
- only shrink positive anchor boost on object-token ids
- and only when the current decoding step has weak middle-layer image attention support
- and only for the strongest object-token positive boosts at that step

The intended goal was:

- keep the useful early-anchor effect
- but stop the anchor from over-promoting plausible-but-absent object nouns

## 2. Offline Feasibility

Offline feasibility used the completed object-local probe:

- input:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/object_local_signal_probe.csv`
- output:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/attention_gate_offline_feasibility.md`
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/attention_gate_offline_feasibility.csv`

Unsupervised thresholds:

- low attention threshold:
  - `p25(image_attention_middle_mean over all object-local events)`
  - value: `0.13209990615194495`
- reference strong boost threshold from offline probe:
  - `p75(positive anchor_adjustment_delta over all object-local events)`
  - value: `1.2488965899946751`

Key feasibility result:

- flat Object-Safe expected correct-hit rate:
  - `0.998`
- Gate A low-attention-only expected correct-hit rate:
  - `0.123`
- Gate B low-attention + strong-boost expected correct-hit rate:
  - `0.055`
- Gate B introduced-hallucination hit rate:
  - `0.110`

Interpretation:

- the attention gate looked much more selective than flat Object-Safe
- it still targeted introduced hallucinations about `2x` as often as correct object mentions
- so the idea was worth a runtime pilot

Important caveat:

- offline feasibility only had event-level summaries
- runtime gating therefore used the same low-attention threshold, but operationalized strong support as:
  - top quartile among current-step positive object-token anchor boosts
- this means the runtime gate was conceptually aligned with feasibility, but not identical to the offline proxy

## 3. Gate Definition

Base method:

- fixed later-step `first_logit / early-anchor`
- same:
  - `gamma = 0.3`
  - `lambda = 0.05`
  - `cd_beta = 0.1`
  - prompt
  - greedy decoding
  - `max_new_tokens = 64`
  - no first-token modification
  - no `The effect`

Primary runtime variant:

- `AttnAnchor`

Rule:

- first generated token stays unchanged
- step `0` only provides the anchor
- from decode step `1` onward:
  - compute middle-layer image attention mass for the current query token
  - if middle attention is below the unsupervised low-attention threshold
  - then identify object-token ids with positive anchor boost
  - among them, keep only the top quartile positive boosts as `strong-support` tokens
  - scale those positive boosts by:
    - `object_positive_scale = 0.25`
- negative adjustments remain unchanged
- non-object tokens remain unchanged

## 4. Implementation Details

Remote implementation:

- main script:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/coco_caption_attention_gated_anchor.py`
- resumable wrapper:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/coco_caption_attention_gated_resumable.py`

Object vocabulary source:

- official CHAIR synonyms:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/resources/chair/data/synonyms.txt`

Object-token matching:

- token-id-level match
- each CHAIR object synonym term is tokenized with the LLaVA tokenizer
- all token ids that appear in tokenized object terms are added to the object-token set
- multi-token objects are therefore approximated by the union of their token ids

Important boundary:

- no image GT is used at runtime
- no full attention tensor is saved
- no hidden states are saved
- the old fixed `first_logit` script is left untouched

## 5. 10-Image Sanity

Remote outputs:

- captions:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/coco_chair/attention_gated_caption_10.json`
- eval:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/coco_chair_attention_gated_eval_10.json`
- summary:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/attention_gated_10_metrics.md`

Health checks:

- first word changed vs fixed `first_logit`:
  - `0`
- first word changed vs regular:
  - `0`
- empty caption count:
  - `0`
- evaluator ran successfully:
  - yes
- runtime was stable:
  - yes
- peak reserved GPU memory:
  - about `14.04 GB`

Sanity conclusion:

- the implementation path is correct
- the gate really triggers at runtime
- there is no first-token violation
- the 10-image slice is too noisy to use for method judgment

## 6. 1000-Image Pilot Result

Remote outputs:

- captions:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/coco_chair/attention_gated_attnanchor_caption_1000.json`
- resumable work log:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/coco_chair/attention_gated_attnanchor_caption_1000_resume.jsonl`
- eval:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/coco_chair_attention_gated_attnanchor_eval_1000.json`
- metrics:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/attention_gated_attnanchor_1000_metrics.csv`
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/attention_gated_attnanchor_1000_metrics.md`

Main metrics:

| Method | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Object Count | s/sample |
|---|---:|---:|---:|---:|---:|---:|---:|
| regular | 1000 | 0.2090 | 0.0657 | 49.6580 | 4522 | 297 | 1.3092 |
| fixed first_logit | 1000 | 0.1610 | 0.0509 | 50.9190 | 4717 | 240 | 1.3110 |
| object_safe_anchor | 1000 | 0.1620 | 0.0530 | 51.3090 | 4228 | 224 | 1.3206 |
| attention_gated_attnanchor | 1000 | 0.1680 | 0.0575 | 51.1140 | 4329 | 249 | 1.3834 |

## 7. Comparison With Fixed First-Logit

Direct comparison vs fixed `first_logit`:

- `CHAIRs`:
  - `0.1610 -> 0.1680`
  - worse
- `CHAIRi`:
  - `0.0509 -> 0.0575`
  - worse
- hallucinated object count:
  - `240 -> 249`
  - worse
- average caption length:
  - `50.9190 -> 51.1140`
  - slightly longer
- object mentions:
  - `4717 -> 4329`
  - `-388`
- correct object mentions:
  - `-397`

Image-level paired behavior vs fixed `first_logit`:

- changed captions:
  - `829 / 1000`
- first word changed:
  - `0 / 1000`
- empty captions:
  - `0`
- improved:
  - `46`
- worsened:
  - `50`
- stable:
  - `904`

Object-level movement vs fixed `first_logit`:

- removed hallucination total:
  - `60`
- introduced hallucination total:
  - `69`
- net hallucinated object delta:
  - `+9`

Top removed hallucinations vs fixed:

- `dining table`: `8`
- `chair`: `7`
- `person`: `6`
- `sports ball`: `4`
- `car`: `4`

Top introduced hallucinations vs fixed:

- `dining table`: `9`
- `microwave`: `6`
- `chair`: `5`
- `bottle`: `5`
- `vase`: `4`
- `sink`: `4`

This means the current gate did **not** solve the indoor / kitchen / furniture introduction pattern cleanly.

## 8. Gate Trigger Analysis

Runtime gate stats on the 1000 pilot:

- average gate-trigger steps per image:
  - `44.315`
- average low-attention steps per image:
  - `44.315`
- total positive object-token boosts observed:
  - `35,821,358`
- total gated positive object-token boosts:
  - `6,337,106`
- gated positive object-token ratio:
  - `0.176909`
- average runtime:
  - `1.3834 s/image`
- peak reserved GPU memory:
  - `14.041 GB`

Interpretation:

- this is much narrower than flat Object-Safe, which effectively touched almost every positive object-token boost
- but it is still active on too many steps and too many token ids
- in practice it still behaves like broad object-token dampening often enough to hurt correct mentions

## 9. Does It Beat Fixed First-Logit?

Current answer:

- no

Why:

- both `CHAIRs` and `CHAIRi` are worse than fixed `first_logit`
- raw hallucinated object count is also worse
- the method reduces object mentions and correct object mentions
- removed hallucinations do not outnumber introduced ones

So the current `AttnAnchor` pilot fails the health gate for automatic full expansion.

## 10. Does It Avoid Object-Safe Collapse?

Current answer:

- only partially

Compared with flat `Object-Safe`:

- object mentions drop:
  - `-388` for attention-gated vs fixed
  - `-489` for object-safe vs fixed
- correct object mentions drop:
  - `-397` for attention-gated vs fixed
  - `-473` for object-safe vs fixed

So the attention gate is somewhat less destructive than flat object-vocab suppression, but not enough to become a better decoding method.

## 11. Why It Likely Failed

The most plausible current explanation is:

- the gate is still defined over a broad object-token-id vocabulary
- low attention happens on many later decoding steps
- on those steps, the top-quartile positive object-token boosts still cover many token ids
- so the gate still suppresses a broad slice of valid object-token support

In other words:

- it is more selective than flat `Object-Safe`
- but not yet selective enough at the actual object-mention decision boundary

## 12. Full Run Decision

Current decision:

- do **not** continue to full `40504`

Reason:

- the `1000` pilot does not beat fixed `first_logit`
- `CHAIRs` and `CHAIRi` are both worse
- hallucinated object count is worse
- object mentions and correct object mentions still fall materially

So the pilot fails the user-specified automatic full-run condition.

## 13. Whether To Continue This Exact Method

Current answer:

- not in its current form

What this pilot still contributes:

- low-attention gating is more defensible than flat object-vocab dampening
- but a step-level token-vocab gate is still too coarse

So the next method should be narrower than:

- `all object-token ids on low-attention steps`

and closer to:

- candidate-object-specific
- phrase-aware
- or mention-local suppression

## 14. Next Recommendation

Recommended next step:

- keep fixed `first_logit / early-anchor` as the best current decoding baseline
- do **not** full-run this `AttnAnchor` variant
- if method work continues, move to a tighter object-local intervention that operates closer to the actual candidate object token or mention span
- do not return to flat object-vocab suppression
- do not start parameter sweep or new benchmark expansion from this pilot
