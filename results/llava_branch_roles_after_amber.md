# LLaVA Branch Roles After AMBER

No final branch selection has been made.
All three retained branches remain preserved.
The user will decide after reviewing the full result package.

## 1. `firstlogit_removal_top10`

- strongest hallucination reduction on full COCO-CHAIR
- strongest hallucination reduction on FLB-aligned COCO-CHAIR-500
- lowest `Hal/Cog` on AMBER full
- more aggressive than the other retained branches
- should remain the metric-optimized / aggressive diagnostic branch

## 2. `dual_phrase_replace_v1`

- quality-preserving retained branch
- strongest paper-facing default candidate if one conservative branch must be described
- on AMBER full, preserves `Cover` relative to fixed / FLB-equivalent
- also improves `Hal/Cog` over fixed / FLB-equivalent
- keeps the "correction without over-aggressive deletion" story clean

## 3. `removal_top10_firstlogit_only_guard` / Candidate A

- safer source-aware removal retained branch
- strong COCO tradeoff
- on AMBER full, preserves `Cover` and is slightly better than `dual` on `Hal`
- remains the safer-removal retained diagnostic branch

## Clear status statement

- `candidateA_dual_replace_then_remove` remains only an additional diagnostic candidate
- it is not a retained branch
- no branch selection has been finalized
- all three retained branches are intentionally preserved side by side
