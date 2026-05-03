# Multidimensional Evidence Verification

> Date: 2026-05-03
> Scope: mention-level hallucination verification using existing object-event labels and completed internal-signal probes. No new decoding, no correction, no second-pass rewrite, no reranking.

## 1. Motivation

The current question is narrower than method design:

- given an already generated caption and one object mention
- can multi-dimensional internal evidence tell us whether that mention is hallucinated

This round keeps the training-free route as the main line, but allows a lightweight classifier as an upper-bound diagnostic for whether the signals contain learnable hallucination information.

## 2. Why Single Signals Are Insufficient

The previous mention-level audit already showed that single signals are informative:

- best single on `hallucinated_vs_correct` was `middle_x_mass_change` with `abs(AUC-0.5)=0.2745`
- the next strongest signals were still concentrated in the same families:
  - `mass_change_late_minus_mid = 0.2701`
  - `middle_to_late_image_attention_delta = 0.2701`
  - `anchor_masschange_x_late_mass = 0.2514`
  - `image_attention_middle_mean = 0.2155`

But that audit also showed a limitation:

- attention shape alone was weak
- visual sensitivity was useful but incomplete
- persistent hallucinations stayed harder than introduced or removed hallucinations

So this round asks whether combining families helps more than any one signal alone.

## 3. Training-Free Composite Definition

All composites were preregistered, equal-weight, and built from direction-aligned z-scores. No learned weights and no threshold tuning were used.

Composite families:

1. `middle_verification_deficit_score`
   - low `image_attention_middle_mean`
   - weak middle rank / probability
   - weak `VE 5-18` and `SR 19-26` support
2. `middle_to_late_abnormal_evolution_score`
   - `mass_change_late_minus_mid`
   - `middle_to_late_image_attention_delta`
   - `middle_x_mass_change`
   - `late_image_attention_recovery_ratio`
3. `anchor_middle_mismatch_score`
   - `anchor_target_token_rank`
   - `anchor_adjustment_delta`
   - `anchor_masschange_x_late_mass`
   - `firstlogitgap_x_verification_masschange`
4. `attention_shape_risk_score`
   - `middle_norm_entropy_mean`
   - `middle_effective_attended_count_mean`
   - `middle_peak_ratio_mean`
   - `middle_head_mass_cv_mean`
   - `middle_head_entropy_std`
   - `middle_head_top10_overlap_mean`
5. `all_evidence_consistency_score`
   - equal-weight average of the four family scores above

Dataset reuse:

- no new probe was needed
- the audit reused the existing balanced `4000`-event mention-level table
- sensitivity features still inherit the old `800`-event coverage boundary

## 4. Composite Results

Primary task: `hallucinated_vs_correct`

| Composite | abs(AUC-0.5) | Category Robustness | Position Robustness | Source Robustness | Missing Rate |
|---|---:|---|---|---|---:|
| `middle_to_late_abnormal_evolution_score` | `0.2684` | moderate | high | high | `0.0000` |
| `all_evidence_consistency_score` | `0.2249` | high | high | high | `0.0000` |
| `middle_verification_deficit_score` | `0.1591` | high | high | high | `0.0000` |
| `anchor_middle_mismatch_score` | `0.1134` | high | low | moderate | `0.0000` |
| `attention_shape_risk_score` | `0.0295` | high | low | low | `0.5045` |

Best composite by comparison:

- `hallucinated_vs_correct`: `middle_to_late_abnormal_evolution_score = 0.2684`
- `introduced_vs_correct`: `middle_to_late_abnormal_evolution_score = 0.3091`
- `persistent_vs_correct`: `middle_to_late_abnormal_evolution_score = 0.1735`
- `removed_vs_correct`: `middle_to_late_abnormal_evolution_score = 0.3227`
- `introduced_vs_removed`: `anchor_middle_mismatch_score = 0.0979`

Main reading:

- the strongest training-free summary is still the middle-to-late evolution family
- the all-family composite helps, but not enough to beat the best evolution-centered single signal
- attention-shape risk is still much weaker than the core verification / evolution / mismatch families

## 5. Composite vs Best Single Signal

Training-free combination did not beat the strongest single signal on any of the main comparisons.

