from transformers import pipeline
from utils.db_utils import get_db_connection

emotion_model = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions", return_all_scores=True)

emotion_cols = [
    "admiration","amusement","anger","annoyance","approval","caring","confusion",
    "curiosity","desire","disappointment","disapproval","disgust","embarrassment",
    "excitement","fear","gratitude","grief","joy","love","nervousness","optimism",
    "pride","realization","relief","remorse","sadness","surprise","neutral"
]

def extract_emotions():
    conn = get_db_connection()
    cur = conn.cursor()
    rows = cur.execute("SELECT id, summary FROM news_today").fetchall()

    for r in rows:
        if not r["summary"]:
            continue
        results = emotion_model(r["summary"][:512])[0]
        emotions = {x["label"]: x["score"] for x in results}
        values = [emotions.get(lbl, 0.0) for lbl in emotion_cols]

        cur.execute(f"""
        INSERT OR IGNORE INTO emotions_today (news_id, {", ".join(emotion_cols)})
        VALUES (?{", ?" * len(emotion_cols)})
        """, [r["id"]] + values)

        cur.execute("INSERT OR IGNORE INTO user_behavior_today (news_id) VALUES (?)", (r["id"],))

    conn.commit()
    conn.close()
    print("✅ Emotions extracted and saved")
