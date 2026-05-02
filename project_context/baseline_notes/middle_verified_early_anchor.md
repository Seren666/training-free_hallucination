# Middle-Verified Early Anchor

> Date: 2026-05-02
> Scope: `1000`-image pilot for a middle-layer verification variant of fixed `first_logit / early-anchor`.

## 1. Why Middle Verification

The middle-layer audit gave the first strong reason to try a narrower follow-up than `Object-Safe`, `Attention-Gated AttnAnchor`, or `Candidate-Object Local Guard`.

Key audit evidence:

- `introduced` vs `correct`
  - `middle_target_rank_mean: 6098.926 vs 3533.189`
  - `image_attention_middle_mean: 0.145080 vs 0.183550`
  - `middle_target_probability_mean: 0.071635 vs 0.144712`
- `introduced` vs `removed`
  - `anchor_adjustment_delta: 1.151627 vs 0.978613`
  - `adjusted_target_rank_if_applied: 1.021 vs 1.467`
- attention shape was more informative than plain mass alone:
  - `mass_change_late_minus_mid abs(AUC-0.5)=0.3113`
  - `image_attention_middle_mean=0.2616`
  - `middle_peak_ratio=0.2323`
  - `middle_head_cv=0.1808`

Working hypothesis:

- fixed `first_logit` helps by giving a useful early anchor
- but some introduced hallucinations are anchor-pushed object candidates without enough middle-layer verification
- so a narrow candidate-level check against middle-layer evidence was worth a controlled `1000` pilot

## 2. Method Definition

Base method:

- start from fixed `first_logit / early-anchor`
- do not change the first generated token
- keep `gamma=0.3`, `lambda=0.05`, `cd_beta=0.1`
- keep prompt `Please describe the image.`
- keep `max_new_tokens=64`
- do not use `The effect`

Runtime rule:

1. At each `decode_step >= 1`, compute regular logits and fixed `first_logit` adjusted logits.
2. Take the adjusted-logit `top-k` candidates with `k=50`.
3. Keep only current `top-k` object-token candidates with positive anchor adjustment.
4. Mark a candidate as `strong_anchor` if its positive anchor boost is in the current-step top quartile among the current object candidates.
5. Mark a candidate as `weak_middle_verification` if:
   - the step middle image attention mean is below the global low-attention threshold, and
   - the candidate middle-layer target rank is worse than the global middle-rank threshold.
6. Only when both conditions hold, scale that candidate's positive anchor boost to `0.25x`.
7. Leave negative adjustments unchanged.
8. Leave non-object tokens unchanged.
9. Leave object tokens outside the current `top-k` untouched.

Object vocabulary:

- source: official CHAIR `synonyms.txt`
- matching: token-id level
- multi-token objects: every token id appearing in the tokenization of official object terms is included
- no image GT is used at runtime

## 3. Threshold Source

Thresholds were fixed before the pilot from the existing object-local audit files.

- `low_attention_threshold = 0.13209990615194495`
  - source: global `p25` of object-event middle attention
- `middle_rank_threshold = 7190.333333333333`
  - source: global `p75` of object-event middle target rank
- `middle_prob_threshold = 0.00013357673189299626`
  - source: global `p25` of middle target probability
  - recorded for analysis, not used in the first runtime gate
- `object_positive_scale = 0.25`
- `candidate_top_k = 50`
- `strong_anchor` was defined per step from the current object-candidate boost distribution, not from final CHAIR score

Important boundary:

- these thresholds were unsupervised
- they were not tuned on final `CHAIRs / CHAIRi`
- no threshold sweep was done

## 4. 10-Image Sanity

Sanity outputs:

- captions generated successfully
- evaluator ran successfully
- `first word changed = 0`
- `empty captions = 0`
- gate was active but narrow:
  - average gate-trigger steps per image: about `3.6`
  - average low-attention steps per image: about `45.6`

Sanity metrics:

| Method | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Object Count | s/sample |
|---|---:|---:|---:|---:|---:|---:|---:|
| regular | 10 | 0.2000 | 0.0789 | 47.5000 | 38 | 3 | 1.3162 |
| fixed_first_logit | 10 | 0.4000 | 0.0889 | 49.4000 | 45 | 4 | 1.3058 |
| middle_verified | 10 | 0.5000 | 0.1136 | 49.4000 | 44 | 5 | 1.5016 |

This was treated as implementation sanity only, not as the method decision point.

## 5. 1000-Image Pilot Result

