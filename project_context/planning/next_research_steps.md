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

### A. First: explain why the broad selective pilots failed

Immediate priority:

- treat `Object-Safe` and `Attention-Gated AttnAnchor` as informative negative results
- isolate what was still too broad in their runtime action
- preserve the current mechanism claim boundary

What this means concretely:

- do not call the current attention gate a method win
- do not expand either failed pilot to full scale
- document the likely failure mode:
  - broad object-token-id suppression still harms correct mentions

### B. Second: design a tighter object-local intervention

If method work continues:

- move closer to the actual candidate object token or mention-local decision
- avoid broad gating over a large object-token vocabulary on many late steps

The next prototype should be narrower than:

- all object-token ids on low-attention steps

The next prototype should be closer to:

- candidate-token-local
- phrase-aware
- mention-local

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
2. record both failed selective pilots clearly
3. design a narrower object-local prototype only if it is materially different from broad object-token dampening
4. use `1000` pilot gates before any new full COCO-CHAIR run
5. avoid parameter sweep, classifier work, and benchmark expansion until a better pilot exists

## 5. Current Research Posture

Best current framing:

- `first_logit / early-anchor` remains the strongest current decoding candidate
- `COCO-CHAIR` remains the main positive benchmark
- object-level evidence still supports an object-token-local mechanism story
- but the current selective prototypes are not yet good enough to beat the fixed baseline
- future method work should become more local, not more global
