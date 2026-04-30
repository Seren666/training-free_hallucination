# Next Stage Dry Check Plan

> Scope: preparation only for the next remote phase.
> Current boundary: no formal experiment, no baseline clone, no model/data download, no long-running job.

## 1. FLB dry check goal

This dry check is not a full FLB reproduction.

It is only meant to answer:

- where the FLB / first-logit / early-anchor idea would hook into the current LLaVA-1.5 + POPE path
- whether the existing remote VCD/LLaVA evaluation entry already exposes the first answer-step information we need
- whether a minimal first-logit analysis can be done without cloning the full FLB baseline first

Explicit non-goals for this dry check:

- no full FLB benchmark reproduction
- no POPE full-split run
- no AMBER run
- no baseline repo clone in this round

## 2. One-forward audit dry check goal

This dry check is not yet the actual signal audit.

It is only meant to confirm that, on a single LLaVA-1.5 + POPE sample, we can read:

- logits
- `output_attentions`
- `output_hidden_states`
- first-token distribution
- image token index range
- answer token index range
- layer-wise attention summary
- head-wise attention summary

Logging rule:

- do not save full large tensors
- do not save raw attention cubes or hidden-state dumps to the Git repo
- only print or save lightweight aggregated statistics if needed

## 3. Minimal remote check sequence

Recommended order on the verified GPU instance:

1. Login to the GPU instance:
   - `ssh -p 31048 root@connect.westb.seetacloud.com`
2. Initialize conda in shell if needed:
   - `source /root/miniconda3/etc/profile.d/conda.sh`
3. Activate the verified environment:
   - `conda activate /root/autodl-tmp/envs/vcd`
4. Set the repo-local import path:
   - `export PYTHONPATH=/root/autodl-tmp/code/VCD/experiments:/root/autodl-tmp/code/VCD:${PYTHONPATH}`
5. Confirm GPU visibility:
   - `nvidia-smi`
6. Confirm the LLaVA-1.5 checkpoint path exists
7. Confirm the POPE annotation path and image root exist
8. Do a script import dry check only:
   - verify the old LLaVA / POPE eval entry imports successfully
9. Do one POPE sample no-save forward dry run
10. If that passes, do one POPE sample `output_attentions` / `output_hidden_states` dry run

The first pass should stay at single-sample scale only.

## 4. What to read in the dry run

For the FLB-oriented side:

- first answer-step logits
- `yes` / `no` first-step margin
- whether first-step support and final answer stay aligned

For the one-forward audit side:

- final logits at the first answer step
- hidden states for selected layers
- attentions for selected layers
- mapping from image tokens to answer-relevant token positions
- compact summaries such as:
  - image-attention mass
  - head disagreement
  - layer-to-layer support drift

## 5. Explicit non-goals

Do not do any of the following in this next-stage dry check:

- do not run POPE full evaluation
- do not run a formal FLB reproduction
- do not clone the FLB baseline repo yet
- do not download any new model or dataset
- do not save full tensors
- do not commit outputs, cache, trace, or large JSONL files
- do not train a classifier
- do not implement a new mitigation method

## 6. Success criteria for the dry check

The dry check is successful if we can confirm all of the following on one sample:

- the old remote eval environment still imports cleanly
- the LLaVA-1.5 checkpoint path resolves correctly
- the POPE annotation and image root are correctly mapped
- one normal forward can be executed without saving outputs
- first-step logits can be inspected
- hidden states and attentions can be requested at single-sample scale
- aggregated layer/head summaries can be produced without writing large artifacts

## 7. Fallbacks if memory or coupling becomes a problem

If `output_attentions` and `output_hidden_states` are too expensive even on one sample:

- reduce to a smaller selected layer set first
- only keep aggregated statistics in memory
- separate the first-logit dry check from the attention audit dry check

If the old VCD eval entry is too tightly coupled to legacy decoding code:

- write a small remote-only probe script later
- keep it outside the local Git repo until the interface is stable
- make the probe read-only with respect to model/data assets

## 8. Immediate next-step recommendation

If this dry check passes:

- move to the smallest possible one-forward signal audit on a tiny POPE slice
- keep the first version descriptive, not optimization-driven
- start with first-logit support plus one middle-layer visual-support view

If it fails:

- first localize whether the issue is import, path, token indexing, or memory
- only then decide whether a lightweight independent probe script is necessary
