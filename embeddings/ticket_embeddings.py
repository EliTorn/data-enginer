from sentence_transformers import SentenceTransformer
from db.repository import save_ticket_embedding, get_jira_issues_without_embedding
from sentence_transformers import SentenceTransformer


def init_ticket_embeddings(batch_size: int = 50):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("Creating ticket embeddings (batched)...")
    while True:
        df = get_jira_issues_without_embedding(batch_size)
        if df.empty:
            print("No tickets without embeddings")
            break
        texts = df["description"].tolist()
        ids = df["id"].tolist()

        embeddings = model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False
        )
        for ticket_id, emb in zip(ids, embeddings):
            save_ticket_embedding(ticket_id, emb)
        print(f"Processed {len(ids)} tickets")
    print("Ticket embeddings saved to database")
