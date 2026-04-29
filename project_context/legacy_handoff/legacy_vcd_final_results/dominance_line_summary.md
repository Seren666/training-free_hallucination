# Legacy VCD: MME Dominance Line Summary

## 1. 这条线为什么值得保留

MME dominance 线不是因为它已经做成了正式 router，而是因为它留下了一个很有价值的研究判断：

> VCD 的一部分 harm risk，确实会在推理轨迹里留下可观察的 self-diagnostic 痕迹。

这对后续任何想做 “early signal / first-logit / early-anchor” 的新项目，都是有参考价值的。

## 2. 这条线做了什么

已经完成的阶段：

1. step0 binary self-diagnostic audit
2. full-vocab early trace audit
3. single-signal p90 offline stitching
4. full-bank fixed single-signal review
5. dominance-aware damping feasibility
6. local skip-VCD feasibility

核心单信号：

- `max_contrastive_dominance_ratio`

## 3. 正面结果

### 3.1 step0 binary proxy 给了方向，但不够

- strongest step0 signal：`dominance_ratio`
- held-out ROC-AUC：`0.859550`
- 但最优 offline router 最后退化成 no-op full VCD

结论：

- step0 binary proxy 不足以形成 MME harm router
- MME 不是 POPE，不能只靠 yes/no answer-boundary 信号

### 3.2 full-vocab early trace 把信号拉出来了

remote trace collection 最终完成：

- natural subset：`400 / 400`
- enriched subset：`169 / 169`

最强信号：

- `max_contrastive_dominance_ratio`

关键指标：

- natural ROC-AUC：`0.818740`
- natural PR-AUC：`0.251662`
- enriched ROC-AUC：`0.811550`
- enriched PR-AUC：`0.467408`

这说明：

- 它不是纯噪声；
- 它比 step0 binary proxy 更贴近 VCD 机制；
- 它确实能捕捉一部分 VCD harmful intervention。

### 3.3 subset 上 single-signal stitching 曾经出现正收益

单信号 p90 offline stitching：

- natural threshold：`14.874778`
- natural delta vs full VCD：`+10.797517`
- natural fallback rate：`0.102500`
- natural harm capture：`0.357143`
- natural benefit false fallback：`0.170732`

- enriched threshold：`16.632816`
- enriched delta vs full VCD：`+4.433879`
- enriched fallback rate：`0.106509`
- enriched harm capture：`0.285714`
- enriched benefit false fallback：`0.146341`

这个结果的意义是：

- high dominance 和 VCD harm 确实有关联；
- 这条线一度从纯 audit 走到了 promising candidate。

## 4. 为什么它最后没有成为稳健 router

full-bank 复核后，边界很明确：

- full-bank p90 threshold：`11.179335`
- full-bank p90 router score：`1674.348840`
- full-bank delta vs full VCD：`-0.080232`
- full-bank fallback rate：`0.100253`
- full-bank harm capture：`0.464286`
- full-bank benefit false fallback：`0.243902`

更保守的 natural-calibrated threshold：

- threshold：`14.874778`
- delta vs full VCD：`+0.669768`

因此最后结论是：

- subset positive result 存在；
- 但 full-bank 不稳定；
- 单信号 dominance 还不足以成为稳健 runtime router。

最核心的原因不是 “没有信号”，而是：

> high dominance 同时包含 harmful over-correction 和 beneficial visual correction。

也就是说，dominance 说明的是 intervention magnitude，不是 intervention validity。

## 5. action space 的负结果

### 5.1 sample-level composite fallback

- 有修复能力
- 但 benefit false fallback 偏高

### 5.2 simple damping

- 比 sample fallback 更少误伤 benefit
- 但对 harmful over-correction 改动太少

代理层面的代表数值：

- full-bank p90 下，`alpha_damped = 0.5` 仅改变 `18 / 238` 个 proxy top1，其中 harm 改变 `2 / 13`
- natural-calibrated threshold 下，两种 damping 都只改变 `5 / 166` 个 proxy top1，其中 harm 改变 `1 / 11`

### 5.3 local skip-VCD

高 dominance 子集：

- sample count：`166`
- threshold：`14.874778`
- subset full VCD：`1423.515826`
- local skip-VCD：`1071.316908`
- delta：`-352.198919`
- trigger rate：`141 / 166 = 84.94%`
- harm repair：`0 / 11`

结论很明确：

- local skip-VCD 太粗暴
- high dominance 不等于该 step 应切回 clean path

## 6. 最终应该怎么记这条线

最稳妥的 legacy 结论是：

1. dominance line 支持 RAD-VCD 的统一叙事，作为 self-diagnostic audit evidence。
2. 它说明 VCD harm risk 可以从推理轨迹中部分观察。
3. 但它没有形成稳健的 MME runtime router。
4. 当前不建议继续在旧 VCD 仓库里沿这条线做 intervention、threshold search 或 end-to-end 扩展。

## 7. 对新项目还有什么参考价值

- 可以把它当作 “early self-diagnostic signal 确实存在” 的证据。
- 也要同时带走它的限制：只看干预有多强不够，还需要第二轴判断干预是否有效。
- 这对后续 first-logit / early-anchor 研究，是一个很有用的背景提醒。

## 8. 来源

- `E:\VScode\VCD\reports\mme_self_diagnostic_signal_audit.md`
- `E:\VScode\VCD\reports\mme_fullvocab_early_trace_audit.md`
- `E:\VScode\VCD\reports\mme_fullvocab_selfdiag_candidates.md`
- `E:\VScode\VCD\reports\mme_dominance_damping_feasibility.md`
- `E:\VScode\VCD\reports\mme_dominance_local_action_feasibility.md`
- `E:\VScode\VCD\reports\mme_dominance_line_summary.md`
