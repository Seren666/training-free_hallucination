# Weighted Evidence Consistency Audit

> Date: 2026-05-03
> Scope: training-free weighted mention-level verification using the existing `4000`-event mention table, with classifier results kept only as upper-bound reference. No decoding, no correction, no second-pass rewrite, no reranking.

## 1. Motivation

The last round left a clear gap:

- single internal signals were real and interpretable
- equal-weight composites were cleaner than single signals as a story
- but equal weighting still trailed the best single separator on the main tasks

So this round asked a narrower question:

- if strong signal families get larger preregistered weights
- and weak or partial-coverage families get smaller weights
- can a training-free score beat both the old equal-weight composite and the best single signal

## 2. Why Equal Weight Was Not Enough

The old composite treated very different families as if they were equally trustworthy:

- `middle_x_mass_change`, `mass_change_late_minus_mid`, and `middle_to_late_image_attention_delta` were repeatedly top-tier and full-coverage
- `anchor_masschange_x_late_mass` and `anchor_target_token_rank` were strong and mechanistically important, especially for introduced / persistent slices
- `attention shape` stayed weaker and had about `50.45%` missingness
- `visual sensitivity` was useful supporting validation, but only had about `20%` coverage

So equal weighting was structurally too generous to weak families and too conservative for the strongest full-coverage families.

## 3. Preregistered Weighting Principles

This round still stayed training-free:

- no learned weights
- no threshold search
- no direct reuse of classifier coefficients as final weights

The manual weighting rule was:

1. give the most weight to signals that were repeatedly top-ranked, full-coverage, and control-robust
2. give medium weight to strong but more slice-specific signals
3. give low weight to weak or partial-coverage families
4. allow failure-mode-specific scores to shift weight toward the signals that fit that trajectory best

That produced five preregistered scores:

1. `global_weighted_evidence_score`
2. `introduced_focused_weighted_score`
3. `persistent_focused_weighted_score`
4. `removed_focused_weighted_score`
5. `risk_minus_rescue_weighted_score`

Design choice:

- the global and failure-mode scores mainly rely on the three dominant full-coverage families:
  - middle-to-late evolution
  - anchor-middle mismatch
  - middle visual verification
- attention shape only gets a small auxiliary role
- visual sensitivity only gets a small auxiliary or persistent-focused role

## 4. Score Definitions

### 4.1 Global weighted score

Main terms:

- `middle_x_mass_change`
- `mass_change_late_minus_mid`
- `middle_to_late_image_attention_delta`
- `anchor_target_token_rank`
- `anchor_masschange_x_late_mass`

Rescue terms:

- `image_attention_middle_mean`
- `middle_target_probability_mean`

Small auxiliary terms:

- `late_image_attention_recovery_ratio`
- `firstlogitgap_x_verification_masschange`

### 4.2 Introduced-focused weighted score

The introduced score increases weight on:

- `anchor_masschange_x_late_mass`
- `firstlogitgap_x_verification_masschange`
- weak middle support via `image_attention_middle_mean` and `middle_target_probability_mean`

This matches the current introduced-hallucination story:

- strong anchor-side push
- weak middle verification
- abnormal middle-to-late evolution

### 4.3 Persistent-focused weighted score

The persistent score increases weight on:

- `anchor_target_token_rank`
- `anchor_masschange_x_late_mass`
- `middle_x_mass_change`
- low `middle_to_late_prob_jump`
- low `top_minus_random_logit_drop`
- low `sensitivity_ratio_prob`

This is the only score that intentionally leans more on supporting validation, because persistent remained the hardest slice and needed extra evidence beyond pure evolution.

### 4.4 Removed-focused weighted score

The removed score increases weight on:

- `middle_x_mass_change`
- `mass_change_late_minus_mid`
- `middle_to_late_image_attention_delta`
- `late_image_attention_recovery_ratio`

This matches the removed-hallucination interpretation:

- a stronger late-stage over-mention / recovery pattern

### 4.5 Risk-minus-rescue weighted score

Risk side:

- middle-to-late evolution
- anchor-middle mismatch
- a small head-consistency risk term

Rescue side:

- stronger middle attention
- stronger middle token probability
- stronger top-vs-random masking sensitivity

Its role is diagnostic rather than task-specific.

## 5. Main Results

Task-matched weighted scores:

| Task | Score | abs(AUC-0.5) | PR-AUC |
|---|---|---:|---:|
| `hallucinated_vs_correct` | `global_weighted_evidence_score` | `0.2922` | `0.9010` |
| `introduced_vs_correct` | `introduced_focused_weighted_score` | `0.3309` | `0.7988` |
| `persistent_vs_correct` | `persistent_focused_weighted_score` | `0.2337` | `0.6830` |
| `removed_vs_correct` | `removed_focused_weighted_score` | `0.3431` | `0.8050` |

Compared with the previous references:

