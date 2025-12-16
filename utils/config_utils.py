import json

import json
import os

REQUIRED_KEYS = {"API_SERVER", "EMAIL", "API_TOKEN"}


def load_config(path: str = "config.json") -> dict:
    """
    Loads and validates Jira configuration from config.json.

    Required keys:
      - API_SERVER
      - EMAIL
      - API_TOKEN

    Example config.json:
    {
      "API_TOKEN": "your_api_token",
      "EMAIL": "your_email@gmail.com",
      "API_SERVER": "https://your-domain.atlassian.net"
    }
    """
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Config file '{path}' not found.\n"
            "Please create a config.json file in the project root."
        )

    try:
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(
            "Invalid JSON format in config.json.\n"
            "The file must contain exactly one valid JSON object.\n\n"
            "Example:\n"
            "{\n"
            '  "API_TOKEN": "your_api_token",\n'
            '  "EMAIL": "your_email@gmail.com",\n'
            '  "API_SERVER": "https://your-domain.atlassian.net"\n'
            "}"
        ) from e

    missing = REQUIRED_KEYS - config.keys()
    if missing:
        raise KeyError(
            "Missing required configuration keys in config.json:\n"
            f"  {', '.join(sorted(missing))}\n\n"
            "Expected format:\n"
            "{\n"
            '  "API_TOKEN": "your_api_token",\n'
            '  "EMAIL": "your_email@gmail.com",\n'
            '  "API_SERVER": "https://your-domain.atlassian.net"\n'
            "}"
        )

    return config


SERVERS = ["srv-prod-01", "SRV-db-02", "Srv-App-03", "srv-cache-04", None]
DB_NAMES = ["Postgres", "MySQL", "Oracle", "MongoDB", "SQLServer"]


def get_url(jira) -> str:
    base = jira._options["server"].rstrip("/")
    return f"{base}/rest/api/3/search/jql"