| Comparison | Best Single | abs(AUC-0.5) | Best Composite | abs(AUC-0.5) |
|---|---|---:|---|---:|
| `hallucinated_vs_correct` | `middle_x_mass_change` | `0.2745` | `middle_to_late_abnormal_evolution_score` | `0.2684` |
| `introduced_vs_correct` | `middle_x_mass_change` | `0.3198` | `middle_to_late_abnormal_evolution_score` | `0.3091` |
| `persistent_vs_correct` | `anchor_target_token_rank` | `0.2173` | `middle_to_late_abnormal_evolution_score` | `0.1735` |
| `removed_vs_correct` | `middle_x_mass_change` | `0.3252` | `middle_to_late_abnormal_evolution_score` | `0.3227` |

Interpretation:

- multi-dimensional training-free evidence is real
- but the current equal-weight composite mainly stabilizes the same story rather than unlocking a clearly stronger verification boundary

## 6. Classifier Upper-Bound Setup

This branch is diagnostic only. It is not a proposed final method.

Models:

- logistic regression
- linear SVM
- random forest

Split:

- by `image_id`
- train / val / test = `60 / 20 / 20`
- fixed seed = `55`

Tasks:

- `hallucinated_vs_correct`
- `introduced_vs_correct`
- `persistent_vs_correct`
- `removed_vs_correct`

Feature groups:

- `A_middle_verification_only`
- `B_middle_to_late_evolution_only`
- `C_anchor_middle_mismatch_only`
- `D_attention_shape_only`
- `E_all_internal_plus_controls`
- `F_all_internal_minus_controls`
- `G_category_position_control`

Control definition for classifier:

- numeric: `mention_position_ratio`
- categorical: `object_category`

## 7. Classifier Results

Best val-selected test result per task:

| Task | Model | Feature Group | ROC-AUC | PR-AUC | Accuracy |
|---|---|---|---:|---:|---:|
| `hallucinated_vs_correct` | logistic regression | `E_all_internal_plus_controls` | `0.8792` | `0.9484` | `0.8128` |
| `introduced_vs_correct` | linear SVM | `E_all_internal_plus_controls` | `0.9211` | `0.9050` | `0.8456` |
| `persistent_vs_correct` | logistic regression | `E_all_internal_plus_controls` | `0.8271` | `0.7991` | `0.7775` |
| `removed_vs_correct` | linear SVM | `E_all_internal_plus_controls` | `0.9175` | `0.9080` | `0.8408` |

Best test ROC-AUC after family ablation:

- `hallucinated_vs_correct`
  - `E_all_internal_plus_controls = 0.8792`
  - `F_all_internal_minus_controls = 0.8600`
  - `G_category_position_control = 0.8099`
- `introduced_vs_correct`
  - `E_all_internal_plus_controls = 0.9256`
  - `F_all_internal_minus_controls = 0.9124`
  - `G_category_position_control = 0.8689`
- `persistent_vs_correct`
  - `E_all_internal_plus_controls = 0.8285`
  - `F_all_internal_minus_controls = 0.8174`
  - `G_category_position_control = 0.7687`
- `removed_vs_correct`
  - `E_all_internal_plus_controls = 0.9175`
  - `F_all_internal_minus_controls = 0.9066`
  - `G_category_position_control = 0.8526`

Main reading:

- internal features clearly beat the category-plus-position control on every task
- adding category plus position helps further, but the internal evidence already carries most of the value
- the classifier substantially beats the training-free composite, so the signals do contain learnable hallucination information

## 8. Feature Family Ablation

Among standalone internal families, the best classifier family is consistently `anchor_middle_mismatch`.

Best test ROC-AUC by standalone family:

- `hallucinated_vs_correct`
  - `C_anchor_middle_mismatch_only = 0.8414`
  - `B_middle_to_late_evolution_only = 0.8207`
  - `A_middle_verification_only = 0.8033`
  - `D_attention_shape_only = 0.6470`
- `introduced_vs_correct`
  - `C_anchor_middle_mismatch_only = 0.8844`
  - `B_middle_to_late_evolution_only = 0.8758`
  - `A_middle_verification_only = 0.8724`
  - `D_attention_shape_only = 0.6891`
