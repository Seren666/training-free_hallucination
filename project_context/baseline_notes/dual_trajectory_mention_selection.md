# Dual-Trajectory Mention Selection

> Date: 2026-05-02
> Scope: offline feasibility for a caption-level dual-trajectory fallback rule between existing `regular` and fixed `first_logit` COCO-CHAIR captions.

## 1. Why token-level guards failed

- fixed `first_logit / early-anchor` remains the strongest current decoding baseline on full COCO-CHAIR
- `Object-Safe Early Anchor`, `Attention-Gated AttnAnchor`, and `Candidate-Object Local Guard` all stayed inside the token-level boost-clipping frame
- all three selective pilots reduced some hallucinations but also hurt correct object mentions
- this suggests the next useful route should not be broader or narrower token suppression inside the same runtime formula

## 2. Why mention-level selection

The dual-trajectory idea was the cleanest framework shift:

- keep the existing full `regular` captions
- keep the existing full fixed `first_logit` captions
- do not edit phrases
- do not regenerate captions
- only decide which full caption is more trustworthy per image

The hoped-for advantage was:

- avoid suppressing valid object tokens inside a single trajectory
- use mention-local support only when `first_logit` adds new object mentions relative to `regular`
- fall back to `regular` only on suspicious `first_logit-only` additions

## 3. Offline feasibility

Remote outputs:

- `/root/autodl-tmp/code/training_free_hallucination_probe/results/dual_trajectory_mention_feasibility.md`
- `/root/autodl-tmp/code/training_free_hallucination_probe/results/dual_trajectory_mention_feasibility.csv`

Feasibility used:

- full paired captions
- `object_event_table.csv`
- existing `object_local_signal_probe.csv` 4000-event subset

The probe subset split into:

- `first_only_hallucinated = 1000`
- `first_only_correct = 63`
- `regular_only_hallucinated = 1000`
- `regular_only_correct = 112`
- `common_hallucinated = 1000`
- `common_correct = 825`

Unsupervised thresholds from the full 4000-event probe:

- `middle_image_attention_mean p25 = 0.132100`
- `hidden_image_cosine_middle_mean p25 = 0.226665`
- `mention_position_ratio p75 = 0.812500`
- `anchor_target_token_rank p75 = 10508.0`

Critical comparison: `first_only_hallucinated` vs `first_only_correct`

- `anchor_target_token_rank`: `abs(AUC-0.5) = 0.1323`
- `anchor_adjustment_delta`: `abs(AUC-0.5) = 0.1035`
- `mention_position_ratio`: `abs(AUC-0.5) = 0.0675`
- `image_attention_middle_mean`: `abs(AUC-0.5) = 0.0465`
- `hidden_image_cosine_middle_mean`: `abs(AUC-0.5) = 0.0313`
- `hidden_image_cosine_late_mean`: `abs(AUC-0.5) = 0.0282`

Main reading:

- pure visual-support separation for the actual rollback target is weak
- `middle_image_attention_mean` moves in the expected direction, but only slightly
- hidden-image cosine is weaker than hoped for this route
- `mention_position_ratio` and `anchor_target_token_rank` are somewhat more directional than pure visual support
- this is meaningfully weaker than the earlier object-local mechanism evidence for `hallucinated` vs `common correct`

## 4. Selection rule

Planned minimal rule before stopping:

- default choose fixed `first_logit`
- inspect `first_logit-only` object mentions
- mark a mention as risky only under a conservative weak-support condition
- switch to `regular` only if weak `first_logit-only` mentions dominate and `regular` does not look equally risky from caption-difference counts

The most defensible weak-support candidate after feasibility was:

- `middle_image_attention_mean < p25`
- and `mention_position_ratio >= p75`

Not chosen:

- pure `middle attention` alone, because separation was too weak
- pure hidden cosine, because it was weaker still

## 5. Threshold source

All thresholds were unsupervised and came from the existing 4000-event object-local probe distribution:

- no CHAIR labels were used to set thresholds
- no improved/worsened labels were used to set thresholds
- no threshold sweep was run

## 6. Selected caption evaluation

Not run.

Reason:

- the feasibility signal for the actual rollback target, `first_logit-only hallucinated` vs `first_logit-only correct`, was too weak to justify a full-dataset fallback simulation
- the user instruction for this route explicitly said to stop if mention-level support showed no useful distinction

I did prepare the necessary runtime-safe candidate pool:

- `first_logit-only` mentions in full event table: `9378`
- corresponding images: `7542`
- `regular-only` mentions: `15686`
- `regular-only` images: `12126`

I also verified that the existing probe pipeline can score these mentions without new generation:

- `20`-mention sanity probe ran successfully
- estimated full runtime was on the order of `6` hours for all `9378` first-only mentions

Given the weak first-only separation, that long run was not justified.

## 7. Comparison with earlier routes

Compared with the negative token-level guards:

- this route is cleaner conceptually
- it avoids runtime token suppression
- it keeps both captions intact

But compared with the evidence needed to trust it:

- the decisive `first_only hallucinated vs first_only correct` signal is weaker than needed
- the best separating features in feasibility were not the pure visual-support features the rollback rule wanted to rely on

## 8. Behavior analysis

Full selected-caption behavior analysis was not run because selected full captions were not built.

The useful feasibility-level behavior takeaway is:

- `common_hallucinated` vs `common_correct` still shows clear separation
- but that is not the real decision boundary for dual-trajectory rollback
- the real rollback boundary is the `first_only` split, and that split is much noisier

## 9. Whether it beats fixed first_logit

Not tested, because selected captions were not constructed.

Current judgment:

- this simple caption-level fallback rule is not sufficiently supported by the current first-only visual-support evidence
- it should not be treated as a promising next full method in its current form

## 10. Failure cases

The core failure mode is structural:

- `first_logit-only hallucinated` and `first_logit-only correct` are too close under the simple support signals that a caption-level rollback would need
- a rollback rule would then either switch too rarely to matter
- or switch often enough to matter but throw away valid `first_logit` additions

This is not a "bug in implementation" failure.
It is a "signal is not sharp enough for this coarse decision granularity" failure.

## 11. Whether to continue this route

Current recommendation:

- do not continue simple caption-level dual-trajectory rollback as the next main method line
- do not launch full selected-caption evaluation from the current weak-support rule

If dual-trajectory work continues later, it should likely move toward:

- phrase-level or mention-level verification rather than whole-caption fallback
- richer support checks than the current simple visual-support threshold
- possibly a more explicit compare-and-select between matched mentions rather than a single caption-level switch

## 12. Caveats

- the existing object-local probe was stratified by event type, so `first_only_correct` is only `63` rows inside the current 4000-event subset
- that means the critical first-only feasibility slice is underpowered
- so this should be read as "not enough support to justify the full selection run", not as a proof that dual-trajectory ideas are impossible
- if this family is revisited, the first thing to improve is the first-only support audit itself, not the fallback threshold
