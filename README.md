# Training-Free Hallucination Mitigation

A lightweight research workspace for post-decoding, training-free mitigation of LVLM/VLM object hallucination.

This repository contains a sanitized public record of experiments around **Object Commitment Verification (OCV)**: a bounded post-decoding verifier that scores object mentions in generated captions and edits only high-risk unsupported commitments. The public repo focuses on aggregate metrics, reproducible tables, and non-sensitive utility code. It does not include model weights, datasets, raw generations, private manuscript files, or remote-machine credentials.

## For Quick Review

- [Headline result audit](docs/headline_result_audit.md): audited headline metrics and caveats.
- [Result analysis](docs/result_analysis.md): aggregate result interpretation.
- [Limitations](docs/limitations.md): limitations and non-claims.
- [Method overview](docs/method_overview.md): method overview.
- [Public result table](results/public/result_table.md): public result table.

## What Is Included

- Method notes: [docs/method_overview.md](docs/method_overview.md)
- Experiment protocol: [docs/experiment_protocol.md](docs/experiment_protocol.md)
- Public aggregate result tables: [results/public/](results/public/)
- Result analysis and limitations: [docs/result_analysis.md](docs/result_analysis.md), [docs/limitations.md](docs/limitations.md)
- Small utility package for bounded post-decoding edits and score aggregation: [src/hallucination_mitigation/](src/hallucination_mitigation/)
- Table generation and repository hygiene scripts: [scripts/](scripts/)

## Terminology

- **Regular**: original caption generation without post-decoding intervention.
- **FLB**: first-logit baseline, a decoding-stage baseline used in this workspace.
- **OCV**: Object Commitment Verification, the bounded post-decoding verifier used here.
- **CHAIRs / Hal / OpenCHAIR**: hallucination-oriented metrics where lower values are better.

## Best Supported Public Result

On COCO/CHAIR-500, InstructBLIP-7B CHAIRs decreases from 0.2360 under the first-logit decoding baseline to 0.1340 with OCV-on-FLB, a 43.2% relative reduction. This is an aggregate public result, not a SOTA or official benchmark claim.

## Key Caption-Side Results

Lower values are better for all hallucination metrics below. These are aggregate rows from completed local/remote experiment artifacts; raw generations and datasets are intentionally excluded.

| Model | Benchmark | Regular | FLB | OCV on FLB | Main delta vs FLB |
| --- | ---: | ---: | ---: | ---: | ---: |
| LLaVA-1.5-7B | COCO/CHAIR-500 CHAIRs | 0.1720 | 0.1560 | **0.1100** | 0.0460 lower |
| InstructBLIP-7B | COCO/CHAIR-500 CHAIRs | 0.2620 | 0.2360 | **0.1340** | 0.1020 lower |
| LLaVA-1.5-7B | AMBER-1004 Hal | 48.2 | 31.6 | **25.0** | 6.6 lower |
| InstructBLIP-7B | AMBER-1004 Hal | 59.0 | 52.5 | **48.4** | 4.1 lower |
| LLaVA-1.5-7B | OpenCHAIR | 0.1803 | 0.1621 | **0.1584** | 0.0036 lower |
| InstructBLIP-7B | OpenCHAIR | 0.1731 | 0.1731* | **0.1667** | 0.0065 lower |

`*` In this InstructBLIP OpenCHAIR run, the reproduced FLB source was regular-equivalent, so the FLB row is not evidence that FLB is generally ineffective.

The strongest clean headline row is the InstructBLIP COCO/CHAIR-500 setting: OCV on FLB source reduces CHAIRs from 0.2360 to 0.1340 relative to FLB and from 0.2620 to 0.1340 relative to regular generation.

## Reproduce Public Tables

The checked-in tables are generated from the small CSV files in `results/public/`:

```bash
python scripts/make_tables.py
```

Run basic repository checks:

```bash
python scripts/check_repo_hygiene.py
python -m unittest discover -s tests
```

Full benchmark reruns require user-provided LVLM checkpoints and benchmark data. Those artifacts are not redistributed here.

## External Baselines

The repository includes same-protocol or caveated external baseline summaries for VCD, AGLA, MaskCD, and DeCo in [results/public/external_baselines.csv](results/public/external_baselines.csv). They are kept separate from the main OCV table because several reproduced baselines have protocol or output-quality caveats.

## Limitations

- This is a research workspace, not an official benchmark package.
- The public repo contains aggregate result records and lightweight utilities, not full raw generations.
- Some settings show small gains or trade-offs; Qwen2.5-VL and some AMBER rows should be read as boundary cases.
- OCV is training-free and post-decoding: it does not update model parameters and depends on the availability of safely editable unsupported object commitments.

## Citation Status

No acceptance, publication, or SOTA claim is made by this repository.
