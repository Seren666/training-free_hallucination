# COCO-CHAIR First-Logit Mechanism Analysis

> Date: 2026-05-02
> Scope: full paired behavior analysis on existing `regular` and `first_logit` captions only.
> Boundary:
> - no new generation
> - no parameter change
> - no prompt change
> - no `The effect`

## 1. Setup

Analyzed caption files:

- `regular`:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/coco_chair/regular_caption_full.json`
- `first_logit`:
  - `/root/autodl-tmp/code/training_free_hallucination_probe/outputs/coco_chair/first_logit_caption_full.json`

Paired evaluation basis:

- same `40504` image ids
- same image order
- same evaluator logic
- same caption prompt and decoding base
- only later-step `first_logit / early-anchor` differs

## 2. Main Full Paired Summary

- total paired images:
  - `40504`
- changed caption count:
  - `40499`
- unchanged caption count:
  - `5`
- first word changed count:
  - `0`
- improved image count:
  - `5066`
- worsened image count:
  - `3287`
- no-delta stable count:
  - `32151`

Full metric deltas:

- `CHAIRs`:
  - `-0.0406`
- `CHAIRi`:
  - `-0.0142`
- hallucinated object count:
  - `11875 -> 9609`
  - delta:
    `-2266`
- average caption length:
  - `49.6823 -> 50.9320`
  - delta:
    `+1.2497`
- object mentions:
  - `181268 -> 187440`
  - delta:
    `+6172`

## 3. Object-Level Change Ranking

### 3.1 Top reduced hallucinated objects

These are the largest net reductions in hallucinated object mentions:

| Object | Net Reduction |
|---|---:|
| person | 915 |
| dining table | 705 |
| chair | 444 |
| car | 339 |
| bowl | 249 |
| cup | 214 |
| sink | 203 |
| bench | 184 |
| backpack | 184 |
| bottle | 178 |
| book | 176 |
| handbag | 159 |
| sports ball | 159 |
| truck | 158 |
| cell phone | 146 |

### 3.2 Top introduced or expanded hallucinated objects

These are the largest net additions in hallucinated object mentions:

| Object | Net Increase |
|---|---:|
| dining table | 577 |
| chair | 322 |
| couch | 218 |
| person | 205 |
| car | 198 |
| sink | 165 |
| bowl | 157 |
| refrigerator | 131 |
| cake | 118 |
| sports ball | 112 |
| tv | 111 |
| spoon | 105 |
| backpack | 100 |
| truck | 100 |
| orange | 99 |

### 3.3 Improved cases: most commonly removed hallucinations

Among improved images, the most frequently removed hallucinated objects are:

| Object | Removed Count |
|---|---:|
| person | 865 |
| dining table | 645 |
| chair | 411 |
| car | 327 |
| bowl | 222 |
| sink | 187 |
| cup | 183 |
| backpack | 168 |
| bench | 167 |
| sports ball | 155 |
| book | 155 |
| handbag | 147 |
| bottle | 141 |
| truck | 141 |
| cell phone | 122 |

### 3.4 Worsened cases: most commonly added hallucinations

Among worsened images, the most frequently newly added hallucinated objects are:

| Object | Added Count |
|---|---:|
| dining table | 496 |
| chair | 274 |
| person | 187 |
| couch | 174 |
| car | 162 |
| sink | 136 |
| bowl | 135 |
| sports ball | 104 |
| cake | 98 |
| refrigerator | 96 |
| spoon | 91 |
| tv | 91 |
| backpack | 90 |
| snowboard | 87 |
| orange | 83 |

## 4. Improved / Worsened / Stable Structure

### 4.1 Stable bucket

Stable cases are overwhelmingly hallucination-free on both sides.

- stable zero-hallucination count:
  - `29812`
- stable nonzero same-hallucination count:
  - `2339`

This means the large stable bucket is mostly:

- caption wording changed
- CHAIR outcome stayed clean

### 4.2 Improved bucket

Improved cases are not dominated by caption shortening:

- improved and longer:
  - `3178`
- improved and shorter:
  - `1288`
- improved and same token length:
  - `600`

Improved cases are also not purely "mention fewer objects":

- improved and object mentions decreased:
  - `3115`
- improved and object mentions increased:
  - `802`
- improved and object mentions stayed the same:
  - `1149`

Important positive-signal count:

- improved, while caption got longer and object mentions also increased:
  - `545`

This directly supports the claim that the gain is not reducible to caption compression.

### 4.3 Worsened bucket

Worsened cases often come with more object mentions:

- worsened and longer:
  - `1841`
- worsened and object mentions increased:
  - `2248`

Common failure mode:

- the caption becomes more elaborative
- extra kitchen / furniture / accessory nouns get inserted

## 5. Caption Behavior Distributions

### 5.1 Caption length delta distribution

Token-count delta bins:

| Delta Bin | Images |
|---|---:|
| `<= -10` | 22 |
| `-9 : -5` | 988 |
| `-4 : -1` | 9901 |
| `0` | 5331 |
| `+1 : +4` | 19304 |
| `+5 : +9` | 4774 |
| `>= +10` | 184 |

Interpretation:

- the dominant pattern is slight caption expansion
- large caption shrinkage is rare

### 5.2 Object mention delta distribution

Object-mention delta bins:

| Delta Bin | Images |
|---|---:|
| `<= -5` | 75 |
| `-4 : -2` | 4159 |
| `-1` | 7554 |
| `0` | 13177 |
| `+1` | 9557 |
| `+2 : +4` | 5897 |
| `>= +5` | 85 |

Interpretation:

- small mention increases are common
- the method does not behave like a blanket object-suppression policy

## 6. "Not Just Shorter / Not Just Fewer Objects" Checks

### 6.1 Caption shortening hypothesis

Rejected.

Evidence:

- full average caption length increases by `+1.2497`
- improved-longer count:
  - `3178`
- improved-shorter count:
  - `1288`

### 6.2 Fewer-object-mentions hypothesis

Rejected as a global explanation.

Evidence:

- total object mentions increase by `+6172`
- images with object-mention increase:
  - `15539`
- images with object-mention decrease:
  - `11788`
- improved while object mentions increased:
  - `802`
- improved while both length and object mentions increased:
  - `545`

Interpretation:

- local object pruning helps in many improved cases
- but the overall effect is better described as object-selection reshaping than global suppression

## 7. First-Word / First-Token Behavior

Observed surface behavior:

- first word changed count:
  - `0 / 40504`

Implementation-level behavior:

- `apply_to_first_generated_token = false`
- `apply_to_later_tokens_only = true`
- `the_effect_used = false`

Interpretation:

- the observed first-word invariance is consistent with the implementation
- this supports the claim that the gain is not coming from `The effect`
- the intervention acts after the first generated token, not by re-priming the first output word

## 8. Representative Examples

### 8.1 Improved examples

1. `image_id=74`
   - removed: `handbag`
   - behavior:
     keeps the dog-and-bicycle scene but removes the unsupported accessory mention.

2. `image_id=192`
   - reduced:
     `baseball glove`, `sports ball` -> `sports ball`
   - behavior:
     makes the caption more player-focused and drops one false baseball object.

3. `image_id=241`
   - removed: `chair`
   - behavior:
     preserves the living-room video-game scene but avoids extra furniture.

4. `image_id=257`
   - removed: `car`
   - behavior:
     narrows the description to the food-truck line.

5. `image_id=357`
   - removed: `sports ball`
   - behavior:
     shifts the baseball description toward player positions and actions.

6. `image_id=428`
   - removed: `dining table`
   - behavior:
     keeps the cake-centered description and removes furniture insertion.

7. `image_id=536`
   - removed: `couch`
   - behavior:
     removes furniture hallucination while preserving a rich description.

8. `image_id=692`
   - removed: `sink`
   - behavior:
     removes a bathroom fixture hallucination without shortening the description.

9. `image_id=772`
   - removed: `person`
   - behavior:
     keeps the caption centered on sheep and the fence rather than inventing a person.

10. `image_id=999`
    - removed: `sports ball`
    - behavior:
      removes a false ball mention even though the caption gets longer.

### 8.2 Worsened examples

1. `image_id=139`
   - introduced: `couch`
   - behavior:
     adds living-room furniture not supported by the scene.

2. `image_id=164`
   - introduced: `sink`
   - behavior:
     expands the kitchen inventory too aggressively.

3. `image_id=196`
   - introduced: `knife`
   - behavior:
     adds utensil detail and increases object mentions.

4. `image_id=294`
   - introduced: `toaster`, `sink`
   - behavior:
     turns a simple kitchen scene into a more hallucination-prone inventory description.

5. `image_id=338`
   - introduced: `sink`
   - behavior:
     rewrites the kitchen framing and inserts a new unsupported fixture.

6. `image_id=395`
   - introduced: `orange`
   - behavior:
     a color-word insertion becomes an object-level error under CHAIR.

7. `image_id=486`
   - `sink` becomes `spoon`, `fork`
   - behavior:
     one hallucinated item is replaced by two different hallucinated utensils.

8. `image_id=589`
   - worsens:
     `baseball bat`, `sports ball` -> `baseball bat`, `sports ball`, `sports ball`
   - behavior:
     amplifies an already bad baseball-scene hallucination pattern.

9. `image_id=775`
   - introduced: `person`
   - behavior:
     imagines a reflected person near the motorcycle.

10. `image_id=1268`
    - `bench` becomes `bench`, `bench`
    - behavior:
      duplicates an already wrong object type and worsens the count.

### 8.3 No-delta stable examples

1. `image_id=42`
   - both methods remain hallucination-free
   - behavior:
     wording changes, grounding outcome unchanged.

2. `image_id=73`
   - both methods remain hallucination-free
   - behavior:
     phrasing changes from `street` to `side of the road`.

3. `image_id=133`
   - both methods remain hallucination-free
   - behavior:
     more repetitive bed description, same CHAIR outcome.

4. `image_id=136`
   - both methods remain hallucination-free
   - behavior:
     `eating hay` becomes `eating from a feeder`.

5. `image_id=143`
   - both methods remain hallucination-free
   - behavior:
     counting style changes, object grounding stable.

6. `image_id=208`
   - both methods remain hallucination-free
   - behavior:
     toy alligator becomes toy crocodile; CHAIR remains unchanged.

7. `image_id=283`
   - both methods remain hallucination-free
   - behavior:
     stylistic rewrite with slight object-mention decrease.

8. `image_id=285`
   - both methods remain hallucination-free
   - behavior:
     keeps the same grounded object set while changing wording.

9. `image_id=328`
   - both methods remain hallucination-free
   - behavior:
     slightly different grouping of the men and book.

10. `image_id=359`
    - both methods remain hallucination-free
    - behavior:
      swaps from cars to traffic lights while staying hallucination-free under CHAIR.

## 9. Mechanism-Oriented Reading

What this full run suggests:

- later-step `first_logit / early-anchor` does not simply make captions shorter
- it does not simply reduce all object mentions
- it often removes high-frequency over-mentioned objects such as:
  - `person`
  - `dining table`
  - `chair`
  - `car`
- but it also introduces new hallucination patterns in some kitchen / furniture / accessory categories

Most useful current interpretation:

- this is a real positive caption-side intervention signal
- but it is not yet a clean selective mechanism
- the next value is in explaining:
  - when the anchor helps prune false object continuation
  - when it instead encourages extra descriptive over-expansion

## 10. Bottom Line

The full paired mechanism analysis reinforces the current high-level conclusion:

- the gain is real
- the gain is not explained by shorter captions
- the gain is not explained by fewer total object mentions
- the first word stays unchanged, so the result is not a `The effect` artifact
- the method is promising, but still mixed enough to require further mechanism analysis before being elevated to a final method claim
