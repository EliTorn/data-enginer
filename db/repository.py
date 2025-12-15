from db.connection import get_connection
import pandas as pd
import re
import numpy as np


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


def extract_text_simple(desc: str) -> str:
    if not desc:
        return ""
    match = re.search(r"'text':\s*'([^']+)'", desc)
    return match.group(1) if match else desc


def save_jira_issues(df):
    conn = get_connection()
    cursor = conn.cursor()
    rows = [
        (
            int(row["id"]),
            row["key"],
            row["summary"],
            extract_text_simple(str(row["description"])),
            str(row["status"])
        )
        for _, row in df.iterrows()
    ]
    cursor.executemany(
        """
        INSERT OR REPLACE INTO jira_issues
        (id, key, summary, description, status)
        VALUES (?, ?, ?, ?, ?)
        """,
        rows
    )

    conn.commit()
    conn.close()


def get_all_jira_issues() -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql(
        "SELECT id, key, summary, description, status, embedding FROM jira_issues",
        conn
    )
    conn.close()
    return df


def get_all_technology_embeddings() -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql(
        "SELECT * FROM technology_embeddings",
        conn
    )
    conn.close()
    return df


def save_ticket_embedding(ticket_id: int, embedding):
    conn = get_connection()
    cursor = conn.cursor()

    embedding_bytes = embedding.astype(np.float32).tobytes()

    cursor.execute(
        """
        UPDATE jira_issues
        SET embedding = ?
        WHERE id = ?
        """,
        (embedding_bytes, ticket_id)
    )

    conn.commit()
    conn.close()


def get_jira_issues_without_embedding(limit: int = 50) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql(
        """
        SELECT id, description
        FROM jira_issues
        WHERE embedding IS NULL
        ORDER BY id
        LIMIT ?
        """,
        conn,
        params=(limit,)
    )
    conn.close()
    return df


def save_ticket_technology_matches(df_match: pd.DataFrame):
    conn = get_connection()
    cursor = conn.cursor()

    rows = [
        (
            int(row["ticket_id"]),
            row["technology"],
            float(row["similarity"])
        )
        for _, row in df_match.iterrows()
    ]

    cursor.executemany(
        """
        INSERT OR REPLACE INTO ticket_technology_match
        (ticket_id, technology_name, similarity)
        VALUES (?, ?, ?)
        """,
        rows
    )

    conn.commit()
    conn.close()


def get_all_ticket_technology_matches() -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql(
        """
        SELECT ticket_id, technology_name, similarity
        FROM ticket_technology_match
        """,
        conn
    )
    conn.close()
    return df
