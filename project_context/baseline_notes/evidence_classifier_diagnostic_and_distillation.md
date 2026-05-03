# Evidence Classifier Diagnostic And Distillation

> Date: 2026-05-03
> Scope: multi-seed classifier diagnostic and training-free score distillation on the existing mention-level verification table. No new decoding, no correction, no second-pass rewrite, no reranking.

## 1. Motivation

The previous round established three things:

- mention-level hallucination verification is feasible
- training-free equal-weight composites are useful but still trail the best single signal
- a lightweight classifier can learn a much stronger verification boundary

So this round asks two follow-up questions:

1. what exactly the classifier is learning
2. whether that diagnostic can be distilled back into a stronger training-free score

The intended use remains constrained:

- training-free evidence consistency stays the main line
- classifier stays upper-bound diagnostic / backup verifier
- no correction method is implemented from this audit alone

## 2. Classifier As Upper-Bound, Not Final Method

Setup:

- seeds: `55, 56, 57, 58, 59`
- split: by `image_id`
- train / val / test = `60 / 20 / 20`
- models:
  - logistic regression
  - linear SVM
  - random forest

Feature settings:

- `A_internal_features_only`
- `B_category_position_control`
- `C_internal_plus_category_position`
- `D_internal_without_category_position`
- `E_middle_to_late_evolution_only`
- `E_anchor_middle_mismatch_only`
- `E_middle_visual_verification_only`
- `E_attention_shape_only`

Important note:

- `A` and `D` are identical by construction in this round because the only control features are `object_category` and `mention_position_ratio`

## 3. Multi-Seed Stability

Best val-selected upper-bound setting is stable across all seeds and all tasks:

| Task | Best Stable Setting | Mean ROC-AUC | Std ROC-AUC | Mean PR-AUC | Std PR-AUC |
|---|---|---:|---:|---:|---:|
| `hallucinated_vs_correct` | `C_internal_plus_category_position` | `0.8712` | `0.0197` | `0.9349` | `0.0151` |
| `introduced_vs_correct` | `C_internal_plus_category_position` | `0.9166` | `0.0117` | `0.8869` | `0.0180` |
| `persistent_vs_correct` | `C_internal_plus_category_position` | `0.8062` | `0.0257` | `0.7608` | `0.0428` |
| `removed_vs_correct` | `C_internal_plus_category_position` | `0.9105` | `0.0116` | `0.8788` | `0.0331` |

Internal-only setting is also stable and strong:

| Task | `A_internal_features_only` Mean ROC-AUC | Std |
|---|---:|---:|
| `hallucinated_vs_correct` | `0.8540` | `0.0172` |
| `introduced_vs_correct` | `0.9016` | `0.0128` |
| `persistent_vs_correct` | `0.7945` | `0.0239` |
| `removed_vs_correct` | `0.8991` | `0.0128` |

Immediate reading:

- the classifier diagnostic is stable enough to keep as a backup route
- stability is strongest on `introduced` and `removed`
- `persistent` remains the hardest slice even for the upper-bound diagnostic

## 4. Feature Family Ablation

Among single-family settings, the strongest learned family is still `anchor-middle mismatch`.

Best family-only mean test ROC-AUC:

- `hallucinated_vs_correct`
  - `anchor_middle_mismatch = 0.8291`
  - `middle_to_late_evolution = 0.8076`
  - `middle_visual_verification = 0.8004`
  - `attention_shape = 0.6515`
- `introduced_vs_correct`
  - `anchor_middle_mismatch = 0.8681`
  - `middle_to_late_evolution = 0.8642`
  - `middle_visual_verification = 0.8634`
  - `attention_shape = 0.6676`
- `persistent_vs_correct`
  - `anchor_middle_mismatch = 0.7484`
  - `middle_visual_verification = 0.7426`
  - `middle_to_late_evolution = 0.7148`
  - `attention_shape = 0.5941`
