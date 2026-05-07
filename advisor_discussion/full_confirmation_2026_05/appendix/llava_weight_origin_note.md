# LLaVA Weight Origin Note

## Purpose

This appendix records the provenance of the current LLaVA weighted verifier so that the paper can describe it accurately as a training-free heuristic rather than a label-trained scorer.

## What was audited

Audited files include:
- `.codex_tmp_remote/analyze_weighted_evidence_consistency.py`
- `.codex_tmp_remote/second_pass_correction_action_pilot.py`
- `.codex_tmp_remote/strict_second_pass_action_matrix_pilot.py`
- `.codex_tmp_remote/regular_source_risk_full_remote.py`
- `.codex_tmp_remote/correction_expanded_confirmation.py`
- `results/high_risk_mentions_firstlogit_full.csv`
- `.codex_tmp_remote/weighted_remote_results/weighted_evidence_score_definitions.csv`
- `.codex_tmp_remote/weighted_remote_results/weighted_evidence_consistency_summary.md`

## Audit conclusion

- The LLaVA weighted verifier is training-free.
- The score families and weights are hand-designed and hard-coded.
- Runtime scoring does not fit weights from CHAIR labels.
- Full-scale `40504` COCO-CHAIR results reuse the frozen weighted verifier and frozen top-quantile action slices.
- Later appendix follow-ups do not show post-hoc score reweighting for the retained branches.

## Formula summary

The retained-branch path uses four main weighted family scores:
- `global_weighted_evidence_score`
- `introduced_focused_weighted_score`
- `persistent_focused_weighted_score`
- `removed_focused_weighted_score`

Each family is a fixed weighted average of aligned internal signals. `risk` signals keep their sign; `rescue` signals are sign-flipped. The main routing score is:
- `primary_risk_score = max(family scores)`

Operating slices are frozen quantiles:
- `top5 = 95th percentile`
- `top10 = 90th percentile`
- `top20 = 80th percentile`

## Label usage

- CHAIR labels are used for retrospective signal analysis and final evaluation.
- They are not used inside the retained-branch runtime score formula.
- Runtime normalization may use reference feature mean / std from an existing signal table, but this is not supervised weight fitting.

## Provenance interpretation

The safest interpretation is:
- signal families were manually assembled from earlier signal-direction audits
- weights were manually assigned and frozen
- full-scale experiments validate the frozen method rather than train it

## Relation to broader calibration work

Later cross-model work shows that broader or model-adaptive scoring can be useful, but it does not retroactively redefine the original LLaVA retained-branch verifier. The retained LLaVA branches remain unchanged, and no final branch selection has been finalized.

## Paper-safe wording

Recommended wording:

`We use a training-free, hand-designed weighted mention-level verifier built from internal uncertainty, attention, and mismatch signals. The verifier uses fixed heuristic weights and fixed quantile operating slices; CHAIR labels are used only for retrospective analysis and evaluation, not for score fitting.`
