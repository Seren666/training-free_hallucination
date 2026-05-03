# Current Core Results Table

> Date: 2026-05-03
> Scope: condensed view of the current benchmark conclusions after the completed POPE and COCO-CHAIR work.

## 1. POPE First-Logit

| Benchmark | Scope | Methods | Result | Current Conclusion | Current Role |
|---|---|---|---|---|---|
| POPE 9 splits | COCO / GQA / A-OKVQA x random / popular / adversarial | `regular`, faithful later-step `first_logit` adaptation | `delta = 0` on all `9/9` splits | POPE is not suitable for later-step `first_logit` intervention evaluation under one-word yes/no decoding | keep POPE as `answer-boundary` / `pre-answer` / false-positive signal-audit benchmark |

Key POPE takeaway:

- `first_logit` on POPE did not improve or worsen any split
- the likely reason is protocol-level:
  - the decisive answer is usually fixed at the first answer token
  - later-step boosting has no room to act
- so POPE should not be used as the main benchmark for later-step `first_logit`

## 2. COCO-CHAIR Regular Baseline

| Stage | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Object Count | Note |
|---|---:|---:|---:|---:|---:|---:|---|
| pilot | 100 | 0.2100 | 0.0533 | 49.9100 | 450 | 24 | first open-ended caption hallucination pilot |
| full | 40504 | 0.2037 | 0.0655 | 49.6823 | 181268 | 11875 | full regular caption baseline |

## 3. COCO-CHAIR First-Logit

| Stage | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Object Count | Delta vs regular |
|---|---:|---:|---:|---:|---:|---:|---|
| pilot | 100 | 0.1500 | 0.0465 | 51.3100 | 452 | 21 | positive signal |
| prefix | 500 | 0.1440 | 0.0429 | 51.0380 | 2356 | 101 | positive |
| prefix | 1000 | 0.1610 | 0.0509 | 50.9190 | 4717 | 240 | positive |
| full | 40504 | 0.1631 | 0.0513 | 50.9320 | 187440 | 9609 | stable positive full confirmation |

## 4. Near-Official Alignment

| Evaluator | Method | Images | CHAIRs | CHAIRi | Delta CHAIRs vs regular | Delta CHAIRi vs regular |
|---|---|---:|---:|---:|---:|---:|
| adapted | regular | 40504 | 0.2037 | 0.0655 | - | - |
| adapted | first_logit | 40504 | 0.1631 | 0.0513 | -0.0406 | -0.0142 |
| near-official | regular | 40504 | 0.1997 | 0.0669 | - | - |
| near-official | first_logit | 40504 | 0.1594 | 0.0524 | -0.0403 | -0.0145 |

Alignment takeaway:

- adapted and near-official evaluators agree on direction
- magnitudes are very close
- current positive result is not an adapted-evaluator illusion

## 5. Image-Level Audit

| Audit | Subset | Main Result | Current Conclusion |
|---|---|---|---|
| one-forward image-level scalar audit | 3000 stratified images | `improved vs worsened` separation is near-random; best absolute AUC shift is only about `0.0167` | coarse image-level selective early-anchor is not supported |

Image-level takeaway:

- coarse image-level scalars do not explain why some samples improve and others worsen
- they weakly hint at `changed` vs `stable`, but not `helpful` vs `harmful`

## 6. Object-Level Audit

| Item | Result |
|---|---|
| object-event table | built successfully on full paired captions |
| removed_hallucination | 6043 |
| introduced_hallucination | 3880 |
| persistent_hallucination | 3924 |
| correct_object_mention | 86458 |
| top removed objects | `person`, `dining table`, `chair`, `car`, `bowl` |
| top introduced objects | `dining table`, `chair`, `couch`, `sink`, `person`, `refrigerator` |
| removed vs introduced signals | `adjusted_target_rank_if_applied`, `anchor_target_token_rank` |
| hallucinated vs correct signals | `anchor_weight_at_object_step`, `mention_position_ratio`, `anchor_target_token_rank` |

Object-level takeaway:

- object-local signals are much more informative than coarse image-level scalars
- the mechanism story now looks object-token-level, not image-level

## 7. Object-Safe Anchor Pilot

| Stage | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Object Count | Current Status |
|---|---:|---:|---:|---:|---:|---:|---|
| 1000 pilot | 1000 | 0.1620 | 0.0530 | 51.3090 | 4228 | 224 | did not beat fixed `first_logit`; stopped before full |

Pilot takeaway:

- raw hallucinated object count improves slightly vs fixed `first_logit`
- but `CHAIRs` is slightly worse and `CHAIRi` is worse
- object mentions drop by `489`
- correct object mentions drop by `473`
- so the current flat object-token positive-boost scaling is too blunt

## 8. Attention-Gated Early Anchor Pilot

