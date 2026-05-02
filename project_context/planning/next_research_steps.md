# Next Research Steps

> Date: 2026-05-02
> Scope: priorities after locking fixed `first_logit / early-anchor` as the decoding reference, stopping the guard family, and completing both the first attention-distribution audit and the first paired regular-vs-early-anchor internal audit.

## 1. Current Reference To Keep Fixed

Keep fixed:

- full `fixed first_logit / early-anchor`

Role:

- strongest current decoding baseline
- main method candidate
- reference trajectory for all future signal audits

What not to do with it now:

- no more threshold tuning around failed guards
- no more token-level clipping follow-ups
- no more broad object-suppression or anchor-cleaning variants

## 2. Priority Order

### A. First: consolidate the mechanism story before any new method

Immediate focus:

- consolidate the finished internal-signal audits into a stable mechanism story
- keep the internal-signal line active, but do not jump from descriptive evidence to a runtime selector
- treat `first_logit`-side object-local middle verification as the main positive signal surface
- treat shared-event `regular -> early-anchor` delta only as a boundary check, not the main method direction

Current strongest families to build on:

- middle image-attention mass
- middle-to-late attention-mass change
- anchor-plus-verification interaction
- controlled visual sensitivity with random-mask comparison
- first-logit-gap x verification-evolution interaction

Signals to de-prioritize as standalone rules:

- diffuse entropy alone
- pure concentration alone
- another broad guard based on low attention or object-token membership
- any shared-event trajectory-delta heuristic that is weak in the paired audit

### B. Second: validate signal stability before designing correction

Next measurement focus:

- check whether the best signals remain stable when the event subset grows or changes
- compare the same signals across asymmetric active-event slices and true shared-event paired deltas
- explicitly separate:
  - within-trajectory verification signals
  - shared-event trajectory-delta signals
- keep measurement first and method design second

The practical question is:

- which signals keep ranking near the top when the subset, object mix, control design, and pairing setup change
- and whether they remain strongest on the `first_logit`-side `introduced vs correct` split rather than only on weak paired deltas

### C. Third: keep early-anchor as the fixed decoding reference, not the optimization target

Near-term posture:

- keep fixed `first_logit / early-anchor` as the reference decoding trajectory
- use it to define future object-event audits
- do not resume active method tweaking around it until the signal story is clearly stronger

This means:

- early-anchor stays fixed
- the research surface moves to internal measurement

### D. Fourth: keep the failed guard family paused

Stay paused:

- `object_safe_anchor`
- `attention_gated_attnanchor`
- `candidate_local_guard`
- `middle_verified`
- `middle_refined`

Why:

- none beat fixed `first_logit`
- the recurring cost remained object-mention or correct-object collapse
- the new attention-distribution audit does not justify returning to that family

### E. Fifth: only resume correction-method design when the signal side is stronger

Only resume method design if a future signal family clearly beats the current weak heuristics.

That means:

- a signal should outperform simple diffuse entropy
- it should remain competitive against middle attention mass and mass-evolution signals
- it should remain meaningful not only on `introduced vs correct`, but also under the relevant paired shared-event view
- it should have a plausible correction interface that is narrower than the failed guard family

Likely acceptable future directions, if justified later:

- first-logit-side object-local middle verification
- mention-level verification with stronger causal support
- phrase-level or trajectory-level methods only if the method boundary becomes much cleaner than the current shared-delta story

## 3. Explicit Pauses

Not now:

- no new token-level clipping variant
- no broad object suppression
- no broad anchor cleaning
- no threshold search
- no classifier training
- no new benchmark branch for this question
- no attempt to turn weak entropy-only effects into a runtime controller

## 4. Current Recommendation

1. keep fixed `first_logit / early-anchor` as the locked decoding reference
2. treat internal hallucination signal discovery as the main active research thread
3. prioritize middle-attention mass, mass-evolution, and anchor-plus-verification interactions over diffuse-entropy heuristics
4. treat visual sensitivity as supporting verification, not a standalone rule
5. do not turn the current weak shared-event trajectory deltas into a runtime controller
6. only return to correction methods when the signal side is clearly strong enough to justify a new action unit
