"""Эндпоинты для работы с пользователями"""
from fastapi import APIRouter, Depends

from schemas import UserRead
from users import get_current_user

router = APIRouter()


@router.get("/me", response_model=UserRead)
def read_users_me(current_user: dict = Depends(get_current_user)):
    """Возвращаем данные текущего авторизованного пользователя"""
    return current_user