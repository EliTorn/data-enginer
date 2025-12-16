from utils.jira_utils import init_jira_or_fail, get_all_tickets_with_retry
from utils.ticket_generator import create_tickets_bulk_async, delete_send_box

from analysis.server_analysis import run_server_analysis, run_technology_analysis
from analysis.cosine_similarity import run_cosine_similarity

from db.schema import create_jira_issues_table, create_ticket_technology_match_table
from db.repository import save_jira_issues, get_all_jira_issues, save_ticket_technology_matches, \
    get_all_ticket_technology_matches, drop_jira_issues_table

from embeddings.technology_embeddings import init_technology_embeddings
from embeddings.ticket_embeddings import init_ticket_embeddings

from my_logger.logger import get_logger

import asyncio

COUNT_TICKET = 5000  # max ticket in free plan Jira
PAGE_SIZE = 10
MAX_RETRY = 3
SLEEP_SEC = 2
SIMILARITY_THRESHOLD = 0.1
logger = get_logger(__name__)


async def create_or_delete_send_box(jira, project_key):
    # create/delete send box
    logger.info("Creating Jira tickets in bulk")
    await create_tickets_bulk_async(jira, project_key, COUNT_TICKET)
    logger.info("Finished creating Jira tickets")
    logger.info("Deleting Jira tickets")
    await delete_send_box(jira, project_key, COUNT_TICKET)
    logger.info("Finished deleting Jira tickets")


async def run_embeddings_and_technology_analysis():
    # Generate embeddings for technologies and Jira tickets
    logger.info("Starting embeddings generation process")

    logger.info("Generating technology embeddings")
    init_technology_embeddings()

    logger.info("Generating Jira ticket embeddings")
    init_ticket_embeddings()

    logger.info("Embeddings generation process completed")

    # Compute cosine similarity
    logger.info("Running cosine similarity")
    df_match = run_cosine_similarity()

    logger.info("Saving similarity matches to database")
    drop_jira_issues_table("technology_embeddings")
    save_ticket_technology_matches(df_match)

    ticket_technology_matches_df = get_all_ticket_technology_matches()

    logger.info("Technologies with embeddings: %d", len(ticket_technology_matches_df))

    logger.info(
        "Sample matches:\n%s",
        ticket_technology_matches_df[
            ["ticket_id", "technology_name", "similarity"]
        ].head(5).to_string(index=False)
    )

    logger.info("Applying similarity threshold: %.2f", SIMILARITY_THRESHOLD)

    filtered_matches = ticket_technology_matches_df[
        ticket_technology_matches_df["similarity"] >= SIMILARITY_THRESHOLD
        ]

    run_technology_analysis(filtered_matches)


def run_server_analysis_topic(df_jira_tickets):
    logger.info("Running server occurrence analysis")
    run_server_analysis(df_jira_tickets)
    logger.info("Server occurrence analysis finished")


def load_and_preview_jira_tickets():
    logger.info("Loading Jira tickets from database")
    df_jira_tickets = get_all_jira_issues()

    logger.info(f"Get Jira - issues DB {len(df_jira_tickets)} tickets successfully")

    logger.info("Previewing Jira tickets data")
    logger.info(
        df_jira_tickets[["id", "key", "summary"]].head(5)
    )

    return df_jira_tickets


def setup_and_save_jira_issues(df_all_tickets):
    logger.info("Ensuring database tables exist")
    create_jira_issues_table()
    create_ticket_technology_match_table()

    logger.info(
        "Saving Jira issues snapshot to database (rows=%d)",
        len(df_all_tickets)
    )
    save_jira_issues(df_all_tickets)


async def fetch_jira_tickets(jira, project_key):
    logger.info(f"Fetching Jira {COUNT_TICKET} tickets from API, With Page number {PAGE_SIZE}")

    df_all_tickets, error, next_token = await get_all_tickets_with_retry(
        jira=jira,
        project_key=project_key,
        batch_size=COUNT_TICKET,
        page_size=PAGE_SIZE,
        max_retry=MAX_RETRY,
        sleep_sec=SLEEP_SEC
    )

    if error:
        logger.error(
            "Finished fetching Jira tickets with error after retries: %s. "
            "Retry can continue from next_token=%s",
            error,
            next_token
        )
    else:
        logger.info(
            "Jira tickets fetched successfully (rows=%d). "
            "Next page token available: %s",
            len(df_all_tickets),
            next_token
        )

    return df_all_tickets


async def main():
    logger.info("Starting Jira data pipeline")

    logger.info("Initializing Jira client")
    jira, project_key = init_jira_or_fail()

    # await create_or_delete_send_box(jira, project_key)

    df_all_tickets = await fetch_jira_tickets(jira, project_key)

    setup_and_save_jira_issues(df_all_tickets)

    df_jira_tickets = load_and_preview_jira_tickets()

    run_server_analysis_topic(df_jira_tickets)

    await run_embeddings_and_technology_analysis()

    logger.info("Jira data pipeline finished successfully")


if __name__ == "__main__":
    asyncio.run(main())
