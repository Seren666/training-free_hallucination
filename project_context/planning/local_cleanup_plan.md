# Local Cleanup Plan

> Status: planning only. No files have been deleted or moved by this plan.
> Goal: shrink the repository to a lightweight paper-facing workspace without losing useful legacy context.

## Current top-level snapshot

Current local top-level entries:

- `.claude/`
- `docs/`
- `experiments/`
- `project_context/`
- `reports/`
- `与导师交流/`
- `EXPERIMENT_ARTIFACT_POLICY.md`
- `MAIN_IDEA.md`
- `idea01.md`
- `idea02.md`
- `object_hallucination_research_notes.md`
- `references.md`

## A. 必须保留

These items should remain available in the new project, either in place or already organized under `project_context/`:

- `object_hallucination_research_notes.md`
- `project_context/legacy_handoff/legacy_handoff_for_new_project.md`
- `project_context/legacy_handoff/legacy_vcd_final_results/pope_final_results.md`
- `project_context/legacy_handoff/legacy_vcd_final_results/mme_final_results.md`
- `project_context/legacy_handoff/legacy_vcd_final_results/dominance_line_summary.md`
- `project_context/legacy_handoff/legacy_vcd_final_results/step0_observation_summary.md`
- `project_context/legacy_handoff/legacy_environment/remote_paths.md`
- `project_context/legacy_handoff/legacy_environment/model_dataset_paths.md`
- `project_context/legacy_handoff/legacy_environment/run_commands.md`
- `project_context/legacy_handoff/cleanup_notes.md`
- new planning files under `project_context/planning/`
- the remote inventory under `project_context/remote/`

## B. 可归档到 `project_context/legacy_handoff/`

These items are potentially valuable, but they are no longer the main paper line. They are better treated as archived context than as root-level project files.

- `EXPERIMENT_ARTIFACT_POLICY.md`
- `MAIN_IDEA.md`
- `idea01.md`
- `idea02.md`
- `references.md`
- `docs/superpowers/` old RAD-VCD design specs and implementation plans
- `reports/advisor_stage_summary.md`
- `reports/scmr_vcd_branch_note.md`
- `reports/SCMR_VCD_stage_report.md`
- `reports/mme_vcd_diff_summary.md`
- `reports/self_understanding_note.md`
- `experiments/path_gated_v1/` lightweight old experiment summaries
- all markdown and PDF files under `与导师交流/`

Recommended archive rule:

- move only after checking that filenames still make sense in the new structure
- prefer markdown over PDF if both contain the same information
- keep a short index note if many archived files are moved together

## C. 可删除

These items look process-heavy, duplicated, or clearly outside the new repository scope.

- `.claude/` local assistant metadata
- `reports/_cache/llava15_cg2b3_seed55_scb_tyfl_mme.jsonl`
- `reports/_cache/mme_manifest.jsonl`
- generated helper scripts that only exist to build old reports:
  - `reports/generate_mme_vcd_diff_analysis.py`
  - `reports/generate_scmr_vcd_stage_report.py`
- derived JSON or intermediate analysis outputs such as:
  - `reports/mme_vcd_diff_analysis.json`
- duplicate advisor PDFs under `与导师交流/*.pdf` once the corresponding markdown is archived or confirmed sufficient
- `experiments/path_gated_v1/**` if its useful conclusions are fully captured elsewhere

Important restriction:

- do not delete any of these until the archived summaries are confirmed sufficient

## D. 删除前需要用户确认

These should not be deleted without an explicit confirmation step:

- the entire `docs/` directory
- the entire `reports/` directory
- the entire `experiments/` directory
- the entire `与导师交流/` directory
- root idea documents:
  - `MAIN_IDEA.md`
  - `idea01.md`
  - `idea02.md`
  - `references.md`
  - `EXPERIMENT_ARTIFACT_POLICY.md`
- all PDF files under `与导师交流/`
- any file that is the only surviving copy of an advisor summary, old result summary, or provenance note

## Recommended cleanup order

When cleanup is approved later, the safest order is:

1. Archive useful markdown summaries into `project_context/legacy_handoff/`.
2. Confirm that old VCD final summaries, MME summaries, and remote path notes are all present.
3. Delete obvious cache/intermediate files.
4. Delete duplicate PDFs and temporary scripts.
5. Re-check `git status` before any large directory removal.

