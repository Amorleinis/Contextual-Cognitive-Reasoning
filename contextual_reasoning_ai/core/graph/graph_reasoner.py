from .graph_engine import KnowledgeGraph

class GraphReasoner:
    def __init__(self, graph: KnowledgeGraph):
        self.graph = graph

    def detect_threat_path(self, user_id):
        # Start from the user and search for paths to known threats
        threat_nodes = [n for n, d in self.graph.graph.nodes(data=True) if d.get("type") == "Threat"]
        paths = []
        for threat in threat_nodes:
            found_paths = self.graph.find_paths(user_id, threat)
            for path in found_paths:
                paths.append({
                    "path": path,
                    "threat": threat,
                    "length": len(path)
                })
        return paths

    def summarize_paths(self, paths):
        if not paths:
            return "No threat paths found."
        summary = []
        for p in paths:
            summary.append(f"Path to {p['threat']}: {' -> '.join(p['path'])} (Length: {p['length']})")
        return "\n".join(summary)
