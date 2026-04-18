# Step0 Attention-Backed Gate Design

> Date: 2026-04-18  
> Status: Proposed  
> Scope: `v1.1-D` cheap-signal refinement of `Path-Gated Visual Risk Decoding`

## 1. Why This Design Exists

The current short-answer POPE main line is still anchored at `gateent03`.

Observed `POPE / coco / random` evidence so far:

- `gateent03` remains the best promoted v1 operating point
- the `A-line` step-aware entropy / margin follow-up did not improve over `gateent03`
- the `P1/P2` preview-confirmation line improved diagnosis and selectivity, but still did not move onto a better quality-speed frontier than `gateent03`

So the next refinement should satisfy two constraints at once:

1. improve the chance of catching the truly important `step0` cases
2. avoid paying the extra-pass preview tax again

That leads to the current design question:

> Can we improve `step0` gate recall with a cheap attention-backed proxy that is already available from the base forward pass, without adding a second model pass?

## 2. Design Goal

The goal of `v1.1-D` is:

> keep the existing on-demand VCD branch unchanged, but enrich the `step0` cheap gate with an attention-backed signal so that the controller is more sensitive to risky early decisions without introducing preview compute.

This design is not trying to build a full attention-based controller.

It is trying to answer one narrower question first:

> whether adding cheap base-forward attention evidence at `step0` can outperform pure entropy gating on the short-answer POPE setting.

## 3. Problem Diagnosis

The current failure mode is unlikely to be "VCD reranking is ineffective when called."

The more likely issue is:

- too many decision-critical `step0` cases are not being sent to VCD
- pure entropy is not the whole story for that first token

For POPE, the answer length is usually around `2` generated tokens, so the first content token is disproportionately important.

The project also now has a second negative lesson:

- making the `step0` gate more visually informed by running a preview pass is possible
- but even a well-controlled preview pipeline still adds too much cost on this short-output benchmark slice

So the next refinement should try to make `step0` more informed while staying inside the original base forward computation.

## 4. Alternative Routes Considered

### 4.1 Route A: Step0 Attention-Backed Cheap Proxy

Use a cheap attention-side signal from the base forward pass at `step0`, combine it with entropy, and keep later steps unchanged.

Pros:

- stays inside one base forward pass
- is more aligned with the main "path risk as selective visual-risk routing" story
- specifically targets the most important decoding step

Cons:

- requires `output_attentions`
- the first available attention proxy is not yet a clean image-token-only statistic

### 4.2 Route B: Step0-Only Logit-Family Refinement

Stay entirely inside logit-derived signals and test a richer `step0` family based on entropy, top probabilities, or EOS-related cues.

Pros:

- cheapest engineering path
- smallest speed risk

Cons:

- likely lower upside because the project already tested adjacent logit-only refinements

### 4.3 Route C: All-Steps Attention Or Composite Gating

Apply attention-backed or mixed signals at every decoding step.

Pros:

- more general method story

Cons:

- unnecessary scope growth for short-answer POPE
- higher risk of paying a broad speed tax before the `step0` hypothesis is validated

## 5. Recommended Route

The recommended route is **Route A**:

> a `step0` attention-backed proxy gate, followed by the existing later-step entropy gate.

Reason:

- it directly tests the main unresolved hypothesis
- it does not reintroduce preview compute
- it keeps the branch narrow enough that a negative result is still informative

## 6. Proposed Method: Step0 Attention-Backed Gate

### 6.1 High-Level Rule

At `step0`, use a higher-recall rule that combines:

- the existing entropy signal
- a cheap attention-backed proxy computed from the base forward pass

For `step >= 1`, keep the current `gateent03` logic unchanged.

### 6.2 Base Distribution

Let the base next-token distribution at step $t$ be:

$$
p_t(y) = P(y_t = y \mid x, q, y_{<t})
$$

and let base entropy be:

$$
H_t = -\sum_y p_t(y)\log p_t(y)
$$

### 6.3 Attention-Backed Proxy

From the final-layer attention tensor of the base forward pass, let the mean-over-heads attention from the current query position to context position $j$ be:

$$
\bar{A}_t(j) = \frac{1}{M}\sum_{m=1}^{M} A_t^{(m)}(j)
$$

where $M$ is the number of attention heads.

The first proxy signal is the maximum concentration of that distribution:

$$
C_t = \max_j \bar{A}_t(j)
$$

This matches the current implementable statistic in the codebase:

- mean across heads
- final query only
- maximum attention mass over all context positions

Important limitation:

- this is **not yet** a strict image-token attention mass
- it is a cheap attention-backed proxy for over-concentrated early commitment

So the scientific claim of this line should remain modest.

### 6.4 Step0 Gate

The first tested `step0` gate is:

$$
g_0^{(D)} = \mathbf{1}\!\left[H_0 \ge \tau_e \;\lor\; C_0 \ge \tau_c\right]
$$

Interpretation:

- high entropy catches uncertain early decisions
- high attention concentration catches brittle, overly committed early decisions

The use of `OR` is intentional in the first round because the goal is to improve `step0` recall, not to suppress firing frequency further.

### 6.5 Later-Step Gate

For later steps, keep the current entropy gate:

