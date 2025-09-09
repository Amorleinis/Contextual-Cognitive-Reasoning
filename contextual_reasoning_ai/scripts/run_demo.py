from core.knowledge_graph.graph_builder import CyberGuardKnowledgeGraph
from core.knowledge_graph.visualizer import visualize_knowledge_graph
from core.knowledge_graph.exporter import export_nodes_to_csv, export_edges_to_csv, export_graph_to_json
from core.knowledge_graph.transformer_injector import add_ai_detected_threat

if __name__ == "__main__":
    kg = CyberGuardKnowledgeGraph()

    kg.add_entity("User", "user_1", name="Alice", role="Admin", location="USA")
    kg.add_entity("Device", "device_1", device_id="D123", type="Laptop", OS="Windows")
    kg.add_entity("Network", "net_1", network_id="N001", subnet="192.168.0.0/24", exposure_level="High")
    kg.add_entity("Threat", "threat_1", threat_id="T001", type="Malware", severity="Critical")
    kg.add_entity("Vulnerability", "vuln_1", cve_id="CVE-2023-1234", description="RCE", severity="High")

    kg.add_relationship("user_1", "device_1", "owns")
    kg.add_relationship("device_1", "net_1", "connects_to")
    kg.add_relationship("net_1", "threat_1", "exposed_to")
    kg.add_relationship("threat_1", "vuln_1", "exploits")

    add_ai_detected_threat(kg)

    kg.print_graph()
    visualize_knowledge_graph(kg.get_graph())

    export_nodes_to_csv(kg.get_graph())
    export_edges_to_csv(kg.get_graph())
    export_graph_to_json(kg.get_graph())
