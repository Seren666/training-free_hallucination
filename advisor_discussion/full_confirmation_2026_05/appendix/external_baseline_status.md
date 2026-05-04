# External Baseline Status

当前 external baseline audit 的结论是：

- 目前没有找到 `VCD / OPERA / RAD-VCD / RITUAL / old CD` 的 full COCO-CHAIR caption json。
- 当前 `VCD` 仓库里的历史产物主要是 POPE yes/no answer files 和 POPE metric text files。
- 这些文件不能和当前 full correction 结果做 same-protocol 的 COCO-CHAIR caption comparison。

更具体地说：

- `training_free_hallucination_probe/outputs/coco_chair/` 下没有外部 baseline 的 full caption payload。
- `VCD/experiments/output/pope/answers` 下找到的是大量 yes/no jsonl，不是 open-ended caption payload。
- `VCD/experiments/output/pope/scores` 下找到的是 POPE precision/recall/F1 一类文本结果，不是 CHAIR metrics。

因此当前能直接同协议比较的 full baseline 只有：

- `regular`
- fixed `first_logit`
- 本项目内部三条 correction branches

关于 `FLB` 的理解：

- 如果这里把 `FLB` 理解为当前项目已经锁定的 fixed `first_logit` baseline，那么它已经有 full adapted 和 near-official 结果。
- 但如果指外部方法族里的另一个独立 full caption baseline，那么当前并没有对应 payload。

当前建议：

- 不把 external baseline 缺失当作当前 object-hallucination full confirmation 的 blocking gap。
- 但要把它明确写成导师沟通时的一个 caveat。
- 真正的 `VCD` full caption baseline 需要单独批准，因为它会是新的 full caption-generation experiment，成本高，不应现在自动启动。
