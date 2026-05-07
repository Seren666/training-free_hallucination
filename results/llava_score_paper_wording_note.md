# LLaVA Score Paper Wording Note

## Safe core wording

Recommended short wording:

`We use a training-free, hand-designed mention-level risk score built from a small set of internal uncertainty, attention, and mismatch signals. The score uses fixed heuristic weights and fixed quantile slices; it is not trained on CHAIR labels. Ground-truth labels are used only for retrospective analysis and final evaluation.`

## Slightly fuller methods wording

Recommended paragraph:

`Our LLaVA verifier is a training-free rule-based heuristic rather than a learned classifier. We manually define several mention-level weighted evidence families from internal model signals, align them by a risk-versus-rescue prior, and aggregate them with fixed weights. Runtime routing uses frozen score families and frozen top-quantile operating slices. CHAIR labels are not used to fit weights or choose thresholds inside the verifier; they are used only retrospectively to analyze signal quality and to evaluate caption-editing outcomes.`

## Full-scale evaluation wording

Recommended wording for the full `40504` result:

`The full COCO-CHAIR correction results evaluate a frozen verifier-and-action pipeline at scale. The full-scale run reuses the same pre-specified weighted score families and operating slices rather than fitting a new scorer on the evaluation set.`

## Cross-model wording

Recommended wording:

`Cross-model audits suggest that the useful signal families are shared in spirit but not universally calibrated. This motivates model-adaptive training-free calibration, rather than a claim that one fixed weight set is universally optimal.`

## Retained-branch wording

Recommended wording:

`The retained LLaVA branches are selected from empirically validated training-free action variants. They are validated by full COCO-CHAIR and AMBER evaluations, but they are not the result of supervised score training.`

## Important nuance to keep

Recommended wording:

`Runtime normalization may use reference feature statistics from an existing signal table, but this does not fit the weights from labels and does not convert the verifier into a supervised model.`

## Phrases to avoid

Avoid:
- `learned weights`
- `trained verifier`
- `supervised verifier`
- `optimized on the test set`
- `score was fit on full labels`
- `universal scoring formula`
- `cross-model universal weights`
- `end-to-end trained correction score`

## Better replacements

Use instead:
- `training-free weighted heuristic`
- `hand-designed rule-based verifier`
- `fixed score family`
- `frozen operating slice`
- `retrospective label analysis`
- `model-adaptive calibration remains future work`

## Bottom line

The safest paper claim is not that the score is globally optimal. The safest claim is that it is a frozen, training-free, manually specified heuristic that was retrospectively analyzed and then validated by downstream caption-editing results.
