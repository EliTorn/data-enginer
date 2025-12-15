from jira import JIRA
from utils.config_utils import load_config
import pandas as pd
import asyncio


# def get_num_tickets_v2(jira, project_key: str, num_of_tickets: int) -> pd.DataFrame:
#     issues = jira.search_issues(f'project={project_key}', maxResults=num_of_tickets)
#
#     data = []
#     for issue in issues:
#         data.append({
#             "id": issue.id,
#             "key": issue.key,
#             "summary": issue.fields.summary,
#             "description": issue.fields.description,
#             "status": issue.fields.status.name
#         })
#
#     return pd.DataFrame(data)
#

def get_jira_client():
    """
    Create Jira client and return (jira, project_key)
    """
    config = load_config()

    jira = JIRA(
        server=config["API_SERVER"],
        basic_auth=(config["EMAIL"], config["API_TOKEN"])
    )
    project_key = jira.projects()[0].key
    return jira, project_key


# todo do here login and retry !!!
async def get_num_tickets(
        jira,
        project_key: str,
        num_of_tickets: int,
        page_size: int = 100
) -> pd.DataFrame:
    base = jira._options["server"].rstrip("/")
    url = f"{base}/rest/api/3/search/jql"
    next_token = None
    rows = []
    while len(rows) < num_of_tickets:
        params = {
            "jql": f'project={project_key} ORDER BY created DESC',
            "maxResults": min(page_size, num_of_tickets - len(rows)),
            "fields": "summary,description,status",
        }
        if next_token:
            params["nextPageToken"] = next_token
        resp = await asyncio.to_thread(jira._session.get, url, params=params)
        resp.raise_for_status()
        payload = resp.json()
        issues = payload.get("issues", [])
        for issue in issues:
            fields = issue.get("fields", {})
            rows.append({
                "id": issue.get("id"),
                "key": issue.get("key"),
                "summary": fields.get("summary"),
                "description": fields.get("description"),
                "status": (fields.get("status") or {}).get("name"),
            })
        next_token = payload.get("nextPageToken")
        if not next_token or not issues:
            break
    return pd.DataFrame(rows)
