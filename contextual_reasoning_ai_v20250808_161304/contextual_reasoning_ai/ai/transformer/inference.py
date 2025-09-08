from .tokenizer import tokenize_text

def extract_entities(text):
    doc = tokenize_text(text)
    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_
        })
    return entities

# Example usage
if __name__ == "__main__":
    sample = "Alice connected her laptop to 192.168.0.0/24 and was exposed to CVE-2023-1234."
    entities = extract_entities(sample)
    for ent in entities:
        print(f"Entity: {ent['text']} (label: {ent['label']})")
