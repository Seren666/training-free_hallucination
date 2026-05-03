# Next Research Steps

> Date: 2026-05-03
> Scope: priorities after locking fixed `first_logit / early-anchor` as the decoding reference, completing the hypothesis audit, finishing the first mention-level verification audit, running the multidimensional-evidence verification follow-up, and finishing the classifier-diagnostic distillation audit.

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
- treat middle-to-late attention evolution as the strongest current evidence family
- treat anchor-middle mismatch interaction as the strongest first-logit-side mismatch family
- treat mention-level verification as now feasible at a diagnostic level
- treat the new training-free multidimensional verification result as a refinement, not a reset:
  - best composite is still `middle_to_late_abnormal_evolution`
  - it remains robust, but does not beat the best single signal
- treat the new weighted-evidence result as the current strongest training-free mention-level verifier:
  - task-matched weighted scores now beat both the best single signal and the old equal-weight composite on all four main tasks
  - the strongest global-style weighted scores are `risk_minus_rescue_weighted_score` and `global_weighted_evidence_score`
  - the failure-mode-specific scores are now:
    - `introduced_focused_weighted_score`
    - `persistent_focused_weighted_score`
    - `removed_focused_weighted_score`
  - persistent remains hardest, but its shortfall improves materially under weighted scoring
- treat the optional lightweight classifier as an upper-bound diagnostic only:
  - it confirms the signals contain learnable hallucination information
  - it does not become the new primary method line
- treat the new multi-seed diagnostic as stable enough to preserve:
  - upper-bound performance is repeatable across seeds
  - internal-only features still beat category + position control consistently
- treat the distillation result as partial, not decisive:
  - introduced-focused distilled mismatch helps
  - global distilled training-free scores still do not close the gap to the upper-bound
- treat the weighted follow-up as a stronger but still incomplete training-free consolidation:
  - it closes part of the gap left by equal weighting
  - it still stays below the classifier upper-bound on split-based evaluation
  - it does not remove the need for a backup verifier
- treat shared-event `regular -> early-anchor` delta only as a boundary check, not the main method direction
- treat the new layer-wise anchor result as a useful negative method result:
  - late-layer ensemble anchors can look cleaner offline
  - but always-on anchor replacement still underperforms fixed `first_logit` at 1000 images

Current strongest families to build on:

- middle image-attention mass
- middle-to-late attention-mass change
- middle-x-mass-change interaction
- anchor-plus-verification interaction
- weighted combinations of those same three dominant families
- controlled visual sensitivity with random-mask comparison
- first-logit-gap x verification-evolution interaction
- layer-group comparisons as a descriptive audit surface, especially:
  - `late_27_31` target-logit support
  - shallow / early-middle image-attention mass

Current evidence status after the hypothesis audit:

- strongly supported:
  - middle verification deficit
  - middle-to-late attention evolution
  - anchor-middle mismatch
  - removed / persistent / introduced are not identical failure paths
- now additionally supported at mention level:
  - hallucinated object mentions can be distinguished from correct mentions above chance
  - the best mention-level candidates are still evolution + mismatch + middle-verification signals
  - multi-dimensional learned combination improves further over the training-free composite
- now additionally supported after distillation:
  - internal-only learned verification is stable across seeds
  - classifier-with-controls is stronger, but category terms absorb too much of the linear explanation to become the preferred story
  - distilled training-free scores help the introduced slice more than the global binary task
- now additionally supported after weighted consolidation:
  - signal-strength-aware training-free weighting is worthwhile
  - failure-mode-aware training-free weighting is worthwhile
  - weighted scores now beat the best single signal at mention level
  - weighted scores also beat the old equal-weight composite at mention level
- weak but still useful:
  - late readiness surge as a relative rank-jump story
  - diffuse attention
  - head agreement
  - layer consistency
  - visual sensitivity
- weak or not useful as standalone rules:
  - diffuse entropy alone
  - pure concentration alone
  - absolute late confidence alone

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
- keep the hypothesis registry framing:
  - mechanism evidence
  - supporting validation evidence
  - correction-facing candidate evidence
  - insufficient runtime rule
- keep the mention-level verification framing:
  - diagnostic verification only
  - not a runtime selector
  - not a correction method yet
  - training-free composite remains the main mechanism-facing route
  - classifier remains backup evidence only
- keep the classifier boundary explicit:
  - preserve it as a backup verifier / upper-bound diagnostic
  - do not let it become the default next method
