import json
import httpx
import certifi
from fastapi import HTTPException, status
from app.database.session import settings

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def build_prompt(record: dict) -> str:
    """Build a structured prompt from the ML prediction record."""
    risk_factors = "\n".join(f"  - {f}" for f in record["top_risk_factors"])

    return f"""You are a business analyst specialising in customer retention.
A machine learning model has generated the following churn prediction for a customer.

--- Customer Profile ---
Customer ID      : {record["customer_id"]}
Customer Segment : {record["customer_segment"]}
Churn Probability: {round(record["churn_probability"] * 100, 1)}%
Risk Level       : {record["risk_level"].upper()}
Prediction Date  : {record["prediction_date"]}
Model Version    : {record["model_version"]}

--- Top Risk Factors (from feature importance) ---
{risk_factors}

--- Suggested Action (rule-based) ---
{record["recommended_action"]}

Based only on the data provided above, respond in the following JSON format with no extra text:

{{
  "summary": "A 2-3 sentence summary of this customer's churn risk situation.",
  "key_insights": [
    "Insight 1 based on the risk factors",
    "Insight 2 based on the risk factors",
    "Insight 3 based on the risk factors"
  ],
  "recommendations": [
    "Specific actionable recommendation 1",
    "Specific actionable recommendation 2",
    "Specific actionable recommendation 3"
  ],
  "limitations": [
    "A limitation or caveat about this prediction"
  ]
}}"""


def parse_ai_response(content: str) -> dict:
    """Parse and validate the AI response JSON. Strips markdown fences if present."""
    content = content.strip()
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    content = content.strip()

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI returned a response that could not be parsed as JSON.",
        )

    required_keys = {"summary", "key_insights", "recommendations", "limitations"}
    missing = required_keys - parsed.keys()
    if missing:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI response is missing required fields: {missing}",
        )

    return parsed


async def call_openrouter(prompt: str) -> dict:
    """Send the prompt to OpenRouter and return the parsed AI response."""
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": settings.OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
    }

    try:
        # verify=False needed for local dev on Windows where SSL cert chain may not be trusted
        async with httpx.AsyncClient(timeout=30.0, verify=False) as client:
            response = await client.post(OPENROUTER_URL, headers=headers, json=payload)
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="OpenRouter API request timed out.",
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to reach OpenRouter API: {str(e)}",
        )

    if response.status_code == 401:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid OpenRouter API key.",
        )
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"OpenRouter API returned error {response.status_code}.",
        )

    content = response.json()["choices"][0]["message"]["content"]
    return parse_ai_response(content)
