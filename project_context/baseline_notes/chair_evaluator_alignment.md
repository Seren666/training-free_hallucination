# CHAIR Evaluator Alignment

> Date: 2026-05-02
> Scope: protocol and code-level alignment audit for the current `Python3 adapted CHAIR-style evaluator`.

## 1. Current Evaluator Under Audit

Current evaluator:

- remote path:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/coco_chair_eval.py`

Reference official-style code available on remote:

- `/root/autodl-tmp/code/training_free_hallucination_probe/resources/chair/chair.py`
- `/root/autodl-tmp/code/training_free_hallucination_probe/resources/chair/misc.py`
- `/root/autodl-tmp/code/training_free_hallucination_probe/resources/chair/data/synonyms.txt`

## 2. Object List / Synonym Mapping Source

The adapted evaluator uses the same synonym source as the official-style CHAIR code:

- source file:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/resources/chair/data/synonyms.txt`

Current adapted logic:

- reads the synonym groups from `synonyms.txt`
- builds:
  - `object_vocab`
  - `inverse_synonym_dict`
- canonicalizes each recognized object word to the first synonym in the group

This is aligned with the official-style `chair.py`, which also:

- reads `data/synonyms.txt`
- expands `mscoco_objects`
- maps each synonym to a canonical representative via `inverse_synonym_dict`

## 3. Ground-Truth Annotation Source

The adapted evaluator uses:

- `instances_val2014.json`
- `captions_val2014.json`

and builds the ground-truth object set for each evaluated image from:

1. COCO instance categories
2. COCO ground-truth captions

This matches the core CHAIR idea in the official-style code:

- objects come from both segmentation / instance annotations and captions

Difference:

- `chair.py` contains helper functions that combine `train2014 + val2014`
- the adapted evaluator uses only `val2014`

Current impact judgment:

- for this benchmark, evaluated images are all `val2014`
- so using `val2014` annotations only should be sufficient for these image ids
- this difference is unlikely to change the current paired comparison materially

## 4. Hallucination Decision Logic

The adapted evaluator marks an object mention as hallucinated if:

1. the object phrase is recognized as a COCO object under the synonym list
2. it is canonicalized to a COCO object label
3. that canonical object is not present in the image-level ground-truth object set

Metric definitions:

- `CHAIRs`:
  - sentence-level rate
  - a caption counts as hallucinated if it contains at least one hallucinated object mention
- `CHAIRi`:
  - instance-level rate
  - hallucinated object mentions divided by total recognized COCO object mentions

This is consistent with the official-style `chair.py` logic:

- `CHAIRs = num_hallucinated_caps / num_caps`
- `CHAIRi = hallucinated_word_count / coco_word_count`

## 5. Caption Normalization / Token Processing

The current adapted evaluator applies the same normalization path to both `regular` and `first_logit` captions:

- lowercase conversion
- regex token extraction:
  - `[a-z]+`
- custom singularization rules for:
  - irregular plurals
  - `-ies`
  - `-ves`
  - `-es`
  - `-s`
- multi-word COCO phrase merging for items such as:
  - `sports ball`
  - `baseball bat`
  - `baseball glove`
  - `traffic light`
  - `wine glass`
  - `potted plant`
- special-case cleanup such as:
  - `toilet seat -> toilet`
  - `bow tie -> tie`

This is directionally aligned with official-style `chair.py`, which uses:

- lowercase conversion
- `nltk.word_tokenize`
- `pattern.en.singularize`
- the same official synonym vocabulary
- the same double-word and special-case rules

## 6. Consistency With Standard CHAIR

### 6.1 Strong alignment points

The adapted evaluator is meaningfully aligned with standard CHAIR on the parts that matter most for current paired analysis:

- same synonym resource
- same canonicalization concept
- same use of segmentation / instance labels plus captions for ground truth
- same sentence-level hallucination definition
- same instance-level hallucination definition
- same double-word and special-case object handling pattern

### 6.2 Known differences

Important differences still remain:

1. runtime / language version
   - official-style code is Python2-era
   - current evaluator is a Python3 adaptation

2. tokenizer / singularizer
   - official-style code uses `nltk.word_tokenize` and `pattern.en.singularize`
   - current evaluator uses regex tokenization plus a custom singularizer

3. annotation loading helper
   - official-style code combines `train2014 + val2014`
   - current evaluator uses `val2014` only
   - for current `val2014` evaluation, this is probably harmless

4. input format
   - official-style code expects a caption-eval dictionary containing `imgToEval` and metrics like `SPICE`, `CIDEr`, `BLEU`
   - current evaluator accepts a lightweight caption payload with `samples`
   - this does not affect CHAIR computation directly, but it means the current run is not an untouched official script execution

5. dependency environment
   - current remote env does not have `pattern` or `nltk`
   - official-style code also contains Python2 print syntax and old dependency assumptions

