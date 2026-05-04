# Correction Full Confirmation Readiness

> Date: 2026-05-03
> Updated: 2026-05-04
> Scope: expanded-confirmation follow-up for weighted-verifier-driven correction on existing COCO-CHAIR captions. This round did not rerun `regular` or fixed `first_logit` generation, did not change the verifier rule, and did not introduce any new correction family.

## 1. Motivation

The strict `1000`-image action matrix already established two viable branches on top of fixed `first_logit`:

- `firstlogit_removal_top10`
  - strongest raw CHAIR improvement
  - but clearly more aggressive and more exposed to correct-object loss and phrase damage
- `dual_phrase_replace_v1`
  - smaller raw gain
  - but healthier object preservation and a cleaner paper story

The open question was therefore no longer whether mention-level risk is useful, but whether these two branches remain credible beyond the `1000`-image pilot.

## 2. Why Two Branches Are Retained

The current evidence still supports keeping both routes alive.

- `firstlogit_removal_top10` is the metric-strong aggressive branch
- `dual_phrase_replace_v1` is the quality-preserving phrase-level branch

They optimize different tradeoffs, so this round did not auto-collapse them into a single winner.

## 3. Full Readiness Check

The first task was to check whether direct full correction on all `40504` captions was already possible without another large probe.

Readiness result:

- full caption files exist for both `regular` and fixed `first_logit`
- full fixed-caption mention extraction already exists in `object_event_table.csv`
- full weighted mention-risk outputs do **not** already exist

Coverage status:

- full fixed-caption mention pool:
  - `84619` mention rows across `39705` images
- existing scored runtime-style pools before this round:
  - only the `1000`-image pilot-scale fixed-source tables
- direct full-score coverage before expansion:
  - only about `2.5%` of full fixed mention rows at the unique-mention level

Missing fields for most full fixed-caption mentions:

- `primary_risk_score`
- weighted family scores
- `top5 / top10 / top20` risk flags
- `risk_group`

## 4. Full Or Expanded Confirmation Setup

Because the full weighted risk table was missing, I measured remote probe cost before choosing scale.

Measured remote benchmark:

- `20` fixed-first-logit images
- `50` mention rows
- model load: `16.9 s`
- probe time: `46.7 s`
- about `2.335 s / image`
- peak CUDA memory: `14.4 GB`

Projected probe-only time:

- `5000` images: about `3.24 h`
- `10000` images: about `6.49 h`
- full `39705` mentionable fixed images: about `25.73 h`

Decision:

- full confirmation was **not** launched
- expanded confirmation on `5000` images was completed instead
- this followed the preregistered rule to avoid starting a new `>8 h` extraction task blindly

Historical note:

- this was the original readiness-stage decision on `2026-05-03`
- a later resumable full run was approved and did complete, and the final full results are recorded in Sections `12-20`

## 5. Weighted Verifier On The Expanded Pool

Expanded fixed-source risk pool:

- mention rows: `10446`
- images with mentions: `4901`
- hallucinated mentions: `987`
- base hallucinated rate: `0.0945`

Top-slice ranking:

- top `5%` threshold: `0.943850`
- top `10%` threshold: `0.670282`
- top `20%` threshold: `0.197901`
- top `10%` precision / recall: `0.3206 / 0.3394`
- top `20%` precision / recall: `0.2713 / 0.5745`

Source-local reading:

- `first_logit_only` top-`10%` precision: `0.4565`
- `common` top-`10%` precision: `0.2091`

Interpretation:

- the weighted verifier remains useful on the expanded pool
- it is still much sharper on source-exclusive risky mentions than on common mentions
- the dominant risk family in top `10%` remains `introduced_focused_weighted_score`

## 6. Main Expanded Metrics

Primary expanded comparison (`5000` images):

| Method | CHAIRs | CHAIRi | Object Mentions | Correct Object Count | Hallucinated Object Count | Edited Images | Edited Mentions | Correct Delta vs fixed | Hallucinated Delta vs fixed |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `regular` | `0.2050` | `0.0662` | `22502` | `21013` | `1489` | `0` | `0` | `-1137` | `+251` |
| fixed `first_logit` | `0.1648` | `0.0529` | `23388` | `22150` | `1238` | `0` | `0` | `0` | `0` |
| `firstlogit_removal_top10` | `0.1344` | `0.0435` | `22715` | `21726` | `989` | `535` | `665` | `-424` | `-249` |
| `dual_phrase_replace_v1` | `0.1456` | `0.0468` | `23016` | `21939` | `1077` | `370` | `370` | `-211` | `-161` |

