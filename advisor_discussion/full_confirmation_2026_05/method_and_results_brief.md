# 方法与结果简报

## 1. 当前结论概览

我们已经在 full COCO-CHAIR scale、`LLaVA-1.5-7B` caption setting 下确认：基于 `weighted training-free mention-level verifier` 的 `bounded correction`，能够在 locked generation baseline `fixed_first_logit` 之上继续降低 object hallucination。

当前保留三条 branch，而且定位不同：

- `firstlogit_removal_top10`
  - raw metric 最强。
  - 是当前 `metric-strong retained branch`。
- `dual_phrase_replace_v1`
  - raw score 稍弱，但 correct-object preservation 和语言质量更好。
  - 是当前 `quality-preserving retained branch`。
- `removal_top10_firstlogit_only_guard`
  - raw score 低于 original removal，但误删更少、correct-object loss 更小、语法损伤更少。
  - 是当前 `safer-removal retained diagnostic branch`。

这三条 branch 当前都不自动淘汰、不自动替换。

如果只看一句话总结：当前 full result 支持的方法主线不是“再造一个新的 decoding”，而是“用一次正常 forward 中可读出的 mention-level internal evidence，对 fixed caption 做 bounded correction”。

术语说明见：

- [appendix/terminology_glossary.md](appendix/terminology_glossary.md)

## 2. 我们先发现了哪些有用信号

当前方法不是先想好 correction，再去找理由；恰恰相反，方法主线是从一轮轮“哪些 internal signals 真有用、哪些看起来直观但其实不够强”的筛选里长出来的。

最开始我们并不确定 object hallucination 能否被 `one-forward` 内部信号稳定区分。早期更自然的想法是：

- 看 image-level scalar 能不能直接判断一张图的 hallucination 风险；
- 看某个简单的 attention statistic 能不能直接当 hallucination detector；
- 或者继续沿 `VCD / CD` 思路，寻找更强的 negative distribution。

实验推进后的结论是：真正稳定的不是 coarse image-level 信号，而是 `mention-local internal evidence`。也就是说，问题不是“整张图现在风险高不高”，而是“这个 caption 里的某个 object mention，在模型内部是否真的拿到了足够视觉支持”。

### 2.1 强信号 / 核心证据

#### `middle visual verification`

- 中文解释：
  - 中间层里，这个 object mention 是否已经得到视觉证据支持。
- 直观理解：
  - 如果某个对象在最终输出里被明确说出来，但在 middle layers 几乎没有视觉支持，它更像是后期语言侧补出来的内容。
- 当前作用：
  - main verifier signal。

#### `middle-to-late attention evolution`

- 中文解释：
  - 从中间层到后期层，object token 对图像区域的关注是否沿着合理路径演化。
- 直观理解：
  - 我们更关心“支持是如何形成和延续的”，而不是只看某一层 attention 高不高。
- 当前作用：
  - main verifier signal。

#### `anchor-middle mismatch`

- 中文解释：
  - `first_logit / early-anchor` 给出的早期支持，是否和 middle-layer verification 不一致。
- 直观理解：
  - 如果 early stage 给出的 anchor 很弱，中间层验证也弱，但后面 token 还是被说出来，就更像语言组织在后期把对象“补”了出来。
- 当前作用：
  - main verifier signal。

#### `source-exclusive first_logit_only risk concentration`

- 中文解释：
  - 只出现在 fixed `first_logit` caption 中、而 regular caption 中没有的对象提及，更容易是风险 mention。
- 直观理解：
  - `first_logit_only` 是一个很关键的 source-group 信号，它并不是 ground truth，但它告诉我们哪些 mention 更像“early-anchor 额外引入”的对象。
- 当前作用：
  - main routing clue，也是 Candidate A 的直接来源。

### 2.2 中等强度或辅助信号

#### `head agreement / head consistency`

- 中文解释：
  - 多个 attention heads 是否围绕同一对象形成相对一致的支持。
