# Step0 Attention-Backed Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven-development (recommended) or executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the `v1.1-D` step0 attention-backed cheap proxy gate in `E:\VScode\VCD`, add offline screening for the new gate family, and carry the workflow through to the point where AutoDL can run the probe, smoke, and 200-sample validation.

**Architecture:** Keep the current entropy, step-aware, proxy-preview, and cascade-preview modes intact. Add a new `step0_attention_proxy` mode that combines `step0` entropy with the existing `attention_concentration` proxy from the base forward pass, while keeping the later-step `gateent03` entropy rule unchanged. Reuse the existing trace pipeline, but extend it so the new gate records its attention-specific metadata and can be screened offline against regular and always-on VCD traces.

**Tech Stack:** Python 3.9, PyTorch, Transformers generation hooks, `unittest`, JSONL trace analysis, AutoDL remote execution

---

## File Map

### Implementation repo

All code changes in this plan happen in `E:\VScode\VCD`.

- Modify: `E:\VScode\VCD\vcd_utils\path_risk_gate.py`
  Responsibility: add the `step0_attention_proxy` gate math, mode dispatch, and argument validation
- Modify: `E:\VScode\VCD\vcd_utils\path_risk_trace.py`
  Responsibility: persist attention-gate metadata and summarize attention-trigger rates
- Modify: `E:\VScode\VCD\vcd_utils\vcd_sample.py`
  Responsibility: compute `attention_concentration` before the gate decision and pass it into online gating
- Modify: `E:\VScode\VCD\experiments\eval\object_hallucination_vqa_llava.py`
  Responsibility: expose the new CLI flag and force attention outputs when the new gate mode is active
- Create: `E:\VScode\VCD\experiments\eval\analyze_attention_gate.py`
  Responsibility: screen `(entropy_threshold, attention_quantile)` pairs from probe traces
- Modify: `E:\VScode\VCD\tests\test_path_risk_gate.py`
  Responsibility: unit tests for the new gate mode and validation checks
- Modify: `E:\VScode\VCD\tests\test_path_risk_trace.py`
  Responsibility: unit tests for attention-gate trace fields and summary counters
- Create: `E:\VScode\VCD\tests\test_analyze_attention_gate.py`
  Responsibility: offline analysis tests for the new screening script

### Paper repo

- Existing spec: `E:\VScode\training-free_hallucination\docs\superpowers\specs\2026-04-18-step0-attention-backed-gate-design.md`
- Create: `E:\VScode\training-free_hallucination\docs\superpowers\plans\2026-04-18-step0-attention-backed-gate-implementation-plan.md`

## Task 1: Add Step0 Attention-Backed Gate Primitives

**Files:**
- Modify: `E:\VScode\VCD\tests\test_path_risk_gate.py`
- Modify: `E:\VScode\VCD\vcd_utils\path_risk_gate.py`

- [ ] **Step 1: Add failing unit tests for the new gate mode**

Append these tests to `E:\VScode\VCD\tests\test_path_risk_gate.py` and extend the import list with `build_step0_attention_proxy_gate_decision`:

```python
    def test_build_step0_attention_proxy_gate_decision_triggers_on_attention(self):
        decision = build_step0_attention_proxy_gate_decision(
            base_token_scores=[8.0, -8.0],
            attention_concentration=0.92,
            entropy_threshold=0.3,
            attention_threshold=0.9,
        )

        self.assertTrue(decision["gate_triggered"])
        self.assertEqual(decision["gate_step_group"], "step0")
        self.assertEqual(decision["gate_rule_name"], "step0_entropy_or_attention")
        self.assertEqual(decision["gate_trigger_sources"], ["attention_concentration"])
        self.assertAlmostEqual(decision["gate_attention_value"], 0.92, places=6)
        self.assertAlmostEqual(decision["gate_attention_threshold"], 0.9, places=6)

    def test_build_step0_attention_proxy_gate_decision_triggers_on_entropy(self):
        decision = build_step0_attention_proxy_gate_decision(
            base_token_scores=[0.0, 0.0],
            attention_concentration=0.2,
            entropy_threshold=0.3,
            attention_threshold=0.9,
        )

        self.assertTrue(decision["gate_triggered"])
        self.assertEqual(decision["gate_trigger_sources"], ["base_entropy"])
        self.assertGreaterEqual(decision["gate_signal_value"], 0.3)

    def test_build_step0_attention_proxy_gate_decision_accepts_when_both_signals_are_low(self):
        decision = build_step0_attention_proxy_gate_decision(
            base_token_scores=[8.0, -8.0],
            attention_concentration=0.2,
            entropy_threshold=0.3,
            attention_threshold=0.9,
        )

        self.assertFalse(decision["gate_triggered"])
        self.assertEqual(decision["gate_action"], "accept")
        self.assertEqual(decision["gate_trigger_sources"], [])

    def test_build_path_gate_decision_uses_attention_proxy_rule_on_step0(self):
        decision = build_path_gate_decision(
            base_token_scores=[8.0, -8.0],
            step_index=0,
            gate_config={
                "mode": "step0_attention_proxy",
                "step0_entropy_threshold": 0.3,
                "step0_attention_threshold": 0.9,
                "later_entropy_threshold": 0.3,
            },
            attention_concentration=0.95,
        )

        self.assertTrue(decision["gate_triggered"])
        self.assertEqual(decision["gate_rule_name"], "step0_entropy_or_attention")
        self.assertEqual(decision["gate_trigger_sources"], ["attention_concentration"])

    def test_build_path_gate_decision_uses_later_entropy_rule_after_step0_for_attention_mode(self):
        decision = build_path_gate_decision(
            base_token_scores=[0.0, 0.0],
            step_index=1,
            gate_config={
                "mode": "step0_attention_proxy",
                "step0_entropy_threshold": 0.3,
                "step0_attention_threshold": 0.9,
                "later_entropy_threshold": 0.2,
            },
        )

        self.assertTrue(decision["gate_triggered"])
        self.assertEqual(decision["gate_step_group"], "later")
        self.assertEqual(decision["gate_rule_name"], "later_entropy")

    def test_validate_path_risk_gate_args_requires_attention_threshold_when_attention_proxy_mode(self):
        with self.assertRaisesRegex(ValueError, "step0 attention threshold"):
            validate_path_risk_gate_args(
                use_cd=True,
                use_path_gate=True,
                gate_mode="step0_attention_proxy",
                step0_entropy_threshold=0.3,
                step0_attention_threshold=None,
                later_entropy_threshold=0.3,
            )
```

