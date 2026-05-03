# Strict Second-Pass Action Matrix

> Date: 2026-05-03
> Scope: strict `1000`-image pilot comparing source-aware verification and bounded correction actions across `regular`, fixed `first_logit`, and dual-caption routes. No new decoding, no fixed-first-logit retuning, no GT-driven runtime decision, no automatic full run.

## 1. Motivation

The weighted training-free mention-level verifier is now strong enough to surface high-risk object mentions on existing captions. The next question is not whether the risk signal exists, but which action is healthiest once the signal fires.

This round therefore moved from a single fixed-caption pilot to a stricter action matrix:

- compare `regular` and fixed `first_logit` high-risk pools under the same verifier
- test conservative removal on both sources
- compare fixed-side dual-caption editing against direct removal
- retry local regeneration in a bounded `v2` form without auto-scaling

## 2. Current Method Mechanism

The verifier stayed fully training-free at runtime.

- risk families:
  - `global_weighted_evidence_score`
  - `introduced_focused_weighted_score`
  - `persistent_focused_weighted_score`
  - `removed_focused_weighted_score`
- primary mention risk:
  - `primary_risk_score = max(global, introduced, persistent, removed)`
- preregistered operating slices:
  - top `5%`
  - top `10%`
  - top `20%`

No threshold search was used. No GT object presence or CHAIR label was used for any edit decision.

## 3. Why Compare Multiple Actions

The earlier fixed-side pilot already suggested a split:

- direct removal gives the strongest raw CHAIR improvement
- phrase-level dual editing preserves more correct objects
- caption-level fallback is extremely conservative but is diagnostic-only
- local regeneration looked attractive in principle but had not actually changed captions

Because these routes optimize different tradeoffs, this round kept them all active in one aligned matrix instead of prematurely choosing a single winner.

## 4. Unified Action Matrix

| Base Source | verification_only | removal_top5 | removal_top10 | dual_phrase_replace_v1 | dual_phrase_replace_strict | dual_sentence_rollback | local_regen_v2 | caption_level_fallback_diagnostic |
|---|---|---|---|---|---|---|---|---|
| `regular` | run | run | run | n/a | n/a | n/a | n/a | n/a |
| fixed `first_logit` | run | run | run | editable source | editable source | editable source | run | run |
| dual `regular + fixed_first_logit` | compare only | n/a | n/a | run | run | run | reference only | run |

Interpretation boundary:

- `caption_level_fallback_diagnostic` is not a main deployable route
- `local_regen_v2` stayed capped at `200` images
- no method may claim success if it wins only by collapsing object mentions

## 5. High-Risk Mention Pool Comparison

| Source | Mention Count | Image Count | Hallucinated Mentions | Base Hallucinated Rate | Top5 Precision / Recall | Top10 Precision / Recall | Top20 Precision / Recall |
|---|---:|---:|---:|---:|---:|---:|---:|
| `regular` | `2273` | `989` | `257` | `0.1131` | `0.4649 / 0.2062` | `0.4386 / 0.3891` | `0.3451 / 0.6109` |
| fixed `first_logit` | `2107` | `982` | `194` | `0.0921` | `0.4245 / 0.2320` | `0.3365 / 0.3660` | `0.2867 / 0.6237` |

Top-10 concentration:

- `regular`:
  - regular-only precision `0.5235`
  - common precision `0.2785`
  - dominant family `introduced_focused_weighted_score=161`
- fixed `first_logit`:
  - first-logit-only precision `0.4800`
  - common precision `0.2072`
  - dominant family `introduced_focused_weighted_score=176`

Reading:

- the verifier works on both caption sources
- the cleanest high-risk concentration is on source-exclusive mentions, not common mentions
- `regular` high-risk ranking is actually sharper than fixed on top-`10%` precision
- fixed remains the stronger base caption stream despite having the noisier risk tail

## 6. Verification-Only Results

Verification-only confirms that the weighted verifier is materially better than the base hallucination rate on both sources.

| Source | Risk Slice | Precision | Recall | Base Hallucinated Rate |
|---|---|---:|---:|---:|
| `regular` | top `5%` | `0.4649` | `0.2062` | `0.1131` |
| `regular` | top `10%` | `0.4386` | `0.3891` | `0.1131` |
| `regular` | top `20%` | `0.3451` | `0.6109` | `0.1131` |
| fixed `first_logit` | top `5%` | `0.4245` | `0.2320` | `0.0921` |
| fixed `first_logit` | top `10%` | `0.3365` | `0.3660` | `0.0921` |
| fixed `first_logit` | top `20%` | `0.2867` | `0.6237` | `0.0921` |

Main takeaways:

- verifier ranking is useful on both streams, not just fixed `first_logit`
- the strongest concentration is on source-exclusive risky mentions:
  - `regular_only`
  - `first_logit_only`
- common mentions remain much noisier and are a worse target for aggressive actions

## 7. Removal Results

### 7.1 Removal on `regular`

| Method | CHAIRs | CHAIRi | Object Mentions | Correct Object Mentions | Hallucinated Object Count | Removed Hallucinated | Removed Correct |
|---|---:|---:|---:|---:|---:|---:|---:|
| `regular` | `0.2090` | `0.0657` | `4522` | `4225` | `297` | `0` | `0` |
| `regular_removal_top5` | `0.1890` | `0.0573` | `4416` | `4163` | `253` | `44` | `60` |
| `regular_removal_top10` | `0.1620` | `0.0506` | `4350` | `4130` | `220` | `77` | `93` |

### 7.2 Removal on fixed `first_logit`

| Method | CHAIRs | CHAIRi | Object Mentions | Correct Object Mentions | Hallucinated Object Count | Removed Hallucinated | Removed Correct |
|---|---:|---:|---:|---:|---:|---:|---:|
| fixed `first_logit` | `0.1610` | `0.0509` | `4717` | `4477` | `240` | `0` | `0` |
| `firstlogit_removal_top5` | `0.1370` | `0.0431` | `4615` | `4416` | `199` | `41` | `58` |
| `firstlogit_removal_top10` | `0.1290` | `0.0413` | `4580` | `4391` | `189` | `51` | `82` |

Removal reading:

- `firstlogit_removal_top10` is the best raw metric result in the entire matrix
- `regular_removal_top10` is notable because it nearly matches fixed-baseline CHAIR scores despite starting from the weaker `regular` stream:
  - `CHAIRs 0.1620` vs fixed baseline `0.1610`
  - `CHAIRi 0.0506` vs fixed baseline `0.0509`
- removal gains are real, but they are not free:
  - correct-object loss is substantial on both sources
  - string-level artifacts still appear in qualitative review

## 8. Dual Phrase / Sentence Results

| Method | CHAIRs | CHAIRi | Object Mentions | Correct Object Mentions | Hallucinated Object Count | Edited Images | Replaced Mentions | Removed Correct |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `dual_phrase_replace_v1` | `0.1400` | `0.0442` | `4637` | `4432` | `205` | `78` | `15` | `44` |
| `dual_phrase_replace_strict` | `0.1400` | `0.0442` | `4636` | `4431` | `205` | `78` | `3` | `44` |
| `dual_sentence_rollback` | `0.1490` | `0.0481` | `4657` | `4433` | `224` | `46` | `46` | `27` |
| `caption_level_fallback_diagnostic` | `0.1530` | `0.0479` | `4698` | `4473` | `225` | `14` | `0` | `13` |

Dual-route reading:

- `dual_phrase_replace_v1` is the healthiest main dual-caption route
- the strict phrase version does not improve over `v1`
- sentence rollback preserves slightly more objects than phrase replacement, but gives back too much hallucination reduction and has more splice issues
- caption-level fallback preserves almost everything and still improves metrics, but it is diagnostic-only and only fires on `14` images

## 9. Local Regeneration v2 Results

`local_regen_v2` remained a failed pilot.

| Setting | Selected Images | Changed Captions | CHAIRs | CHAIRi | Hallucinated Object Count |
|---|---:|---:|---:|---:|---:|
| `local_regen_v2` | `200` budget, `151` selected | `0` | `0.1610` | `0.0509` | `240` |

Conclusion:

- even after switching to a more explicit targeted rewrite prompt, the model effectively returned the original caption
- this route should stay paused unless the user explicitly wants a different rewrite formulation

## 10. Unified Metrics Table