- `removed_vs_correct`
  - `anchor_middle_mismatch = 0.8782`
  - `middle_to_late_evolution = 0.8554`
  - `middle_visual_verification = 0.8206`
  - `attention_shape = 0.6640`

Family takeaway:

- mismatch is the best standalone learned family
- evolution and middle verification remain close behind
- attention shape is still weakest as a standalone family

## 5. Category/Position Control

Control-only setting:

- `B_category_position_control`

Its mean ROC-AUCs are:

- `hallucinated_vs_correct = 0.8099`
- `introduced_vs_correct = 0.8588`
- `persistent_vs_correct = 0.7639`
- `removed_vs_correct = 0.8600`

Internal-only beats control consistently:

- `A_internal_features_only` beats `B_category_position_control` on all `5/5` seeds for all four tasks
- mean ROC deltas are:
  - `+0.0441` on `hallucinated_vs_correct`
  - `+0.0428` on `introduced_vs_correct`
  - `+0.0306` on `persistent_vs_correct`
  - `+0.0391` on `removed_vs_correct`

Internal-plus-control beats control even more strongly:

- `C_internal_plus_category_position` beats `B_category_position_control` on all `5/5` seeds for all four tasks
- mean ROC deltas are:
  - `+0.0613`
  - `+0.0577`
  - `+0.0423`
  - `+0.0505`

Boundary:

- internal evidence is not reducible to category + position bias
- but category still adds extra signal once it is allowed into the model

## 6. Feature Importance

Two lenses are needed.

### 6.1 With controls: what the best upper-bound model actually uses

On `C_internal_plus_category_position`, category one-hot coefficients dominate raw absolute coefficient mass:

- `hallucinated_vs_correct`: control share `0.8633`
- `introduced_vs_correct`: control share `0.8258`
- `persistent_vs_correct`: control share `0.8751`
- `removed_vs_correct`: control share `0.8068`

This means:

- the best learned verifier is not a clean mechanism-only object
- once category is available, linear models lean heavily on it
- raw coefficient magnitude alone should not be mistaken for a preferred scientific explanation

### 6.2 Without controls: what the internal evidence itself prefers

On `A_internal_features_only`, the feature-family balance is much closer to the mechanism story:

| Task | Largest Internal Family Shares |
|---|---|
| `hallucinated_vs_correct` | middle verification `0.324`, mismatch `0.252`, sensitivity `0.208`, evolution `0.137` |
| `introduced_vs_correct` | middle verification `0.323`, mismatch `0.250`, attention shape `0.152`, sensitivity `0.139`, evolution `0.135` |
| `persistent_vs_correct` | evolution `0.277`, middle verification `0.265`, sensitivity `0.193`, mismatch `0.172` |
| `removed_vs_correct` | mismatch `0.271`, middle verification `0.242`, evolution `0.212`, sensitivity `0.160` |

Recurring internal positive-risk features:

- `anchor_target_token_rank`
- `anchor_adjustment_delta`
- `middle_target_rank_mean`
- `obj_semantic_refinement_19_26_target_rank_mean`
- `middle_x_mass_change`
- `mass_change_late_minus_mid`
- `middle_to_late_image_attention_delta`
- `middle_norm_entropy_mean` in the introduced slice

Recurring internal rescue / counter-risk features:

- `image_attention_middle_mean`
- `middle_target_probability_mean`
- `obj_visual_enrichment_5_18_target_rank_mean`
- `obj_semantic_refinement_19_26_target_prob_mean`
- `anchor_support_strong_middle_weak_composite`
- `middle_to_late_prob_jump` often appears as a negative coefficient under multivariate correlation

Interpretation boundary:

- ablation results are more trustworthy than any one coefficient sign
- several coefficient signs flip under correlation, so the right reading is family-level rather than literal one-feature causality

## 7. Distilled Training-Free Scores

Pre-registered distilled scores:

1. `distilled_middle_to_late_dominant_score`
2. `distilled_anchor_middle_mismatch_score`
3. `distilled_risk_minus_rescue_score`
4. `distilled_event_type_adaptive_score`

