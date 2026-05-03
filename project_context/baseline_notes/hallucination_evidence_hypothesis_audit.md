# Hallucination Evidence Hypothesis Audit

> Date: 2026-05-03
> Scope: system-level evidence discovery over existing COCO-CHAIR object-event labels and completed attention / logit-lens / middle-layer probes. No new decoding, no runtime rule, no threshold search, no classifier training.

## 1. Motivation

The project has now intentionally moved away from:

- replacing fixed `first_logit / early-anchor`
- adding another token-level guard
- adding another object-suppression or anchor-cleaning variant

That shift is justified by the completed method line:

- fixed `first_logit / early-anchor` remains the strongest decoding result
- `object_safe_anchor`, `attention_gated`, `candidate_local_guard`, `middle_verified`, `middle_refined`, and `layer_anchor_late_27_31_rank_average` all failed to beat it

So this round asks a different question:

- which internal evidence patterns actually track hallucinated object mentions
- which signals are only descriptive
- which signals are stable enough to become future correction-facing candidates

## 2. Hypothesis Registry

The audit registered ten hypothesis families:

| ID | Hypothesis | Status | Current Reading |
|---|---|---|---|
| H1 | Middle Verification Deficit | supported | strongest clean mechanism signal family |
| H2 | Late Readiness Surge | weak | only relative rank-jump evidence survives; absolute late confidence does not support the claim |
| H3 | Middle-to-Late Attention Evolution | supported | strongest overall evidence family |
| H4 | Attention Diffusion | weak | diffuse attention exists, but separation is small |
| H5 | Extreme Concentration / Spurious Fixation | weak | concentration alone is not grounding and is not a stable hallucination flag |
| H6 | Head Agreement | weak | informative, but weaker than verification-evolution signals |
| H7 | Layer Consistency | weak | some mismatch evidence exists, but not strongly |
| H8 | Anchor-Middle Mismatch | supported | strong first-logit-side mismatch evidence |
| H9 | Visual Sensitivity Validation | weak | useful supporting validation, not the primary separator |
| H10 | Removed vs Introduced Difference | supported | failure modes differ, but direct removed-vs-introduced separation is still weaker than introduced-vs-correct |

No supplemental probe was required. Existing probe tables already covered the needed fields.

## 3. Event Dataset and Labels

The analysis-ready benchmark table used the existing balanced object-event audit subset:

- total events: `4000`
- per event type:
  - `correct_object_mention`: `1000`
  - `introduced_hallucination`: `1000`
  - `removed_hallucination`: `1000`
  - `persistent_hallucination`: `1000`
- caption source:
  - `regular`: `2937`
  - `first_logit`: `1063`

Most frequent categories in the audit subset:

- `person`: `445`
- `dining table`: `433`
- `chair`: `249`
- `car`: `140`
- `bowl`: `116`
- `sports ball`: `105`
- `sink`: `93`
- `couch`: `90`

This means the current hypothesis audit is balanced at the event-type level, but still reflects the natural long-tail category mix inside COCO-CHAIR.

## 4. Signal Families

The audit reused five completed probe families:

- object-local token / anchor signals
- middle-layer rank-lens signals
- layer-group VE / SR / late logit-lens signals
- attention-shape summaries
- attention-guided visual sensitivity summaries

The current evidence map is:

- primary mechanism surface:
  - middle target rank / probability
  - middle image attention mass
  - middle-to-late mass evolution
  - anchor-plus-verification interaction
- supporting validation:
  - head agreement
  - layer-shape consistency
  - top-attention masking sensitivity
- weak standalone cues:
  - diffuse entropy alone
  - pure concentration alone

## 5. Main Results

### 5.1 Strongest supported hypotheses

`H1` Middle Verification Deficit:

- `image_attention_middle_mean`
  - introduced vs correct: `0.1451` vs `0.1835`
  - `abs(AUC-0.5)=0.2616`
- `middle_target_probability_mean`
  - introduced vs correct: `0.0716` vs `0.1447`
  - `abs(AUC-0.5)=0.1612`
- `obj_semantic_refinement_19_26_target_rank_mean`
  - introduced vs correct: `1171.5` vs `435.1`
  - `abs(AUC-0.5)=0.1650`

Interpretation:

- correct mentions already look stronger in the middle and SR layers
- hallucinated mentions are not only a final-layer problem

`H3` Middle-to-Late Attention Evolution:

- `middle_x_mass_change`
  - introduced vs correct: `-0.0028` vs `-0.0108`
  - `abs(AUC-0.5)=0.3333`
- `mass_change_late_minus_mid`
  - introduced vs correct: `-0.0178` vs `-0.0550`
  - `abs(AUC-0.5)=0.3223`
- `middle_to_late_image_attention_delta`
  - numerically the same direction
  - `abs(AUC-0.5)=0.3223`
- `late_image_attention_recovery_ratio`
  - introduced vs correct: `0.8766` vs `0.7002`
  - `abs(AUC-0.5)=0.2691`

Interpretation:

- the strongest signal family is not flat attention mass by itself
- the stronger story is how visual support evolves from middle to late layers

`H8` Anchor-Middle Mismatch:

- `anchor_masschange_x_late_mass`
  - introduced vs correct: `-0.0021` vs `-0.0053`
  - `abs(AUC-0.5)=0.2749`
- `firstlogitgap_x_verification_masschange`
  - introduced vs correct: `-0.0390` vs `-0.0510`
  - `abs(AUC-0.5)=0.1753`
- `anchor_adjustment_delta`
  - introduced vs correct: `1.1516` vs `0.9062`
  - `abs(AUC-0.5)=0.1642`

Interpretation:

- introduced hallucinations still look like anchor-pushed mentions with weak verification backing
- interaction terms are better than anchor strength alone

### 5.2 Weakly supported hypotheses

`H2` Late Readiness Surge:

- weak support only from relative rank-jump signals:
  - `middle_to_late_rank_improvement`: `5584.0` vs `3486.0`, `abs(AUC-0.5)=0.1158`
  - `middle_to_late_rank_jump`: `5071.5` vs `3284.0`, `0.1095`
- important boundary:
  - absolute late probability / logit are actually higher for correct mentions, not introduced hallucinations

Interpretation:

- there is some evidence for late-stage rescue from a weaker middle state
- but not enough to claim that hallucinations simply become more confident than correct mentions at late layers

`H4` Attention Diffusion:

- `middle_effective_attended_count_mean`: `162.0` vs `149.9`, `0.0833`
- `middle_norm_entropy_mean`: `0.7914` vs `0.7773`, `0.0795`

Interpretation:

- diffuse attention is real, but weak
- it should not be treated as the main hallucination story

`H6` Head Agreement:

- `middle_head_mass_cv_mean`: `1.1869` vs `1.1397`, `0.1469`

Interpretation:

- head inconsistency helps
- but it is clearly weaker than middle verification and mass-evolution signals

`H7` Layer Consistency:

- `late_shape_layer_cosine_mean`
  - introduced vs correct: `0.6713` vs `0.6900`, `0.1214`
  - removed vs persistent: `0.6573` vs `0.6898`, `0.1391`

Interpretation:

- some cross-layer mismatch exists
- but consistency is not as strong a separator as the best evolution signals

`H9` Visual Sensitivity Validation:

- `sensitivity_ratio_prob`
  - introduced vs correct: `-0.3293` vs `28.3352`
  - `abs(AUC-0.5)=0.1110`
- `top_minus_random_logit_drop`
  - introduced vs correct: `0.2458` vs `1.0591`
  - `0.0922`
- `top_mask_logit_drop`
  - introduced vs correct: `0.3000` vs `1.0908`
  - `0.0855`

Interpretation:

- correct mentions are more visually dependent than introduced hallucinations
- but sensitivity still behaves like supporting validation, not the leading separator

### 5.3 Unsupported or very weak hypotheses

`H5` Extreme Concentration / Spurious Fixation:

- `middle_top1_mass_mean`
  - hallucinated vs correct: `0.0725` vs `0.0694`
  - `abs(AUC-0.5)=0.0749`
- `middle_head_entropy_std`
  - almost no separation: `0.0122`

Interpretation:

- extreme concentration is not a reliable grounding sign
- it is also not a clean standalone hallucination-risk sign
- concentration needs verification context, otherwise it is too ambiguous

## 6. Attention Distribution Results

The attention-distribution story is now clearer:

- diffuse attention correlates with hallucination, but only weakly
- pure entropy-style signals are too small to carry a correction rule
- pure concentration-style signals are also unreliable
- head agreement and late-shape consistency help, but remain secondary

The current ranking is:

1. middle-to-late mass evolution
2. middle verification quality
3. anchor-middle interaction
4. head agreement / layer consistency
5. visual sensitivity
6. diffuse entropy alone
7. concentration alone

