# Current Core Results Table

> Date: 2026-05-02
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
- do not start `attention_shape_guard` generation from the current offline signal alone

## 11. Current Recommended Next Step

1. keep fixed `first_logit / early-anchor` as the best current decoding baseline
2. treat `object_safe_anchor`, `attention_gated_attnanchor`, `candidate_local_guard`, and `middle_verified` as increasingly narrow but still negative selective pilots
3. keep the middle-layer audit as mechanism evidence, but do not assume it already gives a working runtime clipping rule
4. if method work continues, it needs a materially different family than token-level boost clipping
5. do not start full COCO-CHAIR for a new variant unless it beats fixed `first_logit` on a `1000` pilot
6. do not immediately start parameter sweep, new benchmark expansion, or classifier work

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
