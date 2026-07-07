from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "results" / "public"
MAIN_MODELS = {"LLaVA-1.5-7B", "InstructBLIP-7B"}
MAIN_METHODS = {"Regular", "FLB", "OCV (Regular source)", "OCV (FLB source)"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def fmt_float(value: str) -> str:
    number = float(value)
    if abs(number) < 1:
        return f"{number:.4f}"
    return f"{number:.1f}"


def reduction(baseline: str, proposed: str) -> str:
    if not baseline or not proposed:
        return ""
    base = float(baseline)
    prop = float(proposed)
    if base == 0:
        return f"{base - prop:.4f}"
    delta = base - prop
    relative = delta / base * 100.0
    if abs(base) < 1:
        return f"{delta:.4f} ({relative:.1f}%)"
    return f"{delta:.1f} ({relative:.1f}%)"


def build_main_table(rows: list[dict[str, str]]) -> list[str]:
    selected = [
        row
        for row in rows
        if row["model"] in MAIN_MODELS
        and row["method"] in MAIN_METHODS
        and row["benchmark"] in {"COCO/CHAIR-500", "AMBER-1004", "OpenCHAIR"}
    ]

    grouped: dict[tuple[str, str], dict[str, dict[str, str]]] = defaultdict(dict)
    for row in selected:
        grouped[(row["model"], row["benchmark"])][row["method"]] = row

    lines = [
        "## Main Caption-Side Results",
        "",
        "Lower is better for CHAIRs, CHAIRi, AMBER CHAIR, AMBER Hal, OpenCHAIR, and Sentence.",
        "",
        "| Model | Benchmark | Metric | Regular | FLB | OCV on Regular | OCV on FLB | Reduction vs FLB |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for (model, benchmark), methods in sorted(grouped.items()):
        regular = methods.get("Regular", {})
        flb = methods.get("FLB", {})
        ocv_regular = methods.get("OCV (Regular source)", {})
        ocv_flb = methods.get("OCV (FLB source)", {})
        metric_name = regular.get("primary_metric_name") or ocv_flb.get("primary_metric_name")
        lines.append(
            "| {model} | {benchmark} | {metric} | {regular} | {flb} | {ocv_regular} | {ocv_flb} | {delta} |".format(
                model=model,
                benchmark=benchmark,
                metric=metric_name,
                regular=fmt_float(regular["primary_value"]) if regular.get("primary_value") else "",
                flb=fmt_float(flb["primary_value"]) if flb.get("primary_value") else "",
                ocv_regular=fmt_float(ocv_regular["primary_value"]) if ocv_regular.get("primary_value") else "",
                ocv_flb=fmt_float(ocv_flb["primary_value"]) if ocv_flb.get("primary_value") else "",
                delta=reduction(flb.get("primary_value", ""), ocv_flb.get("primary_value", "")),
            )
        )
    return lines


def build_cross_model_table(rows: list[dict[str, str]]) -> list[str]:
    lines = [
        "## Cross-Model OpenCHAIR Summary",
        "",
        "| Model | Regular | FLB | OCV on Regular | OCV on FLB | Caveat |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    grouped: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in rows:
        if row["benchmark"] == "OpenCHAIR" and row["method"] in MAIN_METHODS:
            grouped[row["model"]][row["method"]] = row
    for model, methods in sorted(grouped.items()):
        caveats = [
            row["caveat"]
            for row in methods.values()
            if "regular-equivalent" in row.get("caveat", "").lower()
        ]
        lines.append(
            "| {model} | {regular} | {flb} | {ocv_regular} | {ocv_flb} | {caveat} |".format(
                model=model,
                regular=fmt_float(methods["Regular"]["primary_value"]),
                flb=fmt_float(methods["FLB"]["primary_value"]),
                ocv_regular=fmt_float(methods["OCV (Regular source)"]["primary_value"]),
                ocv_flb=fmt_float(methods["OCV (FLB source)"]["primary_value"]),
                caveat=caveats[0] if caveats else "",
            )
        )
    return lines


def build_external_table(rows: list[dict[str, str]]) -> list[str]:
    lines = [
        "## External Baseline Records",
        "",
        "These rows are included as reproduced/caveated context, not official leaderboard claims.",
        "",
        "| Method | Benchmark | Scope | CHAIRs | CHAIRi | POPE Acc | POPE F1 | Status | Caveat |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {method} | {benchmark} | {scope} | {chairs} | {chairi} | {acc} | {f1} | {status} | {caveat} |".format(
                method=row["method"],
                benchmark=row["benchmark"],
                scope=row["scope"],
                chairs=row["chairs"],
                chairi=row["chairi"],
                acc=row["pope_accuracy"],
                f1=row["pope_f1"],
                status=row["status"],
                caveat=row["caveat"],
            )
        )
    return lines


def build_runtime_table(rows: list[dict[str, str]]) -> list[str]:
    lines = [
        "## Runtime Summary",
        "",
        "| Model | Benchmark | Stage | Images | Total sec | Sec/image | Includes generation? | Includes verification? |",
        "| --- | --- | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {model} | {benchmark} | {stage} | {images} | {total} | {per_image} | {generation} | {verification} |".format(
                model=row["model"],
                benchmark=row["benchmark"],
                stage=row["stage"],
                images=row["num_images"],
                total=row["total_sec"],
                per_image=row["sec_per_image"],
                generation=row["includes_generation_time"],
                verification=row["includes_signal_extraction_forward"],
            )
        )
    return lines


def main() -> None:
    caption_rows = read_csv(PUBLIC / "caption_side_results.csv")
    external_rows = read_csv(PUBLIC / "external_baselines.csv")
    runtime_rows = read_csv(PUBLIC / "runtime_summary.csv")

    lines = ["# Public Result Tables", ""]
    for section in (
        build_main_table(caption_rows),
        build_cross_model_table(caption_rows),
        build_external_table(external_rows),
        build_runtime_table(runtime_rows),
    ):
        lines.extend(section)
        lines.append("")

    (PUBLIC / "result_table.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