- 当前理解：
  - 单独拿出来不够强，但作为 supporting evidence 有启发。

#### `layer consistency`

- 中文解释：
  - 相邻层或分组层之间，对同一 mention 的支持是否稳定。
- 当前理解：
  - 可以帮助判断某个信号是偶然尖峰还是持续趋势。

#### `visual sensitivity`

- 中文解释：
  - 某个 mention 的生成是否真的对视觉输入敏感，而不是主要由语言先验驱动。
- 当前理解：
  - 是有启发的分析方向，但在当前主线里更多是 diagnostic clue。

#### `rescue evidence`

- 中文解释：
  - 某些看起来 high-risk 的 mention，实际上在 middle verification 或相关视觉支持上又出现了“保留它”的理由。
- 当前理解：
  - 它很重要，因为很多 harmful removal 不是低风险尾部，而是“风险也高，但 rescue 更强”。

#### `risk-minus-rescue`

- 中文解释：
  - 不是只累计风险证据，也要考虑能不能被一些 rescue 证据抵消。
- 当前理解：
  - 当前更像分析框架，而不是最终上线规则。

#### `object category / mention position controls`

- 中文解释：
  - 对象类别、mention 在 caption 中的位置、caption 长度等控制变量。
- 当前理解：
  - 更适合作为 error anatomy 和保守规则候选的分析维度。

### 2.3 弱但有用的负面结论

这部分很重要，因为它解释了为什么当前方法不是别的样子。

#### `image-level scalar` 很弱

- 我们最早希望用一两个图级统计量快速判断 hallucination 风险。
- 结果是：过于 coarse，难以对 caption 内部的具体对象做可靠判断。

#### `diffuse attention alone` 不够

- 单纯说“attention 很分散，所以在 hallucinate”并不稳定。
- attention 分散可能只是复杂场景、长 caption 或对象竞争造成。

#### `pure concentration alone` 不够

- 相反，attention 特别集中也不一定更可靠。
- 集中到错误区域，仍然可能 hallucinate。

#### `absolute late confidence alone` 不够

- 最终层置信度高，不代表这个对象有视觉依据。
- 正因为如此，我们才从 final confidence 转向看 middle-to-late trajectory。

#### `common mentions` 更噪，更容易误删

- 这是 full error anatomy 的关键发现之一。
- `common` mention 不是都安全，但它们比 `first_logit_only` 噪得多， aggressive removal 很容易在这里误伤 correct object。

总的研究脉络可以概括为：

- 最开始以为可以靠 image-level 或简单 attention statistic 判断 hallucination；
- 后来发现真正有效的是 mention-local internal evidence；
- 再往后发现真正需要的不是一个单一神奇分数，而是几个 evidence families 的组合；
- 于是当前方法才会收缩成 `weighted training-free mention-level verifier + bounded correction`。

## 3. 方法从这些信号怎么来

当前方法不是“继续堆一个新的 CD 变体”，而是明确从 `negative distribution construction` 这条路退出来，转向 `one-forward internal evidence`。

### 3.1 为什么不继续堆新的 negative distribution

我们早期阅读和参考过很多 decoding-based mitigation 路线，例如 `VCD / ICD / OPERA / SECOND / Octopus / iTaD / MoD` 一类工作。它们给了很大启发，但也逐步暴露出一个问题：

- 如果不断发明新的 counterfactual image、mask、attention perturbation 或 contrastive branch，方法会越来越像“又一个 decoding patch”；
- 这种路线通常更依赖多 forward、负样本构造方式和调参；
- 但它未必直接回答“模型内部到底哪里开始失去视觉支持”。

所以当前项目把问题改写成：

> 一次正常 forward 中，是否已经存在足够稳定、可解释、可迁移的 hallucination risk signal？

### 3.2 为什么先锁定 `fixed_first_logit`

当前 generation 主线不是 open-ended 地比较很多生成器，而是先把 fixed `first_logit / early-anchor` 锁成 generation baseline。

原因是：

