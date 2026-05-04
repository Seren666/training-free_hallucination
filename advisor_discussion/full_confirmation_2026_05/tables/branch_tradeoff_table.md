# Branch Tradeoff Table

这张表不是为了再做一次“谁分最低”的排序，而是为了把三条 correction branch 的不同定位说清楚。

当前 branch policy 必须保持：

- `firstlogit_removal_top10` remains the metric-strong retained branch.
- `dual_phrase_replace_v1` remains the quality-preserving retained branch.
- `removal_top10_firstlogit_only_guard` remains the safer-removal retained diagnostic branch.
- Candidate A does not replace original removal or dual v1.

## 1. Summary Table

| Branch | Status | Primary role | CHAIRs / CHAIRi | Hallucinated reduction vs fixed | Correct loss vs fixed | Mention loss vs fixed | Grammar/coherence issue rate | Replacement count | Main strength | Main weakness | Keep status |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|
| `firstlogit_removal_top10` | retained | metric-strong branch | `0.1291 / 0.0413` | `-2093` | `-3499` | `-5592` | `0.0449` | `0` | raw CHAIR 最强，幻觉削减最多 | correct-object loss 大，局部删除损伤更明显 | keep |
| `removal_top10_firstlogit_only_guard` | retained diagnostic | safer-removal branch | `0.1356 / 0.0430` | `-1701` | `-1919` | `-3620` | `0.0109` | `0` | 保留 `81.27%` original removal 幻觉削减，同时多保住 `1580` correct mentions | raw score 仍弱于 original removal | keep |
| `dual_phrase_replace_v1` | retained | quality-preserving branch | `0.1403 / 0.0444` | `-1422` | `-1627` | `-3049` | lower than removal; current-scale review remains clearly cleaner | `623` | preservation 更健康，语言质量更自然 | replacement coverage 仍有限，raw gain 弱于 original removal | keep |

## 2. `firstlogit_removal_top10`

机制：

- 对 fixed `first_logit` caption 中的 object mentions 做 risk ranking；
- 取 `top10` risky mentions；
- 直接删除。

优点：

- 是最直接压低 `Hallucinated Objects` 的方式；
- 在 full adapted 和 near-official 上都给出最强 raw score；
- 很适合作为当前方法的 metric-strong branch。

风险：

- correct-object loss 最大；
- object mention loss 也最大；
- 局部删除带来的 grammar / coherence issue 更明显。

为什么保留：

- 因为它的 full score 最亮眼；
- 它清楚地展示了当前 verifier 在 aggressive action 下能把 raw CHAIR 压到多低。

## 3. `dual_phrase_replace_v1`

机制：

- 不是优先删，而是优先尝试局部 `phrase replacement`；
- 利用 regular caption 与 fixed `first_logit` caption 的差异，寻找更安全的局部表达；
- 找不到安全替换时，部分 case 才 fallback 到 removal。

优点：

- raw score 虽然稍弱，但 preservation / quality 更好；
- `Correct Objects` 损失更小；
- current-scale review 显示语言自然度明显好于 direct removal；
- 它确实存在真实 `phrase replacement`，不是“名义替换、实质删除”。

风险：

- true replacement coverage 仍然不高；
- 很多 case 仍然无法完成高质量替换；
- 所以 raw gain 还打不过 original removal。

为什么保留：

- 因为它更适合稳健叙事和质量导向；
- 它提供的是另一种重要 tradeoff，而不是原 removal 的弱化版。

## 4. `removal_top10_firstlogit_only_guard`

机制：

- 仍用同一个 `primary_risk_score top10` slice；
- 但只对 `first_logit_only` high-risk mentions 做 removal；
- 对 `common` mentions 直接 abstain / keep。

优点：

- raw score 虽然低于 original removal，但仍明显优于 fixed `first_logit`；
- 多保了 `1580` correct mentions；
- grammar/coherence heuristic issue rate 只有 `0.0109`，明显低于 original removal 的 `0.0449`；
- 说明 source-aware abstention 的确能显著减少误删。

风险：

- 它不再是最强 raw score；
- 仍然不是 preservation 最优，和 dual 相比 correct-object loss 仍略大。

为什么保留：

- 因为它回答了“如果更保守地做 removal，会不会明显更健康”这个问题；
- 它应该保留为 `safer-removal retained diagnostic branch`；
- 但它不替代 original removal，也不替代 dual。

## 5. 当前最稳妥的讲法

- `firstlogit_removal_top10`：
  - 最强 raw score，适合作为 metric-strong branch。
- `dual_phrase_replace_v1`：
  - raw 稍弱，但 preservation / quality 更好，适合作为 quality-preserving branch。
- `removal_top10_firstlogit_only_guard`：
  - raw 介于两者之间，但误删更少、grammar issue 更低，适合作为 safer-removal diagnostic branch。
