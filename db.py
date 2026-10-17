"""Слой доступа к базе данных (PostgreSQL)"""
import os
from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://todo:todo@localhost:5432/todo"
)


@contextmanager
def db():
    """Открывает соединение, коммитит при успехе, откатывает при ошибке, закрывает."""
    conn = psycopg.connect(DATABASE_URL, row_factory=dict_row)
    try:
        yield conn
        conn.commit()                   # зафиксировать изменения
    except Exception:
        conn.rollback()                 # откатить при ошибке
        raise
    finally:
        conn.close()                    # закрыть в любом случае