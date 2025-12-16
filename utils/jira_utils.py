from jira import JIRA
from utils.config_utils import load_config, get_url
import pandas as pd
import asyncio


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


def init_jira_or_fail():
    """
    Initializes Jira client using config.json.

    Returns:
        (jira, project_key)

    Raises:
        RuntimeError: if config.json is missing or invalid.
    """
    try:
        return get_jira_client()

    except Exception:
        raise RuntimeError(
            "config.json is invalid or missing required fields.\n\n"
            "The file must look exactly like this:\n"
            "{\n"
            '  "API_TOKEN": "YOUR_JIRA_API_TOKEN",\n'
            '  "EMAIL": "your_email@gmail.com",\n'
            '  "API_SERVER": "https://your-domain.atlassian.net"\n'
            "}\n"
        )


def map_issue(issue: dict) -> dict:
    fields = issue.get("fields", {})
    return {
        "id": issue.get("id"),
        "key": issue.get("key"),
        "summary": fields.get("summary"),
        "description": fields.get("description"),
        "status": (fields.get("status") or {}).get("name"),
    }


async def fetch_jira_pages(
        jira,
        url: str,
        project_key: str,
        num_of_tickets: int,
        page_size: int,
        token: str | None = None
) -> tuple[list[dict], str | None]:
    rows = []
    while len(rows) < num_of_tickets:
        params = {
            "jql": f'project={project_key} ORDER BY created DESC',
            "maxResults": min(page_size, num_of_tickets - len(rows)),
            "fields": "summary,description,status",
            **({"nextPageToken": token} if token else {})
        }
        resp = await asyncio.to_thread(jira._session.get, url, params=params)
        resp.raise_for_status()
        payload = resp.json()
        issues = payload.get("issues", [])
        if not issues: break
        rows.extend(map_issue(i) for i in issues)
        token = payload.get("nextPageToken")
        if not token: break
    return rows, token


async def get_num_tickets(
        jira,
        project_key: str,
        num_of_tickets: int,
        page_size: int = 10,
        start_token: str | None = None
) -> tuple[pd.DataFrame, str | None, str | None]:
    url = get_url(jira=jira)
    try:
        rows, next_token = await fetch_jira_pages(
            jira=jira,
            url=url,
            project_key=project_key,
            num_of_tickets=num_of_tickets,
            page_size=page_size,
            token=start_token
        )
        return pd.DataFrame(rows), None, next_token
    except Exception as e:
        return pd.DataFrame(), str(e), start_token


async def get_all_tickets_with_retry(
        jira,
        project_key: str,
        batch_size: int,
        page_size: int,
        max_retry: int = 3,
        sleep_sec: int = 2
):
    all_rows = []
    new_token = None
    error = None
    for i in range(max_retry + 1):
        df, error, new_token = await get_num_tickets(
            jira,
            project_key=project_key,
            num_of_tickets=batch_size,
            page_size=page_size,
            start_token=new_token
        )
        if not error:
            if all_rows:
                all_rows.append(df)
                final_df = pd.concat(all_rows, ignore_index=True)
                return final_df, None, new_token
            return df, None, new_token
        print(f"Error (retry {i + 1}/{max_retry}): {error}")
        await asyncio.sleep(sleep_sec)
        all_rows.append(df)
    final_df = pd.concat(all_rows, ignore_index=True) if all_rows else pd.DataFrame()
    return final_df, error, new_token
