# FLB Reproduction Plan

> Status: planning only. No baseline repo has been cloned locally or remotely by this document.
> Priority: first baseline for the new project because the first-logit / early-anchor idea is directly aligned with the current research note.

## 1. Official paper and code

- paper: [First Logit Boosting: Visual Grounding Method to Mitigate Object Hallucination in Large Vision-Language Models](https://arxiv.org/abs/2604.00455)
- official code: [jiwooha20/FLB](https://github.com/jiwooha20/FLB)

Useful public code observations from the official repo:

- the repo is explicitly marked as the official implementation
- `experiments/` contains `llava/` and `lavis/`, which indicates released support around LLaVA-style and InstructBLIP-style backbones
- released benchmark scripts under `experiments/cd_scripts/` currently include:
  - `llava1.5_AMBER.bash`
  - `instructblip_AMBER.bash`
- the README still lists `How to start` and `CHAIR code` under `To be updated`

## 2. Paper default model / released code target

For the code that is already public, the most directly visible targets are:

- LLaVA-1.5
- InstructBLIP

For this project, LLaVA-1.5 is the preferred first target because:

- the remote machine already has a LLaVA-1.5 checkpoint path
- the current project is already centered around object hallucination and POPE
- this keeps the first reproduction as close as possible to existing resources

## 3. Does FLB officially support POPE / object hallucination?

Current answer:

- the paper topic is object hallucination mitigation
- the released public code is not yet a plug-and-play POPE reproduction package
- the visible public scripts are AMBER-centered
- there is no obvious public `POPE` script in the released repo at the moment

Practical implication:

- `official FLB on POPE` is not a one-command reproduction right now
- the first realistic reproduction path is to port the FLB first-logit logic onto an existing POPE evaluation entry

## 4. Extra data requirements

If reproducing the currently released public scripts as-is:

- AMBER data would be required

If reproducing the mechanism on our current first-stage benchmark:

- we can try to reuse existing remote POPE data
- we can reuse the existing remote LLaVA-1.5 checkpoint
- no new local data download is needed

## 5. Can we use the existing remote LLaVA-1.5 and POPE?

Yes, for a minimal project-aligned reproduction plan.

Important nuance:

- this would be a mechanism-aligned FLB reproduction on POPE
- it would not be identical to simply running an official public POPE script from the FLB repo, because that script does not appear to be publicly released yet

This is acceptable for the current phase because the research goal is not `paper leaderboard recreation at any cost`, but `verify the first-logit / early-anchor signal direction under our current benchmark setup`.

## 6. Expected remote working directory

Recommended remote work directory once GPU access is restored:

- `/root/autodl-tmp/code/training-free_hallucination/flb_repro`

Recommended materials to place there later:

- a remote-only clone of the official FLB repo, or
- a small remote-only adaptation sandbox that ports FLB logic into a POPE-compatible LLaVA-1.5 eval script

Do not create this directory locally and do not download models or datasets into the Git repo.

## 7. Minimal reproduction goal

The first minimal target should be:

1. verify where FLB injects or reuses first-logit information in the released LLaVA-1.5 path
2. reproduce that mechanism on a tiny remote-only POPE pilot using the existing LLaVA-1.5 checkpoint
3. compare:
   - base decoding
   - full VCD legacy baseline
   - a minimal first-logit / early-anchor variant aligned with FLB
4. store only lightweight summaries back in this repo

Recommended first pilot size after GPU access is available:

- 50 to 200 POPE examples on a single split, before any full evaluation

## 8. Likely pitfalls

- the public FLB code release is narrower than the paper headline suggests
- current public scripts are AMBER-oriented rather than POPE-oriented
- the first-logit idea may interact differently with binary yes/no POPE answers than with open-ended generation
- careless implementation can accidentally turn into another VCD variant instead of a clean first-logit baseline
- because POPE is yes/no, we need to distinguish:
  - first-logit support for the queried object
  - first answer-token support for `yes` / `no`
- the current AutoDL instance is in no-GPU mode, so no real reproduction should start on it

## 9. How to avoid downloading large files locally

- do not clone FLB locally
- do not download AMBER locally
- do not download model checkpoints locally
- do all baseline repo cloning and data/model access on the remote machine only
- use the existing remote LLaVA-1.5 checkpoint and POPE paths first
- keep this repository limited to markdown notes and lightweight summary files

## 10. How to record result summaries

Once actual runs begin, keep the local repo limited to lightweight artifacts such as:

- `project_context/baseline_notes/flb_<date>.md`
- `manifest.json`
- `summary.csv`
- short comparison notes that point to remote raw output paths

Do not copy back:

- raw `answers.jsonl`
- trace files
- large caches
- full baseline repo clones

## 11. Recommended next action after GPU access returns

The safest first execution order is:

1. inspect the official FLB LLaVA-1.5 script and its eval entry on the remote machine
2. map its first-logit logic into a POPE-compatible evaluation path
3. run a tiny smoke pilot on POPE
4. only then decide whether a broader FLB reproduction is worth deeper effort