| Method | Base Source | CHAIRs | CHAIRi | Object Mentions | Correct Object Mentions | Hallucinated Object Count | Object Delta vs Source | Correct Delta vs Source | Edited Images |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `regular` | `regular` | `0.2090` | `0.0657` | `4522` | `4225` | `297` | `0` | `0` | `0` |
| fixed `first_logit` | fixed `first_logit` | `0.1610` | `0.0509` | `4717` | `4477` | `240` | `0` | `0` | `0` |
| `regular_removal_top5` | `regular` | `0.1890` | `0.0573` | `4416` | `4163` | `253` | `-106` | `-62` | `81` |
| `regular_removal_top10` | `regular` | `0.1620` | `0.0506` | `4350` | `4130` | `220` | `-172` | `-95` | `137` |
| `firstlogit_removal_top5` | fixed `first_logit` | `0.1370` | `0.0431` | `4615` | `4416` | `199` | `-102` | `-61` | `80` |
| `firstlogit_removal_top10` | fixed `first_logit` | `0.1290` | `0.0413` | `4580` | `4391` | `189` | `-137` | `-86` | `110` |
| `dual_phrase_replace_v1` | fixed `first_logit` | `0.1400` | `0.0442` | `4637` | `4432` | `205` | `-80` | `-45` | `78` |
| `dual_phrase_replace_strict` | fixed `first_logit` | `0.1400` | `0.0442` | `4636` | `4431` | `205` | `-81` | `-46` | `78` |
| `dual_sentence_rollback` | fixed `first_logit` | `0.1490` | `0.0481` | `4657` | `4433` | `224` | `-60` | `-44` | `46` |
| `caption_level_fallback_diagnostic` | fixed `first_logit` | `0.1530` | `0.0479` | `4698` | `4473` | `225` | `-19` | `-4` | `14` |
| `local_regen_v2` | fixed `first_logit` | `0.1610` | `0.0509` | `4717` | `4477` | `240` | `0` | `0` | `0` |

## 11. Quality Review

The remote qualitative review directly covered two candidates:

- `firstlogit_removal_top10`
- `caption_level_fallback_diagnostic`

Observed quality pattern:

- `firstlogit_removal_top10`
  - strongest raw metric improvement
  - many clean successes on obvious introduced kitchen / furniture / utensil objects
  - still shows awkward local deletions such as malformed `Wii remote`, dropped spaces, or partially damaged noun phrases
- `caption_level_fallback_diagnostic`
  - often very clean when it fires
  - preserves correct objects extremely well
  - but only edits `14` images and is not a main deployable action

Quality judgment for the remaining main methods is therefore partly metric-backed rather than fully example-backed:

- `dual_phrase_replace_v1` is the best qualitative main candidate because it:
  - preserves more correct objects than removal
  - edits fewer mentions
  - avoids many of the phrase-destruction artifacts seen in direct removal
- `dual_sentence_rollback` is weaker qualitatively because it is more exposed to sentence-splice drift

## 12. Which Action Has Best Raw Score

Best raw score action:

- `firstlogit_removal_top10`

Why:

- best `CHAIRs = 0.1290`
- best `CHAIRi = 0.0413`
- lowest hallucinated object count `189`

## 13. Which Action Best Preserves Correct Objects

Absolute best preservation:

- `caption_level_fallback_diagnostic`
  - correct-object delta `-4`
  - object-mention delta `-19`

But this is not the main method candidate because it is diagnostic-only.

Best preservation among main candidate methods:

- `dual_phrase_replace_v1`
  - correct-object delta `-45`
  - object-mention delta `-80`

This is materially healthier than `firstlogit_removal_top10`:

- correct-object delta `-86`
- object-mention delta `-137`

## 14. Which Action Has Best Qualitative Quality

Cleanest overall edits:

- `caption_level_fallback_diagnostic`

Best qualitative main action:

- `dual_phrase_replace_v1`

Reason:

- it keeps the edit local
- it avoids many deletion artifacts
- it preserves more supported content than direct removal
- it still gives a real hallucination reduction over fixed `first_logit`

## 15. Whether Any Action Should Enter Full Confirmation

Not automatically.

This round is enough to justify a user-approved full-confirmation discussion, but not an auto-full run.

If the project does continue, the clean comparison should be:

1. `firstlogit_removal_top10` for best raw CHAIR improvement
2. `dual_phrase_replace_v1` for best preservation / quality among main routes
3. optional `caption_level_fallback_diagnostic` only as a preservation reference, not as the primary deployable method

Routes that should not advance as main candidates:

- `local_regen_v2`
- `dual_sentence_rollback`
- `dual_phrase_replace_strict`

## 16. Caveats

- all results are still pilot-scale:
  - `1000` images for removal and dual methods
  - `200` image budget for `local_regen_v2`
- the verifier is sharper on source-exclusive mentions than on common mentions
- the best fixed-side raw gain still costs non-trivial correct-object loss
- the local qualitative review was auto-collected for two candidates, so `dual_phrase_replace_v1` has less direct example coverage than ideal in this report

## 17. Next Recommendation

Keep the current boundaries:

- weighted training-free verifier remains the primary evidence source
- classifier remains backup only
- do not auto-start full confirmation
- do not let Codex choose a correction route unilaterally

If the user wants the next step, the most justified discussion is:

- raw-score-first full confirmation of `firstlogit_removal_top10`
- versus quality-preserving full confirmation of `dual_phrase_replace_v1`
- with `caption_level_fallback_diagnostic` retained only as a reference ceiling for preservation
