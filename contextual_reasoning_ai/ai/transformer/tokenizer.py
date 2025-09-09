import spacy

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

def tokenize_text(text):
    return nlp(text)