| Stage | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Object Count | Current Status |
|---|---:|---:|---:|---:|---:|---:|---|
| 10 sanity | 10 | 0.3000 | 0.0811 | 49.8000 | 37 | 3 | implementation/runtime sanity only; too small for method judgment |
| 1000 pilot | 1000 | 0.1680 | 0.0575 | 51.1140 | 4329 | 249 | did not beat fixed `first_logit`; stopped before full |

Pilot takeaway:

- the offline gate idea looked better than flat `Object-Safe`
- first word changed remains `0`
- empty captions remain `0`
- but the `1000` pilot still underperforms fixed `first_logit`
- `CHAIRs` and `CHAIRi` are both worse than fixed `first_logit`
- hallucinated object count is also worse than fixed `first_logit`
- object mentions drop by `388`
- correct object mentions drop by `397`
- removed hallucinations (`60`) do not outnumber introduced hallucinations (`69`)
- the gate is narrower than flat object suppression, but still too broad at runtime

## 9. Candidate and Attention-Shape Follow-Up

| Route | Stage | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Object Count | Current Status |
|---|---|---:|---:|---:|---:|---:|---:|---|
| attention-shape | offline feasibility | object-local subset | - | - | - | - | - | stopped before generation; diffuse signal too weak |
| candidate-local guard | 10 sanity | 10 | 0.3000 | 0.0909 | 49.5000 | 33 | 3 | implementation/runtime sanity only |
| candidate-local guard | 1000 pilot | 1000 | 0.1680 | 0.0555 | 51.0600 | 4431 | 246 | healthier than previous attention-gated, but still worse than fixed `first_logit` |

Follow-up takeaway:

- offline feasibility favored `candidate_local_guard` over `attention_shape_guard`
- `attention_shape_guard` was not run because:
  - diffuse attention is somewhat more common in introduced hallucinations
  - but separation from correct mentions is too weak for a direct pilot
  - extremely concentrated attention is actually more common in correct mentions
- `candidate_local_guard` was much narrower than previous attention-gated gating:
  - about `10.938` gate-trigger steps per image vs about `44.315`
- `candidate_local_guard` slightly improved over previous attention-gated:
  - same `CHAIRs`
  - better `CHAIRi`
  - better object mentions
  - fewer hallucinated objects
- but it still does not beat fixed `first_logit`
- and object mentions still drop by about `6.1%`, beyond the allowed health line

## 10. Current Main Conclusions

### 10.1 Benchmark split

- `COCO-CHAIR` is now the main positive benchmark for `first_logit / early-anchor`
- `POPE` is retained for one-forward signal audit, not for later-step first-logit intervention scoring
- `AMBER` remains deferred

### 10.2 Method status

- `first_logit / early-anchor` is a promising intervention candidate
- it is not yet the final paper method
- it should not yet be presented as a fully established final conclusion
- the current `object_safe_anchor` pilot does not improve on fixed `first_logit`
- the current `attention_gated_attnanchor` pilot also does not improve on fixed `first_logit`
- the current `candidate_local_guard` pilot is the narrowest and healthiest selective follow-up so far, but still does not improve on fixed `first_logit`
- the current `middle_verified` pilot is even narrower and preserves mentions better, but still does not improve on fixed `first_logit`
- the current `middle_refined` pilot is a different anchor-construction family, but it also does not improve on fixed `first_logit`
- the current `attention_shape_guard` route does not justify runtime generation yet
- fixed `first_logit` remains the strongest decoding result so far

### 10.3 Why the current COCO-CHAIR result matters

- the effect remains positive from `100` to `500` to `1000` to `40504`
- `CHAIRs` and `CHAIRi` both improve
- captions do not get shorter on average
- object mentions do not go down on average
- first word remains unchanged
- `The effect` was not used
- near-official alignment preserves the same positive direction
- object-level local signals now provide mechanism evidence

### 10.4 What the failed follow-up pilots now imply

- flat object-vocab positive-boost suppression is too coarse
- step-level low-attention object-token gating is still too coarse in its current form
- current top-k candidate-local gating is better, but still not local enough
- middle-layer verification makes the gate narrower, but token-level boost clipping still does not beat the fixed trajectory
- anchor construction is a more meaningful new family than token-level clipping, but the current step0 low-attention `middle_refined` rule still broadens into source-level object suppression
- diffuse attention-shape alone is not strong enough to justify a runtime guard
- future selectivity has to move closer to the actual candidate object token or mention-local decision
- a method can be more selective than `Object-Safe` and still fail if it suppresses too many valid object mentions

### 10.5 What is no longer the main line

- do not continue old `VCD / RAD-VCD` as the main paper line
- do not keep tuning `POPE first_logit`
- do not use `The effect` as the main explanation path
- do not treat coarse image-level scalars as a viable selector
- do not expand the current flat `object_safe_anchor` rule to full scale
- do not expand the current `attention_gated_attnanchor` rule to full scale
- do not expand the current `candidate_local_guard` rule to full scale
- do not expand the current `middle_verified` rule to full scale
- do not expand the current `middle_refined` rule to full scale
- do not start `attention_shape_guard` generation from the current offline signal alone

