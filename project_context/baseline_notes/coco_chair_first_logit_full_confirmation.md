# COCO-CHAIR First-Logit Full Confirmation

> Date: 2026-04-30
> Status at report time:
> - `500` and `1000` paired stages completed
> - `full` stage launched and still running on the remote GPU instance
> - this document records the confirmed intermediate trend and the exact full-run setup

## 1. Why Full Confirmation

The 100-image paired pilot gave a real positive signal:

- `regular` vs `first_logit` showed lower `CHAIRs` and `CHAIRi`
- caption length did not collapse
- object mentions did not collapse
- the mechanism did not use `The effect`

That was enough to justify moving beyond a small pilot, but not enough to support a strong claim.

So the current goal is:

- keep the fixed `first_logit / early-anchor` configuration
- launch the full paired confirmation once
- automatically materialize `500 / 1000 / full` metrics during the same long run

## 2. Method Setting

Current method should still be described as:

- `faithful later-step first-logit adaptation`
- not official COCO-CHAIR reproduction from a public FLB script
- not a new training-based method

Fixed configuration:

- `gamma = 0.3`
- `lambda = 0.05`
- `cd_beta = 0.1`
- step-0 image-conditioned first-logit anchor
- later-step full-vocabulary logit adjustment
- first generated token unchanged
- `The effect` not used

Prompt and decoding:

- prompt:
  - `Please describe the image.`
- decoding:
  - greedy / deterministic
- `max_new_tokens = 64`
- same seed:
  - `55`

## 3. Dataset / Image Count

Full confirmation image list:

- full image count:
  - `40504`
- source:
  - image ids from `captions_val2014.json`
  - intersected with existing files under `/root/autodl-tmp/code/VCD/experiments/data/coco/val2014`
- ordering:
  - ascending standard COCO `val2014` image-id order

Compatibility with the 100-image pilot:

- yes
- the first 100 image ids in the full list exactly match the previous pilot prefix:
  - `42, 73, 74, 133, 136, 139, 143, 164, 192, 196, ...`

Remote full image list:

- `/root/autodl-tmp/code/training_free_hallucination_probe/resources/coco_annotations/coco_val2014_full_image_list.json`

## 4. Run Status

Remote full pipeline launcher:

- `/root/autodl-tmp/code/training_free_hallucination_probe/run_coco_chair_full_confirmation.sh`

Remote resumable runner:

- `/root/autodl-tmp/code/training_free_hallucination_probe/coco_caption_resumable.py`

Remote paired report generator:

- `/root/autodl-tmp/code/training_free_hallucination_probe/coco_chair_paired_report.py`

Remote log:

- `/root/autodl-tmp/code/training_free_hallucination_probe/logs/coco_chair_full_confirmation.log`

Runtime state at report time:

- `500` paired stage completed
- `1000` paired stage completed
- `full regular` stage is now running
- `full first_logit` has not started yet because the pipeline is sequential on a single GPU

## 5. 500 / 1000 Trend Table

Table 1: Main metrics

| Stage | Method | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Object Count | s/sample |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 500 | regular | 500 | 0.1880 | 0.0561 | 49.8000 | 2280 | 128 | 1.2973 |
| 500 | first_logit | 500 | 0.1440 | 0.0429 | 51.0380 | 2356 | 101 | 1.3002 |
| 1000 | regular | 1000 | 0.2090 | 0.0657 | 49.6580 | 4522 | 297 | 1.3092 |
| 1000 | first_logit | 1000 | 0.1610 | 0.0509 | 50.9190 | 4717 | 240 | 1.3110 |

Current trend:

- the gain seen at 100 images persists at 500
- it also persists at 1000
- the improvement is not washed out by the larger prefix

## 6. Delta Table

Table 2: Delta vs regular

| Stage | CHAIRs delta | CHAIRi delta | Avg Caption Length delta | Object Mentions delta | Hallucinated Object Count delta | s/sample delta |
|---|---:|---:|---:|---:|---:|---:|
| 500 | -0.0440 | -0.0132 | 1.2380 | 76 | -27 | 0.0029 |
| 1000 | -0.0480 | -0.0148 | 1.2610 | 195 | -57 | 0.0018 |

## 7. Behavior Summary

Table 3: Behavior summary

| Stage | Changed | Unchanged | First Word Changed | Improved | Worsened | No-delta Stable |
|---|---:|---:|---:|---:|---:|---:|
| 500 | 500 | 0 | 0 | 58 | 33 | 409 |
| 1000 | 1000 | 0 | 0 | 130 | 80 | 790 |

