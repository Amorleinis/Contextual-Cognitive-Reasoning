from py2neo import Graph
import torch
from torch_geometric.data import Data

def load_graph_from_neo4j(uri, user, password):
    graph = Graph(uri, auth=(user, password))

    query_nodes = "MATCH (n) RETURN ID(n) as id"
    query_edges = "MATCH (n)-[r]->(m) RETURN ID(n) as src, ID(m) as dst"

    node_results = graph.run(query_nodes).data()
    edge_results = graph.run(query_edges).data()

    id_map = {node['id']: i for i, node in enumerate(node_results)}
    x = torch.eye(len(node_results))  # Dummy features (identity matrix)

    edge_index = torch.tensor([[id_map[e['src']], id_map[e['dst']]] for e in edge_results], dtype=torch.long).t().contiguous()

    data = Data(x=x, edge_index=edge_index)
    return data