| Method | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Object Count | s/sample |
|---|---:|---:|---:|---:|---:|---:|---:|
| regular | 1000 | 0.2090 | 0.0657 | 49.6580 | 4522 | 297 | 1.3092 |
| fixed_first_logit | 1000 | 0.1610 | 0.0509 | 50.9190 | 4717 | 240 | 1.3110 |
| object_safe_anchor | 1000 | 0.1620 | 0.0530 | 51.3090 | 4228 | 224 | 1.3206 |
| previous_attention_gated | 1000 | 0.1680 | 0.0575 | 51.1140 | 4329 | 249 | 1.3834 |
| candidate_local_guard | 1000 | 0.1680 | 0.0555 | 51.0600 | 4431 | 246 | 1.3046 |
| middle_verified | 1000 | 0.1770 | 0.0555 | 51.0110 | 4645 | 258 | 1.4979 |

Direct comparison vs fixed `first_logit`:

- changed captions: `371`
- first word changed: `0`
- empty captions: `0`
- improved images: `12`
- worsened images: `27`
- stable images: `961`
- object mentions delta: `-72`
- correct object mentions delta: `-90`
- hallucinated object delta: `+18`
- removed hallucination total: `18`
- introduced hallucination total: `36`

Top removed hallucinations vs fixed:

- `dining table`: `4`
- `person`: `2`
- `car`: `2`
- `donut`: `2`

Top introduced hallucinations vs fixed:

- `dining table`: `4`
- `bicycle`: `3`
- `bottle`: `3`
- `sports ball`: `2`
- `microwave`: `2`
- `sink`: `2`
- `couch`: `2`

## 6. Gate Behavior

The gate was much narrower than the previous broad attention gate.

- average gate-trigger steps per image: `3.932`
- average low-attention steps per image: `44.384`
- average gated candidates per image: `3.962`
- average `top-k` object candidates per image: `33.136`
- average strong-anchor candidates per image: `22.625`
- average weak-middle-rank candidates per image: `10.460`
- gated candidate ratio: `0.119568`

Most frequently gated token labels:

- `adult`
- `weimaraner`
- `toaster`
- `cake`
- `dachshund`
- `bed`
- `paddleboat`
- `man`
- `skateboard`
- `baseball bat`

Compared with earlier selective pilots:

- vs `Object-Safe`
  - object mentions delta vs fixed improved from `-489` to `-72`
  - correct object mentions delta vs fixed improved from `-473` to `-90`
- vs `previous_attention_gated`
  - object mentions delta vs fixed improved from `-388` to `-72`
  - correct object mentions delta vs fixed improved from `-397` to `-90`
  - gate-trigger steps per image dropped from about `44.3` to about `3.9`
- vs `candidate_local_guard`
  - object mentions delta vs fixed improved from `-286` to `-72`
  - correct object mentions delta vs fixed improved from `-292` to `-90`
  - gate-trigger steps per image dropped from about `10.9` to about `3.9`

So the middle-verified rule clearly avoided the earlier object-mention collapse better than the prior guard family.

## 7. Did It Beat Fixed First-Logit?

No.

Why it stops here:

- `CHAIRs` is worse than fixed `first_logit`: `0.1770` vs `0.1610`
- `CHAIRi` is worse than fixed `first_logit`: `0.0555` vs `0.0509`
- hallucinated object count is higher than fixed `first_logit`: `258` vs `240`
- introduced hallucinations outnumber removed hallucinations: `36` vs `18`

Health judgment:

- no first-word drift
- no empty captions
- no major object-mention collapse
- but the primary hallucination metrics regress

Therefore:

- the method does not meet the full-run condition
- no full run was started
- no threshold tuning or second variant was run

## 8. What This Means

Positive takeaway:

- middle layers are still useful as an audit and mechanism surface
- the pilot confirms that middle-layer verification can make a gate much narrower than earlier broad suppression rules
- the pilot also confirms that narrower runtime action can preserve correct object mentions much better

Negative takeaway:

- using middle-layer evidence as a token-level boost-clipping rule still does not beat fixed `first_logit`
- the remaining errors suggest that the current middle-rank verification is still too indirect or too noisy to decide which candidate boosts should be clipped
- the fixed `first_logit` trajectory may already be close to the best point for many valid mentions, so even a narrower clipping rule can still remove helpful pushes

Attention-shape interpretation:

- attention-shape was valuable in the audit stage
- but it was not added to the first runtime rule
- this pilot therefore does not validate attention-shape as a working runtime selector yet

## 9. Caveats

- token-id object matching is practical and GT-free, but it is still a coarse proxy for full object-mention semantics
- the logged gated token labels reflect CHAIR synonym token ids and can overstate semantic precision
- the runtime gate used middle attention plus middle rank only; it did not yet test a richer mention-boundary or phrase-level verification rule

## 10. Current Recommendation

- keep fixed `first_logit / early-anchor` as the active best decoding baseline
- treat `Middle-Verified Early Anchor` as a useful but negative pilot
- keep the middle-layer audit as mechanism evidence
- do not start full `middle_verified`
- if method work continues, it should move to a materially different family than token-level boost clipping