## 11. Current Recommended Next Step

1. keep fixed `first_logit / early-anchor` as the best current decoding baseline
2. treat `object_safe_anchor`, `attention_gated_attnanchor`, `candidate_local_guard`, and `middle_verified` as increasingly narrow but still negative clipping pilots
3. treat `middle_refined` as a negative anchor-construction pilot: more meaningful than clipping, but still broad in its current form
4. keep the middle-layer audit as mechanism evidence, but do not assume it already gives a working runtime or anchor-construction rule
5. do not start full COCO-CHAIR for a new variant unless it beats fixed `first_logit` on a `1000` pilot without object-mention collapse
6. do not immediately start parameter sweep or new benchmark expansion; any classifier branch should remain upper-bound diagnostic only

## 12. Dual-Trajectory Mention Selection Feasibility

| Item | Result |
|---|---|
| route | caption-level selection between existing `regular` and fixed `first_logit` captions |
| feasibility status | completed |
| selected captions built | no |
| stop point | stopped before full selection simulation |
| why stopped | the critical `first_only hallucinated` vs `first_only correct` split shows only weak separation under the simple visual-support signals needed for rollback |
| first-only probe subset counts | `first_only_hallucinated=1000`, `first_only_correct=63` |
| first-only separation | `middle_image_attention_mean abs(AUC-0.5)=0.0465`, `hidden_image_cosine_middle_mean=0.0313`, `mention_position_ratio=0.0675`, `anchor_target_token_rank=0.1323` |
| threshold source | unsupervised from existing 4000-event object-local probe |
| runtime check | `20`-mention sanity probe succeeded; estimated full first-only probe cost was about `6` hours for `9378` mentions |

Dual-trajectory takeaway:

- caption-level rollback is cleaner than token-level suppression conceptually
- but the actual rollback boundary, `first_logit-only hallucinated` vs `first_logit-only correct`, is too noisy under the current simple support signals
- so this route currently stops at feasibility and does not replace fixed `first_logit`

## 13. Middle-Layer Object-Token Audit

| Item | Result |
|---|---|
| scope | existing 4000-event object-local subset plus new middle/late rank-lens supplement |
| generation rerun | no |
| main positive finding | correct mentions are already stronger in middle-layer target rank and middle-layer visual attention |
| introduced vs correct | `middle_target_rank_mean: 6098.926 vs 3533.189`, `image_attention_middle_mean: 0.145080 vs 0.183550` |
| removed vs correct | `middle_target_rank_mean: 4422.097 vs 3533.189`, `middle_to_late_rank_improvement: 4251.176 vs 3485.976` |
| introduced vs removed | introduced still has stronger anchor-side push: `anchor_adjustment_delta 1.151627 vs 0.978613`, `adjusted_target_rank_if_applied 1.021 vs 1.467` |
| attention shape | stronger than raw mass alone; best current shape signal is `mass_change_late_minus_mid` with `abs(AUC-0.5)=0.3113` for `introduced vs correct` |
| hidden-image cosine | weaker than middle-layer rank and attention signals as a standalone separator |
| current conclusion | middle layers look like a promising verification surface for a constrained next pilot |

Middle-layer takeaway:

- correct mentions are not only better at the final step; they already look better in the middle stage
- introduced hallucinations appear more like anchor-pushed mentions without matching middle-layer verification
- removed hallucinations are consistent with late-stage over-mention that fixed `first_logit` can correct
- the audit justified a `Middle-Verified Early Anchor` pilot, but the pilot still did not beat fixed `first_logit`

## 14. Middle-Verified Early Anchor Pilot

| Stage | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Object Count | Current Status |
|---|---:|---:|---:|---:|---:|---:|---|
| 10 sanity | 10 | 0.5000 | 0.1136 | 49.4000 | 44 | 5 | implementation/runtime sanity only |
| 1000 pilot | 1000 | 0.1770 | 0.0555 | 51.0110 | 4645 | 258 | narrower and healthier than prior guards, but still worse than fixed `first_logit`; stopped before full |

Pilot takeaway:

- the gate is much narrower than previous broad attention gating:
  - about `3.932` gate-trigger steps per image
  - about `3.962` gated candidates per image
  - gated candidate ratio about `0.1196`
- it avoids the earlier object-mention collapse much better:
  - object mentions delta vs fixed `first_logit`: `-72`
  - correct object mentions delta vs fixed `first_logit`: `-90`
- but it still does not beat fixed `first_logit`
- `CHAIRs` regresses from `0.1610` to `0.1770`
- `CHAIRi` regresses from `0.0509` to `0.0555`
- hallucinated object count increases from `240` to `258`
- removed hallucinations (`18`) are outnumbered by introduced hallucinations (`36`)

## 15. Middle-Refined Early Anchor Pilot

