# Early-Anchor Internal Signal Audit

> Date: 2026-05-02
> Scope: paired internal-signal audit comparing the fixed `regular` trajectory with the fixed `first_logit / early-anchor` trajectory, without introducing any new decoding intervention.

## 1. Why This Audit

The current project focus has moved away from:

- another token-level clipping rule
- another object-suppression guard
- another anchor-cleaning variant

That change is now well-supported by the negative pilot sequence:

- `object_safe_anchor`
- `attention_gated_attnanchor`
- `candidate_local_guard`
- `middle_verified`
- `middle_refined`

All of them failed to beat fixed `first_logit / early-anchor`.

At the same time, the recent signal audits gave a clearer mechanism story:

- correct object mentions already look stronger in the middle layers
- `mass_change_late_minus_mid` is stronger than simple diffuse-attention heuristics
- attention-guided visual sensitivity is informative, but weaker than the best middle-mass / mass-evolution signals

So the right next question is no longer:

- "what token should be clipped?"

It is:

- "how do the internal verification dynamics differ between the normal trajectory and the early-anchor trajectory?"

## 2. Audit Setup

This round keeps the decoding side fixed:

- `regular` is the normal trajectory
- fixed `first_logit / early-anchor` is the reference trajectory
- no prompt change
- no model change
- no new generation rule

The analysis target is the object-event level, with special care around which events are genuinely pairable across trajectories.

### 2.1 Shared events

These are the events where a direct paired `regular` vs `first_logit` comparison is meaningful:

- `correct_object_mention`
- `persistent_hallucination`

For these, the same image-level object event exists under both trajectories, so we can compare:

- middle image attention
- middle-to-late attention evolution
- anchor-plus-verification interactions
- visual sensitivity changes before vs after early-anchor

### 2.2 Asymmetric events

These are not true paired two-trajectory events:

- `introduced_hallucination`
- `removed_hallucination`

Interpretation therefore has to stay asymmetric:

- `introduced_hallucination` is a `first_logit`-side mention
- `removed_hallucination` is a `regular`-side mention

They are still useful, but they should be compared as one-sided active trajectories rather than treated as if both trajectories generated the same mention.

## 3. Signal Families

This audit focuses on four families.

### 3.1 Verification mass and evolution

- `middle_image_attention_mean`
- `late_image_attention_mean`
- `mass_change_late_minus_mid`
- middle-to-late image-attention delta
- late image-attention recovery

### 3.2 Anchor and confidence

- `anchor_adjustment_delta`
- `anchor_x_mass_change`
- first-logit confidence gap, where available
- token-probability / margin signals

### 3.3 Interaction signals

- `middle_image_attention_mean x mass_change_late_minus_mid`
- `anchor_x_mass_change x late_image_attention`
- `first_logit_gap x verification_mass_change`
- `visual_sensitivity x attention_mass_evolution`

### 3.4 Control-aware sensitivity

- top-attended patch mask vs random-patch mask
- same attention-mass-bin comparison
- same mention-length comparison
- early-anchor before/after sensitivity delta on shared events

## 4. Evidence Boundary

This audit is meant to separate two kinds of evidence:

### 4.1 Correction-facing signals

These would need to remain useful across multiple views at once:

- active `introduced vs correct` separation
- shared-event paired `regular -> first_logit` delta
- control-aware sensitivity checks

Only signals that stay strong across those slices deserve to be considered future correction-facing handles.

### 4.2 Supporting validation signals

Some signals may still be valuable even if they are not stable enough to drive a future correction unit directly.

Examples:

- weak but consistent top-vs-random masking effects
- modest head-consistency effects
- concentration or entropy signals that help interpretation but do not separate robustly

## 5. Coverage

This audit reuses the already frozen single-trajectory subsets and adds alternate-trajectory probes only where a real paired comparison is meaningful.

### 5.1 Frozen shape subset

- existing attention-shape rows: `1982`
- counts:
  - `correct_object_mention`: `496`
  - `introduced_hallucination`: `496`
  - `removed_hallucination`: `495`
  - `persistent_hallucination`: `495`

### 5.2 Alternate paired shape subset

Only shared events are probed on the alternate trajectory:

- alternate paired rows total: `905`
- counts:
  - `correct_object_mention`: `410`
  - `persistent_hallucination`: `495`

This means:

- `introduced_hallucination` remains a `first_logit`-side one-trajectory event
- `removed_hallucination` remains a `regular`-side one-trajectory event
- only `correct` and `persistent` can support a genuine paired `regular -> first_logit` delta

### 5.3 Frozen sensitivity subset

- existing sensitivity rows: `800`
- counts:
  - `correct_object_mention`: `200`
  - `introduced_hallucination`: `200`
  - `removed_hallucination`: `200`
  - `persistent_hallucination`: `200`

