from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import uuid

from app.services.suggestion_service import SuggestionService

class ExportService:
    def __init__(self, db: Session):
        self.db = db
        self.export_tasks = {}  # Stockage temporaire des tâches d'export
    
    def export_to_google_sheets(
        self,
        analysis_id: str,
        sheet_name: str,
        include_columns: List[str] = None,
        filters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Exporter vers Google Sheets"""
        task_id = str(uuid.uuid4())
        
        # Initialiser le statut de la tâche
        self.export_tasks[task_id] = {
            "status": "processing",
            "progress": 0,
            "message": "Début de l'export..."
        }
        
        try:
            # Récupérer les suggestions
            suggestion_service = SuggestionService(self.db)
            suggestions_result = suggestion_service.list_suggestions(
                analysis_id=analysis_id,
                filters=filters
            )
            
            self.export_tasks[task_id]["progress"] = 30
            self.export_tasks[task_id]["message"] = "Suggestions récupérées, préparation des données..."
            
            # Préparer les données
            data_to_export = []
            for suggestion in suggestions_result["suggestions"]:
                row = {}
                if "source_page" in include_columns:
                    row["Page Source"] = suggestion.source_page
                if "target_page" in include_columns:
                    row["Page Cible"] = suggestion.target_page
                if "anchor_text" in include_columns:
                    row["Ancre"] = suggestion.anchor_text
                if "score" in include_columns:
                    row["Score"] = suggestion.score
                if "status" in include_columns:
                    row["Statut"] = suggestion.status
                if "reasoning" in include_columns:
                    row["Raisonnement"] = suggestion.reasoning
                if "created_at" in include_columns:
                    row["Date de création"] = suggestion.created_at.strftime("%Y-%m-%d %H:%M:%S")
                
                data_to_export.append(row)
            
            self.export_tasks[task_id]["progress"] = 60
            self.export_tasks[task_id]["message"] = "Données préparées, export vers Google Sheets..."
            
            # Exporter vers Google Sheets
            sheet_url = self._export_to_google_sheets(sheet_name, data_to_export)
            
            self.export_tasks[task_id]["progress"] = 100
            self.export_tasks[task_id]["status"] = "completed"
            self.export_tasks[task_id]["message"] = "Export terminé avec succès"
            self.export_tasks[task_id]["sheet_url"] = sheet_url
            self.export_tasks[task_id]["exported_rows"] = len(data_to_export)
            
            return {
                "task_id": task_id,
                "status": "completed",
                "sheet_url": sheet_url,
                "exported_rows": len(data_to_export)
            }
            
        except Exception as e:
            self.export_tasks[task_id]["status"] = "failed"
            self.export_tasks[task_id]["message"] = f"Erreur lors de l'export: {str(e)}"
            
            return {
                "task_id": task_id,
                "status": "failed",
                "error": str(e)
            }
    
    def _export_to_google_sheets(self, sheet_name: str, data: List[Dict[str, Any]]) -> str:
        """Exporter les données vers Google Sheets"""
        try:
            # Configuration des credentials Google Sheets
            # En production, utiliser un fichier de credentials
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Ici on utiliserait les credentials configurés
            # credentials = Credentials.from_service_account_file(
            #     'path/to/credentials.json', scopes=scopes
            # )
            # gc = gspread.authorize(credentials)
            
            # Pour l'instant, simuler l'export
            print(f"Export vers Google Sheets: {sheet_name}")
            print(f"Données: {len(data)} lignes")
            
            # Retourner une URL simulée
            return f"https://docs.google.com/spreadsheets/d/simulated_sheet_id/edit"
            
        except Exception as e:
            raise Exception(f"Erreur lors de l'export Google Sheets: {str(e)}")
    
    def get_export_status(self, task_id: str) -> Dict[str, Any]:
        """Récupérer le statut d'une tâche d'export"""
        task = self.export_tasks.get(task_id)
        if not task:
            return {
                "status": "not_found",
                "message": "Tâche non trouvée"
            }
        
        return task
    
    def export_to_csv(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Exporter vers CSV"""
        try:
            df = pd.DataFrame(data)
            csv_content = df.to_csv(index=False, encoding='utf-8-sig')
            
            # En production, sauvegarder le fichier
            # with open(filename, 'w', encoding='utf-8-sig') as f:
            #     f.write(csv_content)
            
            return csv_content
            
        except Exception as e:
            raise Exception(f"Erreur lors de l'export CSV: {str(e)}")
    
    def export_to_excel(self, data: List[Dict[str, Any]], filename: str) -> bytes:
        """Exporter vers Excel"""
        try:
            df = pd.DataFrame(data)
            
            # Créer un buffer pour le fichier Excel
            import io
            output = io.BytesIO()
            
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Suggestions', index=False)
                
                # Ajouter un onglet avec les statistiques
                stats_data = {
                    "Statistique": ["Total", "En attente", "Approuvé", "Rejeté"],
                    "Valeur": [
                        len(data),
                        len([row for row in data if row.get("Statut") == "pending"]),
                        len([row for row in data if row.get("Statut") == "approved"]),
                        len([row for row in data if row.get("Statut") == "rejected"])
                    ]
                }
                stats_df = pd.DataFrame(stats_data)
                stats_df.to_excel(writer, sheet_name='Statistiques', index=False)
            
            return output.getvalue()
            
        except Exception as e:
            raise Exception(f"Erreur lors de l'export Excel: {str(e)}")
    
    def export_to_json(self, data: List[Dict[str, Any]], analysis_id: str) -> str:
        """Exporter vers JSON"""
        try:
            import json
            
            export_data = {
                "analysis_id": analysis_id,
                "export_date": datetime.now().isoformat(),
                "total_suggestions": len(data),
                "suggestions": data
            }
            
            return json.dumps(export_data, indent=2, ensure_ascii=False)
            
        except Exception as e:
            raise Exception(f"Erreur lors de l'export JSON: {str(e)}")
    
    def cleanup_old_tasks(self, max_age_hours: int = 24):
        """Nettoyer les anciennes tâches d'export"""
        current_time = datetime.now()
        
        tasks_to_remove = []
        for task_id, task_data in self.export_tasks.items():
            if "created_at" in task_data:
                task_age = current_time - task_data["created_at"]
                if task_age.total_seconds() > max_age_hours * 3600:
                    tasks_to_remove.append(task_id)
        
        for task_id in tasks_to_remove:
            del self.export_tasks[task_id] 