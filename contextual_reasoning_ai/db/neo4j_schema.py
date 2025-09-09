from db.neo4j_connector import get_neo4j_driver

def initialize_neo4j_schema():
    driver = get_neo4j_driver()
    with driver.session() as session:
        session.run("""
        CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE;
        CREATE CONSTRAINT IF NOT EXISTS FOR (d:Device) REQUIRE d.id IS UNIQUE;
        CREATE CONSTRAINT IF NOT EXISTS FOR (n:Network) REQUIRE n.id IS UNIQUE;
        CREATE CONSTRAINT IF NOT EXISTS FOR (t:Threat) REQUIRE t.id IS UNIQUE;
        CREATE CONSTRAINT IF NOT EXISTS FOR (v:Vulnerability) REQUIRE v.id IS UNIQUE;
        """)
    driver.close()