Interpretation:

- captions change globally
- exact unchanged captions remain `0`
- the first word remains unchanged on all evaluated prefixes so far
- the direction is not selective in the strict sense
- but it does keep yielding more improved than worsened cases

## 8. Improved Examples

### Image 74

- regular hallucination:
  - `handbag`
- regular caption:
  - `The image features a white dog lying on a sidewalk, resting comfortably on the ground. The dog is positioned near a bicycle, which is leaning against a wall. The scene also includes several people walking by, with some of them carrying handbags.`
- first-logit caption:
  - `The image features a white dog lying on the sidewalk in a city street. The dog is resting on the sidewalk near a bicycle, which is parked on the left side of the scene. The street is lined with a variety of people walking in the background, creating a lively atmosphere.`
- outcome:
  - hallucination count `1 -> 0`

### Image 192

- regular hallucinations:
  - `baseball glove`, `sports ball`
- first-logit result:
  - reduced to only `sports ball`
- outcome:
  - hallucination count `2 -> 1`

### Image 241

- regular hallucination:
  - `chair`
- first-logit caption removes the extra furniture mention
- outcome:
  - hallucination count `1 -> 0`

### Image 257

- regular hallucination:
  - `car`
- first-logit caption stays focused on the food truck queue
- outcome:
  - hallucination count `1 -> 0`

### Image 357

- regular hallucination:
  - `sports ball`
- first-logit caption shifts toward player/action description
- outcome:
  - hallucination count `1 -> 0`

## 9. Worsened Examples

### Image 139

- regular hallucination count:
  - `0`
- first-logit introduces:
  - `couch`

### Image 164

- regular hallucination count:
  - `0`
- first-logit introduces:
  - `sink`

### Image 196

- regular hallucination count:
  - `0`
- first-logit introduces:
  - `knife`

### Image 294

- regular hallucination count:
  - `0`
- first-logit introduces:
  - `toaster`, `sink`

### Image 338

- regular hallucination count:
  - `0`
- first-logit introduces:
  - `sink`

## 10. No-Delta Stable Examples

There are still no exact unchanged captions, so the stable bucket means:

- caption wording changed
- CHAIR hallucination count did not change

Examples:

### Image 42

- both methods remain hallucination-free
- first-logit rewrites the description style but does not change CHAIR outcome

### Image 73

- both methods remain hallucination-free
- first-logit changes the framing from `on a street` to `on the side of the road`

### Image 133

- both methods remain hallucination-free
- first-logit makes the bed description more repetitive but does not create object hallucination

### Image 136

- both methods remain hallucination-free
- first-logit changes `eating hay` to `eating from a feeder`

### Image 143

- both methods remain hallucination-free
- first-logit changes the counting/style of bird description without changing CHAIR outcome

## 11. Is The Gain From Shorter Captions?

Current answer:

- no

Evidence:

- `500`: average caption length increases by `+1.2380`
- `1000`: average caption length increases by `+1.2610`

So the CHAIR gain is not explained by forcing shorter captions.

## 12. Do Object Mentions Decrease?

Current answer:

- no

Evidence:

- `500`: object mentions increase by `+76`
- `1000`: object mentions increase by `+195`

So the CHAIR gain is not explained by simply suppressing object mentions.

## 13. Does The First Word Stay Unchanged?

Current answer:

- yes, on all completed prefixes so far

Evidence:

- `500`: first word changed count `0`
- `1000`: first word changed count `0`

This remains consistent with the intended later-step-only adaptation.

## 14. Current Judgment

The direction still has positive evidence:

- `CHAIRs` improves at `100`, `500`, and `1000`
- `CHAIRi` improves at `100`, `500`, and `1000`
- captions do not get shorter
- object mentions do not decrease
- first token remains untouched

But caution is still necessary:

- the intervention changes all captions
- there are still clear worsened cases
- this is not yet a clean selective mechanism
- the `full` confirmation is still running, so the final conclusion is not available yet

## 15. Recommended Next Step

Current recommendation after the completed `500 / 1000` checkpoints:

1. let the full confirmation finish on the remote machine
2. if the `full` stage preserves the same direction, continue `first_logit / early-anchor` as a serious caption-side baseline
3. in parallel, keep planning the return to `one-forward signal audit`
4. after the full result, choose between:
   - stronger official CHAIR alignment
   - one-forward signal audit on caption-side false positives
   - method redesign if the full gain collapses

At this moment:

- continue `first_logit`: `yes`
- switch immediately away from it: `no`
- stop the full run: `no`