- [ ] **Step 2: Run the gate tests and confirm the new tests fail**

Run:

```powershell
Set-Location E:\VScode\VCD
python -m unittest tests.test_path_risk_gate -v
```

Expected:

- `ImportError` for `build_step0_attention_proxy_gate_decision`
- or `TypeError` because `build_path_gate_decision` / `validate_path_risk_gate_args` do not yet accept the new attention fields

- [ ] **Step 3: Implement the new gate helper and mode dispatch**

Update `E:\VScode\VCD\vcd_utils\path_risk_gate.py` with this function:

```python
def build_step0_attention_proxy_gate_decision(
    base_token_scores: Any,
    attention_concentration: float,
    entropy_threshold: float,
    attention_threshold: float,
) -> Dict[str, Any]:
    probabilities = _softmax(_to_score_list(base_token_scores))
    entropy_value = float(_entropy(probabilities))
    attention_value = float(attention_concentration)

    triggered_by_entropy = entropy_value >= float(entropy_threshold)
    triggered_by_attention = attention_value >= float(attention_threshold)
    trigger_sources = []
    if triggered_by_entropy:
        trigger_sources.append("base_entropy")
    if triggered_by_attention:
        trigger_sources.append("attention_concentration")

    gate_triggered = bool(trigger_sources)
    return {
        "gate_triggered": gate_triggered,
        "gate_signal_name": "step0_entropy_or_attention",
        "gate_signal_value": entropy_value,
        "gate_threshold": float(entropy_threshold),
        "gate_action": "rerank" if gate_triggered else "accept",
        "gate_step_group": "step0",
        "gate_rule_name": "step0_entropy_or_attention",
        "gate_trigger_sources": trigger_sources,
        "gate_margin_value": None,
        "gate_margin_threshold": None,
        "gate_entropy_threshold": float(entropy_threshold),
        "gate_attention_value": attention_value,
        "gate_attention_threshold": float(attention_threshold),
    }
```

Then extend `build_path_gate_decision(...)` to accept:

```python
    attention_concentration: Optional[float] = None,
```

and add this branch before the existing fallback:

```python
    if gate_mode == "step0_attention_proxy":
        if int(step_index) == 0:
            if attention_concentration is None:
                raise ValueError(
                    "Step0 attention-proxy gate requires attention concentration on step 0."
                )
            return build_step0_attention_proxy_gate_decision(
                base_token_scores=base_token_scores,
                attention_concentration=float(attention_concentration),
                entropy_threshold=float(gate_config.get("step0_entropy_threshold", 0.3)),
                attention_threshold=float(gate_config.get("step0_attention_threshold", 0.9)),
            )
        return _build_later_entropy_gate_decision(
            base_token_scores=base_token_scores,
            entropy_threshold=float(gate_config.get("later_entropy_threshold", 0.3)),
        )
```

Finally extend `validate_path_risk_gate_args(...)` with:

```python
    step0_attention_threshold: Optional[float] = None,
```

and add:

```python
    if use_path_gate and gate_mode == "step0_attention_proxy":
        if step0_entropy_threshold is None:
            raise ValueError("Step0 attention-proxy gate requires step0 entropy threshold.")
        if step0_attention_threshold is None:
            raise ValueError("Step0 attention-proxy gate requires step0 attention threshold.")
        if later_entropy_threshold is None:
            raise ValueError("Step0 attention-proxy gate requires later-step entropy threshold.")
```

- [ ] **Step 4: Re-run the gate tests and confirm they pass**

Run:

```powershell
Set-Location E:\VScode\VCD
python -m unittest tests.test_path_risk_gate -v
```

Expected:

- all tests in `tests.test_path_risk_gate` pass

- [ ] **Step 5: Commit the gate primitive changes**

Run:

```powershell
Set-Location E:\VScode\VCD
git add tests/test_path_risk_gate.py vcd_utils/path_risk_gate.py
git commit -m "Add step0 attention proxy gate mode"
```

## Task 2: Persist Attention-Gate Metadata In Traces

**Files:**
- Modify: `E:\VScode\VCD\tests\test_path_risk_trace.py`
- Modify: `E:\VScode\VCD\vcd_utils\path_risk_trace.py`

- [ ] **Step 1: Add failing trace tests for attention-gate metadata**

Append these tests to `E:\VScode\VCD\tests\test_path_risk_trace.py`:

```python
    def test_build_step_trace_records_attention_gate_metadata(self):
        trace = build_step_trace(
            step_index=0,
            base_token_scores=[0.0, 0.0],
            decision_token_scores=[0.0, 0.0],
            selected_token_id=0,
            generated_history=[],
            gate_decision={
                "gate_triggered": True,
                "gate_signal_name": "step0_entropy_or_attention",
                "gate_signal_value": 0.69,
                "gate_threshold": 0.3,
                "gate_action": "rerank",
                "gate_step_group": "step0",
                "gate_rule_name": "step0_entropy_or_attention",
                "gate_trigger_sources": ["attention_concentration"],
                "gate_attention_value": 0.91,
                "gate_attention_threshold": 0.9,
            },
        )

        self.assertEqual(trace["gate_rule_name"], "step0_entropy_or_attention")
        self.assertEqual(trace["gate_trigger_sources"], ["attention_concentration"])
        self.assertAlmostEqual(trace["gate_attention_value"], 0.91, places=6)
        self.assertAlmostEqual(trace["gate_attention_threshold"], 0.9, places=6)

    def test_summarize_trace_reports_attention_gate_rate(self):
        summary = summarize_trace(
            [
                {"gate_trigger_sources": ["attention_concentration"]},
                {"gate_trigger_sources": []},
                {"gate_trigger_sources": ["base_entropy", "attention_concentration"]},
            ]
        )

        self.assertEqual(summary["attention_gate_trigger_count"], 2)
        self.assertAlmostEqual(summary["attention_gate_trigger_rate"], 2 / 3, places=6)
```

- [ ] **Step 2: Run the trace tests and confirm the new assertions fail**

Run:

```powershell
Set-Location E:\VScode\VCD
python -m unittest tests.test_path_risk_trace -v
```

Expected:

- `KeyError` for `gate_attention_value`
- missing summary keys for `attention_gate_trigger_count`

- [ ] **Step 3: Implement the new trace fields and summary counters**

Update `E:\VScode\VCD\vcd_utils\path_risk_trace.py` so `build_step_trace(...)` also returns:

```python
        "gate_attention_value": gate_decision.get("gate_attention_value"),
        "gate_attention_threshold": gate_decision.get("gate_attention_threshold"),
```

Extend the empty-summary branch with:

```python
            "attention_gate_trigger_count": 0,
            "attention_gate_trigger_rate": None,
```

Then add:

```python
    attention_gate_flags = [
        1.0 if "attention_concentration" in trace.get("gate_trigger_sources", []) else 0.0
        for trace in step_traces
        if trace.get("gate_trigger_sources") is not None
    ]
```

and return:

```python
        "attention_gate_trigger_count": (
            int(sum(attention_gate_flags)) if attention_gate_flags else 0
        ),
        "attention_gate_trigger_rate": (
            sum(attention_gate_flags) / len(attention_gate_flags)
            if attention_gate_flags
            else None
        ),
```

- [ ] **Step 4: Re-run the trace tests and confirm they pass**

Run:

```powershell
Set-Location E:\VScode\VCD
python -m unittest tests.test_path_risk_trace -v
```

Expected:

- all tests in `tests.test_path_risk_trace` pass

- [ ] **Step 5: Commit the trace updates**

Run:

```powershell
Set-Location E:\VScode\VCD
git add tests/test_path_risk_trace.py vcd_utils/path_risk_trace.py
git commit -m "Record attention gate trace metadata"
```

## Task 3: Add Offline Attention-Gate Screening

**Files:**
- Create: `E:\VScode\VCD\tests\test_analyze_attention_gate.py`
- Create: `E:\VScode\VCD\experiments\eval\analyze_attention_gate.py`

- [ ] **Step 1: Write failing analysis tests**

Create `E:\VScode\VCD\tests\test_analyze_attention_gate.py` with:

```python
import json
import unittest
from pathlib import Path
from uuid import uuid4

from experiments.eval.analyze_attention_gate import (
    analyze_attention_gate_candidates,
    build_arg_parser,
)


_TEMP_ROOT = Path(__file__).resolve().parent / ".tmp"


def _write_jsonl(path: Path, records):
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record) + "\n")


def _temp_file_path(prefix: str, suffix: str) -> Path:
    _TEMP_ROOT.mkdir(parents=True, exist_ok=True)
    return _TEMP_ROOT / f"{prefix}_{uuid4().hex}{suffix}"


class AnalyzeAttentionGateTests(unittest.TestCase):
    def test_analyze_attention_gate_candidates_reports_quantile_rows(self):
        probe_path = _temp_file_path("probe", ".jsonl")
        regular_path = _temp_file_path("regular", ".jsonl")
        vcd_path = _temp_file_path("vcd", ".jsonl")

        _write_jsonl(
            probe_path,
            [
                {
                    "question_id": 1,
                    "per_step": [{"step": 0, "base_entropy": 0.2, "attention_concentration": 0.95}],
                    "summary": {},
                },
                {
                    "question_id": 2,
                    "per_step": [{"step": 0, "base_entropy": 0.4, "attention_concentration": 0.40}],
                    "summary": {},
                },
                {
                    "question_id": 3,
                    "per_step": [{"step": 0, "base_entropy": 0.1, "attention_concentration": 0.20}],
                    "summary": {},
                },
            ],
        )
        _write_jsonl(
            regular_path,
            [
                {"question_id": 1, "per_step": [{"step": 0, "selected_token_id": 1}], "summary": {}},
                {"question_id": 2, "per_step": [{"step": 0, "selected_token_id": 1}], "summary": {}},
                {"question_id": 3, "per_step": [{"step": 0, "selected_token_id": 0}], "summary": {}},
            ],
        )
        _write_jsonl(
            vcd_path,
            [
                {"question_id": 1, "per_step": [{"step": 0, "selected_token_id": 0}], "summary": {}},
                {"question_id": 2, "per_step": [{"step": 0, "selected_token_id": 0}], "summary": {}},
                {"question_id": 3, "per_step": [{"step": 0, "selected_token_id": 0}], "summary": {}},
            ],
        )

        rows = analyze_attention_gate_candidates(
            probe_trace_path=probe_path,
            regular_trace_path=regular_path,
            vcd_trace_path=vcd_path,
            entropy_thresholds=[0.3],
            attention_quantiles=[0.5],
        )

        self.assertEqual(len(rows), 1)
        self.assertAlmostEqual(rows[0]["step0_attention_threshold"], 0.4, places=6)
        self.assertEqual(rows[0]["triggered_samples"], 2)
        self.assertEqual(rows[0]["trigger_hit_count"], 2)
        self.assertAlmostEqual(rows[0]["trigger_precision"], 1.0, places=6)

    def test_build_arg_parser_lists_attention_screen_flags(self):
        help_text = build_arg_parser().format_help()
        self.assertIn("--probe-trace", help_text)
        self.assertIn("--regular-trace", help_text)
        self.assertIn("--vcd-trace", help_text)
        self.assertIn("--attention-quantiles", help_text)
        self.assertIn("--output-json", help_text)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the new tests and confirm they fail**

Run:

```powershell
Set-Location E:\VScode\VCD
python -m unittest tests.test_analyze_attention_gate -v
```

Expected:

- `ModuleNotFoundError` for `experiments.eval.analyze_attention_gate`

- [ ] **Step 3: Implement the screening script**

Create `E:\VScode\VCD\experiments\eval\analyze_attention_gate.py` with the same JSONL style as the other analysis scripts:

```python
import argparse
import json
from pathlib import Path


