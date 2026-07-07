from __future__ import annotations

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAX_FILE_BYTES = 5 * 1024 * 1024
FORBIDDEN_SUFFIXES = {
    ".bin",
    ".ckpt",
    ".h5",
    ".jsonl",
    ".npy",
    ".npz",
    ".parquet",
    ".pdf",
    ".pt",
    ".pth",
    ".safetensors",
}
FORBIDDEN_PARTS = {
    "__pycache__",
    ".cache",
    ".huggingface",
    "artifacts",
    "cache",
    "caches",
    "checkpoints",
    "data",
    "datasets",
    "hf-home",
    "logs",
    "outputs",
    "runs",
    "tensorboard",
    "tmp",
    "wandb",
}
SECRET_RE = re.compile(
    r"(api[_-]?key\s*[:=]|secret\s*[:=]|password\s*[:=]|token\s*[:=]|ssh\s+-p\s+\d+\s+\w+@|connect\.[\w.-]+)",
    re.IGNORECASE,
)
TEXT_SUFFIXES = {".csv", ".md", ".py", ".toml", ".txt", ".yml", ".yaml"}


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return [ROOT / line.strip() for line in result.stdout.splitlines() if line.strip()]


def main() -> None:
    failures: list[str] = []
    for path in tracked_files():
        rel = path.relative_to(ROOT).as_posix()
        parts = set(path.relative_to(ROOT).parts)
        suffix = path.suffix.lower()

        if suffix in FORBIDDEN_SUFFIXES:
            failures.append(f"forbidden artifact suffix: {rel}")
        if parts & FORBIDDEN_PARTS:
            failures.append(f"forbidden artifact directory: {rel}")
        if path.exists() and path.stat().st_size > MAX_FILE_BYTES:
            failures.append(f"file exceeds 5 MiB: {rel}")
        if suffix in TEXT_SUFFIXES and path.exists():
            text = path.read_text(encoding="utf-8", errors="ignore")
            if SECRET_RE.search(text):
                failures.append(f"possible secret or remote endpoint: {rel}")

    if failures:
        raise SystemExit("Repository hygiene check failed:\n" + "\n".join(failures))
    print("Repository hygiene check passed.")


if __name__ == "__main__":
    main()
