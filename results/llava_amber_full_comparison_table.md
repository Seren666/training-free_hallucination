# LLaVA AMBER Full Comparison Table

Setup:

- dataset: AMBER full generative
- sample count: `1004`
- token budget: `max_new_tokens = 128`
- note: this is a verified read-only refresh of existing outputs, not a rerun

| Method | CHAIR | Cover | Hal | Cog | Delta vs regular | Delta vs fixed / FLB-equiv | Role / interpretation |
|---|---:|---:|---:|---:|---|---|---|
| `regular` | 7.0 | 50.5 | 32.3 | 3.8 | baseline | `CHAIR +2.2`, `Cover +1.7`, `Hal +7.8`, `Cog +1.6` | raw LLaVA baseline |
| fixed / FLB-equivalent | 4.8 | 48.8 | 24.5 | 2.2 | `CHAIR -2.2`, `Cover -1.7`, `Hal -7.8`, `Cog -1.6` | baseline | improved generation-control baseline |
| `firstlogit_removal_top10` | 4.7 | 48.7 | 23.7 | 2.0 | `CHAIR -2.3`, `Cover -1.8`, `Hal -8.6`, `Cog -1.8` | `CHAIR -0.1`, `Cover -0.1`, `Hal -0.8`, `Cog -0.2` | lowest `Hal/Cog`, but more aggressive |
| `dual_phrase_replace_v1` | 4.7 | 48.8 | 24.0 | 2.1 | `CHAIR -2.3`, `Cover -1.7`, `Hal -8.3`, `Cog -1.7` | `CHAIR -0.1`, `Cover +0.0`, `Hal -0.5`, `Cog -0.1` | quality-preserving retained branch |
| `removal_top10_firstlogit_only_guard` / Candidate A | 4.7 | 48.8 | 23.9 | 2.1 | `CHAIR -2.3`, `Cover -1.7`, `Hal -8.4`, `Cog -1.7` | `CHAIR -0.1`, `Cover +0.0`, `Hal -0.6`, `Cog -0.1` | safer source-aware removal branch |

## Interpretation

- fixed / FLB-equivalent clearly improves over regular on full AMBER
- the retained branches provide small additional gains over fixed / FLB-equivalent
- `dual_phrase_replace_v1` and Candidate A preserve `Cover` relative to fixed / FLB-equivalent
- `firstlogit_removal_top10` has the lowest `Hal` and `Cog`, but it is the more aggressive retained diagnostic
- the AMBER full result supports cross-dataset evidence for the framework, but it does not replace the main COCO-CHAIR result
