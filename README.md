# 🚀 Fullstack Todo App (FastAPI + React)

[![Python CI](https://github.com/illustrate55/todo-api/actions/workflows/ci.yml/badge.svg)](https://github.com/illustrate55/todo-api/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)

Современное Fullstack-приложение для управления задачами (Todo List) с безопасной JWT-аутентификацией, изоляцией пользовательских данных и адаптивным интерфейсом.

## ✨ Основные возможности

- 🔐 **Безопасная авторизация**: JWT (Access + Refresh токены) с ротацией и защитой от повторного использования.
- 👥 **Multi-tenancy**: У каждого пользователя свой изолированный список задач.
- ⚛️ **Современный Frontend**: React (Vite) с автоматическим обновлением токена (Axios interceptors) и красивым UI.
- 🐘 **Надежная БД**: PostgreSQL + SQLAlchemy + Alembic для управления миграциями.
- 🐳 **Контейнеризация**: Docker Compose поднимает базу данных и бэкенд одной командой.
- ✅ **Покрытие тестами**: 9 интеграционных тестов (Pytest) для проверки API и безопасности.
- ⚙️ **CI/CD**: GitHub Actions автоматически запускает тесты при каждом пуше.

## 🛠 Технологический стек

**Backend:**
* Python 3.12, FastAPI
* PostgreSQL, Psycopg 3, SQLAlchemy, Alembic
* PyJWT, Bcrypt (безопасность)

**Frontend:**
* React 18, Vite
* Axios (с перехватчиками запросов/ответов)
* Vanilla CSS (современный дизайн)

**DevOps:**
* Docker, Docker Compose
* GitHub Actions (CI)

## 📸 Скриншот интерфейса

*(Здесь ты можешь вставить картинку интерфейса)*
<!-- Например: ![Интерфейс приложения](./screenshot.png) -->

## 🚀 Как запустить локально

### Требования
Убедитесь, что у вас установлены **Docker**, **Node.js** и **Python 3.12+**.

### 1. Запуск бэкенда и базы данных
Клонируйте репозиторий и запустите Docker Compose:
```bash
git clone https://github.com/illustrate55/todo-api.git
cd todo-api
docker compose up --build -d