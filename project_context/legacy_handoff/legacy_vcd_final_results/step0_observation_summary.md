# Legacy VCD: Step0 / Early Decision Observations

## 1. 这份小结为什么保留

旧 VCD 方向虽然整体暂停了，但其中“step0 / early decision 到底能解释多少收益”这个观察，对新项目仍然很有启发。

如果后续新项目要做 first-logit / early-anchor，这份观察可以当动机背景，而不是当要直接复用的方法。

## 2. 在 POPE 上看到的事情

POPE 是非常典型的 yes/no object hallucination 任务。

在这类任务里，旧方向最终得到的核心经验是：

- full VCD 的大多数有效收益，集中在最早的 answer decision；
- 更具体地说，就是 step0 / answer boundary；
- 把 full-depth 干预压缩成 step0 VCD，再加一个极稀疏的 disagreement micro-rescue，就能吃到大多数收益。

这也是为什么 POPE 最终冻结为 `SCMR-VCD`。

它不是在说 “所有任务都只看 step0”，而是在说：

> 对 object hallucination 的 yes/no 边界问题，早期决策位很关键。

## 3. 在 MME 上看到的事情

MME 给出的反例同样重要。

最开始也试过把 POPE 的那套直觉搬过去：

- 先看 step0；
- 先看 answer-aligned binary proxy；
- 再想办法用这个信号决定要不要调整 VCD。

结果不行。

原因很简单：

- MME 不是单纯的 yes/no object boundary 任务；
- 它混合了文本读取、翻译、细粒度识别、landmark、celebrity、scene、count 等不同能力；
- 所以单个 step0 binary proxy 不足以讲清楚 VCD-harm。

换句话说：

> step0 在 POPE 上像主战场，但在 MME 上只够当一个很弱的起点。

## 4. 对新项目最值得带走的两句话

### 4.1 正面经验

在 object hallucination / yes-no 边界任务里，early decision 确实可能携带大部分关键风险信息。

### 4.2 反面经验

不要把这条经验直接外推到更复杂任务。

如果任务不再是单纯的 answer-boundary 决策，只靠 step0 / binary proxy 往往是不够的。

## 5. 对新项目的具体启发

如果新项目后续考虑 first-logit / early-anchor：

- 可以把 POPE / SCMR 经验作为正动机；
- 也要把 MME 的失败经验一起带上：需要提前准备“为什么这个早期信号不会只在简单 yes/no 任务上有效”的论证。

## 6. 相关旧文件

- `E:\VScode\VCD\reports\frozen_branch_status.md`
- `E:\VScode\VCD\reports\mme_self_diagnostic_signal_audit.md`
- `E:\VScode\VCD\vcd_utils\cd_step_selector.py`
- `E:\VScode\VCD\experiments\eval\analyze_shortcircuit_micro_rescue.py`