Best distilled score per comparison:

| Comparison | Best Distilled Score | abs(AUC-0.5) | Diagnostic AUC |
|---|---|---:|---:|
| `hallucinated_vs_correct` | `distilled_middle_to_late_dominant_score` | `0.2684` | `0.7684` |
| `introduced_vs_correct` | `distilled_anchor_middle_mismatch_score` | `0.3213` | `0.8213` |
| `persistent_vs_correct` | `distilled_middle_to_late_dominant_score` | `0.1735` | `0.6735` |
| `removed_vs_correct` | `distilled_middle_to_late_dominant_score` | `0.3227` | `0.8227` |
| `introduced_vs_removed` | `distilled_anchor_middle_mismatch_score` | `0.0806` | `0.5806` |

What changed relative to the old composite family:

- `distilled_middle_to_late_dominant_score` intentionally reproduces the old best evolution composite, so it does not create a new gain by itself
- `distilled_anchor_middle_mismatch_score` is the only new distilled score that produces a genuine improvement:
  - `introduced_vs_correct = 0.3213`
  - previous best composite there was `0.3091`
  - previous best single there was `0.3198`

## 8. Comparison With Best Single, Old Composite, And Classifier

Headline comparison:

| Comparison | Best Single Diag AUC | Best Distilled Diag AUC | Upper-Bound Mean ROC-AUC |
|---|---:|---:|---:|
| `hallucinated_vs_correct` | `0.7745` | `0.7684` | `0.8712` |
| `introduced_vs_correct` | `0.8198` | `0.8213` | `0.9166` |
| `persistent_vs_correct` | `0.7173` | `0.6735` | `0.8062` |
| `removed_vs_correct` | `0.8252` | `0.8227` | `0.9105` |

Route judgment:

- the new distilled training-free scores do **not** clearly beat the best single signal overall
- they beat the old equal-weight composite more convincingly than before
- they beat the best single only in the `introduced_vs_correct` slice, and only slightly
- they remain well below classifier upper-bound, with gaps of about:
  - `0.103` on `hallucinated_vs_correct`
  - `0.095` on `introduced_vs_correct`
  - `0.133` on `persistent_vs_correct`
  - `0.088` on `removed_vs_correct`

## 9. Whether The Training-Free Route Remains Plausible

Yes.

Why:

- internal-only verification remains strong and stable
- the best distilled score improves the introduced-hallucination slice
- the strongest training-free families remain mechanistically meaningful:
  - middle visual verification
  - middle-to-late evolution
  - anchor-middle mismatch

Why it is still incomplete:

- global `hallucinated_vs_correct` still does not beat the best single signal
- persistent hallucinations remain weak under all distilled scores
- the gap to classifier upper-bound is still substantial

## 10. Whether The Classifier Backup Is Worth Preserving

Yes.

Reasons:

- it is stable across `5` seeds
- internal-only already beats control-only consistently
- it confirms the current internal signals contain learnable hallucination information
- it helps identify where distillation still loses information

But its status should stay constrained:

- upper-bound diagnostic
- backup verifier
- not the main method
- not a license to jump into learned correction

## 11. What This Does Not Prove

This audit does not prove:

- a deployable runtime verifier
- a final training-free score
- a second-pass correction policy
- that category-conditioned learned verification should become the main story
- that attention shape alone is enough

## 12. Next Recommendation

Current route status:

1. training-free distilled score does **not** clearly exceed the best single signal overall
2. training-free distilled score is **not** close to the classifier upper-bound
3. classifier is stable enough to preserve as backup / diagnostic
4. internal features do stably beat category / position control
5. this is enough to justify a bounded second-pass correction **design discussion** if the user wants it
6. it is **not** enough to jump straight into correction implementation
7. additional signal discovery / stronger causal validation is still worthwhile, especially for:
   - persistent hallucinations
   - global `hallucinated_vs_correct`
   - closing the gap between training-free scores and the upper-bound diagnostic
