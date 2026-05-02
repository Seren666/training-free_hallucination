# Next Research Steps

> Date: 2026-05-02
> Scope: priorities after locking fixed `first_logit / early-anchor` as the decoding reference, stopping the guard family, and completing the first attention-distribution / visual-sensitivity audits.

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

### A. First: continue internal hallucination signal discovery

Immediate focus:

- treat this round's attention-distribution audit as the new active research line
- keep looking for internal signals that separate hallucinated vs correct object mentions without immediately turning them into a decoding rule

Current strongest families to build on:

- middle image-attention mass
- middle-to-late attention-mass change
- anchor-plus-verification interaction
- controlled visual sensitivity with random-mask comparison

Signals to de-prioritize as standalone rules:

- diffuse entropy alone
- pure concentration alone
- another broad guard based on low attention or object-token membership

### B. Second: validate signal stability before designing correction

Next measurement focus:

- check whether the best signals remain stable when the event subset grows or changes
- compare the same signals across event types instead of only `introduced vs correct`
- keep measurement first and method design second

The practical question is:

- which signals keep ranking near the top when the subset, object mix, or control design changes

### C. Third: keep early-anchor as the fixed decoding reference, not the optimization target

Near-term posture:

- keep fixed `first_logit / early-anchor` as the reference decoding trajectory
- use it to define paired object-event audits
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
- it should have a plausible correction interface that is narrower than the failed guard family

Likely acceptable future directions, if justified later:

- mention-level verification
- candidate-level verification with stronger causal support
- phrase-level or trajectory-level methods only if the measurement story becomes much cleaner

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
3. prioritize middle-attention mass, mass-evolution, and controlled visual sensitivity over diffuse-entropy heuristics
4. only return to correction methods when the signal side is clearly strong enough to justify a new action unit