- `persistent_vs_correct`
  - `C_anchor_middle_mismatch_only = 0.7841`
  - `A_middle_verification_only = 0.7530`
  - `B_middle_to_late_evolution_only = 0.7240`
  - `D_attention_shape_only = 0.5888`
- `removed_vs_correct`
  - `C_anchor_middle_mismatch_only = 0.8762`
  - `B_middle_to_late_evolution_only = 0.8678`
  - `A_middle_verification_only = 0.8236`
  - `D_attention_shape_only = 0.6690`

Important boundary:

- the best training-free composite is still the evolution family
- but the best standalone learned family is mismatch
- attention shape alone remains the weakest family by a wide margin

Coefficient reading:

- family ablation is more trustworthy than raw linear coefficients because the internal features are correlated
- that said, the recurring high-magnitude logistic features on the main binary task are:
  - `image_attention_middle_mean`
  - `anchor_target_token_rank`
  - `anchor_support_strong_middle_weak_composite`
  - `anchor_adjustment_delta`
  - `middle_target_rank_mean`
  - `middle_target_probability_mean`
  - `obj_visual_enrichment_5_18_target_rank_mean`
  - `middle_to_late_prob_jump`
- some sensitivity terms also enter with large coefficients, but their coverage is still limited by the old `800`-event sensitivity subset

## 9. Controls

Training-free composites:

- `middle_to_late_abnormal_evolution_score` is the most robust composite
- its robustness is:
  - category: `moderate`
  - position: `high`
  - source: `high`
- `all_evidence_consistency_score` is more stable than stronger-looking weak families like attention shape, but still does not beat the best single signal

Classifier controls:

- internal-only features beat `category + mention_position` control on all tasks
- the gain over control is largest for:
  - `hallucinated_vs_correct`: `0.8600` vs `0.8099`
  - `removed_vs_correct`: `0.9066` vs `0.8526`
- the gain is still real for:
  - `introduced_vs_correct`: `0.9124` vs `0.8689`
  - `persistent_vs_correct`: `0.8174` vs `0.7687`

Boundary:

- introduced hallucinations are still the easiest slice
- persistent hallucinations remain the hardest slice
- attention-shape composite coverage is incomplete because its fields still carry about `50.45%` missingness

## 10. Whether Multi-dimensional Evidence Improves Mention-Level Verification

Yes, but with an important split conclusion:

- training-free multi-dimensional evidence improves the descriptive story and yields a robust composite
- but it does not beat the strongest single signal on the main tasks
- lightweight learned combination does beat both the best single signal and the best training-free composite

So the verification result is:

- mention-level verification is clearly feasible above chance
- learnable information is present in the internal features
- the current one-forward training-free route is still plausible, but not yet strong enough to claim that a simple equal-weight score is the final verification interface

## 11. Whether One-Forward Training-Free Verification Is Still Plausible

Current answer: yes, but only as a constrained research direction.

Why it still looks plausible:

- the best composite stays close to the best single signal
- the strongest families remain the same ones already supported mechanistically:
  - middle verification
  - middle-to-late evolution
  - anchor-middle mismatch
- the composite remains robust across category, position, and source controls

Why it is not solved:

- equal-weight fusion does not beat the best single evolution feature
- attention-shape evidence stays weak
- persistent hallucinations are still harder to verify cleanly

## 12. Whether the Classifier Route Is Worth Keeping as Backup

Yes, but only as a backup diagnostic route.

What it is good for:

- checking whether internal evidence contains learnable hallucination structure
- testing family ablations
- sanity-checking whether training-free scoring is leaving signal on the table

What it is not good for:

- claiming a deployable runtime verifier
- replacing the training-free line as the main research story
- skipping the need for mechanism clarity and failure analysis

## 13. What This Does Not Prove

This round does not prove:

- a final runtime selector
- a second-pass correction policy
- a deployable one-forward verification rule
- that attention shape alone is enough
- that a learned verifier should become the main paper method

## 14. Next Recommended Discussion

The next acceptable discussion, if the user wants to continue, is:

- whether to keep strengthening the training-free mention-level verification surface
- or whether the evidence is now strong enough to justify a tightly scoped second-pass correction design discussion

What should not happen automatically:

- no correction implementation jump
- no new decoding branch
- no classifier-first method pivot
