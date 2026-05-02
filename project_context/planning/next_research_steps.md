# Next Research Steps

> Date: 2026-05-02
> Scope: near-term priority order after completed full COCO-CHAIR confirmation, evaluator alignment, image-level audit, and object-level mechanism analysis.

## 1. Priority Order

### A. First: consolidate the mechanism story

Immediate priority:

- unify the current narrative across:
  - full COCO-CHAIR positive result
  - near-official evaluator alignment
  - POPE null result
  - image-level audit negative result
  - object-level audit positive result

Why this comes first:

- the evidence is already strong enough to justify a mechanism-oriented story
- the bigger current risk is overclaiming or fragmenting the interpretation
- writing discipline is more valuable now than another experiment

### B. Second: small evaluation alignment / cross-check work

After the mechanism story is clean:

- tighten official or near-official evaluator confidence where feasible
- allow only small cross-checks that do not reopen a large benchmark branch

Examples of acceptable next validation:

- official-style evaluator sanity where no new generation is needed
- narrow consistency checks on already generated captions

### C. Third: consider a selective early-anchor prototype

Only after the story and evaluation base are stable:

- consider a very small object-local selective prototype

If this happens, the starting signals should be:

- `mention_position_ratio`
- `anchor_target_token_rank`
- `adjusted_target_rank_if_applied`
- possibly `anchor_weight_at_object_step`

Important boundary:

- this would be a controlled prototype, not an immediate full method branch

## 2. Explicit De-Prioritization

### D. Do not do parameter sweep now

Not now:

- no `gamma / lambda / cd_beta` sweep
- no benchmark chasing
- no score tuning

Reason:

- current uncertainty is mechanistic, not mainly hyperparameter uncertainty

### E. Do not start a new benchmark line now

Not now:

- no AMBER expansion
- no MME
- no new large benchmark branch

Reason:

- the current evidence is already rich enough on COCO-CHAIR
- adding new benchmark surface area now would dilute the mechanism story

### F. Do not build a classifier now

Not now:

- no classifier training
- no threshold search
- no heavy routing policy work

Reason:

- image-level signals were weak
- object-level signals are promising, but not yet mature enough for a final selector claim

## 3. Current Recommended Sequence

1. finalize mechanism-oriented writing
2. preserve the claim boundary clearly
3. do only small evaluation-alignment or consistency cross-checks if needed
4. if momentum remains strong, design a very small object-local selective prototype later

## 4. Current Research Posture

Best current framing:

- `first_logit / early-anchor` is the strongest current mechanism candidate
- COCO-CHAIR is the main positive result line
- POPE is retained for answer-boundary signal audit
- coarse image-level selective gating is not supported
- future selectivity, if any, should be object-token-level rather than image-level
