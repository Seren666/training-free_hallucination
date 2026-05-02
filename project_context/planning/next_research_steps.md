# Next Research Steps

> Date: 2026-05-02
> Scope: priority order after full COCO-CHAIR confirmation, evaluator alignment, completed mechanism analysis, and the negative `Object-Safe`, `Attention-Gated`, `Candidate-Local`, `Middle-Verified`, and `Middle-Refined` pilots.

## 1. Current Best Baseline

Current decoding baseline to keep fixed:

- full `fixed first_logit / early-anchor`

Reason:

- it is still the strongest current COCO-CHAIR result
- every follow-up pilot so far underperforms it on the `1000` pilot

## 2. Priority Order

### A. First: consolidate the full negative follow-up chain

Immediate priority:

- treat `Object-Safe` and `Attention-Gated AttnAnchor` as informative negative results
- treat `Candidate-Object Local Guard` as a narrower but still negative result
- treat `Middle-Verified Early Anchor` as the narrowest and healthiest token-level clipping follow-up so far, but still negative
- treat `Middle-Refined Early Anchor` as a different anchor-construction family that still fails under broad step0 low-attention refinement
- treat `Attention-Shape` as an offline-only route that did not justify generation
- treat simple caption-level `Dual-Trajectory Mention Selection` as a feasibility-only route that did not justify full selected-caption evaluation
- isolate what was still too broad in their runtime action
- preserve the current mechanism claim boundary

What this means concretely:

- do not call the current attention gate a method win
- do not call the current candidate-local guard a method win
- do not call the current middle-verified gate a method win
- do not call the current middle-refined anchor a method win
- do not call the current dual-trajectory caption-level fallback a method win
- do not expand either failed pilot to full scale
- document the likely failure mode:
  - broad or semi-broad object-token suppression still harms correct mentions
  - diffuse attention-shape alone is not strong enough to define a good runtime rule
  - even middle-layer verification, when used as token-level boost clipping, still perturbs too many helpful pushes
  - even anchor-source refinement can collapse mentions if the step0 refinement trigger is too broad
  - simple caption-level fallback is too coarse when the decisive `first_only` support signals are weak

### B. Second: separate “new family” from “working method”

If method work continues:

- move away from token-level boost clipping as the default follow-up family
- keep anchor-construction refinement on the table conceptually, but do not treat the current `middle_refined` rule as validated
- use the middle-layer audit as analysis evidence, not as a proven runtime or anchor-construction gate
- move closer to an actual mention boundary, phrase boundary, or dual-trajectory verification unit
- avoid broad gating over a large object-token vocabulary on many late steps
- avoid treating a better audit signal as automatically a good intervention signal

The next prototype should be narrower than:

- all object-token ids on low-attention steps
- or all strong object candidates in the current `top-k`
- or all candidates that merely look weak under a coarse middle-rank lens
- or all strong anchor object tokens whenever a global step0 low-attention flag fires

The next prototype should be closer to:

- phrase-aware
- mention-local
- mention-verified
- trajectory-aware without crude whole-caption rollback

Likely implication from this round:

- the next useful method probably has to reason over the specific object phrase or mention boundary
- not just token-id membership plus a coarse score threshold
- if dual-trajectory is revisited, it should likely be phrase-level fusion or mention-level verification, not whole-caption fallback
- do not immediately launch another token-level clipping variant just because it is narrower than `Middle-Verified`
- do not immediately launch another anchor-refinement variant unless it is materially sparser than the current broad step0 source cleaning rule

### C. Third: keep pilot discipline strict

Before any new full run:

- require a `1000` pilot first
- only allow full expansion if the pilot beats fixed `first_logit` or shows a clearly better tradeoff

Health criteria remain:

- no first-word change
- no empty captions
- no substantial object-mention collapse
- no correct-object collapse
- no obvious regression in `CHAIRs / CHAIRi`
- no object-mention drop beyond the explicit health threshold

## 3. Explicit De-Prioritization

### D. Do not do parameter sweep now

Not now:

- no `gamma / lambda / cd_beta` sweep
- no threshold sweep
- no score tuning

Reason:

- the main problem is method shape, not parameter selection

### E. Do not start a new benchmark line now

Not now:

- no AMBER expansion
- no MME
- no new large benchmark branch

Reason:

- the current uncertainty is inside the decoding rule itself
- new benchmark surface area would not resolve that

### F. Do not build a classifier now

Not now:

- no classifier training
- no threshold search
- no heavy routing policy

Reason:

- image-level selectors already failed
- the current selective problem is still at the runtime intervention-definition level

## 4. Current Recommended Sequence

1. keep full fixed `first_logit` as the active baseline
2. record the five negative follow-up results clearly:
   - `object_safe_anchor`
   - `attention_gated_attnanchor`
   - `candidate_local_guard`
   - `middle_verified`
   - `middle_refined`
3. record that `attention_shape_guard` currently stops at offline feasibility
4. record that simple caption-level dual-trajectory rollback also stops at feasibility
5. only design a new prototype if it is materially different from both token-level boost clipping and the current broad anchor-source cleaning rule
6. require a `1000` pilot before any new full COCO-CHAIR run
7. avoid parameter sweep, classifier work, and benchmark expansion until a better pilot exists

## 5. Current Research Posture

Best current framing:

- `first_logit / early-anchor` remains the strongest current decoding candidate
- `COCO-CHAIR` remains the main positive benchmark
- object-level evidence still supports an object-token-local mechanism story
- middle-layer evidence strengthens the mechanism story
- but turning that evidence back into token-level runtime clipping still does not beat the fixed baseline
- and turning it into broad anchor-source cleaning also does not beat the fixed baseline
- attention-shape signal seems real but not strong enough by itself for a runtime guard
- simple dual-trajectory caption-level fallback is cleaner in framing, but its `first_only` support boundary is too weak for rollout
- the `middle_verified` pilot shows that narrower gating can preserve mentions better without becoming a win
- the `middle_refined` pilot shows that a new intervention point alone is not enough if the source-cleaning rule is still too broad
- future method work should change unit of action and keep the runtime action sparse, not only move the same broad rule earlier