- 它已经在 COCO-CHAIR 上被验证为当前最强 generation baseline；
- 它比 regular caption 更能暴露 early-anchor 与后续语言组织之间的关系；
- 一旦 generation baseline 锁定，后续就能把主要变量集中到“caption 内 object mention 的 verification 与 correction”。

这里的意思不是说 `first_logit` 自己就是最终方法，而是：

- generation 先固定；
- hallucination mitigation 再转到 caption 内部做 mention-level correction。

### 3.3 为什么是 `mention-level verifier`

当前主方法的核心单位不是 image、不是整句 caption，而是 `object mention`。

原因是：

- object hallucination 最终发生在具体对象提及上；
- 一句 caption 里可能同时有 correct mentions 和 hallucinated mentions；
- 如果只做 image-level risk，会丢掉最关键的定位信息；
- correction 真正要执行时，也需要知道“改哪个 mention，而不是整句一起动”。

### 3.4 为什么是 `training-free`

当前阶段有意把 verifier 设计成 `training-free`，而不是直接上 classifier。

原因不是 classifier 无效，而是：

- classifier 容易吸收 dataset-specific shortcut；
- classifier 有上界诊断价值，但不一定保留机制可解释性；
- 当前目标是先证明 internal evidence 本身已经有足够区分度；
- 一旦无训练信号都能站住，再讨论 learned verifier 才更有说服力。

所以当前 policy 是：

- classifier only as upper-bound diagnostic / backup；
- 不进入主方法 runtime。

### 3.5 为什么是 `weighted` verifier

当前 verifier 不是 best-single signal，也不是 equal-weight 平均，而是 `weighted training-free verifier`。

原因是：

- strongest evidence families 的强度并不相同；
- 一些信号是 main risk evidence，一些只是 supporting clue，一些则更像 rescue；
- equal-weight 往往把弱信号放得过重，反而稀释了真正有效的中间层证据；
- manual signal-strength-aware weighting 在当前 full pipeline 里已经被证明比单信号和简单平均更稳。

所以“weighted”在这里不是复杂训练，而是：

- 承认不同 evidence families 贡献不同；
- 用明确的、可审计的方式把它们合成一个 mention-level risk score。

### 3.6 为什么是 `top10` 默认 operating slice

`top10` 不是在当前这轮临时挑出来的最优点，而是已经成为当前默认 operating slice。

原因是：

- `top5` 太保守，coverage 不够；
- `top20` 虽然能继续压分，但 correct-object loss 和语言损伤通常更明显；
- `top10` 在 raw gain、preservation 和 action scale 之间形成了目前最可控的平衡。

因此当前 policy 是：

- `top10` 是默认方法 slice；
- `top20` 只保留为 diagnostic upper-bound。

### 3.7 bounded correction 的基本流程

当前主线可以用一句话概括为：

1. 先生成 fixed `first_logit` captions；
2. 抽取 caption 里的 `object mentions`；
3. 用 `weighted training-free mention-level verifier` 给每个 mention 打 risk；
4. 只对 `top10` high-risk mentions 做 `bounded correction`；
5. runtime 不使用 GT / CHAIR label；
6. offline 评估再用 adapted / near-official CHAIR 复核。

## 4. 三条 branch 的机制详解

### 4.1 `firstlogit_removal_top10`

这是当前最直接、也最强势的一条 branch。

它的机制是：

1. 输入是 fixed `first_logit` caption；
2. 对 caption 里的 object mentions 打 risk；
3. 取 `top10` high-risk mentions；
4. 直接删除这些 mention。

为什么它 raw metric 最强，其实很直观：

- object hallucination 在 CHAIR 里最终是“说了不存在的对象”；
- 直接删除 high-risk mention，是最直接降低 `Hallucinated Objects` 的方式。

它的优势在于：

- raw CHAIR 最强；
- hallucinated object reduction 最大；
- full adapted 结果最亮眼。

但它的问题也很明确：

