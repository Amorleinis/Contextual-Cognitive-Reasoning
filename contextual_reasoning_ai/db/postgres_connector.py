import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_postgres_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "contextual_reasoner"),
        user=os.getenv("POSTGRES_USER", "admin"),
        password=os.getenv("POSTGRES_PASSWORD", "admin"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        cursor_factory=RealDictCursor
    )
