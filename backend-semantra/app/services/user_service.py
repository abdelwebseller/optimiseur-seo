from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
import uuid

from app.models.user import User
from app.core.config import settings

# Configuration du hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, email: str, username: str, password: str) -> User:
        """Créer un nouvel utilisateur"""
        # Hacher le mot de passe
        hashed_password = pwd_context.hash(password)
        
        # Créer l'utilisateur
        user = User(
            id=str(uuid.uuid4()),
            email=email,
            username=username,
            hashed_password=hashed_password,
            is_active=True
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Récupérer un utilisateur par email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Récupérer un utilisateur par ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authentifier un utilisateur"""
        user = self.get_user_by_email(email)
        if not user:
            return None
        
        if not pwd_context.verify(password, user.hashed_password):
            return None
        
        return user
    
    def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        """Créer un token d'accès JWT"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[dict]:
        """Vérifier un token JWT"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                return None
            return payload
        except jwt.PyJWTError:
            return None
    
    def get_current_user(self, token: str) -> Optional[User]:
        """Récupérer l'utilisateur actuel à partir du token"""
        payload = self.verify_token(token)
        if payload is None:
            return None
        
        email: str = payload.get("sub")
        if email is None:
            return None
        
        return self.get_user_by_email(email)
    
    def update_user(self, user_id: str, update_data: dict) -> Optional[User]:
        """Mettre à jour un utilisateur"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        for field, value in update_data.items():
            if field == "password":
                # Hacher le nouveau mot de passe
                value = pwd_context.hash(value)
            setattr(user, field, value)
        
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def delete_user(self, user_id: str) -> bool:
        """Supprimer un utilisateur"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        self.db.delete(user)
        self.db.commit()
        
        return True
    
    def list_users(self, skip: int = 0, limit: int = 100) -> list:
        """Lister les utilisateurs"""
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def activate_user(self, user_id: str) -> bool:
        """Activer un utilisateur"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.is_active = True
        self.db.commit()
        
        return True
    
    def deactivate_user(self, user_id: str) -> bool:
        """Désactiver un utilisateur"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.is_active = False
        self.db.commit()
        
        return True 