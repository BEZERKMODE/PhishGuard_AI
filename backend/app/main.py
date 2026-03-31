from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.app.schemas import PredictRequest, BatchPredictRequest
from backend.app.predictor import Predictor

app = FastAPI(
    title="PhishGuard AI API",
    description="Phishing URL detection API with risk scoring and explanations",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor = None


@app.on_event("startup")
def startup_event():
    global predictor
    predictor = Predictor()


@app.get("/health")
def health():
    return {"status": "ok", "service": "PhishGuard AI API"}


@app.post("/predict")
def predict(payload: PredictRequest):
    try:
        result = predictor.predict_one(payload.url)
        return {k: v for k, v in result.items() if k != "features"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/predict/batch")
def predict_batch(payload: BatchPredictRequest):
    try:
        results = predictor.predict_batch(payload.urls)
        return {"results": [{k: v for k, v in r.items() if k != "features"} for r in results]}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/features")
def feature_preview(url: str):
    try:
        result = predictor.predict_one(url)
        return {
            "url": url,
            "prediction": result["prediction"],
            "phishing_probability": result["phishing_probability"],
            "risk_score": result["risk_score"],
            "features": result["features"],
            "reasons": result["reasons"],
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
