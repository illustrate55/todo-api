"""Пользователи и зависимость get_current_user"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from db import db
from security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def user_create(username: str, password_hash: str) -> dict | None:
    """Возвращает созданного пользователя или None, если логин занят"""
    with db() as conn:
        existing = conn.execute("SELECT id FROM users WHERE username = %s", (username,)).fetchone()
        if existing:
            return None
        row = conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id, username",
            (username, password_hash),
        ).fetchone()
    return dict(row)


def user_get_by_username(username: str) -> dict | None:
    with db() as conn:
        row = conn.execute("SELECT id, username, password_hash FROM users WHERE username = %s", (username,)
        ).fetchone()
    return dict(row) if row else None


def user_get_by_id(user_id: int) -> dict | None:
    with db() as conn:
        row = conn.execute("SELECT id, username FROM users WHERE id = %s", (user_id,)).fetchone()
    return dict(row) if row else None


def update_user_refresh_token(user_id: int, token_hash: str | None):
    with db() as conn:
        conn.execute(
            "UPDATE users SET refresh_token_hash = %s WHERE id = %s",
            (token_hash, user_id)
        )


def user_get_by_refresh_hash(token_hash: str) -> dict | None:
    with db() as conn:
        row = conn.execute(
            "SELECT id, username FROM users WHERE refresh_token_hash = %s",
            (token_hash,)
        ).fetchone()
    return dict(row) if row else None


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Декодирует токен и возвращает текущего юзера"""
    payload = decode_token(token, expected_type="access")
    sub = payload.get("sub")
    user = user_get_by_id(int(sub))
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user