| Task | Best Single | Single abs(AUC-0.5) | Old Equal-Weight Composite | Old abs(AUC-0.5) | New Weighted Score | New abs(AUC-0.5) |
|---|---|---:|---|---:|---|---:|
| `hallucinated_vs_correct` | `middle_x_mass_change` | `0.2745` | `composite_middle_to_late_abnormal_evolution` | `0.2684` | `global_weighted_evidence_score` | `0.2922` |
| `introduced_vs_correct` | `middle_x_mass_change` | `0.3198` | `composite_middle_to_late_abnormal_evolution` | `0.3091` | `introduced_focused_weighted_score` | `0.3309` |
| `persistent_vs_correct` | `anchor_target_token_rank` | `0.2173` | `composite_middle_to_late_abnormal_evolution` | `0.1735` | `persistent_focused_weighted_score` | `0.2337` |
| `removed_vs_correct` | `middle_x_mass_change` | `0.3252` | `composite_middle_to_late_abnormal_evolution` | `0.3227` | `removed_focused_weighted_score` | `0.3431` |

Headline result:

- the weighted training-free route now beats the best single signal on all four main mention-level tasks
- it also beats the old equal-weight composite on all four main tasks

## 6. Control Analyses

All five weighted scores were strong under the standard controls:

- category robustness: `high`
- mention-position robustness: `high`
- caption-source robustness: `high`
- missing rate at the final score level: `0.0000`

Important nuance:

- score-level missingness is `0` because weighted averaging renormalizes over available evidence
- that does not mean shape and sensitivity are suddenly full-coverage
- it means they only contribute when present, and their total weight stays small

Interpretation:

- the gain is not coming from a single late-position artifact
- it is not confined to one or two frequent object categories
- it survives the regular vs `first_logit` caption-source split better than the earlier equal-weight composite

## 7. Multi-Seed Stability

Using `image_id` test splits with seeds `55, 56, 57, 58, 59`:

| Task | Task-Matched Score | Mean Test ROC-AUC | Std | Mean Test PR-AUC |
|---|---|---:|---:|---:|
| `hallucinated_vs_correct` | `global_weighted_evidence_score` | `0.8069` | `0.0146` | `0.9138` |
| `introduced_vs_correct` | `introduced_focused_weighted_score` | `0.8503` | `0.0088` | `0.8348` |
| `persistent_vs_correct` | `persistent_focused_weighted_score` | `0.7460` | `0.0168` | `0.7041` |
| `removed_vs_correct` | `removed_focused_weighted_score` | `0.8556` | `0.0213` | `0.8352` |

Stability reading:

- the weighted route is stable enough to be taken seriously
- introduced and removed are the healthiest slices
- persistent is still the hardest slice, but it improved materially over the old composite

Post-hoc observation, not a new preregistration:

- `persistent_focused_weighted_score` generalized surprisingly well even outside the persistent task
- but that is a retrospective finding, so it should not replace the task-matched reading as the main conclusion

## 8. Comparison To Classifier Upper Bound

Classifier reference remains stronger:

| Task | Weighted Test ROC-AUC | Category+Position Control ROC-AUC | Internal-Only ROC-AUC | Classifier Upper-Bound ROC-AUC |
|---|---:|---:|---:|---:|
| `hallucinated_vs_correct` | `0.8069` | `0.8099` | `0.8540` | `0.8712` |
| `introduced_vs_correct` | `0.8503` | `0.8588` | `0.9016` | `0.9166` |
| `persistent_vs_correct` | `0.7460` | `0.7639` | `0.7945` | `0.8062` |
| `removed_vs_correct` | `0.8556` | `0.8600` | `0.8991` | `0.9105` |

So the weighted route closes part of the gap, but not all of it.

Current reading:

- training-free weighting is now clearly better than equal weighting
- it is also better than the previous best single signal under the full mention-level audit
- but classifier still shows there is learnable structure left on the table

## 9. Which Failure Mode Benefits Most

Two answers matter:

1. highest target-task score:
   - `removed_focused_weighted_score = 0.3431`
2. biggest shortfall repair:
   - persistent improves from `0.1735` under the old equal-weight composite to `0.2337` under `persistent_focused_weighted_score`

So:

- removed is the cleanest weighted-score success case
- persistent is the most important improvement relative to the previous training-free baseline

## 10. What This Shows

This round verifies that:

- equal weighting was too blunt
- signal-strength-aware weighting is worthwhile
- failure-mode-aware weighting is worthwhile
- middle-to-late evolution, anchor-middle mismatch, and middle verification are strong enough to support a better training-free verifier together than apart

## 11. What This Still Does Not Show

This round does not justify:

- a runtime selector
- a correction rule
- a second-pass rewrite implementation
- a reranker
- replacing the classifier backup with a fully solved training-free verifier

## 12. Current Route Judgment

1. weighted training-free scores are now the strongest training-free mention-level verifier we have
2. they beat both the best single signal and the old equal-weight composite on the core tasks
3. classifier backup is still worth preserving, because the split-based upper bound is still clearly higher
4. this is enough to justify a bounded second-pass correction design discussion if the user wants one
5. it is still not enough to jump straight into correction implementation without an explicit design round
