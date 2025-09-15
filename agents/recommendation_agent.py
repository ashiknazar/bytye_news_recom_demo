import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from utils.db_utils import get_db_connection

def recommend_for_user():
    with open("models/news_embeddings.pkl", "rb") as f:
        embeddings = pickle.load(f)

    ids = list(embeddings.keys())
    vectors = np.array(list(embeddings.values()))

    conn = get_db_connection()
    viewed = conn.execute("SELECT news_id FROM user_behavior_today WHERE views_count > 0").fetchall()
    viewed_ids = [v["news_id"] for v in viewed]
    conn.close()

    if not viewed_ids:
        print("⚠️ No viewed news yet.")
        return []

    recs = []
    for vid in viewed_ids:
        if vid not in embeddings:
            continue
        idx = ids.index(vid)
        sims = cosine_similarity([embeddings[vid]], vectors)[0]
        best_idx = np.argsort(sims)[::-1][1:6]
        for i in best_idx:
            recs.append(ids[i])

    print("✅ Recommendations ready:", recs[:10])
    return recs
