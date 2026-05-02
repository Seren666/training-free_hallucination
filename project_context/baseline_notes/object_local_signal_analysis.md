# Object Local Signal Analysis

> Date: 2026-05-02
> Scope: object-local token-step probe on existing full COCO-CHAIR paired captions only.
> Boundary:
> - no caption regeneration
> - no first-logit method change
> - no parameter tuning
> - no `The effect`
> - no full attention / hidden-state persistence

## 1. Why Local Probe

The earlier `3000`-image one-forward scalar audit showed:

- coarse image-level signals are weak
- `improved` vs `worsened` separation is near-random

So this round moved to a more local question:

- at the specific object mention step,
- do logits, first-anchor support, visual attention, and hidden-image alignment
- separate:
  - `removed_hallucination`
  - `introduced_hallucination`
  - `persistent_hallucination`
  - `correct_object_mention`

## 2. Subset Construction

Remote event table:

- `/root/autodl-tmp/code/training_free_hallucination_probe/results/object_event_table.csv`

Remote probe subset:

- `/root/autodl-tmp/code/training_free_hallucination_probe/results/object_local_probe_subset.csv`

Sampling:

- fixed seed:
  - `55`
- per class:
  - `1000`

Final subset:

- `removed_hallucination`: `1000`
- `introduced_hallucination`: `1000`
- `persistent_hallucination`: `1000`
- `correct_object_mention`: `1000`

## 3. Probe Setup

Remote probe script:

- `/root/autodl-tmp/code/training_free_hallucination_probe/coco_object_local_signal_probe.py`

Remote analysis script:

- `/root/autodl-tmp/code/training_free_hallucination_probe/analyze_object_local_signals.py`

Prompt stayed identical to caption generation:

- `Please describe the image.`

Important implementation choice:

- teacher-forcing / prefix scoring style analysis only
- no new captions generated
- no full attention tensors saved
- no full hidden states saved
- only per-event aggregated statistics saved

## 4. Completion Status

Remote outputs:

- probe csv:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/object_local_signal_probe.csv`
- analysis markdown:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/object_local_signal_analysis.md`
- analysis csv:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/object_local_signal_analysis.csv`
- analysis json:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/object_local_signal_analysis.json`

Probe completion:

- total rows:
  - `4000`
- valid rows analyzed:
  - `4000`
- failed rows:
  - `0`

So the local probe finished cleanly on the full sampled subset.

## 5. Signals Collected

Per object event, the probe logged:

- metadata:
  - image id
  - object category
  - event type
  - caption source
  - mention position ratio
- current-step object-token statistics:
  - target token probability
  - target token rank
  - entropy
  - top1-top2 margins
- first-anchor support:
  - target token rank under anchor
  - anchor adjustment delta
  - overlap between anchor top-10 and object-step top-10
  - implied adjusted target rank if the fixed first-logit formula were applied
- visual attention:
  - middle / late image attention mass
  - attention entropy summaries
- hidden-image alignment:
  - middle / late hidden-image cosine
  - middle-to-late alignment change

## 6. Group-Level Means

| Signal | Removed | Introduced | Persistent | Correct |
|---|---:|---:|---:|---:|
| target token prob | 0.4396 | 0.4431 | 0.5357 | 0.6150 |
| target token rank | 1.0050 | 1.3380 | 1.0050 | 1.0260 |
| entropy | 2.2317 | 2.1495 | 1.8306 | 1.4687 |
| anchor target rank | 10077.3290 | 7705.1190 | 7541.4470 | 4459.1230 |
| anchor weight at object step | 0.2593 | 0.2558 | 0.2051 | 0.1591 |
| adjusted target rank if applied | 1.4670 | 1.0210 | 1.1710 | 1.0980 |
| middle image attention | 0.1487 | 0.1451 | 0.1619 | 0.1836 |
| late image attention | 0.1312 | 0.1263 | 0.1255 | 0.1291 |
| hidden-image cosine middle | 0.2622 | 0.2701 | 0.2615 | 0.2498 |
| hidden-image cosine late | 0.4727 | 0.4758 | 0.4672 | 0.4709 |
| mention position ratio | 0.7129 | 0.6952 | 0.4552 | 0.3226 |

## 7. What Separates Removed vs Introduced

This is the most important comparison for future selective intervention.

Best separators:

1. `adjusted_target_rank_if_applied`
   - removed vs introduced AUC:
     `0.6512`
2. `anchor_target_token_rank`
   - AUC:
     `0.6147`
3. `target_token_rank`
   - AUC:
     `0.3928`
   - equivalent directional separation because introduced events have worse raw current-step rank
4. `anchor_adjustment_delta`
   - AUC:
     `0.4005`
   - again directional evidence that introduced events get stronger anchor push

Interpretation:

- introduced hallucinations are not mainly explained by stronger visual grounding
- instead, they show stronger early-anchor support than removed hallucinations
- and under the fixed first-logit formula, they are more likely to be pushed toward top-1 at the object step

This is exactly the kind of object-local effect the coarse image-level audit could not see.

## 8. Persistent vs Removed

Best separators:

1. `anchor_weight_at_object_step`
   - AUC:
     `0.2267`
   - directional reading:
     persistent mentions happen earlier and get smaller anchor weight
2. `mention_position_ratio`
   - AUC:
     `0.2270`
   - removed events happen later in the caption
3. `target_token_probability`
   - AUC:
     `0.6037`
4. `top1_top2_probability_margin`
   - AUC:
     `0.5981`

Interpretation:

- removed hallucinations tend to occur later, where the later-step first-logit weight is larger
- persistent hallucinations tend to be more entrenched at the local token step:
  - higher target-token probability
  - lower entropy
  - larger confidence margin

So some failures survive not because the anchor is absent, but because the local object token is already too strong.

## 9. Hallucinated vs Correct

Best separators:

1. `anchor_weight_at_object_step`
   - AUC:
     `0.7865`
2. `mention_position_ratio`
   - AUC:
     `0.7861`
3. `anchor_target_token_rank`
   - AUC:
     `0.7450`
4. `image_attention_middle_mean`
   - AUC:
     `0.2845`
   - directional reading:
     correct mentions have higher middle-layer image attention mass

Interpretation:

- hallucinated object mentions are much more likely to occur later in the caption
- they therefore receive larger first-logit weight
- correct mentions have:
  - higher local token probability
  - lower entropy
  - stronger middle-layer image attention

So hallucinated vs correct is substantially more separable at object-local level than at coarse image-level.

## 10. Useful Signals vs Weak Signals

Signals that look useful:

- `mention_position_ratio`
- `anchor_weight_at_object_step`
- `anchor_target_token_rank`
- `adjusted_target_rank_if_applied`
- `target_token_rank` for removed vs introduced

Signals that remain weak:

- late-layer image attention
- late-layer hidden-image cosine
- middle-to-late alignment change
- anchor top-10 overlap

So the strongest current story is not:

- "better visual attention explains everything"

but rather:

- object-local position and anchor-support structure matter more than coarse late-layer scalar summaries

## 11. Frequent Categories in the Probe

Removed-heavy sampled categories:

- `person`
- `dining table`
- `chair`
- `car`

Introduced-heavy sampled categories:

- `dining table`
- `chair`
- `person`
- `car`
- `couch`
- `refrigerator`
- `sink`

Persistent-heavy sampled categories:

- `dining table`
- `chair`
- `sports ball`
- `person`
- `couch`

This is consistent with the earlier event-level reading:

- the method often helps by pruning high-frequency over-mentions
- but can also introduce plausible indoor / kitchen / furniture nouns

## 12. Main Takeaway

Compared with the earlier image-level scalar audit, the object-local probe is clearly more informative.

What it supports:

- `first_logit / early-anchor` acts in a genuinely object-local way
- introduced hallucinations receive stronger anchor support than removed hallucinations
- removed hallucinations tend to occur later, where the fixed later-step weight is larger
- persistent hallucinations are more locally entrenched
- correct object mentions are more visually grounded than hallucinated ones, especially at middle-layer image attention

What it does not yet support:

- a final selective intervention rule
- a classifier
- threshold-based routing

## 13. Recommendation

Current best next step:

- keep the fixed first-logit method unchanged
- use this object-local picture for mechanism analysis first
- if doing a future selective pilot, start from:
  - object-local position
  - anchor target rank / support
  - implied adjusted target rank

So the current evidence is:

- stronger than the earlier image-level scalar audit
- promising for future selective early-anchor
- but still not enough to claim a finished selector or final method.
