# Current Core Results Table

> Date: 2026-05-02
> Scope: condensed view of the current benchmark conclusions after the completed POPE and COCO-CHAIR work.

## 1. POPE First-Logit

| Benchmark | Scope | Methods | Result | Current Conclusion | Current Role |
|---|---|---|---|---|---|
| POPE 9 splits | COCO / GQA / A-OKVQA x random / popular / adversarial | `regular`, faithful later-step `first_logit` adaptation | `delta = 0` on all `9/9` splits | POPE is not suitable for later-step `first_logit` intervention evaluation under one-word yes/no decoding | keep POPE as `answer-boundary` / `pre-answer` / false-positive signal-audit benchmark |

Key POPE takeaway:

- `first_logit` on POPE did not improve or worsen any split
- the likely reason is protocol-level:
  - the decisive answer is usually fixed at the first answer token
  - later-step boosting has no room to act

## 2. COCO-CHAIR Regular Baseline

| Stage | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Object Count | Note |
|---|---:|---:|---:|---:|---:|---:|---|
| pilot | 100 | 0.2100 | 0.0533 | 49.9100 | 450 | 24 | first open-ended caption hallucination pilot |
| full | 40504 | 0.2037 | 0.0655 | 49.6823 | 181268 | 11875 | full regular caption baseline |

## 3. COCO-CHAIR First-Logit

| Stage | Images | CHAIRs | CHAIRi | Avg Caption Length | Object Mentions | Hallucinated Object Count | Delta vs regular |
|---|---:|---:|---:|---:|---:|---:|---|
| pilot | 100 | 0.1500 | 0.0465 | 51.3100 | 452 | 21 | positive signal |
| prefix | 500 | 0.1440 | 0.0429 | 51.0380 | 2356 | 101 | positive |
| prefix | 1000 | 0.1610 | 0.0509 | 50.9190 | 4717 | 240 | positive |
| full | 40504 | 0.1631 | 0.0513 | 50.9320 | 187440 | 9609 | stable positive full confirmation |

## 4. Current Main Conclusions

### 4.1 Benchmark split

- `COCO-CHAIR` is now the main positive benchmark for `first_logit / early-anchor`
- `POPE` is retained for one-forward signal audit, not for later-step first-logit intervention scoring
- `AMBER` remains deferred

### 4.2 Method status

- `first_logit / early-anchor` is a promising intervention candidate
- it is not yet the final paper method
- it should not yet be presented as a fully established final conclusion

### 4.3 Why the current COCO-CHAIR result matters

- the effect remains positive from `100` to `500` to `1000` to `40504`
- `CHAIRs` and `CHAIRi` both improve
- captions do not get shorter on average
- object mentions do not go down on average
- first word remains unchanged

### 4.4 What is no longer the main line

- do not continue old `VCD / RAD-VCD` as the main paper line
- do not keep tuning `POPE first_logit`
- do not use `The effect` as the main explanation path

## 5. Current Recommended Next Step

1. do evaluator alignment for the current adapted CHAIR pipeline
2. do mechanism analysis on the full paired COCO-CHAIR outputs
3. then return to `one-forward signal audit`
4. do not immediately start parameter sweep or new benchmark expansion
