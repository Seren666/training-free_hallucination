# Signal Evidence Summary

这张表的目的不是只列“最后成功的信号”，而是把当前方法为什么会收缩到 `weighted training-free mention-level verifier` 这条线讲清楚。

一个重要结论是：

- 真正有用的是 `mention-local internal evidence`；
- 而不是粗粒度 image-level scalar；
- 也不是某个单独的简单 attention statistic。

## 1. Core Signals

| Signal / Evidence Item | 中文解释 | 当前作用 | 当前判断 |
|---|---|---|---|
| `middle visual verification` | 中间层里，这个 object mention 是否已经获得视觉证据支持 | main verifier signal | strongest family 之一 |
| `middle-to-late attention evolution` | 从 middle 到 late，object token 对图像区域的关注是否正常演化 | main verifier signal | strongest family 之一 |
| `anchor-middle mismatch` | early anchor / `first_logit` 支持是否与 middle-layer verification 不一致 | main verifier signal | strongest family 之一 |
| `weighted training-free verifier` | 将多个 risk / rescue evidence families 进行手工加权整合的无训练 verifier | main evidence source | 当前主 evidence surface |
| `source-exclusive first_logit_only risk` | 只出现在 fixed `first_logit` caption 中、regular 中没有的 mention，更容易是风险 mention | main verifier signal + routing clue | full anatomy 支持其重要性 |

## 2. Supporting Signals

| Signal / Evidence Item | 中文解释 | 当前作用 | 当前判断 |
|---|---|---|---|
| `head agreement / head consistency` | 多个 attention heads 是否对同一对象形成相对一致支持 | supporting evidence | 单独不够强，但有辅助价值 |
| `layer consistency` | 相邻层或层组之间，对同一 mention 的支持是否稳定 | supporting evidence | 有助于过滤偶然尖峰 |
| `visual sensitivity` | 某个 mention 的生成是否真的依赖视觉输入 | diagnostic-only / future improvement clue | 值得继续作为分析概念保留 |
| `rescue evidence` | 某些高风险 mention 是否同时带有“应当保留”的视觉支持 | future improvement clue | 对 false positives 很关键 |
| `risk-minus-rescue` | 不是只累加 risk，也考虑 rescue 是否抵消风险 | future improvement clue | 当前更像分析框架，不是主规则 |
| `object category / mention position controls` | 对象类别、mention 位置、caption 长度等控制维度 | diagnostic-only | 更适合 error anatomy 和保守规则候选 |

## 3. Weak but Useful Negative Findings

| Signal / Evidence Item | 中文解释 | 当前作用 | 当前判断 |
|---|---|---|---|
| `image-level scalar` | 图级的单一风险分数 | negative / weak standalone signal | 太粗，难以稳定定位 mention 风险 |
| `diffuse attention alone` | 单纯“attention 分散” | negative / weak standalone signal | 不足以单独判断 hallucination |
| `pure concentration alone` | 单纯“attention 高度集中” | negative / weak standalone signal | 集中到错误区域也会 hallucinate |
| `absolute late confidence alone` | final-layer token confidence 很高 | negative / weak standalone signal | 高置信不等于有视觉依据 |
| `common mention risk` | 同时出现在 fixed 和 regular caption 里的 common mention | important caveat / future improvement clue | 风险更噪，容易误删，不适合 aggressive edit |

## 4. 当前方法学上的含义

这些信号合起来，支撑了当前几个关键判断：

- `weighted training-free verifier` 应继续作为主 evidence source；
- `middle visual verification`、`middle-to-late attention evolution`、`anchor-middle mismatch` 是当前最值得讲清楚的三类核心证据；
- `first_logit_only` 是干净得多的 action target；
- `common` mention 是 aggressive removal 最主要的 false-edit 来源之一；
- rescue evidence 很可能是后续更保守 routing 的重要线索，但当前还没有被提升为正式主方法。
