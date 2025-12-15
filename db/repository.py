import numpy as np
from db.connection import get_connection


def technology_embeddings_exist() -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM technology_embeddings
    """)

    count = cursor.fetchone()[0]
    conn.close()

    return count > 0


def save_technology_embedding(name, embedding):
    conn = get_connection()
    cursor = conn.cursor()

    embedding_bytes = embedding.astype(np.float32).tobytes()

    cursor.execute(
        """
        INSERT OR REPLACE INTO technology_embeddings
        (name, embedding)
        VALUES (?, ?)
        """,
        (name, embedding_bytes)
    )

    conn.commit()
    conn.close()
