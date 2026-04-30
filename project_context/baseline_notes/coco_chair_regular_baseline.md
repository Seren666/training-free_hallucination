# COCO-CHAIR Regular Baseline

> Date: 2026-04-30
> Scope: remote-only regular caption baseline preparation for open-ended object hallucination evaluation after the completed POPE `first_logit` result.
> Boundary:
> - no local raw caption sync
> - no baseline repo clone
> - no new model download
> - no new method implementation
> - no `first_logit` caption intervention in this round

## 1. Why Add COCO-CHAIR

The completed POPE result established a narrow but important conclusion:

- POPE is good for `answer-boundary` and `pre-answer` signal audit
- POPE is not suitable for evaluating faithful later-step `first_logit` intervention under one-word yes/no decoding

So the benchmark split now becomes:

- `POPE`
  - answer-boundary signal audit
  - first-answer / pre-answer analysis
  - false-positive hallucination inspection
- `COCO-CHAIR`
  - open-ended caption hallucination evaluation
  - generative object hallucination behavior
  - later-step intervention testing space

## 2. Remote Setup

### Core paths

- COCO val images:
  - `/root/autodl-tmp/code/VCD/experiments/data/coco/val2014`
- LLaVA checkpoint:
  - `/root/autodl-tmp/code/VCD/experiments/checkpoints/llava-v1.5-7b`
- vision tower local snapshot:
  - `/root/autodl-tmp/hf-home/hub/models--openai--clip-vit-large-patch14-336/snapshots/ce19dc912ca5cd21c8a653c79e251e808ccabcd1`
- remote probe workspace:
  - `/root/autodl-tmp/code/training_free_hallucination_probe`

### Downloaded to remote only

- COCO annotations zip:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/resources/coco_annotations/annotations_trainval2014.zip`
- extracted annotation files:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/resources/coco_annotations/captions_train2014.json`
  - `/root/autodl-tmp/code/training_free_hallucination_probe/resources/coco_annotations/captions_val2014.json`
  - `/root/autodl-tmp/code/training_free_hallucination_probe/resources/coco_annotations/instances_train2014.json`
  - `/root/autodl-tmp/code/training_free_hallucination_probe/resources/coco_annotations/instances_val2014.json`
- CHAIR resources:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/resources/chair/chair.py`
  - `/root/autodl-tmp/code/training_free_hallucination_probe/resources/chair/misc.py`
  - `/root/autodl-tmp/code/training_free_hallucination_probe/resources/chair/data/synonyms.txt`

### Wrapper and evaluator

- caption wrapper:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/coco_caption_llava.py`
- evaluator:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/coco_chair_eval.py`

Important note:

- old VCD main code was **not** modified
- the checkpoint config was **not** permanently edited
- the vision tower path is overridden at runtime inside the wrapper

## 3. Caption Generation Protocol

Prompt:

- `Please describe the image.`

Decoding:

- greedy / deterministic
- batch size `1`
- `max_new_tokens = 64`
- no logits / attentions / hidden states saved
- no tensor dumps saved

## 4. CHAIR Evaluator Status

The public CHAIR code was useful as a logic reference, but it was not directly runnable as-is in the current environment because:

- the original script is Python2-style
- it depends on `nltk` and `pattern`
- the env does not currently have `pycocotools`, `pycocoevalcap`, `nltk`, `pattern`, or `language_evaluation`

So the current evaluator is:

- a remote-only adapted Python3 CHAIR-style evaluator
- based on the official CHAIR logic and official `synonyms.txt`
- limited to lightweight metrics needed for current baseline work

This should be described as:

- `adapted CHAIR-style evaluator`
- not an untouched official script run

## 5. Runs Completed

### 10-image sanity

Success:

- image loading worked
- caption generation worked
- runtime vision tower override worked
- output format was stable
- CHAIR-style evaluation ran successfully
- peak reserved GPU memory stayed around `14.04 GB`

Remote raw output:

- `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/coco_chair/regular_caption_10.json`

Remote eval summary:

- `/root/autodl-tmp/code/training_free_hallucination_probe/results/coco_chair_regular_eval_10.json`

### 100-image pilot

Success:

- the same wrapper stayed stable for `100` images
- no path mismatch was observed
- no GPU OOM occurred
- peak reserved GPU memory stayed around `14.04 GB`

Remote raw output:

- `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/coco_chair/regular_caption_100.json`

Remote eval summary:

- `/root/autodl-tmp/code/training_free_hallucination_probe/results/coco_chair_regular_eval_100.json`

## 6. CHAIR Metrics

Remote aggregate metrics:

- `/root/autodl-tmp/code/training_free_hallucination_probe/results/coco_chair_regular_metrics.csv`
- `/root/autodl-tmp/code/training_free_hallucination_probe/results/coco_chair_regular_metrics.md`

Table: regular caption baseline

| Method | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Object Count | s/sample |
|---|---:|---:|---:|---:|---:|---:|---:|
| regular | 10 | 0.2000 | 0.0789 | 47.5000 | 38 | 3 | 1.3162 |
| regular | 100 | 0.2100 | 0.0533 | 49.9100 | 450 | 24 | 1.2993 |

## 7. Early Behavior Notes

The current pilot already shows that:

- caption-side hallucination evaluation is operational on the remote machine
- the benchmark captures object over-mentioning that POPE cannot expose under one-word yes/no output
- the regular captions are fairly verbose under the current prompt and token budget

Examples seen in the 100-image pilot include hallucinated mentions such as:

- `sports ball`
- `dining table`
- `handbag`
- `sink`
- `bench`

This is exactly the kind of caption-side object mention behavior that makes COCO-CHAIR complementary to POPE.

## 8. Current Risks

- the current evaluator is adapted rather than the untouched official script
- some captions approach the `max_new_tokens` limit and can truncate
- prompt style may affect caption length and thus hallucination counts
- the current metrics are only from `10` and `100` image pilot runs, not full COCO evaluation

## 9. Recommendation

Recommended next step:

1. keep POPE for one-forward signal audit
2. keep the current COCO-CHAIR regular pipeline fixed as the caption baseline
3. if intervention work starts next, test `first-logit / early-anchor` on this caption benchmark rather than returning to POPE score tuning
4. AMBER should stay later priority until COCO-CHAIR is used more fully
