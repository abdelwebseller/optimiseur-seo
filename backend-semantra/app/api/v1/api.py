from fastapi import APIRouter
from app.api.v1.endpoints import analysis, suggestions, auth, settings, export

api_router = APIRouter()

# Inclure tous les endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(analysis.router, prefix="/analyze", tags=["analysis"])
api_router.include_router(suggestions.router, prefix="/suggestions", tags=["suggestions"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
api_router.include_router(export.router, prefix="/export", tags=["export"]) 