from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class SuggestionStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class SuggestionCreate(BaseModel):
    analysis_id: str
    source_page: str
    target_page: str
    anchor_text: str
    score: float = Field(..., ge=0.0, le=1.0)
    reasoning: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class SuggestionUpdate(BaseModel):
    status: Optional[SuggestionStatus] = None
    anchor_text: Optional[str] = None
    reasoning: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class SuggestionResponse(BaseModel):
    id: str
    analysis_id: str
    source_page: str
    target_page: str
    anchor_text: str
    score: float
    status: SuggestionStatus
    reasoning: Optional[str] = None
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class SuggestionFilter(BaseModel):
    status: Optional[SuggestionStatus] = None
    min_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    max_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    search_term: Optional[str] = None
    limit: Optional[int] = Field(100, ge=1, le=1000)
    offset: Optional[int] = Field(0, ge=0)

class SuggestionListResponse(BaseModel):
    suggestions: List[SuggestionResponse]
    total: int
    limit: int
    offset: int
    has_more: bool

class AnchorOptimizationRequest(BaseModel):
    current_anchor: str
    target_page_title: str
    context: str
    provider: str = "openai"  # openai, gemini
    style: str = "natural"  # natural, commercial, technical
    max_length: int = Field(50, ge=1, le=200)
    
    class Config:
        json_schema_extra = {
            "example": {
                "current_anchor": "cliquez ici",
                "target_page_title": "Guide SEO Complet",
                "context": "Page sur les techniques SEO",
                "provider": "openai",
                "style": "natural",
                "max_length": 50
            }
        }

class AnchorOptimizationResponse(BaseModel):
    optimized_anchor: str
    confidence_score: float
    alternatives: List[str]
    reasoning: Optional[str] = None 