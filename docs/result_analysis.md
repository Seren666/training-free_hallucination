# Result Analysis

## Strongest Supported Result

The strongest clean headline result is on **InstructBLIP-7B + COCO/CHAIR-500**:

- Regular: CHAIRs 0.2620 / CHAIRi 0.0936
- FLB: CHAIRs 0.2360 / CHAIRi 0.0758
- OCV on FLB: CHAIRs 0.1340 / CHAIRi 0.0464

This reduces CHAIRs by 0.1280 versus regular generation and by 0.1020 versus FLB in this run.

## Cross-Benchmark Pattern

On LLaVA-1.5-7B and InstructBLIP-7B, OCV on FLB source improves over both regular generation and FLB on the main caption-side metrics in the public table:

- COCO/CHAIR-500 improves clearly.
- AMBER hallucination metrics improve, with Cover trade-offs in some rows.
- OpenCHAIR improves, but gains are smaller than on COCO/CHAIR and AMBER.

## Generalization And Boundary Cases

InternVL3.5 provides additional evidence that OCV can transfer beyond the two initial models, especially on COCO/CHAIR and OpenCHAIR. Qwen2.5-VL is a boundary case: it starts with lower hallucination rates and leaves less safely editable headroom, so OCV gains are smaller and preservation trade-offs matter more.

## External Baselines

AGLA, VCD, MaskCD, and DeCo were reproduced or summarized under project-specific protocols. These rows are useful context, but they are not presented as official leaderboard comparisons. DeCo in particular has a full CHAIR-500 row but carries a truncation/fluency caveat.

## Efficiency

Runtime records show that OCV adds a verification-forward overhead over existing captions rather than changing decoding itself. In the fresh InstructBLIP microbenchmark, the combined verification pass over regular and FLB captions was 0.088816 seconds per image on the recorded GPU environment. This supports the claim that the extra post-decoding cost is small in the measured setting, but not a universal speed claim.

## Interpretation

The public results support a cautious claim: OCV can reduce unsupported object mentions as a training-free post-decoding verifier, especially when attached to a stronger source-caption pool. The method is not uniformly dominant; it depends on source caption quality, editable unsupported commitments, and preservation gates.
