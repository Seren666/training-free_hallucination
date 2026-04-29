# Legacy Handoff For New Project

## 1. 旧 VCD 仓库概览

旧本地目录：

- `E:\VScode\VCD`

它原本是基于官方 VCD 仓库扩出来的一条优化实验线，后面陆续长出了：

- POPE / object hallucination 的 `SCMR-VCD`
- MME harm avoidance
- MME self-diagnostic dominance line
- 一批 trace / audit / offline stitching / feasibility 检查

当前状态是：

- 这条旧线已经暂停；
- 不再继续在这个仓库里做 RAD-VCD / POPE-SCMR / MME dominance / VCD 优化实验；
- 新主项目目录已经换成 `E:\VScode\training-free_hallucination`。

## 2. 旧方向为什么暂停

暂停不是因为旧方向完全没有结果，而是因为：

1. POPE 这条线已经比较收束，`SCMR-VCD` 是成熟正结果，再往下改动收益很小。
2. MME 的 harm avoidance 该拿到的关键判断已经拿到了：
   - full VCD 不是全局无害；
   - text-only 是质量最强点，但模板依赖明显；
   - text_translation-only 是更稳妥的 Pareto 点。
3. dominance line 也已经把边界说清楚了：
   - 它是有价值的 self-diagnostic audit evidence；
   - 但还不够形成稳健 runtime router。
4. 再继续在旧仓库里做：
   - threshold 微调
   - rule stacking
   - damping / local skip 这种局部 intervention
   
   边际收益已经很低，而且容易把旧仓库越堆越乱。

所以旧方向现在最合理的处理方式，不是继续研究，而是整理成 legacy knowledge，供新项目按需参考。

## 3. 可保留的核心结论

### 3.1 POPE / object hallucination

- 在 yes/no object hallucination 任务里，VCD 的大多数有效收益集中在很早的 answer decision，尤其是 step0 / answer boundary。
- `SCMR-VCD` 已在 `9/9` POPE split 上同时超过 full VCD 的质量和速度。
- 这部分最适合被新项目复用为：first-logit / early-anchor 思路的动机背景。

### 3.2 MME / harm avoidance

- full VCD 在 MME 上总体很强，但不是全局无害。
- `harm text-only router` 是当前 MME 质量最强点，但有明显模板依赖。
- `harm text_translation-only` 是一个更稳妥的 speed-quality Pareto 点。
- 这部分更适合作为“强干预也会伤人”的经验背景，不适合作为新项目继续扩展的主线。

### 3.3 MME / dominance line

- `max_contrastive_dominance_ratio` 是有意义的 self-diagnostic audit signal。
- 它说明一部分 VCD harm risk 可以从推理轨迹中部分观察到。
- 但它没有形成稳健 runtime router。
- damping 和 local skip-VCD 都给出了负结果或不足结果。

## 4. POPE / step0 观察

旧方向最有价值的 POPE 观察可以压成一句话：

> 在 object hallucination 的 yes/no 决策里，早期 answer-boundary 信号非常强。

这件事的重要性在于：

- 它不是单纯说明 “SCMR 在 POPE 上赢了”；
- 它是在告诉后续新项目：如果研究 first-logit / early-anchor，这个方向是有经验动机的。

但同时也要保留旧线带来的反例：

- 这个结论不能直接外推到 MME 一类更复杂任务；
- 在 MME 上，单靠 step0 binary proxy 不够。

## 5. MME / dominance line 观察

这条线最后真正留下来的判断是：

- self-diagnostic signal 不是没有；
- 但 dominance 单信号只告诉我们 “VCD 这次干预很强”；
- 它不能单独区分：
  - harmful over-correction
  - beneficial visual correction

所以它更适合作为：

- evidence
- limitation

而不是当前正式方法。

### 5.1 需要特别保留的负结果

- sample-level composite fallback：有修复能力，但 benefit false fallback 偏高
- simple alpha damping：误伤少，但修复 harm 太少
- local skip-VCD：太粗暴，明显负结论
- one-token composite rescue：当前实现路径不安全，没有继续作为主线

## 6. 远程机入口和路径

旧方向主要运行在远程 AutoDL 机器：

- host: `connect.westc.seetacloud.com`
- port: `21607`
- user: `root`
- repo root: `/root/autodl-tmp/code/VCD`
- conda env: `/root/autodl-tmp/envs/vcd`
- HF cache: `/root/autodl-tmp/hf-home`

常见激活流程和运行坑，已另存到：

- `legacy_environment/remote_paths.md`

