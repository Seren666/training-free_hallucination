from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class SpanEdit:
    """A bounded text edit over an existing decoded caption."""

    start: int
    end: int
    replacement: str = ""
    reason: str = ""

    def validate(self, text_length: int) -> None:
        if self.start < 0 or self.end < 0:
            raise ValueError("edit offsets must be non-negative")
        if self.start > self.end:
            raise ValueError("edit start must be <= edit end")
        if self.end > text_length:
            raise ValueError("edit end exceeds caption length")


_SPACE_RE = re.compile(r"\s+")
_SPACE_BEFORE_PUNCT_RE = re.compile(r"\s+([,.;:!?])")
_DOUBLE_PUNCT_RE = re.compile(r"([,.;:!?])\1+")


def normalize_caption_spacing(text: str) -> str:
    """Normalize whitespace after bounded edits without rewriting content."""

    cleaned = _SPACE_RE.sub(" ", text).strip()
    cleaned = _SPACE_BEFORE_PUNCT_RE.sub(r"\1", cleaned)
    cleaned = _DOUBLE_PUNCT_RE.sub(r"\1", cleaned)
    return cleaned


def apply_span_edits(caption: str, edits: list[SpanEdit]) -> str:
    """Apply non-overlapping span edits to a caption.

    Edits are applied right-to-left so offsets remain stable. The function is
    deliberately conservative: overlapping edits are rejected rather than
    guessed.
    """

    for edit in edits:
        edit.validate(len(caption))

    ordered = sorted(edits, key=lambda item: (item.start, item.end))
    previous_end = -1
    for edit in ordered:
        if edit.start < previous_end:
            raise ValueError("overlapping edits are not allowed")
        previous_end = edit.end

    edited = caption
    for edit in reversed(ordered):
        edited = edited[: edit.start] + edit.replacement + edited[edit.end :]
    return normalize_caption_spacing(edited)
