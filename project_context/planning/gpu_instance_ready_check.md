# GPU Instance Ready Check

> Status: verification only. No baseline was cloned, no model/data was downloaded, and no formal experiment was started.
> Verified instance: `root@connect.westb.seetacloud.com -p 31048`
> Verification date: 2026-04-29

## Passed checks

- SSH login to the new GPU instance succeeded.
- `nvidia-smi` is healthy and shows `1 x NVIDIA GeForce RTX 4090`.
- VRAM is visible: `49140 MiB`.
- Driver/CUDA reported by `nvidia-smi` are normal: driver `580.105.08`, CUDA `13.0`.
- GPU was idle at verification time: `0 MiB` used, `0%` util.
- `/root/autodl-tmp` exists.
- Old code root exists: `/root/autodl-tmp/code/VCD`.
- Old LLaVA-1.5 checkpoint path exists.
- POPE annotations exist.
- COCO image root exists.
- GQA image root exists.
- POPE `aokvqa` annotation directory exists.
- HF cache root exists: `/root/autodl-tmp/hf-home`.
- VCD eval/script entry files exist.
- Path-based activation of the old environment works:
  - `conda activate /root/autodl-tmp/envs/vcd`
- PyTorch CUDA works in that environment:
  - `torch.cuda.is_available() == True`
  - device count `1`
  - detected device `RTX 4090`
- Tiny CUDA smoke test passed.
- Repo-aware imports work after setting:

```bash
export PYTHONPATH=/root/autodl-tmp/code/VCD/experiments:/root/autodl-tmp/code/VCD:${PYTHONPATH}
```

## Failed checks

- `conda activate vcd` by short environment name failed.
- `import llava` failed before `PYTHONPATH` was set.
- `import vcd_utils.vcd_sample` also failed before `PYTHONPATH` was set, because it depends on `llava`.

These are environment-setup issues, not evidence that the checkpoint or dataset paths are missing.

## Need-to-remember issues

- The old environment is path-based, not name-based, on this instance.
- Running VCD-related code on this instance should use the absolute env path activation command.
- VCD/LLaVA imports appear to expect repo-local source paths rather than only installed site-packages.

## Need user confirmation

- Whether the next stage should keep using the legacy VCD repo in place, or create a separate remote working directory for the new project before any script editing.
- Whether you want a tiny remote helper note or shell snippet prepared next turn for the standard activation command.

## Next-step recommendation

Recommended next step before any real audit or baseline work:

1. Standardize the remote activation recipe for this instance.
2. Do one more script-level dry check around the exact POPE eval entry import path if you want zero setup ambiguity.
3. Then move into FLB preparation or one-forward signal-audit instrumentation, still without cloning baselines locally and still without downloading anything to the local Git repo.

## Overall judgment

Yes: the new GPU instance is ready for the next stage of preparation work.

No: this turn should still not start formal experiments, baseline cloning, or model/data downloads.