Immediate reading:

- both correction branches still beat fixed `first_logit`
- `firstlogit_removal_top10` remains the best raw-score branch
- `dual_phrase_replace_v1` remains the healthier preservation branch

## 7. Comparison With `regular` And Fixed `first_logit`

Relative to `regular`:

- fixed `first_logit` remains the strongest base caption source
- both correction branches stay well below `regular` on `CHAIRs` and `CHAIRi`

Relative to fixed `first_logit`:

- `firstlogit_removal_top10`
  - `CHAIRs: 0.1648 -> 0.1344`
  - `CHAIRi: 0.0529 -> 0.0435`
  - hallucinated objects: `1238 -> 989`
- `dual_phrase_replace_v1`
  - `CHAIRs: 0.1648 -> 0.1456`
  - `CHAIRi: 0.0529 -> 0.0468`
  - hallucinated objects: `1238 -> 1077`

Preservation tradeoff:

- `firstlogit_removal_top10`
  - correct objects: `-424`
  - object mentions: `-673`
- `dual_phrase_replace_v1`
  - correct objects: `-211`
  - object mentions: `-372`

So the aggressive branch is stronger in raw metric reduction, but it pays about double the correct-object loss of the dual branch.

## 8. `firstlogit_removal_top10` Analysis

Strengths:

- best expanded raw metric result
- best expanded hallucinated-object reduction
- broad action coverage:
  - edited images: `535`
  - edited mentions: `665`

Costs:

- all edits are removals
- correct-object loss is substantial:
  - removed hallucinated mentions: `249`
  - removed correct mentions: `416`
- hallucination reduction per correct loss: `0.5986`

Quality review highlights:

- grammar / coherence issue rate: `0.0376`
- first-logit-only share among edited rows: `0.6722`
- correct-loss concentration:
  - `chair 48`
  - `person 30`
  - `remote 28`
  - `cup 25`
  - `car 19`

Typical failure modes:

- malformed local deletions around `Wii remote`
- dropped spaces such as `wine glass,and`
- dangling phrase fragments such as `back .`

Interpretation:

- this remains the best aggressive upper-bound-style correction candidate
- but the qualitative and preservation costs are real and should not be hidden behind CHAIR alone

## 9. `dual_phrase_replace_v1` Analysis

Strengths:

- still materially improves over fixed `first_logit`
- lower edit volume than direct removal:
  - edited images: `370`
  - edited mentions: `370`
- smaller preservation cost:
  - correct delta vs fixed: `-211`
  - object delta vs fixed: `-372`

Edit structure:

- replaced phrase count: `75`
- remaining edit rows are still mostly conservative removals: `295`
- edited rows are strictly `first_logit_only`

Quality review highlights:

- grammar / coherence issue rate: `0.0081`
- first-logit-only share among edited rows: `1.0000`
- correct-loss concentration is milder than removal:
  - `chair 23`
  - `sports ball 13`
  - `cup 13`
  - `car 10`
  - `truck 9`

Interpretation:

- this route is not "pure replacement", but it does perform real phrase replacement when a safer local alternative exists
- it is clearly more natural than direct removal under the current qualitative heuristics

## 10. Risk-Benefit Curve

Diagnostic risk slices on the expanded fixed-source pool:

| Method | Slice | CHAIRs | CHAIRi | Hallucinated Delta vs fixed | Correct Delta vs fixed | Reduction / Correct Loss |
|---|---|---:|---:|---:|---:|---:|
| `firstlogit_removal` | top `5%` | `0.1446` | `0.0464` | `-177` | `-323` | `0.5584` |
| `firstlogit_removal` | top `10%` | `0.1344` | `0.0435` | `-249` | `-424` | `0.5986` |
| `firstlogit_removal` | top `20%` | `0.1150` | `0.0385` | `-375` | `-580` | `0.6625` |
| `dual_phrase_replace_v1` | top `5%` | `0.1530` | `0.0489` | `-105` | `-120` | `0.8750` |
| `dual_phrase_replace_v1` | top `10%` | `0.1456` | `0.0468` | `-161` | `-211` | `0.7630` |
| `dual_phrase_replace_v1` | top `20%` | `0.1286` | `0.0424` | `-273` | `-343` | `0.8101` |

