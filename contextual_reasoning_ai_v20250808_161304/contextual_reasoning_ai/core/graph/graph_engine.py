import networkx as nx

class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self._build_initial_graph()

    def _build_initial_graph(self):
        self.graph.add_node("User_A", type="User", location="US")
        self.graph.add_node("Device_X", type="Device", os="Windows")
        self.graph.add_node("Network_1", type="Network", ip_range="192.168.1.0/24")
        self.graph.add_node("Threat_Z", type="Threat", severity="High")
        self.graph.add_node("Vuln_Y", type="Vulnerability", cve="CVE-2025-1234")

        self.graph.add_edge("User_A", "Device_X", relation="owns")
        self.graph.add_edge("Device_X", "Network_1", relation="connected_to")
        self.graph.add_edge("Network_1", "Threat_Z", relation="exposed_to")
        self.graph.add_edge("Threat_Z", "Vuln_Y", relation="exploits")

    def get_neighbors(self, node):
        return list(self.graph.successors(node))

    def find_paths(self, source, target):
        try:
            return list(nx.all_simple_paths(self.graph, source=source, target=target))
        except nx.NetworkXNoPath:
            return []

    def describe(self):
        return nx.nx_pydot.to_pydot(self.graph).to_string()
