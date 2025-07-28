from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import pandas as pd
import json
from datetime import datetime

from app.core.database import get_db
from app.services.export_service import ExportService
from app.services.suggestion_service import SuggestionService

router = APIRouter()

@router.post("/csv")
async def export_csv(
    analysis_id: str,
    filters: Dict[str, Any] = None,
    db: Session = Depends(get_db)
):
    """Exporter les suggestions en CSV"""
    try:
        export_service = ExportService(db)
        suggestion_service = SuggestionService(db)
        
        # Récupérer les suggestions
        suggestions_result = suggestion_service.list_suggestions(
            analysis_id=analysis_id,
            filters=filters
        )
        
        # Créer le DataFrame
        suggestions_data = []
        for suggestion in suggestions_result["suggestions"]:
            suggestions_data.append({
                "ID": suggestion.id,
                "Page Source": suggestion.source_page,
                "Page Cible": suggestion.target_page,
                "Ancre": suggestion.anchor_text,
                "Score": suggestion.score,
                "Statut": suggestion.status,
                "Raisonnement": suggestion.reasoning,
                "Date de création": suggestion.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        df = pd.DataFrame(suggestions_data)
        
        # Générer le fichier CSV
        filename = f"semantra_suggestions_{analysis_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        csv_content = df.to_csv(index=False, encoding='utf-8-sig')
        
        return {
            "filename": filename,
            "content": csv_content,
            "total_suggestions": len(suggestions_data),
            "export_format": "csv"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'export CSV: {str(e)}")

@router.post("/json")
async def export_json(
    analysis_id: str,
    filters: Dict[str, Any] = None,
    db: Session = Depends(get_db)
):
    """Exporter les suggestions en JSON"""
    try:
        suggestion_service = SuggestionService(db)
        
        # Récupérer les suggestions
        suggestions_result = suggestion_service.list_suggestions(
            analysis_id=analysis_id,
            filters=filters
        )
        
        # Préparer les données
        export_data = {
            "analysis_id": analysis_id,
            "export_date": datetime.now().isoformat(),
            "total_suggestions": suggestions_result["total"],
            "suggestions": []
        }
        
        for suggestion in suggestions_result["suggestions"]:
            export_data["suggestions"].append({
                "id": suggestion.id,
                "source_page": suggestion.source_page,
                "target_page": suggestion.target_page,
                "anchor_text": suggestion.anchor_text,
                "score": suggestion.score,
                "status": suggestion.status,
                "reasoning": suggestion.reasoning,
                "created_at": suggestion.created_at.isoformat(),
                "metadata": suggestion.metadata
            })
        
        filename = f"semantra_suggestions_{analysis_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        return {
            "filename": filename,
            "content": json.dumps(export_data, indent=2, ensure_ascii=False),
            "total_suggestions": len(export_data["suggestions"]),
            "export_format": "json"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'export JSON: {str(e)}")

@router.post("/google-sheets")
async def export_google_sheets(
    analysis_id: str,
    sheet_name: str = None,
    include_columns: List[str] = None,
    filters: Dict[str, Any] = None,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Exporter vers Google Sheets"""
    try:
        export_service = ExportService(db)
        
        # Lancer l'export en arrière-plan
        background_tasks.add_task(
            export_service.export_to_google_sheets,
            analysis_id=analysis_id,
            sheet_name=sheet_name or f"Semantra_Analysis_{analysis_id}",
            include_columns=include_columns or ["source_page", "target_page", "anchor_text", "score", "status"],
            filters=filters
        )
        
        return {
            "message": "Export vers Google Sheets lancé en arrière-plan",
            "analysis_id": analysis_id,
            "sheet_name": sheet_name or f"Semantra_Analysis_{analysis_id}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'export Google Sheets: {str(e)}")

@router.get("/google-sheets/status/{task_id}")
async def get_google_sheets_export_status(
    task_id: str,
    db: Session = Depends(get_db)
):
    """Récupérer le statut d'un export Google Sheets"""
    try:
        export_service = ExportService(db)
        status = export_service.get_export_status(task_id)
        
        return status
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération du statut: {str(e)}")

@router.post("/excel")
async def export_excel(
    analysis_id: str,
    filters: Dict[str, Any] = None,
    db: Session = Depends(get_db)
):
    """Exporter les suggestions en Excel"""
    try:
        export_service = ExportService(db)
        suggestion_service = SuggestionService(db)
        
        # Récupérer les suggestions
        suggestions_result = suggestion_service.list_suggestions(
            analysis_id=analysis_id,
            filters=filters
        )
        
        # Créer le DataFrame
        suggestions_data = []
        for suggestion in suggestions_result["suggestions"]:
            suggestions_data.append({
                "ID": suggestion.id,
                "Page Source": suggestion.source_page,
                "Page Cible": suggestion.target_page,
                "Ancre": suggestion.anchor_text,
                "Score": suggestion.score,
                "Statut": suggestion.status,
                "Raisonnement": suggestion.reasoning,
                "Date de création": suggestion.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        df = pd.DataFrame(suggestions_data)
        
        # Générer le fichier Excel
        filename = f"semantra_suggestions_{analysis_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        # Créer un buffer pour le fichier Excel
        import io
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Suggestions', index=False)
            
            # Ajouter un onglet avec les statistiques
            stats_data = {
                "Statistique": ["Total", "En attente", "Approuvé", "Rejeté", "Score moyen"],
                "Valeur": [
                    suggestions_result["total"],
                    len([s for s in suggestions_result["suggestions"] if s.status == "pending"]),
                    len([s for s in suggestions_result["suggestions"] if s.status == "approved"]),
                    len([s for s in suggestions_result["suggestions"] if s.status == "rejected"]),
                    sum(s.score for s in suggestions_result["suggestions"]) / len(suggestions_result["suggestions"]) if suggestions_result["suggestions"] else 0
                ]
            }
            stats_df = pd.DataFrame(stats_data)
            stats_df.to_excel(writer, sheet_name='Statistiques', index=False)
        
        excel_content = output.getvalue()
        
        return {
            "filename": filename,
            "content": excel_content,
            "total_suggestions": len(suggestions_data),
            "export_format": "excel"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'export Excel: {str(e)}") 