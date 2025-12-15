from utils.jira_utils import load_jira_dataframe
from analysis.server_analysis import run_server_analysis
from embeddings.technology_embeddings import init_technology_embeddings


def main():
    # run once (idempotent)
    init_technology_embeddings()

    # load jira data
    df = load_jira_dataframe(num_of_tickets=100)

    # save raw data (optional)
    df.to_csv("jira_issues.csv", index=False, encoding="utf-8")

    # Phase 1
    run_server_analysis(df)

    # Phase 2
    # run_technology_analysis(df)


if __name__ == "__main__":
    main()
