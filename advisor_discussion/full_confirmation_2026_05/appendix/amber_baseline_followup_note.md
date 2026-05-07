# AMBER Baseline Follow-up Note

## Positioning

- AMBER is treated here as a follow-up dataset comparison rather than a replacement for the main COCO-CHAIR retained-branch story.
- The AMBER results do not demote, rename, or remove any retained branch.

## AMBER Compact 200

Setup:

- subset: first `200` official AMBER generative ids
- token budget: `max_new_tokens = 128`

| Method | CHAIR | Cover | Hal | Cog |
|---|---:|---:|---:|---:|
| `regular` | 7.8 | 50.3 | 35.5 | 3.0 |
| fixed / FLB-equivalent | 5.0 | 47.7 | 26.0 | 1.8 |
| `firstlogit_removal_top10` | 5.1 | 47.5 | 25.0 | 1.7 |
| `dual_phrase_replace_v1` | 5.0 | 47.7 | 25.5 | 1.7 |
| `removal_top10_firstlogit_only_guard` / Candidate A | 5.0 | 47.7 | 25.5 | 1.7 |

Interpretation:

- On compact 200, the retained branches do not cleanly beat fixed / FLB-equivalent on CHAIR.
- `dual` and Candidate A match CHAIR and Cover while slightly improving Hal and Cog.
- `firstlogit_removal_top10` lowers Hal the most but slightly worsens CHAIR and Cover.
- This supports a cross-dataset supplementary-gain story rather than a replacement of the main conclusion.

## AMBER Full 1004

Archive boundary:

- The following full AMBER generative result is recorded from the previous remote handoff.
- It still needs a fresh read-only integrity check against the remote files once SSH access recovers.
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
- The retained branches show light additional gains relative to fixed / FLB-equivalent.
- `dual` and Candidate A preserve Cover while slightly improving the risk metrics.
- `firstlogit_removal_top10` has the lowest Hal / Cog but remains the more aggressive diagnostic branch.

## Current Takeaway

- AMBER supports the usefulness of the fixed / FLB-equivalent baseline beyond COCO-CHAIR.
- It also supports keeping multiple retained branches alive: the aggressive metric branch, the quality-preserving branch, and the safer source-aware guarded-removal branch.
- The AMBER full note should remain appendix-only until the remote integrity check is refreshed.

## Next Required Follow-up

- AMBER full integrity check still needed once SSH recovers.
- InstructBLIP should be the next model expansion target.
- LLaVA-NeXT can be considered after InstructBLIP.
- No branch should be dropped before the user reviews all results.

## 2026-05-07 Integrity Refresh

Read-only SSH verification has now been completed against the remote AMBER full result files.

Verified:

- all five full AMBER output JSONs exist
- all five full AMBER eval JSONs exist
- sample count / `subset_size = 1004` for all five methods
- `generation_success_count = 1004` for all five methods
- `max_new_tokens = 128`
- archived metrics match the remote eval files exactly

Verified AMBER full table:

| Method | CHAIR | Cover | Hal | Cog |
|---|---:|---:|---:|---:|
| `regular` | 7.0 | 50.5 | 32.3 | 3.8 |
| fixed / FLB-equivalent | 4.8 | 48.8 | 24.5 | 2.2 |
| `dual_phrase_replace_v1` | 4.7 | 48.8 | 24.0 | 2.1 |
| `removal_top10_firstlogit_only_guard` / Candidate A | 4.7 | 48.8 | 23.9 | 2.1 |
| `firstlogit_removal_top10` diagnostic | 4.7 | 48.7 | 23.7 | 2.0 |

Cross-dataset reading after this integrity refresh:

- fixed / FLB-equivalent improves over `regular` on both COCO-CHAIR and AMBER
- all three retained branches improve over fixed / FLB-equivalent on both datasets
- `firstlogit_removal_top10` remains the metric-strong aggressive branch
- `dual_phrase_replace_v1` remains the quality-preserving branch
- Candidate A remains the safer source-aware removal branch

Caveats:

- AMBER remains follow-up cross-dataset evidence, not a replacement for the main COCO-CHAIR result
- the retained-branch gains over fixed / FLB-equivalent are smaller on AMBER than on COCO-CHAIR
- no final branch selection has been finalized
