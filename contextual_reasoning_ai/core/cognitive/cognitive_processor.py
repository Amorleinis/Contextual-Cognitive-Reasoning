from transformers import pipeline

class CognitiveProcessor:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        self.memory = {
            "working": [],
            "long_term": []
        }

    def perceive(self, input_text):
        self.memory["working"].append(input_text)
        return input_text

    def process(self):
        if not self.memory["working"]:
            return "No input to process."
        summary = self.summarizer(self.memory["working"][-1], max_length=60, min_length=20, do_sample=False)
        decision = self.decide(summary[0]["summary_text"])
        return decision

    def decide(self, processed_info):
        self.memory["long_term"].append(processed_info)
        return f"[DECISION] Action taken based on: {processed_info}"

    def show_memory(self):
        return {
            "Working Memory": self.memory["working"],
            "Long-Term Memory": self.memory["long_term"]
        }
    
    def create_memory_node(self, content):
        node = {
            "id": len(self.memory["long_term"]) + 1,
            "content": content
        }
        self.memory["long_term"].append(node)
        return node
    
    def retrieve_memory_node(self, node_id):
        for node in self.memory["long_term"]:
            if isinstance(node, dict) and node.get("id") == node_id:
                return node
        return None
    
    def update_memory_node(self, node_id, new_content):
        for node in self.memory["long_term"]:
            if isinstance(node, dict) and node.get("id") == node_id:
                node["content"] = new_content
                return node
        return None
    
    def short_term_memory_node(self, content):
        node = {
            "id": len(self.memory["working"]) + 1,
            "content": content
        }
        self.memory["working"].append(node)
        return node
    
    def long_term_memory_node(self, content):
        node = {
            "id": len(self.memory["long_term"]) + 1,
            "content": content
        }
        self.memory["long_term"].append(node)
        return node 