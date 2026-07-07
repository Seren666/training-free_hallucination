# Research Positioning

This project treats hallucination as a reliability problem in vision-language systems. A generated object mention is useful only when it is grounded in visual evidence or supported by safe context.

## Why Post-Decoding?

Post-decoding methods are attractive when retraining is expensive or unavailable. They can be attached to existing LVLM outputs and can be compared across different source-caption pools such as regular decoding and FLB.

## Link To Visual Grounding

OCV focuses on object commitments: concrete mentions that can be checked against visual evidence. This framing connects hallucination mitigation to broader questions of visual evidence alignment, verifier design, and safe intervention.

## Link To VLA And Embodied Agents

Reliable perception is a prerequisite for reliable action. In embodied or VLA-style systems, an unsupported object mention can become a wrong manipulation target or an unsafe action plan. A verifier that flags weakly grounded object commitments can be a useful layer before downstream planning.

## Future Direction

Future work may combine post-decoding verification with world-model-style consistency checks. For example, imagined rollouts or visual consistency tests could evaluate whether generated descriptions or proposed actions remain grounded across plausible scene states.

This repository does not claim to solve VLA reliability. It positions object hallucination mitigation as one measurable subproblem on the path toward more reliable perception-action systems.
