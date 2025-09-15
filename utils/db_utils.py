import sqlite3
from config import DB_PATH

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS news_today (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        source TEXT,
        title TEXT,
        link TEXT,
        published TEXT,
        summary TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS emotions_today (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        news_id INTEGER,
        admiration REAL, amusement REAL, anger REAL, annoyance REAL, approval REAL,
        caring REAL, confusion REAL, curiosity REAL, desire REAL, disappointment REAL,
        disapproval REAL, disgust REAL, embarrassment REAL, excitement REAL, fear REAL,
        gratitude REAL, grief REAL, joy REAL, love REAL, nervousness REAL, optimism REAL,
        pride REAL, realization REAL, relief REAL, remorse REAL, sadness REAL, surprise REAL,
        neutral REAL,
        FOREIGN KEY(news_id) REFERENCES news_today(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_behavior_today (
        news_id INTEGER PRIMARY KEY,
        views_count INTEGER DEFAULT 0,
        total_read_time INTEGER DEFAULT 0,
        ignored_suggestions INTEGER DEFAULT 0,
        general_view INTEGER DEFAULT 0,
        FOREIGN KEY(news_id) REFERENCES news_today(id)
    )
    """)

    conn.commit()
    conn.close()
