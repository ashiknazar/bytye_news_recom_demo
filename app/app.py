from flask import Flask, render_template
from utils.db_utils import get_db_connection
from agents.recommendation_agent import recommend_for_user

app = Flask(__name__)

@app.route("/")
def index():
    conn = get_db_connection()
    news = conn.execute("SELECT * FROM news_today ORDER BY published DESC LIMIT 10").fetchall()
    conn.close()
    return render_template("index.html", news_list=news)

@app.route("/recommendations")
def recommendations():
    recs = recommend_for_user()
    if not recs:
        return "No recommendations yet!"
    conn = get_db_connection()
    rows = conn.execute(f"SELECT * FROM news_today WHERE id IN ({','.join('?'*len(recs))})", recs).fetchall()
    conn.close()
    return render_template("reco.html", reco_list=rows)

if __name__ == "__main__":
    app.run(debug=True)
