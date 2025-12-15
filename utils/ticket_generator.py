import random
from templates.technologies import TECHNOLOGY_TEMPLATES
from utils.config_utils import SERVERS, DB_NAMES
import asyncio
import time

BULK_LIMIT = 50


def random_case(s):
    if not s: return s
    return ''.join(c.upper() if random.random() > 0.5 else c.lower() for c in s)


def generate_description(template, servers, db_names):
    server = random.choice(servers)
    if server is not None:
        server = random_case(server)
    db_name = random.choice(db_names) if "{db_name}" in template else ""
    return template.format(
        server=server,
        db_name=db_name
    )


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


async def create_tickets_in_batches(
        jira,
        project_key: str,
        total_tickets: int,
        batch_size: int = 100,
        sleep_seconds: int = 1
):
    created = 0
    while created < total_tickets:
        remaining = total_tickets - created
        current_batch = min(batch_size, remaining)

        print(f"Creating batch of {current_batch} tickets "
              f"(progress: {created}/{total_tickets})")

        await create_send_box(
            jira=jira,
            project_key=project_key,
            count_tickets=current_batch
        )

        created += current_batch

        if created < total_tickets:
            await asyncio.sleep(sleep_seconds)

    print(f"Finished creating {total_tickets} tickets")


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


def text_to_adf(text: str) -> dict:
    return {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    }
                ]
            }
        ]
    }


def build_issues(
        project_key: str,
        total_tickets: int
) -> list[dict]:
    technologies = list(TECHNOLOGY_TEMPLATES.keys())

    issues = [
        {
            "fields": {
                "project": {"key": project_key},
                "summary": f"Ticket {i + 1}",
                "description": text_to_adf(
                    generate_description(
                        random.choice(
                            TECHNOLOGY_TEMPLATES[random.choice(technologies)]
                        ),
                        servers=SERVERS,
                        db_names=DB_NAMES
                    )
                ),
                "issuetype": {"name": "Task"}
            }
        }
        for i in range(total_tickets)
    ]

    return issues


def send_bulk_batch(
        jira,
        bulk_url: str,
        batch: list[dict]
):
    return jira._session.post(
        bulk_url,
        json={"issueUpdates": batch}
    )


def handle_bulk_response(response):
    if response.status_code == 429:
        retry = int(response.headers.get("Retry-After", 60))
        print(f"⏳ Rate limited. Sleeping {retry}s")
        time.sleep(retry)
        return False

    response.raise_for_status()
    return True


async def create_tickets_bulk_async(
        jira,
        project_key: str,
        total_tickets: int,
        sleep_seconds: float = 1.0
):
    base_url = "https://play-ground-v1.atlassian.net"
    bulk_url = f"{base_url}/rest/api/3/issue/bulk"

    issues = build_issues(project_key, total_tickets)

    for batch_num, i in enumerate(
            range(0, total_tickets, BULK_LIMIT), start=1
    ):
        batch = issues[i:i + BULK_LIMIT]

        print(
            f"Batch {batch_num}: creating {len(batch)} issues "
            f"(progress {i}/{total_tickets})"
        )

        # 🔑 run blocking HTTP call in thread
        response = await asyncio.to_thread(
            send_bulk_batch,
            jira,
            bulk_url,
            batch
        )

        if not handle_bulk_response(response):
            continue

        await asyncio.sleep(sleep_seconds)

    print(f"Finished creating {total_tickets} tickets")
