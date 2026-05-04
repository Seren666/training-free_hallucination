# Reference Literature and What We Learned

这不是完整 `Related Work`，而是当前项目在方法形成过程中真正参考过、借鉴过、部分采用过、明确排除过的工作清单。

用途是：

- 向导师说明当前方法不是“凭空冒出来”的；
- 说明我们从哪些 decoding / verification / internal-evidence 论文里学到了什么；
- 也说明为什么项目最后没有继续走“再堆一个 contrastive decoding 变体”的路线。

说明：

- 下面的 `Year` 和 `Venue / Publication` 只在能够较可靠确认时写实。
- 若当前只能确认 arXiv 或搜索结果，文中会明确写 `arXiv preprint`、`venue unknown` 或 `待核对`，避免编造。

| Paper / Method | Year | Venue / Publication | Core idea | What we learned | Relation to current project | Status in our project |
|---|---:|---|---|---|---|---|
| `VCD` — *Mitigating Object Hallucinations in Large Vision-Language Models through Visual Contrastive Decoding* | 2024 | CVPR 2024 | 构造视觉扰动 / 反事实视图，与原分布做 contrastive decoding，压制 hallucination | 视觉 contrastive branch 确实能缓解 object hallucination；但继续堆 negative distribution 不一定是我们的主线突破口 | 项目早期重要起点；帮助我们建立 object hallucination benchmark 和 baseline 意识 | background / initial baseline inspiration |
| `FLB / First Logit Boosting` — *First Logit Boosting: Visual Grounding Method to Mitigate Object Hallucination in Large Vision-Language Models* | 2026 | arXiv preprint | 把 first-logit / early-anchor 当作减少 object hallucination 的关键支点 | 我们最直接学到的是 `first_logit` 作为 early anchor 很有价值；但不准备把其 `The effect` 解释变成当前主线 | 直接影响了 fixed `first_logit` baseline 的锁定 | partially adopted; early-anchor idea adopted, “The effect” not adopted |
| `SECOND` — *Mitigating Perceptual Hallucination in Vision-Language Models via Selective and Contrastive Decoding* | 2025 | arXiv preprint; official repo 标注 ICML 2025，待核对 | 用 selective + contrastive 的方式，按对象感知和多尺度视觉信息做对比解码 | “不是所有 step / visual evidence 都该被同等对待”这个想法很重要 | 支持我们对 selective action 和 source-aware targeting 的兴趣 | related work / external comparison candidate |
| `Octopus` — *Alleviating Hallucination via Dynamic Contrastive Decoding* | 2025 | CVPR 2025 | 动态选择 decoding 行为，不同 generation 状态下采用不同 contrastive 处理 | 不同 generation steps 可能需要不同 action；静态单规则未必最优 | 影响了我们对 dynamic routing 的理解，但没有进入当前主方法 | related work / dynamic decoding background |
| `iTaD` — *Mitigating Hallucinations in Multi-modal Large Language Models via Image Token Attention-Guided Decoding* | 2025 | NAACL 2025 | 用 image token attention decline / mismatch 来引导 decoding 调整 | 图像 token attention 的衰减和 hallucination 有关系，但单一 attention signal 不足以单独成方法 | 为我们后续关注 `middle-to-late attention evolution` 提供了概念支持 | conceptual support for attention-evolution view |
| `Devils in Middle Layers / Attention Lens` — *Devils in Middle Layers of Large Vision-Language Models: Interpreting, Detecting and Mitigating Object Hallucinations via Attention Lens* | 2025 | CVPR 2025 | 通过 attention lens 解释 middle layers 的 object hallucination 形成和检测 | middle layers 不是噪声区，而是很有信息量的证据区间 | 很强地支持了我们“middle-layer verification”这条叙事 | strong conceptual support; supports middle-layer verification story |
| `The Hidden Life of Tokens / VISTA` — *The Hidden Life of Tokens: Reducing Hallucination of Large Vision-Language Models via Visual Information Steering* | 2025 | DBLP / OpenReview 显示 ICML 2025，建议再核对 | 研究 token 在层间的轨迹与 visual information steering，并提出 VISTA | token-level hidden trajectory、hidden genuine token、layer-wise evolution 这些概念非常有启发 | 强化了我们对 token / mention 级内部轨迹而非单点 logit 的关注 | conceptual support for token-level / layer-evolution view |
| `MFCD` — *Multi-Frequency Contrastive Decoding: Alleviating Hallucinations for Large Vision-Language Models* | 2025 | EMNLP 2025 | 通过不同频率成分构造 contrastive 分支，缓解模型忽视特定视觉频率信息的问题 | 频域扰动可以提供一种有意义的 negative source，但仍然属于 contrastive decoding 主谱系 | 告诉我们“负样本还能继续设计”，但我们主动没有沿这条路继续扩展 | related contrastive decoding work, not current mainline |
| `ECD` — *Efficient Contrastive Decoding with Probabilistic Hallucination Detection* | 2025 | arXiv preprint; venue unknown / 待核对 | 利用概率式 hallucination detection，在 contrastive decoding 中更高效地调整分布 | intermediate-final discrepancy / uncertainty / discrepancy-style cue 值得看作 hallucination signal | 和我们后续关注 middle-final shift、risk signal 读出存在概念呼应 | diagnostic inspiration; related to layer-wise discrepancy view |
| `MaskCD` — *MaskCD: Mitigating LVLM Hallucinations by Image Head Masked Contrastive Decoding* | 2025 | arXiv preprint | 通过 image-head masking 构造 contrastive sample，减轻 hallucination | masking 视觉头或局部证据可以构造更 targeted 的 contrastive source | 说明 contrastive decoding 还有很多结构化变体，但并不改变我们退出该主线的决定 | related work, not current mainline |
| `MoD` — *Mixture of Decoding: An Attention-Inspired Adaptive Decoding Strategy to Mitigate Hallucinations in Large Vision-Language Models* | 2025 | Findings of ACL 2025 | 根据 attention correctness 动态切换 complementary / contrastive decoding 策略 | “不同状态下用不同 action policy” 这个思想很强，对 routing 很有启发 | 与我们后来的 `source-aware` 和 potential action routing 想法有亲缘性，但不属于当前已确认方法 | related to action routing idea, not current method |
| `Classifier / learned verifier diagnostic` | internal | internal diagnostic | 用内部特征训练分类器，估计 hallucination 或 mention correctness | internal features 确实包含可学习信息，但 learned classifier 容易变成 upper-bound，不一定保留机制清晰度 | 帮助我们确认“内部特征不是噪声”，但没有被纳入主 runtime | upper-bound diagnostic only, not main method |
| `Weighted training-free verifier` | internal | internal method | 将多个 mention-level risk / rescue signals 做手工加权融合，不依赖训练 | manual signal-strength-aware weighting 比 best-single 或 equal-weight 更稳；main gain 来自 evidence families 的组合，而非单一 magic feature | 当前方法主证据源，直接支撑 full correction line | current main evidence source |

## 额外说明

### 1. 我们真正采用了什么

当前主方法真正采用的，不是某篇外部工作里的完整 decoding 机制，而是这些工作共同启发出的几个判断：

- object hallucination mitigation 不一定非要依赖新的 negative distribution；
- middle layers 和 layer evolution 很值得读；
- token / mention 局部证据比 image-level scalar 更可靠；
- action 需要 bounded，不宜一上来就全局 aggressive。

### 2. 我们明确没有继续采用什么

- 没有继续堆新的 `VCD / CD` 变体；
- 没有把 classifier 变成主方法；
- 没有把 dynamic routing / MoD-style action mixture 正式写进当前 full-confirmed pipeline；
- 没有把 `The effect` 变成当前主叙事。

### 3. 为什么这份表对导师沟通有用

这份清单最重要的功能不是“证明我们读得多”，而是帮助导师快速判断：

- 当前方法与 existing decoding literature 的关系是什么；
- 哪些思想已经被我们吸收进来；
- 哪些路线我们是刻意停下来的；
- 为什么当前 full-confirmed 主线更像 `internal evidence + bounded correction`，而不是“又一个 decoder patch”。
