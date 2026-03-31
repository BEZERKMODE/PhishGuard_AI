from pydantic import BaseModel, Field, HttpUrl
from typing import List


class PredictRequest(BaseModel):
    url: str = Field(..., examples=["http://paypal-login-security-alert-example.com"])


class BatchPredictRequest(BaseModel):
    urls: List[str] = Field(..., min_length=1)


class PredictResponse(BaseModel):
    url: str
    prediction: str
    phishing_probability: float
    risk_score: int
    reasons: List[str]