| Stage | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Object Count | Current Status |
|---|---:|---:|---:|---:|---:|---:|---|
| feasibility | 4000 event subset | - | - | - | - | - | supportive offline signal; `introduced flag rate 0.254` vs `correct 0.102` |
| 10 sanity | 10 | 0.2000 | 0.0625 | 49.9000 | 32 | 2 | implementation/runtime sanity only; broad source refinement already visible |
| 1000 pilot | 1000 | 0.1640 | 0.0541 | 51.2880 | 4267 | 231 | more meaningful than clipping family, but still worse than fixed `first_logit`; stopped before full |

Pilot takeaway:

- offline feasibility was genuinely cleaner than flat `Object-Safe`
- but the runtime anchor rule broadened heavily:
  - avg refined object tokens per image: `141.93`
  - avg step0 low-attention trigger rate: `0.978`
- raw hallucinated object count improved slightly vs fixed `first_logit`:
  - `231` vs `240`
- but object mentions and correct mentions collapsed too much:
  - object mentions delta vs fixed: `-450`
  - correct object mentions delta vs fixed: `-441`
- `CHAIRs` and `CHAIRi` still regress vs fixed `first_logit`
- so current `middle_refined` is best viewed as a negative anchor-construction pilot, not a new best method

## 16. Current 1000-Image Method Comparison

| Method | Family | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Object Count | Status |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `regular` | baseline | 1000 | 0.2090 | 0.0657 | 49.6580 | 4522 | 297 | reference baseline |
| `fixed first_logit` | early-anchor main line | 1000 | 0.1610 | 0.0509 | 50.9190 | 4717 | 240 | strongest current method candidate |
| `object_safe_anchor` | flat object suppression | 1000 | 0.1620 | 0.0530 | 51.3090 | 4228 | 224 | lower raw hallucination count, but worse than fixed |
| `previous_attention_gated` | step-level attention gate | 1000 | 0.1680 | 0.0575 | 51.1140 | 4329 | 249 | too broad; worse than fixed |
| `candidate_local_guard` | top-k candidate clipping | 1000 | 0.1680 | 0.0555 | 51.0600 | 4431 | 246 | narrower, but still worse than fixed |
| `middle_verified` | middle-layer token clipping | 1000 | 0.1770 | 0.0555 | 51.0110 | 4645 | 258 | best mention preservation among clipping pilots, but still worse than fixed |
| `middle_refined` | anchor-construction refinement | 1000 | 0.1640 | 0.0541 | 51.2880 | 4267 | 231 | different family, but still worse than fixed |
| `layer_anchor_late_27_31_rank_average` | always-on layer-anchor replacement | 1000 | 0.1800 | 0.0552 | 50.2880 | 4659 | 257 | best offline layer-anchor candidate, but still worse than fixed |

Comparison takeaway:

- fixed `first_logit / early-anchor` remains the strongest current decoding result
- some guards reduce raw hallucinated-object count slightly, but none improve the main CHAIR metrics over fixed `first_logit`
- the recurring cost is object-mention and correct-object collapse
- current token-level suppression and broad anchor-cleaning guard variants should stop here

## 17. Current Position

- treat fixed `first_logit / early-anchor` as the current main method candidate
- treat `object_safe_anchor`, `attention_gated_attnanchor`, `candidate_local_guard`, `middle_verified`, and `middle_refined` as informative negative follow-ups
- do not continue token-level boost clipping, broad object suppression, or broad anchor-cleaning guard expansion
- next work should focus on validating the main early-anchor result and discovering stronger internal hallucination signals rather than searching for another guard variant in the same family

## 18. Attention Distribution Hallucination Audit

| Audit | Scope | Main Result | Current Conclusion |
|---|---|---|---|
| attention-shape probe | frozen balanced subset, `1982` events total: `correct=496`, `introduced=496`, `removed=495`, `persistent=495` | strongest `introduced vs correct` separator is `mass_change_late_minus_mid` with `abs(AUC-0.5)=0.3223`; next is `middle_image_attention_mean` with `0.2761`; diffuse entropy alone is weak at `0.0795` | middle-to-late attention evolution is more informative than simple diffuse-attention heuristics |
| visual sensitivity probe | balanced subset, `800` events total: `200` per event type | correct mentions are more sensitive to top-attention patch masking than introduced hallucinations, but best sensitivity signal (`sensitivity_ratio_prob`, `0.1110`) is still weaker than the best shape / mass signals | attention-guided masking is useful supporting evidence, but not yet the dominant separator |

Attention-distribution takeaway:

- hallucinated mentions do tend to have weaker middle visual support
- they are also somewhat more diffuse, but diffuse entropy is not the main story
- extreme concentration is not automatically a "correct grounding" signal; in this audit it leans more hallucination-like
- head consistency helps somewhat, but middle-to-late mass change is stronger than pure head-overlap heuristics
- current best signal family is:
  - middle image attention mass
  - middle-to-late mass evolution
  - anchor-plus-verification interaction

