from utils.jira_utils import get_jira_client, get_num_tickets
from utils.ticket_generator import create_tickets_bulk_async, delete_send_box


from analysis.server_analysis import run_server_analysis
from analysis.cosine_similarity import run_cosine_similarity

from db.schema import create_jira_issues_table, create_ticket_technology_match_table
from db.repository import save_jira_issues, get_all_jira_issues, get_all_technology_embeddings, \
    save_ticket_technology_matches, get_all_ticket_technology_matches

from embeddings.technology_embeddings import init_technology_embeddings
from embeddings.ticket_embeddings import init_ticket_embeddings

import numpy as np
import asyncio

COUNT_CREATE_TICKET = 20000
COUNT_DELETE_TICKET = 10
NUM_OF_TICKETS = 10000


async def main():
    print('Start Data Engineer Code !')
    # Add evinvoument
    jira, project_key = get_jira_client()

    # create send box
    # await create_tickets_bulk_async(jira,project_key,COUNT_CREATE_TICKET)
    # # await delete_send_box(jira=jira, project_key=project_key, count_tickets=COUNT_DELETE_TICKET)
    #
    # # get All Data
    # df = await get_num_tickets(jira=jira,
    #                            project_key=project_key,
    #                            num_of_tickets=NUM_OF_TICKETS)
    # print(len(df))
    # print(df.count())
    # server_counts = count_servers(df)
    # print(server_counts)
    # print(df.head(5))

    # connect Db , craete and Save in Db
    # create_jira_issues_table()
    # create_ticket_technology_match_table
    # save_jira_issues(df)
    df = get_all_jira_issues()

    df = run_server_analysis(df)

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

    # create_ticket_technology_match_table()

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
