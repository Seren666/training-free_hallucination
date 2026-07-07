# Resume Bullets

Use wording that matches the evidence in `results/public/`. Do not claim paper acceptance, official benchmark status, or SOTA.

## English Version

- Explored a post-decoding, training-free method for mitigating LVLM object hallucination by verifying object commitments in generated captions and applying bounded edits without model retraining.
- Built aggregate evaluation records across COCO/CHAIR-500, AMBER-1004, and OpenCHAIR for LLaVA-1.5-7B and InstructBLIP-7B, comparing regular decoding, FLB source captions, and OCV post-decoding edits.
- In the strongest supported setting, reduced InstructBLIP-7B COCO/CHAIR-500 CHAIRs from 0.2360 with FLB to 0.1340 with OCV-on-FLB, while documenting caveats, preservation trade-offs, and boundary cases.

## Chinese Version

- 独立探索 post-decoding / training-free 的 LVLM object hallucination 缓解方法，通过验证生成 caption 中的 object commitments 并进行有界编辑，在不训练模型参数的情况下降低不受图像支持的物体描述。
- 基于 COCO/CHAIR-500、AMBER-1004 和 OpenCHAIR 整理了 LLaVA-1.5-7B 与 InstructBLIP-7B 的 aggregate evaluation records，对比 regular decoding、FLB source captions 与 OCV post-decoding edits。
- 在当前最强可公开支撑的结果中，InstructBLIP-7B 在 COCO/CHAIR-500 上由 FLB 的 CHAIRs 0.2360 降至 OCV-on-FLB 的 0.1340，同时系统记录了 preservation trade-off、边界模型和外部 baseline caveats。

## Short Version

- Explored training-free post-decoding mitigation for LVLM object hallucination; built verified aggregate tables across COCO/CHAIR, AMBER, and OpenCHAIR and reduced InstructBLIP COCO/CHAIR-500 CHAIRs from 0.2360 to 0.1340 over an FLB source baseline in the strongest supported setting.
