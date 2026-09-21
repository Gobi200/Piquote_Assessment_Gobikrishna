from pydantic import BaseModel


class AIInsightRequest(BaseModel):
    customer_id: int


class AIInsightResponse(BaseModel):
    model_config = {"protected_namespaces": ()}

    customer_id: int
    risk_level: str
    churn_probability: float
    customer_segment: str
    insight: str
    key_insights: list[str]
    recommendations: list[str]
    limitations: list[str]
    model_version: str
    prediction_date: str
