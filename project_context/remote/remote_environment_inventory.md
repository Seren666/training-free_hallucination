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

## GPU instance verification

> Verification date: 2026-04-29
> Verification scope: login, GPU visibility, disk/memory, conda, PyTorch CUDA, old path existence, and minimal module/path checks only.
> Password handling: no password was written into any local file, script, markdown, or Git commit.

### New instance entry

- host: `connect.westb.seetacloud.com`
- port: `31048`
- user: `root`
- current container hostname: `autodl-container-3n631bugr0-97c149e4`
- login status: success

### GPU / driver / CUDA

Direct `nvidia-smi` snapshot:

- GPU model: `NVIDIA GeForce RTX 4090`
- GPU count: `1`
- VRAM: `49140 MiB`
- current GPU memory use at verification time: `0 MiB / 49140 MiB`
- current GPU utilization at verification time: `0%`
- driver version: `580.105.08`
- CUDA version reported by driver: `13.0`

### Disk and memory

Direct `df -h` snapshot:

- `/`: `30G` total, about `27G` available
- `/usr/bin/nvidia-smi` backing disk: `439G` total, about `400G` available
- shared data mount: `AutoFS:fswestb1` at `/autodl-pub/data`, about `20T` total, about `18T` available
- `/root/autodl-tmp`: exists

Direct `free -h` snapshot:

- RAM: `754 GiB` total
- used: `107 GiB`
- free: `322 GiB`
- available: `632 GiB`
- swap: `0`

### Conda environments

`conda env list` output showed:

- `base` at `/root/miniconda3`
- path environment at `/root/autodl-tmp/envs/vcd`

Important note:

- `conda activate vcd` failed because there is no environment registered under the short name `vcd`
- `conda activate /root/autodl-tmp/envs/vcd` succeeded

### PyTorch CUDA verification

Inside `/root/autodl-tmp/envs/vcd`:

- Python: `3.9.25`
- Python path: `/root/autodl-tmp/envs/vcd/bin/python`
- PyTorch: `2.0.1+cu118`
- `torch.cuda.is_available()`: `True`
- `torch.version.cuda`: `11.8`
- `torch.cuda.device_count()`: `1`
- detected device: `NVIDIA GeForce RTX 4090`
- capability: `(8, 9)`

Minimal CUDA smoke test:

- `torch.randn(2, 2, device="cuda")`
- tiny matrix multiplication
- result: success

### Old path existence check

Confirmed existing paths on the new instance:

- `/root/autodl-tmp`
- `/root/autodl-tmp/code`
- `/root/autodl-tmp/code/VCD`
- `/root/autodl-tmp/hf-home`
- `/root/autodl-tmp/code/VCD/experiments/checkpoints/llava-v1.5-7b`
- `/root/autodl-tmp/code/VCD/experiments/data/POPE`
- `/root/autodl-tmp/code/VCD/experiments/data/coco/val2014`
- `/root/autodl-tmp/code/VCD/experiments/data/gqa/images`
- `/root/autodl-tmp/code/VCD/experiments/data/POPE/aokvqa`
- `/root/autodl-tmp/code/VCD/experiments/eval/object_hallucination_vqa_llava.py`
- `/root/autodl-tmp/code/VCD/experiments/eval/eval_pope.py`
- `/root/autodl-tmp/code/VCD/experiments/eval/mme_prepare.py`
- `/root/autodl-tmp/code/VCD/experiments/eval/mme_format_results.py`
- `/root/autodl-tmp/code/VCD/experiments/cd_scripts/llava1.5_pope.bash`

Sample POPE annotation files confirmed:

- `coco_pope_random.json`
- `coco_pope_popular.json`
- `coco_pope_adversarial.json`
- `gqa_pope_random.json`
- `aokvqa_pope_random.json`

### Current module import status

In the activated path environment:

- `import transformers`: success
- `import PIL`: success

Direct import status without extra path setup:

- `import llava`: failed
- `import vcd_utils.vcd_sample`: failed because `llava` was not on `PYTHONPATH`

Import status with repo-aware `PYTHONPATH`:

- `PYTHONPATH=/root/autodl-tmp/code/VCD/experiments:/root/autodl-tmp/code/VCD`
- `import llava`: success
- `import vcd_utils.vcd_sample`: success

Interpretation:

- the codebase itself is present and usable
- but the new instance currently needs the repo-aware `PYTHONPATH` convention documented before any actual script execution

### Differences from the old handoff

Compared with the old no-GPU instance and legacy notes:

- SSH endpoint changed from `connect.westc.seetacloud.com:21607` to `connect.westb.seetacloud.com:31048`
- GPU is now available and healthy
- old path layout is still preserved under `/root/autodl-tmp/code/VCD`
- the `vcd` environment still exists by path, but `conda activate vcd` does not work by short name on this instance
- direct module imports now require explicit `PYTHONPATH` pointing at both:
  - `/root/autodl-tmp/code/VCD`
  - `/root/autodl-tmp/code/VCD/experiments`

### Readiness judgment

Current judgment:

- the new GPU instance is suitable for the next phase of environment-level work
- it is also suitable to begin FLB preparation or one-forward signal-audit preparation
- before any real run, the activation instructions should be normalized to:

```bash
source /root/miniconda3/etc/profile.d/conda.sh
conda activate /root/autodl-tmp/envs/vcd
export PYTHONPATH=/root/autodl-tmp/code/VCD/experiments:/root/autodl-tmp/code/VCD:${PYTHONPATH}
```

This is enough to move into the next stage without downloading anything locally and without running any formal experiment yet.

