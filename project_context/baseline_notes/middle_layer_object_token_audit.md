# Middle-Layer Object-Token Audit

> Date: 2026-05-02
> Scope: middle-layer object-token audit on the existing 4000-event stratified object-local subset, with no new caption generation and no new method implementation.

## 1. Why this audit

Previous object-local analysis already showed:

- fixed `first_logit / early-anchor` acts at object-token-local scale
- introduced hallucinations often carry stronger anchor-side push than removed hallucinations
- correct object mentions carry stronger middle-layer image attention than hallucinated mentions

The missing piece was whether middle layers can act as a more explicit verification surface, especially when combined with:

- middle-layer target rank
- middle-to-late rank shift
- attention shape rather than only attention mass

## 2. Data and probe scope

Used:

- existing `results/object_local_probe_subset.csv`
- existing `results/object_local_signal_probe.csv`
- new supplement `results/object_local_middle_rank_probe.csv`
- new analysis outputs:
  - `results/middle_layer_object_audit.md`
  - `results/middle_layer_object_audit.csv`
  - `results/middle_layer_object_audit.json`

Subset counts:

- `removed_hallucination = 1000`
- `introduced_hallucination = 1000`
- `persistent_hallucination = 1000`
- `correct_object_mention = 1000`

The supplement probe added only lightweight fields:

- selected middle/late layer target ranks
- selected middle/late layer target probabilities
- middle-to-late rank improvement

It did not save:

- full hidden states
- full attention tensors
- new captions

## 3. What was added beyond the previous probe

The previous probe already had:

- final-step target rank and probability
- anchor-side rank and adjustment
- per-layer attention mass / max / std / entropy
- per-layer hidden-image cosine

This audit added a `logit-lens` style view for representative middle and late layers:

- `middle_target_rank_mean`
- `late_target_rank_mean`
- `middle_target_probability_mean`
- `late_target_probability_mean`
- `middle_to_late_rank_improvement`
- `middle_to_late_probability_delta`

It also derived attention-shape features from the saved per-layer aggregates:

- `middle_norm_entropy`
- `middle_effective_ratio`
- `middle_peak_ratio`
- `middle_head_cv`
- `mass_change_late_minus_mid`
- `peak_change_late_minus_mid`
- `cv_change_late_minus_mid`

## 4. Key group-level means

### 4.1 Rank-lens signals

| Signal | Removed | Introduced | Persistent | Correct |
|---|---:|---:|---:|---:|
| `middle_target_rank_mean` | `4422.097` | `6098.926` | `4038.532` | `3533.189` |
| `late_target_rank_mean` | `170.921` | `514.899` | `137.319` | `47.214` |
| `middle_to_late_rank_improvement` | `4251.176` | `5584.027` | `3901.213` | `3485.976` |
| `middle_target_probability_mean` | `0.070131` | `0.071635` | `0.122727` | `0.144712` |
| `late_target_probability_mean` | `0.356334` | `0.345166` | `0.482614` | `0.568903` |

### 4.2 Visual-support signals

| Signal | Removed | Introduced | Persistent | Correct |
|---|---:|---:|---:|---:|
| `image_attention_middle_mean` | `0.148705` | `0.145080` | `0.161936` | `0.183550` |
| `image_attention_late_mean` | `0.131166` | `0.126253` | `0.125515` | `0.129074` |
| `hidden_image_cosine_middle_mean` | `0.262167` | `0.270068` | `0.261482` | `0.249804` |
| `hidden_image_cosine_late_mean` | `0.472734` | `0.475761` | `0.467166` | `0.470856` |

### 4.3 Attention-shape signals

| Signal | Removed | Introduced | Persistent | Correct |
|---|---:|---:|---:|---:|
| `middle_norm_entropy` | `0.786623` | `0.790537` | `0.780531` | `0.780069` |
| `middle_peak_ratio` | `4.739394` | `4.795417` | `4.564500` | `4.349331` |
| `middle_head_cv` | `1.171911` | `1.173529` | `1.140609` | `1.120910` |
| `mass_change_late_minus_mid` | `-0.017539` | `-0.018827` | `-0.036422` | `-0.054476` |
| `peak_change_late_minus_mid` | `0.387097` | `0.313192` | `0.560797` | `0.840778` |
| `cv_change_late_minus_mid` | `0.195172` | `0.172335` | `0.191448` | `0.222587` |

## 5. Answers to the five questions

### 5.1 Do correct object mentions already look stronger in middle layers?

Yes.

Against `introduced_hallucination`:

- `middle_target_rank_mean`: `6098.926` vs `3533.189`
- `image_attention_middle_mean`: `0.145080` vs `0.183550`
- `middle_target_probability_mean`: `0.071635` vs `0.144712`

So correct mentions are already more supported in the middle stage, not only at the final stage.

Important nuance:

- `hidden_image_cosine_middle_mean` is not the strongest middle-layer discriminator by itself
- middle-layer target rank and middle-layer visual attention are more informative than hidden cosine alone

### 5.2 Do introduced hallucinations look like strong anchor support plus weak middle visual evidence?

Directionally yes, with an important qualification.

Relative to `removed_hallucination`, introduced hallucinations still show stronger anchor-side promotion:

