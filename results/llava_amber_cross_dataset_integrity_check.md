# LLaVA AMBER Cross-Dataset Integrity Check

## Scope

This was a read-only integrity refresh for the verified LLaVA AMBER full generative results.

No model run was started.
No captions were regenerated.
No AMBER full evaluation was rerun.

## Checked output JSONs

Confirmed existing files:

- `outputs/amber/llava_regular_amber_full.json`
- `outputs/amber/llava_flb_equiv_fixed_amber_full.json`
- `outputs/amber/llava_dual_phrase_replace_v1_amber_full.json`
- `outputs/amber/llava_candidateA_firstlogit_only_guard_amber_full.json`
- `outputs/amber/llava_firstlogit_removal_top10_amber_full.json`

Result:

- all five output JSONs exist: `yes`
- sample count for all five outputs: `1004`

## Checked eval JSONs

Confirmed existing files:

- `results/llava_amber_full_eval_regular.json`
- `results/llava_amber_full_eval_fixed_flb.json`
- `results/llava_amber_full_eval_dual.json`
- `results/llava_amber_full_eval_candidateA.json`
- `results/llava_amber_full_eval_removal.json`

Result:

- all five eval JSONs exist: `yes`
- `subset_size = 1004` for all five eval files: `yes`
- `generation_success_count = 1004` for all five eval files: `yes`
- `evaluator_compatibility = yes` for all five eval files: `yes`
- `empty_count = 0` and `broken_count = 0` for all five eval files: `yes`
- `max_new_tokens = 128` in all five eval files: `yes`

## Metric match against verified AMBER full values

| Method | Verified CHAIR | Verified Cover | Verified Hal | Verified Cog | File Match |
|---|---:|---:|---:|---:|---|
| `regular` | 7.0 | 50.5 | 32.3 | 3.8 | yes |
| fixed / FLB-equivalent | 4.8 | 48.8 | 24.5 | 2.2 | yes |
| `dual_phrase_replace_v1` | 4.7 | 48.8 | 24.0 | 2.1 | yes |
| `removal_top10_firstlogit_only_guard` / Candidate A | 4.7 | 48.8 | 23.9 | 2.1 | yes |
| `firstlogit_removal_top10` diagnostic | 4.7 | 48.7 | 23.7 | 2.0 | yes |

## Additional read-only notes

- The eval JSONs also preserve the expected method metadata and runtime metadata.
- The edited methods remain caption-side post-processing variants rather than new generation runs.
- This integrity refresh resolves the earlier appendix caveat that AMBER full still needed a fresh SSH-based verification pass.

## Conclusion

- verified AMBER full files present: `yes`
- verified sample count consistent: `yes`
- verified metrics consistent with archived values: `yes`
- rerun needed: `no`
