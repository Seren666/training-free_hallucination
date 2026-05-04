# Object Hallucination Research Notes

> Date: 2026-05-04
> Note: lightweight continuation created under `project_context/baseline_notes` because no existing project-context copy of the living note was present in this workspace.

## 11. Score-First Correction Confirmation Progress

- fixed `first_logit / early-anchor` remains the locked generation baseline
- the mention-level weighted training-free verifier remains the current main evidence source
- the correction line still keeps exactly two retained branches:
  - `firstlogit_removal_top10`
  - `dual_phrase_replace_v1`
- this round completed full confirmation rather than another expanded-only pass

Full confirmation summary:

- images: `40504`
- full weighted risk table:
  - mention rows: `84406`
  - images with mentions: `39606`
- adapted full metrics:
  - fixed `first_logit`: `CHAIRs=0.1631`, `CHAIRi=0.0513`
  - `firstlogit_removal_top10`: `CHAIRs=0.1291`, `CHAIRi=0.0413`
  - `dual_phrase_replace_v1`: `CHAIRs=0.1403`, `CHAIRi=0.0444`
- near-official full alignment preserved the same ordering:
  - `firstlogit_removal_top10` best raw score
  - `dual_phrase_replace_v1` second-best and more preservation-friendly

Current read:

- the `5000` expanded story survived full confirmation
- `firstlogit_removal_top10` is still the metric-strong branch
- `dual_phrase_replace_v1` is still the quality-preserving branch
- `top10` remains the preregistered default slice
- `top20` remains diagnostic only

Next gap:

- no immediate data gap remains for score-first full confirmation itself
- the next step should be synthesis / paper-facing discussion of the confirmed two-branch result, unless the user explicitly approves a new method-design round
