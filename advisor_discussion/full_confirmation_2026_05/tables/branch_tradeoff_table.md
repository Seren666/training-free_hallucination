# Branch Tradeoff Table

| Branch | Status | Primary role | CHAIRs / CHAIRi | Hallucinated reduction vs fixed | Correct loss vs fixed | Mention loss vs fixed | Grammar/coherence issue rate | Replacement count | Main strength | Main weakness | Keep status |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|
| `firstlogit_removal_top10` | retained | metric-strong branch | `0.1291 / 0.0413` | `-2093` | `-3499` | `-5592` | `0.0449` | `0` | raw CHAIR 最强，幻觉削减最多 | correct-object loss 大，局部删除损伤更明显 | keep |
| `removal_top10_firstlogit_only_guard` | retained diagnostic | safer-removal branch | `0.1356 / 0.0430` | `-1701` | `-1919` | `-3620` | `0.0109` | `0` | 保留 `81.27%` original removal 幻觉削减，同时多保住 `1580` correct mentions | raw score 仍弱于 original removal | keep |
| `dual_phrase_replace_v1` | retained | quality-preserving branch | `0.1403 / 0.0444` | `-1422` | `-1627` | `-3049` | lower than removal; current-scale review remains clearly cleaner | `623` | preservation 更健康，语言质量更自然 | replacement coverage 仍有限，raw gain 弱于 original removal | keep |

当前 branch policy：

- `firstlogit_removal_top10` remains the metric-strong retained branch.
- `dual_phrase_replace_v1` remains the quality-preserving retained branch.
- `removal_top10_firstlogit_only_guard` remains the safer-removal retained diagnostic branch.
- Candidate A does not replace original removal or dual v1.
- Candidate A should not be discarded, because it reduces false edits / correct-object loss while keeping most of the original removal gain.
