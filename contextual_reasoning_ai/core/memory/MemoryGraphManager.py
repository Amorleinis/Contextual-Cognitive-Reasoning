from neo4j import GraphDatabase
from datetime import datetime
import uuid

class MemoryGraphManager:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    # ============================================================
    # Create a new WorkingMemory node dynamically
    # ============================================================
    def create_working_memory(self, content, tags=None):
        """
        Create a unique WorkingMemory node with timestamp and optional tags.
        """
        wm_id = f"wm_{uuid.uuid4().hex[:8]}"  # unique ID
        timestamp = datetime.utcnow().isoformat()
        tags = tags if tags else []

        query = """
        MERGE (wm:WorkingMemory {id: $wm_id})
        ON CREATE SET wm.content = $content,
                      wm.timestamp = datetime($timestamp),
                      wm.tags = $tags
        RETURN wm
        """

        with self.driver.session() as session:
            result = session.run(query, wm_id=wm_id, content=content, timestamp=timestamp, tags=tags)
            wm_node = result.single()
            return wm_node[0] if wm_node else None

    # ============================================================
    # Find related memory nodes using simple keyword matching
    # ============================================================
    def find_related_memories(self, keywords):
        """
        Search LongTermMemory, SemanticMemory, and EpisodicMemory for matches.
        """
        query = """
        MATCH (m)
        WHERE (m:LongTermMemory OR m:SemanticMemory OR m:EpisodicMemory)
          AND any(keyword IN $keywords WHERE toLower(m.content) CONTAINS toLower(keyword))
        RETURN m
        """

        with self.driver.session() as session:
            results = session.run(query, keywords=keywords)
            return [record["m"] for record in results]

    # ============================================================
    # Link new WorkingMemory node to relevant memories
    # ============================================================
    def link_memory(self, wm_id, related_nodes):
        """
        Link a new WorkingMemory node to relevant memories dynamically.
        """
        with self.driver.session() as session:
            for node in related_nodes:
                if "LongTermMemory" in node.labels:
                    relation = "REFERS_TO"
                elif "SemanticMemory" in node.labels:
                    relation = "RELATES_TO"
                elif "EpisodicMemory" in node.labels:
                    relation = "RECALLS"
                else:
                    relation = "ASSOCIATED_WITH"

                query = f"""
                MATCH (wm:WorkingMemory {{id: $wm_id}}), (target {{id: $target_id}})
                MERGE (wm)-[:{relation}]->(target)
                """
                session.run(query, wm_id=wm_id, target_id=node["id"])

    # ============================================================
    # High-level function to create and connect WorkingMemory
    # ============================================================
    def process_new_observation(self, content, keywords):
        """
        1. Create a new WorkingMemory node.
        2. Find related memories based on keywords.
        3. Link them together in the graph.
        """
        print(f"[INFO] Creating new working memory for: {content}")
        wm_node = self.create_working_memory(content, tags=keywords)
        if not wm_node:
            print("[ERROR] Failed to create WorkingMemory node.")
            return None

        wm_id = wm_node["id"]

        print(f"[INFO] Searching for related memories using keywords: {keywords}")
        related_nodes = self.find_related_memories(keywords)

        if related_nodes:
            print(f"[INFO] Linking {wm_id} to {len(related_nodes)} related memories...")
            self.link_memory(wm_id, related_nodes)
        else:
            print("[INFO] No related memories found. Node remains standalone.")

        return wm_node

# ============================================================
# Example Usage
# ============================================================
if __name__ == "__main__":
    mg = MemoryGraphManager("bolt://localhost:7687", "neo4j", "securepassword")

    # New observation comes in
    observation = "Suspicious network traffic detected on port 443."
    keywords = ["network", "traffic", "suspicious"]

    new_wm = mg.process_new_observation(observation, keywords)

    if new_wm:
        print(f"[SUCCESS] Created and linked WorkingMemory node: {new_wm['id']}")

    mg.close()
