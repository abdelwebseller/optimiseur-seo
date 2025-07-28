from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime

from app.core.database import get_db
from app.schemas.analysis import (
    AnalysisCreate, 
    AnalysisResponse, 
    AnalysisUpdate,
    AnalysisStatusResponse
)
from app.services.analysis_service import AnalysisService
from app.services.crawl_service import CrawlService
from app.tasks.analysis_tasks import start_analysis_task

router = APIRouter()

@router.post("/", response_model=AnalysisResponse)
async def create_analysis(
    analysis_data: AnalysisCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Créer une nouvelle analyse SEO"""
    try:
        # Créer l'analyse en base
        analysis_service = AnalysisService(db)
        analysis = analysis_service.create_analysis(
            user_id="temp-user-id",  # À remplacer par l'utilisateur authentifié
            sitemap_url=str(analysis_data.sitemap_url),
            crawl_settings=analysis_data.crawl_settings,
            ai_settings=analysis_data.ai_settings
        )
        
        # Lancer l'analyse en arrière-plan
        background_tasks.add_task(
            start_analysis_task,
            analysis_id=analysis.id,
            sitemap_url=str(analysis_data.sitemap_url),
            crawl_settings=analysis_data.crawl_settings,
            ai_settings=analysis_data.ai_settings
        )
        
        return analysis
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: str,
    db: Session = Depends(get_db)
):
    """Récupérer une analyse par son ID"""
    analysis_service = AnalysisService(db)
    analysis = analysis_service.get_analysis(analysis_id)
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analyse non trouvée")
    
    return analysis

@router.get("/{analysis_id}/status", response_model=AnalysisStatusResponse)
async def get_analysis_status(
    analysis_id: str,
    db: Session = Depends(get_db)
):
    """Récupérer le statut d'une analyse"""
    analysis_service = AnalysisService(db)
    analysis = analysis_service.get_analysis(analysis_id)
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analyse non trouvée")
    
    # Calculer les métriques en temps réel
    crawl_service = CrawlService()
    real_time_stats = crawl_service.get_real_time_stats(analysis_id)
    
    return AnalysisStatusResponse(
        id=analysis.id,
        status=analysis.status,
        progress=analysis.progress,
        total_urls=analysis.total_urls,
        crawled_urls=analysis.crawled_urls,
        failed_urls=analysis.failed_urls,
        estimated_completion=real_time_stats.get("estimated_completion"),
        current_speed=real_time_stats.get("current_speed"),
        blocked_requests=real_time_stats.get("blocked_requests", 0),
        retry_queue=real_time_stats.get("retry_queue", 0)
    )

@router.get("/{analysis_id}/results")
async def get_analysis_results(
    analysis_id: str,
    db: Session = Depends(get_db)
):
    """Récupérer les résultats d'une analyse"""
    analysis_service = AnalysisService(db)
    analysis = analysis_service.get_analysis(analysis_id)
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analyse non trouvée")
    
    if analysis.status != "completed":
        raise HTTPException(status_code=400, detail="L'analyse n'est pas encore terminée")
    
    # Récupérer les suggestions
    suggestions = analysis_service.get_suggestions_for_analysis(analysis_id)
    
    return {
        "analysis": analysis,
        "suggestions": suggestions,
        "statistics": analysis.statistics
    }

@router.put("/{analysis_id}", response_model=AnalysisResponse)
async def update_analysis(
    analysis_id: str,
    analysis_update: AnalysisUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour une analyse"""
    analysis_service = AnalysisService(db)
    analysis = analysis_service.update_analysis(analysis_id, analysis_update)
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analyse non trouvée")
    
    return analysis

@router.delete("/{analysis_id}")
async def delete_analysis(
    analysis_id: str,
    db: Session = Depends(get_db)
):
    """Supprimer une analyse"""
    analysis_service = AnalysisService(db)
    success = analysis_service.delete_analysis(analysis_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Analyse non trouvée")
    
    return {"message": "Analyse supprimée avec succès"}

@router.get("/", response_model=List[AnalysisResponse])
async def list_analyses(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lister les analyses d'un utilisateur"""
    analysis_service = AnalysisService(db)
    analyses = analysis_service.list_analyses(
        user_id="temp-user-id",  # À remplacer par l'utilisateur authentifié
        skip=skip,
        limit=limit,
        status=status
    )
    
    return analyses 