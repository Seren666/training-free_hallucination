# Limitations

- The repository contains aggregate records and lightweight utilities, not a complete model-running benchmark package.
- Full reruns require external model checkpoints and benchmark datasets that are not redistributed here.
- Some external baseline rows are protocol-adapted reproductions rather than official native benchmark numbers.
- OpenCHAIR uses an offline local judge setup in these artifacts; results should be interpreted as run-specific aggregate evidence.
- The InstructBLIP OpenCHAIR FLB row is regular-equivalent in this run, so it should not be interpreted as a general FLB failure.
- The method is post-decoding and bounded-edit based. If a caption has no safely editable unsupported commitment, OCV may abstain or provide little improvement.
- AMBER rows can show Cover trade-offs. Hallucination reduction should be read together with preservation statistics.
- No statistical significance test is claimed in the public README.
- No paper acceptance, official benchmark status, or state-of-the-art claim is made.