- 会误删 correct object；
- 会带来更明显的 `Correct Objects` 损失；
- 局部删除可能造成 caption 片段不够自然，出现 grammar / coherence 伤害。

所以它当前的正确定位不是“唯一主方法”，而是：

- `firstlogit_removal_top10 remains the metric-strong retained branch.`

### 4.2 `dual_phrase_replace_v1`

这条 branch 的思路是：如果一个 risky mention 不应该保留，最好的做法未必总是删除；有时更合适的做法是局部改写成一个更安全的短语。

它的机制大致是：

1. 比较 regular caption 和 fixed `first_logit` caption；
2. 对 `first_logit_only` high-risk mention 优先尝试局部 `phrase replacement`；
3. 如果 regular side 或局部对齐中存在更安全的替代表达，就替换；
4. 如果找不到安全替换，部分情况才 fallback 到 removal。

它和 direct removal 的差别在于：

- direct removal 的目标是“把高风险对象拿掉”；
- dual replacement 的目标是“尽量把 risky mention 修成更自然、更保守、且不明显伤害整体语言质量的表达”。

这条 branch 的优势是：

- correct-object preservation 更好；
- object mention loss 更小；
- 语言质量和局部自然度更好；
- 它确实存在真实 `phrase replacement`，不是纯粹换个名字的 removal。

它的瓶颈也很明确：

- `true replacement coverage` 仍然有限；
- 很多 case 最后还是 fallback 到 removal 或保守跳过；
- 所以 raw score 仍然打不过 original removal。

因此它当前的角色是：

- `dual_phrase_replace_v1 remains the quality-preserving retained branch.`

### 4.3 `removal_top10_firstlogit_only_guard` / Candidate A

这条 branch 不是凭空发明出来的，而是从 full error anatomy 里被“逼”出来的。

我们在分析 original removal 的 full failure anatomy 时发现：

- 很大一部分 harmful removal 来自 `common mentions`；
- `first_logit_only` mention 更像 source-exclusive risk pool，precision 更高；
- `common` mention 虽然也会有 hallucination，但噪声更大， aggressive removal 更容易误伤。

于是 Candidate A 的规则非常简单，也非常克制：

1. 仍然从同一个 full high-risk table 出发；
2. 仍然使用同一个 `primary_risk_score top10` slice；
3. 但只对 `source_group == first_logit_only` 的 risky mentions 执行 removal；
4. 对 `common` mentions 直接 abstain / keep。

它没有：

- 改 risk score；
- 改 threshold；
- 改 generation；
- 改 verifier；
- 用 GT / CHAIR label 做 runtime decision。

它的意义在于：

- 不是追求更强 raw score；
- 而是验证“source-aware abstention 能不能显著减少误删”。

full diagnostic 的答案是肯定的：

- 它保留了 `81.27%` original removal 的 hallucination reduction；
- 多保住了 `1580` correct mentions；
- grammar/coherence heuristic issue rate 从 `0.0449` 降到 `0.0109`。

但它也不能被写成替代者，因为：

- raw score 仍弱于 original removal；
- preservation 仍略弱于 dual。

所以它的正确定位是：

- `removal_top10_firstlogit_only_guard is retained as a safer-removal diagnostic branch.`

## 5. Full results and tradeoff

完整主表见：

- [tables/full_main_results.md](tables/full_main_results.md)
- [tables/branch_tradeoff_table.md](tables/branch_tradeoff_table.md)

这里先用最关键的 adapted full numbers 概括：

- fixed `first_logit`
  - `CHAIRs=0.1631`
  - `CHAIRi=0.0513`
  - `hallucinated=9609`
  - `correct=177831`
  - `mentions=187440`

- `firstlogit_removal_top10`
  - `CHAIRs=0.1291`
  - `CHAIRi=0.0413`
  - `hallucinated=7516`
  - `correct=174332`
  - `mentions=181848`

- `removal_top10_firstlogit_only_guard`
  - `CHAIRs=0.1356`
  - `CHAIRi=0.0430`
  - `hallucinated=7908`
  - `correct=175912`
  - `mentions=183820`

