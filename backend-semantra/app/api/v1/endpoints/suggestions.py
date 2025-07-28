from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.schemas.suggestion import (
    SuggestionCreate,
    SuggestionUpdate,
    SuggestionResponse,
    SuggestionFilter,
    SuggestionListResponse,
    AnchorOptimizationRequest,
    AnchorOptimizationResponse
)
from app.services.suggestion_service import SuggestionService
from app.services.ai_service import AIService

router = APIRouter()

@router.post("/", response_model=SuggestionResponse)
async def create_suggestion(
    suggestion_data: SuggestionCreate,
    db: Session = Depends(get_db)
):
    """Créer une nouvelle suggestion"""
    suggestion_service = SuggestionService(db)
    suggestion = suggestion_service.create_suggestion(suggestion_data)
    return suggestion

@router.get("/", response_model=SuggestionListResponse)
async def list_suggestions(
    analysis_id: Optional[str] = Query(None, description="ID de l'analyse"),
    status: Optional[str] = Query(None, description="Statut de la suggestion"),
    min_score: Optional[float] = Query(None, ge=0.0, le=1.0),
    max_score: Optional[float] = Query(None, ge=0.0, le=1.0),
    search_term: Optional[str] = Query(None, description="Terme de recherche"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Lister les suggestions avec filtres"""
    suggestion_service = SuggestionService(db)
    
    filters = SuggestionFilter(
        status=status,
        min_score=min_score,
        max_score=max_score,
        search_term=search_term,
        limit=limit,
        offset=offset
    )
    
    result = suggestion_service.list_suggestions(
        analysis_id=analysis_id,
        filters=filters
    )
    
    return result

@router.get("/{suggestion_id}", response_model=SuggestionResponse)
async def get_suggestion(
    suggestion_id: str,
    db: Session = Depends(get_db)
):
    """Récupérer une suggestion par son ID"""
    suggestion_service = SuggestionService(db)
    suggestion = suggestion_service.get_suggestion(suggestion_id)
    
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion non trouvée")
    
    return suggestion

@router.put("/{suggestion_id}", response_model=SuggestionResponse)
async def update_suggestion(
    suggestion_id: str,
    suggestion_update: SuggestionUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour une suggestion"""
    suggestion_service = SuggestionService(db)
    suggestion = suggestion_service.update_suggestion(suggestion_id, suggestion_update)
    
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion non trouvée")
    
    return suggestion

@router.delete("/{suggestion_id}")
async def delete_suggestion(
    suggestion_id: str,
    db: Session = Depends(get_db)
):
    """Supprimer une suggestion"""
    suggestion_service = SuggestionService(db)
    success = suggestion_service.delete_suggestion(suggestion_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Suggestion non trouvée")
    
    return {"message": "Suggestion supprimée avec succès"}

@router.post("/{suggestion_id}/optimize-anchor", response_model=AnchorOptimizationResponse)
async def optimize_anchor(
    suggestion_id: str,
    optimization_request: AnchorOptimizationRequest,
    db: Session = Depends(get_db)
):
    """Optimiser l'ancre d'une suggestion"""
    suggestion_service = SuggestionService(db)
    suggestion = suggestion_service.get_suggestion(suggestion_id)
    
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion non trouvée")
    
    # Utiliser le service AI pour optimiser l'ancre
    ai_service = AIService()
    optimization_result = ai_service.optimize_anchor(
        current_anchor=optimization_request.current_anchor,
        target_page_title=optimization_request.target_page_title,
        context=optimization_request.context,
        provider=optimization_request.provider,
        style=optimization_request.style,
        max_length=optimization_request.max_length
    )
    
    # Sauvegarder l'optimisation
    suggestion_service.save_anchor_optimization(
        suggestion_id=suggestion_id,
        original_anchor=optimization_request.current_anchor,
        optimized_anchor=optimization_result["optimized_anchor"],
        provider=optimization_request.provider,
        model=optimization_request.provider == "openai" and "gpt-4" or "gemini-pro",
        confidence_score=optimization_result["confidence_score"],
        alternatives=optimization_result["alternatives"]
    )
    
    return AnchorOptimizationResponse(
        optimized_anchor=optimization_result["optimized_anchor"],
        confidence_score=optimization_result["confidence_score"],
        alternatives=optimization_result["alternatives"],
        reasoning=optimization_result.get("reasoning")
    )

@router.post("/optimize-anchor", response_model=AnchorOptimizationResponse)
async def optimize_anchor_standalone(
    optimization_request: AnchorOptimizationRequest
):
    """Optimiser une ancre sans suggestion existante"""
    ai_service = AIService()
    optimization_result = ai_service.optimize_anchor(
        current_anchor=optimization_request.current_anchor,
        target_page_title=optimization_request.target_page_title,
        context=optimization_request.context,
        provider=optimization_request.provider,
        style=optimization_request.style,
        max_length=optimization_request.max_length
    )
    
    return AnchorOptimizationResponse(
        optimized_anchor=optimization_result["optimized_anchor"],
        confidence_score=optimization_result["confidence_score"],
        alternatives=optimization_result["alternatives"],
        reasoning=optimization_result.get("reasoning")
    )

@router.post("/batch-update")
async def batch_update_suggestions(
    suggestion_ids: List[str],
    status: str,
    db: Session = Depends(get_db)
):
    """Mettre à jour plusieurs suggestions en lot"""
    suggestion_service = SuggestionService(db)
    updated_count = suggestion_service.batch_update_status(suggestion_ids, status)
    
    return {
        "message": f"{updated_count} suggestions mises à jour",
        "updated_count": updated_count
    } 