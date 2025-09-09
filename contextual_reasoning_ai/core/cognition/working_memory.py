class WorkingMemory:
    def __init__(self):
        self.memory = {}

    def add(self, key, value):
        self.memory[key] = value

    def get(self, key):
        return self.memory.get(key)

    def clear(self):
        self.memory.clear()
    