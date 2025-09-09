from core.ai.transformer_engine import TransformerEngine

class CognitiveProcessor:
    def __init__(self):
        self.transformer = TransformerEngine()
        self.working_memory = {}

    def perceive(self, input_text):
        print("Perceiving input...")
        analysis = self.transformer.analyze(input_text)
        self.working_memory["analysis"] = analysis

    def decide(self):
        print("Deciding based on analysis...")
        analysis = self.working_memory.get("analysis", [])
        if analysis and analysis[0]["label"] == "POSITIVE":
            return "Take proactive security measures."
        else:
            return "Initiate risk mitigation protocol."

    def respond(self):
        decision = self.decide()
        print("Responding:", decision)
        return decision

    def run_cycle(self, input_text):
        self.perceive(input_text)
        return self.respond()
