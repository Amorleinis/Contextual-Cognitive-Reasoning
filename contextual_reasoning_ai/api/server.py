# server.py (full updated)
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from contextual_reasoning_ai.core.cognition.context_engine import ContextEngine
from contextual_reasoning_ai.simulation.threat_simulator import ThreatSimulator
from contextual_reasoning_ai.multimodal.audio_analyzer import AudioAnalyzer
from contextual_reasoning_ai.db.neo4j_connector import Neo4jConnector
from contextual_reasoning_ai.core.cognition.embeddings import EmbeddingManager
import shutil
import os
import uuid
from datetime import datetime
from typing import Optional, List

app = FastAPI(title="Contextual Reasoner API")

# Initialize engines & connectors
engine = ContextEngine()
neo4j_conn = Neo4jConnector()
embedding_manager = EmbeddingManager()  # default model & neo4j connection via env

# ======================================
# Data Models
# ======================================

class TextInput(BaseModel):
    text: str

class MemoryInput(BaseModel):
    content: str
    memory_type: str  # 'working', 'long_term', 'episodic', 'semantic', 'procedural'
    link_to: Optional[str] = None  # Optional memory type to link this node to
    embed: bool = False  # If true, compute & store embedding immediately

class MemorySearchInput(BaseModel):
    query: str
    memory_type: Optional[str] = None  # Optional filter by memory type
    limit: int = 10
    top_k: int = 5

# Memory type mapping (same as before)
MEMORY_MAP = {
    "working": "WorkingMemory",
    "long_term": "LongTermMemory",
    "episodic": "EpisodicMemory",
    "semantic": "SemanticMemory",
    "procedural": "ProceduralMemory"
}

# ======================================
# Simple helpers
# ======================================
def determine_relationship(src_type, target_type):
    relationships = {
        ("working", "long_term"): "TRANSFERS_TO",
        ("long_term", "episodic"): "CONTAINS_EPISODES",
        ("long_term", "semantic"): "CONTAINS_FACTS",
        ("long_term", "procedural"): "CONTAINS_SKILLS",
        ("episodic", "semantic"): "RELATED_TO",
        ("semantic", "procedural"): "INFORMS"
    }
    return relationships.get((src_type, target_type), "RELATED_TO")

# ======================================
# Basic analysis endpoints
# ======================================
@app.post("/analyze/text")
def analyze_text(data: TextInput):
    return engine.analyze_text(data.text)

@app.post("/analyze/image")
async def analyze_image(file: UploadFile = File(...)):
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    result = engine.analyze_image(temp_path)
    os.remove(temp_path)
    return result

@app.post("/analyze/audio")
async def analyze_audio(file: UploadFile = File(...)):
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    analyzer = AudioAnalyzer()
    result = analyzer.analyze_audio(temp_path)
    os.remove(temp_path)
    return {"transcription": result}

@app.post("/simulate/threats")
def simulate_threats():
    simulator = ThreatSimulator()
    simulator.simulate()
    return {"status": "Simulation completed"}

# ======================================
# Memory creation (supports embedding)
# ======================================
@app.post("/memory/create")
def create_memory(data: MemoryInput):
    if data.memory_type not in MEMORY_MAP:
        return {"error": f"Invalid memory_type '{data.memory_type}'. Must be one of {list(MEMORY_MAP.keys())}"}

    memory_label = MEMORY_MAP[data.memory_type]
    node_id = f"{data.memory_type[:2]}_{uuid.uuid4().hex[:8]}"
    timestamp = datetime.utcnow().isoformat()

    create_query = f"""
    MERGE (m:{memory_label} {{id: $node_id}})
    ON CREATE SET m.content = $content,
                  m.timestamp = datetime($timestamp)
    RETURN m
    """

    with neo4j_conn.get_session() as session:
        result = session.run(create_query, node_id=node_id, content=data.content, timestamp=timestamp)
        node = result.single()[0]

        if data.link_to and data.link_to in MEMORY_MAP:
            link_label = MEMORY_MAP[data.link_to]
            relationship_type = determine_relationship(data.memory_type, data.link_to)
            link_query = f"""
            MATCH (src:{memory_label} {{id: $node_id}}),
                  (target:{link_label} {{id: 'ltm_001'}})
            MERGE (src)-[:{relationship_type}]->(target)
            """
            session.run(link_query, node_id=node_id)

    # optionally compute embedding immediately
    if data.embed:
        try:
            embedding_manager.embed_and_store_node(memory_label, node_id, data.content)
        except Exception as e:
            # don't fail creation because embedding failed; return warning
            return {
                "message": f"{memory_label} node created successfully (embedding failed: {str(e)})",
                "node_id": node_id,
                "linked_to": data.link_to
            }

    return {
        "message": f"{memory_label} node created successfully",
        "node_id": node_id,
        "linked_to": data.link_to
    }

