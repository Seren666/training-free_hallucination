# LLaVA Selected Vs Broad Signal Note

## Why this note exists

The original LLaVA retained-branch verifier uses a compact subset of signals. Recent Version A and Version A+ audits exposed many broader candidate signals. This note explains why the original score stayed small and why adding more signals is not automatically better.

## Signals used by the original LLaVA score

The original weighted verifier keeps a compact, mechanistic subset:

Core evolution / mismatch:
- `middle_x_mass_change`
- `mass_change_late_minus_mid`
- `middle_to_late_image_attention_delta`
- `anchor_masschange_x_late_mass`
- `firstlogitgap_x_verification_masschange`

Anchor support:
- `anchor_target_token_rank`

Verification rescue:
- `image_attention_middle_mean`
- `middle_target_probability_mean`

Late recovery / persistence rescue:
- `late_image_attention_recovery_ratio`
- `middle_to_late_prob_jump`
- `top_minus_random_logit_drop`
- `sensitivity_ratio_prob`

These are the signals actually frozen into the retained-branch scoring path.

## Signals discovered later but not used in the original LLaVA score

Broader later audits surfaced additional useful columns, including examples such as:
- `first_logit_hallucinated_object_count`
- `object_query_position`
- `prefix_length_tokens`
- `mention_position_ratio`
- `probe_mention_word_index`

Version A+ also considered broader families such as:
- extra mention-structure signals
- extra source / trajectory indicators
- extra position or prompt-layout cues
- more model-specific auxiliary features

These were not part of the original LLaVA retained-branch score.

## Why adding broader signals can hurt ranking

Recent A+ comparison gives a concrete warning sign:
- original Version A LLaVA retrospective result: `AUROC/AP = 0.748452 / 0.343287`
- Version A+ retrospective result reported in the appendix: `AUROC/AP = 0.687533 / 0.276979`
- readiness also softened from `action-ready` to `action-promising`

Why broader signals can degrade a frozen ranking:
- extra columns may be correlated but not mechanistically clean
- some signals are useful only in specific models, positions, or source groups
- mixed or inverted priors can dilute a stable core
- more columns increase the chance that weak but abundant cues overpower the cleaner ones

The single-signal audit explicitly shows that not all intuitively relevant signals are stable in LLaVA. Some broad candidates are mixed or harmful under a fixed prior.

## Why compact stable subsets are preferred

The original LLaVA score appears intentionally compact for four reasons:
- the retained signals are low-missingness and operationally available
- they are relatively interpretable as risk / rescue mechanisms
- they remain usable across source / position / category analyses
- they are easier to freeze and reuse across full-table correction scripts

In other words, the compact score is not “small because evidence was unavailable.” It is small because a narrow stable subset was easier to freeze into a robust training-free pipeline.

## How Version A relates to the original LLaVA score

Version A is a cross-model framework extension, not the definition of the original LLaVA retained-branch verifier.

Original LLaVA score:
- model-specific
- hand-designed
- compact
- frozen into retained-branch scripts

Version A:
- cross-model
- percentile-normalized
- block-based
- designed to adapt when signal direction differs by model

So the right interpretation is:
- the original LLaVA score is the validated frozen heuristic for LLaVA retained branches
- Version A is a later framework-level generalization motivated by cross-model portability limits

## Bottom line

The original LLaVA score uses a compact stable subset of signals on purpose. Broader signal families can add descriptive evidence, but they can also weaken ranking quality when folded into a frozen action score. This is why the retained LLaVA verifier should be described as a compact hand-designed heuristic, not as an all-signals or universally optimal formula.