## 7. Bias Check

Current evidence does not suggest a formatting bias toward either `regular` or `first_logit`.

Why:

- both methods use the same evaluator code path
- both methods use the same synonym file
- both methods use the same ground-truth object construction
- both methods use the same `image_id` set and image order
- both methods use the same caption normalization rules

So any residual evaluator mismatch with official CHAIR should mostly affect absolute values, not the internal fairness of the current paired comparison.

## 8. Can We Directly Run The Official Script Right Now?

Not cleanly in the current environment.

Direct-run blockers confirmed on remote:

- `chair.py` is Python2-era and fails Python3 compilation because of old `print` syntax
- the current `vcd` environment does not have:
  - `nltk`
  - `pattern`
- the official-style code expects caption-eval style `imgToEval` input with metric fields
- the current full caption files are lightweight caption payloads, not official caption-eval outputs

So this round still did not execute the untouched official CHAIR evaluator directly.

## 9. Near-Official Alignment Run

A near-official alignment path was completed successfully without rerunning generation.

Remote alignment workspace:

- `/root/autodl-tmp/code/training_free_hallucination_probe/chair_alignment`

Remote alignment result files:

- `/root/autodl-tmp/code/training_free_hallucination_probe/results/chair_alignment_regular_eval.json`
- `/root/autodl-tmp/code/training_free_hallucination_probe/results/chair_alignment_first_logit_eval.json`
- `/root/autodl-tmp/code/training_free_hallucination_probe/results/chair_alignment_metrics.csv`
- `/root/autodl-tmp/code/training_free_hallucination_probe/results/chair_alignment_metrics.md`

Artifact caveat:

- a summary json was emitted remotely with a stray carriage-return suffix in its filename
- it is not needed for the result comparison
- the authoritative outputs are the two `*_eval.json` files plus `metrics.csv` / `metrics.md`

Near-official implementation choices:

- official `synonyms.txt`
- official-style double-word and special-case object rules
- combined `train2014 + val2014` GT caption / instance annotations
- converted official-like `imgToEval` payload
- vendored `nltk` tokenizer path
- custom singularizer fallback because `pattern.en` was unavailable

Actual runtime modes:

- tokenizer:
  - `nltk_word_tokenize`
- singularizer:
  - `custom`

## 10. Adapted Vs Near-Official Comparison

| Evaluator | Method | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Objects |
|---|---|---:|---:|---:|---:|---:|---:|
| adapted | regular | 40504 | 0.2037 | 0.0655 | 49.6823 | 181268 | 11875 |
| adapted | first_logit | 40504 | 0.1631 | 0.0513 | 50.9320 | 187440 | 9609 |
| near_official | regular | 40504 | 0.1997 | 0.0669 | 49.3534 | 172330 | 11528 |
| near_official | first_logit | 40504 | 0.1594 | 0.0524 | 50.5482 | 178315 | 9337 |

Delta vs regular:

- adapted:
  - `CHAIRs`: `-0.0406`
  - `CHAIRi`: `-0.0142`
- near-official:
  - `CHAIRs`: `-0.0403`
  - `CHAIRi`: `-0.0145`

Judgment:

- improvement direction is the same
- improvement magnitude is very close
- evaluator changes slightly move the absolute values
- evaluator changes do not reverse the method ranking

## 11. Credibility Judgment

Current judgment:

- the adapted evaluator remains credible for internal paired comparison and mechanism analysis
- the near-official alignment materially strengthens confidence in the full COCO-CHAIR result
- the main qualitative conclusion still holds:
  - `first_logit` lowers `CHAIRs` and `CHAIRi` on full `40504`-image COCO-CHAIR
- the current result should now be described as:
  - `adapted evaluator result confirmed by near-official alignment`
  - not yet an untouched official CHAIR execution

Recommended phrasing for current result quality:

- good enough for research direction filtering
- strong enough to justify mechanism analysis
- still short of the strictest paper-level protocol claim

## 12. What Still Needs To Be Done For Paper-Level Alignment

If later we want stronger protocol alignment, the next steps should be:

1. provision a clean official-compatible CHAIR environment
   - ideally with Python2-compatible execution or an explicitly validated faithful port

2. restore official-style singularization as closely as possible
   - `pattern.en` or a validated substitute

3. rerun CHAIR scoring only on the existing `regular` and `first_logit` full captions
   - no new generation needed

4. compare:
   - adapted evaluator numbers
   - near-official alignment numbers
   - untouched official or validated official-port numbers

## 13. Bottom Line

The adapted evaluator is not identical to the untouched official CHAIR code, but it is strongly aligned on the core hallucination logic and it does not show an obvious bias favoring `regular` or `first_logit`.

After the near-official alignment run:

- the paired full COCO-CHAIR result remains credible
- the positive `first_logit` direction survives a more official-like evaluation path
- the absolute metric values should still carry an official-alignment caveat
