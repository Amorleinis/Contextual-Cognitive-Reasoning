import networkx as nx

class CyberGuardKnowledgeGraph:
    def __init__(self):
        self.graph = nx.MultiDiGraph()

    def add_entity(self, entity_type, entity_id, **attributes):
        self.graph.add_node(entity_id, type=entity_type, **attributes)

    def add_relationship(self, source_id, target_id, relationship_type, **attributes):
        self.graph.add_edge(source_id, target_id, key=relationship_type, **attributes)

    def get_neighbors(self, entity_id):
        return list(self.graph[entity_id])

    def find_path(self, start, end):
        try:
            return nx.shortest_path(self.graph, source=start, target=end)
        except nx.NetworkXNoPath:
            return None

    def get_graph(self):
        return self.graph

    def print_graph(self):
        for node, data in self.graph.nodes(data=True):
            print(f"Node: {node}, Data: {data}")
        for u, v, k, data in self.graph.edges(keys=True, data=True):
            print(f"Edge: {u} -[{k}]-> {v}, Data: {data}")
