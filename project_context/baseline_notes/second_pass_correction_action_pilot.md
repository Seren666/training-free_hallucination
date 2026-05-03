# Second-Pass Correction Action Pilot

> Date: 2026-05-03
> Scope: pilot comparison of four verification / correction actions driven by the weighted training-free mention-level verifier, using the existing `fixed first_logit` `1000`-image COCO-CHAIR subset. No new decoding, no new classifier, no GT-driven runtime decision, no evaluator changes.

## 1. Motivation

The weighted mention-level verifier is now the strongest current non-learned risk signal for object mentions. The next question is no longer whether the signal exists, but what to do when it flags a high-risk mention.

This round therefore compared four bounded actions:

- `A` verification-only
- `B` conservative local removal
- `C` local second-pass regeneration
- `D` dual-caption phrase replacement / sentence rollback

The goal was not to prove a final correction method. It was to see which action reduces hallucination most effectively without winning only by saying fewer objects.

## 2. Weighted Verifier Used

Risk scoring used the existing weighted mention-level evidence families:

- `global_weighted_evidence_score`
- `introduced_focused_weighted_score`
- `persistent_focused_weighted_score`
- `removed_focused_weighted_score`

Primary runtime-style risk score:

- `primary_risk_score = max(global, introduced, persistent, removed)`
- `primary_risk_family = argmax(...)`

Risk groups were preregistered by quantile, not tuned:

- top `5%` = `very_high_risk`
- top `10%` = `high_risk`
- top `20%` = `medium_high_risk`

Primary reporting uses top `10%`.

## 3. High-Risk Mention Pool

The action pool was built only from `fixed first_logit` captions, because all four actions operate on that caption stream.

| Item | Result |
|---|---|
| images in pilot caption set | `1000` |
| images with eligible first-logit object mentions | `982` |
| mention count | `2107` |
| hallucinated mentions | `194` |
| correct mentions | `1913` |
| base hallucinated-mention rate | `9.2%` |
| top `5%` threshold | `0.985287` |
| top `10%` threshold | `0.700944` |
| top `20%` threshold | `0.243182` |
| top `10%` mention count | `211` |
| top `10%` dominant risk families | `introduced_focused=176`, `persistent_focused=26`, `removed_focused=9` |
| top `10%` mention position | `late=151`, `middle=54`, `early=6` |

Reading:

- the verifier is mostly surfacing introduced-style risk at the top
- high-risk mentions are heavily late-positioned
- the pool is sparse enough to support local action rather than caption-wide rewriting

## 4. Action A: Verification-Only

This action does not edit captions. It only asks whether the weighted verifier pushes hallucinated mentions into the high-risk tail.

| Slice | Mention Count | Precision | Recall | Correct False Alarms |
|---|---:|---:|---:|---:|
| top `5%` | `106` | `0.4245` | `0.2320` | `61` |
| top `10%` | `211` | `0.3365` | `0.3660` | `140` |
| top `20%` | `422` | `0.2867` | `0.6237` | `301` |

Event-type hit rates:

- top `10%` introduced hit rate: `0.4848`
- top `10%` persistent hit rate: `0.2421`
- removed hit rate is not applicable on the actionable first-logit-side pool

Verification-only takeaway:

- the verifier clearly concentrates hallucinated mentions above the base `9.2%` rate
- top `5%` precision reaches `42.5%`
- top `10%` precision reaches `33.7%`
- persistent remains harder than introduced
- false alarms are still meaningful, so the verifier is usable as a pilot trigger but not yet a clean standalone rule

## 5. Action B: Conservative Local Removal

Removal edits the risky noun phrase directly, with conservative grammar cleanup and at most `1-2` removals per caption.

### `removal_top10`

| Metric | Result |
|---|---:|
| CHAIRs | `0.1290` |
| CHAIRi | `0.0413` |
| Avg Caption Length | `50.6060` |
| Object Mentions | `4580` |
| Correct Object Mentions | `4391` |
| Hallucinated Object Count | `189` |
| edited images | `110` |
| edited mentions | `133` |
| object mention delta vs fixed | `-137` |
| correct mention delta vs fixed | `-86` |
| hallucinated object delta vs fixed | `-51` |
| removed hallucinated mentions | `51` |
| removed correct mentions | `82` |
| hallucination reduction per removed correct mention | `0.6220` |

