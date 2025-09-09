def map_entity_to_type(label, text):
    # Simple mapping based on label or pattern
    if label == "PERSON":
        return "User"
    elif "CVE" in text:
        return "Vulnerability"
    elif "/" in text:
        return "Network"
    elif label == "ORG":
        return "Threat"
    else:
        return "Unknown"

def inject_entities_into_graph(kg, entities):
    for i, ent in enumerate(entities):
        ent_type = map_entity_to_type(ent["label"], ent["text"])
        ent_id = f"{ent_type.lower()}_{i}_{ent['text'].replace(' ', '_')}"
        if ent_type != "Unknown":
            kg.add_entity(ent_type, ent_id, label=ent["text"])
