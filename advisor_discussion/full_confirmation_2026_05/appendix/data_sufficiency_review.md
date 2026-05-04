# Data Sufficiency Review

## Review Scope

- 已阅读本地方法状态文档：
  - `project_context/baseline_notes/current_core_results_table.md`
  - `project_context/baseline_notes/correction_full_confirmation_readiness.md`
  - `project_context/planning/next_research_steps.md`
  - `project_context/baseline_notes/object_hallucination_research_notes.md`
- 已对照远端 full result / quality / audit 文档：
  - `results/full_correction_metrics.md`
  - `results/full_correction_near_official_alignment_metrics.md`
  - `results/full_correction_risk_benefit_curve.md`
  - `results/firstlogit_removal_top10_quality_review_current_scale.md`
  - `results/dual_phrase_replace_v1_quality_review_current_scale.md`
  - `results/removal_top10_firstlogit_only_guard_full_diagnostic_report.md`
  - `results/removal_top10_firstlogit_only_guard_tradeoff.md`
  - `results/removal_top10_firstlogit_only_guard_near_official_metrics.md`
  - `results/external_baseline_availability_audit.md`
  - `results/full_correction_improvement_opportunity_report.md`

## Question-by-Question Review

1. 当前 full results 是否足以和导师沟通？

- 是。
- 当前已经有 `40504` image full-scale adapted 结果、near-official 一致性、branch tradeoff、quality review、Candidate A diagnostic 和 external baseline status。

2. main table 是否完整？

- 是。
- 当前已经能构成一张完整主表：
  - `regular`
  - fixed `first_logit`
  - `firstlogit_removal_top10`
  - `removal_top10_firstlogit_only_guard`
  - `dual_phrase_replace_v1`

3. adapted evaluator 和 near-official evaluator 是否一致？

- 是。
- 顺序一致，方向一致，数值也接近。
- 当前没有“只在 adapted evaluator 上成立”的迹象。

4. 是否已经证明不只是 5000 subset 效果？

- 是。
- 当前核心结果已经从 `5000` expanded 扩展到 full `40504` image confirmation。
- 因此不再只是 subset signal。

5. 是否已经检查“少说 object”问题？

- 是。
- 当前所有 full main branches 都记录了：
  - `Object Mentions`
  - `Correct Object Count`
  - `Delta vs fixed`
- 所以“分数下降是不是只是少说 object”已经被显式检查。

6. correct-object loss 是否已被记录？

- 是。
- 三条 branch 都有 `Correct Object Count` 和 `Δ Correct vs fixed`。
- `firstlogit_removal_top10`、`dual_phrase_replace_v1`、`removal_top10_firstlogit_only_guard` 都已有 preservation 侧记录。

7. quality review 是否支持 branch tradeoff？

- 是。
- original removal 已有 current-scale quality review。
- dual 已有 current-scale quality review。
- Candidate A 已有 full diagnostic report 和 quality spotcheck。
- 因此“raw score / preservation / grammar damage”的 tradeoff 已经有证据支撑。

8. 三条 branch 的定位是否清楚？

- 是。
- 当前定位已经清楚：
  - `firstlogit_removal_top10`: metric-strong retained branch
  - `dual_phrase_replace_v1`: quality-preserving retained branch
  - `removal_top10_firstlogit_only_guard`: safer-removal retained diagnostic branch

9. Candidate A 是否应进入导师沟通材料？

- 是。
- 它不替代 retained branches，但它明确回答了“source-aware abstention 能否减少误删”这个关键问题。
- 它有 full adapted、near-official、quality、tradeoff 四类证据，因此值得进导师沟通包。

10. external baseline 缺失是否是 blocking gap？

- 否。
- 这是重要 caveat，但不是 blocking gap。
- 当前已经足够和导师沟通：
  - internal baseline 是否成立
  - correction 是否在 full scale 有效
  - 三条 branch 的 tradeoff 如何摆放

11. 是否需要在和导师沟通前再跑 VCD full？

- 不需要。
- 这会是一个新的 full caption-generation experiment，成本高，而且当前并不是进入导师沟通的必要前提。

12. 当前最主要 caveats 是什么？

- 没有 same-protocol 的 external `VCD / OPERA / RAD-VCD / RITUAL` full COCO-CHAIR caption baseline。
- `dual_phrase_replace_v1` replacement coverage 仍有限。
- `firstlogit_removal_top10` 仍有较明显 correct-object loss 和 grammar damage。
- Candidate A 是 diagnostic safer-removal branch，不是替代 retained main branches 的新结论。
- 当前指标聚焦 object hallucination / COCO-CHAIR，不覆盖全部 hallucination 类型。

13. 是否存在必须立刻补的数据？

- 没有发现必须在导师沟通前立刻补的数据。
- 当前缺的是“更完整的 external baseline comparison”，但这属于后续可选扩展，不是当前 blocking item。

## Conclusion

- `ready_for_advisor_discussion: yes`
- `blocking_gaps:`
  - none that block advisor discussion
- `recommended_next_before_advisor:`
  - 把 full adapted、near-official、three-branch tradeoff 和 external baseline caveat 整理成一套简洁沟通包
  - 明确三条 branch 的定位，不自动替换任何 retained branch
  - 在主报告中把 external baseline 缺失写成 caveat，而不是方法失败
