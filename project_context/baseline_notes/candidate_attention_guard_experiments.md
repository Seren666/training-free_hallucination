# Candidate and Attention-Shape Guard Experiments

> Date: 2026-05-02
> Scope: controlled follow-up after the failed `Object-Safe` and `Attention-Gated AttnAnchor` pilots.
> Boundary:
> - no regular rerun
> - no fixed first-logit rerun
> - no prompt change
> - no evaluator change
> - no `The effect`
> - no parameter sweep
> - no classifier
> - no full run unless a `1000` pilot beats fixed `first_logit`

## 1. Why These Two Variants

The previous two selective pilots failed for opposite but related reasons:

- `Object-Safe`:
  - touched almost all positive object-token boosts
  - reduced some hallucinations
  - but collapsed too many correct object mentions
- `Attention-Gated AttnAnchor`:
  - was narrower than `Object-Safe`
  - but still triggered on about `44` decoding steps per image
  - so it still behaved like broad step-level object suppression

The next controlled hypothesis was:

- the useful intervention should be narrower than:
  - whole object vocabulary
  - or all object tokens on low-attention steps

So two new routes were tested:

1. `Candidate-Object Local Guard`
   - only act on current `adjusted top-k` object candidates
2. `Attention-Shape Local Guard`
   - only act when attention-shape suggests weak grounding, not just low mass

## 2. Offline Feasibility

Remote analysis outputs:

- `/root/autodl-tmp/code/training_free_hallucination_probe/results/candidate_attention_shape_feasibility.md`
- `/root/autodl-tmp/code/training_free_hallucination_probe/results/candidate_attention_shape_feasibility.csv`
- `/root/autodl-tmp/code/training_free_hallucination_probe/results/candidate_attention_shape_feasibility.json`

Input:

- `/root/autodl-tmp/code/training_free_hallucination_probe/results/object_local_signal_probe.csv`

No extra probe rerun was needed because the existing object-local probe already contained:

- anchor support fields
- adjusted-rank fields
- middle / late image-attention mass
- image-attention entropy
- head-level mass mean / max / std summaries

### 2.1 Threshold Sources

All thresholds were unsupervised and not tuned on final CHAIR scores.

- candidate top-k:
  - `50`
- rank improvement threshold:
  - `p75` of positive rank improvement
  - value: `2`
- strong boost threshold:
  - `p75` of positive `anchor_adjustment_delta`
  - value: `1.2488965899946751`
- high diffuse threshold:
  - `p75` of middle normalized image-attention entropy
  - value: `0.8176946155949347`
- low middle-mass threshold:
  - `p25` of middle image-attention mass
  - value: `0.13209990615194495`
- extreme concentration threshold:
  - `p10` of middle normalized image-attention entropy
  - value: `0.7223034219776446`

### 2.2 Candidate-Object Feasibility

Offline result:

- introduced hit rate:
  - `0.368`
- correct hit rate:
  - `0.190`
- introduced / correct ratio:
  - `1.937`

Interpretation:

- this was clearly more selective than flat object-vocab gating
- it was also more selective than the previous step-level attention-gated route
- so it was worth a runtime pilot

### 2.3 Attention-Shape Feasibility

Offline result:

- introduced hit rate:
  - `0.298`
- correct hit rate:
  - `0.209`
- introduced / correct ratio:
  - `1.426`

Additional attention-shape observations:

- diffuse high-entropy attention is more common in introduced hallucinations than in correct mentions
- but the separation is only moderate
- extremely concentrated attention is actually more common in correct mentions than in introduced hallucinations

Interpretation:

- diffuse attention has some signal
- but it is not strong enough to justify a direct generation pilot yet
- it does not look like a better immediate decoding rule than the candidate-local route

### 2.4 Offline Decision

Decision:

- run `Candidate-Object Local Guard`
- do **not** run `Attention-Shape Local Guard` generation yet

Reason:

