import matplotlib.pyplot as plt


def count_servers(df, description_col="description"):
    df = df.copy()
    df["servers"] = df[description_col].str.lower().str.findall(r"(srv-[a-z0-9-]+)")
    df["servers"] = df["servers"].apply(lambda x: x if x else ["unknown"])
    return df.explode("servers")["servers"].value_counts()


def plot_counts_bar(counts, title="Server Occurrences"):
    counts.plot(kind="bar", figsize=(8, 4))
    plt.xlabel("Server")
    plt.ylabel("Count")
    plt.title(title)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig("server_occurrences.png")
    plt.close()