- `anchor_adjustment_delta`: `1.151627` vs `0.978613`
- `adjusted_target_rank_if_applied`: `1.021` vs `1.467`

But relative to `correct_object_mention`, they still have weak middle verification:

- `middle_target_rank_mean`: `6098.926` vs `3533.189`
- `image_attention_middle_mean`: `0.145080` vs `0.183550`
- `middle_target_probability_mean`: `0.071635` vs `0.144712`

So the better reading is:

- introduced hallucinations are not “anchor strong” in an absolute correct-vs-hallucinated sense
- they are anchor-pushed within the hallucinated population
- but that push is not matched by equally strong middle-layer visual support

### 5.3 Are removed hallucinations cases where fixed first_logit corrected late-stage over-mention unsupported by middle layers?

Directionally yes.

Compared with `correct_object_mention`, removed hallucinations still look weaker in middle layers:

- `middle_target_rank_mean`: `4422.097` vs `3533.189`
- `image_attention_middle_mean`: `0.148705` vs `0.183550`

But they also show later promotion:

- `late_target_rank_mean`: `170.921` vs `47.214`
- `middle_to_late_rank_improvement`: `4251.176` vs `3485.976`

This supports the interpretation that some regular-caption hallucinations become competitive late, even though middle-layer evidence is not as strong as in correct mentions.

That is compatible with the current mechanism story:

- fixed `first_logit` can remove some late-stage over-mentions that middle layers do not really ground

### 5.4 Does middle-to-late rank shift separate hallucinated vs correct mentions?

Yes, but not as the single strongest signal.

Selected results:

- `introduced vs correct`
  - `middle_to_late_rank_improvement` delta = `2098.052`
  - `abs(AUC-0.5) = 0.1158`
- `removed vs correct`
  - `middle_to_late_rank_improvement` delta = `765.200`
  - `abs(AUC-0.5) = 0.0609`
- `removed vs introduced`
  - `middle_to_late_rank_improvement` delta = `-1332.851`
  - `abs(AUC-0.5) = 0.0617`

So rank shift helps, especially for `introduced vs correct`, but it is not enough alone to define a selector.

Its main value is mechanism evidence:

- hallucinated mentions, especially introduced ones, rely more on later promotion
- correct mentions are relatively stronger already in the middle stage

### 5.5 Is attention shape more explanatory than plain attention mass?

Yes.

For `introduced_hallucination vs correct_object_mention`:

- `mass_change_late_minus_mid`: `abs(AUC-0.5) = 0.3113`
- `image_attention_middle_mean`: `0.2616`
- `peak_change_late_minus_mid`: `0.2445`
- `middle_peak_ratio`: `0.2323`
- `middle_head_cv`: `0.1808`

This matters because:

- plain middle attention mass is already useful
- but shape features add more mechanism detail
- especially whether attention stays visually anchored into late layers, and whether middle attention is diffuse vs peaky and head-consistent vs fragmented

The best current reading is:

- correct mentions lose more mass from middle to late because they already got useful middle grounding
- hallucinated mentions keep weaker or less diagnostic middle grounding and show less of that grounded middle-to-late drop
- diffuse / concentrated / cross-head-consistency features are more explanatory than mass alone

## 6. What seems strong vs weak

Most useful current signals:

- `mention_position_ratio`
- `image_attention_middle_mean`
- `mass_change_late_minus_mid`
- `middle_peak_ratio`
- `anchor_target_token_rank`
- `middle_target_rank_mean`
- `late_target_probability_mean`

Useful but secondary:

- `middle_to_late_rank_improvement`
- `middle_head_cv`
- `peak_change_late_minus_mid`

Still weak as standalone:

- `hidden_image_cosine_middle_mean`
- `hidden_image_cosine_late_mean`

## 7. Current mechanism reading

This audit strengthens the mechanism story:

- early-anchor is not enough by itself
- the more important question is whether the candidate object is already receiving convincing middle-layer visual support
- correct mentions tend to look better in middle-layer rank and middle-layer attention
- introduced hallucinations look more like anchor-pushed mentions without matching middle-layer verification
- removed hallucinations are consistent with late-stage over-mention that fixed `first_logit` can suppress

So middle layers now look like a more plausible verification surface than:

- coarse image-level scalars
- broad token-vocab suppression
- caption-level rollback

## 8. Whether this justifies a new pilot

Yes, conditionally.

This audit does not justify:

- threshold search
- classifier training
- new benchmark expansion

But it does justify one constrained next pilot if method work continues:

- `Middle-Verified Early Anchor Decoding` on `1000` COCO-CHAIR images

Why that next step is justified:

- middle-layer evidence is clearly more local and more explanatory than the failed coarse selectors
- attention shape adds information beyond raw mass
- the new rank-lens supplement shows that correct mentions are already stronger in the middle stage, while hallucinated mentions rely more on later promotion

## 9. Caveats

- this is still a stratified 4000-event subset, not full object-event coverage
- the rank-lens view is a lightweight diagnostic, not a calibrated probability model
- strong separation here does not mean a runtime selector will automatically work
- method claims should stay bounded until a `1000` pilot is run and compared against fixed `first_logit`
