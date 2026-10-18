"""Эндпоинты ругистрации и входа"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from schemas import Token, UserCreate, UserRead
from security import create_access_token, hash_password, verify_password
from users import user_create, user_get_by_username

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
    token = create_access_token(user["id"])
    return {"access_token": token, "token_type": "bearer"}