### 5.4 Alternate paired sensitivity subset

- alternate paired rows total: `372`
- counts:
  - `correct_object_mention`: `172`
  - `persistent_hallucination`: `200`

### 5.5 Practical implication

The audit therefore has two complementary lenses:

- asymmetric active-event comparison:
  - `introduced_first_logit_only`
  - `removed_regular_only`
  - trajectory-specific `correct` references
- true paired shared-event comparison:
  - `correct_object_mention`
  - `persistent_hallucination`

## 6. Main Results

The strongest result of this round is not a large paired `regular -> first_logit` trajectory delta.

The strongest result is that, on the `first_logit` side itself, introduced hallucinations still look like weakly verified mentions under middle-to-late visual evidence.

### 6.1 Strongest introduced-vs-correct first-logit-side signals

Best separators for `introduced_first_logit_only vs correct_first_logit`:

- `middle_image_attention_mean x mass_change_late_minus_mid`
  - means: `-0.0028` vs `-0.0117`
  - `abs(AUC-0.5)=0.3612`
- `mass_change_late_minus_mid`
  - means: `-0.0178` vs `-0.0594`
  - `abs(AUC-0.5)=0.3541`
- `middle_to_late_image_attention_delta`
  - numerically the same direction as above
  - `abs(AUC-0.5)=0.3541`
- `first_logit_gap x verification_mass_change`
  - means: `-0.0131` vs `-0.0411`
  - `abs(AUC-0.5)=0.3319`
- `anchor_x_mass_change x late_image_attention`
  - means: `-0.0018` vs `-0.0059`
  - `abs(AUC-0.5)=0.3123`
- `late_image_attention_recovery_ratio`
  - means: `0.8766` vs `0.6860`
  - `abs(AUC-0.5)=0.2996`
- `anchor_x_mass_change`
  - means: `-0.0176` vs `-0.0492`
  - `abs(AUC-0.5)=0.2926`
- `middle_image_attention_mean`
  - means: `0.1422` vs `0.1853`
  - `abs(AUC-0.5)=0.2858`

Interpretation:

- the best story is still verification quality and its evolution
- introduced first-logit-side mentions recover less visual support from middle to late
- raw middle mass matters, but mass evolution and interaction terms matter more

### 6.2 Removed-vs-introduced is much weaker

`removed_regular_only vs introduced_first_logit_only` is much less clean:

- best signal is still `anchor_adjustment_delta`, but only `abs(AUC-0.5)=0.0895`
- next are `middle_target_rank_mean` at `0.0729`
- and `middle_image_attention_mean` at `0.0623`

Interpretation:

- removed and introduced are both hard cases
- once the comparison becomes cross-trajectory and asymmetric, separation weakens quickly
- this is one reason image-level or rollback-style selectors have stayed unstable

### 6.3 Shared-event paired deltas are small

For true shared events, `regular -> early-anchor` internal shifts are present but small.

Correct shared mentions:

- middle image attention mean:
  - `0.1899 -> 0.1878`
  - delta `-0.0022`
- mass change late minus middle:
  - `-0.0620 -> -0.0616`
  - delta `+0.0004`
- late-image-attention recovery ratio:
  - `0.6778 -> 0.6774`
  - delta `-0.0005`

Persistent hallucinations:

- middle image attention mean:
  - `0.1634 -> 0.1606`
  - delta `-0.0029`
- mass change late minus middle:
  - `-0.0372 -> -0.0357`
  - delta `+0.0015`
- late-image-attention recovery ratio:
  - `0.7771 -> 0.7836`
  - delta `+0.0065`

Best paired-delta separators for `persistent vs correct` are weak:

- `anchor_masschange_x_late_mass`: `abs(AUC-0.5)=0.0461`
- `anchor_x_mass_change`: `0.0403`
- `top1_top2_probability_margin`: `0.0385`

Interpretation:

- early-anchor does not drastically rewrite shared-event internal dynamics
- the bigger signal remains whether a mention is weakly verified in the first place
- that is a weaker foundation for any direct trajectory-switch rule than the asymmetric `introduced vs correct` story

## 7. Control-Aware Sensitivity

The control-aware sensitivity results are useful, but they behave more like supporting validation than primary separation.

### 7.1 First-logit-side introduced vs correct

Key first-logit-side sensitivity results:

- `top_minus_random_logit_drop`
  - introduced: `0.2458`
  - correct: `1.0550`
  - `abs(AUC-0.5)=0.0721`
- `top_mask_logit_drop`
  - introduced: `0.3000`
  - correct: `1.1080`
  - `abs(AUC-0.5)=0.0698`
