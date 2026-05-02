# Next Research Steps

> Date: 2026-05-03
> Scope: priorities after locking fixed `first_logit / early-anchor` as the decoding reference, stopping the guard family, completing the internal-signal audits, and testing the first layer-wise anchor replacement route.

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
- treat the new layer-wise anchor result as a useful negative method result:
  - late-layer ensemble anchors can look cleaner offline
  - but always-on anchor replacement still underperforms fixed `first_logit` at 1000 images

Current strongest families to build on:

- middle image-attention mass
- middle-to-late attention-mass change
- anchor-plus-verification interaction
- controlled visual sensitivity with random-mask comparison
- first-logit-gap x verification-evolution interaction
- layer-group comparisons as a descriptive audit surface, especially:
  - `late_27_31` target-logit support
  - shallow / early-middle image-attention mass

Signals to de-prioritize as standalone rules:

- diffuse entropy alone
- pure concentration alone
- another broad guard based on low attention or object-token membership
- any shared-event trajectory-delta heuristic that is weak in the paired audit
- simple middle-weak plus late-strong trigger rules
- always-on layer-anchor replacement without stronger runtime evidence

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
- layer-wise anchor signals can still be audited, but not promoted to a new default decoding anchor yet

### D. Fourth: keep the failed guard family paused

Stay paused:

- `object_safe_anchor`
- `attention_gated_attnanchor`
- `candidate_local_guard`
- `middle_verified`
- `middle_refined`
- broad always-on layer-anchor replacement as a new main-line decoding method

Why:

- none beat fixed `first_logit`
- the recurring cost remained object-mention or correct-object collapse
- the new attention-distribution audit does not justify returning to that family
- the new layer-wise anchor audit is mechanistically interesting, but the best 1000 pilot still regresses on CHAIR

### E. Fifth: only resume correction-method design when the signal side is stronger

Only resume method design if a future signal family clearly beats the current weak heuristics.

That means:

- a signal should outperform simple diffuse entropy
- it should remain competitive against middle attention mass and mass-evolution signals
- it should remain meaningful not only on `introduced vs correct`, but also under the relevant paired shared-event view
- it should have a plausible correction interface that is narrower than the failed guard family

Likely acceptable future directions, if justified later:

- first-logit-side object-local middle verification
- layer-group signal analysis, but not direct late-layer anchor replacement
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
- no immediate second round of layer-anchor replacement tuning
- no immediate mismatch-trigger runtime implementation

## 4. Current Recommendation

1. keep fixed `first_logit / early-anchor` as the locked decoding reference
2. treat internal hallucination signal discovery as the main active research thread
3. prioritize middle-attention mass, mass-evolution, and anchor-plus-verification interactions over diffuse-entropy heuristics
4. treat visual sensitivity as supporting verification, not a standalone rule
5. do not turn the current weak shared-event trajectory deltas into a runtime controller
6. treat layer-wise anchor evidence as descriptive support, not as a new default anchor source
7. do not turn the current mismatch signals into a runtime controller yet
8. only return to correction methods when the signal side is clearly strong enough to justify a new action unit
