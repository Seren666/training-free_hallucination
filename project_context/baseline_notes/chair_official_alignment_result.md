# CHAIR Official Alignment Result

> Date: 2026-05-02
> Scope: re-evaluate existing full COCO-CHAIR captions with an official / near-official CHAIR path only; no caption generation rerun.

## 1. Status

This round did not rerun caption generation.

Inputs:

- regular captions:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/coco_chair/regular_caption_full.json`
- first-logit captions:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/coco_chair/first_logit_caption_full.json`

Current conclusion:

- untouched official `chair.py` is not directly runnable in the current `vcd` environment
- a near-official alignment path was completed successfully
- the near-official result preserves the same improvement direction as the adapted evaluator

## 2. Why Untouched Official CHAIR Did Not Run Directly

Reference remote files:

- `/root/autodl-tmp/code/training_free_hallucination_probe/resources/chair/chair.py`
- `/root/autodl-tmp/code/training_free_hallucination_probe/resources/chair/data/synonyms.txt`
- `/root/autodl-tmp/code/training_free_hallucination_probe/resources/chair/requirements.txt`

Direct-run blockers:

1. `chair.py` is Python2-era code and fails Python3 compilation because of old `print` syntax.
2. The current `vcd` environment does not have `nltk` or `pattern`.
3. Official-style code expects caption-eval style `imgToEval` input rather than the current lightweight caption payload.

So this round should be described as:

- `near-official CHAIR alignment`
- not `untouched official CHAIR execution`

## 3. Near-Official Alignment Setup

Remote alignment workspace:

- `/root/autodl-tmp/code/training_free_hallucination_probe/chair_alignment`

New remote-only scripts:

- `convert_captions_to_chair_format.py`
- `chair_official_alignment_eval.py`

Alignment principles used:

- official `synonyms.txt`
- official-style double-word and special-case object handling
- combined `train2014 + val2014` captions / instances for GT object construction
- official-like `imgToEval` payload after conversion
- no change to existing adapted evaluator
- no new caption generation

Actual runtime modes:

- tokenizer mode:
  - `nltk_word_tokenize`
- singularizer mode:
  - `custom`

Interpretation:

- tokenizer path is close to official
- singularization is still not official because `pattern.en` was unavailable

## 4. Main Alignment Metrics

| Evaluator | Method | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Objects |
|---|---|---:|---:|---:|---:|---:|---:|
| adapted | regular | 40504 | 0.2037 | 0.0655 | 49.6823 | 181268 | 11875 |
| adapted | first_logit | 40504 | 0.1631 | 0.0513 | 50.9320 | 187440 | 9609 |
| near_official | regular | 40504 | 0.1997 | 0.0669 | 49.3534 | 172330 | 11528 |
| near_official | first_logit | 40504 | 0.1594 | 0.0524 | 50.5482 | 178315 | 9337 |

Remote near-official result files:

- `/root/autodl-tmp/code/training_free_hallucination_probe/results/chair_alignment_regular_eval.json`
- `/root/autodl-tmp/code/training_free_hallucination_probe/results/chair_alignment_first_logit_eval.json`
- `/root/autodl-tmp/code/training_free_hallucination_probe/results/chair_alignment_metrics.csv`
- `/root/autodl-tmp/code/training_free_hallucination_probe/results/chair_alignment_metrics.md`

Note:

- a summary json was also emitted remotely with a stray carriage-return suffix in its filename
- it is not used as an authoritative artifact
- the authoritative alignment outputs are the two `*_eval.json` files plus `metrics.csv` / `metrics.md`

## 5. Delta Vs Regular

| Evaluator | CHAIRs delta | CHAIRi delta | AvgLen delta | Object Mentions delta | Hallucinated Objects delta |
|---|---:|---:|---:|---:|---:|
| adapted | -0.0406 | -0.0142 | +1.2497 | +6172 | -2266 |
| near_official | -0.0403 | -0.0145 | +1.1948 | +5985 | -2191 |

Consistency judgment:

- `CHAIRs` improvement direction:
  - same
- `CHAIRi` improvement direction:
  - same
- magnitude:
  - very close

## 6. What Shifted Between Evaluators

Absolute values moved slightly:

- `CHAIRs`
  - regular: `0.2037 -> 0.1997`
  - first_logit: `0.1631 -> 0.1594`
- `CHAIRi`
  - regular: `0.0655 -> 0.0669`
  - first_logit: `0.0513 -> 0.0524`

Most likely reasons:

1. near-official path uses `nltk.word_tokenize`
2. adapted evaluator used regex tokenization
3. near-official path uses combined `train + val` GT caption/instance annotations
4. singularization still uses a custom fallback rather than `pattern.en`

These differences change absolute counts slightly, but they do not flip the method ranking.

## 7. Bottom Line

The alignment result still supports the same project-level conclusion:

- `first_logit / early-anchor` remains positive on full COCO-CHAIR
- the positive direction is not an artifact of only the adapted evaluator
- the result is now stronger than `adapted-only`, but still not identical to an untouched official CHAIR run

Current safest wording:

- `near-official CHAIR alignment preserves the full-run first_logit gain`
- `paper-level claims should still carry an official-alignment caveat until untouched official or a more exact port is confirmed`
