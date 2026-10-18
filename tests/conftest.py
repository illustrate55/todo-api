"""Натсройка окружения для тестов"""
import os
import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "postgresql://todo:todo@localhost:5432/todo_test"
os.environ["JWT_SECRET"] = "test-secret-key-for-testing-only-32-chars"

from app import app
from db import db
from sqlalchemy import create_engine
from models import Base


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Создаем таблицы в тестовой БД перед всеми тестами и удаляем после"""
    engine = create_engine("postgresql+psycopg://todo:todo@localhost:5432/todo_test")
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(autouse=True)
def clean_db():
    """Очищаем базу перед каждым тестом, чтобы они не влияли друг на друга"""
    with db() as conn:
        conn.execute("TRUNCATE TABLE tasks, users RESTART IDENTITY CASCADE")
    yield


@pytest.fixture
def client():
    """Возвращаем тестовый HTTP-клиент"""
    with TestClient(app) as c:
        yield c