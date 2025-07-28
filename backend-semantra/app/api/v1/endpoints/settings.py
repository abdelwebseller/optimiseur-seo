from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.core.database import get_db
from app.services.settings_service import SettingsService

router = APIRouter()

@router.get("/")
async def get_settings(
    db: Session = Depends(get_db)
):
    """Récupérer les paramètres de l'utilisateur"""
    settings_service = SettingsService(db)
    settings = settings_service.get_user_settings("temp-user-id")  # À remplacer par l'utilisateur authentifié
    
    return settings

@router.put("/")
async def update_settings(
    settings_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Mettre à jour les paramètres de l'utilisateur"""
    settings_service = SettingsService(db)
    updated_settings = settings_service.update_user_settings(
        "temp-user-id",  # À remplacer par l'utilisateur authentifié
        settings_data
    )
    
    return {
        "message": "Paramètres mis à jour avec succès",
        "settings": updated_settings
    }

@router.get("/embedding-models")
async def get_embedding_models(
    db: Session = Depends(get_db)
):
    """Récupérer les modèles d'embedding disponibles"""
    settings_service = SettingsService(db)
    models = settings_service.get_embedding_models()
    
    return {
        "models": models,
        "default_model": "text-embedding-3-large"
    }

@router.post("/embedding-models")
async def add_embedding_model(
    model_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Ajouter un nouveau modèle d'embedding"""
    settings_service = SettingsService(db)
    model = settings_service.add_embedding_model(model_data)
    
    return {
        "message": "Modèle d'embedding ajouté avec succès",
        "model": model
    }

@router.get("/crawl-configs")
async def get_crawl_configs(
    db: Session = Depends(get_db)
):
    """Récupérer les configurations de crawl"""
    settings_service = SettingsService(db)
    configs = settings_service.get_crawl_configs("temp-user-id")
    
    return configs

@router.post("/crawl-configs")
async def create_crawl_config(
    config_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Créer une nouvelle configuration de crawl"""
    settings_service = SettingsService(db)
    config = settings_service.create_crawl_config(
        "temp-user-id",  # À remplacer par l'utilisateur authentifié
        config_data
    )
    
    return {
        "message": "Configuration de crawl créée avec succès",
        "config": config
    } 