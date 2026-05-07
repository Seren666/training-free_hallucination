# LLaVA COCO-CHAIR vs AMBER Cross-Dataset Analysis

## 1. Are method trends consistent across COCO-CHAIR and AMBER

Yes, directionally.

Across full COCO-CHAIR, FLB-aligned COCO-CHAIR-500, and AMBER full:
- fixed / FLB-equivalent improves over `regular`
- all three retained branches improve over fixed / FLB-equivalent
- `firstlogit_removal_top10` is the most metric-aggressive branch
- `dual_phrase_replace_v1` and Candidate A are the more conservative retained branches

The exact margins differ by dataset, but the method ordering and qualitative tradeoff structure are stable.

## 2. Does fixed / FLB improve regular on both datasets

Yes.

On full COCO-CHAIR:
- `CHAIRs: 0.2037 -> 0.1631`
- `CHAIRi: 0.0655 -> 0.0513`
- `hallucinated: 11875 -> 9609`
- `correct: 169393 -> 177831`

On AMBER full:
- `CHAIR: 7.0 -> 4.8`
- `Hal: 32.3 -> 24.5`
- `Cog: 3.8 -> 2.2`

AMBER also shows the same basic cost pattern seen elsewhere:
- improved hallucination metrics
- some `Cover` reduction relative to `regular`

## 3. Do retained branches improve over fixed / FLB on both datasets

Yes.

On full COCO-CHAIR, all three retained branches reduce `CHAIRs` and `CHAIRi` further than fixed / FLB-equivalent.

On AMBER full, all three retained branches improve at least slightly over fixed / FLB-equivalent:
- `dual`: same `Cover`, lower `CHAIR/Hal/Cog`
- Candidate A: same `Cover`, lower `CHAIR/Hal/Cog`
- `firstlogit_removal_top10`: lower `CHAIR/Hal/Cog`, but `Cover -0.1`

The AMBER gains are small, but they are consistent with the COCO trend.

## 4. Which branch is most metric-strong

`firstlogit_removal_top10`.

Evidence:
- best full COCO-CHAIR `CHAIRs/CHAIRi`
- best FLB-aligned COCO-500 `CHAIRs/CHAIRi`
- lowest AMBER `Hal/Cog`

It remains the strongest raw hallucination-reduction branch, but also the most aggressive.

## 5. Which branch is most quality-preserving

`dual_phrase_replace_v1`.

Evidence:
- it is already the quality-preserving retained branch in the COCO archive
- on AMBER full, it preserves `Cover` relative to fixed / FLB-equivalent
- it improves `Hal/Cog` without taking the extra `Cover` drop seen in raw removal

Candidate A is also conservative, but its role is safer source-aware removal rather than the main quality-preserving replacement-style branch.

## 6. Which branch is safest to present as default

If a paper-facing default branch must be described before final user selection, `dual_phrase_replace_v1` is the safest default to present.

Reason:
- it preserves the intended "quality-preserving" story
- it improves over fixed / FLB-equivalent on both COCO-CHAIR and AMBER
- it avoids presenting the most aggressive removal branch as the default user-facing method

Important caveat:
- no final branch selection has been finalized
- all three retained branches remain preserved

## 7. Does AMBER reduce the concern that the result is COCO-only

Yes, partially.

AMBER full generative evaluation strengthens the claim that the retained-branch pattern is not only a COCO-CHAIR artifact:
- the improved fixed / FLB-equivalent baseline transfers
- the retained branches still provide additional gains
- the same branch roles remain recognizable

So AMBER supports cross-dataset generality of the mention-level correction framework.

## 8. What caveats remain

- COCO-CHAIR and AMBER use different protocols, so raw CHAIR scales should not be directly compared
- AMBER full is smaller than COCO-CHAIR full and should remain follow-up evidence rather than the main result
- the retained-branch gains over fixed / FLB-equivalent are smaller on AMBER than the COCO gains
- `firstlogit_removal_top10` remains aggressive and should not be presented as the only story
- Candidate A remains a retained safer-removal branch, not a final replacement for the other retained branches
- `candidateA_dual_replace_then_remove` is still only an additional diagnostic, not a retained branch

## Bottom line

AMBER does not replace COCO-CHAIR as the main benchmark, but it materially reduces the concern that the retained-branch result is COCO-only. The most stable cross-dataset story is:

- fixed / FLB-equivalent is a robust improved baseline
- `firstlogit_removal_top10` is the metric-strong aggressive branch
- `dual_phrase_replace_v1` is the quality-preserving branch
- Candidate A is the safer source-aware removal branch
