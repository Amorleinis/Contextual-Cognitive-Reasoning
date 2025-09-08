import matplotlib.pyplot as plt
import networkx as nx

def visualize_knowledge_graph(graph, title="CyberGuard Knowledge Graph"):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(12, 8))

    node_labels = {node: f"{data['type']}:\n{node}" for node, data in graph.nodes(data=True)}
    edge_labels = {(u, v): k for u, v, k in graph.edges(keys=True)}

    nx.draw_networkx_nodes(graph, pos, node_size=1000, node_color="skyblue")
    nx.draw_networkx_edges(graph, pos, arrows=True)
    nx.draw_networkx_labels(graph, pos, labels=node_labels, font_size=8)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)

    plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    plt.show()
