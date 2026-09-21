import json
import os
from fastapi import HTTPException, status
from app.ai.service import build_prompt, call_openrouter

ML_OUTPUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "data", "ml_output.json"
)


def load_ml_record(customer_id: int) -> dict:
    """Load the ML prediction record for a given customer_id from ml_output.json."""
    try:
        with open(ML_OUTPUT_PATH, "r") as f:
            ml_output = json.load(f)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ML output dataset not found. Run model_training.ipynb first.",
        )

    record = next((r for r in ml_output if r["customer_id"] == customer_id), None)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No ML prediction found for customer_id {customer_id}.",
        )
    return record


async def get_ai_insight(customer_id: int) -> dict:
    """
    Business logic:
    1. Load ML prediction record for the customer
    2. Build a structured prompt
    3. Call OpenRouter
    4. Return structured insight response
    """
    record = load_ml_record(customer_id)
    prompt = build_prompt(record)
    ai_data = await call_openrouter(prompt)

    return {
        "customer_id":       customer_id,
        "risk_level":        record["risk_level"],
        "churn_probability": record["churn_probability"],
        "customer_segment":  record["customer_segment"],
        "insight":           ai_data["summary"],
        "key_insights":      ai_data["key_insights"],
        "recommendations":   ai_data["recommendations"],
        "limitations":       ai_data["limitations"],
        "model_version":     record["model_version"],
        "prediction_date":   record["prediction_date"],
    }
