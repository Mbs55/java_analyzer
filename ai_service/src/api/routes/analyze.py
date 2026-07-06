from fastapi import APIRouter,Depends
from src.api.schemas.analyze import AnalyzeResponse,AnalyzeRequest
from  src.infrastructure.models.OllamaService import model
from src.api.dependencies.model import get_model
router=APIRouter(prefix="/AIService",tags=["AIService"])
llm=model()
@router.post("/analyze",response_model=AnalyzeResponse)
async def analyze(method:AnalyzeRequest,llm:model=Depends(get_model))->AnalyzeResponse:
    response=llm.prompt(method)
    return response






