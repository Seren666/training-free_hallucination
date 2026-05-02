# Layer-Wise Anchor Audit

> Date: 2026-05-03
> Scope: layer-wise early/middle anchor audit, offline layer-ensemble anchor comparison, one Branch A 1000-image pilot, and offline middle-late mismatch feasibility.

## 1. Motivation

The current question was no longer whether another token-level guard could beat fixed `first_logit / early-anchor`.

That family already failed repeatedly:

- `object_safe_anchor`
- `attention_gated_attnanchor`
- `candidate_local_guard`
- `middle_verified`
- `middle_refined`

So this round shifted to a different question:

- which decoder layer groups contain the cleanest object support signal
- whether a layer-ensemble anchor could outperform the fixed final-layer first-logit anchor
- whether middle-late mismatch is strong enough to justify a later trigger-style method

## 2. Literature-Inspired Layer Grouping

This round treated the 32 decoder layers of LLaVA-1.5-7B with a working grouping, not a proven partition:

- `shallow_0_4`
- `visual_enrichment_5_18`
- `semantic_refinement_19_26`
- `middle_all_5_26`
- `late_27_31`
- final LM-head logits

The point was to test which groups were actually informative under the current COCO-CHAIR object-event audit, not to hard-commit to a universal layer taxonomy.

## 3. Layer-Wise Audit

The layer-group audit reused the existing balanced 4000-event subset:

- `correct_object_mention = 1000`
- `introduced_hallucination = 1000`
- `removed_hallucination = 1000`
- `persistent_hallucination = 1000`

Main introduced-vs-correct findings:

- strongest object-step logit-lens signal:
  - `obj_late_27_31_target_logit_mean`
  - `abs(AUC-0.5)=0.2523`
  - means `15.4720 vs 18.3254`
- strongest attention signal:
  - `attn_shallow_0_4_image_mass_mean`
  - `abs(AUC-0.5)=0.3250`
  - means `0.2063 vs 0.2360`
- second-best attention signal:
  - `attn_visual_enrichment_5_18_image_mass_mean`
  - `abs(AUC-0.5)=0.3085`
- strongest middle-late transition signal:
  - `middle_to_late_mass_change`
  - `abs(AUC-0.5)=0.2574`
- strongest anchor-side signal:
  - `anchor_late_27_31_target_logit_mean`
  - `abs(AUC-0.5)=0.2442`

Interpretation:

- correct objects still show stronger visual support before the final layer
- but the cleanest target-logit separation in this audit sits in `late_27_31`, not in the earlier middle groups
- shallow / early-middle layers help more from the attention-mass side than from direct target-logit support

## 4. Fusion Methods Compared

Three offline fusion methods were compared:

- `rank_average`
- `z_normalized_logits`
- `temperature_softmax`

The offline comparison used support-rate and AUC criteria, not CHAIR tuning.

Best offline candidates:

- `late_27_31 + rank_average`
  - selection score `1.0180`
  - correct support `0.3430`
  - introduced support `0.0500`
- `late_27_31 + z_normalized_logits`
  - selection score `1.0140`
  - correct support `0.2890`
  - introduced support `0.0400`

Reference fixed anchor:

- `final + fixed_firstlogit`
  - selection score `0.9188`

So offline, late-layer ensemble anchors looked genuinely cleaner than the fixed final first-logit anchor on the chosen object-event support metrics.

## 5. Branch A Sanity

Two 10-image sanity runs were completed.

`late_27_31 + rank_average`:

- `CHAIRs = 0.2000`
- `CHAIRi = 0.0526`
- `Object Mentions = 38`
- `Hallucinated Object Count = 2`
- first word changed vs fixed `= 0`
- empty captions `= 0`

`late_27_31 + z_normalized_logits`:

- `CHAIRs = 0.3000`
- `CHAIRi = 0.0909`
- `Object Mentions = 44`
- `Hallucinated Object Count = 4`
- first word changed vs fixed `= 0`
- empty captions `= 0`

Both methods passed implementation sanity. But `z_normalized_logits` was already clearly worse than `rank_average` on the same 10 images.

## 6. Branch A 1000 Pilot

Only the stronger candidate advanced:

