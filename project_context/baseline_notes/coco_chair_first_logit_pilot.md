# COCO-CHAIR First-Logit Pilot

> Date: 2026-04-30
> Scope: small paired `regular` vs `first_logit / early-anchor` caption pilot on the same COCO-CHAIR 100-image subset.
> Boundary:
> - no full benchmark
> - no parameter sweep
> - no `The effect`
> - no old VCD code modification
> - no local raw caption sync

## 1. Paired Setup

This pilot reused the exact same 100-image subset as the completed regular caption pilot.

Paired controls:

- same image ids:
  - recovered directly from `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/coco_chair/regular_caption_100.json`
- same prompt:
  - `Please describe the image.`
- same `max_new_tokens`:
  - `64`
- same decoding base:
  - greedy / deterministic
- same seed:
  - `55`
- same model:
  - `/root/autodl-tmp/code/VCD/experiments/checkpoints/llava-v1.5-7b`
- same vision tower local snapshot:
  - `/root/autodl-tmp/hf-home/hub/models--openai--clip-vit-large-patch14-336/snapshots/ce19dc912ca5cd21c8a653c79e251e808ccabcd1`

Only the `first_logit / early-anchor` intervention was changed.

## 2. Intervention Type

This is best described as:

- a `faithful later-step first-logit adaptation`
- not an official public `COCO-CHAIR` script reproduction
- not a claim of official FLB benchmark reproduction on captioning

What was done:

- the first-logit anchor was extracted at step `0`
  - specifically, from the normal forward on the image-conditioned caption prompt, before any caption token was generated
- that step-0 next-token logit distribution was stored as the `early anchor`
- for later decode steps only, the script reused the same recurrence already used in the earlier POPE pilot:
  - `weight_t = gamma * (1 - exp(-lambda * step))`
  - `adjusted_logits = current_logits + weight_t * first_anchor_logits`
  - a plausibility mask was applied using the current-step logits and `cd_beta`

Important implementation boundaries:

- it acted on the full token vocabulary
- it acted on later generation steps only
- it did **not** modify the first generated token
- it did **not** use any extra forward
- it did **not** use `The effect`
- it did **not** train any classifier

Fixed pilot coefficients:

- `flb_gamma = 0.3`
- `flb_lambda = 0.05`
- `cd_beta = 0.1`

Source of these defaults:

- reused from the earlier POPE `first_logit` adaptation based on the inspected released FLB-style recurrence
- no new sweep was run here

## 3. Remote Outputs

Remote first-logit caption outputs:

- 10-image sanity:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/coco_chair/first_logit_caption_10.json`
- 100-image paired pilot:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/coco_chair/first_logit_caption_100.json`

Remote evaluation outputs:

- `/root/autodl-tmp/code/training_free_hallucination_probe/results/coco_chair_first_logit_eval_10.json`
- `/root/autodl-tmp/code/training_free_hallucination_probe/results/coco_chair_first_logit_eval_100.json`
- `/root/autodl-tmp/code/training_free_hallucination_probe/results/coco_chair_first_logit_metrics.csv`
- `/root/autodl-tmp/code/training_free_hallucination_probe/results/coco_chair_first_logit_metrics.md`

## 4. Sanity Result

10-image sanity succeeded:

- caption generation worked
- CHAIR-style evaluator worked
- no empty-caption failure was observed
- no GPU OOM occurred
- peak reserved GPU memory stayed around `14.04 GB`

Small-sample note:

- the 10-image run was slightly worse than regular
- so the 100-image paired pilot was necessary before drawing conclusions

## 5. Main Paired Result

Table 1: Main metrics

| Method | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Object Count | s/sample |
|---|---:|---:|---:|---:|---:|---:|---:|
| regular | 100 | 0.2100 | 0.0533 | 49.9100 | 450 | 24 | 1.2993 |
| first_logit | 100 | 0.1500 | 0.0465 | 51.3100 | 452 | 21 | 1.2961 |

Table 2: Delta vs regular

| CHAIRs delta | CHAIRi delta | Avg Caption Length delta | Object Mentions delta | Hallucinated Object Count delta | s/sample delta |
|---:|---:|---:|---:|---:|---:|
| -0.0600 | -0.0068 | 1.4000 | 2 | -3 | -0.0032 |

## 6. Behavior Summary

Table 3: Behavior summary

| Item | Value |
|---|---:|
| changed caption count | 100 |
| unchanged caption count | 0 |
| same first word count | 100 |
| improved image count | 14 |
| worsened image count | 10 |
| same hallucination-count image count | 76 |

Interpretation:

- `first_logit` did change captions
- it changed all `100/100` captions
- it did **not** change the first generated word in this paired subset
- overall object mentions did **not** go down
  - they rose slightly from `450` to `452`
- average caption length did **not** shrink
  - it rose from `49.91` to `51.31`
- hallucinated object count dropped from `24` to `21`

So the pilot improvement is **not** explained by simply making captions shorter or mentioning fewer objects.

## 7. Improved Examples

### Image 74

- regular hallucination:
  - `handbag`
- regular caption:
  - `The image features a white dog lying on a sidewalk, resting comfortably on the ground. The dog is positioned near a bicycle, which is leaning against a wall. The scene also includes several people walking by, with some of them carrying handbags.`
