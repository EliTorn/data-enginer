from db.connection import get_connection

def create_technology_embeddings_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS technology_embeddings (
        name TEXT PRIMARY KEY,
        embedding BLOB
    )
    """)

    conn.commit()
    conn.close()
