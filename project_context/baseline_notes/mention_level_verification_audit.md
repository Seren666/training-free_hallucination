# Mention-Level Verification Audit

> Date: 2026-05-03
> Scope: offline mention-level verification audit over existing object-event labels and completed internal-signal probes. No new decoding, no correction, no reranking, no second-pass rewrite.

## 1. Motivation

The active research question has shifted again:

- not "what new decoding rule should be added"
- not "what guard should clip object tokens"
- not "how to replace fixed `first_logit / early-anchor`"

The current question is narrower and more diagnostic:

- given a generated caption and one object mention inside it
- can internal model evidence tell us whether that mention is hallucinated

This is important because the next acceptable method discussion, if any, should rest on a stable mention-level verification story rather than another broad runtime heuristic.

## 2. Dataset Construction

This round reused the existing balanced `4000`-event object-local audit subset rather than rebuilding from the full event table.

Why that choice was acceptable:

- it already contains the core middle-rank, attention, layer-group, and anchor signals
- it already aligns with the prior hypothesis audit
- it avoids any new full-scale teacher-forcing rerun

Dataset size:

- total events: `4000`
- per class:
- `correct_object_mention`: `1000`
- `introduced_hallucination`: `1000`
- `removed_hallucination`: `1000`
- `persistent_hallucination`: `1000`
- caption source:
- `regular`: `2937`
- `first_logit`: `1063`

Limitations:

- visual-sensitivity fields only cover the previously completed `800`-event sensitivity subset
- so sensitivity-family signals carry high missing rate in the main binary task
- the `first_logit`-side `correct_object_mention` slice is still small: only `63` events

## 3. Event Labels

The main binary task is:

- `hallucinated = 1`
- `introduced_hallucination`
- `removed_hallucination`
- `persistent_hallucination`
- `hallucinated = 0`
- `correct_object_mention`

The multiclass label is retained for failure-mode analysis:

- `correct_object_mention`
- `introduced_hallucination`
- `removed_hallucination`
- `persistent_hallucination`

## 4. Signal Families

The mention-level audit evaluates five signal families.

### 4.1 Middle visual verification

- `middle_target_rank_mean`
- `middle_target_probability_mean`
- `image_attention_middle_mean`
- `hidden_image_cosine_middle_mean`
- `VE 5-18` and `SR 19-26` rank / probability signals

### 4.2 Middle-to-late evolution

- `mass_change_late_minus_mid`
- `middle_to_late_image_attention_delta`
- `late_image_attention_recovery_ratio`
- `middle_x_mass_change`
- `middle_to_late_rank_jump`
- `middle_to_late_prob_jump`

### 4.3 Anchor-middle mismatch

- `anchor_target_token_rank`
- `anchor_adjustment_delta`
- `firstlogitgap_x_verification_masschange`
- `anchor_masschange_x_late_mass`
- `anchor_support_strong_middle_weak_composite`

### 4.4 Attention shape / head agreement

- `middle_norm_entropy_mean`
- `middle_effective_attended_count_mean`
- `middle_top1_mass_mean`
- `middle_peak_ratio_mean`
- `middle_head_mass_cv_mean`
- `middle_head_entropy_std`
- `middle_head_top10_overlap_mean`

### 4.5 Visual sensitivity

- `top_mask_logit_drop`
- `top_minus_random_logit_drop`
- `sensitivity_ratio_prob`
- `top_mask_rank_delta`

## 5. Single-Signal Results

### 5.1 Primary binary task: hallucinated vs correct

Strongest single signals:

- `middle_x_mass_change`
- hallucinated vs correct: `-0.0042` vs `-0.0107`
- `abs(AUC-0.5)=0.2745`
- `mass_change_late_minus_mid`
- `-0.0243` vs `-0.0545`
- `0.2701`
- `middle_to_late_image_attention_delta`
- same direction
- `0.2701`
- `anchor_masschange_x_late_mass`
- `-0.0024` vs `-0.0053`
- `0.2514`
- `late_image_attention_recovery_ratio`
- `0.8462` vs `0.7110`
- `0.2283`
- `image_attention_middle_mean`
- `0.1519` vs `0.1836`
- `0.2155`

Interpretation:

- mention-level verification is feasible at a diagnostic level
- the strongest signals are still not entropy or sensitivity
- they are still middle verification plus middle-to-late evolution plus anchor interaction

### 5.2 Introduced vs correct

Strongest single signals:

- `middle_x_mass_change`: `0.3198`
- `mass_change_late_minus_mid`: `0.3113`
- `middle_to_late_image_attention_delta`: `0.3113`
- `anchor_masschange_x_late_mass`: `0.2749`
- `image_attention_middle_mean`: `0.2616`
- `late_image_attention_recovery_ratio`: `0.2612`

Interpretation:

- introduced hallucinations remain the clearest first-logit-side verification failure pattern

### 5.3 Removed vs correct

Strongest single signals:

- `middle_x_mass_change`: `0.3252`
- `mass_change_late_minus_mid`: `0.3233`
- `middle_to_late_image_attention_delta`: `0.3233`
- `anchor_masschange_x_late_mass`: `0.3035`
- `late_image_attention_recovery_ratio`: `0.2926`

Interpretation:

- removed hallucinations are at least as separable as introduced hallucinations
- this is consistent with the idea that many removed mentions are late-stage over-mentions lacking stable verification

### 5.4 Persistent vs correct

Persistent hallucinations are harder:

- best single signal is `anchor_target_token_rank`: `0.2173`, but in the opposite direction from the simple anchor-support expectation
- best direction-consistent signals are:
- `middle_x_mass_change`: `0.1786`
- `anchor_masschange_x_late_mass`: `0.1757`
- `mass_change_late_minus_mid`: `0.1757`

Interpretation:

- persistent hallucinations are still detectable above chance
- but they are less clean than introduced or removed hallucinations

### 5.5 Cross-hallucination comparisons

`introduced vs removed` is weaker:

- best single signal:
- `anchor_support_strong_middle_weak_composite`: `0.1102`

`persistent vs removed` is stronger:

- `mass_change_late_minus_mid`: `0.2046`
- `middle_x_mass_change`: `0.1986`
- `late_image_attention_recovery_ratio`: `0.1949`

Interpretation:

- removed and persistent hallucinations are meaningfully different
- introduced and removed are also different, but less dramatically under the current features

## 6. Composite Evidence Results

The composites were preregistered, equal-weight, and not learned from labels.

### 6.1 Primary binary task

Best composites:

- `composite_middle_to_late_abnormal_evolution`
- hallucinated vs correct: `0.2684`
- `composite_combined_evidence_consistency`
- `0.2361`
- `composite_middle_verification_deficit`
- `0.2150`
- `composite_anchor_middle_mismatch`
- `0.1891`

### 6.2 Comparison to best single signal

Important boundary:

- best single on the primary task:
- `middle_x_mass_change`: `0.2745`
- best composite on the primary task:
- `composite_middle_to_late_abnormal_evolution`: `0.2684`

So:

- the composite evidence is useful
- but it does not beat the best single signal

The same is true for `introduced vs correct`:

- best single: `middle_x_mass_change = 0.3198`
- best composite: `composite_middle_to_late_abnormal_evolution = 0.3091`

Interpretation:

- equal-weight diagnostic composites help summarize the evidence
- but they do not unlock a stronger verification boundary than the best evolution signals already provide

## 7. Control Analyses

### 7.1 Category-controlled

The strongest signals remain stable across both high-frequency and low-frequency categories.

Examples for `introduced vs correct`:

- `middle_x_mass_change`
- low-frequency: `0.3354`
- high-frequency: `0.3139`
- `mass_change_late_minus_mid`
- low-frequency: `0.3315`
- high-frequency: `0.3033`
- `image_attention_middle_mean`
- strong within `person`, `car`, and `sink`

Boundary:

- some very small category slices produce `0.5` artifacts, especially in sensitivity signals
- those should not be over-interpreted

### 7.2 Mention-position-controlled

The best evolution signals remain strong across early, middle, and late mention bins.

For `introduced vs correct`:

- early bin:
- `middle_x_mass_change = 0.2483`
- `mass_change_late_minus_mid = 0.2452`
- middle and late bins still keep the correct direction, though sensitivity becomes more visible in later bins

Interpretation:

- the evolution signal is not just a trivial `hallucinations appear later` effect

### 7.3 Mention-length-controlled

