class DecisionCycle:
    def __init__(self, working_memory):
        self.working_memory = working_memory

    def perceive(self, gnn_output, transformer_output):
        self.working_memory.update("gnn", gnn_output)
        self.working_memory.update("transformer", transformer_output)

    def process(self):
        gnn_vector = self.working_memory.retrieve("gnn")
        transformer_vector = self.working_memory.retrieve("transformer")
        # Simplified reasoning: weighted average
        if gnn_vector is not None and transformer_vector is not None:
            decision_vector = (gnn_vector + transformer_vector) / 2
            self.working_memory.update("decision", decision_vector)
            return decision_vector
        return None

    def respond(self):
        decision = self.working_memory.retrieve("decision")
        if decision is not None:
            return "Threat context understood. Action recommended."
        return "Insufficient data for decision."