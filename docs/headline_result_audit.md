# Headline Result Audit

Scope: this note audits only the committed public files in `README.md`, `docs/resume_bullets.md`, `docs/result_analysis.md`, `results/public/result_table.md`, and `results/public/*.csv`. No new experiments were run.

All metrics below are hallucination metrics where lower is better. The deltas are computed as `FLB - OCV on FLB`; positive values mean OCV on FLB is lower than FLB.

## Top 5 Candidate Headline Results

| Rank | Model | Benchmark | Metric | Regular | FLB | OCV on Regular | OCV on FLB | Absolute delta vs FLB | Relative reduction vs FLB | Lower is better? | Caveats | Resume-safe? |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| 1 | InstructBLIP-7B | COCO/CHAIR-500 | CHAIRs | 0.2620 | 0.2360 | 0.2620 | 0.1340 | 0.1020 | 43.2% | Yes | OCV on Regular selected zero surviving edits in this cell; the strong result is specifically OCV on FLB source. | Yes. Best single headline because it is large, clean, and already identified as the strongest supported setting. |
| 2 | LLaVA-1.5-7B | COCO/CHAIR-500 | CHAIRs | 0.1720 | 0.1560 | 0.1220 | 0.1100 | 0.0460 | 29.5% | Yes | Caption-side aggregate row only; no SOTA or official benchmark claim. | Yes. Strong alternative and useful because OCV improves both Regular and FLB. |
| 3 | LLaVA-1.5-7B | AMBER-1004 | AMBER Hal | 48.2 | 31.6 | 40.5 | 25.0 | 6.6 | 20.9% | Yes | AMBER Cover drops from 50.1 under FLB to 47.8 under OCV on FLB, so preservation trade-off must be mentioned if this is used. | Yes, but better as a supporting cross-benchmark result than the single headline. |
| 4 | InstructBLIP-7B | AMBER-1004 | AMBER Hal | 59.0 | 52.5 | 53.0 | 48.4 | 4.1 | 7.8% | Yes | AMBER Cover drops from 54.5 under FLB to 52.5 under OCV on FLB. Improvement is smaller than the COCO/CHAIR result. | Yes as supporting evidence, with Cover trade-off. |
| 5 | LLaVA-1.5-7B | OpenCHAIR | OpenCHAIR | 0.180299 | 0.162093 | 0.173015 | 0.158447 | 0.003646 | 2.2% | Yes | Gain over FLB is small; useful mainly to show open-vocabulary transfer. | Safe as supporting evidence, not strong enough as the main headline. |

## Best Single Chinese Resume Bullet

The following line is written with HTML numeric entities so the Markdown source stays ASCII-safe while GitHub renders it as Chinese:

> &#29420;&#31435;&#25506;&#32034; post-decoding / training-free &#30340; LVLM &#29289;&#20307;&#24187;&#35273;&#32531;&#35299;&#26041;&#27861;&#65292;&#22522;&#20110; COCO/CHAIR-500&#12289;AMBER-1004 &#19982; OpenCHAIR &#25972;&#29702;&#21487;&#22797;&#26680; aggregate results&#65307;&#22312;&#26368;&#24378;&#21487;&#20844;&#24320;&#25903;&#25745;&#35774;&#32622;&#20013;&#65292;&#23558; InstructBLIP-7B &#22312; COCO/CHAIR-500 &#19978;&#30340; CHAIRs &#20174; FLB &#30340; 0.2360 &#38477;&#33267; OCV-on-FLB &#30340; 0.1340&#65292;&#30456;&#23545;&#38477;&#20302; 43.2%&#65292;&#24182;&#35760;&#24405; preservation trade-off &#19982;&#36793;&#30028;&#26696;&#20363;&#12290;

## Short Email Sentence

The safest short sentence is:

> I cleaned the public repository around aggregate, reproducible results; the strongest supported headline is that OCV-on-FLB reduces InstructBLIP-7B COCO/CHAIR-500 CHAIRs from 0.2360 to 0.1340, a 43.2% relative reduction over FLB, without claiming SOTA or official benchmark status.

## Results Not Recommended As Headline Claims

| Result family | Why it should not be the headline |
| --- | --- |
| POPE rows in `external_baselines.csv` | POPE is a diagnostic yes/no VQA-side record in this public repo, not the main caption-side claim. |
| AGLA / VCD / MaskCD / DeCo rows | These are external baseline context rows with protocol or output-quality caveats, not official leaderboard comparisons. |
| DeCo smoke10 | Smoke-only status and explicitly not a carried score line. |
| DeCo CHAIR-500 full row | Completed, but the public caveat says the row is truncation-heavy with many max-token endings and dangling outputs. |
| InstructBLIP OpenCHAIR | The FLB source is regular-equivalent in this run, so OCV-on-FLB matching OCV-on-Regular should not be used as a strong FLB-comparison headline. |
| InternVL3.5 AMBER | Marked partial coverage; the OCV-on-FLB CHAIR value is worse than FLB even though Hal improves slightly. |
| Qwen2.5-VL AMBER | AMBER CHAIR worsens from 3.3 to 3.4 and Cover drops, despite a small Hal improvement. |
| Qwen2.5-VL COCO/OpenCHAIR | Useful boundary evidence, but lower baseline hallucination and large edit-volume caveats make it weaker for a resume headline. |
| OCV on Regular for InstructBLIP COCO/CHAIR-500 | It selected zero surviving edits and ties Regular, so the safe claim is specifically OCV on FLB source. |
| OpenCHAIR gains alone | The LLaVA OpenCHAIR row is clean but the gain over FLB is small; use it as transfer evidence, not the headline. |

## Audit Conclusion

The safest public-facing headline is **InstructBLIP-7B + COCO/CHAIR-500 + CHAIRs**, comparing FLB to OCV on FLB. It is the largest clean relative reduction in the main caption-side table and is already consistent with `README.md`, `docs/result_analysis.md`, and `results/public/result_table.md`.
