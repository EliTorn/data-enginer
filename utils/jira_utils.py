from jira import JIRA
from utils.config_utils import load_config
import pandas as pd


def get_num_tickets(jira, project_key: str, num_of_tickets: int) -> pd.DataFrame:
    issues = jira.search_issues(f'project={project_key}', maxResults=num_of_tickets)

    data = []
    for issue in issues:
        data.append({
            "id": issue.id,
            "key": issue.key,
            "summary": issue.fields.summary,
            "description": issue.fields.description,
            "status": issue.fields.status.name
        })

    return pd.DataFrame(data)


def load_jira_dataframe(num_of_tickets: int):
    config = load_config()

    jira = JIRA(
        server=config["API_SERVER"],
        basic_auth=(config["EMAIL"], config["API_TOKEN"])
    )

    project_key = jira.projects()[0].key
    return get_num_tickets(jira, project_key, num_of_tickets)