### `removal_top5`

| Metric | Result |
|---|---:|
| CHAIRs | `0.1370` |
| CHAIRi | `0.0431` |
| Avg Caption Length | `50.6840` |
| Object Mentions | `4615` |
| Correct Object Mentions | `4416` |
| Hallucinated Object Count | `199` |
| edited images | `80` |
| edited mentions | `99` |
| object mention delta vs fixed | `-102` |
| correct mention delta vs fixed | `-61` |
| hallucinated object delta vs fixed | `-41` |
| removed hallucinated mentions | `41` |
| removed correct mentions | `58` |
| hallucination reduction per removed correct mention | `0.7069` |

Removal takeaway:

- `top10` is the strongest metric result in this round
- `top5` is slightly more conservative, but gives back some hallucination reduction
- the gain is not coming from a collapse in caption length
- but it still does remove a non-trivial number of correct mentions, so this is not a clean win yet

## 6. Action C: Local Second-Pass Regeneration

This route used a rewrite prompt on the risky image-caption pair, with a `200`-image edit budget. In practice, only `151` images were selected by the high-risk pool.

Observed result:

- output file: `local_regen_caption_200.json`
- attempted edited images: `151`
- effective changed captions: `0`
- CHAIR metrics: exactly unchanged from fixed `first_logit`

| Metric | Result |
|---|---:|
| CHAIRs | `0.1610` |
| CHAIRi | `0.0509` |
| Avg Caption Length | `50.9190` |
| Object Mentions | `4717` |
| Correct Object Mentions | `4477` |
| Hallucinated Object Count | `240` |

Local-regen takeaway:

- under the current prompt and greedy rewrite setup, the model effectively reproduced the original caption
- this means the route did not produce a meaningful correction signal in this pilot
- it should be treated as a failed pilot in its current form, not as evidence against all rewrite-based approaches in principle

## 7. Action D: Dual-Caption Phrase Replacement / Selection

Two conservative dual-caption variants were tested against the same fixed `first_logit` baseline.

### `dual_phrase_replace`

| Metric | Result |
|---|---:|
| CHAIRs | `0.1400` |
| CHAIRi | `0.0442` |
| Avg Caption Length | `50.7370` |
| Object Mentions | `4637` |
| Correct Object Mentions | `4432` |
| Hallucinated Object Count | `205` |
| edited images | `78` |
| edited mentions | `78` |
| object mention delta vs fixed | `-80` |
| correct mention delta vs fixed | `-45` |
| hallucinated object delta vs fixed | `-35` |
| removed hallucinated mentions | `34` |
| removed correct mentions | `44` |
| hallucination reduction per removed correct mention | `0.7955` |

### `dual_sentence_rollback`

| Metric | Result |
|---|---:|
| CHAIRs | `0.1490` |
| CHAIRi | `0.0481` |
| Avg Caption Length | `50.7910` |
| Object Mentions | `4657` |
| Correct Object Mentions | `4433` |
| Hallucinated Object Count | `224` |
| edited images | `46` |
| edited mentions | `46` |
| object mention delta vs fixed | `-60` |
| correct mention delta vs fixed | `-44` |
| hallucinated object delta vs fixed | `-16` |
| removed hallucinated mentions | `19` |
| removed correct mentions | `27` |
| hallucination reduction per removed correct mention | `0.5926` |

Dual-caption takeaway:

- phrase-level rollback is clearly healthier than sentence-level rollback
- `dual_phrase_replace` gives up less information than removal while still reducing hallucination meaningfully
- sentence-level rollback introduces more coherence and splice issues than the phrase-level route

## 8. Unified Metric Table

| Method | CHAIRs | CHAIRi | Object Mentions | Correct Object Mentions | Hallucinated Object Count | Edited Images |
|---|---:|---:|---:|---:|---:|---:|
| `regular` | `0.2090` | `0.0657` | `4522` | `4225` | `297` | `0` |
| `fixed_first_logit` | `0.1610` | `0.0509` | `4717` | `4477` | `240` | `0` |
| `removal_top10` | `0.1290` | `0.0413` | `4580` | `4391` | `189` | `110` |
| `removal_top5` | `0.1370` | `0.0431` | `4615` | `4416` | `199` | `80` |
| `dual_phrase_replace` | `0.1400` | `0.0442` | `4637` | `4432` | `205` | `78` |
| `dual_sentence_rollback` | `0.1490` | `0.0481` | `4657` | `4433` | `224` | `46` |
| `local_regen` | `0.1610` | `0.0509` | `4717` | `4477` | `240` | `0` effective |