- `dual_phrase_replace_v1`
  - `CHAIRs=0.1403`
  - `CHAIRi=0.0444`
  - `hallucinated=8187`
  - `correct=176204`
  - `mentions=184391`

如果只看 `CHAIRs / CHAIRi`，结论会是：

- original removal 最强；
- Candidate A 第二；
- dual 第三。

但如果把 `Hallucinated Objects / Correct Objects / Object Mentions` 一起看，tradeoff 才完整：

- `firstlogit_removal_top10`
  - hallucination reduction 最强；
  - 但 correct-object loss 也最大。
- `dual_phrase_replace_v1`
  - 幻觉削减略弱；
  - 但 preservation 更好，整体语言质量也更稳。
- `removal_top10_firstlogit_only_guard`
  - 介于两者之间；
  - 放弃一部分 raw reduction，换来更少误删和更干净的局部文本。

这也是为什么当前不能只看 CHAIR：

- CHAIR 告诉我们 hallucination 降了多少；
- `Correct Objects` 告诉我们是不是靠“误删真实对象”在降分；
- `Object Mentions` 告诉我们是不是靠整体变得更少说 object 在降分。

因此当前最稳妥的叙事不是“单一最优”，而是：

- original removal 给出最强 raw score；
- dual 给出更好的 preservation / quality；
- Candidate A 给出 safer-removal tradeoff。

## 6. Near-official alignment

当前 full 结果不是只在一个工程 evaluator 上成立。

我们同时保留了两套评估口径：

- `adapted evaluator`
  - 当前项目中稳定运行的 Python3 CHAIR evaluator；
  - 可扩展到 full `40504` image scale；
  - 是我们主工程评估表。
- `near-official evaluator`
  - 使用 `chair_alignment` 中更接近官方 CHAIR 的流程做复核；
  - 目的不是重新生成 caption，而是检查 adapted 结果是不是 evaluator artifact。

当前 near-official full 排序是：

- regular: `0.1997 / 0.0669`
- fixed `first_logit`: `0.1594 / 0.0524`
- `firstlogit_removal_top10`: `0.1267 / 0.0424`
- `removal_top10_firstlogit_only_guard`: `0.1329 / 0.0441`
- `dual_phrase_replace_v1`: `0.1374 / 0.0455`

排序与 adapted evaluator 一致，方向也一致。

这意味着：

- 当前 full result 不是 adapted evaluator 的偶然产物；
- 三条 branch 的相对位置在更接近官方口径的复核下也能站住。

## 7. 当前 caveats

当前结果已经足够和导师沟通，但仍然有几个必须诚实保留的 caveats：

- 还没有 same-protocol 的 external `VCD / OPERA / RAD-VCD / RITUAL` full COCO-CHAIR caption baseline。
- 当前工作聚焦在 `COCO-CHAIR object hallucination`，不代表所有类型 hallucination 都已被解决。
- `dual_phrase_replace_v1` 的 true replacement coverage 仍然有限。
- `firstlogit_removal_top10` 虽然 raw score 最强，但 correct-object loss 仍明显。
- `removal_top10_firstlogit_only_guard` 是 diagnostic retained branch，不是替代全部方法的新主线。
- classifier 不是主方法，只是 upper-bound diagnostic。

## 8. 希望导师反馈的问题

- 当前 full result 是否已经足以支撑方法主线？
- 三条 branch 是否都应该进入 main table？
- Candidate A 更适合作为 main diagnostic，还是放在 appendix 更合适？
- 是否需要在论文主实验前先补 `VCD` full baseline？
- 是否应该继续优先优化 dual replacement coverage？
- 当前是否可以开始写论文中的方法与实验部分？
- `firstlogit_removal_top10`、`dual_phrase_replace_v1`、`removal_top10_firstlogit_only_guard` 三条 branch 的主次关系，是否适合按现在这种“raw / quality / safer-removal diagnostic”方式叙述？
