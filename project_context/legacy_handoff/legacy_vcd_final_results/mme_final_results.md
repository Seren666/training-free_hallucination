# Legacy VCD: MME Final Results

## 1. 这部分为什么值得保留

旧方向在 MME 上最重要的遗产，不是某个 router 本身，而是下面这件事已经被证明了：

> full VCD 不是全局无害的。

也就是说：

- 在 MME 上，full VCD 总体很强；
- 但它会伤害一部分 text / landmark / 细粒度识别类问题；
- 因此 MME 更适合被理解成 `harm avoidance` 问题，而不是简单的 “谁更值得上 full VCD”。

这条观察对新项目仍有参考价值：它提醒我们不要把 “更强的干预” 自动等同于 “更好的结果”。

## 2. 基线与最终可保留结果

### 2.1 基线

| Method | Perception | Cognition | Total | s/sample | 说明 |
|---|---:|---:|---:|---:|---|
| regular | 1183.679372 | 350.714286 | 1534.393657 | N/A | reproduced baseline |
| composite / coer2 | 1259.364546 | 386.071429 | 1645.435974 | 0.309650 | old composite reference |
| full VCD | 1289.429072 | 385.000000 | 1674.429072 | 0.277428 | MME 主基线 |

### 2.2 harm avoidance 最终应保留结果

| Method | Perception | Cognition | Total | s/sample | 相对 full VCD | 说明 |
|---|---:|---:|---:|---:|---:|---|
| harm oracle: text_translation + landmark fallback | 1290.679072 | 392.500000 | 1683.179072 | 0.284497 | +8.750000 | 方向证明，不是最终方法 |
| harm text-only router | 1293.035814 | 392.500000 | 1685.535814 | 0.286677 | +11.106743 | 当前 MME 质量最强点，但有模板依赖 |
| harm text_translation-only | 1289.429072 | 392.500000 | 1681.929072 | 0.279358 | +7.500000 | 当前 speed-quality Pareto 点 |

## 3. 最稳妥的结论

1. `full VCD` 比 `composite / coer2` 更强，也更快。
2. MME 上真正的问题不是 “VCD 到底有没有用”，而是 “VCD 在哪些问题上会伤人”。
3. `harm text-only router` 是当前质量最强点，但它依赖显式 question-text cues，存在模板依赖。
4. `harm text_translation-only` 是更保守、也更适合作为 Pareto 展示的点，因为它几乎贴着 full VCD 的速度。
5. 当前不应继续把时间花在 MME threshold / rule search 上。

## 4. 不应过强声称的内容

下面这些都不应该再作为 legacy 结论往外讲：

- 不要说 MME 已经有通用 harm router。
- 不要说 text-only harm router 是通用 classifier。
- 不要说 MME 速度已经全面超过 full VCD。
- 不要说这条线已经形成新的完整论文主线。

更稳妥的 legacy 表述是：

- MME 证明了 full VCD 不是全局无害的；
- text-only harm router 是一个质量很强、但模板依赖明显的点；
- text_translation-only 是一个很好的 speed-quality Pareto 点；
- 这些结果更适合作为经验背景，而不是新项目继续深挖的主线。

## 5. 为什么旧方向在 MME 上暂停

暂停不是因为完全没有结果，而是因为该拿到的结论已经拿到了：

- quality 结论已经比较清楚；
- speed 结论已经有边界；
- 再继续做小规则、小阈值、小回退策略，边际收益很低；
- 后面 dominance line 也表明：问题不只是“找一个阈值”，而是缺一个能区分 harmful vs beneficial intervention 的第二轴。

所以旧方向暂停，不是“失败”，而是“该收束为 legacy knowledge，而不是继续扩方法树”。

## 6. 对新项目还有什么参考价值

- 需要保留 “full VCD 并非全局无害” 这个认识。
- 需要保留 “text-sensitive / detail-sensitive 任务可能被强干预伤害” 这个经验。
- 但不建议把旧 MME router 直接搬进新项目继续发展。

## 7. 来源

- `E:\VScode\VCD\reports\mme_harm_avoid_end2end_validation.md`
- `E:\VScode\VCD\reports\mme_speed_comparison.md`
- `E:\VScode\VCD\reports\rad_vcd_current_questions_summary.md`
- `E:\VScode\training-free_hallucination\reports\self_understanding_note.md`
- `E:\VScode\training-free_hallucination\reports\advisor_stage_summary.md`
