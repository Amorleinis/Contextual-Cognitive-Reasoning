import torch
from working_memory import WorkingMemory
from decision_cycle import DecisionCycle

# Simulated input vectors
gnn_output = torch.randn(1, 768)
transformer_output = torch.randn(1, 768)

wm = WorkingMemory()
dc = DecisionCycle(wm)

dc.perceive(gnn_output, transformer_output)
decision_vector = dc.process()
response = dc.respond()

print("Response:", response)