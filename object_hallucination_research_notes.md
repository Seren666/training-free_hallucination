# Object Hallucination 机制探索阶段性笔记

> 本文档是一个 **living research note**，用于记录当前阶段关于 LVLM object hallucination 的阅读启发、讨论想法、候选信号和后续实验问题。  
> 它不是论文综述，不是方法定稿，也不是结论文档。  
> 文中所有判断都只是当前阶段的猜测、假设和可探索方向，后续需要通过实验统计、消融和可视化结果不断修正。

---

## 0. 文档定位

这份文档的目标不是总结每一篇论文的具体做法，而是沉淀目前讨论中认为可能有用的判断。

当前阶段需要避免：

```text
1. 把已有论文逐篇复述；
2. 过早固定新方法 idea；
3. 把尚未验证的猜测写成确定结论；
4. 继续堆叠 VCD / CD 变体；
5. 围绕单一 benchmark 做过度工程化优化。
```

更希望保留的是：

```text
1. 哪些现象可能与 object hallucination 有关；
2. 哪些内部信号可能用于 hallucination risk 判断；
3. 哪些方向暂时不值得深挖；
4. 后续实验应该优先验证什么。
```

本文档后续会放入实验仓库，随着实验推进持续补充。

---

## 1. 当前研究目标

当前阶段的目标可以暂时表述为：

> 探索一种 training-free 的 object hallucination 缓解方向。理想情况下，通过一次正常 forward，从 LVLM 内部的 attention、logits、tokens、layer-wise 差异、head-wise 差异等信息中读取 hallucination risk signal；随后根据风险信号，只对可能存在问题的样本或 token 做轻量化干预。

这里的重点不是立刻确定最终 mitigation 方法，而是先验证：

```text
一次正常 forward 中，是否已经包含足够的信息来判断 object hallucination risk？
```

如果存在稳定信号，后续再考虑如何干预。干预可以是 selective CD、logit adjustment、early-anchor correction、轻量 attention/head intervention 或其他方式，具体需要实验决定。

当前先将问题收缩到：

```text
Task focus:
    object hallucination

Initial benchmark:
    POPE

Current advantage:
    已复现 VCD 完整数据，可作为参考基础
```

先聚焦 object hallucination 的原因：

```text
1. 已读方法大多主要作用于 object-level hallucination；
2. object hallucination 与视觉证据支持关系更直接；
3. POPE 适合作为第一阶段验证场景；
4. VCD 已有复现结果，方便比较和分析；
5. 若 risk signal 无法在 object hallucination 上稳定成立，就不宜过早扩展到更复杂任务；
6. 过早追求全领域适配容易导致 benchmark engineering。
```

---

## 2. 当前阅读后的总体判断

### 2.1 CD 类方法的统一抽象

目前看到的大量 CD / decoding 方法，虽然形式不同，但可以被统一理解为：

```text
选择 LVLM 中的某个信息源
    ↓
构造一个弱化版 / 失真版 / 去信息版分布
    ↓
用原始分布与该分布进行 logits correction
    ↓
试图压制 hallucination
```

这些信息源可能包括：

```text
视觉输入
视觉频率成分
prompt / instruction
attention heads
visual patches / scales
intermediate layers
attended image tokens
decoding strategy
```

这些方法的有效性说明：

```text
hallucination 可能受到多个信息源或内部通路影响。
```

但需要警惕：

```text
某个 source 被 perturb / mask / contrast 后有效
≠
该 source 是 hallucination 的唯一因果来源
≠
其他 source 不影响 hallucination
```

因此，继续寻找一个“更好的负样本分布”未必能带来本质突破。

---

### 2.2 Object hallucination 可能是分布式失败

当前一个更合理但仍待验证的猜测是：

> Object hallucination 可能不是单个模块、单个 head、单个输入源造成的，而是视觉接入、视觉信息处理、attention routing、多模态对齐、语义细化、语言侧组织等多个环节共同作用下的分布式失败。

也就是说，hallucination 可能不是一个局部错误，而是一个系统级现象。

可能相关的环节包括：

