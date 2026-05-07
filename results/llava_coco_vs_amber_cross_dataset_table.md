# LLaVA COCO-CHAIR vs AMBER Cross-Dataset Table

Important note:

- do not directly compare numeric CHAIR scale across COCO-CHAIR and AMBER
- compare only within-dataset relative trends

## Full COCO-CHAIR 40504

| Method | CHAIRs | CHAIRi | Hallucinated | Correct | Mentions |
|---|---:|---:|---:|---:|---:|
| `regular` | 0.2037 | 0.0655 | 11875 | 169393 | 181268 |
| fixed / FLB-equivalent | 0.1631 | 0.0513 | 9609 | 177831 | 187440 |
| `firstlogit_removal_top10` | 0.1291 | 0.0413 | 7516 | 174332 | 181848 |
| `dual_phrase_replace_v1` | 0.1403 | 0.0444 | 8187 | 176204 | 184391 |
| `removal_top10_firstlogit_only_guard` / Candidate A | 0.1356 | 0.0430 | 7908 | 175912 | 183820 |

## FLB-Aligned COCO-CHAIR-500

| Method | CHAIRs | CHAIRi |
|---|---:|---:|
| `regular` | 0.1880 | 0.0561 |
| fixed / FLB-equivalent | 0.1440 | 0.0429 |
| `firstlogit_removal_top10` | 0.1160 | 0.0353 |
| `dual_phrase_replace_v1` | 0.1260 | 0.0378 |
| `removal_top10_firstlogit_only_guard` / Candidate A | 0.1220 | 0.0371 |

## AMBER Full 1004

| Method | CHAIR | Cover | Hal | Cog |
|---|---:|---:|---:|---:|
| `regular` | 7.0 | 50.5 | 32.3 | 3.8 |
| fixed / FLB-equivalent | 4.8 | 48.8 | 24.5 | 2.2 |
| `firstlogit_removal_top10` | 4.7 | 48.7 | 23.7 | 2.0 |
| `dual_phrase_replace_v1` | 4.7 | 48.8 | 24.0 | 2.1 |
| `removal_top10_firstlogit_only_guard` / Candidate A | 4.7 | 48.8 | 23.9 | 2.1 |

## Relative Trend Summary

| Method | Full COCO-CHAIR trend | FLB-aligned COCO-500 trend | AMBER full trend | Cross-dataset role |
|---|---|---|---|---|
| fixed / FLB-equivalent | clear improvement over `regular` | clear improvement over `regular` | clear improvement over `regular` | robust improved baseline |
| `firstlogit_removal_top10` | strongest raw hallucination reduction | strongest raw hallucination reduction | lowest `Hal/Cog`, slight `Cover` cost | metric-strong aggressive diagnostic |
| `dual_phrase_replace_v1` | improves over fixed with less correct-loss than raw removal | improves over fixed with conservative tradeoff | preserves `Cover` while improving `Hal/Cog` | quality-preserving retained branch |
| Candidate A | improves over fixed with safer-removal profile | improves over fixed with safer-removal profile | preserves `Cover`, slightly better `Hal` than `dual` | safer source-aware removal retained branch |
