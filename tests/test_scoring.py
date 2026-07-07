import sys
from pathlib import Path
import unittest


SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from hallucination_mitigation import EvidenceWeights, weighted_risk_score


class ScoringTests(unittest.TestCase):
    def test_weighted_risk_score_is_bounded(self):
        score = weighted_risk_score(
            probability_risk=0.9,
            visual_risk=0.7,
            attention_risk=0.3,
            anchor_risk=0.1,
        )
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)

    def test_weighted_risk_score_honors_weights(self):
        probability_only = weighted_risk_score(
            probability_risk=1.0,
            visual_risk=0.0,
            weights=EvidenceWeights(probability=1.0, visual=0.0, attention=0.0, anchor=0.0),
        )
        self.assertEqual(probability_only, 1.0)


if __name__ == "__main__":
    unittest.main()
