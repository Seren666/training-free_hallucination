# Attention Distribution Hallucination Audit

> Date: 2026-05-02
> Scope: offline signal audit after stopping the token-level clipping / object-suppression / anchor-cleaning guard family.

## 1. Why Attention Distribution Audit

The current project focus is no longer "keep tuning fixed `first_logit`" or "try one more guard."

What changed:

- fixed `first_logit / early-anchor` remains the strongest decoding baseline
- every guard-style follow-up failed to beat it
- the next useful question is not "how do we clip another token family"
- the next useful question is "what internal signal actually tracks hallucination"

This round therefore shifts from correction to measurement:

- inspect the shape of image attention around object mentions
- test whether attended image patches are causally useful for the object token under teacher forcing

## 2. Relation To Early-Anchor / Middle-Layer Findings

This audit is downstream of two already-established findings:

- object-local signals are more informative than coarse image-level scalars
- correct object mentions are already stronger in middle-layer rank / probability / image attention

The specific question here was narrower:

- does the distribution shape of visual attention add useful signal beyond raw attention mass
- do hallucinated object tokens actually depend less on the regions they attend to

## 3. Subset Construction

Subset source:

- reused the existing seed-55 balanced `object_local_probe_subset.csv`
- that subset was already derived from `object_event_table.csv`
- then re-exported it to `attention_shape_audit_subset.csv` with round-robin ordering across event types

Target design:

- `correct_object_mention`
- `introduced_hallucination`
- `removed_hallucination`
- `persistent_hallucination`

Planned maximum:

- up to `1000` events per class

What actually ran for this round:

- attention-shape probe frozen at `1982` events total
- counts: `correct=496`, `introduced=496`, `removed=495`, `persistent=495`

Why it stopped there:

- the probe had already exceeded the fallback bar of `300+` events per class
- signal directions had stabilized
- continuing to the full `4000` rows would have cost roughly another `45` minutes without changing whether Stage 4 should proceed

Visual sensitivity subset:

- `200` events per class
- total `800` events

## 4. Attention Shape Metrics

Per object event, the shape probe extracted aggregated statistics only:

- middle and late image-attention mass
- normalized entropy
- effective attended token count
- top-1 / top-5 / top-10 / top-5%-patch attention mass
- peak ratio
- HHI / Gini concentration
- head overlap and head mass CV
- middle-to-late shape change
- centroid drift
- middle-to-late distribution cosine

It also merged already useful signals from earlier audits:

- target token rank / probability
- anchor support
- hidden-image cosine
- middle-rank lens statistics

## 5. Attention Shape Results

Final balanced shape counts:

- `correct_object_mention`: `496`
- `introduced_hallucination`: `496`
- `removed_hallucination`: `495`
- `persistent_hallucination`: `495`

Most useful `introduced vs correct` separators:

- `mass_change_late_minus_mid`: `abs(AUC-0.5)=0.3223`
- `middle_image_attention_mean`: `0.2761`
- `anchor_x_mass_change`: `0.2690`
- `anchor_over_middle_mass`: `0.2384`
- `anchor_target_token_rank`: `0.2104`

Best plain attention-shape-only signals were weaker:

- `middle_head_mass_cv_mean`: `0.1469`
- `middle_gini_mean`: `0.1404`
- `middle_head_top10_overlap_mean`: `0.0954`
- `middle_norm_entropy_mean`: `0.0795`
- `middle_to_late_shape_cosine_mean`: `0.0621`

Group means reinforce the same story:

- introduced mentions have lower middle image attention than correct
  - `0.1422` vs `0.1834`
- introduced mentions have weaker late-minus-middle mass decrease
  - `-0.0178` vs `-0.0550`
- introduced mentions are slightly more diffuse
  - `middle_norm_entropy_mean 0.7914` vs `0.7773`
- but entropy alone is not the main separator

## 6. Visual Sensitivity Probe

Probe design:

- use the middle-attention top `5%` patches from the shape probe
- mask those patches
- also mask a random control set with the same patch count
- re-score the same object token under teacher forcing

This was done on `800` events total:

- `200` per event type

No masked images were saved.

## 7. Visual Sensitivity Results

Counts:

- `correct_object_mention`: `200`
- `introduced_hallucination`: `200`
- `removed_hallucination`: `200`
- `persistent_hallucination`: `200`

Key group-level means:

- top-attention mask logit drop:
  - correct: `1.0908`
  - introduced: `0.3000`
  - removed: `0.5482`
  - persistent: `0.4949`

- top-minus-random logit drop:
  - correct: `1.0591`
  - introduced: `0.2458`
  - removed: `0.4715`
  - persistent: `0.3979`

Best `introduced vs correct` sensitivity signals:

- `sensitivity_ratio_prob`: `abs(AUC-0.5)=0.1110`
- `middle_head_top10_overlap_mean`: `0.0972`
- `top_minus_random_logit_drop`: `0.0922`
- `top_mask_logit_drop`: `0.0855`

Best `hallucinated vs correct` sensitivity signals:

- `middle_target_probability_mean`: `0.1373`
- `anchor_adjustment_delta`: `0.1061`
- `middle_head_top10_overlap_mean`: `0.0905`
- `top_minus_random_logit_drop`: `0.0790`

## 8. Which Signals Best Separate Hallucinated vs Correct Object Mentions

Current strongest families in this round:

1. middle-to-late mass evolution
2. middle image attention mass
3. anchor-plus-shape interaction
4. middle-rank / late-rank style token-confidence signals

Current weaker families:

- raw diffuse entropy by itself
- pure concentration metrics by themselves
- simple attention-guided sensitivity without control-aware combination

The most useful concise summary is:

- "middle visual support is weaker for hallucinated mentions"
- "late-minus-middle attention evolution is even more informative"
- "diffuse attention exists, but is not the main story"

## 9. Whether Attention Uniformity Is A Useful Hallucination Signal

Only weakly.

Evidence:

- `middle_norm_entropy_mean` on `introduced vs correct`: `abs(AUC-0.5)=0.0795`
- `middle_norm_entropy_mean` on `hallucinated vs correct`: `0.0368`

Interpretation:

- hallucinated mentions are somewhat more diffuse on average
- but diffuse / uniform attention alone is much weaker than:
  - middle image attention mass
  - middle-to-late mass change
  - anchor interaction signals

So "diffuse attention = hallucination" is too crude.

## 10. Whether Extreme Concentration Is Helpful Or Suspicious

In this round, extreme concentration leaned more hallucination-like than correct-like.

Evidence:

- `middle_top1_mass_mean` is slightly higher in hallucinated mentions than correct
  - `0.0725` vs `0.0694`
- the analysis summary marked concentration signals as leaning toward hallucinated mentions on `hallucinated vs correct`

Interpretation:

- strong concentration is not automatically a sign of correct grounding
- it can also reflect fixation on a plausible but misleading region

That said, pure concentration signals were still weaker than mass-evolution and mass-level signals.

## 11. Whether Head / Layer Consistency Matters

Yes, but not equally.

Head consistency:

- `middle_head_mass_cv_mean` was one of the better shape-only signals
  - `introduced vs correct abs(AUC-0.5)=0.1469`
- `middle_head_top10_overlap_mean` also helped
  - `0.0954` in the shape audit
  - `0.0972` on the sensitivity subset

Layer consistency mattered more:

- `mass_change_late_minus_mid` was the strongest signal overall in the shape audit
  - `introduced vs correct abs(AUC-0.5)=0.3223`
- `late_shape_layer_cosine_mean` also helped for `persistent vs removed`

So the useful consistency signal is less "all heads agree" and more "does the visual support evolve like a correct mention from middle to late."

## 12. Whether This Supports Future Correction Methods

Yes, but with an important boundary.

Supported:

- future correction methods should look at middle-to-late verification dynamics
- middle attention mass and mass evolution are stronger than coarse entropy heuristics
- top-attention masking shows that correct mentions are more visually sensitive than introduced hallucinations on average

Not yet supported:

- a simple runtime rule based only on diffuse entropy
- a simple runtime rule based only on masking sensitivity
- immediate return to token-level clipping

Current evidence is stronger for:

- verification-style signals
- offline risk scoring
- candidate-level or mention-level auditing

than for a one-line runtime gate.

## 13. Caveats

- the attention-shape probe was frozen at `1982` events, not the full planned `4000`
- this was still above the fallback `300+` per class bar and above the `200/class` sensitivity bar
- only one model / prompt / image processor stack was used
- the sensitivity probe used top `5%` patch masking, not a sweep over masking styles
- random-mask control helped, but was still a simple control
- no object-box GT was used for patch supervision
- these are offline separability results, not a deployed runtime selector

## 14. Next Recommendation

Do not go back to another clipping or object-suppression variant.

Recommended next step:

1. keep fixed `first_logit / early-anchor` fixed as the decoding reference
2. continue internal signal discovery
3. prioritize signals built from:
   - middle image attention mass
   - middle-to-late mass change
   - anchor-plus-verification interaction
   - controlled visual sensitivity
4. only design a new correction method when it clearly beats simple mass and mass-evolution signals in offline audit

Current bottom line:

- attention shape is useful
- diffuse entropy alone is not enough
- visual sensitivity is informative but not yet stronger than the best shape / mass signals
- middle-to-late verification dynamics currently look like the most promising correction-facing signal family