The best signals remain strong for both:

- `single_token`
- `multi_token`

Examples:

- `middle_x_mass_change`
- multi-token: `0.3252`
- single-token: `0.3094`
- `mass_change_late_minus_mid`
- multi-token: `0.3228`
- single-token: `0.2934`

Interpretation:

- the mention-level verification story is not just a tokenization artifact

### 7.4 Caption-source-controlled

This is the noisiest control, mainly because `first_logit`-side correct mentions are scarce.

For `introduced vs correct`, `caption_source=first_logit`:

- `anchor_masschange_x_late_mass = 0.1330`
- `top_minus_random_logit_drop = 0.1120`
- `top_mask_logit_drop = 0.1027`
- `mass_change_late_minus_mid = 0.0984`

Interpretation:

- the direction mostly survives
- but the first-logit-side control slice is still underpowered

### 7.5 Frequency-controlled

The strongest evolution signals remain high in both bins:

- low-frequency objects:
- `middle_x_mass_change = 0.3354`
- `mass_change_late_minus_mid = 0.3315`
- high-frequency objects:
- `middle_x_mass_change = 0.3139`
- `mass_change_late_minus_mid = 0.3033`

Interpretation:

- the main result is not only driven by common COCO hallucination categories

## 8. Best Mention-Level Verification Candidates

Current strongest mention-level verification candidates are:

- `middle_x_mass_change`
- `mass_change_late_minus_mid`
- `middle_to_late_image_attention_delta`
- `composite_middle_to_late_abnormal_evolution`
- `anchor_masschange_x_late_mass`
- `composite_combined_evidence_consistency`
- `late_image_attention_recovery_ratio`
- `image_attention_middle_mean`
- `composite_middle_verification_deficit`
- `composite_anchor_middle_mismatch`

These are the only signals that currently satisfy all of the following at once:

- useful on the main hallucinated-vs-correct task
- stable after category / position / length / frequency controls
- interpretable in the same mechanism story

## 9. Signals That Are Only Supporting Validation

These are useful, but they should not carry the main verification decision by themselves:

- `middle_head_mass_cv_mean`
- `sensitivity_ratio_prob`
- `top_minus_random_logit_drop`
- `top_mask_logit_drop`

Why they are secondary:

- lower coverage
- weaker effect size
- more instability under small controlled slices

## 10. Unsupported or Weak Signals

Weak or unstable families:

- diffuse attention alone
- pure concentration alone
- hidden-image cosine as a standalone main separator
- late probability jump as a direct verification signal
- direct anchor rank without context

Important subtlety:

- some of these still have explanatory value
- but they are not stable enough to be the main mention-level verification handle

## 11. What This Verifies

This audit does verify that:

- hallucinated object mentions can be identified above chance using internal signals alone
- the most useful signals are mention-local verification signals, not broad image-level scalars
- middle-to-late evolution is the strongest current mention-level family
- anchor-middle mismatch contributes real verification value
- verification is easier for `introduced` and `removed` than for `persistent`

## 12. What It Does Not Verify

This audit does not verify:

- a runtime selector
- a correction rule
- a second-pass rewriting policy
- a reranking policy
- a learned mention classifier

It also does not show that the best diagnostic composite clearly exceeds the best single signal.

## 13. Whether This Supports Second-Pass Correction

Current answer:

- yes for a design discussion
- no for immediate implementation

Why `yes` for discussion:

- mention-level verification is now supported empirically
- the strongest signals are stable across several control views
- the signal family is narrower and more local than the failed guard-family routes

Why still `no` for implementation:

- the primary binary separation is still moderate, not overwhelming
- first-logit-side caption-source control remains sample-limited
- persistent hallucinations remain harder than introduced or removed
- composites do not clearly dominate the best single signal

So the current boundary should be:

- the project can discuss a second-pass correction design next
- but Codex should not start designing or implementing it without explicit user approval

## 14. Next Recommendation

1. keep fixed `first_logit / early-anchor` as the strongest generation baseline
2. keep hallucination evidence discovery as the main active research line
3. treat mention-level verification as now feasible at a diagnostic level
4. if the user wants to continue, the next step can be a user-approved second-pass correction design discussion
5. do not let Codex jump directly from this audit to a correction implementation