```text
1. Visual Access
   视觉输入是否被模型正常接入？

2. Visual Evidence Quality
   模型是否充分利用了对象相关视觉证据？

3. Attention Routing
   attention 是否落到关键区域？
   多个 heads 是否支持一致视觉方向？

4. Visual-Text Alignment
   object token hidden state 是否与 image-token hidden states 对齐？

5. Semantic Refinement
   中间层视觉信息是否被正确语义化？

6. Late Language Organization
   后期语言整合是否把没有视觉支持的 object token 补出来？

7. Token Competition
   真实 token 是否内部存在但最终被 hallucinated token 压过？
```

这仍然只是一个工作假设，需要后续实验验证。

---

## 3. 从“构造负样本”转向“读取内部风险信号”

当前阶段更值得探索的问题是：

```text
不是：如何构造新的 negative distribution？
而是：一次正常 forward 中，是否存在可解释的 hallucination risk signal？
```

这背后的想法是：

```text
如果真实 object token 和 hallucinated object token 在模型内部确实存在可检测差异，
那么不一定需要额外构造扰动输入、负样本图像、多阶段 patch 或训练 router。
```

理想方向是：

```text
one normal forward
    ↓
read internal signals
    ↓
estimate hallucination risk
    ↓
selectively intervene only when needed
```

这里需要区分不同成本等级：

```text
Level 0:
    只读信号，不干预，用于诊断分析。

Level 1:
    一次 forward 内完成 logit adjustment / risk penalty。
    最符合 one-forward 目标。

Level 2:
    只在高风险情况下额外触发 CD 或轻量二次计算。
    不是严格 one-forward，但比全程 CD 更省。

Level 3:
    全程多 forward / 多负样本 CD。
    当前不作为主线。
```

---

## 4. 暂时的 early / middle / late 工作假设

目前可以粗略假设，LVLM 内部推理过程可能存在不同阶段。这个划分不是结论，只是用于组织后续观察的工作框架。

### 4.1 Early stage：visual access / early multimodal anchor

Early stage 可能更偏向：

```text
1. 接收视觉 token；
2. 接收语义 token；
3. 建立初始 multimodal state；
4. 形成 early visual / linguistic prior。
```

一个值得关注的信号是：

```text
first logit / step0 distribution
```

当前猜测：

```text
step0 / first-token distribution 可能包含较强的 early multimodal state。
后续生成中的 hallucination 可能与生成轨迹逐渐偏离这个 early anchor 有关。
```

这与此前实验中“单纯 VCD 在 step0 处处理能获得大部分收益”的现象存在呼应。

但需要注意：

```text
first logit 不应被简单等同于纯视觉证据。
它可能同时包含：
    1. early visual prior；
    2. sentence-initial linguistic prior；
    3. discourse initialization bias。
```

因此，FLB 中的 first-logit 思路值得参考，但其 “The effect” 暂不作为深挖方向。

---

### 4.2 Middle stage：visual information processing / grounding

Middle stage 可能是视觉信息被真正处理、注入 object token、并与文本语义对齐的关键阶段。

当前猜测：

```text
如果某个 object token 在 middle layers 中缺少视觉支持，
但在 late layers 或 final logits 中显著突出，
那么它可能是后期语言整合阶段补出来的 hallucination。
```

Middle stage 可能需要观察：

```text
1. object token 是否吸收 image-token 信息；
2. object token hidden state 是否与 image-token hidden states 对齐；
3. 多个 heads 是否支持一致视觉区域或语义方向；
4. visual attention 是否稳定增长；
5. middle-layer distribution 是否已经支持该 object token。
```

这里的重点不是单纯看 attention mass，而是看视觉信息是否被稳定、合理、一致地用于支持当前 object token。

---

### 4.3 Late stage：semantic refinement / language emergence

Late stage 可能更多负责：

```text
1. 语义细化；
2. 文本组织；
3. 语言流畅性；
4. 最终 token selection。
```

风险模式可能是：

```text
middle-layer visual support weak
+
late-layer object confidence high
=
potential hallucination risk
```

也就是说，如果一个 object token 在 middle stage 没有足够视觉支持，却在 late stage 突然变强，那么它可能更多来自语言侧补全，而不是视觉证据。

这可以暂时称为：

```text
late emergence risk
```

该假设需要后续通过 layer-wise logit / token ranking / attention / alignment 统计验证。

---

## 5. 候选 hallucination risk signals

下面这些信号都只是候选项，不代表已经确定有效。后续需要分别做统计验证、消融和失败案例分析。

---

### 5.1 First-logit support

问题：

