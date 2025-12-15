def count_servers(df, description_col="description"):
    df = df.copy()
    df["servers"] = df[description_col].str.lower().str.findall(r"(srv-[a-z0-9-]+)")
    df["servers"] = df["servers"].apply(lambda x: x if x else ["unknown"])
    return df.explode("servers")["servers"].value_counts()
