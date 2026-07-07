# Technical Report

## Summary

Object Commitment Verification (OCV) is a post-decoding, training-free verifier for object hallucination in LVLM captions. It scores object mentions after caption generation and applies bounded edits when a mention appears unsupported.

## Benchmarks

The public aggregate records cover COCO/CHAIR-500, AMBER-1004, and OpenCHAIR. The two main models are LLaVA-1.5-7B and InstructBLIP-7B; InternVL3.5 and Qwen2.5-VL are included as transfer or boundary settings.

## Main Result Snapshot

| Setting | Regular | FLB | OCV on FLB |
| --- | ---: | ---: | ---: |
| LLaVA COCO/CHAIR-500 CHAIRs | 0.1720 | 0.1560 | 0.1100 |
| InstructBLIP COCO/CHAIR-500 CHAIRs | 0.2620 | 0.2360 | 0.1340 |
| LLaVA AMBER Hal | 48.2 | 31.6 | 25.0 |
| InstructBLIP AMBER Hal | 59.0 | 52.5 | 48.4 |
| LLaVA OpenCHAIR | 0.1803 | 0.1621 | 0.1584 |
| InstructBLIP OpenCHAIR | 0.1731 | 0.1731 | 0.1667 |

## Efficiency

The public runtime record separates caption generation from OCV verification. The clean fresh microbenchmark measured InstructBLIP OCV verification over existing regular and FLB captions at 1.7763 seconds for 20 images, or 0.088816 seconds per image, excluding model loading and evaluation.

## Cautions

- The method is not universally dominant.
- Some gains are small on lower-hallucination models.
- The InstructBLIP OpenCHAIR FLB row is regular-equivalent in the recorded run.
- External baselines are retained with protocol caveats and should not be read as official leaderboard claims.
