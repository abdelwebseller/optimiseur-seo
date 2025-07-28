from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class AnalysisStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class CrawlSpeed(str, Enum):
    SLOW = "slow"
    MEDIUM = "medium"
    FAST = "fast"

class AnalysisCreate(BaseModel):
    sitemap_url: HttpUrl
    crawl_settings: Optional[Dict[str, Any]] = Field(default_factory=dict)
    ai_settings: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    class Config:
        json_schema_extra = {
            "example": {
                "sitemap_url": "https://example.com/sitemap.xml",
                "crawl_settings": {
                    "max_urls": 1000000,
                    "crawl_speed": "medium",
                    "user_agent": "Semantra Bot 1.0",
                    "delay_between_requests": 1000,
                    "retry_attempts": 3
                },
                "ai_settings": {
                    "embedding_model": "text-embedding-3-large",
                    "openai_api_key": "sk-...",
                    "anchor_optimization": {
                        "enabled": True,
                        "provider": "openai",
                        "model": "gpt-4"
                    }
                }
            }
        }

class AnalysisUpdate(BaseModel):
    status: Optional[AnalysisStatus] = None
    progress: Optional[int] = Field(None, ge=0, le=100)
    total_urls: Optional[int] = None
    crawled_urls: Optional[int] = None
    failed_urls: Optional[int] = None
    statistics: Optional[Dict[str, Any]] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class AnalysisResponse(BaseModel):
    id: str
    user_id: str
    sitemap_url: str
    status: AnalysisStatus
    progress: int
    total_urls: int
    crawled_urls: int
    failed_urls: int
    crawl_settings: Dict[str, Any]
    ai_settings: Dict[str, Any]
    statistics: Dict[str, Any]
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class AnalysisStatusResponse(BaseModel):
    id: str
    status: AnalysisStatus
    progress: int
    total_urls: int
    crawled_urls: int
    failed_urls: int
    estimated_completion: Optional[datetime] = None
    current_speed: Optional[str] = None
    blocked_requests: int = 0
    retry_queue: int = 0 