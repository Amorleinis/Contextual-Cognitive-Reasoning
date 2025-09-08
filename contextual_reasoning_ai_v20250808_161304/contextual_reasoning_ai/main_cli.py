from core.cognition.working_memory import WorkingMemory
from core.cognition.long_term_memory import LongTermMemory
from core.cognition.decision_cycle import DecisionCycle
from core.cognition.behavior_module import BehaviorModule
from core.sensors.simulation_input import SensorInputSimulator

def run_cli():
    wm = WorkingMemory()
    ltm = LongTermMemory()
    dc = DecisionCycle(wm, ltm)
    behavior = BehaviorModule(dc)
    sensor = SensorInputSimulator()

    print("🧠 Contextual Reasoning AI - CLI Active")
    for input_data in sensor.stream():
        print(f"🛰️ Sensor: {input_data}")
        dc.perceive(input_data)
        dc.process()
        response = behavior.act()
        print(f"🤖 Response: {response}\n")

if __name__ == "__main__":
    run_cli()
