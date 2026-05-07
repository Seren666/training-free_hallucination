# Branch Full Result Archive

## Scope

- This appendix consolidates all completed retained-branch results across the finished datasets and evaluation protocols.
- It keeps the three retained LLaVA branches visible side by side: `firstlogit_removal_top10`, `dual_phrase_replace_v1`, and `removal_top10_firstlogit_only_guard / Candidate A`.
- `candidateA_dual_replace_then_remove` remains an additional diagnostic candidate only and is not listed as a retained branch.
- No branch selection has been finalized.

## 1. COCO-CHAIR Full 40504

| Method | CHAIRs | CHAIRi | Hallucinated | Correct | Mentions |
|---|---:|---:|---:|---:|---:|
| `regular` | 0.2037 | 0.0655 | 11875 | 169393 | 181268 |
| fixed `firstlogit` / FLB-equivalent | 0.1631 | 0.0513 | 9609 | 177831 | 187440 |
| `firstlogit_removal_top10` | 0.1291 | 0.0413 | 7516 | 174332 | 181848 |
| `dual_phrase_replace_v1` | 0.1403 | 0.0444 | 8187 | 176204 | 184391 |
| `removal_top10_firstlogit_only_guard` / Candidate A | 0.1356 | 0.0430 | 7908 | 175912 | 183820 |

Interpretation:

- `firstlogit_removal_top10` gives the strongest raw CHAIR reduction, but it also pays the largest correct-object loss.
- `dual_phrase_replace_v1` preserves correct objects and caption quality more naturally.
- Candidate A keeps the safer source-aware guarded-removal story.
- All three branches remain retained; no selection has been made.

## 2. Near-Official CHAIR Full Alignment

| Method | CHAIRs | CHAIRi |
|---|---:|---:|
| `regular` | 0.1997 | 0.0669 |
| fixed `firstlogit` | 0.1594 | 0.0524 |
| `firstlogit_removal_top10` | 0.1267 | 0.0424 |
| `dual_phrase_replace_v1` | 0.1374 | 0.0455 |
| `removal_top10_firstlogit_only_guard` / Candidate A | 0.1329 | 0.0441 |

Interpretation:

- The near-official alignment check preserves the same ranking trend as the adapted evaluator.
- This reduces concern that the main COCO-CHAIR conclusion is an adapted-evaluator artifact.
- It supports keeping all three retained branches in the advisor package.

## 3. FLB-Aligned COCO-CHAIR-500

| Method | CHAIRs | CHAIRi | Hallucinated / Correct / Mentions |
|---|---:|---:|---:|
| `regular` | 0.1880 | 0.0561 | 128 / 2152 / 2280 |
| fixed `firstlogit` | 0.1440 | 0.0429 | 101 / 2255 / 2356 |
| FLB exact | 0.1440 | 0.0429 | 101 / 2255 / 2356 |
| `firstlogit_removal_top10` | 0.1160 | 0.0353 | 81 / 2212 / 2293 |
| `dual_phrase_replace_v1` | 0.1260 | 0.0378 | 88 / 2237 / 2325 |
| `removal_top10_firstlogit_only_guard` / Candidate A | 0.1220 | 0.0371 | 86 / 2233 / 2319 |

Interpretation:

- On the current deterministic LLaVA caption path, `FLB exact == fixed_firstlogit`.
- All three retained branches beat the FLB-equivalent baseline.
- `firstlogit_removal_top10` is strongest in raw score; `dual` and Candidate A are the more conservative branches.
- This comparison does not remove any retained branch.

## 4. AMBER Compact 200

| Method | CHAIR | Cover | Hal | Cog |
|---|---:|---:|---:|---:|
| `regular` | 7.8 | 50.3 | 35.5 | 3.0 |
| fixed / FLB-equivalent | 5.0 | 47.7 | 26.0 | 1.8 |
| `firstlogit_removal_top10` | 5.1 | 47.5 | 25.0 | 1.7 |
| `dual_phrase_replace_v1` | 5.0 | 47.7 | 25.5 | 1.7 |
| `removal_top10_firstlogit_only_guard` / Candidate A | 5.0 | 47.7 | 25.5 | 1.7 |

Interpretation:

- On AMBER compact 200, the retained branches do not cleanly dominate fixed / FLB-equivalent on CHAIR.
- `dual` and Candidate A match CHAIR and Cover while slightly improving Hal and Cog.
- `firstlogit_removal_top10` has the lowest Hal but gives up a little CHAIR / Cover.
- This is cross-dataset follow-up evidence, not a replacement for the main COCO-CHAIR conclusion.

## 5. AMBER Full 1004

Archive boundary:

- The following full AMBER generative result comes from the previous remote handoff.
- It still needs a fresh read-only integrity check against the remote result files once SSH access recovers.
- Current recorded setup: `sample count = 1004`, `max_new_tokens = 128`.