- `sensitivity_ratio_logit`
  - introduced: `3.0185`
  - correct: `16.7507`
  - `abs(AUC-0.5)=0.0674`

The strongest sensitivity-side feature is actually an interaction:

- `visual_sensitivity_ratio_prob x mass_change_late_minus_mid`
  - `abs(AUC-0.5)=0.0966`

Interpretation:

- correct first-logit-side mentions do depend more on the attended region than introduced hallucinations
- but pure sensitivity remains weaker than the best mass-evolution features

### 7.2 Same attention-mass bins

Within all three middle-attention-mass bins, correct still beats introduced on top-vs-random probability drop:

- low-mass bin:
  - correct `0.0364`
  - introduced `-0.0019`
  - `abs(AUC-0.5)=0.0233`
- middle-mass bin:
  - correct `0.0853`
  - introduced `0.0374`
  - `0.0066`
- high-mass bin:
  - correct `0.0892`
  - introduced `0.0498`
  - `0.0394`

Interpretation:

- sensitivity keeps the same direction after coarse mass control
- but its standalone separation is still small inside matched mass bins

### 7.3 Same mention-length groups

Within all mention-length groups, correct again stays above introduced:

- one-token mentions:
  - correct `0.0843`
  - introduced `0.0069`
  - `abs(AUC-0.5)=0.0690`
- two-token mentions:
  - correct `0.0690`
  - introduced `0.0290`
  - `0.0376`
- three-plus-token mentions:
  - correct `0.0824`
  - introduced `0.0315`
  - `0.0176`

Interpretation:

- the direction is robust
- but the effect remains secondary compared with attention-mass evolution

### 7.4 Shared-event sensitivity deltas are weak

Best paired sensitivity deltas for `persistent vs correct`:

- `sensitivity_ratio_prob`: `abs(AUC-0.5)=0.0502`
- `top_mask_probability_drop`: `0.0386`
- `top_minus_random_probability_drop`: `0.0379`

Interpretation:

- early-anchor does not create a large paired sensitivity shift on shared mentions
- sensitivity is therefore more useful as a supporting verification readout than as a direct trajectory-delta controller

## 8. Correction-Facing vs Supporting Signals

### 8.1 Best correction-facing candidates

The best correction-facing signals from this round are still descriptive only, but they are now clearer:

- `mass_change_late_minus_mid`
- middle-to-late image-attention delta
- `middle_image_attention_mean x mass_change_late_minus_mid`
- `first_logit_gap x verification_mass_change`
- `anchor_x_mass_change x late_image_attention`
- `anchor_x_mass_change`
- `middle_image_attention_mean`

Why these are the strongest candidates:

- they dominate the first-logit-side `introduced vs correct` comparison
- they tell a coherent story about weak middle verification and weak late recovery
- they are more stable than pure diffuse-entropy or pure concentration heuristics

### 8.2 Why they are not yet runtime-ready

The same signals do not stay strong as true shared-event paired `regular -> first_logit` deltas.

That is the key boundary from this round:

- within-trajectory verification quality is informative
- but early-anchor does not produce a large enough shared-event internal shift to justify a direct trajectory-delta control rule yet
- so the current signal story is still not stable enough for a new runtime selector or rollback rule

### 8.3 Supporting validation signals

Useful, but weaker:

- top-vs-random attention-guided sensitivity
- same-mass-bin sensitivity comparisons
- same-mention-length sensitivity comparisons
- paired sensitivity deltas
- first-logit confidence gap by itself
- `removed vs introduced` asymmetric comparisons

Their value is:

- confirm that correct mentions are more visually dependent than introduced hallucinations
- support the verification story
- but not replace the stronger attention-mass-evolution signals

## 9. Current Boundary

This audit does not support a new runtime correction rule yet.

What it does support:

- the strongest signals remain verification-surface signals, especially middle-to-late visual support evolution
- interaction terms are more informative than flat entropy or concentration heuristics
- visual sensitivity is useful supporting evidence, not the primary separator

What it does not yet support:

- a strong shared-event trajectory-delta controller
- a claim that early-anchor drastically rewrites internal verification for already-shared mentions
- a new token-level clipping, object-suppression, or broad-guard runtime family

The next acceptable step would still need all of the following:

- the same signal stays strong across asymmetric event comparison and true shared-event paired deltas
- the control-aware sensitivity checks support the same direction
- the failure modes are concrete rather than anecdotal

Until then, the safe position remains:

- keep fixed `first_logit / early-anchor` as the decoding reference
- keep internal signal discovery as the active line
- do not jump from a descriptive signal straight into another decoding intervention
- do not continue token-level clipping, object suppression, or broad guard-family expansion