```text
后续出现的 object token 是否在 step0 / first logit 中已经有一定支持？
```

可能风险模式：

```text
final object confidence high
+
first-logit support low
=
potential language-driven emergence
```

直觉：

```text
如果某个 object token 在后续变得很强，
但在最早的 multimodal state 中几乎没有支持，
它可能更像是后期文本整合中冒出来的 token。
```

注意：

```text
first logit 是 early multimodal anchor，
不是纯 visual oracle。
```

---

### 5.2 Middle-layer visual support

问题：

```text
object token 在 middle layers 中是否获得足够 image-token 支持？
```

可观察内容：

```text
1. object token 对 image tokens 的 attention mass；
2. object token 与 image-token hidden states 的相似度；
3. image-token 信息是否在 middle layers 注入 object token；
4. middle-layer token distribution 是否已经支持该 object。
```

可能风险模式：

```text
middle-layer visual support low
+
final confidence high
=
potential hallucination risk
```

---

### 5.3 Visual-text alignment

问题：

```text
object token hidden state 是否与相关 image-token hidden states 形成稳定对齐？
```

可观察内容：

```text
1. object hidden state 与 image-token hidden states 的最大相似度；
2. top-k image tokens 的平均相似度；
3. top-k image tokens 是否语义一致；
4. image tokens 经 logit lens 或其他方式投影后，是否包含候选 object 语义。
```

风险直觉：

```text
如果 object token 的最终概率很高，
但它与 image-token representations 的 alignment 很弱，
则该 object 可能缺少视觉 grounding。
```

---

### 5.4 Head consistency

问题：

```text
多个 heads 是否支持一致的视觉区域或语义方向？
```

当前猜测：

```text
真实 object token 可能不是所有 heads 都看同一个点，
但多个 heads 的关注区域应当共同支持同一对象或相邻对象区域。

hallucinated object token 可能表现为：
    heads 分别关注背景、其他对象、边缘区域或不一致区域，
    最终被语言侧整合成一个错误对象。
```

可观察内容：

```text
1. head-to-head attention map similarity；
2. image attention entropy across heads；
3. image heads 是否参与当前 object token；
4. 多头关注区域是否语义一致。
```

---

### 5.5 Layer-wise distribution shift

问题：

```text
middle-layer token distribution 与 final-layer distribution 是否发生剧烈偏移？
```

可能风险模式：

```text
middle layers 不支持某 object token
但 final layer 突然强烈支持
```

可观察内容：

```text
1. KL / JS divergence between middle-layer distribution and final distribution；
2. token rank jump from middle to final；
3. object token 是否从 middle top-k 外突然进入 final top-k；
4. preceding-final distribution shift。
```

这个方向与 ECD 中使用 intermediate-final KL / NLL 特征的思路存在呼应，但当前目标是不训练 classifier，而是先验证无训练统计信号是否有区分度。

---

### 5.6 Late emergence

问题：

```text
object token 是否在 early/middle 不明显，但在 late layers 或 late generation steps 突然上升？
```

可能风险模式：

```text
early support weak
+
middle visual grounding weak
+
late confidence jump
=
high hallucination risk candidate
```

这可能对应：

```text
object token 不是由视觉处理自然产生，
而是在后期 semantic refinement / language organization 中被补出来。
```

---

### 5.7 Token ranking trajectory

问题：

```text
真实 token、幻觉 token、隐藏真实 token 在生成过程中的 ranking 轨迹是否不同？
```

可能观察：

```text
1. genuine tokens 随生成逐渐下沉；
2. hallucinated tokens 随生成逐渐上浮；
3. hidden genuine tokens 内部存在但最终没被 decoded；
4. hallucinated token 在后期超过 genuine token。
```

这个方向不只看最终 logits，而是看 token 在时间维度上的“生命轨迹”。

---

### 5.8 Hidden genuine competition

问题：

```text
图中真实存在但未输出的 object token 是否曾在模型内部保持较高 ranking？
```

如果存在，说明：

```text
模型可能并不是完全没有识别真实对象，
而是最终 decoding 中真实 token 输给了 hallucinated token 或语言模板。
```

这有助于区分两类情况：

```text
1. Visual evidence absence:
   模型内部确实没有真实对象信息。

2. Hidden genuine suppression:
   模型内部有真实对象信息，但最终没有输出。
```

