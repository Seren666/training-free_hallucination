# LLaVA AMBER Paper-Ready Summary

## Recommended positioning

- COCO-CHAIR remains the main result dataset
- AMBER full should be presented as cross-dataset follow-up evidence
- AMBER strengthens generality claims, but it does not replace COCO-CHAIR

## Clean AMBER Full Table

| Method | CHAIR | Cover | Hal | Cog |
|---|---:|---:|---:|---:|
| `regular` | 7.0 | 50.5 | 32.3 | 3.8 |
| fixed / FLB-equivalent | 4.8 | 48.8 | 24.5 | 2.2 |
| `firstlogit_removal_top10` | 4.7 | 48.7 | 23.7 | 2.0 |
| `dual_phrase_replace_v1` | 4.7 | 48.8 | 24.0 | 2.1 |
| `removal_top10_firstlogit_only_guard` / Candidate A | 4.7 | 48.8 | 23.9 | 2.1 |

## Cross-Dataset Trend Table

| Trend question | Full COCO-CHAIR | FLB-aligned COCO-500 | AMBER full | Overall reading |
|---|---|---|---|---|
| fixed / FLB-equivalent beats `regular` | yes | yes | yes | stable |
| retained branches beat fixed / FLB-equivalent | yes | yes | yes, by small margins | stable but modest on AMBER |
| `firstlogit_removal_top10` is most metric-strong | yes | yes | yes | stable |
| `dual_phrase_replace_v1` is most quality-preserving | yes | yes | yes | stable |
| Candidate A is safer-removal / source-aware | yes | yes | yes | stable |

## Recommended wording

Suggested wording:

`On AMBER full generative evaluation, FLB-equivalent substantially improves over regular LLaVA, and our retained correction branches provide additional small but consistent reductions in hallucination metrics. In particular, dual_phrase_replace_v1 and Candidate A preserve Cover while reducing Hal/Cog, supporting cross-dataset generality of the mention-level correction framework.`

Safer extension:

`These AMBER results complement, rather than replace, the main COCO-CHAIR findings. They show that the direction of improvement is not confined to a single benchmark protocol.`

## Caveats

- do not claim raw COCO-CHAIR and AMBER CHAIR scales are directly comparable
- do not claim AMBER replaces COCO-CHAIR as the main benchmark
- do not claim universal superiority across all datasets
- do not claim final branch selection
- do not claim InstructBLIP or Qwen retained-branch portability here

## What belongs in main paper vs appendix

Main paper:
- one compact AMBER table
- one short cross-dataset trend paragraph
- one sentence on branch roles

Appendix:
- detailed full AMBER comparison table with deltas
- branch-role archive
- cross-dataset caveats
- retention summary with "no final branch selection" explicitly stated
