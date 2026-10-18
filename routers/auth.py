from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from schemas import Token, UserCreate, UserRead, RefreshTokenRequest
from security import (
    create_access_token, create_refresh_token, hash_password, 
    verify_password, decode_token, get_token_hash
)
from users import (
    user_create, user_get_by_username, update_user_refresh_token, 
    user_get_by_refresh_hash, get_current_user
)

router = APIRouter()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate):
    user = user_create(payload.username, hash_password(payload.password))
    if user is None:
        raise HTTPException(status_code=400, detail="Username already taken")
    return user

@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = user_get_by_username(form.username)
    if user is None or not verify_password(form.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = create_access_token(user["id"])
    refresh_token = create_refresh_token(user["id"])
    
    # Сохраняем хеш refresh-токена в БД
    update_user_refresh_token(user["id"], get_token_hash(refresh_token))
    
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token, 
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
def refresh(payload: RefreshTokenRequest):
    # 1. Декодируем refresh-токен
    token_data = decode_token(payload.refresh_token, expected_type="refresh")
    user_id = int(token_data["sub"])
    
    # 2. Проверяем, есть ли такой хеш в БД (защита от повторного использования)
    token_hash = get_token_hash(payload.refresh_token)
    user = user_get_by_refresh_hash(token_hash)
    if user is None or user["id"] != user_id:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    # 3. Генерируем НОВУЮ пару (Rotation)
    new_access = create_access_token(user_id)
    new_refresh = create_refresh_token(user_id)
    
    # 4. Обновляем хеш в БД
    update_user_refresh_token(user_id, get_token_hash(new_refresh))
    
    return {
        "access_token": new_access, 
        "refresh_token": new_refresh, 
        "token_type": "bearer"
    }

@router.post("/logout")
def logout(current_user: dict = Depends(get_current_user)):
    # Удаляем refresh-токен из БД
    update_user_refresh_token(current_user["id"], None)
    return {"message": "Logged out successfully"}