- candidate-local route was supportive
- attention-shape route was not clearly supportive enough

## 3. Candidate-Object Local Guard Definition

Remote implementation:

- main:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/coco_caption_candidate_local_guard.py`
- resumable:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/coco_caption_candidate_local_guard_resumable.py`

Base method:

- fixed later-step `first_logit / early-anchor`
- same:
  - `gamma = 0.3`
  - `lambda = 0.05`
  - `cd_beta = 0.1`
  - prompt
  - greedy decoding
  - `max_new_tokens = 64`
  - no first-token modification
  - no `The effect`

New rule:

- from decode step `1` onward:
  1. compute fixed `first_logit` adjusted logits
  2. take current adjusted `top-k`, with `k = 50`
  3. keep only object-token candidates inside that `top-k`
  4. keep only positive anchor-boost candidates
  5. gate only the candidates that satisfy at least one:
     - rank improvement >= offline threshold
     - strong boost >= offline threshold and also in the current candidate boost top quartile
  6. for those gated candidates only:
     - scale positive boost by `0.25`

What this avoids:

- no whole-object-vocab suppression
- no whole-step low-attention suppression
- no image GT

## 4. Attention-Shape Local Guard Definition

This route was defined only at offline feasibility stage.

Planned first rule:

- current `top-k` object candidate
- positive anchor boost
- high middle-layer normalized image-attention entropy
  - diffuse / weakly grounded attention shape

But runtime generation was not launched because offline support was too weak.

Current status:

- not implemented as a generation script
- stopped before sanity / `1000`

## 5. Sanity Result

Candidate guard `10`-image sanity outputs:

- captions:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/coco_chair/candidate_local_guard_caption_10.json`
- eval:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/coco_chair_candidate_local_guard_eval_10.json`

Health checks:

- first word changed vs fixed:
  - `0`
- first word changed vs regular:
  - `0`
- empty captions:
  - `0`
- average gate trigger steps per image:
  - `10.0`
- average gated candidates per image:
  - `12.0`
- peak reserved GPU memory:
  - about `14.04 GB`

Sanity conclusion:

- implementation is healthy
- the gate is much narrower than the previous `Attention-Gated AttnAnchor`
- small-sample CHAIR numbers are too noisy to use for method judgment

## 6. 1000 Pilot Table

Candidate guard outputs:

- captions:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/coco_chair/candidate_local_guard_caption_1000.json`
- resumable work log:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/coco_chair/candidate_local_guard_caption_1000_resume.jsonl`
- eval:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/coco_chair_candidate_local_guard_eval_1000.json`
- summary:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/candidate_local_guard_1000_metrics.csv`
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/candidate_local_guard_1000_metrics.md`
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/candidate_local_guard_1000_summary.json`

| Method | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Object Count | s/sample |
|---|---:|---:|---:|---:|---:|---:|---:|
| regular | 1000 | 0.2090 | 0.0657 | 49.6580 | 4522 | 297 | 1.3092 |
| fixed first_logit | 1000 | 0.1610 | 0.0509 | 50.9190 | 4717 | 240 | 1.3110 |
| object_safe_anchor | 1000 | 0.1620 | 0.0530 | 51.3090 | 4228 | 224 | 1.3206 |
| previous attention_gated | 1000 | 0.1680 | 0.0575 | 51.1140 | 4329 | 249 | 1.3834 |
| candidate_local_guard | 1000 | 0.1680 | 0.0555 | 51.0600 | 4431 | 246 | 1.3046 |

## 7. Comparison With Fixed First-Logit

Candidate guard vs fixed `first_logit`:

- `CHAIRs`:
  - `0.1610 -> 0.1680`
  - worse
- `CHAIRi`:
  - `0.0509 -> 0.0555`
  - worse
- hallucinated object count:
  - `240 -> 246`
  - worse
- average caption length:
  - `50.9190 -> 51.0600`
  - slightly longer
