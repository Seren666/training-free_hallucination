# Public Result Tables

## Main Caption-Side Results

Lower is better for CHAIRs, CHAIRi, AMBER CHAIR, AMBER Hal, OpenCHAIR, and Sentence.

| Model | Benchmark | Metric | Regular | FLB | OCV on Regular | OCV on FLB | Reduction vs FLB |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| InstructBLIP-7B | AMBER-1004 | AMBER CHAIR | 14.1 | 10.9 | 12.1 | 10.3 | 0.6 (5.5%) |
| InstructBLIP-7B | COCO/CHAIR-500 | CHAIRs | 0.2620 | 0.2360 | 0.2620 | 0.1340 | 0.1020 (43.2%) |
| InstructBLIP-7B | OpenCHAIR | OpenCHAIR | 0.1731 | 0.1731 | 0.1667 | 0.1667 | 0.0065 (3.7%) |
| LLaVA-1.5-7B | AMBER-1004 | AMBER CHAIR | 11.6 | 6.1 | 8.8 | 5.0 | 1.1 (18.0%) |
| LLaVA-1.5-7B | COCO/CHAIR-500 | CHAIRs | 0.1720 | 0.1560 | 0.1220 | 0.1100 | 0.0460 (29.5%) |
| LLaVA-1.5-7B | OpenCHAIR | OpenCHAIR | 0.1803 | 0.1621 | 0.1730 | 0.1584 | 0.0036 (2.2%) |

## Cross-Model OpenCHAIR Summary

| Model | Regular | FLB | OCV on Regular | OCV on FLB | Caveat |
| --- | ---: | ---: | ---: | ---: | --- |
| InstructBLIP-7B | 0.1731 | 0.1731 | 0.1667 | 0.1667 | Strict FLB branch executed but produced 0 caption changes vs Regular and saved processor summaries do not verify hook entry; treat as regular-equivalent source in this round. |
| InternVL3.5-8B-HF | 0.2340 | 0.2275 | 0.2259 | 0.2218 |  |
| LLaVA-1.5-7B | 0.1803 | 0.1621 | 0.1730 | 0.1584 |  |
| Qwen2.5-VL-7B-Instruct | 0.1825 | 0.1788 | 0.1782 | 0.1726 |  |

## External Baseline Records

These rows are included as reproduced/caveated context, not official leaderboard claims.

| Method | Benchmark | Scope | CHAIRs | CHAIRi | POPE Acc | POPE F1 | Status | Caveat |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| regular | COCO/CHAIR | locked CHAIR-500 | 0.1880 | 0.0561 |  |  | main_baseline | Main caption baseline under the locked subset and current evaluator. |
| fixed_FLB_equivalent | COCO/CHAIR | locked CHAIR-500 | 0.1440 | 0.0429 |  |  | internal_reference | Stronger-source OCV variant; not an external baseline. |
| firstlogit_removal_top10 | COCO/CHAIR | locked CHAIR-500 | 0.1160 | 0.0353 |  |  | internal_reference | Stronger-source OCV variant; not an external baseline. |
| dual_phrase_replace_v1 | COCO/CHAIR | locked CHAIR-500 | 0.1260 | 0.0378 |  |  | internal_reference | Retained internal branch; not an external baseline. |
| VCD | COCO/CHAIR | locked CHAIR-500 | 0.2220 | 0.0779 |  |  | external_actual_score | Same-protocol reproduction only; weak under our caption protocol; not an official native caption result. |
| AGLA | COCO/CHAIR | locked CHAIR-500 | 0.1900 | 0.0578 |  |  | external_actual_score | Repo is more native to POPE than to CHAIR, but the caption-side reproduction is stable and evaluator-compatible. |
| MaskCD | COCO/CHAIR | locked CHAIR-500 | 0.3460 | 0.1014 |  |  | external_actual_score | Protocol-compatible and caption-native, but outputs are long and templated and inflate object commitments. |
| DeCo | COCO/CHAIR | smoke10 | 0.1000 | 0.0278 |  |  | smoke_only | Quality unstable; safe_to_run_chair500=no; not a carried score line. |
| DeCo | COCO/CHAIR | locked CHAIR-500 | 0.1560 | 0.0559 |  |  | external_actual_score | Completed full row, but quality remains truncation-heavy: 474/500 hit max_new_tokens and 107/500 show obvious dangling endings. |
| regular | POPE | COCO 3-split average |  |  | 0.8552 | 0.8407 | main_baseline | COCO-only average; do not mix with the separate 27k all-dataset average. |
| AGLA | POPE | COCO 3-split average |  |  | 0.8574 | 0.8437 | external_actual_score | COCO only in this round; GQA and AOKVQA were not rerun here. |
| VCD | POPE | COCO 3-split average |  |  | 0.8341 | 0.8217 | caveated_actual_score | Mixed-provenance head-to-head; do not treat this row as a clean official VCD verdict. |

## Runtime Summary

| Model | Benchmark | Stage | Images | Total sec | Sec/image | Includes generation? | Includes verification? |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| LLaVA-1.5-7B | COCO/CHAIR-500 | Regular generation | 20 | 20.6637 | 1.033185 | yes | no |
| LLaVA-1.5-7B | COCO/CHAIR-500 | Regular generation | 500 | unknown | 1.288 | yes | no |
| LLaVA-1.5-7B | COCO/CHAIR-500 | FLB generation | 500 | unknown | 1.2923 | yes | no |
| LLaVA-1.5-7B | COCO/CHAIR-500 | OCV signal extraction | 495 | unknown | 0.053347 | no | yes |
| InstructBLIP-7B | COCO/CHAIR-500 | Regular generation | 500 | unknown | 1.2221 | yes | no |
| InstructBLIP-7B | COCO/CHAIR-500 | FLB generation | 500 | unknown | 1.2368 | yes | no |
| InstructBLIP-7B | COCO/CHAIR-500 | OCV verification forward | 20 | 1.7763 | 0.088816 | no | yes |
| InstructBLIP-7B | COCO/CHAIR-500 | OCV verification forward | 20 | 0.5071 | 0.025356 | no | yes |
| InstructBLIP-7B | COCO/CHAIR-500 | OCV verification forward | 20 | 0.4457 | 0.022287 | no | yes |
| InstructBLIP-7B | COCO/CHAIR-500 | OCV signal extraction | 489 | unknown | 0.02223 | no | yes |
| InstructBLIP-7B | COCO/CHAIR-500 | OCV signal extraction | 498 | unknown | 0.027573 | no | yes |
| all artifact-backed rows | mixed | risk scoring table aggregation | not_applicable | 0.002106 | not_applicable | no | no |
| all artifact-backed rows | mixed | bounded-editing summary aggregation | not_applicable | 0.00134 | not_applicable | no | no |
