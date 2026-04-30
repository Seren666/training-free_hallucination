# First-Logit POPE Reproduction

> Date: 2026-04-30
> Scope: full POPE 9-split baseline reproduction on the remote GPU instance using the existing LLaVA-1.5 checkpoint and existing POPE data.
> Boundary:
> - no baseline repo clone
> - no model or dataset download
> - no The effect
> - no extra forward
> - no full attention / hidden-state dumping
> - no local raw-output sync

## 1. Bottom line

Completed:

- full POPE `9/9` splits
- methods:
  - `regular`
  - `first_logit`

Main result:

- under the current LLaVA-1.5 + POPE one-word protocol, `first_logit` is numerically identical to `regular` on all 9 splits
- all metric deltas are `0.0000` at the reported precision for:
  - Accuracy
  - Precision
  - Recall
  - F1
  - Yes Rate
- there is no split with improvement and no split with regression

Interpretation:

- this run is not an official public POPE script from the FLB repo
- it is a faithful adaptation of the released FLB-style first-logit recurrence onto the existing POPE yes/no setting
- because POPE here uses a one-word answer protocol, the first answer token already fixes the yes/no decision
- the faithful FLB-style recurrence only boosts later decode steps, so it does not change the benchmark outcome in this setup

## 1.1 Explicit POPE conclusion

The POPE result should be read as:

- `first_logit` on POPE `9/9` splits has `delta = 0` against `regular`
- this is not a failed implementation signal
- this is a benchmark-protocol signal

The key reason is:

- under the current POPE prompt, the decisive output is usually the first answer token itself
- faithful later-step first-logit boosting starts to matter only after that decision has already been made

Therefore:

- POPE is not an appropriate benchmark for evaluating a later-step first-logit intervention
- POPE is still useful for probing first-answer or pre-answer internal signals
- this result does **not** negate the broader `first-logit / early-anchor` research direction
- it only shows that the current POPE one-word yes/no protocol leaves no room for this specific later-step baseline to act

## 2. What Exactly Was Reproduced

### 2.1 Reproduction type

- `regular`: new custom greedy baseline under the current protocol
- `first_logit`: faithful adaptation, not official direct POPE code release

### 2.2 First-logit implementation choice

Implemented behavior:

- extract the first generated-token logits at step 0 from the same normal forward
- keep them as the anchor distribution
- for later decode steps only, apply the FLB-style recurrence:
  - `weight_t = gamma * (1 - exp(-lambda * step))`
  - `adjusted_logits = current_logits + weight_t * first_anchor_logits`
  - plausibility mask based on the current-step logits and `cd_beta`

Used defaults from the inspected public FLB release:

- `flb_gamma = 0.3`
- `flb_lambda = 0.05`
- `cd_beta = 0.1`

Not used:

- `The effect`
- extra forward
- any object-specific hand tuning
- any classifier

### 2.3 Important protocol caveat

The current prompt keeps the old POPE convention:

- append:
  - `Please answer this question with one word.`

This means:

- the benchmark decision is usually fixed by the first answer token
- faithful FLB-style later-step boosting is expected to have little or no effect on POPE scores

That expectation is exactly what the full run confirmed.

## 3. Runtime Setup

Remote script:

- `/root/autodl-tmp/code/training_free_hallucination_probe/pope_first_logit_eval.py`

Remote raw outputs:

- `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/first_logit_pope_full/`

Remote aggregate metrics:

- `/root/autodl-tmp/code/training_free_hallucination_probe/results/first_logit_pope_metrics.csv`
- `/root/autodl-tmp/code/training_free_hallucination_probe/results/first_logit_pope_metrics.md`

Model and data:

- model:
  - `/root/autodl-tmp/code/VCD/experiments/checkpoints/llava-v1.5-7b`
- POPE root:
  - `/root/autodl-tmp/code/VCD/experiments/data/POPE`
- COCO image root:
  - `/root/autodl-tmp/code/VCD/experiments/data/coco/val2014`
- GQA image root:
  - `/root/autodl-tmp/code/VCD/experiments/data/gqa/images`
- A-OKVQA image root:
  - `/root/autodl-tmp/code/VCD/experiments/data/coco/val2014`

Vision tower offline fix:

- no checkpoint config file was permanently edited
- the probe/eval wrapper overrides the vision tower path at runtime to:
  - `/root/autodl-tmp/hf-home/hub/models--openai--clip-vit-large-patch14-336/snapshots/ce19dc912ca5cd21c8a653c79e251e808ccabcd1`

## 4. Main Result Table

Table 1: Main POPE result

