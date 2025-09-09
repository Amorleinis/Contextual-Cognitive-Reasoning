// ============================
// Neo4j Memory Graph Initialization
// ============================

// Drop constraints if they exist
DROP CONSTRAINT wm_id_unique IF EXISTS;
DROP CONSTRAINT ltm_id_unique IF EXISTS;
DROP CONSTRAINT em_id_unique IF EXISTS;
DROP CONSTRAINT sm_id_unique IF EXISTS;
DROP CONSTRAINT pm_id_unique IF EXISTS;

// Create constraints for unique IDs
CREATE CONSTRAINT wm_id_unique IF NOT EXISTS
FOR (wm:WorkingMemory)
REQUIRE wm.id IS UNIQUE;

CREATE CONSTRAINT ltm_id_unique IF NOT EXISTS
FOR (ltm:LongTermMemory)
REQUIRE ltm.id IS UNIQUE;

CREATE CONSTRAINT em_id_unique IF NOT EXISTS
FOR (em:EpisodicMemory)
REQUIRE em.id IS UNIQUE;

CREATE CONSTRAINT sm_id_unique IF NOT EXISTS
FOR (sm:SemanticMemory)
REQUIRE sm.id IS UNIQUE;

CREATE CONSTRAINT pm_id_unique IF NOT EXISTS
FOR (pm:ProceduralMemory)
REQUIRE pm.id IS UNIQUE;

// ============================
// Safe node creation using MERGE
// ============================

MERGE (wm:WorkingMemory {id: "wm_001"})
ON CREATE SET wm.description = "Temporary short-term memory buffer";

MERGE (ltm:LongTermMemory {id: "ltm_001"})
ON CREATE SET ltm.description = "Permanent long-term memory store";

MERGE (em:EpisodicMemory {id: "em_001"})
ON CREATE SET em.description = "Memory of specific events";

MERGE (sm:SemanticMemory {id: "sm_001"})
ON CREATE SET sm.description = "General knowledge and facts";

MERGE (pm:ProceduralMemory {id: "pm_001"})
ON CREATE SET pm.description = "Skills and processes";

// ============================
// Relationships
// ============================

MATCH (wm:WorkingMemory {id: "wm_001"}), (ltm:LongTermMemory {id: "ltm_001"})
MERGE (wm)-[:TRANSFERS_TO]->(ltm);

MATCH (ltm:LongTermMemory {id: "ltm_001"}), (em:EpisodicMemory {id: "em_001"})
MERGE (ltm)-[:CONTAINS_EPISODES]->(em);

MATCH (ltm:LongTermMemory {id: "ltm_001"}), (sm:SemanticMemory {id: "sm_001"})
MERGE (ltm)-[:CONTAINS_FACTS]->(sm);

MATCH (ltm:LongTermMemory {id: "ltm_001"}), (pm:ProceduralMemory {id: "pm_001"})
MERGE (ltm)-[:CONTAINS_SKILLS]->(pm);
