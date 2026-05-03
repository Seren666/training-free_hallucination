# Correction Full Confirmation Readiness

> Date: 2026-05-03
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

Shared pattern:

- both methods mainly act on source-exclusive risky mentions
- this is good news for the current mechanism story, because the verifier is not mostly firing on shared/common objects

## 12. Near-Official Alignment

Near-official `5000`-subset alignment was completed on the same expanded subset without rerunning captions.

| Method | CHAIRs | CHAIRi | Object Mentions | Hallucinated Objects |
|---|---:|---:|---:|---:|
| `regular_subset` | `0.2038` | `0.0682` | `21460` | `1463` |
| `fixed_first_logit_subset` | `0.1620` | `0.0543` | `22270` | `1209` |
| `firstlogit_removal_top10` | `0.1318` | `0.0448` | `21631` | `970` |
| `dual_phrase_replace_v1` | `0.1430` | `0.0482` | `21920` | `1056` |

Alignment reading:

- the method ordering is unchanged under the near-official path
- `firstlogit_removal_top10` still gives the best raw CHAIR reduction
- `dual_phrase_replace_v1` still improves clearly over fixed `first_logit`
- the expanded adapted-evaluator conclusion is therefore not a scoring artifact

## 13. Whether Results Are Strong Enough For Full Confirmation Or Paper Discussion

Current judgment:

- strong enough for a user-approved full-confirmation discussion: `yes`
- strong enough to auto-start full confirmation without approval: `no`
- strong enough for paper-positioning discussion: `yes`, with the usual near-official caveat

Why not auto-full:

- full weighted risk extraction is still missing
- projected full probe-only time is about `25.7 h`
- this round already achieved a meaningful scale-up from `1000` to `5000`

## 14. Which Branch Is Metric-Strong

Metric-strong branch:

- `firstlogit_removal_top10`

Current role:

- aggressive correction candidate
- likely upper-bound-style route for raw hallucination reduction

## 15. Which Branch Is Quality-Preserving

Quality-preserving branch:

- `dual_phrase_replace_v1`

Current role:

- cleaner phrase-level correction candidate
- better aligned with a paper narrative centered on preserving supported content while editing unsupported local mentions

## 16. Remaining Caveats

- this is still expanded confirmation, not full `40504`-image confirmation
- the verifier is still sharper on source-exclusive mentions than on common mentions
- `firstlogit_removal_top10` still raises the "fewer objects" challenge if presented without preservation metrics
- `dual_phrase_replace_v1` still removes many mentions and is not a pure replacement method
- near-official alignment is stronger than adapted-only evaluation, but it is still not untouched official Python2 CHAIR

## 17. Next Recommendation

The clean next-step discussion is now:

1. whether to run a user-approved full two-branch confirmation
2. or whether the current `5000`-image expanded confirmation is already sufficient for paper-level method positioning

What should stay fixed:

- keep both branches alive
- do not let Codex auto-eliminate one branch
- do not let Codex auto-start a full extraction run
- keep the weighted training-free verifier as the primary evidence source
- keep the classifier only as backup / diagnostic
