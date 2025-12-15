import random
from templates.technologies import TECHNOLOGY_TEMPLATES


def random_case(s):
    if not s:
        return s
    return ''.join(c.upper() if random.random() > 0.5 else c.lower() for c in s)


def generate_description(template, servers, db_names):
    s1 = random.choice(servers)
    s2 = random.choice(servers) if "{server2}" in template else None
    if random.random() < 0.2:
        s1 = None
    if s2 and random.random() < 0.2:
        s2 = None
    s1 = random_case(s1) if s1 else "unknown"
    s2 = random_case(s2) if s2 else None
    db_name = random.choice(db_names) if "{db_name}" in template else ""
    return template.format(server=s1, server2=s2, db_name=db_name)


def create_send_box(jira, project_key: str, count_tickets: int):
    servers = ["srv-prod-01", "SRV-db-02", "Srv-App-03", "srv-cache-04", None]
    db_names = ["Postgres", "MySQL", "Oracle", "MongoDB", "SQLServer"]
    technologies = list(TECHNOLOGY_TEMPLATES.keys())
    for i in range(count_tickets):
        tech = random.choice(technologies)
        template = random.choice(TECHNOLOGY_TEMPLATES[tech])
        description = generate_description(template, servers, db_names)

        issue_dict = {
            "project": {"key": project_key},
            "summary": f"Ticket {i + 1}",
            "description": description,
            "issuetype": {"name": "Task"}
        }

        issue = jira.create_issue(fields=issue_dict)
        print(f"Created Issue: {issue.key}")
