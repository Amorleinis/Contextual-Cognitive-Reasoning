import json
import csv

def export_nodes_to_csv(graph, filename="nodes.csv"):
    with open(filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Type", "Attributes"])
        for node, data in graph.nodes(data=True):
            writer.writerow([node, data.get("type", ""), json.dumps(data)])

def export_edges_to_csv(graph, filename="edges.csv"):
    with open(filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Source", "Target", "Relationship", "Attributes"])
        for u, v, k, data in graph.edges(keys=True, data=True):
            writer.writerow([u, v, k, json.dumps(data)])

def export_graph_to_json(graph, filename="graph.json"):
    data = {
        "nodes": [
            {"id": n, "type": d.get("type"), "attributes": d}
            for n, d in graph.nodes(data=True)
        ],
        "edges": [
            {"source": u, "target": v, "relationship": k, "attributes": d}
            for u, v, k, d in graph.edges(keys=True, data=True)
        ]
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
