from neo4j import GraphDatabase
from datetime import datetime
import uuid

class MemoryGraph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_working_memory(self, content):
        wm_id = f"wm_{uuid.uuid4().hex[:8]}"  # unique ID
        timestamp = datetime.utcnow().isoformat()

        query = """
        MERGE (wm:WorkingMemory {id: $wm_id})
        ON CREATE SET wm.content = $content,
                      wm.timestamp = datetime($timestamp)
        RETURN wm
        """

        with self.driver.session() as session:
            result = session.run(query, wm_id=wm_id, content=content, timestamp=timestamp)
            return result.single()[0]

# ============================
# Example usage
if __name__ == "__main__":
    mg = MemoryGraph("bolt://localhost:7687", "neo4j", "securepassword")
    new_wm = mg.create_working_memory("Observed new network anomaly.")
    print(f"Created working memory node: {new_wm}")
    mg.close()