## 19. Current Research Shift

- fixed `first_logit / early-anchor` remains the decoding reference and main method candidate
- the active exploration line has now shifted away from new clipping / suppression variants
- the current question is no longer "what guard should be added"
- the current question is "what internal signal actually tracks hallucination reliably"
- present evidence says:
  - middle-layer verification matters
  - layer-evolution signals matter more than diffuse entropy alone
  - attention-guided visual sensitivity is informative, but not yet stronger than the best attention mass / evolution signals

## 20. Early-Anchor Internal Signal Audit

| Audit | Scope | Main Result | Current Conclusion |
|---|---|---|---|
| paired regular-vs-early-anchor internal audit | current frozen shape subset (`1982`) plus alternate shared-trajectory shape subset (`905`); current sensitivity subset (`800`) plus alternate shared-trajectory sensitivity subset (`372`) | the strongest `introduced_first_logit_only vs correct_first_logit` signals are still middle-to-late verification-evolution terms, not shared-event trajectory deltas | within-trajectory verification quality is informative; shared-event `regular -> first_logit` internal shifts are small, so no runtime correction rule is justified yet |

Internal-audit takeaway:

- strongest `introduced_first_logit_only vs correct_first_logit` separators:
  - `middle_x_mass_change`: `abs(AUC-0.5)=0.3612`
  - `mass_change_late_minus_mid`: `0.3541`
  - `middle_to_late_image_attention_delta`: `0.3541`
  - `firstlogitgap_x_verification_masschange`: `0.3319`
  - `anchor_masschange_x_late_mass`: `0.3123`
  - `late_image_attention_recovery_ratio`: `0.2996`
  - `middle_image_attention_mean`: `0.2858`
- those signals beat pure sensitivity and clearly beat pure entropy-style heuristics
- but true shared-event paired deltas are weak:
  - best `persistent vs correct` paired delta from the shape side is only `anchor_masschange_x_late_mass` at `0.0461`
  - best paired sensitivity delta is `sensitivity_ratio_prob` at `0.0502`
- paired group means show that early-anchor changes shared-event middle attention and mass evolution only slightly:
  - correct middle attention mean: `0.1899 -> 0.1878`
  - persistent middle attention mean: `0.1634 -> 0.1606`
  - correct mass change: `-0.0620 -> -0.0616`
  - persistent mass change: `-0.0372 -> -0.0357`
- control-aware sensitivity keeps the right direction, but remains secondary:
  - `top_minus_random_logit_drop`: introduced `0.2458` vs correct `1.0550`
  - within every middle-attention-mass bin, correct still exceeds introduced, but with small `abs(AUC-0.5)` values
  - within every mention-length group, correct still exceeds introduced, but again weakly

Current implication:

- the best current signal family is still:
  - middle verification mass
  - middle-to-late verification evolution
  - anchor-plus-verification interaction
- these are now better supported as correction-facing signal candidates than pure entropy, concentration, or raw sensitivity
- but they are not yet strong as direct shared-event trajectory-delta controls
- the safe next move is still more signal consolidation, not a new decoding intervention

Current correction-facing candidates:

- `mass_change_late_minus_mid`
- `middle_to_late_image_attention_delta`
- `middle_x_mass_change`
- `firstlogitgap_x_verification_masschange`
- `anchor_masschange_x_late_mass`
- `late_image_attention_recovery_ratio`
- `middle_image_attention_mean`

## 21. Layer-Wise Anchor Audit

| Audit | Scope | Main Result | Current Conclusion |
|---|---|---|---|
| layer-group object-step audit | balanced `4000`-event subset; groups `shallow_0_4`, `visual_enrichment_5_18`, `semantic_refinement_19_26`, `middle_all_5_26`, `late_27_31` | strongest introduced-vs-correct object-step logit-lens signal is `obj_late_27_31_target_logit_mean` with `abs(AUC-0.5)=0.2523`; strongest attention signal is `attn_shallow_0_4_image_mass_mean` with `0.3250`; strongest middle-late transition signal is `middle_to_late_mass_change` with `0.2574` | layer-wise evidence is informative, but it does not yet identify a replacement decoding anchor by itself |
| layer-ensemble anchor offline comparison | full layer-anchor support comparison over the same `4000`-event audit | best offline candidates are `late_27_31 + rank_average` with selection score `1.0180` and `late_27_31 + z_normalized_logits` with `1.0140`, both above fixed `firstlogit` at `0.9188` | late-layer ensemble anchors can look cleaner offline than fixed first-logit on support separation |
| Branch A runtime pilot | 10-image sanity for two candidates, then 1000 pilot for the stronger candidate | `late_27_31 + rank_average` 1000 pilot reaches `CHAIRs=0.1800`, `CHAIRi=0.0552`, `Object Mentions=4659`, `Hallucinated Object Count=257` | the best offline candidate still fails to beat fixed `first_logit` (`0.1610 / 0.0509 / 4717 / 240`), so no full run |
| Branch B mismatch feasibility | offline-only trigger analysis from the cleaned layer-group audit | strongest descriptive mismatch signals are `middle_to_late_mass_change=0.2574`, `middle_x_mass_change=0.2503`, `attn_middle_all_5_26_image_mass_mean=0.2213`; simple combined trigger hit is only `0.015` on introduced vs `0.002` false-hit on correct | mismatch is informative but not yet strong enough to justify a runtime trigger |

