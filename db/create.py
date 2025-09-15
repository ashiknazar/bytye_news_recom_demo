import sqlite3

def init_db(db_path="news.db"):
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")  # ✅ enforce foreign keys
    cursor = conn.cursor()

    # --- news_today ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news_today (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            source TEXT,
            title TEXT,
            link TEXT UNIQUE,
            published TEXT,
            summary TEXT,
            created_at TEXT
        )
    """)

    # --- emotions_today ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emotions_today (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            news_id INTEGER,
            admiration REAL,
            amusement REAL,
            anger REAL,
            annoyance REAL,
            approval REAL,
            caring REAL,
            confusion REAL,
            curiosity REAL,
            desire REAL,
            disappointment REAL,
            disapproval REAL,
            disgust REAL,
            embarrassment REAL,
            excitement REAL,
            fear REAL,
            gratitude REAL,
            grief REAL,
            joy REAL,
            love REAL,
            nervousness REAL,
            optimism REAL,
            pride REAL,
            realization REAL,
            relief REAL,
            remorse REAL,
            sadness REAL,
            surprise REAL,
            neutral REAL,
            FOREIGN KEY (news_id) REFERENCES news_today(id) ON DELETE CASCADE
        )
    """)

    # --- user_behavior_today ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_behavior_today (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            news_id INTEGER,
            views_count INTEGER DEFAULT 0,
            total_read_time INTEGER DEFAULT 0,
            ignored_suggestions INTEGER DEFAULT 0,
            general_view INTEGER DEFAULT 0,
            FOREIGN KEY (news_id) REFERENCES news_today(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("✅ Tables created with foreign key constraints")