Reading:

- pure CHAIR keeps improving through top `20%` for both branches
- preservation is healthier for the dual route at every slice
- top `20%` behaves like a diagnostic upper bound, not a default action
- top `10%` remains the clean preregistered default operating slice for reporting

## 11. Quality Review

Quality verdict by branch:

- `firstlogit_removal_top10`
  - strongest raw score
  - more visible local deletion damage
  - more concentrated correct-object loss
- `dual_phrase_replace_v1`
  - clearly cleaner local language
  - lower grammar artifact rate
  - lower correct-object loss
  - more naturally aligns with a phrase-level correction story

## 12. Full Confirmation Update

The readiness question is now resolved: the score-first full run completed on the full `40504`-image caption pool.

Final full fixed-source risk table:

- mention rows: `84406`
- images with mentions: `39606`
- hallucinated mentions: `7781`
- top `10%` threshold: `0.693014`
- top `10%` precision / recall: `0.3179 / 0.3448`
- `first_logit_only` top-`10%` precision: `0.4712`
- `common` top-`10%` precision: `0.1961`

Interpretation:

- the weighted verifier remains much sharper on source-exclusive risky mentions
- dominant top-`10%` family remains `introduced_focused_weighted_score`
- full confirmation supports keeping the weighted training-free verifier as the main evidence surface

## 13. Full Main Metrics

Full `40504`-image adapted evaluation:

| Method | CHAIRs | CHAIRi | Object Mentions | Correct Object Count | Hallucinated Object Count | Edited Images | Edited Mentions | Correct Delta vs fixed | Hallucinated Delta vs fixed |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `regular` | `0.2037` | `0.0655` | `181268` | `169393` | `11875` | `0` | `0` | `-8438` | `+2266` |
| fixed `first_logit` | `0.1631` | `0.0513` | `187440` | `177831` | `9609` | `0` | `0` | `0` | `0` |
| `firstlogit_removal_top10` | `0.1291` | `0.0413` | `181848` | `174332` | `7516` | `4463` | `5540` | `-3499` | `-2093` |
| `dual_phrase_replace_v1` | `0.1403` | `0.0444` | `184391` | `176204` | `8187` | `3037` | `3037` | `-1627` | `-1422` |

Full-scale reading:

- both retained correction branches still beat fixed `first_logit`
- `firstlogit_removal_top10` stays the metric-strong aggressive branch
- `dual_phrase_replace_v1` stays the quality-preserving branch
- the `5000`-image story did not flip at full scale

## 14. Full Risk-Benefit And Quality Takeaways

Full diagnostic slices:

- removal `top5 / top10 / top20` CHAIRs:
  - `0.1422 / 0.1291 / 0.1105`
- dual `top5 / top10 / top20` CHAIRs:
  - `0.1507 / 0.1403 / 0.1248`

Preservation ratios:

- removal hallucination reduction per correct-loss:
  - `top5 0.5334`
  - `top10 0.6060`
  - `top20 0.6504`
- dual hallucination reduction per correct-loss:
  - `top5 0.9680`
  - `top10 0.8772`
  - `top20 0.8332`

Quality review at full scale:

- removal grammar/coherence issue rate: `0.0449`
- dual grammar/coherence issue rate: markedly lower and still the cleaner local-language branch
- removal correct-loss concentration remains visible in categories such as `chair`, `remote`, `person`, and `cup`
- dual still performs real phrase replacement:
  - replaced phrase count: `623`
- dual did not collapse into a pure removal-only route

Current conclusion:

- `top10` remains the preregistered default operating slice
- `top20` still behaves like a diagnostic upper bound, not the default reportable action
- both branches should still be retained

## 15. Full Near-Official Alignment

Full near-official Python3 alignment was successfully reused without touching the official Python2 script.

Near-official full results:

- `regular`
  - `CHAIRs=0.1997`
  - `CHAIRi=0.0669`
- fixed `first_logit`
  - `CHAIRs=0.1594`
  - `CHAIRi=0.0524`
- `firstlogit_removal_top10`
  - `CHAIRs=0.1267`
  - `CHAIRi=0.0424`
- `dual_phrase_replace_v1`
  - `CHAIRs=0.1374`
  - `CHAIRi=0.0455`

