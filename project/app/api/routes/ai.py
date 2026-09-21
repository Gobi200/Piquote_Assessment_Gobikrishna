from fastapi import APIRouter
from app.schemas.ai import AIInsightRequest, AIInsightResponse
from app.services.ai_service import get_ai_insight

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/insights", response_model=AIInsightResponse)
async def ai_insights(request: AIInsightRequest):
    return await get_ai_insight(request.customer_id)
