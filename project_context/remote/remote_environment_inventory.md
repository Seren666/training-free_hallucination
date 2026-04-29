# Remote Environment Inventory

> Query date: 2026-04-29
> Source mix: direct SSH query to the current AutoDL instance plus path/provenance cross-checks from `project_context/legacy_handoff/legacy_environment/`.
> Important status note: the current AutoDL instance is running in no-GPU mode. The user confirmed that GPU capacity is insufficient on this instance; a cloned or upgraded GPU-enabled instance may be needed before formal experiments.

## 1. Remote entry

- host: `connect.westc.seetacloud.com`
- port: `21607`
- user: `root`
- current container hostname: `autodl-container-d82c46a42d-28053b02`
- legacy repo root that still exists remotely: `/root/autodl-tmp/code/VCD`

## 2. GPU status

Current query result:

- `nvidia-smi -L`: no devices found
- `nvidia-smi`: no devices were found
- active PyTorch environment also reports:
  - `torch.cuda.is_available() == False`
  - `torch.cuda.device_count() == 0`

Interpretation:

- this does not prove the project has no GPU access in general
- it only proves that the currently attached instance is a no-GPU instance at query time
- GPU model, GPU count, VRAM size, and GPU utilization are therefore unavailable from this instance

Follow-up requirement before real experiments:

- switch to a GPU-enabled instance, or
- clone/upgrade the current instance to a configuration with enough GPUs/VRAM

## 3. Disk space

Direct query snapshot:

- `/`: `30G` total, `4.0G` used, `27G` available
- `/root`: same overlay-backed capacity as above
- `/root/autodl-tmp`: `150G` total, `91G` used, `60G` available, `61%` used

Implication:

- there is still usable remote disk for lightweight code and notes
- large new baseline downloads should still be planned carefully

## 4. CUDA / Python / Conda

### Default shell environment

- `python` was not on the default non-activated shell path
- `nvcc` was not found on the default shell path

### Activated VCD environment

After:

```bash
source /root/miniconda3/etc/profile.d/conda.sh
conda activate /root/autodl-tmp/envs/vcd
```

Observed:

- Python: `3.9.25`
- Python path: `/root/autodl-tmp/envs/vcd/bin/python`
- PyTorch: `2.0.1+cu118`
- CUDA visibility inside PyTorch: unavailable on the current no-GPU instance

Available conda environments:

- `base` at `/root/miniconda3`
- `vcd` at `/root/autodl-tmp/envs/vcd`

## 5. HuggingFace cache

- path exists: `/root/autodl-tmp/hf-home`
- size snapshot: about `1.6G`

This suggests there is already a usable HF cache root on the remote machine.

## 6. Model and dataset paths

Confirmed existing paths:

- old VCD repo: `/root/autodl-tmp/code/VCD`
- LLaVA-1.5 checkpoint: `/root/autodl-tmp/code/VCD/experiments/checkpoints/llava-v1.5-7b`
- POPE annotations: `/root/autodl-tmp/code/VCD/experiments/data/POPE`
- COCO val2014 images: `/root/autodl-tmp/code/VCD/experiments/data/coco/val2014`
- GQA images: `/root/autodl-tmp/code/VCD/experiments/data/gqa/images`

Remote code root listing at query time:

- `/root/autodl-tmp/code` currently contains only `VCD`

## 7. Legacy VCD provenance that remains useful

Useful archived files already copied locally:

- `project_context/legacy_handoff/legacy_environment/remote_paths.md`
- `project_context/legacy_handoff/legacy_environment/model_dataset_paths.md`
- `project_context/legacy_handoff/legacy_environment/run_commands.md`

These remain the best provenance source for:

- old run-command templates
- known path conventions
- old offline/HF environment variables

## 8. Current LVLM environment readiness

What appears ready:

- remote VCD codebase exists
- LLaVA-1.5 checkpoint exists
- POPE dataset path exists
- a dedicated `vcd` conda environment exists
- HF cache root exists

What is missing or not yet verified:

- active GPU access on the current instance
- `llava` as a globally installed Python package in the current env
- any dedicated new-project remote work directory

Likely interpretation:

- the environment is still centered around repo-local VCD/LLaVA code rather than a separately installed `llava` package

## 9. Recommended remote work directory for new baselines

Recommended new work directory for the new project:

- `/root/autodl-tmp/code/training-free_hallucination`

Status:

- recommended only
- not created during this planning stage

Reason:

- keeps the new project separate from the frozen legacy VCD repo
- makes it easier to clone small baseline repos remotely without polluting the old tree

## 10. Immediate constraints for the next stage

- no formal experiment should start on the current no-GPU instance
- heavy baseline cloning or model downloads should happen only on the remote machine, not locally
- if FLB or another baseline requires a different model family, prefer remote-only setup in a dedicated remote work directory

