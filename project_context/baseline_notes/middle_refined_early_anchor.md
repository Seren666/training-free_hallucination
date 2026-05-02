# Middle-Refined Early Anchor

> Date: 2026-05-02
> Scope: feasibility plus `1000`-image pilot for anchor-construction refinement based on middle-layer verification.

## 1. Why Middle-Refined Anchor

The prior conclusion was already clear:

- fixed `first_logit / early-anchor` is still the best decoding baseline
- `Object-Safe`, `Attention-Gated`, `Candidate-Local`, and `Middle-Verified` all failed to beat it
- token-level boost clipping should not keep expanding

But the middle-layer audit still gave a mechanism hint worth testing at a different intervention point:

- correct object mentions are already stronger in the middle stage
- introduced hallucinations often have stronger anchor-side push but weaker middle-layer verification
- attention shape, middle rank, and middle attention are all more informative than coarse image-level scalars

So the next question was:

- instead of clipping object tokens at every later decode step, can we clean the anchor itself once at construction time?

## 2. Difference From Token-Level Clipping

Fixed `first_logit`:

- build the raw step-0 anchor
- keep the first generated token unchanged
- inject that anchor at later decode steps

`Middle-Verified`:

- keep the raw anchor
- at later decode steps, clip some candidate object-token boosts

`Middle-Refined`:

- build the raw step-0 anchor
- verify strong object-token anchor support against step-0 middle-layer evidence
- clean the anchor once before later decode begins
- then keep the normal fixed `first_logit` later-step injection logic

This matters because the intervention unit changes:

- no per-step object-token clipping
- no later-step gate over the evolving candidate set
- only source-anchor cleaning

## 3. Feasibility Analysis

Offline feasibility used the existing `4000`-event object-local subset:

- `removed_hallucination=1000`
- `introduced_hallucination=1000`
- `persistent_hallucination=1000`
- `correct_object_mention=1000`

Thresholds were unsupervised:

- strong anchor threshold: `anchor_adjustment_delta p75 = 1.2488965899946751`
- weak middle-rank threshold: `middle_target_rank_mean p75 = 7190.333333333333`
- weak middle-attention threshold: `image_attention_middle_mean p25 = 0.13209990615194495`
- weak middle-probability threshold: `middle_target_probability_mean p25 = 0.00013357673189299626`

Feasibility flag:

- `strong_anchor`
- and `weak_middle = weak_middle_rank OR weak_middle_attention`

Main feasibility result:

- introduced flagged rate: `254/1000 = 0.254`
- correct flagged rate: `102/1000 = 0.102`
- introduced vs correct risk-score AUC: `0.7378`

Flat `Object-Safe` comparison:

- theoretical collateral on correct positive-anchor mentions: `0.998`
- theoretical coverage on introduced positive-anchor mentions: `0.999`

Interpretation:

- the proposed anchor-source cleaning is much more selective than flat `Object-Safe`
- so the route was worth a real pilot

## 4. Method Definition

Base decoding stayed fixed:

- same model
- same prompt: `Please describe the image.`
- same `gamma=0.3`, `lambda=0.05`, `cd_beta=0.1`
- same `max_new_tokens=64`
- first generated token unchanged
- no `The effect`
- no image GT

Anchor refinement rule:

1. Run the normal step-0 forward pass.
2. Read the raw first-anchor logits.
3. Read step-0 middle-layer evidence:
   - middle-layer rank-lens approximation for object-token candidates
   - step-0 middle image attention
4. Keep only positive object-token anchor candidates from official CHAIR `synonyms.txt`.
5. Mark `strong_anchor` as the current-image top quartile of positive object-token anchor scores.
6. Mark `weak_middle` if:
   - `middle_target_rank > p75`, or
   - `step0 middle image attention < p25`
7. For those flagged object tokens only, scale the positive anchor component to `0.25x`.
8. Use the refined anchor in later fixed-`first_logit` decoding.

