import matplotlib.pyplot as plt


def plot_counts_bar(counts, title="Server Occurrences"):
    counts.plot(kind="bar", figsize=(8, 4))
    plt.xlabel("Server")
    plt.ylabel("Count")
    plt.title(title)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()
