from utils.jira_utils import get_jira_client, get_all_tickets_with_retry
from utils.ticket_generator import create_tickets_bulk_async, delete_send_box

from analysis.server_analysis import run_server_analysis
from analysis.cosine_similarity import run_cosine_similarity

from db.schema import create_jira_issues_table, create_ticket_technology_match_table
from db.repository import save_jira_issues, get_all_jira_issues, get_all_technology_embeddings, \
    save_ticket_technology_matches, get_all_ticket_technology_matches

from embeddings.technology_embeddings import init_technology_embeddings
from embeddings.ticket_embeddings import init_ticket_embeddings

from my_logger.logger import get_logger

import numpy as np
import asyncio
import time
import pandas as pd

COUNT_TICKET = 5000  # max ticket in free plan Jira
NUM_OF_TICKETS = 10000
PAGE_SIZE = 10
MAX_RETRY = 3
SLEEP_SEC = 2

logger = get_logger(__name__)


async def main():
    logger.info('Start Data Engineer Code !')
    # Add evinvoument
    jira, project_key = get_jira_client()

    # create/delete  send box
    # await create_tickets_bulk_async(jira,project_key,COUNT_CREATE_TICKET)
    # delete_send_box()

    #
    # get All Data
    df, error, next_token = await get_all_tickets_with_retry(
        jira=jira,
        project_key=project_key,
        batch_size=NUM_OF_TICKETS,
        page_size=PAGE_SIZE,
        max_retry=MAX_RETRY,
        sleep_sec=SLEEP_SEC
    )
    if error:
        print("Finished with error:", error)
    df.head(10).to_csv(
        "jira_issues_sample.csv",
        index=False,
        encoding="utf-8"
    )

    # connect Db , craete and Save in Db
    create_jira_issues_table()
    create_ticket_technology_match_table()

    save_jira_issues(df)
    df_jira_tickets = get_all_jira_issues()
    print(df_jira_tickets.head(5))
    #
    # df = run_server_analysis(df)

    # create embddings
    # init_technology_embeddings()
    # init_ticket_embeddings()

    # # df = get_all_technology_embeddings()
    # df["embedding"] = df["embedding"].apply(
    #     lambda x: None if x is None else np.frombuffer(x, dtype=np.float32).tolist()
    # )
    #
    # df.head(10).to_csv(
    #     "jira_issues_sample.csv",
    #     index=False,
    #     encoding="utf-8"
    # )

    # Mush Conine Similarity
    # df_match = run_cosine_similarity()
    # save_ticket_technology_matches(df_match)
    # print(df_match)
    # df = get_all_ticket_technology_matches()
    # df.to_csv(
    #     "ticket_technology_match.csv",
    #     index=False,
    #     encoding="utf-8"
    # )


# create embddings
# init_technology_embeddings()
# init_ticket_embeddings()

# # get all db data
# get_all_technology_embeddings()
# get_all_jira_issues


if __name__ == "__main__":
    asyncio.run(main())
