from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from ..agent.trend_analyzer import TrendAnalyzer
from ..agent.sentiment_analyzer import SentimentAnalyzer

app = FastAPI(title="Crypto Trend AI Agent")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzers
trend_analyzer = TrendAnalyzer()
sentiment_analyzer = SentimentAnalyzer()

class TrendRequest(BaseModel):
    hours_back: int = 24
    keywords: List[str] = None

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/analyze/trends")
async def analyze_trends(request: TrendRequest):
    try:
        if request.keywords:
            trend_analyzer.tracked_keywords = request.keywords
        
        trends = trend_analyzer.analyze_social_trends(hours_back=request.hours_back)
        return {"trends": trends}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trending/topics")
async def get_trending_topics():
    try:
        trends = trend_analyzer.analyze_social_trends()
        # Sort topics by mention count
        sorted_trends = sorted(
            trends.items(),
            key=lambda x: x[1]['mention_count'] if x[1] else 0,
            reverse=True
        )
        return {"trending_topics": sorted_trends[:5]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 