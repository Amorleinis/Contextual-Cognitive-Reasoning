import sys
from contextual_reasoning_ai.core.cognition.working_memory import WorkingMemory
from contextual_reasoning_ai.core.cognition.long_term_memory import LongTermMemory
from contextual_reasoning_ai.core.cognition.decision_cycle import DecisionCycle
from contextual_reasoning_ai.core.cognition.behavior_module import BehaviorModule

def main():
    wm = WorkingMemory()
    ltm = LongTermMemory()
    dc = DecisionCycle(wm, ltm)
    behavior = BehaviorModule(dc)

    if len(sys.argv) > 1:
        input_text = " ".join(sys.argv[1:])
    else:
        input_text = input("Enter text: ")

    dc.perceive(input_text)
    dc.process()
    response = behavior.act()
    print("AI Response:", response)

if __name__ == "__main__":
    main()
