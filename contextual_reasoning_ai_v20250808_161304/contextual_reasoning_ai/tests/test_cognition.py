import unittest
from core.cognition.working_memory import WorkingMemory
from core.cognition.long_term_memory import LongTermMemory
from core.cognition.decision_cycle import DecisionCycle
from core.cognition.behavior_module import BehaviorModule

class TestCognitiveModules(unittest.TestCase):
    def test_working_memory(self):
        wm = WorkingMemory()
        wm.store("test input")
        self.assertIn("test input", wm.get_all())

    def test_long_term_memory(self):
        ltm = LongTermMemory()
        ltm.remember("key", "value")
        self.assertEqual(ltm.recall("key"), "value")

    def test_decision_cycle(self):
        wm = WorkingMemory()
        ltm = LongTermMemory()
        dc = DecisionCycle(wm, ltm)
        dc.perceive("alert")
        dc.process()
        self.assertIn("alert", wm.get_all())

    def test_behavior_module(self):
        wm = WorkingMemory()
        ltm = LongTermMemory()
        dc = DecisionCycle(wm, ltm)
        behavior = BehaviorModule(dc)
        dc.perceive("threat detected")
        dc.process()
        action = behavior.act()
        self.assertIsInstance(action, str)

if __name__ == '__main__':
    unittest.main()
