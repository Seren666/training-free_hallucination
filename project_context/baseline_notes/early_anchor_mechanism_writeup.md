# Early-Anchor Mechanism Writeup

> Date: 2026-05-02
> Scope: current mechanism-oriented writeup for the `first_logit / early-anchor` line after completed POPE, full COCO-CHAIR, evaluator alignment, image-level audit, and object-level audit.
> Claim boundary:
> - not a final paper method
> - not a selective runtime policy
> - not cross-model or cross-benchmark validated
> - not a `The effect` story

## 1. Motivation

The working question behind this line is:

- can an early multimodal next-token distribution act as an anchor for later open-ended generation?

The motivating intuition is:

- LLaVA-style caption generation begins with an image-conditioned prompt state
- that state already contains a rich multimodal distribution over plausible next tokens
- if later decoding drifts toward hallucinated nouns, an early anchor might help reshape later token ranking

This is interesting only if:

- the effect survives at full benchmark scale
- it is not a trivial artifact of shorter captions
- it is not just a first-word manipulation
- it has at least some mechanism evidence beyond end metrics

At the current stage, the strongest benchmark for this question is open-ended COCO captioning with CHAIR-style object hallucination evaluation.

## 2. Why POPE Failed For Later-Step First-Logit

The completed POPE result is unambiguous:

- faithful later-step `first_logit` adaptation has `delta = 0` on all `9/9` POPE splits
- `regular` and `first_logit` are identical on:
  - Accuracy
  - Precision
  - Recall
  - F1
  - Yes Rate

This does **not** mean the idea failed in general.

The protocol explanation is stronger:

- POPE under the current setup is a one-word yes/no benchmark
- the decisive answer is usually fixed by the first answer token
- the current `first_logit` adaptation acts only on later decode steps
- so in POPE there is almost no intervention space left after the first answer token

Therefore the right interpretation is:

- POPE is not a suitable benchmark for later-step first-logit intervention evaluation
- POPE should be retained as an `answer-boundary` / `pre-answer` signal-audit benchmark
- the POPE null result is a benchmark-protocol result, not a general refutation of early-anchor signals

## 3. Why COCO-CHAIR Is Appropriate

COCO-CHAIR is a much better fit for this question because it evaluates:

- open-ended caption generation
- object mention behavior over many later decode steps
- explicit object hallucination outcomes

This gives later-step first-logit a real opportunity to matter:

- captions are multi-token
- object nouns often appear well after the first generated word
- object hallucination can be tracked at sentence level and object-instance level

This is exactly the regime where a later-step anchor-based intervention should be judged.

## 4. Full COCO-CHAIR Result

The completed full paired run on `40504` COCO `val2014` images shows a stable positive result.

Regular:

- `CHAIRs = 0.2037`
- `CHAIRi = 0.0655`
- `Avg Caption Length = 49.6823`
- `Object Mentions = 181268`
- `Hallucinated Objects = 11875`
- `s/sample = 1.2956`

First-logit / early-anchor:

- `CHAIRs = 0.1631`
- `CHAIRi = 0.0513`
- `Avg Caption Length = 50.9320`
- `Object Mentions = 187440`
- `Hallucinated Objects = 9609`
- `s/sample = 1.2897`

Full deltas vs regular:

- `CHAIRs = -0.0406`
- `CHAIRi = -0.0142`
- `Avg Caption Length = +1.2497`
- `Object Mentions = +6172`
- `Hallucinated Objects = -2266`

Important behavior facts:

- `changed captions = 40499 / 40504`
- `unchanged captions = 5 / 40504`
- `first word changed = 0 / 40504`
- `The effect` was not used

So the positive result is not explainable as:

- shorter captions
- fewer object mentions
- or first-word manipulation

The method improves CHAIR while:

- captions get slightly longer
- object mentions increase overall
- first word remains unchanged

## 5. Evaluator Alignment

The positive result is not confined to the adapted evaluator.

Adapted evaluator delta:

- `CHAIRs = -0.0406`
- `CHAIRi = -0.0142`

Near-official evaluator delta:

- `CHAIRs = -0.0403`
- `CHAIRi = -0.0145`

These two conclusions are:

- same direction
- very similar magnitude

So the current result is not well explained as an artifact of the Python3 adapted evaluator.

