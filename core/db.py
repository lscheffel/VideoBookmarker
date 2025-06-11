import sqlite3
import json

class Database:
    def __init__(self, db_path="video_bookmarker.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        c = self.conn.cursor()
        # Tabela de sessões
        c.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        ''')
        # Tabela de vídeos (playlist) vinculada a uma sessão
        c.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                page_url TEXT NOT NULL,
                url TEXT,
                title TEXT,
                valid INTEGER,
                favorite INTEGER,
                FOREIGN KEY(session_id) REFERENCES sessions(id) ON DELETE CASCADE
            )
        ''')
        self.conn.commit()

    def save_session(self, name, playlist):
        c = self.conn.cursor()
        # Tenta inserir nova sessão
        c.execute('INSERT OR IGNORE INTO sessions (name) VALUES (?)', (name,))
        # Busca o id da sessão
        c.execute('SELECT id FROM sessions WHERE name = ?', (name,))
        session_row = c.fetchone()
        if not session_row:
            return False
        session_id = session_row['id']
        # Remove vídeos antigos da sessão
        c.execute('DELETE FROM videos WHERE session_id = ?', (session_id,))
        # Insere os vídeos da playlist
        for item in playlist:
            c.execute('''
                INSERT INTO videos (session_id, page_url, url, title, valid, favorite)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                session_id,
                item.get('page_url'),
                item.get('url'),
                item.get('title'),
                1 if item.get('valid') else 0,
                1 if item.get('favorite') else 0
            ))
        self.conn.commit()
        return True

    def list_sessions(self):
        c = self.conn.cursor()
        c.execute('SELECT name FROM sessions ORDER BY name')
        rows = c.fetchall()
        return [row['name'] for row in rows]

    def load_session(self, name):
        c = self.conn.cursor()
        c.execute('SELECT id FROM sessions WHERE name = ?', (name,))
        session_row = c.fetchone()
        if not session_row:
            return None
        session_id = session_row['id']
        c.execute('SELECT page_url, url, title, valid, favorite FROM videos WHERE session_id = ?', (session_id,))
        rows = c.fetchall()
        playlist = []
        for row in rows:
            playlist.append({
                'page_url': row['page_url'],
                'url': row['url'],
                'title': row['title'],
                'valid': bool(row['valid']),
                'favorite': bool(row['favorite'])
            })
        return playlist
    def close(self):
        self.conn.close()

