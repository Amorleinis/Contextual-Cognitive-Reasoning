from transformers import pipeline

class TransformerEngine:
    def __init__(self, model_name="distilbert-base-uncased"):
        self.pipeline = pipeline("text-classification", model=model_name)

    def analyze(self, text):
        return self.pipeline(text)
