# Object-Level Event Analysis

> Date: 2026-05-02
> Scope: object-event reconstruction on existing full COCO-CHAIR paired captions only.
> Boundary:
> - no caption regeneration
> - no first-logit method change
> - no parameter tuning
> - no `The effect`

## 1. Why Object-Level Analysis

The image-level `3000`-sample one-forward scalar audit already showed that coarse prompt-state summaries are weak separators for:

- `improved` vs `worsened`
- and only modestly separate `changed` vs `stable`

That makes the next question more local:

- not whether an image is globally "easy" or "hard"
- but which object mentions are:
  - removed hallucinations
  - introduced hallucinations
  - persistent hallucinations
  - correct object mentions

So this round reconstructs explicit object events from the existing full paired captions and evaluator outputs before doing any deeper internal probe.

## 2. Event Table Construction

Remote source captions:

- `regular`:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/coco_chair/regular_caption_full.json`
- `first_logit`:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/coco_chair/first_logit_caption_full.json`

Remote event builder:

- `/root/autodl-tmp/code/training_free_hallucination_probe/build_object_event_table.py`

Remote outputs:

- full event table:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/object_event_table.csv`
- summary csv:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/object_event_summary.csv`
- summary markdown:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/object_event_summary.md`
- summary json:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/results/object_event_summary.json`

Each event row is keyed by `image_id + object_category + event_type`.

Event types:

- `removed_hallucination`
- `introduced_hallucination`
- `persistent_hallucination`
- `correct_object_mention`

Each row stores:

- paired captions
- GT object set
- hallucinated object sets on both sides
- generated object mentions on both sides
- mention span metadata when recoverable
- a chosen caption source for later object-local probing

## 3. Event Counts

| Event Type | Count |
|---|---:|
| `correct_object_mention` | 86458 |
| `removed_hallucination` | 6043 |
| `introduced_hallucination` | 3880 |
| `persistent_hallucination` | 3924 |

Immediate read:

- the positive effect is not rare at object level:
  - there are `6043` removed hallucination events
- but the method is not uniformly corrective:
  - there are also `3880` introduced hallucination events
- and a nontrivial set of hallucinations survive unchanged:
  - `3924` persistent events

## 4. Top Removed / Introduced / Persistent Objects

### 4.1 Top removed hallucinated objects

| Object | Count |
|---|---:|
| `person` | 775 |
| `dining table` | 472 |
| `chair` | 382 |
| `car` | 258 |
| `bowl` | 214 |
| `cup` | 200 |
| `bottle` | 169 |
| `backpack` | 168 |
| `sink` | 163 |
| `book` | 162 |
| `bench` | 158 |
| `handbag` | 151 |
| `truck` | 141 |
| `cell phone` | 131 |
| `tie` | 127 |
| `sports ball` | 125 |

### 4.2 Top introduced hallucinated objects

| Object | Count |
|---|---:|
| `dining table` | 375 |
| `chair` | 279 |
| `couch` | 168 |
| `sink` | 146 |
| `person` | 144 |
| `car` | 137 |
| `bowl` | 128 |
| `refrigerator` | 123 |
| `spoon` | 97 |
| `backpack` | 94 |
| `tv` | 94 |
| `truck` | 93 |
| `tie` | 88 |
| `orange` | 85 |
| `cake` | 84 |

### 4.3 Top persistent hallucinated objects

| Object | Count |
|---|---:|
| `dining table` | 859 |
| `chair` | 236 |
| `sports ball` | 166 |
| `person` | 165 |
| `orange` | 148 |
| `couch` | 138 |
| `car` | 128 |
| `sink` | 119 |
| `bowl` | 103 |
| `refrigerator` | 95 |

### 4.4 Top correct objects

| Object | Count |
|---|---:|
| `person` | 19965 |
| `dining table` | 5455 |
| `car` | 2462 |
| `chair` | 2277 |
| `sports ball` | 1660 |
| `cat` | 1425 |
| `laptop` | 1398 |
| `sink` | 1345 |
| `dog` | 1340 |
| `bowl` | 1330 |

## 5. Category Overlap

Removed and introduced hallucinations overlap on `79` object categories.

This matters because the effect is not:

- "always suppress object X"
- or "always amplify object Y"

Instead, some high-frequency categories are mixed:

- often removed in some contexts
- introduced in others
- persistent in still others

The strongest example is `dining table`:

- removed:
  - `472`
- introduced:
  - `375`
- persistent:
  - `859`
- correct:
  - `5455`

So the method clearly interacts with context, not just with a static object blacklist.

## 6. Focus Objects

| Object | Removed | Introduced | Persistent | Correct |
|---|---:|---:|---:|---:|
| `person` | 775 | 144 | 165 | 19965 |
| `dining table` | 472 | 375 | 859 | 5455 |
| `chair` | 382 | 279 | 236 | 2277 |
| `car` | 258 | 137 | 128 | 2462 |
| `couch` | 84 | 168 | 138 | 1175 |
| `sink` | 163 | 146 | 119 | 1345 |
| `refrigerator` | 71 | 123 | 95 | 586 |
| `spoon` | 113 | 97 | 47 | 349 |
| `tv` | 59 | 94 | 21 | 1066 |
| `bowl` | 214 | 128 | 103 | 1330 |
| `handbag` | 151 | 57 | 38 | 472 |
| `toaster` | 33 | 37 | 24 | 40 |

## 7. Key Observations

### 7.1 What first-logit seems to remove best

The method most clearly removes frequent over-mentioned nouns such as:

- `person`
- `dining table`
- `chair`
- `car`
- `bowl`

These are exactly the kinds of objects that are easy to insert as generic scene fillers.

### 7.2 What it can also introduce

The main failure additions are scene-related but absent nouns, especially:

- furniture:
  - `chair`, `couch`, `dining table`
- kitchen objects:
  - `sink`, `refrigerator`, `spoon`
- indoor scene expansions:
  - `tv`
- accessory / food detail:
  - `orange`, `cake`

This matches the earlier paired-caption reading:

- good cases often prune common over-mentions
- bad cases often elaborate the scene with plausible but absent detail nouns

### 7.3 Improved and worsened behavior is category-dependent

The data already suggests:

- improvements concentrate partly in generic high-frequency over-mentions
- worsened cases concentrate partly in furniture / kitchen / accessory elaboration

So the method is neither:

- a pure anti-hallucination suppressor
- nor a pure verbosity effect

It changes object-local token behavior in a category- and context-dependent way.

## 8. Why Image-Level Scalar Was Insufficient

The earlier image-level scalar audit asked whether coarse prompt-state summaries could separate:

- `improved`
- `worsened`
- `stable`

That mostly failed.

This event analysis shows why that failure is unsurprising:

- the same image can contain multiple object decisions
- the gain or loss is often concentrated in a specific noun mention
- the important distinction is local:
  - whether a particular object token is strongly supported
  - whether it is visually grounded
  - whether the early anchor reinforces it

So the more promising next step is:

- not another image-level scalar
- but an object-local token-step probe on:
  - `removed_hallucination`
  - `introduced_hallucination`
  - `persistent_hallucination`
  - `correct_object_mention`

## 9. Current Takeaway

At object-event level, the full COCO-CHAIR result looks structurally real:

- `first_logit / early-anchor` removes many hallucinated object mentions
- it also introduces a smaller but substantial set of new hallucinated mentions
- persistent failures remain
- the effect is strongly object-category- and context-dependent

This supports moving from:

- image-level coarse signal audit

to:

- object-local token analysis

as the right next mechanism-analysis step.
