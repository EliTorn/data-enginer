import json


def load_config():
    with open("config.json", "r") as f:
        return json.load(f)


SERVERS = ["srv-prod-01", "SRV-db-02", "Srv-App-03", "srv-cache-04", None]
DB_NAMES = ["Postgres", "MySQL", "Oracle", "MongoDB", "SQLServer"]
