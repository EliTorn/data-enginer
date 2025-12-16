import matplotlib.pyplot as plt
from my_logger.logger import get_logger

logger = get_logger(__name__)


def count_servers(df, description_col="description"):
    df = df.copy()
    df["servers"] = df[description_col].str.lower().str.findall(r"(srv-[a-z0-9-]+)")
    df["servers"] = df["servers"].apply(lambda x: x if x else ["unknown"])
    return df.explode("servers")["servers"].value_counts()


def plot_server_counts_bar(
    counts,
    title="Server Occurrences",
    output_path="server_occurrences.png"
):
    counts.plot(kind="bar", figsize=(8, 4))
    plt.xlabel("Server")
    plt.ylabel("Count")
    plt.title(title)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(output_path)
    logger.info(
        "Server occurrences bar chart generated and saved to '%s'",
        output_path
    )
    plt.close()


def count_tickets_by_technology(df, technology_col="technology_name"):
    """
    Counts how many tickets are associated with each technology.
    """
    return df[technology_col].value_counts()


def plot_technology_counts_bar(
    counts,
    title="Tickets per Technology",
    output_path="technology_ticket_counts.png"
):
    counts.plot(kind="bar", figsize=(8, 4))
    plt.xlabel("Technology")
    plt.ylabel("Ticket Count")
    plt.title(title)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(output_path)

    logger.info(
        "Technology ticket counts bar chart generated and saved to '%s'",
        output_path
    )

    plt.close()
