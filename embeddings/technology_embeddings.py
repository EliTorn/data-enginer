from sentence_transformers import SentenceTransformer
from templates.technologies import TECHNOLOGIES_DESCRIPTIONS
from db.schema import create_technology_embeddings_table
from db.repository import (
    save_technology_embedding,
    technology_embeddings_exist,
    drop_jira_issues_table
)
from my_logger.logger import get_logger

logger = get_logger(__name__)


def init_technology_embeddings():
    """
    Create and store technology embeddings once.
    Safe to run multiple times (idempotent).
    """

    create_technology_embeddings_table()

    if technology_embeddings_exist():
        logger.info("Technology embeddings already exist. Skipping creation.")
        return

    logger.info("Creating technology embeddings...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    tech_names = list(TECHNOLOGIES_DESCRIPTIONS.keys())
    tech_texts = list(TECHNOLOGIES_DESCRIPTIONS.values())

    tech_embeddings = model.encode(
        tech_texts,
        normalize_embeddings=True
    )
    drop_jira_issues_table(name_table="technology_embeddings")
    for name, emb in zip(tech_names, tech_embeddings):
        save_technology_embedding(name, emb)

    logger.info("Technology embeddings saved to database")