## 7. Layer Evolution Results

This round supports a stronger layer-evolution story than a flat `late confidence` story.

What is supported:

- correct mentions have stronger middle evidence
- introduced hallucinations show weaker middle evidence and weaker late visual recovery
- relative middle-to-late rank jump is somewhat larger for introduced hallucinations

What is not supported cleanly:

- absolute late token probability or late logit being higher for hallucinations than for correct mentions

So the safer wording is:

- hallucinations often show middle weakness plus abnormal late evolution

not:

- hallucinations simply become more confident than correct mentions in late layers

## 8. Anchor / Middle Mismatch Results

This is one of the strongest confirmed mechanism stories.

Supported pattern:

- strong anchor-side push
- weak middle verification
- weak or abnormal late visual recovery

This is why the best mismatch signals are interaction terms:

- `anchor_masschange_x_late_mass`
- `firstlogitgap_x_verification_masschange`

These are better than:

- anchor strength alone
- late mass alone

## 9. Visual Sensitivity Results

The visual sensitivity audit remains useful, but only as supporting validation.

What it supports:

- correct mentions depend more on top-attended evidence than introduced hallucinations do
- the top-attention mask matters more than the random mask for correct mentions

What it does not support:

- using sensitivity as a standalone hallucination detector
- replacing the stronger middle verification / mass-evolution signals

## 10. Control Analyses

The main positive result is that the strongest signals survive controls reasonably well.

Most robust signals:

- `middle_x_mass_change`
- `mass_change_late_minus_mid`
- `image_attention_middle_mean`
- `anchor_masschange_x_late_mass`

Examples:

- `middle_x_mass_change`
  - `introduced vs correct`, `person`: `abs(AUC-0.5)=0.3725`
  - `introduced vs correct`, low-frequency categories: `0.3462`
- `mass_change_late_minus_mid`
  - `introduced vs correct`, `person`: `0.3671`
  - `introduced vs correct`, low-frequency categories: `0.3404`
- `image_attention_middle_mean`
  - `introduced vs correct`, `person`: `0.3524`
  - `introduced vs correct`, `car`: `0.2809`

What remains unstable:

- diffuse / concentration-only signals
- some head-agreement signals across small category slices
- direct caption-source-controlled sensitivity slices where first-logit-side correct counts stay small

## 11. Best Evidence Candidates

Current strongest correction-facing candidates:

- `middle_x_mass_change`
- `mass_change_late_minus_mid`
- `middle_to_late_image_attention_delta`
- `anchor_masschange_x_late_mass`
- `image_attention_middle_mean`
- `firstlogitgap_x_verification_masschange`
- `middle_target_probability_mean`
- `obj_semantic_refinement_19_26_target_rank_mean`

Current best supporting validation signals:

- `middle_head_mass_cv_mean`
- `late_shape_layer_cosine_mean`
- `sensitivity_ratio_prob`
- `top_minus_random_logit_drop`

## 12. Unsupported Hypotheses

The strongest negative conclusion is now stable:

- diffuse attention alone is too weak
- extreme concentration alone is too ambiguous
- pure late absolute confidence does not support a simple `hallucinations get stronger late` claim

## 13. What This Proves

This audit does support the following claims:

- hallucinated object mentions often have weaker middle visual verification
- middle-to-late attention evolution is one of the strongest hallucination evidence families
- anchor-side push plus weak verification is a real first-logit-side hallucination pattern
- removed and introduced hallucinations should not be treated as exactly the same failure mode

## 14. What This Does Not Prove

This audit does not prove:

- that any current signal is already a deployable runtime rule
- that a single scalar can safely decide rollback, suppression, or correction
- that late absolute token confidence alone explains hallucination
- that attention concentration by itself is grounding

## 15. Whether Current Evidence Supports Correction

Current evidence is now good enough for:

- mechanism explanation
- prioritizing future correction-facing signal families
- ruling out weak families

Current evidence is still not good enough for:

- an automatic runtime selector
- a new decoding intervention without a fresh user-approved design step

## 16. Next Recommended Research Direction

The current safe direction is:

1. keep fixed `first_logit / early-anchor` frozen as the decoding reference
2. keep the active line on hallucination evidence discovery
3. prioritize the verified families:
   - middle verification
   - middle-to-late attention evolution
   - anchor-middle mismatch interaction
4. treat head agreement and visual sensitivity as supporting validation
5. do not start a new correction method unless the signal story is discussed and approved first
