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
