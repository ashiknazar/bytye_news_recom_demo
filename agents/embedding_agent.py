from sentence_transformers import SentenceTransformer
import pickle
from utils.db_utils import get_db_connection

model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embeddings():
    conn = get_db_connection()
    rows = conn.execute("SELECT id, title, summary FROM news_today").fetchall()
    texts = [(r["id"], (r["title"] or "") + " " + (r["summary"] or "")) for r in rows]
    conn.close()

    embeddings = {nid: model.encode(text) for nid, text in texts}
    with open("models/news_embeddings.pkl", "wb") as f:
        pickle.dump(embeddings, f)

    print("✅ Embeddings created and saved")
