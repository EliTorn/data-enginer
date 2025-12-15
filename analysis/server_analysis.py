from utils.plot_utils import count_servers
from utils.plot_utils import plot_counts_bar


def run_server_analysis(df):
    server_counts = count_servers(df)
    plot_counts_bar(server_counts)
    return server_counts
