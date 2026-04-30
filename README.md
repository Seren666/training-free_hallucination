# training-free_hallucination

This repository is the lightweight paper-facing workspace for the new training-free LVLM object hallucination project.

Current focus:

- task: object hallucination
- initial benchmark: POPE
- first-priority baseline: FLB / first-logit
- current stage: migration, environment inventory, and planning only

Repository rules:

- keep `object_hallucination_research_notes.md` as the living research note
- keep legacy VCD findings only as lightweight summaries under `project_context/legacy_handoff/`
- do not store models, datasets, raw outputs, cache, or large logs in this repository
- run heavy baseline cloning, downloads, and experiments on the remote machine only

Main structure:

- `object_hallucination_research_notes.md`: current living research note
- `project_context/legacy_handoff/`: legacy VCD summaries, remote paths, and run-command provenance
- `project_context/planning/`: current planning documents
- `project_context/remote/`: remote environment inventory
- `project_context/literature/`: official paper/code link notes
- `project_context/baseline_notes/`: lightweight baseline run summaries when experiments begin