# ======================================
# Endpoint to encode & attach embedding to an existing node
# ======================================
class EncodeInput(BaseModel):
    memory_type: str
    node_id: str
    content: Optional[str] = None  # optional: re-encode this content instead of node.content

@app.post("/memory/encode")
def encode_node_embedding(data: EncodeInput):
    if data.memory_type not in MEMORY_MAP:
        return {"error": f"Invalid memory_type '{data.memory_type}'."}
    label = MEMORY_MAP[data.memory_type]

    # If explicit content provided, use it; else fetch node content
    content_to_embed = data.content
    if not content_to_embed:
        q = f"MATCH (n:{label} {{id: $node_id}}) RETURN n.content AS content"
        with neo4j_conn.get_session() as session:
            res = session.run(q, node_id=data.node_id)
            rec = res.single()
            if not rec:
                return {"error": "Node not found"}
            content_to_embed = rec["content"]

    try:
        embedding_manager.embed_and_store_node(label, data.node_id, content_to_embed)
    except Exception as e:
        return {"error": f"Embedding failed: {str(e)}"}

    return {"message": "Embedding stored", "node_id": data.node_id}

# ======================================
# Semantic similarity search endpoint
# ======================================
class SimilarityInput(BaseModel):
    query: str
    memory_type: Optional[str] = None  # limit candidates to a type
    candidate_limit: int = 1000
    top_k: int = 5

@app.post("/memory/similarity")
def memory_similarity_search(data: SimilarityInput):
    # memory_label optional
    memory_label = None
    if data.memory_type:
        if data.memory_type not in MEMORY_MAP:
            return {"error": f"Invalid memory_type '{data.memory_type}'."}
        memory_label = MEMORY_MAP[data.memory_type]

    try:
        results = embedding_manager.find_top_k_similar(data.query, k=data.top_k, memory_label=memory_label, candidate_limit=data.candidate_limit)
    except Exception as e:
        return {"error": f"Similarity search failed: {str(e)}"}

    # normalize response
    out = []
    for r in results:
        entry = {
            "id": r.get("id"),
            "label": r.get("label") if "label" in r else data.memory_type if data.memory_type else None,
            "content": r.get("content"),
            "score": r.get("score")
        }
        out.append(entry)

    return {"query": data.query, "results": out}

# ======================================
# Retrieval endpoints (existing)
# ======================================
@app.get("/memory/all/{memory_type}")
def get_all_memories(memory_type: str):
    if memory_type not in MEMORY_MAP:
        return {"error": f"Invalid memory_type '{memory_type}'. Must be one of {list(MEMORY_MAP.keys())}"}

    query = f"""
    MATCH (m:{MEMORY_MAP[memory_type]})
    RETURN m.id AS id, m.content AS content, m.timestamp AS timestamp
    ORDER BY m.timestamp DESC
    """
    with neo4j_conn.get_session() as session:
        result = session.run(query)
        return [record.data() for record in result]

@app.get("/memory/{memory_type}/{node_id}")
def get_memory_by_id(memory_type: str, node_id: str):
    if memory_type not in MEMORY_MAP:
        return {"error": f"Invalid memory_type '{memory_type}'."}

    query = f"""
    MATCH (m:{MEMORY_MAP[memory_type]} {{id: $node_id}})
    RETURN m.id AS id, m.content AS content, m.timestamp AS timestamp, m.embedding AS embedding
    """
    with neo4j_conn.get_session() as session:
        result = session.run(query, node_id=node_id)
        record = result.single()
        return record.data() if record else {"error": "Memory node not found"}

@app.post("/memory/search")
def search_memories(data: MemorySearchInput):
    if data.memory_type and data.memory_type not in MEMORY_MAP:
        return {"error": f"Invalid memory_type '{data.memory_type}'."}

    if data.memory_type:
        query = f"""
        MATCH (m:{MEMORY_MAP[data.memory_type]})
        WHERE toLower(m.content) CONTAINS toLower($query)
        RETURN m.id AS id, m.content AS content, m.timestamp AS timestamp
        ORDER BY m.timestamp DESC
        LIMIT $limit
        """
    else:
        query = """
        MATCH (m)
        WHERE toLower(m.content) CONTAINS toLower($query)
        RETURN labels(m)[0] AS type, m.id AS id, m.content AS content, m.timestamp AS timestamp
        ORDER BY m.timestamp DESC
        LIMIT $limit
        """

    with neo4j_conn.get_session() as session:
        result = session.run(query, query=data.query, limit=data.limit)
        return [record.data() for record in result]

@app.get("/memory/graph/{node_id}")
def get_memory_graph(node_id: str):
    query = """
    MATCH (start {id: $node_id})-[r*1..3]-(connected)
    RETURN start, r, connected
    """
    with neo4j_conn.get_session() as session:
        result = session.run(query, node_id=node_id)
        graph_data = []
        for record in result:
            graph_data.append({
                "start": record["start"],
                "connected": record["connected"],
                "relationships": [rel.type for rel in record["r"]]
            })
        return graph_data
