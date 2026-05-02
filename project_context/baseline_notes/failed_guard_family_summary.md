# Failed Guard Family Summary

> Date: 2026-05-02
> Scope: why the guard-family follow-ups do not replace fixed `first_logit / early-anchor`.

## 1. Setup

Starting point:

- fixed `first_logit / early-anchor` is the current best decoding baseline on COCO-CHAIR
- it improves both `CHAIRs` and `CHAIRi`
- it does not win by shortening captions, reducing object mentions, or changing the first generated token

The failed follow-up family tried to reduce introduced hallucinations by suppressing object support in different ways:

- flat object-token suppression
- step-level attention gating
- top-k candidate clipping
- middle-layer verified token clipping
- anchor-construction cleaning

## 2. Object-Safe

Definition:

- scale down all positive boosts on the object-token vocabulary

Why it looked promising:

- raw hallucinated object count dropped from `240` to `224`

Why it failed:

- `CHAIRs` worsened from `0.1610` to `0.1620`
- `CHAIRi` worsened from `0.0509` to `0.0530`
- object mentions dropped by `489`
- correct object mentions dropped by `473`

Interpretation:

- flat object-vocab suppression is too blunt
- it removes too many valid object mentions together with some hallucinations

## 3. Attention-Gated

Definition:

- on low-attention steps, suppress positive object-token boosts

Why it looked promising:

- it was more selective than flat `Object-Safe` in the offline story

Why it failed:

- `CHAIRs` worsened to `0.1680`
- `CHAIRi` worsened to `0.0575`
- hallucinated object count worsened to `249`
- object mentions dropped by `388`
- correct object mentions dropped by `397`
- removed hallucinations (`60`) did not outnumber introduced hallucinations (`69`)
- average gate-trigger steps were about `44.315` per image

Interpretation:

- the runtime gate was still far too broad
- low-attention step gating is not local enough by itself

## 4. Candidate-Object Guard

Definition:

- only clip positive boosts among current top-k object candidates

Why it looked promising:

- it was much narrower than the previous attention gate
- gate-trigger steps dropped to about `10.938` per image

Why it failed:

- `CHAIRs` stayed at `0.1680`
- `CHAIRi` stayed worse than fixed at `0.0555`
- hallucinated object count stayed worse than fixed at `246`
- object mentions dropped by `286`
- correct object mentions dropped by `292`

Interpretation:

- narrowing to current top-k candidates helps, but not enough
- the clipping rule still removes too many helpful object pushes

## 5. Middle-Verified

Definition:

- clip later-step positive object boosts only when middle-layer verification is weak

Why it looked promising:

- the middle-layer audit gave real mechanism support
- correct mentions are stronger in middle-layer rank and attention

What improved:

- this was the healthiest clipping pilot on mention preservation
- object mentions delta vs fixed improved to `-72`
- correct object mentions delta vs fixed improved to `-90`
- gate-trigger steps dropped to about `3.932` per image

Why it still failed:

- `CHAIRs` worsened to `0.1770`
- `CHAIRi` worsened to `0.0555`
- hallucinated object count worsened to `258`
- removed hallucinations (`18`) were outnumbered by introduced hallucinations (`36`)

Interpretation:

- middle-layer verification is useful as an audit surface
- but turning it into token-level later-step clipping still does not beat fixed `first_logit`

## 6. Middle-Refined

Definition:

- clean the anchor once at construction time instead of clipping later decode steps

Why it looked promising:

- offline feasibility was much cleaner than flat `Object-Safe`
- introduced flag rate was `0.254`
- correct flag rate was only `0.102`

Why it still failed:

- `CHAIRs` worsened to `0.1640`
- `CHAIRi` worsened to `0.0541`
- object mentions dropped by `450`
- correct object mentions dropped by `441`
- even though raw hallucinated object count improved to `231`
- step0 low-attention fired on `97.8%` of images
- average refined object tokens per image was `141.93`

Interpretation:

- this is a more meaningful new family than token-level clipping
- but the current rule still broadens into source-level object suppression
- moving the intervention earlier is not enough if the rule is still broad

## 7. Shared Failure Pattern

Across the whole guard family:

- some variants reduce raw hallucinated-object count slightly
- none improve the main `CHAIRs / CHAIRi` result over fixed `first_logit`
- the recurring cost is object mention collapse
- the deeper recurring cost is correct object mention collapse

Common pattern by family:

- `Object-Safe`: very broad vocabulary-level suppression
- `Attention-Gated`: broad step-level suppression
- `Candidate-Object Guard`: narrower, but still suppresses helpful pushes
- `Middle-Verified`: healthier clipping, but still perturbs the fixed trajectory
- `Middle-Refined`: earlier intervention point, but still broad source suppression

## 8. Conclusion

- do not continue token-level boost clipping expansion
- do not continue broad object suppression
- do not continue broad anchor-cleaning guard expansion
- keep fixed `first_logit / early-anchor` as the current main method candidate
- treat the failed guard family as useful negative evidence about what not to do next

## 9. What The Negative Results Still Teach Us

- middle-layer signals are mechanistically meaningful
- image-level scalars are too coarse
- object-local evidence matters
- but a signal that is good for audit is not automatically good for runtime suppression
- future follow-up work, if any, should move to a different unit of action rather than another variant of broad guard-based suppression
