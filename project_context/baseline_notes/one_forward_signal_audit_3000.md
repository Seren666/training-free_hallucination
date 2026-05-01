# One-Forward Signal Audit 3000

> Date: 2026-05-02
> Scope: stratified COCO-CHAIR one-forward internal signal audit on existing full paired results only.

## 1. Why This Audit

The current project state is:

- `first_logit / early-anchor` has a stable positive effect on full COCO-CHAIR
- the effect survives near-official CHAIR alignment
- but the method is not yet selective:
  - some images improve
  - some worsen
  - most remain no-delta stable

This audit asks a narrower question:

- can a single normal prompt forward already provide coarse internal signals that separate:
  - `improved`
  - `worsened`
  - `stable`

Goal of this round:

- analysis only
- no generation rerun
- no method change
- no parameter tuning

## 2. Subset Construction

Outcome labels were built from the full paired adapted-CHAIR object-level comparison:

- `improved`:
  - `first_logit hallucinated object count < regular hallucinated object count`
- `worsened`:
  - `first_logit hallucinated object count > regular hallucinated object count`
- `stable`:
  - `first_logit hallucinated object count == regular hallucinated object count`

Full paired counts reproduced exactly:

- improved:
  - `5066`
- worsened:
  - `3287`
- stable:
  - `32151`

Audit subset:

- fixed seed:
  - `55`
- stratified subset size:
  - `3000`
- sampled per group:
  - `1000 improved`
  - `1000 worsened`
  - `1000 stable`

Remote files:

- paired labels:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/paired_outcome_labels.csv`
- subset list:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/one_forward_audit_subset_3000.csv`

## 3. Probe Setup

Prompt:

- `Please describe the image.`

Model path:

- `/root/autodl-tmp/code/VCD/experiments/checkpoints/llava-v1.5-7b`

Vision tower local override:

- `/root/autodl-tmp/hf-home/hub/models--openai--clip-vit-large-patch14-336/snapshots/ce19dc912ca5cd21c8a653c79e251e808ccabcd1`

Remote-only scripts added:

- probe:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/coco_one_forward_signal_probe.py`
- analysis:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/analyze_one_forward_signal_audit.py`

Important implementation choice:

- this probe uses one prompt-only forward with `output_attentions=True` and `output_hidden_states=True`
- it does **not** save generated captions
- it does **not** save full attention tensors or full hidden states
- it only saves aggregated per-image statistics

## 4. Audit Completion Status

The `3000`-image audit completed successfully.

Counts:

- improved rows:
  - `1000`
- worsened rows:
  - `1000`
- stable rows:
  - `1000`
- failures:
  - `0`

Runtime / memory notes:

- prompt-only one-forward runtime per image was about `0.28s` in the sanity run
- peak reserved GPU memory stayed around `14.29 GB`

Remote outputs:

- per-image audit csv:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/one_forward_signal_audit_3000.csv`
- summary csv:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/one_forward_signal_audit_3000_summary.csv`
- summary json:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/one_forward_signal_audit_3000_summary.json`
- summary markdown:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/one_forward_signal_audit_3000_summary.md`

## 5. Signals Collected

Per image, the probe logged:

- metadata:
  - image id
  - outcome label
  - regular / first-logit hallucinated object counts
  - hallucination delta
- first-token / anchor statistics:
  - top-10 tokens / probabilities
  - entropy
  - top1-top2 margin
  - top-10 mass
  - HHI concentration
- visual attention summaries:
  - image token range
  - pre-generation query position
  - per-layer image attention mass summaries
  - middle-layer and late-layer averages
  - attention entropy summaries
- hidden alignment summaries:
  - per-layer hidden-image cosine
  - pre-hidden norms
  - pooled-image norms
  - middle / late cosine means
  - middle-to-late alignment change
- runtime / memory:
  - runtime
  - peak allocated / reserved memory

## 6. Main Result

The coarse one-forward scalar signals are **weak separators**.

Most important observation:

- `improved vs worsened` separation is nearly null for every tested scalar
- the best absolute AUC shift from `0.5` is only about `0.0167`

So this audit does **not** show a strong image-level one-forward predictor for whether later-step first-logit will help or hurt a sample.

## 7. Group-Level Signal Table