$$
g_t^{(\ge 1)} = \mathbf{1}\!\left[H_t \ge \tau_{\text{later}}\right]
$$

with the current anchored default:

$$
\tau_{\text{later}} = 0.3
$$

### 6.6 Unified Gate

The full gate is:

$$
g_t =
\begin{cases}
1, & t = 0 \text{ and } \left(H_0 \ge \tau_e \lor C_0 \ge \tau_c\right) \\
1, & t \ge 1 \text{ and } H_t \ge \tau_{\text{later}} \\
0, & \text{otherwise}
\end{cases}
$$

### 6.7 Controller Behavior

This design does not change the controller actions.

When $g_t = 0$:

- `accept`

When $g_t = 1$:

- invoke the existing VCD branch
- apply the existing rerank logic

No preview branch is added.

## 7. Engineering Principles

### 7.1 No Extra Forward Pass

This branch must not add a preview or second inference pass.

Allowed:

- enabling `output_attentions` on the base forward
- deriving a cheap proxy from that output

Forbidden:

- any `step0` preview run
- any extra noisy-image confirmation stage

### 7.2 Later-Step Stability

The later-step rule should remain the current anchored `gateent03` logic in the first round.

That keeps attribution clean:

- if this line improves, the gain is most plausibly from the `step0` refinement
- if it fails, the negative result is easy to interpret

### 7.3 Honest Positioning

This method should be described as an **attention-backed cheap proxy gate**, not as a fully image-grounded attention gate.

The first round uses the statistic the codebase can already collect reliably.

If the line is promising later, a stricter image-token attention statistic can be explored as a follow-up.

## 8. Required Trace And Analysis Support

The implementation should support the following artifacts.

### 8.1 Probe Trace

The `attention probe` trace should expose, at minimum:

- `step0 attention_concentration`
- `step0 base_entropy`
- selected token id
- latency
- tokens/s

### 8.2 Gate Trace

The online gated runs should record:

- `gate_triggered`
- `gate_step_group`
- `gate_rule_name`
- `gate_trigger_sources`
- `gate_signal_name`
- `gate_signal_value`
- `gate_threshold`
- `attention_concentration`

### 8.3 Offline Screening Output

The screening result should report:

- entropy threshold
- attention threshold
- total samples
- triggered samples
- trigger rate
- step0 VCD-changed samples
- trigger hit count
- trigger hit rate
- trigger precision

## 9. Experimental Plan

### 9.1 Phase 0: Attention Probe On 200 Samples

Run a lightweight `regular + trace_attention` probe on:

- `POPE / coco / random / 200 / seed55`

Purpose:

- estimate the empirical distribution of `step0 attention_concentration`
- estimate its alignment with `always-on vcd` step0 changes
- measure the speed tax of enabling attention output

### 9.2 Phase 1: Offline Threshold Screening

Using:

- the new probe trace
- the existing `regular` trace
- the existing `always-on vcd` trace

screen:

$$
H_0 \ge \tau_e \lor C_0 \ge \tau_c
$$

The first threshold family should stay small:

- `\tau_e \in \{0.25, 0.30, 0.35\}`
- `\tau_c` chosen from empirical probe quantiles such as `p60 / p70 / p80 / p90`

### 9.3 Phase 2: Smoke Speed Check

Promote exactly two online candidates:

- `D-lite`
- `D-main`

Then run a `20`-sample smoke check first.

Goal:

- verify that enabling attention output does not push runtime too close to `always-on vcd`

If the smoke result already shows poor efficiency, stop the line early.

### 9.4 Phase 3: 200-Sample Online Validation

Only if smoke passes, run:

- `D-lite`
- `D-main`

against:

- `regular`
- `always-on vcd`
- `gateent03`

### 9.5 Promotion Rule

Only promote `D-line` beyond the 200-sample comparison if at least one candidate:

- clearly improves over `gateent03` on F1 or accuracy
- and remains clearly faster than `always-on vcd`

If the result is:

- worse quality than `gateent03`
- or tied quality with worse efficiency

then archive the line as a documented negative refinement.

## 10. Success Criteria

This line is promising if it can show all of the following:

- a meaningful improvement in `step0` trigger recall over pure entropy gating
- at least one online candidate that improves the `gateent03` quality-speed frontier
- a clean narrative that the gain came from a cheaper, more visually relevant early-step signal rather than from an extra compute branch

## 11. Fallback Route

If the probe or smoke phase shows that attention-backed gating is too expensive or poorly aligned, the immediate fallback should be:

> `step0-only logit-family refinement`

This fallback keeps the same overall experimental ladder, but removes `output_attentions` and returns to purely logit-derived cheap signals.

That fallback is intentionally secondary, not parallel-first:

- main route: `Step0 Attention-Backed Gate`
- fallback route: `Step0-Only Logit-Family Refinement`

## 12. Scope Boundary

### In Scope

- `step0` attention-backed cheap proxy
- later-step entropy gate unchanged
- 200-sample probe and online validation
- early-stop smoke screening
- lightweight offline threshold analysis

### Out Of Scope

- preview-based confirmation
- all-step attention gating
- image-token span reconstruction in the first round
- EOS-promote changes
- benchmark expansion before the 200-sample result is known