- `late_27_31 + rank_average`

1000-image pilot result:

- `CHAIRs = 0.1800`
- `CHAIRi = 0.0552`
- `Avg Caption Length = 50.2880`
- `Object Mentions = 4659`
- `Hallucinated Object Count = 257`
- `s/sample = 1.2946`

Compared with fixed `first_logit` 1000:

- fixed `CHAIRs = 0.1610`
- fixed `CHAIRi = 0.0509`
- fixed `Object Mentions = 4717`
- fixed `Hallucinated Object Count = 240`

Delta vs fixed `first_logit`:

- object mentions: `-58`
- correct object mentions: `-75`
- hallucinated objects: `+17`
- improved images: `67`
- worsened images: `85`
- stable images: `848`
- removed hallucinations: `100`
- introduced hallucinations: `117`
- first word changed vs fixed: `0`
- empty captions: `0`

Conclusion:

- offline support separation did not translate into better caption-time CHAIR behavior
- the best late-layer ensemble anchor still underperformed fixed `first_logit`
- the failure was not a catastrophic object-mention collapse
- but it was still a clear regression on the main hallucination metrics

Because the best offline candidate already failed 1000, and `z_normalized_logits` had weaker offline score plus worse 10-image sanity, the second 1000 pilot was not run.

## 7. Branch B Mismatch Feasibility

Middle-late mismatch stayed informative but not yet runtime-ready.

Best introduced-vs-correct signals:

- `middle_to_late_mass_change`
  - `abs(AUC-0.5)=0.2574`
- `middle_x_mass_change`
  - `0.2503`
- `attn_middle_all_5_26_image_mass_mean`
  - `0.2213`
- `obj_late_27_31_target_rank_mean`
  - `0.2020`
- `firstlogitgap_x_verification_masschange`
  - `0.1753`

Simple trigger behavior:

- `trigger_mass_middlelow_lategain`
  - introduced hit `0.2850`
  - correct false-hit `0.1040`
- `trigger_combined_rank_and_mass`
  - introduced hit `0.0150`
  - correct false-hit `0.0020`

Interpretation:

- the descriptive mismatch story is real
- but the straightforward trigger is still too weak or too sparse
- this does not justify a runtime mismatch-triggered method yet

## 8. Comparison With Fixed First-Logit

What improved relative to earlier negative guard families:

- this round finally produced a cleaner offline candidate-selection story
- it did not rely on object-vocab suppression
- it did not use token-level boost clipping

What still failed:

- always-on layer-anchor replacement did not beat fixed `first_logit`
- the best 1000 pilot regressed on `CHAIRs`, `CHAIRi`, and hallucinated-object count

So the decoding reference still remains fixed `first_logit / early-anchor`.

## 9. Whether Any Layer-Ensemble Anchor Beat Fixed First-Logit

Offline:

- yes, several `late_27_31` fusion variants beat fixed `first_logit` on the pre-registered support-separation score

Runtime 1000 pilot:

- no

This round therefore produced a useful negative result:

- better offline target-support separation is not sufficient, by itself, to beat the fixed final-layer first-logit anchor in actual decoding

## 10. Caveats

- the layer grouping is a working hypothesis, not a proven decoder-stage decomposition
- the offline selection score is still a support surrogate, not a direct caption metric
- only the top offline candidate reached the 1000 pilot
- the second candidate was stopped after worse sanity and weaker offline ranking, not after a full 1000 comparison

## 11. Current Recommendation

Current safest position:

- keep fixed `first_logit / early-anchor` as the decoding reference
- keep `late_27_31` as a meaningful signal-bearing group, not a replacement anchor source
- keep `middle_to_late_mass_change` and related interactions as informative descriptive signals
- do not promote middle-late mismatch to a runtime trigger yet
- do not continue broad always-on layer-anchor replacement without a stronger mechanism story

## 12. Next Step

The most reasonable next step is not another immediate pilot.

It is to consolidate the mechanism boundary from this round:

- late-layer anchor support can look cleaner offline than fixed first-logit
- but replacing the final-layer anchor trajectory still hurts caption-time CHAIR
- mismatch-style signals remain useful for analysis, but still do not supply a clean runtime action rule