## 9. Object-Mention And Correct-Mention Preservation

Relative to fixed `first_logit`:

- `removal_top10`
  - hallucinated object count: `-21.3%`
  - object mentions: `-2.9%`
  - correct object mentions: `-1.9%`
- `removal_top5`
  - hallucinated object count: `-17.1%`
  - object mentions: `-2.2%`
  - correct object mentions: `-1.4%`
- `dual_phrase_replace`
  - hallucinated object count: `-14.6%`
  - object mentions: `-1.7%`
  - correct object mentions: `-1.0%`
- `dual_sentence_rollback`
  - hallucinated object count: `-6.7%`
  - object mentions: `-1.3%`
  - correct object mentions: `-1.0%`

Preservation takeaway:

- `removal_top10` gets the largest hallucination drop
- `dual_phrase_replace` is the gentlest successful action on object and correct-mention preservation
- none of the successful actions collapse caption length or object counts
- but all successful editing actions still pay a real correct-mention cost

## 10. Sample-Level Qualitative Review

Qualitative pattern summary:

- `removal_top10`
  - best raw metric improvement
  - many clean wins on obviously unsupported `first_logit_only` mentions
  - still produces harmful removals and occasional awkward truncation
- `dual_phrase_replace`
  - best overall editing quality among the actions that actually changed captions
  - more local and usually less destructive than plain removal
  - still shows phrase-level grammar glitches and some correct-object loss
- `dual_sentence_rollback`
  - can rescue some hard cases
  - but splice artifacts and content drift are clearly worse than phrase-level edits
- `local_regen`
  - no changed captions
  - no meaningful qualitative evidence either way

## 11. Which Action Is Most Promising

By raw benchmark metrics:

- `removal_top10` is the strongest pilot

By quality / preservation among actions that actually edit:

- `dual_phrase_replace` is the healthiest route

Best balanced reading:

- `removal_top10` is the current best score-seeking action
- `dual_phrase_replace` is the current best quality-preserving action

## 12. Which Action Fails And Why

Clearly weak or failed in this round:

- `local_regen`
  - failed to change captions under the current rewrite prompt
- `dual_sentence_rollback`
  - improves less than the other editing routes
  - introduces more splice and coherence problems

Borderline:

- `removal_top5`
  - healthy and conservative
  - but strictly weaker than `removal_top10` on the core metrics

## 13. Whether Any Action Should Go To Full Confirmation

Not automatically.

Current judgment:

- `removal_top10` and `dual_phrase_replace` are the only pilots worth carrying into a user-approved follow-up discussion
- `removal_top10` is strong enough to justify that discussion because it clearly beats fixed `first_logit`
- `dual_phrase_replace` is strong enough to justify that discussion because it preserves more correct mentions and looks cleaner qualitatively
- but neither route is clean enough to auto-promote to full `40504`-image confirmation in this round

Why not auto-full:

- correct-mention loss is still real
- some local edits remain awkward
- the pilot does not yet prove that the gain is independent of local object deletion cost

## 14. Caveats

- the actionable pool is first-logit-side only, so removed-hallucination hit-rate reporting is not symmetric here
- the verifier is useful but still noisy; top `10%` precision is `33.7%`, not close to a pure verifier
- local regeneration was tested only in a simple greedy rewrite form
- this is a correction-action pilot, not a final method claim

## 15. Next Recommendation

If the user wants to continue this line, the acceptable next step is a discussion between two bounded follow-ups:

- full confirmation of `removal_top10`
- or a refinement / confirmation round centered on `dual_phrase_replace`

What should stay fixed:

- weighted training-free verifier remains the primary risk signal
- classifier remains backup / diagnostic only
- no new decoding
- no automatic full run
- no Codex-initiated correction redesign without user confirmation