| Dataset | Split | Method | Accuracy | Precision | Recall | F1 | Yes Rate | Samples | s/sample |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| COCO | random | regular | 0.8707 | 0.9720 | 0.7633 | 0.8551 | 0.3927 | 3000 | 0.0995 |
| COCO | random | first_logit | 0.8707 | 0.9720 | 0.7633 | 0.8551 | 0.3927 | 3000 | 0.0992 |
| COCO | popular | regular | 0.8590 | 0.9439 | 0.7633 | 0.8441 | 0.4043 | 3000 | 0.0990 |
| COCO | popular | first_logit | 0.8590 | 0.9439 | 0.7633 | 0.8441 | 0.4043 | 3000 | 0.0992 |
| COCO | adversarial | regular | 0.8360 | 0.8938 | 0.7627 | 0.8230 | 0.4267 | 3000 | 0.0993 |
| COCO | adversarial | first_logit | 0.8360 | 0.8938 | 0.7627 | 0.8230 | 0.4267 | 3000 | 0.0992 |
| GQA | random | regular | 0.8937 | 0.9332 | 0.8480 | 0.8886 | 0.4543 | 3000 | 0.0993 |
| GQA | random | first_logit | 0.8937 | 0.9332 | 0.8480 | 0.8886 | 0.4543 | 3000 | 0.0992 |
| GQA | popular | regular | 0.8403 | 0.8352 | 0.8480 | 0.8415 | 0.5077 | 3000 | 0.0990 |
| GQA | popular | first_logit | 0.8403 | 0.8352 | 0.8480 | 0.8415 | 0.5077 | 3000 | 0.0992 |
| GQA | adversarial | regular | 0.8090 | 0.7866 | 0.8480 | 0.8162 | 0.5390 | 3000 | 0.0989 |
| GQA | adversarial | first_logit | 0.8090 | 0.7866 | 0.8480 | 0.8162 | 0.5390 | 3000 | 0.0989 |
| A-OKVQA | random | regular | 0.8870 | 0.9290 | 0.8380 | 0.8812 | 0.4510 | 3000 | 0.0990 |
| A-OKVQA | random | first_logit | 0.8870 | 0.9290 | 0.8380 | 0.8812 | 0.4510 | 3000 | 0.0988 |
| A-OKVQA | popular | regular | 0.8523 | 0.8627 | 0.8380 | 0.8502 | 0.4857 | 3000 | 0.0990 |
| A-OKVQA | popular | first_logit | 0.8523 | 0.8627 | 0.8380 | 0.8502 | 0.4857 | 3000 | 0.0990 |
| A-OKVQA | adversarial | regular | 0.7887 | 0.7627 | 0.8380 | 0.7986 | 0.5493 | 3000 | 0.0989 |
| A-OKVQA | adversarial | first_logit | 0.7887 | 0.7627 | 0.8380 | 0.7986 | 0.5493 | 3000 | 0.0989 |

## 5. Delta Vs Regular

Table 2: Delta vs regular

| Dataset | Split | First-logit Acc Gain | First-logit F1 Gain | Precision Change | Recall Change | Yes Rate Change | Speed Change |
|---|---|---:|---:|---:|---:|---:|---:|
| COCO | random | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | -0.0003 |
| COCO | popular | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0002 |
| COCO | adversarial | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | -0.0001 |
| GQA | random | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | -0.0001 |
| GQA | popular | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0001 |
| GQA | adversarial | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | -0.0000 |
| A-OKVQA | random | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | -0.0002 |
| A-OKVQA | popular | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| A-OKVQA | adversarial | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | -0.0000 |

## 6. Historical Comparison

Table 3: Historical comparison

> Format in each cell: `Accuracy / F1 / s-sample`
>
> Important caveat:
> - `Full VCD` and `SCMR-VCD` are legacy numbers copied from the frozen old VCD summary
> - current `regular` and `first_logit` come from the new custom greedy wrapper
> - the historical table is useful for orientation, but it is not a strict same-code-path apples-to-apples comparison