## 7. 模型 checkpoint 路径

- checkpoint: `/root/autodl-tmp/code/VCD/experiments/checkpoints/llava-v1.5-7b`

旧本地仓库中常见的相对写法：

- `experiments/checkpoints/llava-v1.5-7b`

## 8. POPE / MME 数据路径

### POPE

- 本地注释目录：`E:\VScode\VCD\experiments\data\POPE`
- 远程注释目录：`/root/autodl-tmp/code/VCD/experiments/data/POPE`
- 远程 COCO images：`/root/autodl-tmp/code/VCD/experiments/data/coco/val2014`
- 远程 GQA images：`/root/autodl-tmp/code/VCD/experiments/data/gqa/images`

### MME

- 远程 parquet dataset：`/root/autodl-tmp/code/VCD/experiments/data/MME_Benchmark`
- 远程 prepared images：`/root/autodl-tmp/code/VCD/experiments/output/mme/images`
- 远程 eval tool：`/root/autodl-tmp/code/VCD/experiments/tools/mme/eval_tool`

本地旧仓库当前没有完整 `MME_Benchmark` 数据目录。

## 9. 旧实验主要运行命令

只保留最主要的 provenance 入口：

- 远程环境激活命令
- POPE baseline / VCD 模板
- MME prepare 命令
- MME full VCD 推理命令
- MME format 命令

已整理到：

- `legacy_environment/run_commands.md`

## 10. 新项目可复用的信息

对新项目最值得复用的，不是旧 VCD 方法本身，而是这些经验：

1. 在 object hallucination 的 yes/no 任务里，early decision 信号可能非常强。
2. 强视觉对比干预不一定总是有益，full VCD 也会在一部分问题上伤人。
3. 只看 intervention magnitude 不够，还需要判断 intervention validity。
4. 旧 MME dominance 线最有用的位置是 “evidence + limitation”，不是 “现成 router”。

## 11. 已复制到新目录的文件列表

本次新生成并整理到新项目的文件：

- `project_context/legacy_handoff/legacy_handoff_for_new_project.md`
- `project_context/legacy_handoff/legacy_vcd_final_results/pope_final_results.md`
- `project_context/legacy_handoff/legacy_vcd_final_results/mme_final_results.md`
- `project_context/legacy_handoff/legacy_vcd_final_results/dominance_line_summary.md`
- `project_context/legacy_handoff/legacy_vcd_final_results/step0_observation_summary.md`
- `project_context/legacy_handoff/legacy_environment/remote_paths.md`
- `project_context/legacy_handoff/legacy_environment/model_dataset_paths.md`
- `project_context/legacy_handoff/legacy_environment/run_commands.md`
- `project_context/legacy_handoff/cleanup_notes.md`

## 12. 建议删除的文件列表

只给建议，不执行删除。

优先考虑清理的旧目录：

- `E:\VScode\VCD\tmp`
- `E:\VScode\VCD\experiments\cache`
- `E:\VScode\VCD\artifacts`
- `E:\VScode\VCD\.pytest_cache`
- `E:\VScode\VCD\tests\.tmp`
- `E:\VScode\VCD\**\__pycache__`

它们里边大多是：

- raw trace
- 临时 answer bank
- subset cache
- remote smoke 中间产物
- 大量 jsonl / json 中间结果

更细的清理建议见：

- `cleanup_notes.md`

## 13. 删除前注意事项

删除前建议先确认：

1. 是否还需要任何 raw outputs 做完全复原。
2. 是否还想保留 `generalization_compare` 下的 answer bank 作为人工抽查证据。
3. 是否还需要 `reports/mme_risk_router_feature_table.jsonl` 这类较大的 feature bank。
4. 旧仓库如果还想保留“可读可考古”状态，不要删：
   - `reports/`
   - `docs/`
   - `experiments/eval/`
   - `vcd_utils/`

## 14. 对新线程的建议

如果后续要开一个新的 Codex 线程继续新项目，不建议再把它引回旧 VCD 优化实验。

更推荐的新线程起手阅读顺序：

1. `project_context/legacy_handoff/legacy_handoff_for_new_project.md`
2. `project_context/legacy_handoff/legacy_vcd_final_results/step0_observation_summary.md`
3. `project_context/legacy_handoff/legacy_vcd_final_results/pope_final_results.md`
4. `project_context/legacy_handoff/legacy_vcd_final_results/mme_final_results.md`
5. `project_context/legacy_handoff/legacy_vcd_final_results/dominance_line_summary.md`

读完这些，就够理解旧方向留下来的真正有用部分了。
