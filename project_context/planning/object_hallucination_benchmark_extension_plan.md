# Object Hallucination Benchmark Extension Plan

> Date: 2026-04-30
> Scope: decide and prepare the first generative object-hallucination benchmark after the completed POPE `first_logit` result.
> Current conclusion:
> - do not continue POPE `first_logit` tuning
> - keep POPE for one-forward answer-boundary / false-positive signal audit
> - use `COCO caption + CHAIR` as the first generative benchmark extension

## 1. Why We Need A Second Benchmark

The completed POPE result already answers one important question:

- POPE is useful for `answer-boundary` and `pre-answer` signal audit
- POPE is not useful for evaluating a faithful `later-step first-logit` intervention under one-word yes/no decoding

So the benchmark split should now be:

- `POPE`
  - one-forward signal audit
  - first-answer decision analysis
  - false-positive hallucination inspection
- `new generative benchmark`
  - evaluate whether later-step or caption-level interventions can matter once generation is longer than a single yes/no token

## 2. Candidate Comparison

## 2.1 Option A: AMBER

### What it is

AMBER is a more recent MLLM hallucination benchmark with both:

- generative hallucination evaluation
- discriminative yes/no-style evaluation

The public project materials explicitly position it as an `LLM-free` hallucination benchmark, which is attractive for reproducible evaluation.

### Fit for our current question

Pros:

- directly targets MLLM hallucination
- includes a generative setting, so it is much better than POPE for testing whether later-step interventions can change output behavior
- evaluator is not tied to a paid GPT judge
- conceptually closer to a true `object hallucination generation` benchmark than POPE

Cons:

- remote check found no AMBER data or evaluator already present
- moving to AMBER would require downloading new benchmark resources later
- we have not found an already wired LLaVA-1.5 AMBER entry in the current remote workspace
- relative to COCO-CHAIR, it has higher setup uncertainty for the current repo

### LLaVA-1.5 integration difficulty

Current judgment:

- moderate
- likely feasible through a lightweight remote wrapper
- but not as frictionless as reusing existing COCO images

### Need new data?

- yes
- AMBER resources are not currently present on the checked remote paths

### Suitability for first-logit / early-anchor intervention benchmark

- yes, especially for the generative part
- because generation length is longer than POPE and gives later-step intervention some room to matter

## 2.2 Option B: COCO caption + CHAIR

### What it is

This option uses:

- standard image caption generation on COCO images
- CHAIR-style hallucination evaluation against COCO object annotations

This is the classic caption-side object hallucination benchmark family and is strongly complementary to POPE.

### Fit for our current question

Pros:

- directly tests generative object hallucination
- naturally gives later tokens room to matter
- conceptually clean complement to POPE:
  - POPE asks `is object X present?`
  - CHAIR asks `what objects does the model mention while captioning?`
- COCO `val2014` images already exist remotely
- no new image download is needed

Cons:

- the original public CHAIR script is Python2-style and not directly runnable in the current env
- the current env does not have `pycocotools`, `pycocoevalcap`, `nltk`, `pattern`, or `language_evaluation`
- caption prompting choices can affect caption style and hallucination rate

### LLaVA-1.5 integration difficulty

Current judgment:

- low to moderate
- a custom wrapper is needed
- but the current remote probe infrastructure already proved that:
  - offline LLaVA-1.5 loading works
  - runtime vision-tower override works
  - custom prompt wrappers are straightforward

### Need new data?

- not new images
- only lightweight annotation/evaluator assets on the remote machine:
  - COCO caption annotations
  - COCO instance annotations
  - CHAIR resources such as `synonyms.txt`

### Suitability for first-logit / early-anchor intervention benchmark

- very good
- caption generation is longer and more generation-sensitive than POPE
- this is the cleanest immediate test of whether later-step intervention has any real object-hallucination leverage

### Complementarity with POPE

Very strong:

- `POPE` stays as the answer-boundary benchmark
- `COCO-CHAIR` becomes the caption-generation benchmark
- together they separate:
  - binary decision hallucination
  - open-ended object mention hallucination

## 2.3 Option C: MMHal-Bench

### What it is

MMHal-Bench is a broader hallucination benchmark for multimodal models, but its standard headline evaluation is tied to a strong LLM judge.

### Fit for our current question

Pros:

- useful later as a small broader hallucination sanity check
- can serve as a downstream generalization check after we already have a clearer object-hallucination mechanism story

Cons:

- not object-hallucination-specific enough for the immediate next step
- standard evaluation is judge-dependent rather than fully lightweight and local
- less attractive than CHAIR or AMBER for the current mechanism-focused phase

### Priority

- not first priority

## 3. Current COCO-CHAIR Status

### Remote resources now present

Confirmed present:

- COCO val images:
  - `/root/autodl-tmp/code/VCD/experiments/data/coco/val2014`
- existing LLaVA-1.5 checkpoint:
  - `/root/autodl-tmp/code/VCD/experiments/checkpoints/llava-v1.5-7b`
- remote probe workspace:
  - `/root/autodl-tmp/code/training_free_hallucination_probe`
- remaining remote disk:
  - about `160G` free under `/root/autodl-tmp`

Downloaded to the remote machine only:

