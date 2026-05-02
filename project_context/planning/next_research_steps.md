# Next Research Steps

> Date: 2026-05-02
> Scope: priority order after full COCO-CHAIR confirmation, evaluator alignment, completed mechanism analysis, the negative `Object-Safe` pilot, and the negative `Attention-Gated AttnAnchor` pilot.

## 1. Current Best Baseline

Current decoding baseline to keep fixed:

- full `fixed first_logit / early-anchor`

Reason:

- it is still the strongest current COCO-CHAIR result
- both follow-up selective pilots underperform it on the `1000` pilot

## 2. Priority Order

### A. First: consolidate the new negative selective-pilot evidence

Immediate priority:

- treat `Object-Safe` and `Attention-Gated AttnAnchor` as informative negative results
- treat `Candidate-Object Local Guard` as a narrower but still negative result
- treat `Attention-Shape` as an offline-only route that did not justify generation
- treat simple caption-level `Dual-Trajectory Mention Selection` as a feasibility-only route that did not justify full selected-caption evaluation
- isolate what was still too broad in their runtime action
- preserve the current mechanism claim boundary

What this means concretely:

- do not call the current attention gate a method win
- do not call the current candidate-local guard a method win
- do not call the current dual-trajectory caption-level fallback a method win
- do not expand either failed pilot to full scale
- document the likely failure mode:
  - broad or semi-broad object-token suppression still harms correct mentions
  - diffuse attention-shape alone is not strong enough to define a good runtime rule
  - simple caption-level fallback is too coarse when the decisive `first_only` support signals are weak

### B. Second: design a tighter object-local intervention

If method work continues:

- move closer to the actual candidate object token or mention-local decision
- avoid broad gating over a large object-token vocabulary on many late steps
- prefer a middle-layer verification surface over coarse image-level or caption-level routing

The next prototype should be narrower than:

- all object-token ids on low-attention steps
- or all strong object candidates in the current `top-k`

The next prototype should be closer to:

- candidate-token-local
- phrase-aware
- mention-local
- mention-verified without whole-caption rollback

Likely implication from this round:

- the next useful method probably has to reason over the specific object phrase or mention boundary
- not just token-id membership plus a coarse score threshold
- if dual-trajectory is revisited, it should likely be phrase-level fusion or mention-level verification, not whole-caption fallback
- the most justified next prototype is now a constrained `Middle-Verified Early Anchor` pilot on `1000` COCO-CHAIR images

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
2. record the three negative selective results clearly:
   - `object_safe_anchor`
   - `attention_gated_attnanchor`
   - `candidate_local_guard`
3. record that `attention_shape_guard` currently stops at offline feasibility
4. design a narrower object-local prototype only if it is materially different from broad or semi-broad object-token dampening
5. if method work continues, prioritize one `Middle-Verified Early Anchor` `1000` pilot before any broader expansion
6. do not launch simple caption-level dual-trajectory rollback from the current weak-support signals
7. use `1000` pilot gates before any new full COCO-CHAIR run
8. avoid parameter sweep, classifier work, and benchmark expansion until a better pilot exists

## 5. Current Research Posture

Best current framing:

- `first_logit / early-anchor` remains the strongest current decoding candidate
- `COCO-CHAIR` remains the main positive benchmark
- object-level evidence still supports an object-token-local mechanism story
- but the current selective prototypes are still not local enough to beat the fixed baseline
- attention-shape signal seems real but not strong enough by itself for a runtime guard
- simple dual-trajectory caption-level fallback is cleaner in framing, but its `first_only` support boundary is too weak for rollout
- the new middle-layer audit is the first follow-up that clearly strengthens a more local verification story
- future method work should become more local, not more global
