# Terminology Glossary

这份词汇表的目标是让导师不需要追完整项目历史，也能快速读懂当前沟通包里的专有词、内部命名和指标。

## object hallucination

中文解释：
模型在 caption 或回答中提到了图像中并不存在的对象。

项目中怎么用：
当前项目的主问题就是 `object hallucination`，而不是 relation、OCR、knowledge QA 等更广义 hallucination。

为什么重要：
这是当前 full result 的唯一聚焦对象，也是 COCO-CHAIR 最直接评估的现象。

## COCO-CHAIR

中文解释：
用于评估 image caption 中 object hallucination 的经典基准与指标体系。

项目中怎么用：
当前 full confirmation 全部围绕 COCO-CHAIR 展开。

为什么重要：
它是当前主 benchmark，也是我们和 regular / fixed / correction branches 比较的统一协议。

## CHAIRs

中文解释：
caption-level hallucination rate，即有多少比例的 caption 至少包含一个 hallucinated object。

项目中怎么用：
所有 main table 都报告 `CHAIRs`。

为什么重要：
它能反映“句子层面有多少 caption 出现幻觉”。

## CHAIRi

中文解释：
object-instance-level hallucination rate，即全部 object mentions 中有多少比例是 hallucinated mention。

项目中怎么用：
所有 main table 都报告 `CHAIRi`。

为什么重要：
它比 `CHAIRs` 更细，能反映对象提及层面的 hallucination 密度。

## hallucinated object count

中文解释：
被 CHAIR 判定为图像中不存在，但 caption 提到的对象数量。

项目中怎么用：
在 adapted full 和 near-official full 中都会统计。

为什么重要：
这是衡量 correction 是否真的删掉或修掉 hallucinated mentions 的直接计数。

## correct object count

中文解释：
被 CHAIR 判定为图像中存在，且 caption 正确提到的对象数量。

项目中怎么用：
用于衡量 preservation。

为什么重要：
如果 hallucinated object 降了，但 correct object 也掉很多，就说明方法可能靠误删在压分。

## object mentions

中文解释：
caption 中被 CHAIR 识别出来的对象提及总数，通常等于 `correct object count + hallucinated object count`。

项目中怎么用：
作为“是不是只是变得更少说 object”的检查量。

为什么重要：
它可以帮助区分“更准”与“只是更保守地少说”。

## fixed_first_logit

中文解释：
当前锁定的 generation baseline，基于 `first_logit / early-anchor` 路线生成 caption。

项目中怎么用：
所有 correction 都是在 fixed `first_logit` caption 之上做后处理。

为什么重要：
它是当前整个 correction story 的固定出发点。

## early-anchor

中文解释：
生成早期、尤其是 `first_logit` 所携带的初始多模态支持或初始化锚点。

项目中怎么用：
我们把 `first_logit` 看成一种 early anchor，用来理解后续 token 是否偏离早期视觉支持。

为什么重要：
它直接影响了 locked generation baseline 的选择，也影响了 `anchor-middle mismatch` 叙事。

## first-logit / FLB-style baseline

中文解释：
参考 `First Logit Boosting` 一类工作，将 `first_logit` 视作重要 early grounding signal 的 baseline 思路。

项目中怎么用：
当前 fixed `first_logit` 可以理解为一个 `FLB-style` locked generation baseline。

为什么重要：
它说明我们当前不是和普通 regular generation 比，而是和一个更强、更受控的 baseline 比。

## weighted training-free verifier

中文解释：
把多个 mention-level internal evidence families 用手工权重组合起来的无训练 verifier。

项目中怎么用：
这是当前主 evidence source。

为什么重要：
它决定哪些 mention 被判成 high-risk，以及后续 correction 作用到哪里。

## mention-level verifier

中文解释：
不是对整张图或整句 caption 打分，而是对 caption 里的每个 object mention 单独做风险判断。

项目中怎么用：
当前所有 correction 都先做 mention-level risk ranking。

为什么重要：
object hallucination 最终发生在具体对象提及上，mention-level 才能精确定位 action target。

## object mention

中文解释：
caption 里的一个对象提及，例如 `a dog`、`two chairs`、`a remote`。

项目中怎么用：
是 risk scoring 和 correction 的基本单位。

为什么重要：
不区分 mention，就无法做 bounded correction。

## top10 risk slice

中文解释：
按当前 primary risk score 排序后，默认只对最高风险的前 10 个 mention 执行 action 的 operating slice。

项目中怎么用：
`top10` 已经成为当前默认主结果设置。

为什么重要：
它是在 coverage、raw gain、preservation 和 action scale 之间当前最稳定的平衡点。

## top20 diagnostic upper-bound

中文解释：
把 action 范围扩到 top20，用来观察更激进上限，但不作为默认主结果。

项目中怎么用：
当前只保留为 diagnostic upper-bound。

为什么重要：
它能显示“如果更激进还能压到哪里”，但通常会带来更大的误删风险。

## bounded correction

中文解释：
不是重写整句 caption，而是只在少量 high-risk mention 上做局部、受限的修正。

