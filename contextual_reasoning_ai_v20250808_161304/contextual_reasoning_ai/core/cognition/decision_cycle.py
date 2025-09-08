class DecisionCycle:
    def __init__(self, wm, ltm):
        self.wm = wm
        self.ltm = ltm

    def perceive(self, sensory_input):
        self.wm.add("input", sensory_input)

    def process(self):
        input_data = self.wm.get("input")
        if input_data:
            decision = f"Analyze: {input_data}"
            self.wm.add("decision", decision)
            self.ltm.store("last_decision", decision)

    def respond(self):
        return self.wm.get("decision")