Alignment takeaway:

- ordering matches the adapted evaluator
- full near-official supports the same main ranking:
  - `firstlogit_removal_top10` best raw score
  - `dual_phrase_replace_v1` second-best and more preservation-friendly

Shared pattern:

- both methods mainly act on source-exclusive risky mentions
- this is good news for the current mechanism story, because the verifier is not mostly firing on shared/common objects

## 15A. Candidate A Safer-Removal Diagnostic

Candidate A full diagnostic:

- method: `removal_top10_firstlogit_only_guard`
- rule:
  - keep the current full top-`10%` risk slice
  - remove only `first_logit_only` risky mentions
  - abstain on all `common` mentions
- adapted full metrics:
  - `CHAIRs=0.1356`
  - `CHAIRi=0.0430`
  - hallucinated objects: `7908`
  - correct object count: `175912`
- near-official full metrics:
  - `CHAIRs=0.1329`
  - `CHAIRi=0.0441`
  - hallucinated objects: `7712`
  - object mentions: `174848`

Tradeoff summary versus original `firstlogit_removal_top10`:

- retains `81.27%` of original removal hallucination reduction
- saves `1580` correct mentions
- gives back `392` hallucinated objects
- edits are fully source-exclusive by construction:
  - `first_logit_only edit count = 3599`
  - `common edit count = 0`
- grammar / coherence heuristic issue rate:
  - Candidate A: `0.0109`
  - original removal: `0.0449`

Interpretation:

- Candidate A is useful as an additional safer-removal diagnostic branch
- it sits between original removal and `dual_phrase_replace_v1`
- it does **not** replace `firstlogit_removal_top10`
- it does **not** replace `dual_phrase_replace_v1`
- the retained full-confirmed branches remain unchanged

## 16. Historical `5000` Near-Official Alignment

Keep the old expanded subset alignment for reference:

| Method | CHAIRs | CHAIRi | Object Mentions | Hallucinated Objects |
|---|---:|---:|---:|---:|
| `regular_subset` | `0.2038` | `0.0682` | `21460` | `1463` |
| `fixed_first_logit_subset` | `0.1620` | `0.0543` | `22270` | `1209` |
| `firstlogit_removal_top10` | `0.1318` | `0.0448` | `21631` | `970` |
| `dual_phrase_replace_v1` | `0.1430` | `0.0482` | `21920` | `1056` |

Why keep it:

- it preserves the earlier expanded confirmation checkpoint
- it shows the full result did not reverse the `5000` ordering

## 17. Whether Results Are Strong Enough For Full Confirmation Or Paper Discussion

Current judgment:

- full confirmation: `completed`
- strong enough for paper-positioning discussion: `yes`
- strong enough to collapse to a single branch automatically: `no`

Interpretation:

- the data requirement for score-first confirmation is now satisfied
- the next discussion can move to how to present the two-branch result, not whether the branches survive scale-up

## 18. Which Branch Is Metric-Strong

Metric-strong branch:

- `firstlogit_removal_top10`

Current role:

- aggressive correction candidate
- upper-bound-style route for maximum hallucination reduction under the current verifier

## 19. Which Branch Is Quality-Preserving

Quality-preserving branch:

- `dual_phrase_replace_v1`

Current role:

- cleaner phrase-level correction candidate
- better aligned with a story centered on preserving supported content while editing unsupported local mentions

## 20. Remaining Caveats And Next Recommendation

Remaining caveats:

- the verifier is still sharper on source-exclusive mentions than on common mentions
- `firstlogit_removal_top10` still raises the "fewer objects" challenge if presented without preservation metrics
- `dual_phrase_replace_v1` still mixes real replacement with conservative removal, rather than being a pure replacement-only method
- near-official alignment is strong supporting evidence, but it is still the Python3 alignment path rather than untouched official Python2 execution

Next recommendation:

1. keep both branches alive for paper-facing discussion
2. present `firstlogit_removal_top10` as the metric-strong aggressive branch
3. present `dual_phrase_replace_v1` as the quality-preserving branch
4. keep `removal_top10_firstlogit_only_guard` only as an additional safer-removal diagnostic branch
5. do not let Candidate A replace either retained branch automatically
6. keep the weighted training-free verifier as the main evidence source
7. keep the classifier only as backup / diagnostic
8. do not let Codex auto-start a new method line without explicit user approval
