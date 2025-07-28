from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from app.models.embedding_model import EmbeddingModel
from app.models.crawl_config import CrawlConfig
from app.models.url_filter import UrlFilter

class SettingsService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_settings(self, user_id: str) -> Dict[str, Any]:
        """Récupérer les paramètres d'un utilisateur"""
        # Paramètres par défaut
        default_settings = {
            "openai_api_key": "",
            "gemini_api_key": "",
            "similarity_threshold": 0.7,
            "max_suggestions": 50,
            "dark_mode": False,
            "auto_approve": False,
            "email_notifications": True,
            "embedding_model": "text-embedding-3-large",
            "custom_json_params": "{}",
            "backend_api_url": "http://localhost:8000",
            "crawl_settings": {
                "max_urls": 1000000,
                "user_agent": "Semantra Bot 1.0",
                "crawl_speed": "medium",
                "delay_between_requests": 1000,
                "retry_attempts": 3,
                "timeout": 30
            },
            "ai_settings": {
                "embedding_model": "text-embedding-3-large",
                "anchor_optimization": {
                    "enabled": True,
                    "provider": "openai",
                    "model": "gpt-4"
                }
            }
        }
        
        # Ici on pourrait charger les paramètres depuis la base de données
        # Pour l'instant, retourner les paramètres par défaut
        return default_settings
    
    def update_user_settings(self, user_id: str, settings_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mettre à jour les paramètres d'un utilisateur"""
        # Ici on pourrait sauvegarder les paramètres en base de données
        # Pour l'instant, retourner les paramètres mis à jour
        return settings_data
    
    def get_embedding_models(self) -> List[Dict[str, Any]]:
        """Récupérer les modèles d'embedding disponibles"""
        models = self.db.query(EmbeddingModel).filter(EmbeddingModel.is_active == True).all()
        
        # Modèles par défaut si aucun en base
        if not models:
            default_models = [
                {
                    "id": "default-ada-002",
                    "name": "text-embedding-ada-002",
                    "provider": "openai",
                    "model_id": "text-embedding-ada-002",
                    "dimensions": 1536,
                    "max_tokens": 8191,
                    "is_active": True,
                    "is_default": False
                },
                {
                    "id": "default-3-small",
                    "name": "text-embedding-3-small",
                    "provider": "openai",
                    "model_id": "text-embedding-3-small",
                    "dimensions": 1536,
                    "max_tokens": 8191,
                    "is_active": True,
                    "is_default": False
                },
                {
                    "id": "default-3-large",
                    "name": "text-embedding-3-large",
                    "provider": "openai",
                    "model_id": "text-embedding-3-large",
                    "dimensions": 3072,
                    "max_tokens": 8191,
                    "is_active": True,
                    "is_default": True
                }
            ]
            return default_models
        
        return [
            {
                "id": model.id,
                "name": model.name,
                "provider": model.provider,
                "model_id": model.model_id,
                "dimensions": model.dimensions,
                "max_tokens": model.max_tokens,
                "is_active": model.is_active,
                "is_default": model.is_default
            }
            for model in models
        ]
    
    def add_embedding_model(self, model_data: Dict[str, Any]) -> Dict[str, Any]:
        """Ajouter un nouveau modèle d'embedding"""
        model = EmbeddingModel(
            id=str(uuid.uuid4()),
            name=model_data["name"],
            provider=model_data["provider"],
            api_key=model_data.get("api_key", ""),
            model_id=model_data["model_id"],
            dimensions=model_data.get("dimensions", 1536),
            max_tokens=model_data.get("max_tokens", 8191),
            is_active=True,
            is_default=model_data.get("is_default", False),
            metadata=model_data.get("metadata", "{}")
        )
        
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        
        return {
            "id": model.id,
            "name": model.name,
            "provider": model.provider,
            "model_id": model.model_id,
            "dimensions": model.dimensions,
            "max_tokens": model.max_tokens,
            "is_active": model.is_active,
            "is_default": model.is_default
        }
    
    def get_crawl_configs(self, user_id: str) -> List[Dict[str, Any]]:
        """Récupérer les configurations de crawl d'un utilisateur"""
        configs = self.db.query(CrawlConfig).filter(CrawlConfig.user_id == user_id).all()
        
        return [
            {
                "id": config.id,
                "name": config.name,
                "max_urls": config.max_urls,
                "crawl_speed": config.crawl_speed,
                "delay_between_requests": config.delay_between_requests,
                "retry_attempts": config.retry_attempts,
                "timeout": config.timeout,
                "user_agent": config.user_agent,
                "user_agents_rotation": config.user_agents_rotation,
                "proxy_enabled": config.proxy_enabled,
                "proxy_list": config.proxy_list,
                "adaptive_speed": config.adaptive_speed,
                "adaptive_user_agent": config.adaptive_user_agent,
                "created_at": config.created_at.isoformat() if config.created_at else None
            }
            for config in configs
        ]
    
    def create_crawl_config(self, user_id: str, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """Créer une nouvelle configuration de crawl"""
        config = CrawlConfig(
            id=str(uuid.uuid4()),
            user_id=user_id,
            name=config_data["name"],
            max_urls=config_data.get("max_urls", 1000000),
            crawl_speed=config_data.get("crawl_speed", "medium"),
            delay_between_requests=config_data.get("delay_between_requests", 1000),
            retry_attempts=config_data.get("retry_attempts", 3),
            timeout=config_data.get("timeout", 30),
            user_agent=config_data.get("user_agent", "Semantra Bot 1.0"),
            user_agents_rotation=config_data.get("user_agents_rotation", []),
            proxy_enabled=config_data.get("proxy_enabled", False),
            proxy_list=config_data.get("proxy_list", []),
            adaptive_speed=config_data.get("adaptive_speed", True),
            adaptive_user_agent=config_data.get("adaptive_user_agent", True)
        )
        
        self.db.add(config)
        self.db.commit()
        self.db.refresh(config)
        
        # Ajouter les filtres URL si fournis
        if "url_filters" in config_data:
            for filter_data in config_data["url_filters"]:
                url_filter = UrlFilter(
                    id=str(uuid.uuid4()),
                    crawl_config_id=config.id,
                    filter_type=filter_data["filter_type"],
                    filter_value=filter_data["filter_value"],
                    is_exclude=filter_data.get("is_exclude", False),
                    priority=filter_data.get("priority", 0)
                )
                self.db.add(url_filter)
            
            self.db.commit()
        
        return {
            "id": config.id,
            "name": config.name,
            "max_urls": config.max_urls,
            "crawl_speed": config.crawl_speed,
            "delay_between_requests": config.delay_between_requests,
            "retry_attempts": config.retry_attempts,
            "timeout": config.timeout,
            "user_agent": config.user_agent,
            "user_agents_rotation": config.user_agents_rotation,
            "proxy_enabled": config.proxy_enabled,
            "proxy_list": config.proxy_list,
            "adaptive_speed": config.adaptive_speed,
            "adaptive_user_agent": config.adaptive_user_agent,
            "created_at": config.created_at.isoformat() if config.created_at else None
        }
    
    def update_crawl_config(self, config_id: str, config_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Mettre à jour une configuration de crawl"""
        config = self.db.query(CrawlConfig).filter(CrawlConfig.id == config_id).first()
        if not config:
            return None
        
        for field, value in config_data.items():
            if hasattr(config, field):
                setattr(config, field, value)
        
        config.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(config)
        
        return {
            "id": config.id,
            "name": config.name,
            "max_urls": config.max_urls,
            "crawl_speed": config.crawl_speed,
            "delay_between_requests": config.delay_between_requests,
            "retry_attempts": config.retry_attempts,
            "timeout": config.timeout,
            "user_agent": config.user_agent,
            "user_agents_rotation": config.user_agents_rotation,
            "proxy_enabled": config.proxy_enabled,
            "proxy_list": config.proxy_list,
            "adaptive_speed": config.adaptive_speed,
            "adaptive_user_agent": config.adaptive_user_agent,
            "updated_at": config.updated_at.isoformat() if config.updated_at else None
        }
    
    def delete_crawl_config(self, config_id: str) -> bool:
        """Supprimer une configuration de crawl"""
        config = self.db.query(CrawlConfig).filter(CrawlConfig.id == config_id).first()
        if not config:
            return False
        
        self.db.delete(config)
        self.db.commit()
        
        return True 