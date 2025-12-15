import random
from templates.technologies import TECHNOLOGY_TEMPLATES
from utils.config_utils import SERVERS, DB_NAMES
import asyncio
import time


def random_case(s):
    if not s: return s
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


async def create_send_box(jira, project_key: str, count_tickets: int):
    start_time = time.perf_counter()
    technologies = list(TECHNOLOGY_TEMPLATES.keys())
    tasks = []
    for i in range(count_tickets):
        tech = random.choice(technologies)
        template = random.choice(TECHNOLOGY_TEMPLATES[tech])
        description = generate_description(template, servers=SERVERS, db_names=DB_NAMES)

        issue_dict = {
            "project": {"key": project_key},
            "summary": f"Ticket {i + 1}",
            "description": description,
            "issuetype": {"name": "Task"}
        }

        task = asyncio.to_thread(
            jira.create_issue,
            fields=issue_dict
        )
        tasks.append(task)

    await asyncio.gather(*tasks)
    end_time = time.perf_counter()
    duration = end_time - start_time

    print(f"Created {count_tickets} tickets in {duration:.2f} seconds")


async def delete_send_box_3(jira, project_key: str, count_tickets: int):
    start_time = time.perf_counter()
    issues = jira.search_issues(
        f'project={project_key}',
        maxResults=count_tickets
    )
    tasks = []
    for issue in issues:
        task = asyncio.to_thread(
            jira.delete(),
            issue.key
        )
        tasks.append(task)
    await asyncio.gather(*tasks)
    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"Deleted {len(issues)} tickets in {duration:.2f} seconds")


async def delete_send_box(jira, project_key: str, count_tickets: int):
    start_time = time.perf_counter()

    issues = jira.search_issues(
        f'project={project_key}',
        maxResults=count_tickets
    )

    tasks = []
    for issue in issues:
        task = asyncio.to_thread(
            issue.delete
        )
        tasks.append(task)

    await asyncio.gather(*tasks)

    end_time = time.perf_counter()
    duration = end_time - start_time

    print(f"Deleted {len(issues)} tickets in {duration:.2f} seconds")