| Method | CHAIR | Cover | Hal | Cog |
|---|---:|---:|---:|---:|
| `regular` | 7.0 | 50.5 | 32.3 | 3.8 |
| fixed / FLB-equivalent | 4.8 | 48.8 | 24.5 | 2.2 |
| `dual_phrase_replace_v1` | 4.7 | 48.8 | 24.0 | 2.1 |
| `removal_top10_firstlogit_only_guard` / Candidate A | 4.7 | 48.8 | 23.9 | 2.1 |
| `firstlogit_removal_top10` diagnostic | 4.7 | 48.7 | 23.7 | 2.0 |

Interpretation:

- Fixed / FLB-equivalent clearly improves over regular on full AMBER.
- The retained branches show mild additional gains relative to fixed / FLB-equivalent.
- `dual` and Candidate A preserve Cover, while `firstlogit_removal_top10` stays the most aggressive diagnostic branch.
- The AMBER full result is archived as follow-up evidence and still needs a fresh integrity check.

## 6. Qwen Cross-Model Diagnostic Summary

| Model | Scale | Regular CHAIRs / CHAIRi | Fixed CHAIRs / CHAIRi | Main signal note | Action note |
|---|---|---|---|---|---|
| `Qwen3-VL` | 5000-image probe | 0.0568 / 0.0344 | 0.0578 / 0.0348 | attention-anchor signal partially useful | removal unsafe; replacement coverage `0/10`; action blocked |
| `Qwen2.5-VL-7B-Instruct` | 1000 paired caption / probe / action pilot | 0.0540 / 0.0349 | 0.0570 / 0.0367 | attention useful; visual cosine inverted / useless | removal unsafe; replacement coverage `0/10`; action blocked |

Interpretation:

- The Qwen pipeline shows portable generation-control-probe mechanics and partially portable internal signals.
- It does not provide portable action correction.
- Qwen does not change the retained LLaVA branch status.

## 7. Retention Summary Across Finished Results

| Branch | Main COCO role | FLB-aligned CHAIR-500 | AMBER compact | AMBER full | Current retained status |
|---|---|---|---|---|---|
| `firstlogit_removal_top10` | metric-strong / aggressive | strongest raw score | best Hal, slightly worse CHAIR / Cover | best Hal / Cog, more aggressive | retained |
| `dual_phrase_replace_v1` | quality-preserving / replacement | beats FLB-equivalent; more conservative than raw removal | matches CHAIR / Cover, slightly better Hal / Cog | mild gain over fixed / FLB, Cover preserved | retained |
| `removal_top10_firstlogit_only_guard` / Candidate A | safer-removal / source-aware guarded | beats FLB-equivalent; sits between removal and dual | matches CHAIR / Cover, slightly better Hal / Cog | mild gain over fixed / FLB, Cover preserved | retained |

Interpretation:

- The branch archive supports keeping three distinct retained positions rather than collapsing to one winner too early.
- No branch selection has been finalized.

## 8. Follow-up Queue

- AMBER full integrity check is still needed once SSH access recovers.
- InstructBLIP should be the next model expansion target.
- LLaVA-NeXT can be considered after InstructBLIP.
- MME, HallusionBench, and MMHal-Bench can be prepared as appendix diagnostics.
- No branch should be dropped before the user reviews all retained-branch results.

## 9. 2026-05-07 AMBER Full Integrity Refresh

The earlier AMBER full archive caveat has now been refreshed by a read-only SSH verification against the remote files.

Verified:

- all five AMBER full output JSONs exist
- all five AMBER full eval JSONs exist
- all five methods have `1004` samples and `1004` generation successes
- all archived metrics match the remote eval files exactly

Refreshed AMBER full table:

| Method | CHAIR | Cover | Hal | Cog |
|---|---:|---:|---:|---:|
| `regular` | 7.0 | 50.5 | 32.3 | 3.8 |
| fixed / FLB-equivalent | 4.8 | 48.8 | 24.5 | 2.2 |
| `firstlogit_removal_top10` diagnostic | 4.7 | 48.7 | 23.7 | 2.0 |
| `dual_phrase_replace_v1` | 4.7 | 48.8 | 24.0 | 2.1 |
| `removal_top10_firstlogit_only_guard` / Candidate A | 4.7 | 48.8 | 23.9 | 2.1 |

Cross-dataset reading:

- the same qualitative branch ordering survives from COCO-CHAIR to AMBER
- fixed / FLB-equivalent remains the robust improved baseline
- `firstlogit_removal_top10` remains the strongest metric branch, but also the most aggressive
- `dual_phrase_replace_v1` remains the cleanest quality-preserving branch to describe in paper text
- Candidate A remains the safer source-aware removal branch

Archive caveats remain:

- AMBER is cross-dataset support evidence, not a replacement for the COCO-CHAIR main result
- `candidateA_dual_replace_then_remove` remains an additional diagnostic only
- no final branch selection has been finalized
