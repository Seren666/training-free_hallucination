# Baseline Reproduction Plan

> Status: planning only. No additional baseline repositories have been cloned in this stage.
> Purpose: prioritize baselines by relevance to the new one-forward signal question, compatibility with existing remote resources, and expected reproduction cost.

## Priority summary

Recommended priority order for the next stage:

1. FLB
2. VISTA
3. Devils in Middle Layers / Attention Lens
4. MFCD
5. SECOND
6. iTaD
7. Octopus

## Candidate table

| Baseline | Official source | Main idea | POPE / object-hallucination fit | Existing LLaVA-1.5 + POPE fit | Reproduction cost | Suggested priority | Notes |
|---|---|---|---|---|---|---|---|
| FLB | [Paper](https://arxiv.org/abs/2604.00455), [Code](https://github.com/jiwooha20/FLB) | First-logit / early-anchor boosting | High concept fit, but public code looks AMBER-first | High for mechanism port, medium for exact official repro | Medium | P1 | Best first baseline because it directly matches the new first-logit question |
| VISTA | [Paper](https://arxiv.org/abs/2502.03628), [Code](https://github.com/LzVv123456/VISTA) | Early-layer self-logits augmentation + visual steering | Strong, official repo includes `run_pope.sh` | High | Medium | P2 | Strong signal-audit relevance: gradual visual information loss, early excitation, hidden genuine info |
| Devils in Middle Layers / Attention Lens | [Paper](https://arxiv.org/abs/2411.16724), [Code](https://github.com/ZhangqiJiang07/middle_layers_indicating_hallucinations) | Middle-layer attention analysis, VAR features, head-guided intervention | Strong object-hallucination relevance, but CHAIR-first and classifier-heavy | Medium | Medium | P2 | Very useful for signal auditing, but not ideal as the first direct baseline because it trains a detector |
| MFCD | [Code](https://github.com/liubq-dev/mfcd) | Multi-frequency contrastive decoding | Official repo includes POPE eval commands | High | Medium to high | P3 | Compatible with LLaVA-1.5 and POPE, but method direction is still another CD-family perturbation rather than a one-forward signal method |
| SECOND | [Project page](https://aidaslab.github.io/SECOND/), [Code](https://github.com/AIDASLab/SECOND) | Selective multi-scale + multi-stage contrastive decoding | Official results include POPE | Low to medium | High | P4 | Strong method and official POPE support, but published backbones are LLaVA-Next / OneVision / Yi-VL rather than the current LLaVA-1.5 setup |
| iTaD | [Paper](https://aclanthology.org/2025.naacl-long.75/) | Image-token attention-guided inter-layer contrastive decoding | Conceptually relevant | Unknown to medium | Medium to high | P5 | Good signal intuition, but official public code was not clearly located during this planning pass |
| Octopus | [Paper](https://arxiv.org/abs/2503.00361), [Code](https://github.com/LijunZhang01/Octopus) | Dynamic contrastive decoding | Public repo is AMBER-focused | Medium | Medium | P6 | Useful contrastive reference, but less aligned with the new one-forward risk-reading line than FLB or VISTA |

## Short justification per candidate

### 1. FLB

- highest conceptual alignment with the current research note
- uses first-logit / early-anchor intuition rather than a heavy new decoding stack
- best first baseline for testing whether one normal forward already contains a useful risk signal

### 2. VISTA

- especially relevant to the new signal-audit stage
- official repo already exposes POPE support and LLaVA-1.5 support
- useful after FLB because it turns hidden early-layer evidence into a concrete inference-time intervention

### 3. Devils in Middle Layers / Attention Lens

- highly relevant for middle-layer visual support, head consistency, and attention-lens analysis
- more valuable as a signal-audit reference than as the very first reproduction target
- public code includes classifier training, which is outside the current preferred direction

### 4. MFCD

- easy benchmark/model compatibility
- useful as a CD-family comparator if we later want a stronger non-FLB baseline set
- less valuable than FLB/VISTA for the current one-forward signal question

### 5. SECOND

- strong recent baseline with official POPE results
- higher remote cost and weaker fit to current available model resources
- better to postpone until after the lighter LLaVA-1.5-aligned baselines are understood

### 6. iTaD

- attention-drop intuition is close to the new signal plan
- lack of clearly accessible public code raises setup risk
- good paper to reference during audit design even before any reproduction

### 7. Octopus

- official code exists
- public setup is AMBER-centered and dynamically contrastive
- not the most direct answer to the current first-logit / one-forward question

## Recommended staging

### Stage A: first wave

- FLB
- VISTA

### Stage B: signal-analysis references

- Devils in Middle Layers / Attention Lens
- iTaD

### Stage C: broader contrastive comparators

- MFCD
- SECOND
- Octopus

## Execution rule for this stage

For now:

- no local clone of any baseline repo
- no baseline execution
- no local model/data download
- use this document only as a queue and priority guide

