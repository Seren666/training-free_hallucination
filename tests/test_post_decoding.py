import sys
from pathlib import Path
import unittest


SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from hallucination_mitigation import SpanEdit, apply_span_edits


class PostDecodingTests(unittest.TestCase):
    def test_apply_span_edits_removes_object_phrase(self):
        caption = "A man sits beside a bicycle and a phantom umbrella."
        start = caption.index(" and a phantom umbrella")
        edited = apply_span_edits(caption, [SpanEdit(start=start, end=len(caption) - 1, reason="unsupported")])
        self.assertEqual(edited, "A man sits beside a bicycle.")

    def test_overlapping_edits_are_rejected(self):
        with self.assertRaises(ValueError):
            apply_span_edits("A red car.", [SpanEdit(2, 7), SpanEdit(4, 8)])


if __name__ == "__main__":
    unittest.main()