def _load_trace_records(trace_path):
    records = []
    with Path(trace_path).open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                records.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL in {trace_path} at line {line_number}") from exc
    return records


def _records_by_question_id(records, trace_name):
    indexed = {}
    for record in records:
        question_id = record["question_id"]
        if question_id in indexed:
            raise ValueError(f"Duplicate question_id {question_id} in {trace_name}")
        indexed[question_id] = record
    return indexed


def _step0_record(record):
    steps = {step["step"]: step for step in record["per_step"]}
    if 0 not in steps:
        raise ValueError(f"Missing step 0 for question_id {record['question_id']}")
    return steps[0]


def _percentile(values, fraction):
    ordered = sorted(float(value) for value in values)
    if not ordered:
        return None
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * float(fraction)
    lower_index = int(position)
    upper_index = min(lower_index + 1, len(ordered) - 1)
    weight = position - lower_index
    return ordered[lower_index] + (ordered[upper_index] - ordered[lower_index]) * weight


def analyze_attention_gate_candidates(
    probe_trace_path,
    regular_trace_path,
    vcd_trace_path,
    entropy_thresholds,
    attention_quantiles,
):
    probe_records = _records_by_question_id(_load_trace_records(probe_trace_path), "probe trace")
    regular_records = _records_by_question_id(_load_trace_records(regular_trace_path), "regular trace")
    vcd_records = _records_by_question_id(_load_trace_records(vcd_trace_path), "vcd trace")

    if set(probe_records) != set(regular_records) or set(probe_records) != set(vcd_records):
        raise ValueError("Mismatched question_id sets between probe, regular, and vcd traces")

    aligned = []
    for question_id in sorted(probe_records):
        probe_step0 = _step0_record(probe_records[question_id])
        regular_step0 = _step0_record(regular_records[question_id])
        vcd_step0 = _step0_record(vcd_records[question_id])
        aligned.append(
            {
                "question_id": question_id,
                "base_entropy": float(probe_step0["base_entropy"]),
                "attention_concentration": float(probe_step0["attention_concentration"]),
                "vcd_changed": int(
                    regular_step0["selected_token_id"] != vcd_step0["selected_token_id"]
                ),
            }
        )

    changed_total = sum(row["vcd_changed"] for row in aligned)
    attention_values = [row["attention_concentration"] for row in aligned]
    results = []
    for entropy_threshold in entropy_thresholds:
        for attention_quantile in attention_quantiles:
            attention_threshold = _percentile(attention_values, attention_quantile)
            triggered_rows = [
                row
                for row in aligned
                if row["base_entropy"] >= float(entropy_threshold)
                or row["attention_concentration"] >= float(attention_threshold)
            ]
            hit_count = sum(row["vcd_changed"] for row in triggered_rows)
            results.append(
                {
                    "step0_entropy_threshold": float(entropy_threshold),
                    "step0_attention_quantile": float(attention_quantile),
                    "step0_attention_threshold": float(attention_threshold),
                    "total_samples": len(aligned),
                    "triggered_samples": len(triggered_rows),
                    "trigger_rate": len(triggered_rows) / len(aligned) if aligned else None,
                    "step0_vcd_changed_samples": changed_total,
                    "trigger_hit_count": hit_count,
                    "trigger_hit_rate": hit_count / changed_total if changed_total else None,
                    "trigger_precision": hit_count / len(triggered_rows) if triggered_rows else None,
                }
            )
    return results


def build_arg_parser():
    parser = argparse.ArgumentParser(
        description="Screen step-0 entropy-or-attention gate candidates from attention probe traces."
    )
    parser.add_argument("--probe-trace", required=True)
    parser.add_argument("--regular-trace", required=True)
    parser.add_argument("--vcd-trace", required=True)
    parser.add_argument("--entropy-thresholds", nargs="+", type=float, required=True)
    parser.add_argument("--attention-quantiles", nargs="+", type=float, required=True)
    parser.add_argument("--output-json", default=None)
    return parser


