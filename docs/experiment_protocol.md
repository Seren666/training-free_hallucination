# Experiment Protocol

## Main Benchmarks

The public result tables emphasize caption-side hallucination benchmarks:

- **COCO/CHAIR-500**: reports CHAIRs and CHAIRi. Lower is better.
- **AMBER-1004**: reports AMBER CHAIR, Cover, Hal, and Cog. Lower hallucination metrics are better; Cover is a preservation-oriented metric.
- **OpenCHAIR**: reports object-level OpenCHAIR and sentence-level hallucination scores. Lower is better.

POPE appears only as a diagnostic yes/no VQA record in the project history. It is not used as the primary claim in this public repository.

## Models

Public aggregate records cover:

- LLaVA-1.5-7B
- InstructBLIP-7B
- InternVL3.5-8B-HF
- Qwen2.5-VL-7B-Instruct

The strongest and cleanest public headline results are on LLaVA-1.5-7B and InstructBLIP-7B. InternVL3.5 and Qwen2.5-VL are included for transfer and boundary-case evidence.

## Methods Compared

- **Regular**: standard caption generation.
- **FLB**: a first-logit / stronger-source generation baseline where available.
- **OCV on Regular source**: OCV applied directly to regular captions.
- **OCV on FLB source**: OCV applied after FLB source captions.

External baseline summaries for VCD, AGLA, MaskCD, and DeCo are stored separately in `results/public/external_baselines.csv` because several reproduced rows have protocol or output-quality caveats.

## Reproduction Boundary

The checked-in public tables can be regenerated without model weights:

```bash
python scripts/make_tables.py
```

Full benchmark reruns require:

- user-provided LVLM checkpoints
- benchmark datasets and annotations
- GPU hardware compatible with the relevant model
- model-specific probe runners not redistributed in this sanitized public repo

## Runtime Records

`results/public/runtime_summary.csv` separates generation time from OCV verification-forward overhead. The cleanest fresh microbenchmark row is InstructBLIP-7B on COCO/CHAIR-500: OCV verification over existing regular and FLB captions took 1.7763 seconds total for 20 images, or 0.088816 seconds per image, excluding model loading and evaluation.

This is an overhead decomposition, not a matched speed claim against all decoding-time baselines.
