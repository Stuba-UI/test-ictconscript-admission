import sqlite3

DB_FILE = "logbook.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            title   TEXT NOT NULL,
            body    TEXT NOT NULL,
            isoTime TEXT NOT NULL,
            lat     REAL,
            lon     REAL
        )
    """)

def get_all_entries():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM entries ORDER BY isoTime DESC").fetchall()
    conn.close()
    return rows
    conn.commit()
    conn.close()

def get_entry(entry_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM entries WHERE id = ?", (entry_id,)).fetchone()
    conn.close()
    return row

