from utils.plot_utils import count_servers, count_tickets_by_technology, plot_server_counts_bar, \
    plot_technology_counts_bar

import pandas as pd


def run_server_analysis(df: pd.DataFrame) -> None:
    """
    Performs server-level analysis on Jira ticket data.

    The function extracts server identifiers from ticket descriptions
    and generates a bar chart showing their distribution.
    """
    server_counts = count_servers(df)
    plot_server_counts_bar(server_counts)


def run_technology_analysis(df: pd.DataFrame) -> None:
    """
    Performs technology-level analysis on ticket-technology match data.

    The function counts how many tickets are associated with each technology
    and generates a bar chart showing their distribution.
    """
    technology_counts = count_tickets_by_technology(df)
    plot_technology_counts_bar(technology_counts)
