# Early-Anchor Main Method Candidate

> Date: 2026-05-02
> Scope: why fixed `first_logit / early-anchor` is the current main method candidate.

## 1. Main Result

Current strongest method:

- fixed `first_logit / early-anchor`

On full COCO-CHAIR:

- `regular`: `CHAIRs 0.2037`, `CHAIRi 0.0655`
- `fixed first_logit`: `CHAIRs 0.1631`, `CHAIRi 0.0513`

Other full-result properties:

- hallucinated objects decrease from `11875` to `9609`
- average caption length increases from `49.6823` to `50.9320`
- object mentions increase from `181268` to `187440`
- first word changed remains `0`
- `The effect` was not used

This means the gain is not coming from shorter captions or fewer object mentions.

## 2. Near-Official Alignment

The result survives a near-official evaluator check.

Full-set alignment:

- adapted evaluator:
  - `regular`: `0.2037 / 0.0655`
  - `first_logit`: `0.1631 / 0.0513`
  - delta: `-0.0406 / -0.0142`
- near-official evaluator:
  - `regular`: `0.1997 / 0.0669`
  - `first_logit`: `0.1594 / 0.0524`
  - delta: `-0.0403 / -0.0145`

Interpretation:

- direction matches
- magnitude matches closely
- the current positive result is not an artifact of the adapted evaluator

## 3. Why POPE Gave Delta = 0

POPE is still informative, but not as the main later-step intervention benchmark.

Observed result:

- faithful later-step `first_logit` gave `delta = 0` on all `9/9` POPE splits

Protocol explanation:

- POPE is essentially a one-word yes/no answer-boundary task
- the answer is usually determined at the first generated answer token
- later-step anchor injection has little or no room to act

Interpretation:

- POPE should be kept as an answer-boundary signal audit benchmark
- it should not be used as the main score surface for later-step early-anchor decoding

## 4. Mechanism Support From Middle-Layer and Object-Level Audit

The mechanism story is no longer only metric-level.

Full paired event table:

- `removed_hallucination = 6043`
- `introduced_hallucination = 3880`
- `persistent_hallucination = 3924`
- `correct_object_mention = 86458`

Useful separating signals:

- removed vs introduced:
  - `adjusted_target_rank_if_applied`
  - `anchor_target_token_rank`
- hallucinated vs correct:
  - `anchor_weight_at_object_step`
  - `mention_position_ratio`
  - `anchor_target_token_rank`

Middle-layer support:

- introduced vs correct:
  - `middle_target_rank_mean: 6098.926 vs 3533.189`
  - `image_attention_middle_mean: 0.145080 vs 0.183550`
  - `middle_target_probability_mean: 0.071635 vs 0.144712`
- introduced vs removed:
  - `anchor_adjustment_delta: 1.151627 vs 0.978613`
  - `adjusted_target_rank_if_applied: 1.021 vs 1.467`

Interpretation:

- early-anchor likely provides a useful grounding prior
- later object-token outcomes depend on whether that prior aligns with stronger middle-layer evidence

## 5. Why It Is The Current Main Method Candidate

Why fixed `first_logit / early-anchor` currently leads:

- it is the only method with a stable positive result from pilot to full COCO-CHAIR
- it remains positive under near-official alignment
- it does not win by shrinking caption content
- it has a plausible object-level and middle-layer mechanism story
- every current follow-up guard family fails to beat it

Negative follow-ups that did not replace it:

- `object_safe_anchor`
- `attention_gated_attnanchor`
- `candidate_local_guard`
- `middle_verified`
- `middle_refined`

So the right current posture is:

- keep fixed `first_logit / early-anchor` as the main method candidate
- stop treating guard-family follow-ups as likely replacements

## 6. Current Claim Boundary

What we can claim now:

- this is a promising decoding-time method candidate
- it has stable positive evidence on full COCO-CHAIR
- the result is not explained by evaluator mismatch
- the mechanism story has object-level and middle-layer support

What we should not claim now:

- not a final paper method yet
- not SOTA
- not universal hallucination mitigation
- not validated across all settings
- not backed by a successful selective runtime controller

## 7. What Validation Is Still Missing

Most important next validations:

- stronger external baseline alignment
- stability checks across seeds or closely related decoding settings
- cross-setting verification that preserves the same main trend
- clearer comparison against external or published baseline surfaces where feasible

Still not needed right now:

- more token-level guard variants
- more broad object suppression variants
- another threshold sweep
- classifier training

## 8. Current Recommendation

- lock fixed `first_logit / early-anchor` as the active main method candidate
- consolidate the failed guard family as negative evidence
- move the next phase toward validation and external alignment rather than another guard search
