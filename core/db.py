import sqlite3
import threading
import time
from typing import Optional, Dict, Any

DB_PATH = "auto_core.db"
_lock = threading.Lock()

def _connect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with _lock:
        conn = _connect()
        cur = conn.cursor()
        # posts table: avoid duplicate posting
        cur.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id TEXT PRIMARY KEY,
                title TEXT,
                slug TEXT,
                published_at INTEGER,
                platforms TEXT,
                lang TEXT,
                hash TEXT
            )
        """)
        # images cache
        cur.execute("""
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt_hash TEXT UNIQUE,
                url TEXT,
                created_at INTEGER
            )
        """)
        # internal links (simple storage)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS internal_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                url TEXT,
                tags TEXT,
                created_at INTEGER
            )
        """)
        # settings and quotas
        cur.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        conn.commit()
        conn.close()

def mark_posted(post_id: str, title: str, slug: str, platforms: str, lang: str, hash_value: str):
    with _lock:
        conn = _connect()
        cur = conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO posts (id, title, slug, published_at, platforms, lang, hash)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (post_id, title, slug, int(time.time()), platforms, lang, hash_value))
        conn.commit()
        conn.close()

def is_posted(post_id: str) -> bool:
    with _lock:
        conn = _connect()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM posts WHERE id = ?", (post_id,))
        row = cur.fetchone()
        conn.close()
        return row is not None

def find_similar_image(prompt_hash: str) -> Optional[str]:
    with _lock:
        conn = _connect()
        cur = conn.cursor()
        cur.execute("SELECT url FROM images WHERE prompt_hash = ?", (prompt_hash,))
        row = cur.fetchone()
        conn.close()
        return row["url"] if row else None

def save_image_cache(prompt_hash: str, url: str):
    with _lock:
        conn = _connect()
        cur = conn.cursor()
        cur.execute("INSERT OR REPLACE INTO images (prompt_hash, url, created_at) VALUES (?, ?, ?)",
                    (prompt_hash, url, int(time.time())))
        conn.commit()
        conn.close()

def add_internal_link(title: str, url: str, tags: str = ""):
    with _lock:
        conn = _connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO internal_links (title, url, tags, created_at) VALUES (?, ?, ?, ?)",
                    (title, url, tags, int(time.time())))
        conn.commit()
        conn.close()

def get_random_internal_links(limit: int = 3):
    with _lock:
        conn = _connect()
        cur = conn.cursor()
        cur.execute("SELECT title, url FROM internal_links ORDER BY RANDOM() LIMIT ?", (limit,))
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]
