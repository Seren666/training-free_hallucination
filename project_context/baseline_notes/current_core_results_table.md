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

## 8. Current Main Conclusions

### 8.1 Benchmark split

- `COCO-CHAIR` is now the main positive benchmark for `first_logit / early-anchor`
- `POPE` is retained for one-forward signal audit, not for later-step first-logit intervention scoring
- `AMBER` remains deferred

### 8.2 Method status

- `first_logit / early-anchor` is a promising intervention candidate
- it is not yet the final paper method
- it should not yet be presented as a fully established final conclusion
- the current `object_safe_anchor` pilot does not yet improve on fixed `first_logit`

### 8.3 Why the current COCO-CHAIR result matters

- the effect remains positive from `100` to `500` to `1000` to `40504`
- `CHAIRs` and `CHAIRi` both improve
- captions do not get shorter on average
- object mentions do not go down on average
- first word remains unchanged
- `The effect` was not used
- near-official alignment preserves the same positive direction
- object-level local signals now provide mechanism evidence

### 8.4 What is no longer the main line

- do not continue old `VCD / RAD-VCD` as the main paper line
- do not keep tuning `POPE first_logit`
- do not use `The effect` as the main explanation path
- do not treat coarse image-level scalars as a viable selector
- do not expand the current flat `object_safe_anchor` rule to full scale

## 9. Current Recommended Next Step

1. use the negative `object_safe_anchor` pilot as evidence that flat object-token dampening is too coarse
2. keep mechanism design focused on object-local selectivity rather than global object suppression
3. only later consider a tighter object-local selective prototype
4. do not immediately start parameter sweep, new benchmark expansion, or classifier work
