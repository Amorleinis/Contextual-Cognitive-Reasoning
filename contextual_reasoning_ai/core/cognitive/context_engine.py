import uuid
from datetime import datetime
from neo4j import GraphDatabase

class MemoryGraphManager:
    """
    Manages creation and linking of WorkingMemory, LongTermMemory,
    SemanticMemory, and EpisodicMemory nodes in the Neo4j graph.
    """

    def __init__(self, uri="bolt://neo4j_db:7687", user="neo4j", password="securepassword"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    # ============================================================
    # Create a new WorkingMemory node
    # ============================================================
    def create_working_memory(self, content, tags=None):
        wm_id = f"wm_{uuid.uuid4().hex[:8]}"
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
    # Search for related memory nodes
    # ============================================================
    def find_related_memories(self, keywords):
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
    # Link WorkingMemory node to other memory types
    # ============================================================
    def link_memory(self, wm_id, related_nodes):
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
    # High-level process for new observations
    # ============================================================
    def process_new_observation(self, content, keywords):
        wm_node = self.create_working_memory(content, tags=keywords)
        if not wm_node:
            print("[ERROR] Failed to create WorkingMemory node.")
            return None

        wm_id = wm_node["id"]

        # Search for related memories
        related_nodes = self.find_related_memories(keywords)

        if related_nodes:
            self.link_memory(wm_id, related_nodes)
            print(f"[INFO] Linked {wm_id} to {len(related_nodes)} related memories.")
        else:
            print("[INFO] No related memories found. Node remains standalone.")

        return wm_node


# ============================================================
# Context Engine
# ============================================================
class ContextEngine:
    """
    Central reasoning engine for contextual AI.
    Integrates memory graph with cognitive reasoning.
    """

    def __init__(self):
        self.memory_graph = MemoryGraphManager()

    def analyze_text(self, text):
        """
        Process text input and store it in WorkingMemory.
        Automatically link to related memories using Neo4j graph.
        """
        print(f"[CONTEXT ENGINE] Processing new text input: {text}")

        # Generate keywords (placeholder: simple split, can use NLP later)
        keywords = [word.lower() for word in text.split() if len(word) > 3]

        # Create and link memory nodes
        wm_node = self.memory_graph.process_new_observation(text, keywords)

        return {
            "status": "processed",
            "working_memory_id": wm_node["id"] if wm_node else None,
            "keywords": keywords
        }

    def analyze_image(self, image_path):
        """
        Stub for image analysis that would connect to visual memory.
        """
        print(f"[CONTEXT ENGINE] Processing image: {image_path}")
        return {"status": "image processed", "image_path": image_path}

    def recall_memory(self, keyword):
        """
        Search memory graph for relevant past observations.
        """
        print(f"[CONTEXT ENGINE] Recalling memories for keyword: {keyword}")
        query = """
        MATCH (wm:WorkingMemory)
        WHERE toLower(wm.content) CONTAINS toLower($keyword)
        RETURN wm
        """
        with self.memory_graph.driver.session() as session:
            results = session.run(query, keyword=keyword)
            return [record["wm"] for record in results]

    def close(self):
        self.memory_graph.close()


# ============================================================
# Example standalone run
# ============================================================
if __name__ == "__main__":
    engine = ContextEngine()

    # Example text input
    response = engine.analyze_text("Suspicious network traffic detected on port 443 from IP 192.168.1.10")
    print(response)

    # Recall past related events
    recalled = engine.recall_memory("network")
    print(f"Recalled {len(recalled)} related memory nodes.")

    engine.close()

   