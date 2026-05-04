# Full Confirmation Advisor Discussion Package

用途说明：

- 这个文件夹只用于和导师沟通当前方法、full data results、tradeoff、证据和下一步选择。
- 这不是论文初稿。
- 这不是最终投稿版本。
- 这不是 abstract / introduction。
- 这里的目标是把当前 full-confirmed object hallucination 结果讲清楚，便于导师判断主线是否稳定、三条 branch 如何摆放、下一步是否还要补外部 baseline 或方法优化。

文件说明：

- `method_and_results_brief.md`
  - 给导师看的主报告。
  - 总结方法背景、三条 branch、full result、tradeoff、证据和想请导师给的反馈。
- `tables/full_main_results.md`
  - full adapted 和 near-official 两张主结果表。
- `tables/branch_tradeoff_table.md`
  - 三条 correction branch 的定位、分数、preservation、grammar risk 和 keep status 对比表。
- `tables/signal_evidence_summary.md`
  - 当前最有用的 internal evidence / verifier 信号总结表。
- `appendix/data_sufficiency_review.md`
  - 先做的数据充分性审查，回答当前是否已经足够进入导师沟通。
- `appendix/external_baseline_status.md`
  - external baseline availability audit 的简版整理，说明为什么当前还没有 same-protocol VCD full comparison。
- `appendix/candidate_A_diagnostic_note.md`
  - Candidate A / `removal_top10_firstlogit_only_guard` 的完整诊断说明。

当前保留锚点：

- `firstlogit_removal_top10` remains the metric-strong retained branch.
- `dual_phrase_replace_v1` remains the quality-preserving retained branch.
- `removal_top10_firstlogit_only_guard` is retained as a safer-removal diagnostic branch.
- 当前不自动替换、不自动删除、不自动降级任何一条 branch。
