from pydantic import BaseModel


class FraudResult(BaseModel):
    fraud_score: float
    category: str
    explanation: str
    ela_score: float
    latency_ms: float
    category_breakdown: dict


class ErrorResult(BaseModel):
    error: str
    message: str