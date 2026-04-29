# Remote Runbook

> Scope: stable remote usage notes for the verified GPU instance
> Status: environment/runbook only. No formal experiments are started by this document.
> Password rule: never write the SSH password into local files, scripts, markdown, or Git commits.

## 1. Remote instance

- host: `connect.westb.seetacloud.com`
- port: `31048`
- user: `root`

Login form:

```bash
ssh -p 31048 root@connect.westb.seetacloud.com
```

Do not save the password inside the repository.

## 2. Legacy remote code root

- old VCD remote path: `/root/autodl-tmp/code/VCD`

Do not delete this remote path.
Do not delete remote model/data directories under it.

## 3. Conda activation

Use the absolute-path environment activation command:

```bash
source /root/miniconda3/etc/profile.d/conda.sh
conda activate /root/autodl-tmp/envs/vcd
```

Important note:

- `conda activate vcd` does **not** work reliably on the verified instance
- use the absolute env path instead

## 4. Required PYTHONPATH

Before running old VCD / LLaVA-related scripts, export:

```bash
export PYTHONPATH=/root/autodl-tmp/code/VCD/experiments:/root/autodl-tmp/code/VCD:${PYTHONPATH}
```

Reason:

- repo-local imports such as `llava` and `vcd_utils.vcd_sample` depend on these source paths

## 5. Key remote paths

### Checkpoint

- LLaVA-1.5 checkpoint: `/root/autodl-tmp/code/VCD/experiments/checkpoints/llava-v1.5-7b`

### POPE annotations

- POPE root: `/root/autodl-tmp/code/VCD/experiments/data/POPE`
- COCO split annotations live under: `/root/autodl-tmp/code/VCD/experiments/data/POPE/coco`
- GQA split annotations live under: `/root/autodl-tmp/code/VCD/experiments/data/POPE/gqa`
- A-OKVQA split annotations live under: `/root/autodl-tmp/code/VCD/experiments/data/POPE/aokvqa`

### Image roots

- COCO image root: `/root/autodl-tmp/code/VCD/experiments/data/coco/val2014`
- GQA image root: `/root/autodl-tmp/code/VCD/experiments/data/gqa/images`

### HuggingFace cache

- HF cache root: `/root/autodl-tmp/hf-home`

## 6. Common checks

### GPU

```bash
nvidia-smi
```

### Disk

```bash
df -h
```

### Conda environments

```bash
conda env list
```

### PyTorch CUDA check

```bash
python - <<'PY'
import torch
print("torch:", torch.__version__)
print("cuda available:", torch.cuda.is_available())
print("cuda version:", torch.version.cuda)
print("device count:", torch.cuda.device_count())
if torch.cuda.is_available():
    print("device:", torch.cuda.get_device_name(0))
    print("capability:", torch.cuda.get_device_capability(0))
PY
```

### Tiny CUDA smoke test

```bash
python - <<'PY'
import torch
x = torch.randn(2, 2, device="cuda")
print(x @ x)
print("ok")
PY
```

## 7. Old VCD script entry points

Main old entry files:

- `/root/autodl-tmp/code/VCD/experiments/eval/object_hallucination_vqa_llava.py`
- `/root/autodl-tmp/code/VCD/experiments/eval/eval_pope.py`
- `/root/autodl-tmp/code/VCD/experiments/eval/mme_prepare.py`
- `/root/autodl-tmp/code/VCD/experiments/eval/mme_format_results.py`
- `/root/autodl-tmp/code/VCD/experiments/cd_scripts/llava1.5_pope.bash`

## 8. Pre-run checklist

Before any future dry check or experiment:

1. Confirm GPU is visible with `nvidia-smi`.
2. Activate the env with the absolute path command.
3. Export the repo-aware `PYTHONPATH`.
4. Confirm PyTorch CUDA is available.
5. Confirm checkpoint path exists.
6. Confirm POPE annotation path exists.
7. Confirm COCO / GQA image roots exist.
8. Confirm no outputs, cache, or downloaded artifacts will be written into the local Git repo.

## 9. Repository hygiene rules

- Do not download models or datasets to the local Windows Git repository.
- Do not copy remote raw outputs back into the local Git repository.
- Do not commit cache, outputs, traces, checkpoints, or large JSON/JSONL files to GitHub.
- Keep GitHub updates limited to lightweight markdown notes, manifests, and small summaries.

## 10. Current boundary

Allowed in the current project phase:

- environment verification
- script-level dry checks
- path verification
- planning
- lightweight markdown documentation

Not allowed in the current project phase unless explicitly requested later:

- formal benchmark runs
- baseline cloning
- new model downloads
- new dataset downloads
- long-running jobs

