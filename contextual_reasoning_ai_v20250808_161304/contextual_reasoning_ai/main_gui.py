import tkinter as tk
from core.cognition.working_memory import WorkingMemory
from core.cognition.long_term_memory import LongTermMemory
from core.cognition.decision_cycle import DecisionCycle
from core.cognition.behavior_module import BehaviorModule

class ContextualAIApp:
    def __init__(self, root):
        self.wm = WorkingMemory()
        self.ltm = LongTermMemory()
        self.dc = DecisionCycle(self.wm, self.ltm)
        self.behavior = BehaviorModule(self.dc)

        root.title("Contextual Reasoning AI")
        root.geometry("600x400")

        self.input_text = tk.StringVar()
        self.response_text = tk.StringVar()

        tk.Label(root, text="Input:").pack()
        tk.Entry(root, textvariable=self.input_text, width=80).pack()
        tk.Button(root, text="Process", command=self.process_input).pack()
        tk.Label(root, text="Response:").pack()
        tk.Label(root, textvariable=self.response_text, wraplength=500, fg="blue").pack()

    def process_input(self):
        data = self.input_text.get()
        self.dc.perceive(data)
        self.dc.process()
        response = self.behavior.act()
        self.response_text.set(response)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContextualAIApp(root)
    root.mainloop()
