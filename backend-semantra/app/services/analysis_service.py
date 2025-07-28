from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from app.models.analysis import Analysis
from app.schemas.analysis import AnalysisCreate, AnalysisUpdate

class AnalysisService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_analysis(
        self,
        user_id: str,
        sitemap_url: str,
        crawl_settings: Dict[str, Any] = None,
        ai_settings: Dict[str, Any] = None
    ) -> Analysis:
        """Créer une nouvelle analyse"""
        analysis = Analysis(
            id=str(uuid.uuid4()),
            user_id=user_id,
            sitemap_url=sitemap_url,
            status="pending",
            progress=0,
            crawl_settings=crawl_settings or {},
            ai_settings=ai_settings or {},
            statistics={}
        )
        
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)
        
        return analysis
    
    def get_analysis(self, analysis_id: str) -> Optional[Analysis]:
        """Récupérer une analyse par son ID"""
        return self.db.query(Analysis).filter(Analysis.id == analysis_id).first()
    
    def update_analysis(
        self,
        analysis_id: str,
        analysis_update: AnalysisUpdate
    ) -> Optional[Analysis]:
        """Mettre à jour une analyse"""
        analysis = self.get_analysis(analysis_id)
        if not analysis:
            return None
        
        update_data = analysis_update.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            if field == "started_at" and value:
                setattr(analysis, field, datetime.fromisoformat(value))
            elif field == "completed_at" and value:
                setattr(analysis, field, datetime.fromisoformat(value))
            else:
                setattr(analysis, field, value)
        
        self.db.commit()
        self.db.refresh(analysis)
        
        return analysis
    
    def delete_analysis(self, analysis_id: str) -> bool:
        """Supprimer une analyse"""
        analysis = self.get_analysis(analysis_id)
        if not analysis:
            return False
        
        self.db.delete(analysis)
        self.db.commit()
        
        return True
    
    def list_analyses(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[Analysis]:
        """Lister les analyses d'un utilisateur"""
        query = self.db.query(Analysis).filter(Analysis.user_id == user_id)
        
        if status:
            query = query.filter(Analysis.status == status)
        
        return query.order_by(desc(Analysis.created_at)).offset(skip).limit(limit).all()
    
    def get_suggestions_for_analysis(self, analysis_id: str) -> List[Dict[str, Any]]:
        """Récupérer les suggestions pour une analyse"""
        from app.models.suggestion import Suggestion
        
        suggestions = self.db.query(Suggestion).filter(
            Suggestion.analysis_id == analysis_id
        ).all()
        
        return [suggestion.__dict__ for suggestion in suggestions]
    
    def update_analysis_progress(
        self,
        analysis_id: str,
        progress: int,
        crawled_urls: int = None,
        failed_urls: int = None
    ) -> bool:
        """Mettre à jour la progression d'une analyse"""
        analysis = self.get_analysis(analysis_id)
        if not analysis:
            return False
        
        analysis.progress = progress
        if crawled_urls is not None:
            analysis.crawled_urls = crawled_urls
        if failed_urls is not None:
            analysis.failed_urls = failed_urls
        
        self.db.commit()
        return True
    
    def complete_analysis(
        self,
        analysis_id: str,
        statistics: Dict[str, Any] = None
    ) -> bool:
        """Marquer une analyse comme terminée"""
        analysis = self.get_analysis(analysis_id)
        if not analysis:
            return False
        
        analysis.status = "completed"
        analysis.progress = 100
        analysis.completed_at = datetime.utcnow()
        
        if statistics:
            analysis.statistics = statistics
        
        self.db.commit()
        return True
    
    def fail_analysis(
        self,
        analysis_id: str,
        error_message: str = None
    ) -> bool:
        """Marquer une analyse comme échouée"""
        analysis = self.get_analysis(analysis_id)
        if not analysis:
            return False
        
        analysis.status = "failed"
        analysis.completed_at = datetime.utcnow()
        
        if error_message:
            analysis.statistics = {"error": error_message}
        
        self.db.commit()
        return True 