| Signal | Improved Mean | Worsened Mean | Stable Mean | Improved vs Worsened AUC | Improved vs Stable AUC | Worsened vs Stable AUC |
|---|---:|---:|---:|---:|---:|---:|
| first_token_entropy | 0.4830 | 0.4759 | 0.5097 | 0.5119 | 0.4591 | 0.4492 |
| first_token_top1_top2_margin | 0.7528 | 0.7558 | 0.7302 | 0.4861 | 0.5459 | 0.5564 |
| anchor_top10_mass | 0.999477 | 0.999476 | 0.999421 | 0.4976 | 0.5702 | 0.5717 |
| anchor_hhi | 0.7617 | 0.7657 | 0.7450 | 0.4864 | 0.5424 | 0.5535 |
| image_attention_middle_mean | 0.1157 | 0.1161 | 0.1150 | 0.4833 | 0.5299 | 0.5445 |
| image_attention_late_mean | 0.0766 | 0.0762 | 0.0756 | 0.5136 | 0.5402 | 0.5266 |
| image_attention_middle_entropy_mean | 5.0643 | 5.0688 | 5.0738 | 0.4899 | 0.4733 | 0.4845 |
| image_attention_late_entropy_mean | 5.2539 | 5.2585 | 5.2577 | 0.4890 | 0.4920 | 0.5030 |
| hidden_image_cosine_middle_mean | 0.2289 | 0.2299 | 0.2262 | 0.4854 | 0.5496 | 0.5647 |
| hidden_image_cosine_late_mean | 0.5117 | 0.5119 | 0.5111 | 0.4975 | 0.5133 | 0.5151 |
| middle_to_late_alignment_change | 0.2827 | 0.2820 | 0.2849 | 0.5076 | 0.4594 | 0.4494 |

## 8. What Separates, What Does Not

### 8.1 Improved vs worsened

This is the main target for selective intervention, and the answer is currently:

- almost nothing separates them well at this coarse image-level summary granularity

Best `improved vs worsened` signals by AUC shift:

1. `image_attention_middle_mean`
   - AUC `0.4833`
2. `hidden_image_cosine_middle_mean`
   - AUC `0.4854`
3. `first_token_top1_top2_margin`
   - AUC `0.4861`
4. `image_attention_late_mean`
   - AUC `0.5136`
5. `anchor_hhi`
   - AUC `0.4864`

Interpretation:

- all of these are still too close to random
- they do not support a strong coarse selector for `helpful` vs `harmful`

### 8.2 Improved / worsened vs stable

There is a slightly stronger but still modest trend for `changed` outcomes vs `stable`.

Signals with the clearest stable-separation tendency:

- `anchor_top10_mass`
  - improved vs stable AUC `0.5702`
  - worsened vs stable AUC `0.5717`
- `hidden_image_cosine_middle_mean`
  - improved vs stable AUC `0.5496`
  - worsened vs stable AUC `0.5647`
- `first_token_top1_top2_margin`
  - improved vs stable AUC `0.5459`
  - worsened vs stable AUC `0.5564`
- `anchor_hhi`
  - improved vs stable AUC `0.5424`
  - worsened vs stable AUC `0.5535`

Interpretation:

- these signals may weakly reflect whether the prompt state is in a more easily steerable regime
- but they still do not tell us whether the eventual change will be beneficial or harmful

## 9. Does This Support Selective Early-Anchor?

Current answer:

- not yet

What this audit supports:

- the one-forward signal family is not completely meaningless
- some signals weakly distinguish `stable` from `changed`

What it does **not** support:

- a strong coarse image-level selector for `improved` vs `worsened`
- an immediate jump to selective early-anchor routing based on these summary scalars alone

## 10. Current Caveats

1. This is a `3000`-image stratified subset, not the full `40504`.
2. Signals are coarse image-level summaries, not object-token-level measurements.
3. The probe reads only the standard prompt forward, not the internal first-logit intervention branch itself.
4. Outcome labels come from the adapted CHAIR path for exact count consistency with the established full paired report.
5. Near-official alignment strengthens the overall method claim, but was not used as the label source for this grouping step.

## 11. Recommendation

Recommended next step:

- **do not** jump straight to full signal extraction across all `40504` images
- **do not** claim that selective early-anchor is already predictable from these coarse one-forward scalars
- move to **object-level token analysis** on changed samples, especially:
  - improved cases where major hallucinated objects disappear
  - worsened cases where new hallucinated objects are introduced
  - token-position and object-category-specific internal signal differences

Working interpretation:

- the helpful vs harmful distinction likely lives at a finer object-token level than these global prompt-level summaries capture
- so the right next analysis target is more local and category-aware, not broader brute-force extraction
