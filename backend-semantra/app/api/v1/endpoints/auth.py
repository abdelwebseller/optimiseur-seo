from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
import jwt

from app.core.database import get_db
from app.core.config import settings
from app.services.user_service import UserService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register")
async def register(
    email: str,
    username: str,
    password: str,
    db: Session = Depends(get_db)
):
    """Enregistrer un nouvel utilisateur"""
    user_service = UserService(db)
    
    # Vérifier si l'utilisateur existe déjà
    existing_user = user_service.get_user_by_email(email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Un utilisateur avec cet email existe déjà"
        )
    
    # Créer l'utilisateur
    user = user_service.create_user(email, username, password)
    
    return {
        "message": "Utilisateur créé avec succès",
        "user_id": user.id,
        "email": user.email,
        "username": user.username
    }

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Se connecter"""
    user_service = UserService(db)
    
    # Authentifier l'utilisateur
    user = user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Créer le token d'accès
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = user_service.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "username": user.username
    }

@router.get("/profile")
async def get_profile(
    current_user = Depends(user_service.get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer le profil de l'utilisateur connecté"""
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at
    }

@router.post("/logout")
async def logout():
    """Se déconnecter"""
    return {"message": "Déconnexion réussie"}

@router.post("/refresh")
async def refresh_token(
    current_user = Depends(user_service.get_current_user)
):
    """Rafraîchir le token d'accès"""
    user_service = UserService()
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = user_service.create_access_token(
        data={"sub": current_user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    } 