Layer-wise takeaway:

- `late_27_31` is the most informative current logit-lens anchor group
- `shallow_0_4` and `visual_enrichment_5_18` are stronger from the attention-mass side than from direct anchor support
- offline support separation can improve while caption-time CHAIR still gets worse
- always-on layer-anchor replacement therefore does not currently beat fixed `first_logit`
- middle-late mismatch should remain an analysis signal, not a runtime method in the current state

## 22. Hallucination Evidence Hypothesis Audit

| Hypothesis | Status | Strongest Current Signal | Main Result | Current Interpretation |
|---|---|---|---|---|
| `H1` Middle Verification Deficit | supported | `image_attention_middle_mean` | introduced vs correct: `0.1451` vs `0.1835`, `abs(AUC-0.5)=0.2616` | hallucinated mentions are already weaker in middle visual verification |
| `H2` Late Readiness Surge | weak | `middle_to_late_rank_improvement` | introduced vs correct: `5584.0` vs `3486.0`, `0.1158` | only relative rank-jump support remains; absolute late confidence does not support the claim |
| `H3` Middle-to-Late Attention Evolution | supported | `middle_x_mass_change` | introduced vs correct: `-0.0028` vs `-0.0108`, `0.3333` | strongest overall signal family |
| `H4` Attention Diffusion | weak | `middle_effective_attended_count_mean` | introduced vs correct: `162.0` vs `149.9`, `0.0833` | diffuse attention is real but too weak as a main rule |
| `H5` Extreme Concentration / Spurious Fixation | weak | `middle_top1_mass_mean` | hallucinated vs correct: `0.0725` vs `0.0694`, `0.0749` | concentration alone is not grounding and not a stable hallucination flag |
| `H6` Head Agreement | weak | `middle_head_mass_cv_mean` | introduced vs correct: `1.1869` vs `1.1397`, `0.1469` | useful supporting evidence, weaker than verification-evolution signals |
| `H7` Layer Consistency | weak | `late_shape_layer_cosine_mean` | introduced vs correct: `0.6713` vs `0.6900`, `0.1214` | cross-layer mismatch exists, but not strongly enough alone |
| `H8` Anchor-Middle Mismatch | supported | `anchor_masschange_x_late_mass` | introduced vs correct: `-0.0021` vs `-0.0053`, `0.2749` | strong first-logit-side mismatch story |
| `H9` Visual Sensitivity Validation | weak | `sensitivity_ratio_prob` | introduced vs correct: `-0.3293` vs `28.3352`, `0.1110` | supporting validation signal, not the main separator |
| `H10` Removed vs Introduced Difference | supported | `mass_change_late_minus_mid` | removed vs persistent: `-0.0175` vs `-0.0372`, `0.2159` | removed / persistent / introduced are not identical trajectories |

Evidence-discovery takeaway:

- strongest supported families:
  - middle verification
  - middle-to-late attention evolution
  - anchor-middle mismatch interaction
- weak but useful supporting families:
  - head agreement
  - layer consistency
  - attention-guided visual sensitivity
- weak standalone families:
  - diffuse entropy alone
  - pure concentration alone

Current best correction-facing evidence candidates:

- `middle_x_mass_change`
- `mass_change_late_minus_mid`
- `middle_to_late_image_attention_delta`
- `anchor_masschange_x_late_mass`
- `image_attention_middle_mean`
- `firstlogitgap_x_verification_masschange`
- `middle_target_probability_mean`
- `obj_semantic_refinement_19_26_target_rank_mean`

Current boundary:

- the audit supports stronger mechanism claims
- it does **not** yet support a runtime rule, selector, or new decoding intervention
- method design should stay paused until the user explicitly approves a new correction-design round

## 23. Current Research Posture

- fixed `first_logit / early-anchor` remains the strongest decoding reference and main method candidate
- the active branch is now hallucination evidence discovery, not local first-logit optimization
- do not continue:
  - token-level clipping
  - object suppression
  - anchor cleaning
  - layer-anchor replacement
  - runtime mismatch triggering
- only discuss correction again if the evidence story becomes stable enough and the user explicitly wants to turn it into a method

## 24. Mention-Level Verification Audit

