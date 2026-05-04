# Candidate A Diagnostic Note

## Rule

- method name: `removal_top10_firstlogit_only_guard`
- rule:
  - 从当前 full high-risk table 出发
  - 使用同一个 `primary_risk_score top10` operating slice
  - 只对 `source_group == first_logit_only` 的 risky mentions 做 removal
  - `common` mentions 一律 abstain / keep
- 不改 risk score
- 不改 threshold
- 不使用 GT / CHAIR label 做 runtime decision

## Full Adapted Metrics

- `CHAIRs=0.1356`
- `CHAIRi=0.0430`
- `hallucinated=7908`
- `correct=175912`
- `mentions=183820`

## Full Near-Official Metrics

- `CHAIRs=0.1329`
- `CHAIRi=0.0441`
- `hallucinated=7712`
- `mentions=174848`

## Comparison Vs fixed `first_logit`

- hallucinated `-1701`
- correct `-1919`
- mentions `-3620`

结论：

- Candidate A 明显优于 fixed `first_logit`。
- 它不是“无效的保守版”，而是保留了大部分 correction gain。

## Comparison Vs original `firstlogit_removal_top10`

- hallucinated `+392`
- correct `+1580`
- mentions `+1972`
- retained hallucination reduction ratio: `81.27%`

结论：

- Candidate A raw score 弱于 original removal。
- 但它显著减少了 correct-object loss。
- 它因此适合作为 safer-removal diagnostic branch。

## Comparison Vs `dual_phrase_replace_v1`

- Candidate A adapted `CHAIRs / CHAIRi`: `0.1356 / 0.0430`
- dual adapted `CHAIRs / CHAIRi`: `0.1403 / 0.0444`
- Candidate A correct count: `175912`
- dual correct count: `176204`

结论：

- Candidate A raw score 略强于 dual。
- 但 preservation 仍略弱于 dual。
- 所以它不替代 dual 的 quality-preserving role。

## Quality Result

- Candidate A grammar/coherence heuristic issue rate: `0.0109`
- original removal grammar/coherence heuristic issue rate: `0.0449`
- Candidate A common edit count: `0`
- Candidate A first-logit-only edit count: `3599`

这说明：

- 它确实避免了最糟糕的 `common` mention 删除错误。
- 剩余 harmful edits 主要是 `first_logit_only` false positives。

## Why It Is Retained

- 它回答了一个很实际的问题：
  - 如果只在 source-exclusive risky mentions 上 action，是否能减少误删？
- full diagnostic 的答案是肯定的。
- 因此它值得保留为 safer-removal retained diagnostic branch。

## Why It Should Not Be Discarded

- 它不是最好 raw score，但它显著改善了 removal 的误删问题。
- 它是当前三条 branch 中唯一明确回答“如何更保守地做 removal”这一问题的 full diagnostic result。

## Why It Does Not Replace Original Removal Or Dual

- 它不替代 `firstlogit_removal_top10`，因为 original removal 仍是 raw metric 最强分支。
- 它不替代 `dual_phrase_replace_v1`，因为 dual 仍是 preservation / quality 更好的分支。
- 正确定位应是：
  - `firstlogit_removal_top10` remains the metric-strong retained branch
  - `dual_phrase_replace_v1` remains the quality-preserving retained branch
  - `removal_top10_firstlogit_only_guard` remains the safer-removal retained diagnostic branch
