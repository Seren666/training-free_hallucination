# Full Main Results

## 1. 这张表在看什么

这份主表分成两部分：

- `Adapted Full Results`
  - 使用当前项目中稳定运行的 Python3 CHAIR evaluator；
  - 用于 full-scale `40504` image 批量评估；
  - 输出 `CHAIRs`、`CHAIRi`、`Hallucinated Objects`、`Correct Objects`、`Object Mentions`；
  - 是我们当前最主要、最完整的工程评估表。
- `Near-Official Full Results`
  - 使用 `chair_alignment` 中更接近官方 CHAIR 口径的评估流程；
  - 目的不是重新生成 caption，而是做 evaluator alignment check；
  - 重点看排序和趋势是否一致，验证 adapted evaluator 不是 artifact。

为什么需要两个 evaluator：

- adapted evaluator 方便 full-scale、工程稳定、可扩展；
- near-official evaluator 更接近官方 CHAIR 口径；
- 如果两者排序一致，结果可信度会明显更强。

术语说明见：

- [../appendix/terminology_glossary.md](../appendix/terminology_glossary.md)

## 2. 指标解释

- `CHAIRs`
  - caption-level hallucination rate。
  - 含义是：多少比例的 caption 至少包含一个 hallucinated object。
- `CHAIRi`
  - object-instance-level hallucination rate。
  - 含义是：全部 object mentions 中，有多少比例是 hallucinated mentions。
- `Hallucinated Objects`
  - 被 CHAIR 判定为图像中不存在、但 caption 提到的 object 数量。
- `Correct Objects`
  - 被 CHAIR 判定为图像中存在、且 caption 提到的 object 数量。
- `Object Mentions`
  - `Correct Objects + Hallucinated Objects`。
- `Δ vs fixed`
  - 相对于 fixed `first_logit` baseline 的变化。
  - `Hallucinated` 为负数表示 hallucination 减少；
  - `Correct` 和 `Mentions` 为负数表示损失了正确对象或总 object 提及。

## 3. Adapted Full Results

这张表是当前主工程表，覆盖 full `40504` image。

| Method | Role | CHAIRs | CHAIRi | Hallucinated Objects | Correct Objects | Object Mentions | Δ Hallucinated vs fixed | Δ Correct vs fixed | Δ Mentions vs fixed |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `regular` | original generation baseline | 0.2037 | 0.0655 | 11875 | 169393 | 181268 | +2266 | -8438 | -6172 |
| fixed `first_logit` | locked generation baseline / FLB-style early-anchor baseline | 0.1631 | 0.0513 | 9609 | 177831 | 187440 | 0 | 0 | 0 |
| `firstlogit_removal_top10` | metric-strong retained branch | 0.1291 | 0.0413 | 7516 | 174332 | 181848 | -2093 | -3499 | -5592 |
| `removal_top10_firstlogit_only_guard` | safer-removal retained diagnostic branch | 0.1356 | 0.0430 | 7908 | 175912 | 183820 | -1701 | -1919 | -3620 |
| `dual_phrase_replace_v1` | quality-preserving retained branch | 0.1403 | 0.0444 | 8187 | 176204 | 184391 | -1422 | -1627 | -3049 |

读表重点：

- `firstlogit_removal_top10` 仍然给出最强 raw CHAIR。
- `dual_phrase_replace_v1` 的 `Correct Objects` 损失最小，因此 preservation 更健康。
- `removal_top10_firstlogit_only_guard` 位于两者之间，说明 source-aware abstention 的确能换来更少误删。
- `regular -> fixed_first_logit` 本身已经说明 locked generation baseline 比原始 regular caption 更强。

## 4. Near-Official Full Results

这张表是 alignment check，不是新的 caption run。

| Method | CHAIRs | CHAIRi | Object Mentions | Hallucinated Objects | Ordering note |
|---|---:|---:|---:|---:|---|
| `regular` | 0.1997 | 0.0669 | 172330 | 11528 | weakest baseline |
| fixed `first_logit` | 0.1594 | 0.0524 | 178315 | 9337 | locked generation baseline |
| `firstlogit_removal_top10` | 0.1267 | 0.0424 | 172980 | 7335 | best raw score |
| `removal_top10_firstlogit_only_guard` | 0.1329 | 0.0441 | 174848 | 7712 | safer-removal diagnostic branch between original removal and dual |
| `dual_phrase_replace_v1` | 0.1374 | 0.0455 | 175394 | 7984 | preservation / quality branch |

一致性说明：

- near-official 与 adapted evaluator 排序一致。
- 方向一致，数值也接近。
- 这增强了当前 full result 的可信度，因为它说明结果不是某个单一 evaluator 的工程偏差。

## 5. 如何解读这两张表

如果只看 `CHAIRs / CHAIRi`：

- `firstlogit_removal_top10` 最强；
- `removal_top10_firstlogit_only_guard` 第二；
- `dual_phrase_replace_v1` 第三。

但如果把 `Hallucinated / Correct / Mentions` 一起看：

- original removal 是最激进、最强分的方案；
- dual 是更 preservation-friendly、质量更稳的方案；
- Candidate A 是中间 tradeoff，放弃部分 raw gain，换来更少 correct-object loss 和更低 grammar risk。

因此这张主表的核心价值，不只是“谁分最低”，而是让导师能同时看到：

- hallucination 降了多少；
- correct object 牺牲了多少；
- object mention 总量是否也在一起下降。