| Item | Result |
|---|---|
| dataset | reused existing balanced `4000`-event object-local audit subset |
| classes | `1000` each for `correct`, `introduced`, `removed`, `persistent` |
| caption source | `regular=2937`, `first_logit=1063` |
| sensitivity coverage | only the existing `800`-event sensitivity subset, so sensitivity-family missing rate remains high |
| primary task | `hallucinated object mention` vs `correct object mention` |
| strongest single signal | `middle_x_mass_change`, `abs(AUC-0.5)=0.2745` on `hallucinated_vs_correct` |
| next strongest single signals | `mass_change_late_minus_mid=0.2701`, `middle_to_late_image_attention_delta=0.2701`, `anchor_masschange_x_late_mass=0.2514`, `image_attention_middle_mean=0.2155` |
| best composite on primary task | `composite_middle_to_late_abnormal_evolution=0.2684` |
| composite vs best single | composite helps summarize evidence, but does **not** beat the best single signal |
| introduced vs correct | best single `middle_x_mass_change=0.3198`; best composite `middle_to_late_abnormal_evolution=0.3091` |
| removed vs correct | strongest current slice: `middle_x_mass_change=0.3252`, `mass_change_late_minus_mid=0.3233` |
| persistent vs correct | weaker and harder: best direction-consistent signals around `0.175` to `0.179` |
| control robustness | top evolution / mismatch / middle-verification signals stay strong across category, position, mention-length, and frequency controls |
| first-logit-side caption-source control | weaker because only `63` first-logit-side correct events are available, but direction mostly survives |

Mention-level verification takeaway:

- mention-level verification is now supported at a diagnostic level
- the strongest current families are:
  - middle-to-late evolution
  - anchor-middle mismatch
  - middle visual verification
- attention shape / head agreement and visual sensitivity remain supporting validation, not the main verification core
- diffuse attention, pure concentration, and raw late confidence are still too weak or too unstable as standalone mention-level rules

Current best mention-level verification candidates:

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

Current boundary:

- this is enough to support a future second-pass correction **discussion**
- it is **not** enough to justify implementing a correction method yet
- Codex should not jump from this audit directly into second-pass correction without user approval

## 25. Multidimensional Evidence Verification

| Item | Result |
|---|---|
| scope | training-free multi-dimensional mention-level verification plus optional lightweight classifier upper bound |
| dataset | reused the existing balanced `4000`-event mention-level table |
| new probe | none |
| training-free composite rule | equal-weight direction-aligned z-score average; no learned weights and no threshold tuning |
| best composite on `hallucinated_vs_correct` | `middle_to_late_abnormal_evolution_score`, `abs(AUC-0.5)=0.2684` |
| best single vs best composite | best single stays `middle_x_mass_change=0.2745`, so composite does **not** beat the best single |
| introduced vs correct | best composite `middle_to_late_abnormal_evolution_score=0.3091`; best single remains `middle_x_mass_change=0.3198` |
| removed vs correct | best composite `middle_to_late_abnormal_evolution_score=0.3227`; best single remains `middle_x_mass_change=0.3252` |
| persistent vs correct | still hardest slice; best composite only `0.1735` |
| best composite robustness | `middle_to_late_abnormal_evolution_score`: category `moderate`, position `high`, source `high` |
| attention-shape composite | weak: `0.0295` with `50.45%` missing rate |
| classifier split | by `image_id`, `60 / 20 / 20`, seed `55` |
| control definition for classifier | `object_category + mention_position_ratio` only |
| best val-selected classifier | all four tasks select `E_all_internal_plus_controls`; test ROC-AUCs: `0.8792`, `0.9211`, `0.8271`, `0.9175` |
| internal-only vs control-only | `F_all_internal_minus_controls` beats `G_category_position_control` on all four tasks |
| best standalone learned family | `C_anchor_middle_mismatch_only`: `0.8414`, `0.8844`, `0.7841`, `0.8762` across the four main tasks |
| attention-shape-only classifier family | still weakest: `0.6470`, `0.6891`, `0.5888`, `0.6690` |

Multidimensional-verification takeaway:

- multi-dimensional evidence clearly helps mention-level verification
- the training-free route is still plausible, but the current equal-weight composite does not beat the best single evolution signal
- the lightweight classifier substantially beats the training-free composite, so the internal signals contain real learnable hallucination information
- the most important families remain:
  - middle visual verification
  - middle-to-late evolution
  - anchor-middle mismatch
- attention shape remains supporting evidence, not the main verification core
- this is enough to support a future correction **discussion**
- it is still not enough to justify automatic correction implementation or a classifier-first method pivot

## 26. Classifier Diagnostic And Distillation

