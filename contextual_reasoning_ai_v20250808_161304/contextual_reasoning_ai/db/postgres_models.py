from db.postgres_connector import get_postgres_connection

def initialize_postgres_tables():
    conn = get_postgres_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS threat_logs (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMPTZ DEFAULT now(),
        source TEXT,
        threat_type TEXT,
        severity TEXT,
        details JSONB
    );
    """)

    conn.commit()
    cur.close()
    conn.close()
