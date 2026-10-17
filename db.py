import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_FILE = Path(__file__).parent / "tasks.db"


@contextmanager
def db():
    """Открывает соединение, коммитит при успехе, откатывает при ошибке, закрывает."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row      # доступ к колонкам по имени: row['id]
    try:
        yield conn
        conn.commit()                   # зафиксировать изменения
    except Exception:
        conn.rollback()                 # откатить при ошибке
        raise
    finally:
        conn.close()                    # закрыть в любом случае

def init_db():
    with db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL
            )
        """)