class LongTermMemory:
    def __init__(self):
        self.knowledge = {}

    def store(self, key, value):
        self.knowledge[key] = value

    def recall(self, key):
        return self.knowledge.get(key)

    def all_knowledge(self):
        return self.knowledge