- object mentions:
  - `4717 -> 4431`
  - `-286`
  - about `-6.1%`
- correct object mentions:
  - `-292`

Image-level paired behavior:

- changed captions:
  - `857 / 1000`
- first word changed:
  - `0`
- empty captions:
  - `0`
- improved:
  - `60`
- worsened:
  - `63`
- stable:
  - `877`

Object-level movement vs fixed:

- removed hallucination total:
  - `82`
- introduced hallucination total:
  - `88`
- net hallucinated object delta:
  - `+6`

Top removed hallucinations:

- `dining table`: `11`
- `chair`: `9`
- `person`: `7`
- `car`: `5`

Top introduced hallucinations:

- `car`: `8`
- `chair`: `7`
- `truck`: `5`
- `dining table`: `5`
- `person`: `4`
- `microwave`: `4`
- `refrigerator`: `4`

## 8. Comparison With Previous Attention-Gated

Relative to the previous `Attention-Gated AttnAnchor` pilot:

- `CHAIRs`:
  - `0.1680 -> 0.1680`
  - unchanged
- `CHAIRi`:
  - `0.0575 -> 0.0555`
  - slightly better
- object mentions:
  - `4329 -> 4431`
  - slightly better
- hallucinated object count:
  - `249 -> 246`
  - slightly better
- average gate width:
  - previous attention-gated:
    - about `44.315` trigger steps per image
  - candidate guard:
    - about `10.938` trigger steps per image

So the candidate-local route is clearly narrower and somewhat healthier than the previous step-level attention gate.

But that narrower gate is still not enough to beat fixed `first_logit`.

## 9. Gate Trigger Stats

Candidate guard runtime stats:

- average gate trigger steps per image:
  - `10.938`
- average gated candidates per image:
  - `12.059`
- average top-k object candidates per image:
  - `33.308`
- gated candidate ratio:
  - `0.362045`
- average runtime:
  - `1.3046 s/image`
- peak reserved GPU memory:
  - `14.041 GB`

Top gated token-level proxies:

- `adult`
- `toaster`
- `oriole`
- `weimaraner`
- `lamb`
- `dachshund`

Important caveat:

- these are token-level / synonym-level proxies, not perfect phrase-level object categories
- they still show the gate is acting on a narrower candidate slice than the previous attention-gated method

## 10. Behavior Analysis

Main takeaways:

- candidate-local gating is better than broad step-level gating
- it reduces the intervention width substantially
- it preserves average caption length
- it preserves more object mentions than `Object-Safe` and previous `Attention-Gated`

But it still fails the core objective:

- it does not beat fixed `first_logit`
- it still drops object mentions beyond the allowed `5%` threshold
- it still drops correct object mentions
- it still introduces at least as many hallucinations as it removes

So this is an informative negative result, not a method win.

## 11. Did Any Method Beat Fixed First-Logit?

Current answer:

- no

Within this round:

- `Attention-Shape` route was stopped at offline feasibility
- `Candidate-Object Local Guard` ran to `1000`, but did not beat fixed `first_logit`

## 12. Full Decision

Current decision:

- do **not** start full

Reason:

- `CHAIRs` is not better than fixed `first_logit`
- `CHAIRi` is not better than fixed `first_logit`
- hallucinated object count is worse than fixed `first_logit`
- object mentions drop by more than `5%`
- correct object mentions also drop

So the user-specified full-run health gate is not met.

## 13. Current Recommendation

Recommended interpretation:

- candidate-local gating was a more useful direction than broad attention-gated suppression
- but it still is not selective enough at the actual object-mention decision boundary

Recommended next step:

- do not full-run any method from this round
- do not tune thresholds or sweep
- if a new method is attempted later, it must be even more local than current top-k candidate gating
- likely directions are:
  - phrase-aware / multi-token object decisions
  - direct candidate replacement or reranking at the mention boundary
  - mention-local rather than broad candidate-slice suppression