Object vocabulary:

- source: official CHAIR `synonyms.txt`
- matching: token-id level
- multi-token objects: all token ids appearing in tokenized object terms are included

## 5. Threshold Source

Runtime thresholds were pre-registered from the existing audit outputs.

- `middle_rank_threshold = 7190.333333333333`
- `low_attention_threshold = 0.13209990615194495`
- `middle_prob_threshold = 0.00013357673189299626`
  - recorded for analysis, not used as a direct gate condition in this first pilot
- `object_anchor_quantile = 0.75`
- `object_positive_scale = 0.25`

Important boundary:

- no CHAIR-score tuning
- no threshold search
- no second variant

## 6. 10-Image Sanity

Sanity passed functionally:

- caption generation succeeded
- evaluator succeeded
- `first word changed = 0`
- `empty caption = 0`
- refined anchor was non-empty

Sanity metrics:

| Method | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Object Count | s/sample |
|---|---:|---:|---:|---:|---:|---:|---:|
| regular | 10 | 0.2000 | 0.0789 | 47.5000 | 38 | 3 | 1.3162 |
| fixed_first_logit | 10 | 0.4000 | 0.0889 | 49.4000 | 45 | 4 | 1.3058 |
| middle_refined | 10 | 0.2000 | 0.0625 | 49.9000 | 32 | 2 | 1.5922 |

Most important sanity warning:

- `step0_low_attention_triggered = 1` on all `10/10` images
- refined object tokens per image were already about `142-144`

So the method was functional, but the anchor-stage low-attention branch was already suspiciously broad.

## 7. 1000-Image Pilot Result

| Method | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Object Count | s/sample |
|---|---:|---:|---:|---:|---:|---:|---:|
| regular | 1000 | 0.2090 | 0.0657 | 49.6580 | 4522 | 297 | 1.3092 |
| fixed_first_logit | 1000 | 0.1610 | 0.0509 | 50.9190 | 4717 | 240 | 1.3110 |
| object_safe_anchor | 1000 | 0.1620 | 0.0530 | 51.3090 | 4228 | 224 | 1.3206 |
| previous_attention_gated | 1000 | 0.1680 | 0.0575 | 51.1140 | 4329 | 249 | 1.3834 |
| candidate_local_guard | 1000 | 0.1680 | 0.0555 | 51.0600 | 4431 | 246 | 1.3046 |
| middle_verified | 1000 | 0.1770 | 0.0555 | 51.0110 | 4645 | 258 | 1.4979 |
| middle_refined | 1000 | 0.1640 | 0.0541 | 51.2880 | 4267 | 231 | 1.5460 |

Direct comparison vs fixed `first_logit`:

- changed captions: `950`
- first word changed: `0`
- empty captions: `0`
- improved images: `76`
- worsened images: `73`
- stable images: `851`
- object mentions delta: `-450`
- correct object mentions delta: `-441`
- hallucinated object delta: `-9`
- removed hallucinations: `115`
- introduced hallucinations: `106`

Top removed hallucinations vs fixed:

- `dining table`: `14`
- `person`: `11`
- `chair`: `11`
- `spoon`: `7`
- `car`: `7`

Top introduced hallucinations vs fixed:

- `car`: `11`
- `dining table`: `10`
- `microwave`: `8`
- `chair`: `8`
- `bench`: `5`

## 8. Behavior Analysis

### 8.1 Did it beat fixed first_logit?

No.

- `CHAIRs` is worse: `0.1640` vs `0.1610`
- `CHAIRi` is worse: `0.0541` vs `0.0509`

### 8.2 Did it reduce raw hallucinations?

Yes, but not enough to count as a win.

- hallucinated object count improved: `231` vs `240`
- removed hallucinations (`115`) slightly outnumber introduced (`106`)

This makes it closer to `Object-Safe` than to `Middle-Verified`:

- lower raw hallucinated-object count
- but worse CHAIR and noticeably lower object mentions

### 8.3 Did it preserve the fixed trajectory?

Only partly.

- first word remained unchanged
- average caption length did not collapse
- but the caption trajectory still changed a lot:
  - `changed_caption_count = 950/1000`

So source-anchor cleaning is still capable of heavily perturbing the later trajectory, even without decode-time clipping.

### 8.4 Did it avoid object mention collapse?

No.

- object mentions dropped by `450`
- correct object mentions dropped by `441`
- relative object-mention drop vs fixed is about `9.5%`, which is beyond the allowed health boundary

This is better interpreted as broad source suppression than as precise verification.

### 8.5 What did refinement actually do?

Anchor refinement stats show the core failure mode:

- avg refined object tokens per image: `141.93`
- avg positive object anchor candidates per image: `568.638`
- avg strong-anchor candidates per image: `142.526`
- avg weak-middle-rank candidates per image: `494.156`
- avg step0 middle attention mean: `0.115429`
- avg step0 low-attention trigger rate: `0.978`
- refined object ratio: `0.249596`

Most frequently refined object labels:

- `pheasant`
- `trolley`
- `paddleboat`
- `thief`
- `feline`
- `heifer`
- `beagle`
- `cockatiel`

This is the most important diagnosis:

- the step-0 low-attention condition triggers on almost every image
- so the rule degenerates into refining nearly the whole top quartile of positive object anchor tokens
- in practice this becomes broad anchor cleaning, not sparse middle verification

### 8.6 Comparison with prior failed guards

Compared with `Middle-Verified`:

- `middle_refined` is better on primary metrics than `middle_verified`
- it is also closer to fixed `first_logit`
- but it still fails the health test because mention loss is large

Compared with `Object-Safe`:

- `middle_refined` is slightly healthier on object mentions:
  - `4267` vs `4228`
- but raw hallucination count is slightly worse:
  - `231` vs `224`
- and `CHAIRs / CHAIRi` still do not beat fixed `first_logit`

So this pilot is a more meaningful negative result than `Object-Safe`, but still a negative result.

## 9. Why It Failed

Most likely failure reasons:

1. Anchor refinement was still too broad.
   - the step-0 low-attention branch fired on `97.8%` of images
   - this turned the rule into broad strong-anchor suppression

2. The step-0 attention threshold did not transfer cleanly from object-mention-time audit space to anchor-construction space.
   - the audit thresholds came from object-token local events
   - the runtime anchor rule used step-0 prompt-query evidence
   - those are related, but not the same operating surface

3. Even source-anchor cleaning can still over-remove helpful object support.
   - first token is unchanged
   - but later caption trajectories still shift a lot because the refined anchor is reused everywhere afterward

4. Fixed `first_logit` may already be close to the best point under the current setup.
   - many follow-up variants can reduce some raw hallucinations
   - but they consistently pay for it with correct-mention loss

## 10. Full-Run Decision

No full run was started.

Why:

- object mentions dropped by more than `5%`
- correct object mentions also dropped substantially
- `CHAIRs` and `CHAIRi` did not beat fixed `first_logit`

So the method failed the health gate even though raw hallucinated-object count improved slightly.

## 11. Caveats

- the middle-rank signal at runtime is a rank-lens approximation, not a fully supervised object verifier
- the current low-attention threshold was transferred from object-local audit space to anchor-construction space without tuning
- the refined-token labels reflect CHAIR token-id vocabulary and can overstate semantic precision

## 12. Next Recommendation

- keep fixed `first_logit / early-anchor` as the active best baseline
- treat `Middle-Refined Early Anchor` as an informative negative pilot
- do not start full `middle_refined`
- do not treat “anchor construction” as automatically safer than later-step clipping
- if method work continues, the next anchor-construction idea must be much sparser than global step-0 low-attention plus top-quartile object refinement
