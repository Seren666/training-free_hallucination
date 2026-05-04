# Full Main Results

## Adapted Full Results

| Method | Role | CHAIRs | CHAIRi | Hallucinated Objects | Correct Objects | Object Mentions | Δ Hallucinated vs fixed | Δ Correct vs fixed | Δ Mentions vs fixed |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `regular` | open-ended regular baseline | 0.2037 | 0.0655 | 11875 | 169393 | 181268 | +2266 | -8438 | -6172 |
| fixed `first_logit` | locked generation baseline | 0.1631 | 0.0513 | 9609 | 177831 | 187440 | 0 | 0 | 0 |
| `firstlogit_removal_top10` | metric-strong retained branch | 0.1291 | 0.0413 | 7516 | 174332 | 181848 | -2093 | -3499 | -5592 |
| `removal_top10_firstlogit_only_guard` | safer-removal retained diagnostic branch | 0.1356 | 0.0430 | 7908 | 175912 | 183820 | -1701 | -1919 | -3620 |
| `dual_phrase_replace_v1` | quality-preserving retained branch | 0.1403 | 0.0444 | 8187 | 176204 | 184391 | -1422 | -1627 | -3049 |

读表说明：

- `firstlogit_removal_top10` 仍然是 raw CHAIR 最强分支。
- `dual_phrase_replace_v1` correct-object preservation 更好。
- `removal_top10_firstlogit_only_guard` 介于两者之间，是 safer-removal diagnostic branch。

## Near-Official Full Results

| Method | CHAIRs | CHAIRi | Object Mentions | Hallucinated Objects | Ordering note |
|---|---:|---:|---:|---:|---|
| `regular` | 0.1997 | 0.0669 | 172330 | 11528 | weakest baseline |
| fixed `first_logit` | 0.1594 | 0.0524 | 178315 | 9337 | locked generation baseline |
| `firstlogit_removal_top10` | 0.1267 | 0.0424 | 172980 | 7335 | best raw score |
| `removal_top10_firstlogit_only_guard` | 0.1329 | 0.0441 | 174848 | 7712 | safer-removal diagnostic branch between original removal and dual |
| `dual_phrase_replace_v1` | 0.1374 | 0.0455 | 175394 | 7984 | preservation / quality branch |

一致性说明：

- near-official 与 adapted evaluator 排序一致。
- 因此当前 full result 不是某一个 evaluator 的偶然产物。