---

### 5.9 Visual sensitivity

问题：

```text
当前 object token probability 是否真的依赖视觉输入？
```

可能风险模式：

```text
object token probability 对视觉输入变化不敏感
=
language-prior dominated candidate
```

这里的 visual sensitivity 可以先作为分析概念，不一定立刻做额外 forward。后续可考虑轻量 probe 或利用已有 VCD 复现结果对照。

---

## 6. 可考虑的 risk-guided intervention 方向

当前不确定最终优化方式。只有在候选 risk signal 被验证具有区分度后，才考虑具体干预。

可能方向包括：

### 6.1 Selective CD

```text
只在高风险样本或 token 上启用 CD，
而不是全程启用。
```

优点：

```text
1. 利用已有 VCD 复现基础；
2. 可减少不必要 CD harm；
3. 可作为第一阶段可控实验。
```

风险：

```text
1. 仍可能需要额外 forward；
2. risk 判断错误会导致误触发或漏触发；
3. 仍可能陷入 CD 负样本框架。
```

---

### 6.2 Logit penalty / risk reweighting

```text
对 high-risk object candidate 做 logit penalty。
```

可能形式：

```text
final_score(token)
=
model_confidence(token)
-
lambda * hallucination_risk(token)
```

风险：

```text
1. risk score 需要可靠；
2. 可能误伤真实但罕见 object；
3. 需要控制对生成丰富度的影响。
```

---

### 6.3 First-logit / early-anchor correction

```text
使用 step0 / first-logit distribution 作为 early anchor，
判断后续 object token 是否偏离 early multimodal state。
```

可借鉴 FLB 的 first-logit 思路，但暂不深挖 “The effect”。

可能方向：

```text
1. 不直接把 first logit 全局加到后续所有 token；
2. 将 first-logit support 作为 risk signal；
3. 仅对 late-emerging 且 first-support 弱的 object token 干预。
```

---

### 6.4 Lightweight attention / head intervention

```text
如果某个 object token 的 visual support 弱或 head inconsistency 高，
可以尝试轻量调整 attention / head contribution。
```

风险：

```text
1. attention 不等于 grounding；
2. head-level intervention 可能模型依赖强；
3. 需要避免破坏正常语义组织。
```

---

### 6.5 Conservative object decoding

```text
对于视觉支持弱但语言概率高的 object candidate，
采用更保守的 decoding 策略。
```

可能形式：

```text
1. 降低 object token 选择概率；
2. 要求更高 visual support；
3. 在不确定时避免引入新 object。
```

风险：

```text
1. 可能让模型变得过度保守；
2. 可能降低 recall / coverage；
3. 需要和 POPE / CHAIR 等指标平衡。
```

---

## 7. 暂不作为主线的方向

### 7.1 多负样本 CD

目前多种方法仍然是在更换 negative source，例如视觉扰动、频域扰动、prompt 扰动、head mask、patch scale 等。

这些方法有启发，但暂时不作为主线，因为：

```text
1. 推理成本通常较高；
2. 负样本是否对应真实 hallucination mechanism 不确定；
3. 方法很容易依赖超参数；
4. 容易变成又一个 VCD 变体。
```

---

### 7.2 Trained router / classifier

类似训练 router 或 hallucination classifier 的方法可以证明内部特征有可分性，但暂时不是当前方向。

原因：

```text
1. 当前目标偏 training-free；
2. 训练数据和标注方式可能引入 dataset-specific shortcuts；
3. 分类器有效不等于机制可解释；
4. 不利于先探索 one-forward 无训练信号。
```

但它们提供的 feature 设计可以参考。

---

### 7.3 FLB 的 “The effect”

FLB 值得借鉴的是：

```text
first logit / early anchor
```

而不是：

```text
“The effect”
```

当前判断：

```text
“The effect” 更像 captioning 场景中的语言初始化或 discourse bias。
它可能通过减少 indefinite object introduction 来降低 hallucination，
但机制深度不足，且容易变成风格性 trick。
```

因此暂不深挖。

---

### 7.4 单一 attention mass

不能把 attention mass 简单等同于 grounding。

原因：

```text
1. attention 高可能是错误关注；
2. attention 低不一定没有视觉信息，视觉信息可能经 anchor token 或 residual stream 间接传播；
3. 多头 attention 可能混合不同对象；
4. attention 是否有用还取决于 layer、head、token type 和任务形式。
```

