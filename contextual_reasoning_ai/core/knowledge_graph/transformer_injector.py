def add_ai_detected_threat(kg):
    threat_id = "threat_phish_001"
    kg.add_entity("Threat", threat_id, type="Phishing", severity="Medium")
    kg.add_relationship(threat_id, "vuln_1", "exploits")
    kg.add_relationship("net_1", threat_id, "exposed_to")