- first-logit caption:
  - `The image features a white dog lying on the sidewalk in a city street. The dog is resting on the sidewalk near a bicycle, which is parked on the left side of the scene. The street is lined with a variety of people walking in the background, creating a lively atmosphere.`
- outcome:
  - hallucination count `1 -> 0`

### Image 241

- regular hallucination:
  - `chair`
- regular caption:
  - `The image depicts a group of people gathered in a living room, enjoying a video game session on a Nintendo Wii console. A man is standing in the center of the room, holding a Wii remote, while others are sitting on couches and chairs around him.`
- first-logit caption:
  - `The image depicts a group of people gathered in a living room, enjoying a video game session on a Nintendo Wii console. A man in a plaid shirt is standing in the center of the room, holding a Wii remote in his hand, while the others watch and engage in the`
- outcome:
  - hallucination count `1 -> 0`

### Image 257

- regular hallucination:
  - `car`
- regular caption:
  - `The image depicts a busy city street with a large group of people gathered around a food truck. The food truck is parked in front of a monument, and there are several other trucks and cars in the vicinity.`
- first-logit caption:
  - `The image depicts a busy city street with a large group of people gathered around a food truck. The truck is parked in the middle of the scene, and the people are standing in a line, waiting to be served.`
- outcome:
  - hallucination count `1 -> 0`

## 8. Worsened Examples

### Image 139

- regular hallucination count:
  - `0`
- first-logit hallucination:
  - `couch`
- regular caption:
  - `The image depicts a spacious and well-lit living room with a dining area. A woman is standing in the dining area, which features a dining table surrounded by chairs.`
- first-logit caption:
  - `The image depicts a spacious and well-lit living room with a dining area. The dining table is surrounded by several chairs, and the room features a TV on the left side. The living room is furnished with a couch and a potted plant, and the space is bright`
- outcome:
  - hallucination count `0 -> 1`

### Image 164

- regular hallucination count:
  - `0`
- first-logit hallucination:
  - `sink`
- regular caption:
  - `The image depicts a small, cluttered kitchen with a white refrigerator and a microwave oven. The kitchen is filled with various items, including numerous bottles, cups, and bowls.`
- first-logit caption:
  - `The image depicts a small, cluttered kitchen with a white refrigerator and a microwave oven. The kitchen is filled with various items, including a dining table, a chair, and a sink.`
- outcome:
  - hallucination count `0 -> 1`

### Image 294

- regular hallucination count:
  - `0`
- first-logit hallucinations:
  - `toaster`, `sink`
- regular caption:
  - `The image features a man standing in a kitchen, holding a frying pan in his hand. He is positioned in front of a wall with various pots and pans hanging on it.`
- first-logit caption:
  - `The image features a man standing in a kitchen, holding a frying pan in his hand. The kitchen is well-equipped with a variety of utensils and cooking tools, including a microwave, a toaster, and a sink.`
- outcome:
  - hallucination count `0 -> 2`

## 9. Unchanged Cases

Exact unchanged captions:

- none
- `changed caption count = 100`
- `unchanged caption count = 0`

Because there are no exact unchanged captions in this paired pilot, the closest stable cases are `no-delta hallucination` examples where caption wording changed but CHAIR outcome did not:

### Image 42

- regular caption:
  - `The image features a dog lying on a shelf, surrounded by various shoes. The dog is curled up and appears to be sleeping or resting comfortably.`
- first-logit caption:
  - `The image features a dog lying on a shelf, surrounded by various shoes. The dog is in the center of the scene, with the shoes placed in a pile around it.`
- outcome:
  - hallucination count stayed `0`

### Image 73

- regular caption:
  - `The image features an old-fashioned motorcycle parked on a street. The motorcycle is positioned in the center of the scene, with its front wheel prominently visible.`
- first-logit caption:
  - `The image features an old-fashioned motorcycle parked on the side of the road. The motorcycle is the main focus of the scene, and it is parked in the foreground.`
- outcome:
  - hallucination count stayed `0`

### Image 133

- regular caption:
  - `The image features a bedroom with a neatly made bed, positioned against the wall. The bed is covered with a white sheet and has a wooden headboard.`
- first-logit caption:
  - `The image features a bedroom with a neatly made bed, positioned in the corner of the room. The bed is the main focus of the scene, and it is the only bed in the room.`
- outcome:
  - hallucination count stayed `0`

## 10. Verdict

The pilot gives a real positive signal:

- `CHAIRs` improved
- `CHAIRi` improved
- caption length did not collapse
- object mentions did not collapse
- captions really changed

At the same time, there are cautions:

- all `100/100` captions changed
- the mechanism is not selective
- there are clear worsened cases

## 11. Recommendation

Current recommendation:

1. do **not** tune parameters on this 100-image result
2. do **not** introduce `The effect`
3. one fixed-config expansion to `500` images is justified
   - only as a confirmation run
   - only with the same configuration
4. if the `500`-image result does not preserve the gain, stop this intervention direction and return to one-forward signal audit

So the present answer is:

- suggest a cautious `500`-image confirmation run: `yes`
- suggest unrestricted continuation or sweep: `no`
