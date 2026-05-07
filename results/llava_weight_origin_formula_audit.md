# LLaVA Weighted Score Formula Audit

## Scope

This note audits where the current LLaVA weighted risk score is defined, how it is computed, and whether CHAIR labels enter runtime scoring.

## Formula source files

Primary definition and analysis:
- `.codex_tmp_remote/analyze_weighted_evidence_consistency.py`

Runtime / action reuse:
- `.codex_tmp_remote/second_pass_correction_action_pilot.py`

Frozen downstream consumers:
- `.codex_tmp_remote/strict_second_pass_action_matrix_pilot.py`
- `.codex_tmp_remote/regular_source_risk_full_remote.py`
- `.codex_tmp_remote/correction_expanded_confirmation.py`

Supporting result tables:
- `.codex_tmp_remote/weighted_remote_results/weighted_evidence_score_definitions.csv`
- `results/high_risk_mentions_firstlogit_full.csv`

## Score columns

Primary weighted family scores:
- `global_weighted_evidence_score`
- `introduced_focused_weighted_score`
- `persistent_focused_weighted_score`
- `removed_focused_weighted_score`

Analysis-only extra score:
- `risk_minus_rescue_weighted_score`

Full-table routing fields:
- `primary_risk_score`
- `primary_risk_family`
- `is_top5_risk`
- `is_top10_risk`
- `is_top20_risk`
- `risk_group`

## Computation pattern

The analysis script defines each score family in `SCORE_SPECS`. Each family is a manually specified weighted sum of aligned features.

Core computation:
1. derive or read feature columns
2. z-score each feature
3. flip the sign for `rescue` features
4. compute an available-weight normalized weighted average

Analysis form in `analyze_weighted_evidence_consistency.py`:

```text
aligned_feature = zscore(feature)
if mode == rescue:
    aligned_feature = -aligned_feature
score = sum(weight * aligned_feature) / sum(weight for available aligned features)
```

Runtime form in `second_pass_correction_action_pilot.py`:
- the same weighted families are re-declared in `WEIGHTED_SCORE_SPECS`
- z-scores are computed with reference mean / std from `mention_verification_signal_table.csv`
- the same risk / rescue sign rule is applied

Primary routing:
- `primary_risk_score = max(global, introduced, persistent, removed)`
- `primary_risk_family = argmax(...)`

Risk slices:
- `top5 = 95th percentile`
- `top10 = 90th percentile`
- `top20 = 80th percentile`

## Signal families used

The original LLaVA weighted verifier uses a compact subset of hand-chosen signals:

Evolution / mismatch:
- `middle_x_mass_change`
- `mass_change_late_minus_mid`
- `middle_to_late_image_attention_delta`
- `anchor_masschange_x_late_mass`
- `firstlogitgap_x_verification_masschange`

Anchor / rank:
- `anchor_target_token_rank`

Middle verification rescue:
- `image_attention_middle_mean`
- `middle_target_probability_mean`

Late recovery:
- `late_image_attention_recovery_ratio`

Persistent-specific rescue / visual sensitivity:
- `middle_to_late_prob_jump`
- `top_minus_random_logit_drop`
- `sensitivity_ratio_prob`

Analysis-only extra:
- `middle_head_mass_cv_mean` appears only in `risk_minus_rescue_weighted_score`

## Explicit weights

### `global_weighted_evidence_score`
- `middle_x_mass_change`: `0.25` risk
- `mass_change_late_minus_mid`: `0.15` risk
- `middle_to_late_image_attention_delta`: `0.15` risk
- `anchor_target_token_rank`: `0.12` risk
- `anchor_masschange_x_late_mass`: `0.12` risk
- `image_attention_middle_mean`: `0.10` rescue
- `middle_target_probability_mean`: `0.05` rescue
- `late_image_attention_recovery_ratio`: `0.03` risk
- `firstlogitgap_x_verification_masschange`: `0.03` risk

### `introduced_focused_weighted_score`
- `middle_x_mass_change`: `0.20` risk
- `mass_change_late_minus_mid`: `0.15` risk
- `middle_to_late_image_attention_delta`: `0.15` risk
- `anchor_masschange_x_late_mass`: `0.15` risk
- `anchor_target_token_rank`: `0.10` risk
- `image_attention_middle_mean`: `0.10` rescue
- `firstlogitgap_x_verification_masschange`: `0.10` risk
- `middle_target_probability_mean`: `0.05` rescue

### `persistent_focused_weighted_score`
- `anchor_target_token_rank`: `0.25` risk
- `image_attention_middle_mean`: `0.15` rescue
- `anchor_masschange_x_late_mass`: `0.15` risk
- `middle_x_mass_change`: `0.15` risk
- `middle_to_late_prob_jump`: `0.10` rescue
- `top_minus_random_logit_drop`: `0.10` rescue
- `sensitivity_ratio_prob`: `0.10` rescue

### `removed_focused_weighted_score`
- `middle_x_mass_change`: `0.20` risk
- `mass_change_late_minus_mid`: `0.18` risk
- `middle_to_late_image_attention_delta`: `0.18` risk
- `anchor_target_token_rank`: `0.12` risk
- `late_image_attention_recovery_ratio`: `0.12` risk
- `anchor_masschange_x_late_mass`: `0.10` risk
- `image_attention_middle_mean`: `0.10` rescue

## Hard-coded or learned

- weights are explicit and hard-coded: `yes`
- score families are manually enumerated: `yes`
- score fitting / learning step exists in these scripts: `no`
- runtime scoring imports a trained classifier: `no`

There are separate diagnostic classifier-analysis scripts elsewhere in the repo, but the retained-branch weighted verifier does not call them.

## Are CHAIR labels used inside scoring

Directly inside score computation:
- `no`

Used later for retrospective analysis and evaluation:
- `yes`

Important nuance:
- `second_pass_correction_action_pilot.py` uses `mention_verification_signal_table.csv` as a reference table for feature mean / std normalization.
- That reference use is numeric calibration only.
- The weighted score calculation itself does not read `hallucinated_label` or `correct_label` to set weights or thresholds.

## Bottom line

The current LLaVA weighted verifier is a training-free, hand-designed weighted heuristic. It is not a learned weight vector and it does not use CHAIR labels inside runtime scoring.
