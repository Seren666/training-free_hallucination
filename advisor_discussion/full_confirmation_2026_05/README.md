# Full Confirmation Advisor Discussion Package

用途说明：

- 这个文件夹只用于和导师沟通当前方法、full data results、tradeoff、证据、风险和下一步选择。
- 这不是论文初稿。
- 这不是最终投稿版本。
- 这不是 abstract / introduction。
- 这里的目标是把当前 `LLaVA-1.5-7B + COCO-CHAIR object hallucination` 结果讲清楚，便于讨论主线是否稳定、三条 branch 如何摆放、是否还需要补 external baseline，以及下一步先做写作还是继续补数据。

推荐阅读顺序：

1. `method_and_results_brief.md`
2. `tables/full_main_results.md`
3. `tables/branch_tradeoff_table.md`
4. `tables/signal_evidence_summary.md`
5. `appendix/data_sufficiency_review.md`
6. `appendix/reference_literature_summary.md`
7. `appendix/terminology_glossary.md`

文件说明：

- `method_and_results_brief.md`
  - 给导师看的主报告。
  - 先讲我们最终发现哪些 internal signals 真正有用，再解释方法主线、三条 branch 机制、full result 和希望导师给的反馈。
- `tables/full_main_results.md`
  - full adapted evaluator 和 near-official evaluator 两张主结果表。
  - 也解释为什么需要两个 evaluator，以及每个指标代表什么。
- `tables/branch_tradeoff_table.md`
  - 三条 correction branches 的定位、分数、preservation、grammar risk 和 keep status 对比。
  - 除了表格，也补了每条 branch 的中文解释。
- `tables/signal_evidence_summary.md`
  - 当前最有用的 internal evidence / verifier 信号总结。
  - 同时保留了弱信号和负面结论，便于导师理解方法是怎么收缩到当前形态的。
- `appendix/data_sufficiency_review.md`
  - 数据充分性审查。
  - 结论是当前 full result 已经足够进入导师沟通，不需要先补新的 full experiment。
- `appendix/external_baseline_status.md`
  - external baseline availability audit 的简版整理。
  - 说明为什么当前还没有 same-protocol `VCD / OPERA / RAD-VCD / RITUAL` full caption comparison。
- `appendix/candidate_A_diagnostic_note.md`
  - Candidate A / `removal_top10_firstlogit_only_guard` 的完整诊断说明。
  - 重点是解释它为什么值得保留，但为什么不替代已有 retained branches。
- `appendix/reference_literature_summary.md`
  - 当前项目阅读过、借鉴过、排除过、采用过的相关论文和内部参考的简表。
  - 这不是完整 related work，而是导师沟通版“方法谱系说明”。
- `appendix/terminology_glossary.md`
  - 项目里的关键术语、内部命名和评估指标解释。
  - 适合作为配套词汇表使用，避免导师必须追完整实验历史。

当前保留锚点：

- `firstlogit_removal_top10` remains the metric-strong retained branch.
- `dual_phrase_replace_v1` remains the quality-preserving retained branch.
- `removal_top10_firstlogit_only_guard` is retained as a safer-removal diagnostic branch.
- 当前不自动替换、不自动删除、不自动降级任何一条 branch。
