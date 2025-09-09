class BehaviorModule:
    def __init__(self, decision_cycle):
        self.dc = decision_cycle

    def act(self):
        decision = self.dc.respond()
        if decision:
            if "CVE" in decision:
                return "Flagged potential vulnerability for review"
            elif "Analyze" in decision:
                return "Performing threat analysis"
            else:
                return f"Default action: {decision}"
        return "No decision made"
