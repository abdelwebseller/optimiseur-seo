from celery import current_task
from app.core.celery_app import celery_app
from app.services.analysis_service import AnalysisService
from app.services.crawl_service import CrawlService
from app.services.ai_service import AIService
from app.core.database import SessionLocal
from typing import Dict, Any, List
import asyncio
from app.services.suggestion_service import SuggestionService

@celery_app.task(bind=True)
def start_analysis_task(
    self,
    analysis_id: str,
    sitemap_url: str,
    crawl_settings: Dict[str, Any] = None,
    ai_settings: Dict[str, Any] = None
):
    """Tâche principale pour démarrer une analyse SEO"""
    try:
        # Initialiser les services
        db = SessionLocal()
        analysis_service = AnalysisService(db)
        
        # Mettre à jour le statut
        analysis_service.update_analysis(
            analysis_id,
            {"status": "processing", "started_at": "now"}
        )
        
        # Lancer l'analyse asynchrone
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                _run_analysis_async(
                    analysis_id,
                    sitemap_url,
                    crawl_settings,
                    ai_settings
                )
            )
            
            # Marquer comme terminé
            analysis_service.complete_analysis(
                analysis_id,
                statistics=result.get("statistics", {})
            )
            
            return {
                "status": "success",
                "analysis_id": analysis_id,
                "statistics": result.get("statistics", {})
            }
            
        finally:
            loop.close()
            
    except Exception as e:
        # Marquer comme échoué
        analysis_service.fail_analysis(analysis_id, str(e))
        
        return {
            "status": "error",
            "analysis_id": analysis_id,
            "error": str(e)
        }
    finally:
        db.close()

async def _run_analysis_async(
    analysis_id: str,
    sitemap_url: str,
    crawl_settings: Dict[str, Any] = None,
    ai_settings: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Exécuter l'analyse de manière asynchrone"""
    
    # Initialiser les services
    db = SessionLocal()
    analysis_service = AnalysisService(db)
    ai_service = AIService()
    
    try:
        # Étape 1: Crawler le sitemap
        async with CrawlService() as crawl_service:
            urls = await crawl_service.crawl_sitemap(
                sitemap_url,
                analysis_id,
                crawl_settings
            )
            
            # Mettre à jour la progression
            analysis_service.update_analysis_progress(
                analysis_id,
                progress=10,
                crawled_urls=0,
                failed_urls=0
            )
            
            # Étape 2: Crawler les pages
            crawled_pages = await crawl_service.crawl_pages(
                urls,
                analysis_id,
                crawl_settings
            )
            
            # Mettre à jour la progression
            analysis_service.update_analysis_progress(
                analysis_id,
                progress=50,
                crawled_urls=len(crawled_pages),
                failed_urls=len(urls) - len(crawled_pages)
            )
        
        # Étape 3: Générer les embeddings
        embeddings = await ai_service.generate_embeddings(
            crawled_pages,
            ai_settings.get("embedding_model", "text-embedding-3-large")
        )
        
        # Mettre à jour la progression
        analysis_service.update_analysis_progress(
            analysis_id,
            progress=70
        )
        
        # Étape 4: Analyser les similarités et générer les suggestions
        suggestions = await ai_service.analyze_similarities(
            crawled_pages,
            embeddings,
            ai_settings
        )
        
        # Étape 5: Sauvegarder les suggestions
        suggestion_service = SuggestionService(db)
        for suggestion_data in suggestions:
            suggestion_service.create_suggestion(suggestion_data)
        
        # Mettre à jour la progression finale
        analysis_service.update_analysis_progress(
            analysis_id,
            progress=100
        )
        
        # Calculer les statistiques
        statistics = {
            "total_pages": len(crawled_pages),
            "total_suggestions": len(suggestions),
            "success_rate": len(crawled_pages) / len(urls) if urls else 0,
            "processing_time": "completed"
        }
        
        return {
            "statistics": statistics,
            "suggestions_count": len(suggestions)
        }
        
    finally:
        db.close()

@celery_app.task
def update_analysis_progress(
    analysis_id: str,
    progress: int,
    crawled_urls: int = None,
    failed_urls: int = None
):
    """Mettre à jour la progression d'une analyse"""
    try:
        db = SessionLocal()
        analysis_service = AnalysisService(db)
        
        analysis_service.update_analysis_progress(
            analysis_id,
            progress,
            crawled_urls,
            failed_urls
        )
        
        return {"status": "success", "progress": progress}
        
    except Exception as e:
        return {"status": "error", "error": str(e)}
    finally:
        db.close()

@celery_app.task
def cancel_analysis_task(analysis_id: str):
    """Annuler une analyse en cours"""
    try:
        db = SessionLocal()
        analysis_service = AnalysisService(db)
        
        # Marquer comme annulé
        analysis_service.update_analysis(
            analysis_id,
            {"status": "cancelled"}
        )
        
        return {"status": "success", "message": "Analyse annulée"}
        
    except Exception as e:
        return {"status": "error", "error": str(e)}
    finally:
        db.close() 