def main():
    parser = build_arg_parser()
    args = parser.parse_args()
    rows = analyze_attention_gate_candidates(
        probe_trace_path=args.probe_trace,
        regular_trace_path=args.regular_trace,
        vcd_trace_path=args.vcd_trace,
        entropy_thresholds=args.entropy_thresholds,
        attention_quantiles=args.attention_quantiles,
    )
    for row in rows:
        print(json.dumps(row, ensure_ascii=False))
    if args.output_json:
        Path(args.output_json).write_text(json.dumps(rows, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the new tests and the local analysis bundle**

Run:

```powershell
Set-Location E:\VScode\VCD
python -m unittest tests.test_analyze_attention_gate -v
python -m unittest tests.test_path_risk_gate tests.test_path_risk_trace tests.test_analyze_gate_signals tests.test_analyze_step0_gate tests.test_analyze_preview_gate tests.test_analyze_cascade_gate tests.test_analyze_attention_gate -v
```

Expected:

- the new analysis tests pass
- the full listed bundle passes

- [ ] **Step 5: Commit the analysis script**

Run:

```powershell
Set-Location E:\VScode\VCD
git add tests/test_analyze_attention_gate.py experiments/eval/analyze_attention_gate.py
git commit -m "Add attention gate screening analysis"
```

## Task 4: Wire Attention Gating Into Sampling And CLI

**Files:**
- Modify: `E:\VScode\VCD\vcd_utils\vcd_sample.py`
- Modify: `E:\VScode\VCD\experiments\eval\object_hallucination_vqa_llava.py`

- [ ] **Step 1: Update the sampler so attention is computed before the gate decision**

In `E:\VScode\VCD\vcd_utils\vcd_sample.py`, move `step_index = len(generated_history)` so it is defined before the gate block and add:

```python
        base_attention_concentration = None
        if (
            use_cd
            and use_path_gate
            and path_risk_gate.get("mode", "entropy") == "step0_attention_proxy"
            and step_index == 0
        ):
            base_attention_concentration = _compute_attention_concentration(
                getattr(outputs, "attentions", None)
            )
```

Then extend the existing gate call to:

```python
            gate_decision = build_path_gate_decision(
                base_token_scores=next_token_logits[0],
                step_index=step_index,
                gate_config=path_risk_gate,
                preview_token_scores=(
                    preview_token_logits[0] if preview_token_logits is not None else None
                ),
                prefilter_decision=prefilter_decision,
                attention_concentration=base_attention_concentration,
            )
```

Finally, reuse the same value for tracing:

```python
            attention_concentration = base_attention_concentration
            if attention_concentration is None and trace_config.get("trace_attention"):
                attention_concentration = _compute_attention_concentration(
                    getattr(outputs, "attentions", None)
                )
```

- [ ] **Step 2: Extend the eval CLI**

In `E:\VScode\VCD\experiments\eval\object_hallucination_vqa_llava.py`, add:

```python
    parser.add_argument("--gate-step0-attention-threshold", type=float, default=0.9)
```

Pass it into validation:

```python
        step0_attention_threshold=args.gate_step0_attention_threshold,
```

and add it to the generation config:

```python
                    "step0_attention_threshold": args.gate_step0_attention_threshold,
```

Also force attention outputs when this gate mode is active:

```python
    requires_attention_proxy = bool(args.use_path_gate) and args.path_gate_mode == "step0_attention_proxy"
```

and change the generation call to:

```python
                output_attentions=bool(args.trace_attention or requires_attention_proxy),
```

- [ ] **Step 3: Run the local verification bundle**

Run:

```powershell
Set-Location E:\VScode\VCD
python -m unittest tests.test_path_risk_gate tests.test_path_risk_trace tests.test_analyze_gate_signals tests.test_analyze_step0_gate tests.test_analyze_preview_gate tests.test_analyze_cascade_gate tests.test_analyze_attention_gate -v
python -m py_compile vcd_utils\path_risk_gate.py vcd_utils\path_risk_trace.py vcd_utils\vcd_sample.py experiments\eval\object_hallucination_vqa_llava.py experiments\eval\analyze_attention_gate.py
```

Expected:

- all listed tests pass
- `py_compile` exits cleanly with no output

Note:

- skip local `object_hallucination_vqa_llava.py --help` if the Windows environment does not have the full Torch stack; that runtime validation is covered on AutoDL in Task 5

- [ ] **Step 4: Commit the sampler and CLI wiring**

Run:

```powershell
Set-Location E:\VScode\VCD
git add vcd_utils/vcd_sample.py experiments/eval/object_hallucination_vqa_llava.py
git commit -m "Wire step0 attention proxy gate into sampling"
```

## Task 5: Sync To AutoDL And Verify The New Mode

**Files:**
- Sync: `E:\VScode\VCD\vcd_utils\path_risk_gate.py`
- Sync: `E:\VScode\VCD\vcd_utils\path_risk_trace.py`
- Sync: `E:\VScode\VCD\vcd_utils\vcd_sample.py`
- Sync: `E:\VScode\VCD\experiments\eval\object_hallucination_vqa_llava.py`
- Sync: `E:\VScode\VCD\experiments\eval\analyze_attention_gate.py`
- Sync: `E:\VScode\VCD\tests\test_path_risk_gate.py`
- Sync: `E:\VScode\VCD\tests\test_path_risk_trace.py`
- Sync: `E:\VScode\VCD\tests\test_analyze_attention_gate.py`

- [ ] **Step 1: Copy the changed files to AutoDL**

Run from Windows PowerShell:

```powershell
scp -P 21607 E:\VScode\VCD\vcd_utils\path_risk_gate.py E:\VScode\VCD\vcd_utils\path_risk_trace.py E:\VScode\VCD\vcd_utils\vcd_sample.py root@connect.westc.seetacloud.com:/root/autodl-tmp/code/VCD/vcd_utils/
scp -P 21607 E:\VScode\VCD\experiments\eval\object_hallucination_vqa_llava.py E:\VScode\VCD\experiments\eval\analyze_attention_gate.py root@connect.westc.seetacloud.com:/root/autodl-tmp/code/VCD/experiments/eval/
scp -P 21607 E:\VScode\VCD\tests\test_path_risk_gate.py E:\VScode\VCD\tests\test_path_risk_trace.py E:\VScode\VCD\tests\test_analyze_attention_gate.py root@connect.westc.seetacloud.com:/root/autodl-tmp/code/VCD/tests/
```

- [ ] **Step 2: Verify the remote test bundle and CLI help**

Run on AutoDL:

```bash
cd /root/autodl-tmp/code/VCD
source /root/miniconda3/etc/profile.d/conda.sh
conda activate /root/autodl-tmp/envs/vcd
export OMP_NUM_THREADS=8
python -m unittest tests.test_path_risk_gate tests.test_path_risk_trace tests.test_analyze_gate_signals tests.test_analyze_step0_gate tests.test_analyze_preview_gate tests.test_analyze_cascade_gate tests.test_analyze_attention_gate -v
python experiments/eval/object_hallucination_vqa_llava.py --help
```

Expected:

- all listed tests pass
- help text includes `--gate-step0-attention-threshold`

- [ ] **Step 3: Create reproducible 20-sample and 200-sample subset files**

Run on AutoDL:

```bash
cd /root/autodl-tmp/code/VCD/experiments
python - <<'PY'
from pathlib import Path

src = Path("./data/POPE/coco/coco_pope_random.json")
rows = src.read_text(encoding="utf-8").splitlines()

Path("/tmp/coco_pope_random_20.json").write_text(
    "\n".join(rows[:20]) + "\n",
    encoding="utf-8",
)
Path("/tmp/coco_pope_random_200.json").write_text(
    "\n".join(rows[:200]) + "\n",
    encoding="utf-8",
)
print("wrote", "/tmp/coco_pope_random_20.json", "and", "/tmp/coco_pope_random_200.json")
PY
```

Expected:

- two subset files are written under `/tmp`

## Task 6: Run The Attention Probe, Screening, Smoke, And 200-Sample Validation

**Files:**
- Remote artifact: `/root/autodl-tmp/code/VCD/experiments/output/pope/answers/llava15_attnprobe_coco_random_200_seed55.jsonl`
- Remote artifact: `/root/autodl-tmp/code/VCD/experiments/output/pope/traces/llava15_attnprobe_coco_random_200_seed55.jsonl`
- Remote artifact: `/root/autodl-tmp/code/VCD/experiments/output/pope/traces/attention_gate_screen_coco_random_200_seed55.json`
- Remote artifact: `/root/autodl-tmp/code/VCD/experiments/output/pope/answers/llava15_dlite_coco_random_smoke20_seed55.jsonl`
- Remote artifact: `/root/autodl-tmp/code/VCD/experiments/output/pope/traces/llava15_dlite_coco_random_smoke20_seed55.jsonl`
- Remote artifact: `/root/autodl-tmp/code/VCD/experiments/output/pope/answers/llava15_dmain_coco_random_smoke20_seed55.jsonl`
- Remote artifact: `/root/autodl-tmp/code/VCD/experiments/output/pope/traces/llava15_dmain_coco_random_smoke20_seed55.jsonl`
- Remote artifact: `/root/autodl-tmp/code/VCD/experiments/output/pope/answers/llava15_dlite_coco_random_200_seed55.jsonl`
- Remote artifact: `/root/autodl-tmp/code/VCD/experiments/output/pope/traces/llava15_dlite_coco_random_200_seed55.jsonl`
- Remote artifact: `/root/autodl-tmp/code/VCD/experiments/output/pope/answers/llava15_dmain_coco_random_200_seed55.jsonl`
- Remote artifact: `/root/autodl-tmp/code/VCD/experiments/output/pope/traces/llava15_dmain_coco_random_200_seed55.jsonl`

- [ ] **Step 1: Run the attention probe on the 200-sample subset**

Run on AutoDL:

```bash
cd /root/autodl-tmp/code/VCD/experiments

unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY
export HF_HOME=/root/autodl-tmp/hf-home
export TRANSFORMERS_OFFLINE=1
export HF_HUB_OFFLINE=1
export HF_DATASETS_OFFLINE=1
export OMP_NUM_THREADS=8

python ./eval/object_hallucination_vqa_llava.py \
  --model-path ./checkpoints/llava-v1.5-7b \
  --question-file /tmp/coco_pope_random_200.json \
  --image-folder ./data/coco/val2014 \
  --answers-file ./output/pope/answers/llava15_attnprobe_coco_random_200_seed55.jsonl \
  --trace-file ./output/pope/traces/llava15_attnprobe_coco_random_200_seed55.jsonl \
  --trace-attention \
  --seed 55
```

Expected:

- `200/200` completes successfully
- the trace file contains `attention_concentration` on `step 0`

- [ ] **Step 2: Screen entropy-or-attention candidates offline**

Run on AutoDL:

```bash
cd /root/autodl-tmp/code/VCD/experiments
python ./eval/analyze_attention_gate.py \
  --probe-trace ./output/pope/traces/llava15_attnprobe_coco_random_200_seed55.jsonl \
  --regular-trace ./output/pope/traces/llava15_regular_coco_random_dualtrace_200_seed55.jsonl \
  --vcd-trace ./output/pope/traces/llava15_vcd_coco_random_dualtrace_200_seed55_a1_b02_ns500.jsonl \
  --entropy-thresholds 0.25 0.30 0.35 \
  --attention-quantiles 0.60 0.70 0.80 0.90 \
  --output-json ./output/pope/traces/attention_gate_screen_coco_random_200_seed55.json
```

Expected:

- one JSON row per `(entropy_threshold, attention_quantile)` pair
- every row includes `step0_attention_threshold`

- [ ] **Step 3: Select D-main and D-lite deterministically from the screening output**

Run on AutoDL:

```bash
cd /root/autodl-tmp/code/VCD/experiments
python - <<'PY'
import json
from pathlib import Path

rows = json.loads(
    Path("./output/pope/traces/attention_gate_screen_coco_random_200_seed55.json").read_text(
        encoding="utf-8"
    )
)
rows = [row for row in rows if row["trigger_precision"] is not None]

d_main = max(
    rows,
    key=lambda row: (
        row["trigger_hit_rate"],
        row["trigger_precision"],
        -row["trigger_rate"],
        -row["step0_attention_quantile"],
    ),
)
eligible_for_lite = [
    row
    for row in rows
    if row["trigger_hit_rate"] is not None
    and row["trigger_hit_rate"] >= d_main["trigger_hit_rate"] - 0.05
]
d_lite = max(
    eligible_for_lite,
    key=lambda row: (
        row["trigger_precision"],
        -row["trigger_rate"],
        row["step0_attention_quantile"],
        row["step0_entropy_threshold"],
    ),
)

payload = {
    "d_main": d_main,
    "d_lite": d_lite,
}
Path("/tmp/attention_gate_selected_rows.json").write_text(
    json.dumps(payload, indent=2),
    encoding="utf-8",
)
print(json.dumps(payload, indent=2))
PY
```

Expected:

- `/tmp/attention_gate_selected_rows.json` is written
- the output prints one `d_main` row and one `d_lite` row

- [ ] **Step 4: Export the selected thresholds into shell variables**

Run on AutoDL:

```bash
eval "$(
python - <<'PY'
import json
from pathlib import Path

payload = json.loads(Path("/tmp/attention_gate_selected_rows.json").read_text(encoding="utf-8"))
d_main = payload["d_main"]
d_lite = payload["d_lite"]

print(f"export D_MAIN_E={d_main['step0_entropy_threshold']}")
print(f"export D_MAIN_C={d_main['step0_attention_threshold']}")
print(f"export D_LITE_E={d_lite['step0_entropy_threshold']}")
print(f"export D_LITE_C={d_lite['step0_attention_threshold']}")
PY
)"

printf 'D-main: entropy=%s attention=%s\n' "$D_MAIN_E" "$D_MAIN_C"
printf 'D-lite: entropy=%s attention=%s\n' "$D_LITE_E" "$D_LITE_C"
```

Expected:

- all four shell variables are exported

- [ ] **Step 5: Run the 20-sample smoke check**

Run on AutoDL:

```bash
cd /root/autodl-tmp/code/VCD/experiments

python ./eval/object_hallucination_vqa_llava.py \
  --model-path ./checkpoints/llava-v1.5-7b \
  --question-file /tmp/coco_pope_random_20.json \
  --image-folder ./data/coco/val2014 \
  --answers-file ./output/pope/answers/llava15_dlite_coco_random_smoke20_seed55.jsonl \
  --trace-file ./output/pope/traces/llava15_dlite_coco_random_smoke20_seed55.jsonl \
  --use_cd \
  --cd_alpha 1 \
  --cd_beta 0.2 \
  --noise_step 500 \
  --use-path-gate \
  --path-gate-mode step0_attention_proxy \
  --gate-step0-entropy-threshold "$D_LITE_E" \
  --gate-step0-attention-threshold "$D_LITE_C" \
  --gate-later-entropy-threshold 0.3 \
  --trace-attention \
  --seed 55

python ./eval/object_hallucination_vqa_llava.py \
  --model-path ./checkpoints/llava-v1.5-7b \
  --question-file /tmp/coco_pope_random_20.json \
  --image-folder ./data/coco/val2014 \
  --answers-file ./output/pope/answers/llava15_dmain_coco_random_smoke20_seed55.jsonl \
  --trace-file ./output/pope/traces/llava15_dmain_coco_random_smoke20_seed55.jsonl \
  --use_cd \
  --cd_alpha 1 \
  --cd_beta 0.2 \
  --noise_step 500 \
  --use-path-gate \
  --path-gate-mode step0_attention_proxy \
  --gate-step0-entropy-threshold "$D_MAIN_E" \
  --gate-step0-attention-threshold "$D_MAIN_C" \
  --gate-later-entropy-threshold 0.3 \
  --trace-attention \
  --seed 55
```

- [ ] **Step 6: Summarize the smoke traces and decide whether to stop early**

Run on AutoDL:

```bash
cd /root/autodl-tmp/code/VCD/experiments
python - <<'PY'
import json
from pathlib import Path

files = {
    "gateent03": Path("./output/pope/traces/llava15_gateent03_coco_random_200_seed55.jsonl"),
    "vcd": Path("./output/pope/traces/llava15_vcd_coco_random_dualtrace_200_seed55_a1_b02_ns500.jsonl"),
    "D_lite_smoke": Path("./output/pope/traces/llava15_dlite_coco_random_smoke20_seed55.jsonl"),
    "D_main_smoke": Path("./output/pope/traces/llava15_dmain_coco_random_smoke20_seed55.jsonl"),
}

def mean(values):
    values = [value for value in values if value is not None]
    return sum(values) / len(values) if values else None

def fmt(value):
    return "NA" if value is None else f"{value:.6f}"

print("name\\tsamples\\tmean_latency\\tmean_tps\\tmean_gate_rate\\tmean_step0_gate_rate\\tmean_attention")
for name, path in files.items():
    rows = [json.loads(line) for line in path.open("r", encoding="utf-8") if line.strip()]
    summaries = [row["summary"] for row in rows]
    print(
        f"{name}\\t{len(rows)}\\t"
        f"{fmt(mean([s.get('latency_sec') for s in summaries]))}\\t"
        f"{fmt(mean([s.get('tokens_per_second') for s in summaries]))}\\t"
        f"{fmt(mean([s.get('gate_trigger_rate') for s in summaries]))}\\t"
        f"{fmt(mean([s.get('step0_gate_trigger_rate') for s in summaries]))}\\t"
        f"{fmt(mean([s.get('mean_attention_concentration') for s in summaries]))}"
    )
PY
```

Early-stop rule:

- stop the line if both smoke candidates are already too close to `always-on vcd` speed
- or both are clearly slower than `gateent03` without any sign of better selectivity

- [ ] **Step 7: If smoke passes, run the 200-sample online validation**

Run on AutoDL:

```bash
cd /root/autodl-tmp/code/VCD/experiments

python ./eval/object_hallucination_vqa_llava.py \
  --model-path ./checkpoints/llava-v1.5-7b \
  --question-file /tmp/coco_pope_random_200.json \
  --image-folder ./data/coco/val2014 \
  --answers-file ./output/pope/answers/llava15_dlite_coco_random_200_seed55.jsonl \
  --trace-file ./output/pope/traces/llava15_dlite_coco_random_200_seed55.jsonl \
  --use_cd \
  --cd_alpha 1 \
  --cd_beta 0.2 \
  --noise_step 500 \
  --use-path-gate \
  --path-gate-mode step0_attention_proxy \
  --gate-step0-entropy-threshold "$D_LITE_E" \
  --gate-step0-attention-threshold "$D_LITE_C" \
  --gate-later-entropy-threshold 0.3 \
  --trace-attention \
  --seed 55

python ./eval/object_hallucination_vqa_llava.py \
  --model-path ./checkpoints/llava-v1.5-7b \
  --question-file /tmp/coco_pope_random_200.json \
  --image-folder ./data/coco/val2014 \
  --answers-file ./output/pope/answers/llava15_dmain_coco_random_200_seed55.jsonl \
  --trace-file ./output/pope/traces/llava15_dmain_coco_random_200_seed55.jsonl \
  --use_cd \
  --cd_alpha 1 \
  --cd_beta 0.2 \
  --noise_step 500 \
  --use-path-gate \
  --path-gate-mode step0_attention_proxy \
  --gate-step0-entropy-threshold "$D_MAIN_E" \
  --gate-step0-attention-threshold "$D_MAIN_C" \
  --gate-later-entropy-threshold 0.3 \
  --trace-attention \
  --seed 55
```

- [ ] **Step 8: Evaluate the 200-sample outputs**

Run on AutoDL:

```bash
cd /root/autodl-tmp/code/VCD/experiments

python ./eval/eval_pope.py \
  --gt_files /tmp/coco_pope_random_200.json \
  --gen_files ./output/pope/answers/llava15_dlite_coco_random_200_seed55.jsonl

python ./eval/eval_pope.py \
  --gt_files /tmp/coco_pope_random_200.json \
  --gen_files ./output/pope/answers/llava15_dmain_coco_random_200_seed55.jsonl
```

- [ ] **Step 9: Summarize the final traces against the existing baselines**

Run on AutoDL:

```bash
cd /root/autodl-tmp/code/VCD/experiments
python - <<'PY'
import json
from pathlib import Path

files = {
    "gateent03": Path("./output/pope/traces/llava15_gateent03_coco_random_200_seed55.jsonl"),
    "vcd": Path("./output/pope/traces/llava15_vcd_coco_random_dualtrace_200_seed55_a1_b02_ns500.jsonl"),
    "D_lite": Path("./output/pope/traces/llava15_dlite_coco_random_200_seed55.jsonl"),
    "D_main": Path("./output/pope/traces/llava15_dmain_coco_random_200_seed55.jsonl"),
}

def mean(values):
    values = [value for value in values if value is not None]
    return sum(values) / len(values) if values else None

def fmt(value):
    return "NA" if value is None else f"{value:.6f}"

print("name\\tsamples\\tmean_latency\\tmean_tps\\tmean_gate_rate\\tmean_step0_gate_rate\\tmean_attention\\tmean_attention_gate_rate")
for name, path in files.items():
    rows = [json.loads(line) for line in path.open("r", encoding="utf-8") if line.strip()]
    summaries = [row["summary"] for row in rows]
    print(
        f"{name}\\t{len(rows)}\\t"
        f"{fmt(mean([s.get('latency_sec') for s in summaries]))}\\t"
        f"{fmt(mean([s.get('tokens_per_second') for s in summaries]))}\\t"
        f"{fmt(mean([s.get('gate_trigger_rate') for s in summaries]))}\\t"
        f"{fmt(mean([s.get('step0_gate_trigger_rate') for s in summaries]))}\\t"
        f"{fmt(mean([s.get('mean_attention_concentration') for s in summaries]))}\\t"
        f"{fmt(mean([s.get('attention_gate_trigger_rate') for s in summaries]))}"
    )
PY
```

- [ ] **Step 10: Apply the promotion rule**

Decision rule:

- promote only if `D-lite` or `D-main` clearly improves over `gateent03` on F1 or accuracy
- and remains clearly faster than `always-on vcd`
- otherwise archive this line as a documented negative refinement and pivot to the fallback `step0-only logit-family refinement`
