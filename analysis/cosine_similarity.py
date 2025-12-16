import numpy as np
import pandas as pd
from embeddings.utils import blob_to_vec

from db.repository import (
    get_all_jira_issues,
    get_all_technology_embeddings
)

from my_logger.logger import get_logger

logger = get_logger(__name__)

KEYWORDS = {
    "authentication": ["login", "auth", "credential", "password"],
    "networking": ["vpn", "dns", "firewall", "packet"],
    "storage": ["disk", "nfs", "raid", "volume"],
    "api": ["api", "endpoint", "http", "webhook"],
    "database": ["db", "database", "sql", "replication"]
}


def load_embeddings():
    df_tickets = get_all_jira_issues()
    df_tech = get_all_technology_embeddings()

    logger.info("Tickets:")
    logger.info(df_tickets.head())

    logger.info("\nTechnologies:")
    logger.info(df_tech.head())

    df_tickets = df_tickets[df_tickets["embedding"].notna()]
    df_tech = df_tech[df_tech["embedding"].notna()]

    logger.info("Tickets with embeddings: %d", len(df_tickets))
    logger.info("Technologies with embeddings: %d", len(df_tech))

    df_tickets["embedding_vec"] = df_tickets["embedding"].apply(blob_to_vec)
    df_tech["embedding_vec"] = df_tech["embedding"].apply(blob_to_vec)

    logger.info(len(df_tickets["embedding_vec"].iloc[0]))
    logger.info(len(df_tech["embedding_vec"].iloc[0]))

    return df_tickets, df_tech


def compute_best_technology_match(df_tickets, df_tech) -> pd.DataFrame:
    ticket_vecs = np.vstack(df_tickets["embedding_vec"].values)
    tech_vecs = np.vstack(df_tech["embedding_vec"].values)

    ticket_ids = df_tickets["id"].tolist()
    tech_names = df_tech["name"].tolist()

    similarity_matrix = ticket_vecs @ tech_vecs.T

    final_scores = []

    for i, ticket_id in enumerate(ticket_ids):
        text = df_tickets.iloc[i]["description"]
        scores = []

        for j, tech in enumerate(tech_names):
            score = similarity_matrix[i, j]
            score += keyword_bonus(text, tech)
            scores.append(score)

        final_scores.append(scores)

    final_scores = np.array(final_scores)

    best_tech_idx = np.argmax(final_scores, axis=1)
    best_scores = final_scores[np.arange(len(ticket_ids)), best_tech_idx]

    df_match = pd.DataFrame({
        "ticket_id": ticket_ids,
        "technology": [tech_names[i] for i in best_tech_idx],
        "similarity": best_scores
    })

    return df_match


def run_cosine_similarity():
    df_tickets, df_tech = load_embeddings()
    df_match = compute_best_technology_match(df_tickets, df_tech)

    logger.info(df_match.head())
    return df_match


def keyword_bonus(text: str, technology: str) -> float:
    if not text:
        return 0.0

    text = text.lower()
    keywords = KEYWORDS.get(technology, [])

    hits = sum(1 for k in keywords if k in text)
    return 0.05 * hits
