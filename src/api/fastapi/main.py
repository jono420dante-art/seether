from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
from src.automation.bots.pricing_bot import PricingBot
from src.automation.youtube.trend_detector import TrendDetector

app = FastAPI(
    title="Transparent Programs & Design API",
    description="AI-first automation engines for e-com/SaaS/dropshipping",
    version="1.0.0"
)

# Zero-trust security middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://jono-tower.fyi"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"]
)

# Initialize bots
pricing_bot = PricingBot()
trend_detector = TrendDetector()

class PricingRequest(BaseModel):
    product_id: str
    base_cost: float
    is_integrity: bool = False

class TrendRequest(BaseModel):
    video_id: str
    current_views: int
    previous_views: int
    current_engagement: float
    previous_engagement: float
    negative_sentiment_score: float = 0.0
    views_24h: int = 0

@app.get("/health")
async def health_check():
    return {"status": "operational", "version": "1.0.0"}

@app.post("/api/pricing")
async def get_optimal_pricing(request: PricingRequest):
    try:
        price = await pricing_bot.calculate_optimal_price(
            request.product_id,
            request.base_cost,
            request.is_integrity
        )
        return {"product_id": request.product_id, "optimal_price": price}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/trends")
async def detect_video_trends(request: TrendRequest):
    try:
        analysis = await trend_detector.detect_spike(
            video_id=request.video_id,
            current_views=request.current_views,
            previous_views=request.previous_views,
            current_engagement=request.current_engagement,
            previous_engagement=request.previous_engagement,
            negative_sentiment_score=request.negative_sentiment_score,
            views_24h=request.views_24h
        )
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
