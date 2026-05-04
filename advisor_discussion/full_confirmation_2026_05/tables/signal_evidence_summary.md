# Signal Evidence Summary

| Signal / Evidence Item | What it currently supports | Current status |
|---|---|---|
| `middle visual verification` | 支持 hallucinated mention 和 correct mention 的区分，是当前主 evidence family 之一 | strong |
| `middle-to-late attention evolution` | 支持“中层验证不足 + 后期演化异常”这一主线，是当前 strongest family 之一 | strong |
| `anchor-middle mismatch` | 支持 first-logit 侧 mismatch story，是当前 strongest family 之一 | strong |
| weighted training-free verifier | 把上述 families 组合成当前主 mention-level verifier，不依赖 classifier | main evidence source |
| source-exclusive risk concentration | `first_logit_only` top10 precision 明显高于 `common`，说明 source-exclusive mentions 更干净 | important routing evidence |
| common mention risk weakness | `common` mentions 更容易误伤，解释了 aggressive removal 的主要 false-edit 来源 | important caveat |
| rescue evidence for false positives | harmful removal 往往 rescue 更强，提示后续更保守 routing 可能有价值 | analysis evidence only |
| classifier | 证明 internal signals 可学，但只作为 upper-bound diagnostic / backup | not main method |

当前总判断：

- image-level scalar 弱。
- mention-local evidence 强。
- weighted training-free verifier 足以支撑当前 full correction story。
- source group 尤其是 `first_logit_only` vs `common` 的区别，对 branch tradeoff 很关键。
