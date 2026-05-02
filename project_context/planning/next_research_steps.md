# Next Research Steps

> Date: 2026-05-02
> Scope: next-stage priorities after full COCO-CHAIR confirmation, near-official alignment, middle-layer mechanism audit, and the completed negative guard-family follow-ups.

## 1. Current Baseline To Keep Fixed

Active main method candidate:

- full `fixed first_logit / early-anchor`

Why:

- it remains the strongest current COCO-CHAIR result
- no guard-family follow-up has beaten it on the `1000` pilot
- its positive full-result story already has evaluator-alignment and mechanism support

## 2. Priority Order

### A. First: solidify Early-Anchor Decoding

Immediate focus:

- lock fixed `first_logit / early-anchor` as the current main method candidate
- consolidate the positive result story across:
  - full COCO-CHAIR
  - near-official evaluator alignment
  - POPE protocol interpretation
  - object-level and middle-layer mechanism evidence
- make the negative guard-family results explicit so they stop competing for the main line

### B. Second: do external baseline alignment

Next validation focus:

- align the current main result against stronger external or published baseline surfaces where feasible
- improve confidence that the current gain is meaningful beyond the internal regular-vs-first-logit comparison
- keep this as validation work, not a new method-search branch

### C. Third: do stability and cross-setting validation

Next empirical focus:

- test whether the fixed early-anchor result remains stable across nearby settings
- prioritize robustness checks over inventing another suppression rule
- keep pilot discipline strict:
  - require `1000`-image checks before any new full expansion
  - require no first-word drift
  - require no empty captions
  - require no object-mention or correct-object collapse

### D. Fourth: pause token-level guard and object-suppression work

Stop here:

- no more token-level boost clipping variants
- no more broad object-suppression variants
- no more broad anchor-cleaning guard variants
- no threshold sweep for the failed guard family

Why:

- `object_safe_anchor`
- `attention_gated_attnanchor`
- `candidate_local_guard`
- `middle_verified`
- `middle_refined`

all fail to beat fixed `first_logit`, and the shared failure mode is still object-mention and correct-object collapse.

### E. Fifth: only revisit new selective methods with stronger mechanism grounding

If method work resumes later:

- only consider trajectory-level or phrase-level ideas if there is fresh mechanism evidence that clearly justifies them
- prefer a genuinely different unit of action over another broad suppression rule
- do not resume guard-family expansion by default

## 3. Explicit Pauses

Not now:

- no `gamma / lambda / cd_beta` sweep
- no threshold search
- no classifier training
- no new benchmark branch such as POPE / AMBER / MME expansion for this method question
- no continuation of the current token-level guard family

## 4. Current Recommendation

1. keep full fixed `first_logit / early-anchor` as the active main baseline and main method candidate
2. consolidate all failed guard-family results into one clear negative evidence chain
3. spend the next cycle on result solidification, external alignment, and stability checks
4. only revisit new selective methods if the next mechanism evidence clearly supports a different, more local action unit
