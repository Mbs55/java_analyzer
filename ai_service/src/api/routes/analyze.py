from fastapi import APIRouter
from src.api.schemas.analyze import AnalyzeResponse
router=APIRouter(prefix="AIService",tags=["AIService"])
@router.post("analyze",response_model=AnalyzeResponse)