| Dataset | Split | Regular | Full VCD | SCMR-VCD | First-logit |
|---|---|---|---|---|---|
| COCO | random | 0.8707 / 0.8551 / 0.0995 | 0.8557 / 0.8409 / 0.2219 | 0.8623 / 0.8491 / 0.1893 | 0.8707 / 0.8551 / 0.0992 |
| COCO | popular | 0.8590 / 0.8441 / 0.0990 | 0.8357 / 0.8227 / 0.2278 | 0.8430 / 0.8315 / 0.2091 | 0.8590 / 0.8441 / 0.0992 |
| COCO | adversarial | 0.8360 / 0.8230 / 0.0993 | 0.8110 / 0.8014 / 0.2228 | 0.8193 / 0.8106 / 0.2156 | 0.8360 / 0.8230 / 0.0992 |
| GQA | random | 0.8937 / 0.8886 / 0.0993 | 0.8593 / 0.8550 / 0.2192 | 0.8647 / 0.8611 / 0.1901 | 0.8937 / 0.8886 / 0.0992 |
| GQA | popular | 0.8403 / 0.8415 / 0.0990 | 0.7927 / 0.8000 / 0.2194 | 0.8003 / 0.8078 / 0.1945 | 0.8403 / 0.8415 / 0.0992 |
| GQA | adversarial | 0.8090 / 0.8162 / 0.0989 | 0.7650 / 0.7793 / 0.2199 | 0.7730 / 0.7880 / 0.2176 | 0.8090 / 0.8162 / 0.0989 |
| A-OKVQA | random | 0.8870 / 0.8812 / 0.0990 | 0.8590 / 0.8547 / 0.2207 | 0.8627 / 0.8597 / 0.1933 | 0.8870 / 0.8812 / 0.0988 |
| A-OKVQA | popular | 0.8523 / 0.8502 / 0.0990 | 0.8210 / 0.8225 / 0.2221 | 0.8230 / 0.8262 / 0.1963 | 0.8523 / 0.8502 / 0.0990 |
| A-OKVQA | adversarial | 0.7887 / 0.7986 / 0.0989 | 0.7620 / 0.7776 / 0.2213 | 0.7640 / 0.7813 / 0.1968 | 0.7887 / 0.7986 / 0.0989 |

## 7. Failure / Behavior Summary

Table 4: Failure / behavior summary

| Dataset | Split | Regular FP | Regular FN | First-logit FP | First-logit FN | Yes Rate Change | Precision Change | Recall Change | Behavior |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| COCO | random | 33 | 355 | 33 | 355 | 0.0000 | 0.0000 | 0.0000 | identical |
| COCO | popular | 68 | 355 | 68 | 355 | 0.0000 | 0.0000 | 0.0000 | identical |
| COCO | adversarial | 136 | 356 | 136 | 356 | 0.0000 | 0.0000 | 0.0000 | identical |
| GQA | random | 91 | 228 | 91 | 228 | 0.0000 | 0.0000 | 0.0000 | identical |
| GQA | popular | 251 | 228 | 251 | 228 | 0.0000 | 0.0000 | 0.0000 | identical |
| GQA | adversarial | 345 | 228 | 345 | 228 | 0.0000 | 0.0000 | 0.0000 | identical |
| A-OKVQA | random | 96 | 243 | 96 | 243 | 0.0000 | 0.0000 | 0.0000 | identical |
| A-OKVQA | popular | 200 | 243 | 200 | 243 | 0.0000 | 0.0000 | 0.0000 | identical |
| A-OKVQA | adversarial | 391 | 243 | 391 | 243 | 0.0000 | 0.0000 | 0.0000 | identical |

## 8. Interpretation

What this run does show:

- the first-logit / early-anchor idea is implementable in the current LLaVA-1.5 + POPE pipeline
- a faithful FLB-style later-step-only adaptation can be reproduced without cloning the baseline repo and without modifying the frozen VCD codebase
- the runtime path is stable and cheap:
  - around `0.099 s/sample`
  - zero sample failures on all `18` runs

What this run does not show:

- it does not validate first-logit as an effective POPE intervention under the current one-word yes/no protocol
- it does not prove the broader first-logit research direction is wrong

The more precise conclusion is:

> under POPE yes/no one-word decoding, faithful FLB-style later-step boosting is too late to alter the benchmark decision boundary.

This is consistent with the earlier step0 / early-decision observation:

- the useful decision is already concentrated at the first answer token
- if the intervention does not touch that token, the score stays unchanged

This should not be misread as:

- `first-logit` signal is useless
- early-anchor analysis is unmotivated
- POPE is no longer useful

The more careful reading is:

- POPE remains a strong benchmark for `answer-boundary` and `pre-answer` signal audit
- POPE is a weak benchmark for `later-step` first-logit intervention evaluation
- false-positive hallucinations on POPE are still valuable for one-forward internal-signal analysis

## 9. Recommendation

Recommended next step:

1. do not spend more time squeezing POPE score from this exact faithful FLB-style baseline
2. keep this result as an important negative baseline:
   - `faithful later-step first-logit reuse is ineffective on one-word POPE`
3. move to the planned one-forward signal audit / first-answer decision analysis
4. if later returning to intervention design, focus on:
   - first-answer token decision
   - pre-answer hidden / logit state
   - early-anchor signals that can actually influence the first answer boundary
5. do not continue tuning `first_logit` on POPE:
   - no `The effect`
   - no parameter sweep for score chasing
   - no further POPE-only baseline optimization
