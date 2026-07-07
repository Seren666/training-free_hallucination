# Artifact Inventory

This inventory records the public commit policy used for this repository cleanup.

## Committed Public Artifacts

| Path | Type | Commit? | Reason | Large/raw/private? | Aggregate metrics? |
| --- | --- | --- | --- | --- | --- |
| `README.md` | documentation | yes | public entry point | no | summary only |
| `docs/method_overview.md` | documentation | yes | explains the method without private manuscript text | no | no |
| `docs/experiment_protocol.md` | documentation | yes | states benchmark/model/protocol boundaries | no | no |
| `docs/result_analysis.md` | documentation | yes | summarizes supported results and caveats | no | yes |
| `docs/limitations.md` | documentation | yes | prevents overclaiming | no | no |
| `docs/resume_bullets.md` | documentation | yes | gives honest resume wording | no | summary only |
| `docs/research_positioning.md` | documentation | yes | connects the project to long-term research interests | no | no |
| `docs/technical_report.md` | documentation | yes | compact public report | no | yes |
| `results/public/caption_side_results.csv` | aggregate metrics | yes | main public result record | no | yes |
| `results/public/external_baselines.csv` | aggregate metrics | yes | caveated external baseline record | no | yes |
| `results/public/runtime_summary.csv` | aggregate metrics | yes | runtime overhead record | no | yes |
| `results/public/result_table.md` | generated table | yes | human-readable table generated from public CSVs | no | yes |
| `src/hallucination_mitigation/` | source code | yes | non-sensitive bounded-edit and scoring utilities | no | no |
| `scripts/make_tables.py` | script | yes | regenerates Markdown tables from public CSVs | no | no |
| `scripts/check_repo_hygiene.py` | script | yes | checks size, secret, and forbidden artifact policy | no | no |
| `tests/` | tests | yes | verifies lightweight utility behavior | no | no |

## Not Committed

| Pattern | Reason |
| --- | --- |
| raw generations and JSONL outputs | large and model/data dependent |
| model weights, checkpoints, `.pt`, `.pth`, `.safetensors`, `.bin` | too large and not redistributable |
| datasets and annotation dumps | external licensing and size concerns |
| private manuscript TeX/PDF/Overleaf exports | not part of the public repository |
| remote-machine runbooks with hosts, ports, or user accounts | not needed for public reproduction |
| huge logs, cache folders, `__pycache__`, `wandb`, tensorboard runs | not useful for public review |

## Source Of Public Metrics

The public CSVs were derived from local aggregate artifacts already present in the research workspace:

- `results/ocv_source_specific_expanded_table_final_v2.csv`
- `results/external_baseline_consolidated_score_table.csv`
- `results/ocv_runtime_microbenchmark_final.csv`

Only small aggregate rows were copied into this repo. Raw captions, evaluator caches, and model-specific private paths were not copied.