| Item | Result |
|---|---|
| scope | multi-seed lightweight classifier diagnostic plus training-free score distillation |
| seeds | `55, 56, 57, 58, 59` |
| split | `image_id` only, `60 / 20 / 20` |
| best upper-bound setting | `C_internal_plus_category_position` on all four main tasks |
| upper-bound mean ROC-AUC | `0.8712` hallucinated, `0.9166` introduced, `0.8062` persistent, `0.9105` removed |
| stability | all four upper-bound tasks show low std, about `0.0116` to `0.0257` |
| internal-only mean ROC-AUC | `0.8540`, `0.9016`, `0.7945`, `0.8991` on the same four tasks |
| internal-only vs control-only | `A_internal_features_only` beats `B_category_position_control` on all `5/5` seeds for all four tasks |
| best family-only setting | `E_anchor_middle_mismatch_only` on all four tasks |
| weakest family-only setting | `E_attention_shape_only` on all four tasks |
| coefficient caveat | with controls enabled, category one-hot features dominate raw linear coefficient mass |
| internal-only family picture | still aligns with mechanism: middle verification, anchor mismatch, and evolution remain the core families |
| best distilled global score | `distilled_middle_to_late_dominant_score = 0.2684` on `hallucinated_vs_correct`, exactly matching the old best evolution composite |
| best distilled improvement | `distilled_anchor_middle_mismatch_score = 0.3213` on `introduced_vs_correct`, slightly above best single `0.3198` and above old composite `0.3091` |
| global distilled verdict | no distilled score clearly beats the best single signal overall |
| gap to upper-bound | still about `0.103`, `0.095`, `0.133`, `0.088` on hallucinated / introduced / persistent / removed |

Classifier-distillation takeaway:

- classifier backup is stable and worth preserving
- internal features genuinely carry verification signal beyond category and position controls
- distilled training-free scores improve the mechanism story and help the introduced slice
- but the training-free route still does not close the gap to the learned upper-bound
- training-free should remain the preferred route, with classifier kept as backup / diagnostic only

## 27. Weighted Evidence Consistency Audit

| Item | Result |
|---|---|
| scope | preregistered training-free weighted mention-level verification over the existing balanced `4000`-event table |
| new probe | none |
| weighting rule | manual signal-strength-aware / failure-mode-aware weights; no learned weights and no threshold tuning |
| weighted score families | `global`, `introduced_focused`, `persistent_focused`, `removed_focused`, `risk_minus_rescue` |
| global weighted on `hallucinated_vs_correct` | `global_weighted_evidence_score = 0.2922`, above best single `0.2745` and old equal-weight composite `0.2684` |
| introduced-focused on `introduced_vs_correct` | `introduced_focused_weighted_score = 0.3309`, above best single `0.3198` and old composite `0.3091` |
| persistent-focused on `persistent_vs_correct` | `persistent_focused_weighted_score = 0.2337`, above best single `0.2173` and well above old composite `0.1735` |
| removed-focused on `removed_vs_correct` | `removed_focused_weighted_score = 0.3431`, above best single `0.3252` and old composite `0.3227` |
| risk-minus-rescue on `hallucinated_vs_correct` | `risk_minus_rescue_weighted_score = 0.2965`, strongest current global-style weighted score |
| control robustness | all five weighted scores are `high` on category / position / source under the standard control summary |
| score-level missing rate | `0.0000` after available-evidence renormalization; shape and sensitivity still keep only small weights |
| multi-seed stability | task-matched weighted scores show low std on test splits, about `0.0088` to `0.0213` |
| task-matched test ROC-AUC | `0.8069`, `0.8503`, `0.7460`, `0.8556` on hallucinated / introduced / persistent / removed |
| classifier upper-bound mean ROC-AUC | still higher at `0.8712`, `0.9166`, `0.8062`, `0.9105` |
| classifier control-only mean ROC-AUC | `0.8099`, `0.8588`, `0.7639`, `0.8600`; weighted training-free narrows the gap but does not consistently beat the control-only classifier on split-based evaluation |

Weighted-audit takeaway:

- weighted training-free verification is now stronger than both:
  - the best single signal
  - the old equal-weight composite
- the biggest training-free gain is no longer only the introduced slice
- persistent improves materially:
  - from `0.1735` under the old equal-weight composite
  - to `0.2337` under `persistent_focused_weighted_score`
- removed is the cleanest target-task success case:
  - `removed_focused_weighted_score = 0.3431`
- the strongest current training-free verifier is now a weighted evidence score family, not a single signal
- classifier backup is still worth preserving because the weighted route remains about `0.055` to `0.066` mean ROC-AUC below the upper-bound diagnostic on split-based tests

Current best training-free mention-level verification candidates:

- `risk_minus_rescue_weighted_score`
- `global_weighted_evidence_score`
- `introduced_focused_weighted_score`
- `persistent_focused_weighted_score`
- `removed_focused_weighted_score`
- `middle_x_mass_change`
- `mass_change_late_minus_mid`
- `anchor_masschange_x_late_mass`
- `image_attention_middle_mean`

Current boundary update:

- weighted training-free verification is now strong enough to support a bounded second-pass correction **design discussion**
- it is still **not** enough to justify correction implementation without an explicit user-approved design round
- classifier remains:
  - upper-bound diagnostic
  - backup verifier
  - not the main method
