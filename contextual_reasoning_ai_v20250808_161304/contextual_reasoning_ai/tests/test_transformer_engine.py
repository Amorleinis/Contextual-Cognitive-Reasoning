import unittest
from core.ai.transformer_engine import TransformerEngine

class TestTransformerEngine(unittest.TestCase):
    def setUp(self):
        self.engine = TransformerEngine()

    def test_analysis_output(self):
        result = self.engine.analyze("This is a great system.")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn("label", result[0])
        self.assertIn("score", result[0])

if __name__ == "__main__":
    unittest.main()
