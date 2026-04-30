# One-Forward Signal Audit Plan

> Goal: verify whether one normal forward already contains enough information to estimate object hallucination risk on POPE, before designing any new intervention.
> Stage rule: no new method implementation in this phase.
> Constraint rule: avoid training classifiers and avoid POPE-specific rule engineering that will not transfer beyond the benchmark.

## 0. Current benchmark reading after the full first-logit POPE run

The completed `regular` vs `first_logit` POPE reproduction gives an important benchmark-usage conclusion:

- POPE is **not** a suitable benchmark for evaluating a faithful later-step first-logit baseline under the current one-word yes/no protocol
- the decisive answer is usually fixed by the first answer token
- a later-step-only first-logit boost therefore has no practical action space on this benchmark

This should update how POPE is used in the project:

- keep POPE as the first `one-forward answer-boundary signal audit` benchmark
- do **not** keep using POPE as the main benchmark for later-step first-logit intervention scoring
- on POPE, the next focus should be false-positive hallucination cases and their internal signals, especially `absent-but-answered-yes`

Operational consequence:

- prioritize first-answer / pre-answer signals
- treat later-step token effects on POPE as secondary or mostly diagnostic
- do not continue tuning later-step first-logit boosting on POPE

## 1. Core audit setup

### Target model and benchmark

- model family: start with LLaVA-1.5
- benchmark: POPE
- scope of this phase: diagnostic logging and signal separation only

### POPE label definitions for this audit

At sample level:

- positive sample: the queried object is present
- negative sample: the queried object is absent
- hallucination sample: a negative sample answered as if the object is present, typically a false `yes`

At the first POPE stage, because output is usually binary:

- primary decision token pair: `yes` vs `no`
- primary object handle: the queried object noun in the question

This is a benchmark-specific measurement surface, not the final desired method definition. Later, when moving to open-ended benchmarks, the same signal family should be checked on generated object tokens rather than only `yes`/`no`.

### Logging principle

Use one normal forward only. Read extra information from that same forward through:

- logits
- hidden states
- attentions
- layer-wise projections using the same hidden states

Do not trigger:

- contrastive second forward
- image perturbation branch
- trained detector
- learned router

### Instrumentation rule

Phase-1 logging options:

- `output_hidden_states=True` when the signal needs layer-wise state access
- `output_attentions=True` when the signal needs attention/head analysis

For memory control:

- first run a small audited subset
- enable only the flags needed for the current signal family
- do not turn every hook on for full-scale evaluation at once

## 2. Anti-overfitting rules

### How to avoid training a classifier

Use only:

- single scalar scores
- rank-based statistics
- threshold-free separability metrics such as AUC
- simple correlation analysis
- fixed, human-readable score formulas if later combining signals

Do not use:

- learned MLPs
- logistic regression
- tuned routing classifiers

### How to avoid benchmark engineering

- do not fit different thresholds per POPE split in the first audit
- do not use COCO ground-truth labels at inference time
- do not build custom if-else rules tied only to POPE wording
- prefer signals that can later transfer from binary POPE answers to open-ended object tokens
- keep the first pass descriptive and statistical, not leaderboard-driven

## 3. Signal-by-signal audit plan

## 3.1 First-logit support

### What to read

- first answer-step logits
- `yes` / `no` logit margin at the first decision step
- support rank or logit value for queried-object-related tokens if projected from the same early state

### One forward enough?

- yes

### Need attentions / hidden states?

- attentions: no
- hidden states: optional

### POPE signal definition

Risk intuition:

- final `yes` confidence high
- but first-step support is weak or inconsistent

For POPE, compare:

- correct positive: object present, model says `yes`
- correct negative: object absent, model says `no`
- hallucination: object absent, model says `yes`

### No-classifier version

- scalar score: low first-step `yes` support combined with later strong `yes`
- report AUC or distribution overlap, not a learned boundary

### Minimal experiment

- log first-step top-k logits and `yes/no` margin on a small POPE subset
- test whether false-positive hallucination samples show weaker early support than correct positives

## 3.2 Middle-layer visual support

### What to read

- middle-layer attentions from answer-relevant tokens to image tokens
- hidden-state similarity between the queried-object representation and image-token representations
- layer-wise object support projected from middle-layer hidden states

### One forward enough?

- yes

### Need attentions / hidden states?

- attentions: yes
- hidden states: yes

### POPE signal definition

Because POPE answers are binary, use the queried object noun from the question as the object anchor.

Risk intuition:

- the model answers `yes`
- but middle layers show weak image-token support for the queried object

### No-classifier version

- mean image-attention mass
- top-k image-token cosine similarity
- middle-layer object support rank

### Minimal experiment

- compare absent-yes vs absent-no vs present-yes on a small subset
- inspect a fixed middle-layer window rather than tuning layers per split
- prioritize absent-yes false positives rather than chasing split-level score gains

## 3.3 Visual-text alignment

### What to read

- queried-object token hidden state
- image-token hidden states
- similarity or alignment statistics between them

### One forward enough?

- yes

### Need attentions / hidden states?

- attentions: optional
- hidden states: yes

### POPE signal definition

Use the queried object token in the question as the text anchor.

Risk intuition:

- hallucination samples should show weaker alignment between the queried-object text representation and image-token representations than correct positive samples

### No-classifier version

- max similarity to image tokens
- mean similarity of top-k image tokens
- consistency of top aligned image tokens across nearby layers

### Minimal experiment

- measure alignment curves across layers for the three POPE sample groups
- check whether hallucination samples fail earlier than correct positives

## 3.4 Head consistency

### What to read