Current best wording is:

- `adapted evaluator result confirmed by near-official alignment`

This still leaves a paper-grade caveat:

- untouched official CHAIR execution is still desirable for final presentation

But the current positive direction is already robust under evaluator alignment.

## 6. Image-Level Audit Limitation

The completed image-level one-forward audit on a stratified `3000`-image subset gave a negative result for coarse selection.

Main finding:

- coarse image-level scalar summaries almost cannot separate `improved` vs `worsened`
- the best absolute AUC shift from `0.5` is only about `0.0167`

What those scalars may weakly indicate:

- whether a sample is more likely to be `changed` vs `stable`

What they do **not** support:

- a useful coarse image-level runtime selector for `helpful` vs `harmful`

This is a strong negative result against the simple story:

- "just read one prompt-level scalar and decide whether to apply early-anchor"

So coarse image-level selective early-anchor is not currently supported.

## 7. Object-Level Mechanism Evidence

The object-event reconstruction succeeded on the full paired outputs.

Event counts:

- `removed_hallucination = 6043`
- `introduced_hallucination = 3880`
- `persistent_hallucination = 3924`
- `correct_object_mention = 86458`

Top removed hallucinated objects:

- `person`
- `dining table`
- `chair`
- `car`
- `bowl`

Top introduced hallucinated objects:

- `dining table`
- `chair`
- `couch`
- `sink`
- `person`
- `refrigerator`

This already suggests a nontrivial mechanism shape:

- the method removes many high-frequency over-mentioned nouns
- but it can also introduce plausible absent indoor / kitchen / furniture nouns

The object-local token-step probe then gave a stronger signal than the image-level audit.

For `removed_hallucination` vs `introduced_hallucination`, the most informative signals are:

- `adjusted_target_rank_if_applied`
  - AUC `0.6512`
- `anchor_target_token_rank`
  - AUC `0.6147`

For `hallucinated` vs `correct`, the most informative signals are:

- `anchor_weight_at_object_step`
  - AUC `0.7865`
- `mention_position_ratio`
  - AUC `0.7861`
- `anchor_target_token_rank`
  - AUC `0.7450`

This means object-local signals are materially more informative than image-level scalars.

## 8. Mechanism Hypothesis

The current mechanism hypothesis is:

- the step-0 image-conditioned first-logit distribution acts as an early multimodal grounding anchor
- later in caption generation, this anchor reshapes object-token ranking
- when the anchor pushes against high-frequency over-mentioned nouns, some hallucinated objects are removed
- when the anchor instead supports plausible but absent scene nouns, new hallucinations can be introduced

The most plausible current picture is not:

- a global caption-shortening effect
- a global object-suppression effect
- a first-word effect
- or a coarse image-level gating effect

The more plausible picture is:

- an object-token-level rank reshaping process
- whose effect depends on:
  - where the object token appears
  - how strong the object token already is locally
  - how much support it receives from the early anchor

This naturally explains the observed asymmetry:

- some object hallucinations are removed
- some are persistent
- some plausible absent nouns are newly introduced

## 9. Current Limitations

Current claim boundary should remain conservative.

What this work **does** support:

- `first_logit / early-anchor` is a promising mechanism candidate
- it has a stable positive effect on full COCO-CHAIR
- the effect survives near-official evaluator alignment
- object-local signals provide real mechanism evidence

What this work does **not** yet support:

- a final deployable method
- a runtime selector
- a classifier
- a threshold-based selective policy
- cross-model generality
- cross-benchmark generality
- SOTA or universal hallucination mitigation claims

So the right framing is:

- promising early-anchor mechanism candidate
- not final paper method

## 10. Next Research Questions

The most sensible next questions are:

1. Can the current mechanism story be written clearly enough for internal review or paper framing?
2. Can official / near-official evaluation alignment be tightened further without changing generation?
3. Can object-local signals support a very small, controlled selective prototype later?
4. Which object categories are consistently helped vs harmed across settings?
5. Does the same object-local pattern hold under small cross-checks without opening a large new benchmark branch?

The important constraint is:

- do not immediately jump to parameter sweep, large benchmark expansion, or classifier training

The evidence now favors:

- mechanism-first consolidation
- then small validation
- only then selective-prototype thinking