更值得观察的是：

```text
attention correctness
head consistency
visual-text alignment
attention stability
middle-layer support
```

---

### 7.5 全领域 hallucination mitigation

当前不急于追求 OCR、relation、reasoning、knowledge QA、多轮对话等全领域适配。

原因：

```text
1. object hallucination 更适合作为第一阶段；
2. 视觉证据关系更直接；
3. 已有 VCD 复现结果可利用；
4. 多领域适配容易导致问题发散；
5. 当前内部信号是否有效尚未验证。
```

---

## 8. 待验证实验问题

以下问题均为待验证方向，不是结论。

### 8.1 Step0 / first-logit signal

```text
1. first-logit support 能否区分真实 object 与 hallucinated object？
2. step0 signal 能否预测整句 POPE / CHAIR hallucination？
3. VCD 在 step0 的收益是否来自改变 early multimodal state？
4. first-logit support 与后续 late emergence 是否相关？
```

---

### 8.2 Middle-layer visual grounding

```text
1. hallucinated object token 是否在 middle layers 中 visual support 更弱？
2. middle visual support gap 是否比 final confidence 更能预测 hallucination？
3. 哪些 layer range 的 visual support 最有信息量？
4. middle-layer object-image alignment 是否能区分真实/幻觉 object？
```

---

### 8.3 Head consistency

```text
1. 真实 object token 和 hallucinated object token 的 head consistency 是否存在统计差异？
2. image heads 是否对 object hallucination risk 有稳定指示作用？
3. 多头关注不一致是否对应更高 hallucination rate？
4. token type 是否影响 head-level visual reliance？
```

---

### 8.4 Layer-wise distribution shift / late emergence

```text
1. middle-final KL / JS divergence 是否能预测 hallucination？
2. hallucinated object 是否更容易出现 late-layer rank jump？
3. final high-confidence 但 middle low-support 的 token 是否更容易 hallucinate？
4. late emergence score 是否可以无训练地区分 object token 风险？
```

---

### 8.5 Token ranking trajectory

```text
1. genuine token 是否在生成过程中逐渐下沉？
2. hallucinated token 是否在生成过程中逐渐上浮？
3. hidden genuine token 是否存在但最终未输出？
4. token ranking trajectory 是否比 final logits 更有诊断价值？
```

---

### 8.6 Risk-guided intervention

```text
1. 若某个 risk signal 有效，是否可以只在高风险 token 上启用 CD？
2. 简单 logit penalty 是否能缓解 object hallucination？
3. first-logit support 能否作为 re-ranking prior？
4. 风险干预是否会降低 recall / coverage？
5. 在 POPE 上，risk-guided intervention 是否优于 full VCD？
```

---

## 9. 实验记录与后续更新模板

后续每做一组实验，可以按以下格式补充。

### Experiment Template

```markdown
### Experiment X: <实验名称>

- Date:
- Model:
- Dataset:
- Task:
- Signal / Method:
- Implementation note:
- Main observation:
- Failure cases:
- 是否支持当前假设:
- 是否保留该信号:
- Next step:
```

---

### Candidate Signal Tracking

| Candidate signal | Status | Initial observation | Keep? | Notes |
|---|---|---|---|---|
| First-logit support | pending |  |  |  |
| Middle-layer visual support | pending |  |  |  |
| Visual-text alignment | pending |  |  |  |
| Head consistency | pending |  |  |  |
| Layer-wise distribution shift | pending |  |  |  |
| Late emergence | pending |  |  |  |
| Token ranking trajectory | pending |  |  |  |
| Hidden genuine competition | pending |  |  |  |
| Visual sensitivity | pending |  |  |  |

---

## 10. 当前阶段一句话总结

当前阶段的问题不应继续停留在：

```text
如何构造一个新的 negative distribution？
```

而应转向：

```text
一次正常 forward 中，是否已经存在可解释、可迁移、可用于干预的 object hallucination risk signal？
```

目前最值得关注的候选方向包括：

```text
first-logit support
middle-layer visual grounding
visual-text alignment
head consistency
layer-wise distribution shift
late emergence
token ranking trajectory
```

但这些都还只是想法，后续需要通过 POPE 等 object hallucination benchmark 上的统计和消融来验证。