- keep measurement first and method design second

The practical question is:

- which signals keep ranking near the top when the subset, object mix, control design, and pairing setup change
- and whether they remain strongest on the `first_logit`-side `introduced vs correct` split rather than only on weak paired deltas
- and whether the mention-level verification story is strong enough to justify a user-approved second-pass correction design discussion
- and whether the new weighted verifier should be the default training-free verification surface for any future design discussion
- and whether the gap between training-free composite and classifier is better closed by stronger causal validation rather than more decoding heuristics
- and whether the next training-free attempt should stay global or become more intentionally introduced-focused

### C. Third: keep early-anchor as the fixed decoding reference, not the optimization target

Near-term posture:

- keep fixed `first_logit / early-anchor` as the reference decoding trajectory
- use it to define future object-event audits
- do not resume active method tweaking around it until the signal story is clearly stronger

This means:

- early-anchor stays fixed
- the research surface moves to internal measurement
- layer-wise anchor signals can still be audited, but not promoted to a new default decoding anchor yet
- no new correction method should start without a fresh user-approved design discussion
- fixed `first_logit` remains the strongest generation baseline, but it is no longer the only active research target

### D. Fourth: keep the failed guard family paused

Stay paused:

- `object_safe_anchor`
- `attention_gated_attnanchor`
- `candidate_local_guard`
- `middle_verified`
- `middle_refined`
- broad always-on layer-anchor replacement as a new main-line decoding method
- runtime mismatch-trigger methods

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
- and the user should explicitly want to turn the evidence line back into a method-design round

Likely acceptable future directions, if justified later:

- first-logit-side object-local middle verification
- middle-to-late attention evolution with stronger causal support
- anchor-middle mismatch with better control evidence
- mention-level verification as a second-pass design surface, but only after user approval
- a weighted training-free verification surface is now the strongest current non-learned route, but still not solved
- an introduced-focused training-free verifier now looks more plausible than a fully global distilled score
- layer-group signal analysis, but not direct late-layer anchor replacement
- mention-level verification with stronger causal support
- phrase-level or trajectory-level methods only if the method boundary becomes much cleaner than the current shared-delta story

## 3. Explicit Pauses

Not now:

- no new token-level clipping variant
- no broad object suppression
- no broad anchor cleaning
- no new layer-anchor replacement branch
- no threshold search
- no further classifier expansion as a main-line method
- no heavy learned verifier branch
- no classifier claim beyond upper-bound diagnostic evidence
- no classifier-led correction implementation
- no new benchmark branch for this question
- no attempt to turn weak entropy-only effects into a runtime controller
- no immediate second round of layer-anchor replacement tuning
- no immediate mismatch-trigger runtime implementation
- no automatic jump from evidence discovery to correction design
- no automatic jump from mention-level verification to second-pass correction implementation

## 4. Current Recommendation

1. keep fixed `first_logit / early-anchor` as the locked decoding reference
2. treat internal hallucination signal discovery as the main active research thread
3. treat mention-level verification as the current highest-value narrowing step between mechanism story and any future correction discussion
4. keep the training-free composite line active, but recognize that the current equal-weight composite still trails the best single evolution signal
5. upgrade the weighted training-free evidence score family to the current default mention-level verification surface
6. keep the lightweight classifier only as a backup upper-bound check that the internal signals carry learnable information
7. treat the new multi-seed classifier result as backup evidence, not as permission to pivot the project toward learned verification
8. prioritize middle-attention mass, mass-evolution, anchor-plus-verification interactions, and their weighted combinations over diffuse-entropy heuristics
9. treat visual sensitivity, head agreement, and layer consistency as supporting verification, not standalone rules
10. do not turn the current weak shared-event trajectory deltas into a runtime controller
11. treat layer-wise anchor evidence as descriptive support, not as a new default anchor source
12. do not turn the current mismatch signals into a runtime controller yet
13. if methods are revisited later, center them on the strongest supported families:
   - middle verification deficit
   - middle-to-late attention evolution
   - anchor-middle mismatch
14. if the user wants to continue, the next acceptable step is a second-pass correction **design discussion** or stronger causal verification analysis, not an implementation jump
15. if that discussion happens, prefer a narrowly scoped training-free weighted route first; keep classifier as backup verifier only
16. do not start any correction implementation without explicit user discussion and approval first
