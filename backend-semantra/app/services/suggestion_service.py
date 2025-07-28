from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, or_
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from app.models.suggestion import Suggestion
from app.models.anchor_optimization import AnchorOptimization
from app.schemas.suggestion import SuggestionCreate, SuggestionUpdate, SuggestionFilter

class SuggestionService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_suggestion(self, suggestion_data: SuggestionCreate) -> Suggestion:
        """Créer une nouvelle suggestion"""
        suggestion = Suggestion(
            id=str(uuid.uuid4()),
            analysis_id=suggestion_data.analysis_id,
            source_page=suggestion_data.source_page,
            target_page=suggestion_data.target_page,
            anchor_text=suggestion_data.anchor_text,
            score=suggestion_data.score,
            reasoning=suggestion_data.reasoning,
            metadata=suggestion_data.metadata or {}
        )
        
        self.db.add(suggestion)
        self.db.commit()
        self.db.refresh(suggestion)
        
        return suggestion
    
    def get_suggestion(self, suggestion_id: str) -> Optional[Suggestion]:
        """Récupérer une suggestion par son ID"""
        return self.db.query(Suggestion).filter(Suggestion.id == suggestion_id).first()
    
    def update_suggestion(
        self,
        suggestion_id: str,
        suggestion_update: SuggestionUpdate
    ) -> Optional[Suggestion]:
        """Mettre à jour une suggestion"""
        suggestion = self.get_suggestion(suggestion_id)
        if not suggestion:
            return None
        
        update_data = suggestion_update.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(suggestion, field, value)
        
        suggestion.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(suggestion)
        
        return suggestion
    
    def delete_suggestion(self, suggestion_id: str) -> bool:
        """Supprimer une suggestion"""
        suggestion = self.get_suggestion(suggestion_id)
        if not suggestion:
            return False
        
        self.db.delete(suggestion)
        self.db.commit()
        
        return True
    
    def list_suggestions(
        self,
        analysis_id: Optional[str] = None,
        filters: SuggestionFilter = None
    ) -> Dict[str, Any]:
        """Lister les suggestions avec filtres"""
        query = self.db.query(Suggestion)
        
        # Filtrer par analyse
        if analysis_id:
            query = query.filter(Suggestion.analysis_id == analysis_id)
        
        # Appliquer les filtres
        if filters:
            if filters.status:
                query = query.filter(Suggestion.status == filters.status)
            
            if filters.min_score is not None:
                query = query.filter(Suggestion.score >= filters.min_score)
            
            if filters.max_score is not None:
                query = query.filter(Suggestion.score <= filters.max_score)
            
            if filters.search_term:
                search_term = f"%{filters.search_term}%"
                query = query.filter(
                    or_(
                        Suggestion.anchor_text.ilike(search_term),
                        Suggestion.source_page.ilike(search_term),
                        Suggestion.target_page.ilike(search_term)
                    )
                )
        
        # Compter le total
        total = query.count()
        
        # Pagination
        if filters:
            query = query.offset(filters.offset).limit(filters.limit)
        
        # Tri par score décroissant
        suggestions = query.order_by(desc(Suggestion.score)).all()
        
        return {
            "suggestions": suggestions,
            "total": total,
            "limit": filters.limit if filters else 100,
            "offset": filters.offset if filters else 0,
            "has_more": total > (filters.offset + filters.limit) if filters else False
        }
    
    def batch_update_status(
        self,
        suggestion_ids: List[str],
        status: str
    ) -> int:
        """Mettre à jour le statut de plusieurs suggestions"""
        updated_count = self.db.query(Suggestion).filter(
            Suggestion.id.in_(suggestion_ids)
        ).update(
            {"status": status, "updated_at": datetime.utcnow()},
            synchronize_session=False
        )
        
        self.db.commit()
        return updated_count
    
    def save_anchor_optimization(
        self,
        suggestion_id: str,
        original_anchor: str,
        optimized_anchor: str,
        provider: str,
        model: str,
        confidence_score: float,
        alternatives: List[str] = None
    ) -> AnchorOptimization:
        """Sauvegarder une optimisation d'ancre"""
        optimization = AnchorOptimization(
            id=str(uuid.uuid4()),
            suggestion_id=suggestion_id,
            original_anchor=original_anchor,
            optimized_anchor=optimized_anchor,
            provider=provider,
            model=model,
            confidence_score=confidence_score,
            alternatives=alternatives or [],
            parameters={}
        )
        
        self.db.add(optimization)
        self.db.commit()
        self.db.refresh(optimization)
        
        return optimization
    
    def get_suggestions_by_score_range(
        self,
        min_score: float = 0.0,
        max_score: float = 1.0,
        limit: int = 100
    ) -> List[Suggestion]:
        """Récupérer les suggestions par plage de score"""
        return self.db.query(Suggestion).filter(
            and_(
                Suggestion.score >= min_score,
                Suggestion.score <= max_score
            )
        ).order_by(desc(Suggestion.score)).limit(limit).all()
    
    def get_suggestions_by_status(
        self,
        status: str,
        limit: int = 100
    ) -> List[Suggestion]:
        """Récupérer les suggestions par statut"""
        return self.db.query(Suggestion).filter(
            Suggestion.status == status
        ).order_by(desc(Suggestion.created_at)).limit(limit).all()
    
    def get_suggestions_statistics(self, analysis_id: Optional[str] = None) -> Dict[str, Any]:
        """Récupérer les statistiques des suggestions"""
        query = self.db.query(Suggestion)
        
        if analysis_id:
            query = query.filter(Suggestion.analysis_id == analysis_id)
        
        total = query.count()
        pending = query.filter(Suggestion.status == "pending").count()
        approved = query.filter(Suggestion.status == "approved").count()
        rejected = query.filter(Suggestion.status == "rejected").count()
        
        # Score moyen
        avg_score = self.db.query(Suggestion.score).filter(
            Suggestion.analysis_id == analysis_id
        ).scalar() if analysis_id else 0.0
        
        return {
            "total": total,
            "pending": pending,
            "approved": approved,
            "rejected": rejected,
            "average_score": float(avg_score) if avg_score else 0.0
        } 