class WorkingMemory:
    def __init__(self):
        self.memory = {}

    def update(self, key, value):
        self.memory[key] = value

    def retrieve(self, key):
        return self.memory.get(key, None)

    def clear(self):
        self.memory.clear()