- head-wise attention maps from object-relevant or answer-relevant positions to image tokens
- cross-head similarity
- head-wise entropy over attended image regions

### One forward enough?

- yes

### Need attentions / hidden states?

- attentions: yes
- hidden states: optional

### POPE signal definition

Risk intuition:

- on hallucination samples, heads may attend to inconsistent or noisy image regions while still ending in a strong `yes`

### No-classifier version

- head-to-head map similarity
- entropy across heads
- fraction of heads that meaningfully attend to image tokens

### Minimal experiment

- audit a small fixed set of layers and heads
- identify whether absent-yes samples have higher head disagreement than present-yes samples

## 3.5 Layer-wise distribution shift

### What to read

- projected token distributions from selected middle layers
- final-layer token distribution
- rank shifts for `yes`, `no`, and queried-object-related tokens

### One forward enough?

- yes

### Need attentions / hidden states?

- attentions: no
- hidden states: yes

### POPE signal definition

Risk intuition:

- middle layers do not strongly support the eventual answer
- final layer sharply shifts toward `yes`

### No-classifier version

- KL or JS divergence between projected middle-layer distribution and final distribution
- rank jump size for `yes`
- support gap between `yes` and `no`

### Minimal experiment

- choose a few layer checkpoints, such as early, middle, late
- measure whether hallucination samples have larger middle-to-final shifts

## 3.6 Late emergence

### What to read

- layer-wise score trajectory for the final chosen answer token
- optionally, trajectory of queried-object-related support

### One forward enough?

- yes

### Need attentions / hidden states?

- attentions: no
- hidden states: yes

### POPE signal definition

Risk intuition:

- `yes` is not strong early or middle
- then becomes strong only in late layers

### No-classifier version

- late-rise score
- last-third minus middle-third support gap
- earliest layer where `yes` enters top-k

### Minimal experiment

- compare late-rise profiles for absent-yes, absent-no, and present-yes samples
- keep this as an internal-signal analysis, not as justification for another POPE later-step intervention sweep

## 3.7 Token ranking trajectory

### What to read

- rank of `yes`, `no`, and queried-object-related tokens across layers
- if generation includes more than one step, also track across the first few decode steps

### One forward enough?

- yes for layer trajectory
- mostly yes for short POPE generation, because answer length is usually minimal

### Need attentions / hidden states?

- attentions: no
- hidden states: yes

### POPE signal definition

Risk intuition:

- hallucination may appear as `yes` steadily rising while `no` stays competitive and then loses late

### No-classifier version

- rank slope
- crossover layer
- time-to-top-k

### Minimal experiment

- focus first on the answer boundary, not long free-form continuation
- report a few interpretable trajectory templates rather than tuning scores aggressively
- because POPE answer strings are short, layer-wise trajectory is more important here than multi-step decode trajectory

## 3.8 Hidden genuine competition

### What to read

- whether `no` remains highly ranked inside negative samples that are finally answered as `yes`
- whether the model internally keeps a competitive non-hallucinated alternative before final selection

### One forward enough?

- yes

### Need attentions / hidden states?

- attentions: optional
- hidden states: yes

### POPE signal definition

At the POPE stage, `hidden genuine competition` is best instantiated as:

- a negative sample where `no` remains competitive for much of the layer trajectory
- but late decoding still selects `yes`

This keeps the idea close to the object-hallucination question without training a separate detector.

### No-classifier version

- competitive-layer count for `no`
- minimal rank gap between `yes` and `no`
- whether `no` is still in top-k shortly before the final layer

### Minimal experiment

- inspect absent-yes failures first
- verify whether there is a suppressed truthful alternative rather than complete absence of truthful evidence

## 3.9 Visual sensitivity

### What to read

Strict visual sensitivity usually asks whether token probability changes when visual input changes.

### One forward enough?

- strict version: no
- one-forward proxy version: only partially

### Need attentions / hidden states?

- for proxy analysis, yes if using internal reliance measures

### POPE signal definition

Phase-1 plan:

- do not treat this as a core one-forward signal
- instead, keep it as a later validation concept

Possible proxy within one forward:

- how much the answer-relevant computation actually routes through image tokens
- whether image-token support is thin despite high final confidence

### No-classifier version

- use it only as a descriptive cross-check in Phase 1
- reserve any true perturbation-based sensitivity test for a later, explicitly non-one-forward follow-up

### Minimal experiment

- postpone strict visual-sensitivity measurement
- if needed later, compare against already existing legacy VCD observations rather than making it the first audit target

## 4. Suggested audit order

The safest first audit order is:

1. first-logit support
2. layer-wise distribution shift
3. late emergence
4. token ranking trajectory
5. middle-layer visual support
6. visual-text alignment
7. head consistency
8. hidden genuine competition
9. visual sensitivity proxy only

Reason:

- the first four are the cheapest to inspect from one forward
- they directly test the early-anchor hypothesis
- they align with the updated POPE role as an answer-boundary audit benchmark
- they let us decide whether deeper attention instrumentation is worth the extra logging cost

## 5. Minimal phase-1 experiment package

Once GPU access is restored, the first audit should stay small:

- benchmark slice: a small POPE subset before any full run
- output: only lightweight summary tables and notes
- statistics:
  - per-signal scalar distributions
  - AUC or rank-separation statistics
  - a few representative success/failure cases

Success criterion for Phase 1:

- at least one or two single-forward signals separate hallucination failures from non-failures with interpretable and reasonably stable behavior

If that fails:

- do not jump straight to a new intervention
- first check whether the signal failed because POPE is too binary, or because the one-forward hypothesis is too weak
