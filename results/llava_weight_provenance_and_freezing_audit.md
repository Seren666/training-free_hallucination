# LLaVA Weight Provenance And Freezing Audit

## Short answer

The evidence supports a frozen, hand-designed LLaVA verifier rather than a label-fit verifier. Full-scale `40504` evaluations appear to reuse the same weighted families and the same quantile action slices rather than re-tuning them on full labels.

## 1. Were the weights manually designed

Yes.

Evidence:
- `.codex_tmp_remote/analyze_weighted_evidence_consistency.py` declares `SCORE_SPECS` with explicit feature lists, weights, `risk` / `rescue` alignment, and human-readable reasons.
- `.codex_tmp_remote/weighted_remote_results/weighted_evidence_score_definitions.csv` mirrors those choices as a definition table.

## 2. Were they chosen from signal direction analysis

Yes, in the heuristic sense.

The score definitions are written as signal-family hypotheses:
- global evolution / mismatch
- introduced-focused mismatch
- persistent-focused anchor risk with rescue
- removed-focused recovery / over-mention evolution

The companion analysis file `.codex_tmp_remote/weighted_remote_results/weighted_evidence_consistency_summary.md` compares these hand-built families against:
- best single signals
- older composite signals
- category / position / source robustness
- multi-seed retrospective performance

This supports the interpretation that weights were chosen from prior signal audits and then retrospectively validated, not fitted by supervised optimization.

## 3. Were labels used to fit weights

No evidence was found that labels were used to fit the retained-branch weighted score.

What the audited scoring scripts do:
- fixed hard-coded components
- fixed hard-coded weights
- z-score normalization
- fixed risk / rescue sign handling
- fixed `max` routing across score families
- fixed top `5%` / `10%` / `20%` quantile slices

What they do not do:
- gradient-based fitting
- logistic-regression fitting
- tree fitting
- hyperparameter search
- label-driven weight search

## 4. Were labels only used for retrospective evaluation

Mostly yes, with one important nuance.

Retrospective label use:
- AUC / PR-AUC reporting
- robustness summaries
- quality / action outcome audits
- full CHAIR and AMBER evaluation

Nuance:
- `second_pass_correction_action_pilot.py` uses `mention_verification_signal_table.csv` to compute reference mean / std for z-score normalization.
- This uses the signal table as a reference distribution, not as a label-fitting step.
- The runtime weighted score does not branch on CHAIR labels and does not estimate weights from them.

## 5. Was full 40504 used to tune weights, or only to evaluate frozen methods

The evidence supports: full `40504` was used to evaluate frozen methods.

Evidence:
- `.codex_tmp_remote/regular_source_risk_full_remote.py` explicitly says: `Reuse the existing weighted training-free verifier exactly as-is.`
- `.codex_tmp_remote/correction_expanded_confirmation.py` imports and reuses `derive_weighted_scores`.
- `results/high_risk_mentions_firstlogit_full.csv` contains the same family scores and top-risk flags, indicating the same scorer was carried to full scale.

I did not find evidence that the full table was used to refit the weighted families.

## 6. When were top10 / top20 choices introduced

They were already present in the 1000-scale weighted action path, before the full archived comparison.

Evidence:
- `.codex_tmp_remote/second_pass_correction_action_pilot.py` defines:
  - top5 = 95th percentile
  - top10 = 90th percentile
  - top20 = 80th percentile
- `results/high_risk_mentions_firstlogit_1000_summary.md` already reports top10 threshold and top10 slice statistics.

## 7. Was top10 chosen before full diagnostic

Yes.

The strongest wording evidence is:
- `.codex_tmp_remote/score_first_correction_confirmation.py` writes `top10 remains the preregistered default slice`

Later full-scale anatomy confirms the same frozen choice:
- `results/risk_family_rescue_action_anatomy.md` says the existing full curve still supports `top10` as the default compromise, while `top20` remains diagnostic only.

This is consistent with:
- top10 being introduced before full confirmation
- full analysis being used to validate the frozen choice rather than invent it afterward

## 8. Were retained branches modified after full confirmation

No evidence was found that later follow-ups changed the weighted score formula or demoted / renamed the retained branches after full confirmation.

What later notes show:
- appendix follow-ups are additive
- additional candidates are marked diagnostic
- later FLB / AMBER / cross-model notes explicitly keep retained branches unchanged

Examples:
- `advisor_discussion/full_confirmation_2026_05/appendix/branch_full_result_archive.md`
- `advisor_discussion/full_confirmation_2026_05/appendix/candidate_A_diagnostic_note.md`
- `advisor_discussion/full_confirmation_2026_05/appendix/amber_baseline_followup_note.md`

Conservative wording:
- later diagnostics enriched the archive and tradeoff interpretation
- they did not show evidence of post-hoc score reweighting for the existing LLaVA retained branches

## 9. Which parts are heuristic and which are validated

Heuristic / hand-designed:
- signal subset selection
- risk vs rescue sign choice
- exact numeric weights
- family decomposition
- `primary_risk_score = max(family scores)`
- top `5%` / `10%` / `20%` quantile operating slices

Retrospectively validated:
- single-signal and composite comparisons
- robustness across source / position / category
- top-slice summaries
- 1000-scale action pilots
- full `40504` COCO-CHAIR evaluation
- near-official alignment checks
- AMBER follow-up checks

## Bottom line

The current evidence supports the paper-safe claim that the LLaVA weighted verifier is a frozen training-free heuristic whose weights were hand-designed and retrospectively validated. Full-scale results evaluate that frozen method family rather than a full-label-trained scorer.