项目中怎么用：
当前 correction 主线就是 bounded correction。

为什么重要：
它让方法更可解释，也更容易把 gain 和 damage 对应到具体 mention。

## source-exclusive mention

中文解释：
只出现在某一个 caption source 中、而不出现在另一个对照 source 中的 mention。

项目中怎么用：
最重要的是 `first_logit_only`。

为什么重要：
source-exclusive mentions 往往更能反映某条生成分支额外引入了什么对象。

## first_logit_only

中文解释：
只出现在 fixed `first_logit` caption 中，而 regular caption 中没有的 mention。

项目中怎么用：
它是当前最重要的 source group 之一，也是 Candidate A 只保留 action 的对象。

为什么重要：
它在 full anatomy 中显示出更高 precision，更适合做 aggressive action target。

## common mention

中文解释：
同时出现在 fixed `first_logit` 和 regular caption 中的 mention。

项目中怎么用：
它是另一个关键 source group。

为什么重要：
`common` mention 风险更噪， aggressive removal 更容易在这里误删 correct object。

## rescue signal

中文解释：
虽然某个 mention 有风险证据，但同时存在支持“应当保留”的视觉或中层证据。

项目中怎么用：
目前主要用于 error anatomy 和 false-positive 解释。

为什么重要：
它解释了为什么一些高风险行仍然会是 harmful removal。

## middle visual verification

中文解释：
中间层中，这个 object mention 是否已经得到视觉证据支持。

项目中怎么用：
是 current verifier 的 strongest family 之一。

为什么重要：
它直接支撑“对象是否真的有视觉 grounding”这一判断。

## middle-to-late attention evolution

中文解释：
从 middle 到 late layers，针对该 mention 的视觉关注是否沿合理路径演化。

项目中怎么用：
是 current verifier 的 strongest family 之一。

为什么重要：
它提供的是“支持如何形成”的动态信息，而不是单层静态值。

## anchor-middle mismatch

中文解释：
early anchor / `first_logit` 支持与 middle-layer verification 之间的不一致。

项目中怎么用：
是 current verifier 的 strongest family 之一。

为什么重要：
它帮助识别“早期没有站住、中层也没站住，但后期被语言组织补出来”的 hallucination 风险。

## phrase replacement

中文解释：
不直接删除 mention，而是把局部 risky phrase 换成一个更安全、更自然的替代表达。

项目中怎么用：
这是 `dual_phrase_replace_v1` 的核心动作。

为什么重要：
它是 preservation / quality branch 区别于 direct removal 的关键机制。

## fallback removal

中文解释：
当安全 replacement 找不到时，退回到直接删除的保守动作。

项目中怎么用：
`dual_phrase_replace_v1` 在部分 case 中仍会 fallback removal。

为什么重要：
它解释了 dual 为什么有时仍然会带有 removal 痕迹，也说明 replacement coverage 目前还不够高。

## retained branch

中文解释：
当前已经保留、可以进入方法讨论和结果表的 branch。

项目中怎么用：
`firstlogit_removal_top10` 和 `dual_phrase_replace_v1` 是当前两个 retained main branches。

为什么重要：
它决定哪些结果属于当前正式方法线，而不是一次性试验。

## diagnostic branch

中文解释：
保留用于解释 tradeoff、失败机制或更保守变体价值的 branch。

项目中怎么用：
`removal_top10_firstlogit_only_guard` 是 retained diagnostic branch。

为什么重要：
它帮助方法叙事更完整，但不自动升级为主分支。

## adapted evaluator

中文解释：
当前项目中稳定运行、可扩展到 full-scale 的 Python3 CHAIR evaluator。

项目中怎么用：
full main metrics 主要来自 adapted evaluator。

为什么重要：
它提供了当前主工程表。

## near-official evaluator

中文解释：
更接近官方 CHAIR 口径的对齐评估流程。

项目中怎么用：
用于复核 adapted evaluator 的稳定性和排序一致性。

为什么重要：
它增强了 full result 的可信度。

## external baseline

中文解释：
来自项目外部、可同协议比较的已有方法 baseline，例如 `VCD / OPERA / RITUAL` 的 full caption results。

项目中怎么用：
当前 external baseline availability audit 发现这部分还缺同协议 full payload。

为什么重要：
它是当前和导师沟通时必须诚实说明的 caveat 之一。

## VCD

中文解释：
`Visual Contrastive Decoding`，通过视觉扰动构造 contrastive 分支，抑制 object hallucination。

项目中怎么用：
它是项目早期重要参考和 baseline inspiration。

为什么重要：
很多后续路线都可以被理解为围绕 VCD 谱系展开。

## classifier upper-bound diagnostic

中文解释：
用内部特征训练分类器，估计 hallucination 风险，用作“如果允许训练，内部信号上限能到哪里”的诊断。

项目中怎么用：
只作为 upper-bound diagnostic / backup。

为什么重要：
它证明 internal features 不是纯噪声，但我们没有把它变成当前主方法。
