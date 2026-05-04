# 方法与结果简报

## 1. 当前一句话结论

我们已经在 full COCO-CHAIR scale、LLaVA-1.5-7B caption setting 下确认：基于 weighted training-free mention-level verifier 的 bounded correction，能够继续降低 fixed `first_logit` caption 的 object hallucination。当前保留三条 branch：`firstlogit_removal_top10` 是 raw metric 最强分支，`dual_phrase_replace_v1` 是 preservation / quality 更好的分支，`removal_top10_firstlogit_only_guard` 是更少误删的 safer-removal diagnostic branch。

## 2. 项目从哪里来

- 早期项目参考过 `VCD / CD / attention-guided decoding` 一类路线。
- 但当前主线已经不再继续堆 negative distribution 或新 decoding。
- `fixed_first_logit / early-anchor` 已经成为 locked generation baseline。
- 旧的 runtime guard / clipping / anchor-replacement 路线大多是负结果或暂停分支。
- 因此项目重心转向 one-forward / mention-level internal evidence，再基于这个 evidence 做 bounded correction。

## 3. 方法原理

- 第一步：先生成 fixed `first_logit` captions。
- 第二步：从 caption 中抽取 object mentions。
- 第三步：对每个 mention 用 weighted training-free mention-level verifier 打 risk score。
- verifier 当前主要依赖三类 internal evidence：
  - `middle visual verification`
  - `middle-to-late attention evolution`
  - `anchor-middle mismatch`
- 第四步：在默认 `top10` operating slice 上做 bounded correction。
- runtime decision 不使用 GT / CHAIR label。
- classifier 只作为 upper-bound diagnostic / backup，不作为主方法。

## 4. 三条当前保留分支

### A. `firstlogit_removal_top10`

- 机制：直接删除高风险 mention。
- 优点：raw CHAIR 最强。
- 缺点：correct-object loss 更大，局部删除损伤更多。
- 当前定位：metric-strong retained branch。

### B. `dual_phrase_replace_v1`

- 机制：尝试用 dual-caption 的局部 phrase replacement；找不到合适替换时才保守 fallback。
- 优点：preservation 和语言质量更好。
- 缺点：raw gain 稍弱，replacement coverage 仍有限。
- 当前定位：quality-preserving retained branch。

### C. `removal_top10_firstlogit_only_guard`

- 机制：只对 `first_logit_only` 的 high-risk mention 执行 removal，`common` mention 直接 abstain。
- 优点：raw score 虽弱于 original removal，但误删更少、correct-object loss 更小、grammar/coherence 也更健康。
- 缺点：不再追求最强 raw CHAIR。
- 当前定位：safer-removal retained diagnostic branch。

当前 branch policy：

- 三条 branch 都保留，但定位不同。
- 当前不二选一，也不自动替换。
- `firstlogit_removal_top10` remains the metric-strong retained branch.
- `dual_phrase_replace_v1` remains the quality-preserving retained branch.
- `removal_top10_firstlogit_only_guard` is retained as a safer-removal diagnostic branch.

## 5. Full result table

主表见：

- [tables/full_main_results.md](tables/full_main_results.md)

## 6. Tradeoff interpretation

- `firstlogit_removal_top10`
  - adapted full: `CHAIRs=0.1291`, `CHAIRi=0.0413`
  - 相对 fixed：
    - hallucinated `-2093`
    - correct `-3499`
    - mentions `-5592`
  - 它仍然是 raw metric 最强分支。

- `dual_phrase_replace_v1`
  - adapted full: `CHAIRs=0.1403`, `CHAIRi=0.0444`
  - 相对 fixed：
    - hallucinated `-1422`
    - correct `-1627`
    - mentions `-3049`
  - raw gain 弱于 original removal，但 preservation 和局部语言质量明显更好。

- `removal_top10_firstlogit_only_guard`
  - adapted full: `CHAIRs=0.1356`, `CHAIRi=0.0430`
  - 相对 fixed：
    - hallucinated `-1701`
    - correct `-1919`
    - mentions `-3620`
  - 相对 original removal：
    - 保留 `81.27%` original removal hallucination reduction
    - 多保住 `1580` correct mentions
    - grammar/coherence heuristic issue rate `0.0109` vs original removal `0.0449`

三者关系可以概括为：

- original removal 给出最强 raw score；
- dual 给出更好的 preservation / quality；
- Candidate A 提供一个更少误删的 safer-removal tradeoff。

另外，near-official alignment 也保持了同样排序，不是 adapted evaluator 的偶然现象。

## 7. 有用信号发现

- image-level scalar 基本弱，不能支撑 coarse selector。
- mention-local evidence 更强。
- 当前最稳定的 evidence families 是：
  - `middle visual verification`
  - `middle-to-late attention evolution`
  - `anchor-middle mismatch`
- `weighted training-free verifier` 是当前主 evidence surface。
- `first_logit_only` / source-exclusive mentions 更干净，风险更集中。
- `common` mentions 更容易误伤。
- rescue evidence 对 false positives 有提示，但当前还只是分析证据，不是主方法。

## 8. 当前 caveats

- 当前还没有 same-protocol 的 external `VCD` full COCO-CHAIR caption baseline。
- `dual_phrase_replace_v1` 的 replacement coverage 仍有限。
- `firstlogit_removal_top10` 仍有明显 correct-object loss。
- `removal_top10_firstlogit_only_guard` 是 safer-removal diagnostic branch，不是替代全部方法的新主线。
- `CHAIR / near-official` 仍然只覆盖 caption-level object hallucination，不代表所有 hallucination 类型。

## 9. 希望导师给的反馈

- 当前 full results 是否已经足以支撑方法主线？
- 三条 branch 应该如何放在 main results / appendix？
- 是否需要先补 `VCD` full baseline？
- 是否应该继续优化 dual replacement coverage？
- 当前是否可以开始写论文中的方法与实验部分？
- Candidate A 更适合保留为正式分支，还是只作为 diagnostic ablation？
