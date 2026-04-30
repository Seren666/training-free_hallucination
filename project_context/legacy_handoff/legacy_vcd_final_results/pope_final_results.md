# Legacy VCD: POPE Final Results

## 1. 这部分为什么值得保留

旧 VCD 仓库里，POPE / object hallucination 方向是最成熟、最稳定的一条线。

后续新项目即使不继续做 RAD-VCD，本部分仍然有两个可复用价值：

1. 它说明在 yes/no object hallucination 任务里，VCD 的主要收益高度集中在早期 answer decision，尤其是 step0 / answer boundary。
2. 它为后续的 first-logit / early-anchor 思路提供了一个很强的经验动机：早期决策位确实能吃到大多数有用信号。

## 2. 冻结方法

方法名：

- `SCMR-VCD`
- 全称：`Short-Circuit VCD with Disagreement Micro-Rescue`

冻结配置：

- `confmargin_threshold = 4.5`
- `confmargin_apply_tasks = pope`
- `shortcircuit_micro_rescue = enabled`
- `step0 VCD = enabled`
- `OPERA = disabled`
- `detector = disabled`
- `training = none`

冻结原因：

- 已在 `9/9` POPE split 上同时超过 full VCD 的质量和速度。
- 再继续改这条线的收益很低，而且会破坏已经清楚的主结论。

## 3. 最终结论

- `9/9` split: `F1 > full VCD`
- `9/9` split: `Accuracy > full VCD`
- `9/9` split: `s/sample < full VCD`
- `micro-rescue activation rate` 很低：约 `1.53%` 到 `3.33%`

更重要的理解不是“又比 full VCD 高了几点”，而是：

> 在 POPE 这类 yes/no object hallucination 上，full VCD 的主要有效干预并不需要 everywhere / full-depth 地持续开着；把干预压缩到最早的关键决策点，反而更好。

## 4. 9 个 split 最终表

| Split | Ours F1 | Full VCD F1 | F1 Gain | Ours Acc | Full VCD Acc | Acc Gain | Ours s/sample | Full VCD s/sample | Speedup | Rescue Rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| COCO random | 0.849105 | 0.840867 | +0.008238 | 0.862333 | 0.855667 | +0.006666 | 0.189322 | 0.221860 | 14.67% | 1.83% |
| COCO popular | 0.831485 | 0.822726 | +0.008759 | 0.843000 | 0.835667 | +0.007333 | 0.209124 | 0.227800 | 8.20% | 1.83% |
| COCO adversarial | 0.810622 | 0.801401 | +0.009221 | 0.819333 | 0.811000 | +0.008333 | 0.215628 | 0.222816 | 3.23% | 2.33% |
| GQA random | 0.861149 | 0.854983 | +0.006166 | 0.864667 | 0.859333 | +0.005334 | 0.190068 | 0.219241 | 13.31% | 1.53% |
| GQA popular | 0.807828 | 0.800000 | +0.007828 | 0.800333 | 0.792667 | +0.007666 | 0.194491 | 0.219389 | 11.35% | 2.50% |
| GQA adversarial | 0.788049 | 0.779343 | +0.008706 | 0.773000 | 0.765000 | +0.008000 | 0.217626 | 0.219898 | 1.03% | 2.90% |
| A-OKVQA random | 0.859673 | 0.854689 | +0.004984 | 0.862667 | 0.859000 | +0.003667 | 0.193268 | 0.220672 | 12.42% | 1.70% |
| A-OKVQA popular | 0.826187 | 0.822479 | +0.003708 | 0.823000 | 0.821000 | +0.002000 | 0.196252 | 0.222072 | 11.63% | 2.50% |
| A-OKVQA adversarial | 0.781347 | 0.777570 | +0.003777 | 0.764000 | 0.762000 | +0.002000 | 0.196838 | 0.221266 | 11.04% | 3.33% |

## 5. 对新项目还有什么参考价值

- 不要把它理解成“POPE 的 benchmark trick”。
- 真正能带走的是：在 object hallucination 的 yes/no 决策里，早期 answer-boundary 信号很强。
- 这份经验可以作为新项目里 first-logit / early-anchor 方向的背景动机。
- 但不要把这份 legacy 结论直接外推到 MME 一类更复杂任务。

## 6. 旧仓库中的相关入口

- 主评测入口：`E:\VScode\VCD\experiments\eval\object_hallucination_vqa_llava.py`
- POPE 评测脚本：`E:\VScode\VCD\experiments\eval\eval_pope.py`
- POPE baseline 命令模板：`E:\VScode\VCD\experiments\cd_scripts\llava1.5_pope.bash`
- step0 / micro-rescue 逻辑：`E:\VScode\VCD\vcd_utils\cd_step_selector.py`
- 底层采样与 route bookkeeping：`E:\VScode\VCD\vcd_utils\vcd_sample.py`

## 7. 来源

- `E:\VScode\VCD\reports\frozen_branch_status.md`
- `E:\VScode\training-free_hallucination\reports\self_understanding_note.md`
- `E:\VScode\training-free_hallucination\reports\advisor_stage_summary.md`
