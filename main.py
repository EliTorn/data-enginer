from utils.jira_utils import get_jira_client, load_jira_dataframe
from utils.ticket_generator import create_send_box, delete_send_box
from analysis.server_analysis import run_server_analysis
from embeddings.technology_embeddings import init_technology_embeddings

import asyncio

COUNT_CREATE_TICKET = 100
COUNT_DELETE_TICKET = 10


async def main():
    print('Hello')
    jira, project_key = get_jira_client()
    await create_send_box(jira, project_key, COUNT_CREATE_TICKET)
    # await delete_send_box(jira, project_key, COUNT_TICKET)



if __name__ == "__main__":
    asyncio.run(main())

    # # run once (idempotent)
    # init_technology_embeddings()
    #
    # # load jira data
    # df = load_jira_dataframe(num_of_tickets=100)
    #
    # # save raw data (optional)
    # df.to_csv("jira_issues.csv", index=False, encoding="utf-8")
    #
    # # Phase 1
    # run_server_analysis(df)
    #
    # # Phase 2
    # # run_technology_analysis(df)
