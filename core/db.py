import sqlite3

def init_db():
    conn = sqlite3.connect("videos.db")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS playlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            session TEXT DEFAULT 'default'
        )
    ''')
    conn.commit()
    conn.close()

def add_to_playlist(urls, session='default'):
    conn = sqlite3.connect("videos.db")
    cur = conn.cursor()
    for url in urls:
        cur.execute("INSERT INTO playlist (url, session) VALUES (?, ?)", (url, session))
    conn.commit()
    conn.close()

def get_playlist(session='default'):
    conn = sqlite3.connect("videos.db")
    cur = conn.cursor()
    cur.execute("SELECT id, url FROM playlist WHERE session = ?", (session,))
    items = cur.fetchall()
    conn.close()
    return items
