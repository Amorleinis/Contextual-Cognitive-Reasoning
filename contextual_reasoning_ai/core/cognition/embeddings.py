# embeddings.py
# Manage text embeddings and store/retrieve them from Neo4j.
# Uses sentence-transformers for local embedding generation.

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from neo4j import GraphDatabase
import os
from typing import List, Dict, Any

class EmbeddingManager:
    def __init__(self,
                 model_name: str = "all-MiniLM-L6-v2",
                 neo4j_uri: str = None,
                 neo4j_user: str = None,
                 neo4j_password: str = None):
        # Load model (this may download weights the first time)
        self.model = SentenceTransformer(model_name)

        # Neo4j connection (optional; only needed if you want to write embeddings to Neo4j)
        self.neo4j_uri = neo4j_uri or os.getenv("NEO4J_URI", "bolt://neo4j_db:7687")
        self.neo4j_user = neo4j_user or os.getenv("NEO4J_USER", "neo4j")
        self.neo4j_password = neo4j_password or os.getenv("NEO4J_PASSWORD", "securepassword")
        self.driver = GraphDatabase.driver(self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_password))

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Produce embeddings for a list of texts (returns list-of-lists of floats).
        """
        embs = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        # convert to python lists for storage in Neo4j
        return [emb.tolist() for emb in embs]

    def embed_text(self, text: str) -> List[float]:
        return self.embed_texts([text])[0]

    # ------------------------
    # Neo4j storage helpers
    # ------------------------
    def store_embedding_on_node(self, node_label: str, node_id: str, embedding: List[float]) -> None:
        """
        Store an embedding list on a node in Neo4j as property `embedding`.
        """
        query = f"""
        MATCH (n:{node_label} {{id: $node_id}})
        SET n.embedding = $embedding
        RETURN n.id
        """
        with self.driver.session() as session:
            session.run(query, node_id=node_id, embedding=embedding)

    def get_nodes_with_embeddings(self, memory_label: str = None, limit: int = 1000) -> List[Dict[str, Any]]:
        """
        Retrieve nodes (id, content, embedding) from Neo4j that have an embedding property.
        Optionally filter by memory label.
        """
        if memory_label:
            query = f"""
            MATCH (n:{memory_label})
            WHERE exists(n.embedding)
            RETURN n.id AS id, n.content AS content, n.embedding AS embedding
            ORDER BY n.timestamp DESC
            LIMIT $limit
            """
        else:
            query = """
            MATCH (n)
            WHERE exists(n.embedding)
            RETURN labels(n)[0] AS label, n.id AS id, n.content AS content, n.embedding AS embedding
            ORDER BY n.timestamp DESC
            LIMIT $limit
            """
        with self.driver.session() as session:
            result = session.run(query, limit=limit)
            rows = []
            for r in result:
                row = dict(r)
                # Ensure embedding is list of floats
                if "embedding" in row and row["embedding"] is not None:
                    # Neo4j driver returns a list-like object; keep as python list
                    row["embedding"] = [float(x) for x in row["embedding"]]
                rows.append(row)
            return rows

    # ------------------------
    # Similarity functions
    # ------------------------
    @staticmethod
    def _cosine_sim_matrix(query_vec: np.ndarray, matrix: np.ndarray) -> np.ndarray:
        """
        Expect shape: query_vec (1, D), matrix (N, D) -> returns (N,)
        """
        # Use sklearn's pairwise cosine_similarity which handles norms
        sims = cosine_similarity(query_vec, matrix)  # shape (1, N)
        return sims.flatten()

    def find_top_k_similar(self, query: str, k: int = 5, memory_label: str = None, candidate_limit: int = 1000) -> List[Dict[str, Any]]:
        """
        1) embed the query
        2) load candidate nodes with embeddings
        3) compute cosine similarity and return top-k nodes
        """
        # 1. embed query
        q_vec = np.array(self.embed_text(query)).reshape(1, -1)  # shape (1, D)

        # 2. get candidates
        candidates = self.get_nodes_with_embeddings(memory_label=memory_label, limit=candidate_limit)
        if not candidates:
            return []

        emb_matrix = np.array([c["embedding"] for c in candidates])  # shape (N, D)

        # 3. compute similarities
        sims = self._cosine_sim_matrix(q_vec, emb_matrix)  # shape (N,)
        # attach sims back to candidates
        for i, c in enumerate(candidates):
            c["score"] = float(sims[i])

        # 4. sort and return top-k
        candidates.sort(key=lambda x: x["score"], reverse=True)
        return candidates[:k]

    # ------------------------
    # Convenience: embed & store node content
    # ------------------------
    def embed_and_store_node(self, node_label: str, node_id: str, content: str) -> None:
        emb = self.embed_text(content)
        self.store_embedding_on_node(node_label, node_id, emb)

    def close(self):
        self.driver.close()
