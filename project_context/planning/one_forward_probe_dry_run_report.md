# One-Forward Probe Dry Run Report

> Scope: remote-only lightweight probe dry run for one-forward signal audit preparation.
> Date: 2026-04-30
> Phase boundary:
> - not a formal experiment
> - not a baseline reproduction
> - not a full-POPE run
> - no intervention logic
> - no full attention/hidden-state tensor saving

## 1. Probe script status

Completed.

Remote-only probe script path:

- `/root/autodl-tmp/code/training_free_hallucination_probe/pope_one_forward_probe.py`

Remote-only probe workspace:

- `/root/autodl-tmp/code/training_free_hallucination_probe`

The probe is outside the frozen legacy VCD repo and uses the old code only through imports.

## 2. Whether old VCD main code was modified

No.

What was done:

- created a new remote-only workspace
- created a new remote-only probe script
- reused old VCD / LLaVA code through:
  - `PYTHONPATH=/root/autodl-tmp/code/VCD/experiments:/root/autodl-tmp/code/VCD:${PYTHONPATH}`

What was not done:

- no edit to `/root/autodl-tmp/code/VCD`
- no edit to the old checkpoint files
- no permanent config rewrite

## 3. How the vision-tower local path was handled

Problem:

- stock loading still points to:
  - `openai/clip-vit-large-patch14-336`
- the current instance cannot rely on online HF resolution

Probe-side solution:

- override the vision tower path at runtime
- do not modify the original checkpoint config on disk

Actual local vision-tower path used by the probe:

- `/root/autodl-tmp/hf-home/hub/models--openai--clip-vit-large-patch14-336/snapshots/ce19dc912ca5cd21c8a653c79e251e808ccabcd1`

Implementation behavior:

- load `AutoConfig` locally
- set `cfg.mm_vision_tower` to the local snapshot path
- if `vision_tower` exists in config, override it too
- load the model with `local_files_only=True`

This solved the offline loading problem without downloading anything.

## 4. One-sample probe result

Successful.

Probe target sample:

- `question_id = 1`
- question:
  - `Is there a snowboard in the image?`

Output file:

- `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/pope_probe_qid1_summary.jsonl`

Observed result:

- generated answer:
  - `Yes`
- first-token top-1:
  - `Yes`
- first-token yes/no probability margin:
  - `0.3097560703754425`

Readability confirmed for:

- first-token logits
- yes/no margin
- token index metadata
- attention summary
- hidden-state summary
- GPU memory summary

## 5. Tiny probe result

Successful.

Tiny probe size:

- `10` POPE samples

Output file:

- `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/pope_probe_tiny_summary.jsonl`

Summary:

- processed `question_id` values:
  - `1` through `10`
- generated answers:
  - `Yes, No, Yes, No, Yes, No, Yes, No, Yes, No`
- yes/no probability margin range:
  - min: `-0.9877651478163898`
  - max: `0.9367330595850945`
- peak allocated GPU memory range:
  - min: `14.5667 GB`
  - max: `14.5670 GB`

Interpretation:

- probe execution is stable on a tiny sequential sample set
- first-token binary preference is strongly readable
- attention / hidden-state summary collection is stable at this scale

## 6. First-token logits readability

Confirmed.

Per-sample output includes:

- top-10 token ids
- top-10 token strings
- top-10 probabilities
- top-10 logits
- top-1 / top-2 token and ids
- top-1 / top-2 probability margin
- top-1 / top-2 logit margin
- entropy

This is enough for the first-logit support audit.

## 7. Yes/No margin readability

Confirmed.

Per-sample output includes:

- `yes_probability`
- `no_probability`
- `yes_no_probability_margin`
- `yes_logit`
- `no_logit`
- `yes_no_logit_margin`
- `predicted_yes_no`

This is enough for the binary POPE decision surface without using the label as a runtime decision input.

## 8. Image attention mass readability

Confirmed.

Per-sample attention summary includes:

- number of layers
- number of heads
- attention tensor shape
- per-layer:
  - image attention mass mean across heads
  - image attention mass max across heads
  - image attention mass std across heads
  - image-attention entropy

Example from sample `question_id=1`, layer 0:

- `image_attention_mass_mean = 0.6610627174377441`
- `image_attention_mass_max = 0.9075139760971069`
- `image_attention_mass_std = 0.23903276026248932`
- `image_attention_entropy = 6.288759708404541`

## 9. Layer-wise attention summary readability

Confirmed.

The probe stores only aggregate per-layer statistics and does not save full attention tensors.

This is suitable for:

- middle-layer visual support
- head consistency summary
- pre-answer image-attention analysis

## 10. Hidden-state summary readability

Confirmed.

Per-sample hidden summary includes:

- hidden-state entry count
- hidden-state shape
- selected layer summaries for:
  - pre-answer hidden norm
  - cosine similarity between pre-answer hidden and pooled image hidden

Example from sample `question_id=1`:

- hidden index `0`:
  - norm `0.5915884375572205`
  - cosine `0.010353793390095234`
- hidden index `16`:
  - norm `28.907154083251953`
  - cosine `0.18432091176509857`
- hidden index `32`:
  - norm `101.30224609375`
  - cosine `0.45816755294799805`

This is enough for an initial alignment / hidden-support audit.

## 11. Token-position stability

Confirmed.

For the first sample:

- image token range:
  - `[35, 610]`
- pre-answer query position:
  - `634`
- first generated answer position:
  - `635`

The probe records:

- sequence length
- image token start/end
- pre-answer query position
- first generated answer position
- raw input id length

This is enough for stable downstream aggregation logic.

## 12. GPU memory

Observed peak allocated GPU memory:

- one-sample probe:
  - about `14.5667 GB`
- tiny 10-sample probe:
  - stable around `14.5667` to `14.5670 GB`

Judgment:

- 49 GB VRAM is comfortably sufficient for this one-sample / tiny-sample probe mode

## 13. Remote output file paths

Probe script:

- `/root/autodl-tmp/code/training_free_hallucination_probe/pope_one_forward_probe.py`

Output directory:

- `/root/autodl-tmp/code/training_free_hallucination_probe/outputs`

Current small outputs:

- `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/pope_probe_qid1_summary.jsonl`
- `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/pope_probe_tiny_summary.jsonl`

These outputs remain remote-only and should not be committed to GitHub.

## 14. Recommendation on entering the formal one-forward signal audit

Recommended: yes, for the minimal audit stage.

Reason:

- the remote GPU path is stable
- the loader workaround is known and reproducible
- first-token logits are stable and readable
- yes/no margins are stable and readable
- image-attention summaries are stable and readable
- hidden-state summaries are stable and readable
- token index recovery is stable
- memory is not the bottleneck at this scale

## 15. Current technical risks

Primary risk:

- the probe still depends on runtime override of the local vision-tower path
- stock offline loading remains unreliable if that override is omitted

Secondary risk:

- when launching remote commands from the current Windows shell with multiline wrapping, one output filename temporarily picked up a trailing carriage return
- this was corrected by renaming the remote file
- future remote invocations should prefer simpler quoting or single-line output-path arguments

Minor risk:

- the current probe is tailored to the LLaVA-1.5 + POPE binary setting
- later open-ended object-token analysis may need additional token-alignment logic

## 16. Bottom-line judgment

The remote-only one-forward probe is now in place and already good enough to support the next smallest audit step.

The next recommended move is:

1. keep using this remote-only probe
2. expand the tiny sample count modestly only when needed
3. start computing first-logit / pre-answer / middle-layer signal tables for the first audit notebook or markdown summary
