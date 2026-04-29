# Legacy VCD Cleanup Notes

本文件只给删除建议，不执行删除。

旧目录：

- `E:\VScode\VCD`

新整理目录：

- `E:\VScode\training-free_hallucination\project_context\legacy_handoff`

## A. 建议保留并已复制的文件

这些文件已经整理到新项目目录，可作为新线程优先阅读入口：

- `project_context/legacy_handoff/legacy_handoff_for_new_project.md`
- `project_context/legacy_handoff/legacy_vcd_final_results/pope_final_results.md`
- `project_context/legacy_handoff/legacy_vcd_final_results/mme_final_results.md`
- `project_context/legacy_handoff/legacy_vcd_final_results/dominance_line_summary.md`
- `project_context/legacy_handoff/legacy_vcd_final_results/step0_observation_summary.md`
- `project_context/legacy_handoff/legacy_environment/remote_paths.md`
- `project_context/legacy_handoff/legacy_environment/model_dataset_paths.md`
- `project_context/legacy_handoff/legacy_environment/run_commands.md`
- `project_context/legacy_handoff/cleanup_notes.md`

## B. 建议不复制，但暂时可留在旧目录的文件

这些文件体积不大，且保留 provenance 价值，建议暂时留在旧仓库，不必删除得太急：

- `E:\VScode\VCD\reports\frozen_branch_status.md`
- `E:\VScode\VCD\reports\mme_harm_avoid_end2end_validation.md`
- `E:\VScode\VCD\reports\mme_speed_comparison.md`
- `E:\VScode\VCD\reports\rad_vcd_current_questions_summary.md`
- `E:\VScode\VCD\reports\mme_self_diagnostic_signal_audit.md`
- `E:\VScode\VCD\reports\mme_fullvocab_early_trace_audit.md`
- `E:\VScode\VCD\reports\mme_fullvocab_selfdiag_candidates.md`
- `E:\VScode\VCD\reports\mme_dominance_damping_feasibility.md`
- `E:\VScode\VCD\reports\mme_dominance_local_action_feasibility.md`
- `E:\VScode\VCD\reports\mme_dominance_line_summary.md`
- `E:\VScode\VCD\docs\baseline_reproduction_log.md`
- `E:\VScode\VCD\docs\baseline_comparison_tables.md`
- `E:\VScode\VCD\docs\README.md`
- `E:\VScode\VCD\docs\codex_handoff_docs\codex_handoff_unified_optimized.md`
- `E:\VScode\VCD\experiments\eval\object_hallucination_vqa_llava.py`
- `E:\VScode\VCD\experiments\eval\eval_pope.py`
- `E:\VScode\VCD\experiments\eval\mme_prepare.py`
- `E:\VScode\VCD\experiments\eval\mme_format_results.py`
- `E:\VScode\VCD\vcd_utils\cd_step_selector.py`
- `E:\VScode\VCD\vcd_utils\vcd_sample.py`

## C. 建议删除的文件或目录

这些大多是过程性 cache、trace、raw output、临时 answer bank、remote smoke 中间产物。当前新项目不再以旧 VCD 优化为主线，可优先考虑进入待删清单。

### 建议优先删除的目录

- `E:\VScode\VCD\tmp\coco_adv_vit1`
- `E:\VScode\VCD\tmp\generalization_compare`
- `E:\VScode\VCD\tmp\mme_harm_validate`
- `E:\VScode\VCD\tmp\remote_runs`
- `E:\VScode\VCD\tmp\remote_smoke_analysis`
- `E:\VScode\VCD\tmp\remote_smoke_compare`
- `E:\VScode\VCD\tmp\speed1000ctrl`
- `E:\VScode\VCD\tmp\timing_sq0427`
- `E:\VScode\VCD\artifacts\incoming`
- `E:\VScode\VCD\artifacts\anchor_analysis`
- `E:\VScode\VCD\.pytest_cache`
- `E:\VScode\VCD\tests\.tmp`
- `E:\VScode\VCD\**\__pycache__`

### 建议优先删除的大文件类型

- `experiments/cache/*.trace.jsonl`
- `experiments/cache/*fullbank*.jsonl`
- `experiments/cache/*subset*.jsonl`
- `experiments/cache/*.answers.jsonl`
- `tmp/**/*.jsonl`
- `artifacts/**/*.jsonl`
- `artifacts/**/*.json`
- `reports/mme_risk_router_feature_table.jsonl`（如果只需要最终结论，不再需要 feature bank）

## D. 可能占用大量空间的目录

本次粗略盘点到的空间占用：

- `E:\VScode\VCD\tmp`：约 `1070.95 MB`
- `E:\VScode\VCD\experiments\cache`：约 `297.41 MB`
- `E:\VScode\VCD\artifacts`：约 `251.68 MB`
- `E:\VScode\VCD\reports`：约 `6.07 MB`

最重的单文件包括：

- `experiments/cache/mme_selfdiag_fullvocab_trace_fullbank.jsonl`：约 `202 MB`
- `tmp/timing_sq0427/*.jsonl`：约 `96 MB` 到 `100 MB`
- `tmp/remote_smoke_compare/*.trace.jsonl`：约 `99 MB`
- `experiments/cache/mme_selfdiag_fullvocab_trace_subset.jsonl`：约 `34 MB`
- `experiments/cache/mme_selfdiag_fullvocab_trace_subset_enriched.jsonl`：约 `14 MB`
- `experiments/cache/mme_dominance_local_action_*trace.jsonl`：约 `14 MB` 到 `15 MB`

## E. 删除前需要用户确认的内容

在真正删除旧目录内容前，建议先确认这几件事：

1. 是否还需要任何 raw answer bank / trace 用于“完全复原旧结论”。
2. 是否还想保留 `generalization_compare` 里的 answer files 作为人工抽查材料。
3. 是否还需要 `mme_risk_router_feature_table.jsonl` 做更细的 post-hoc 审计。
4. 是否要保留旧代码入口作为纯参考仓库；如果要，删除时应只删 `tmp / artifacts / cache`，不要删 `docs / reports / experiments/eval / vcd_utils`。
5. 旧仓库如果仍在 git 管理下，不要在未确认前做大规模清理，以免把未来还要查的 provenance 一起抹掉。

## 建议的实际清理顺序

如果用户后续决定真删，建议顺序是：

1. 先删 `tmp/`
2. 再删 `experiments/cache/` 中的大型 trace / answers / subset artifacts
3. 再删 `artifacts/`
4. 最后视需要再处理 `.pytest_cache / tests/.tmp / __pycache__`

不要先删：

- `reports/`
- `docs/`
- `experiments/eval/`
- `vcd_utils/`

除非确认旧仓库完全不再需要考古。
