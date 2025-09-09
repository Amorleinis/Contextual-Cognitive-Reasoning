    def initialize_constraints(self):
        """
        Verify and create Neo4j constraints if they don't already exist.
        """
        print("[Neo4j] Initializing memory constraints...")
        constraints = {
            "WorkingMemory": "wm_id_unique",
            "LongTermMemory": "ltm_id_unique",
            "SemanticMemory": "sem_id_unique",
            "EpisodicMemory": "epi_id_unique"
        }

        with self.driver.session() as session:
            for label, constraint_name in constraints.items():
                query = f"""
                CREATE CONSTRAINT {constraint_name} IF NOT EXISTS
                FOR (n:{label})
                REQUIRE n.id IS UNIQUE
                """
                session.run(query)
        print("[Neo4j] Memory constraints ready.")
