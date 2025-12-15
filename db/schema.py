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


def create_jira_issues_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jira_issues (
        id INTEGER PRIMARY KEY,
        key TEXT NOT NULL,
        summary TEXT,
        description TEXT,
        status TEXT,
        embedding BLOB DEFAULT NULL
    )
    """)

    conn.commit()
    conn.close()


def create_ticket_technology_match_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ticket_technology_match (
        ticket_id INTEGER PRIMARY KEY,
        technology_name TEXT NOT NULL,
        similarity REAL NOT NULL
    )
    """)

    conn.commit()
    conn.close()