- COCO annotations zip:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/resources/coco_annotations/annotations_trainval2014.zip`
- extracted annotation jsons:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/resources/coco_annotations/captions_train2014.json`
  - `/root/autodl-tmp/code/training_free_hallucination_probe/resources/coco_annotations/captions_val2014.json`
  - `/root/autodl-tmp/code/training_free_hallucination_probe/resources/coco_annotations/instances_train2014.json`
  - `/root/autodl-tmp/code/training_free_hallucination_probe/resources/coco_annotations/instances_val2014.json`
- CHAIR resources:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/resources/chair/chair.py`
  - `/root/autodl-tmp/code/training_free_hallucination_probe/resources/chair/misc.py`
  - `/root/autodl-tmp/code/training_free_hallucination_probe/resources/chair/data/synonyms.txt`

Still not installed in env:

- `pycocotools`
- `pycocoevalcap`
- `nltk`
- `pattern`
- `language_evaluation`

This is acceptable for the current phase because the pilot uses a remote-only adapted evaluator instead of the original Python2 + dependency-heavy script.

### Remote wrappers now present

Remote-only scripts added in the probe workspace:

- caption wrapper:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/coco_caption_llava.py`
- adapted evaluator:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/coco_chair_eval.py`

Important boundary:

- old VCD main code was not modified
- the LLaVA checkpoint config was not permanently edited
- the vision tower path is overridden at runtime to:
  - `/root/autodl-tmp/hf-home/hub/models--openai--clip-vit-large-patch14-336/snapshots/ce19dc912ca5cd21c8a653c79e251e808ccabcd1`

## 4. Current Pilot Result

Caption setting:

- prompt:
  - `Please describe the image.`
- decoding:
  - greedy / deterministic
- batch size:
  - `1`
- max new tokens:
  - `64`

Remote raw caption outputs:

- 10-image sanity:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/coco_chair/regular_caption_10.json`
- 100-image pilot:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/coco_chair/regular_caption_100.json`

Remote metrics:

- per-run eval summaries:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/coco_chair_regular_eval_10.json`
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/coco_chair_regular_eval_100.json`
- aggregate metrics:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/coco_chair_regular_metrics.csv`
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/coco_chair_regular_metrics.md`

Pilot metrics:

| Method | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Object Count | s/sample |
|---|---:|---:|---:|---:|---:|---:|---:|
| regular | 10 | 0.2000 | 0.0789 | 47.5000 | 38 | 3 | 1.3162 |
| regular | 100 | 0.2100 | 0.0533 | 49.9100 | 450 | 24 | 1.2993 |

What this means:

- the regular caption baseline now runs end-to-end on remote COCO images
- the current CHAIR-style evaluation path is usable for sanity and pilot benchmarking
- this benchmark now fills the open-ended generation gap left by POPE

## 5. Recommendation

### Recommended first added benchmark: COCO caption + CHAIR

This recommendation is now stronger than before because the remote pilot already succeeded.

Why it should stay first:

1. it is the lowest-friction generative benchmark extension from the current state
2. COCO images are already present remotely
3. the annotation/evaluator gap is now resolved at pilot level
4. it directly targets open-ended object hallucination
5. it complements POPE very cleanly

### Recommended role split

- `POPE`
  - one-forward answer-boundary signal audit
  - first-answer / pre-answer signal study
  - false-positive hallucination analysis
- `COCO-CHAIR`
  - generative object hallucination benchmark
  - later-step intervention evaluation
  - caption-level object hallucination behavior

### AMBER recommendation

AMBER remains the second generative benchmark, not the first.

Reason:

- COCO-CHAIR is already partially operational
- AMBER still has a setup gap on the remote machine
- there is no need to split effort before using the cheaper benchmark extension first

### MMHal-Bench recommendation

- keep as a later small-scale general hallucination check
- not first priority

## 6. Main Risks

For COCO-CHAIR:

- the current evaluator is an adapted Python3 CHAIR-style implementation, not the untouched original script
- some captions are long and can approach the current `max_new_tokens` limit
- caption prompt and stopping behavior may affect style and hallucination rate
- CHAIR remains COCO-object-vocabulary-bound rather than fully open-vocabulary

For AMBER:

- setup cost is still higher from the current workspace
- no remote AMBER assets are present yet
- evaluation protocol still needs careful alignment before use

## 7. Practical Next Step

Recommended next move:

1. keep POPE fixed as the one-forward signal-audit benchmark
2. do **not** keep tuning later-step `first_logit` on POPE
3. keep the current COCO-CHAIR regular prompt/decoding fixed
4. if we want intervention evaluation next, use this COCO-CHAIR pipeline before touching AMBER
5. begin with small caption-side intervention checks, not full benchmark expansion

## 8. Sources

- AMBER repo: [junyangwang0410/AMBER](https://github.com/junyangwang0410/AMBER)
- AMBER paper page: [AMBER: An LLM-free Multi-dimensional Benchmark for MLLMs Hallucination Evaluation](https://huggingface.co/papers/2311.07397)
- MMHal-Bench dataset page: [Shengcao1006/MMHal-Bench](https://huggingface.co/datasets/Shengcao1006/MMHal-Bench)
- CHAIR original repo: [LisaAnne/Hallucination](https://github.com/LisaAnne/Hallucination)
