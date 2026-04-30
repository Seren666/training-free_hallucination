# Remote Dry Run Report

> Scope: remote FLB dry check / one-forward audit preparation only.
> Date: 2026-04-30 (remote instance time during verification)
> Boundary reminder:
> - no formal experiment
> - no baseline clone
> - no model or dataset download
> - no full-POPE evaluation
> - no large tensor or output artifact saved back to the Git repo

## 1. Git push status

- local `main` already contains:
  - `11eb564 docs: record delete status and dry check plan`
- pre-checks run:
  - `git status`
  - `git log --oneline main -3`
- `git push origin main` was retried 2 times in this round and still failed

Observed errors:

- attempt 1: `Recv failure: Connection was reset`
- attempt 2: `Failed to connect to github.com port 443 after 21125 ms: Could not connect to server`

Current judgment:

- local lightweight docs are committed on `main`
- GitHub push is still blocked by network connectivity, not by repo content

## 2. Remote GPU / system quick re-check

Remote instance:

- host: `connect.westb.seetacloud.com`
- port: `31048`
- user: `root`
- container hostname: `autodl-container-3n631bugr0-97c149e4`

Quick environment snapshot:

- GPU: `NVIDIA GeForce RTX 4090`
- VRAM: `49140 MiB`
- driver: `580.105.08`
- CUDA reported by driver: `13.0`
- PyTorch: `2.0.1+cu118`
- `torch.cuda.is_available()`: `True`
- `torch.cuda.device_count()`: `1`
- current idle allocation at check time:
  - allocated: `0.0 GB`
  - reserved: `0.0 GB`

System resources at re-check:

- `/`: about `27G` available
- `/usr/bin/nvidia-smi` backing disk: about `400G` available
- RAM available: about `630 GiB`

## 3. Conda / PYTHONPATH status

Confirmed working commands:

```bash
source /root/miniconda3/etc/profile.d/conda.sh
conda activate /root/autodl-tmp/envs/vcd
export PYTHONPATH=/root/autodl-tmp/code/VCD/experiments:/root/autodl-tmp/code/VCD:${PYTHONPATH}
```

Status:

- `conda activate /root/autodl-tmp/envs/vcd`: success
- repo-aware `PYTHONPATH`: required and working
- `import llava`: success with the documented `PYTHONPATH`
- `import vcd_utils.vcd_sample`: success with the documented `PYTHONPATH`

## 4. Script-level dry check result

Checked successfully:

- `object_hallucination_vqa_llava.py` import: success
- `object_hallucination_vqa_llava.py --help`: success
- `eval_pope.py --help`: success
- `bash -n experiments/cd_scripts/llava1.5_pope.bash`: success
- LLaVA/VCD module imports: success

Important finding:

- the old codebase is importable
- the main loader path is not the blocker
- the main blocker was later found in model loading under offline HF resolution

## 5. POPE single-sample selection

Selected sample:

- annotation file:
  - `/root/autodl-tmp/code/VCD/experiments/data/POPE/coco/coco_pope_random.json`
- `question_id`: `1`
- question:
  - `Is there a snowboard in the image?`
- label:
  - `yes`
- image file:
  - `COCO_val2014_000000310196.jpg`
- image path:
  - `/root/autodl-tmp/code/VCD/experiments/data/coco/val2014/COCO_val2014_000000310196.jpg`
- image exists:
  - `True`

No annotation file was modified.
No formal output file was created.

## 6. Model-loading blocker and dry-run workaround

### Stock loading failure

Direct stock loading through the usual checkpoint path failed before generation because:

- checkpoint config uses:
  - `mm_vision_tower = openai/clip-vit-large-patch14-336`
- the current instance cannot reach `huggingface.co`
- `transformers` could not resolve that repo id through the normal offline path on this instance

Representative failure surface:

- failed while resolving `openai/clip-vit-large-patch14-336/config.json`
- raised an offline / connection error before ordinary generation began

### Verified workaround

A local vision-tower snapshot already exists on the remote machine:

- `/root/autodl-tmp/hf-home/hub/models--openai--clip-vit-large-patch14-336/snapshots/ce19dc912ca5cd21c8a653c79e251e808ccabcd1`

Verified workaround:

- load the LLaVA checkpoint locally
- patch `cfg.mm_vision_tower` at runtime to the local snapshot path
- then load the vision tower from that local snapshot only

This workaround succeeded without downloading anything.

## 7. Step 5: single-sample no-save forward dry run

Dry-run path:

- manual local-only checkpoint load
- single POPE sample
- no VCD
- no FLB
- no output file
- no full evaluation

Prompt used:

- same LLaVA chat-style prompt template as the old eval path
- appended instruction:
  - `Please answer this question with one word.`

Observed prompt/input stats:

- `input_ids_shape`: `(1, 60)`
- `image_tensor_shape`: `(1, 3, 336, 336)`
- image placeholder position in tokenized prompt:
  - `[35]`
- expanded multimodal prompt length:
  - `635`
- inferred visual token count:
  - `576`
- inferred image token range:
  - `[35, 610]`
- first answer token position:
  - `635`

Generation result:

- generated answer:
  - `Yes`
- generated token ids:
  - `[3869, 2]`
- first-step logits shape:
  - `(1, 32000)`

First-token top-k logits:

- `Yes`: `26.4062`
- `No`: `25.7656`
- `There`: `15.3828`
- `no`: `14.2812`
- `Y`: `14.2031`

Peak memory during Step 5:

- `13.8941 GB`

Judgment:

- ordinary single-sample forward/generation path is working

## 8. Step 6: attentions / hidden_states dry run

Run setting:

- same single POPE sample
- `max_new_tokens=1`
- `output_attentions=True`
- `output_hidden_states=True`
- no tensor dump saved
- only aggregated statistics inspected

Observed structure:

- `len(attentions) = 1`
- `len(hidden_states) = 1`
- attention layer count:
  - `32`
- head count:
  - `32`
- attention tensor shape:
  - first layer: `(1, 32, 635, 635)`
  - last layer: `(1, 32, 635, 635)`
- hidden-state entry count:
  - `33`
- hidden-state tensor shape:
  - first entry: `(1, 635, 4096)`
  - last entry: `(1, 635, 4096)`

Important interpretation:

- the returned attention/hidden-state tensors correspond to the prompt-prefill forward
- therefore the most meaningful query position for first-answer analysis is the last prompt position
- that pre-answer prompt position is:
  - `634`
- the first generated answer token would be at:
  - `635`

Image-token localization:

- image token range is locatable:
  - `[35, 610]`
- answer token position is locatable:
  - first answer token position `635`
- pre-answer query position is locatable:
  - `634`

Simple image-token attention mass using the pre-answer query position:

- mean across layers:
  - `0.10405254364013672`
- first layer:
  - `0.6611328125`
- middle layer:
  - `0.0684814453125`
- last layer:
  - `0.1312255859375`

Step-6 first-token top-k remained readable and matched Step 5:

- `Yes`: `26.4062`
- `No`: `25.7656`
- `There`: `15.3828`

Peak memory during Step 6:

- `14.5664 GB`

Judgment:

- attentions are readable
- hidden states are readable
- layer/head dimensions are readable
- image-token / answer-token indexing is recoverable

## 9. Can we enter the minimal one-forward signal audit stage?

Yes, with one caveat.

What is already confirmed:

- remote GPU environment is healthy
- single-sample normal forward works
- first-token logits are readable
- prompt-prefill attentions and hidden states are readable
- image-token range is recoverable
- pre-answer / answer-token positions are recoverable
- peak memory is comfortably below 49 GB for this single-sample setting

Main caveat:

- stock checkpoint loading is not robust in the current offline environment unless the vision tower path is normalized to the local snapshot

## 10. Do we need an independent probe script?

Recommended: yes, a lightweight remote-only probe script is worth writing before broader audit runs.

Reason:

- not because one-forward audit is impossible
- but because the current reliable path uses a runtime patch for `mm_vision_tower`
- and because a small dedicated probe can keep the next audit cleaner than reusing the full old VCD eval entry

Suggested scope for that probe:

- single-sample input only
- no output file writing by default
- explicit local vision snapshot path handling
- optional flags for:
  - `output_scores`
  - `output_attentions`
  - `output_hidden_states`
- only aggregate-stat output

## 11. Current blockers

Primary blocker:

- stock offline model loading still fails unless the vision tower is redirected to the existing local snapshot path

Secondary blocker:

- GitHub push from the local machine is still failing due network connectivity to `github.com`

Not blockers at this stage:

- GPU memory
- POPE image path
- checkpoint existence
- LLaVA/VCD imports
- one-sample no-save generation

## 12. Recommendation for the next step

Recommended next step:

1. write a lightweight remote-only probe script or wrapper for the patched local vision-tower load path
2. keep it single-sample and aggregate-only
3. start the minimal one-forward signal audit with:
   - first-token logits
   - pre-answer prompt hidden state
   - pre-answer prompt attention to image tokens
   - layer-wise summary statistics

Not recommended yet:

- full POPE run
- formal FLB reproduction
- baseline cloning
- any output-heavy trace collection
