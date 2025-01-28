from fastapi import APIRouter, Depends, HTTPException, Security
from pydantic import BaseModel
from typing import List, Dict
from loguru import logger
from fastapi.security.api_key import APIKeyHeader

from ..services import (
    BlockchainService,
    TwitterService,
    NFTTracker,
    DeFiEducator,
    AstroportTracker,
    ServiceManager
)
from ..schemas.responses import (
    NetworkStatus,
    SocialMetrics,
    ContentResponse,
    AnalyticsResponse
)

router = APIRouter()
service_manager = ServiceManager()
api_key_header = APIKeyHeader(name="X-API-KEY")

class ChatMessage(BaseModel):
    message: str

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != "expected_api_key":
        raise HTTPException(status_code=403, detail="Could not validate credentials")

@router.post("/chat")
async def chat_endpoint(message: ChatMessage):
    """Chat endpoint with enhanced responses"""
    try:
        response = await service_manager.content_generator.generate_chat_response(
            message.message
        )
        return {
            "response": response['response'],
            "suggested_actions": response.get('follow_up', []),
            "data": response.get('data', {})
        }
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Chat processing failed")

@router.get("/blockchain/status")
async def get_blockchain_status(
    blockchain: BlockchainService = Depends(lambda: BlockchainService())
) -> Dict:
    """Get blockchain connection status."""
    status = await blockchain.verify_connection()
    return {"connected": status}

@router.get("/nft/{collection_address}/stats")
async def get_nft_stats(
    collection_address: str,
    blockchain: BlockchainService = Depends(lambda: BlockchainService()),
    nft_tracker: NFTTracker = Depends(lambda: NFTTracker(blockchain))
) -> Dict:
    """Get NFT collection statistics."""
    stats = await nft_tracker.get_collection_stats(collection_address)
    if not stats:
        raise HTTPException(status_code=404, detail="Collection not found")
    return stats

@router.post("/defi/educate/{topic}")
async def create_educational_content(
    topic: str,
    twitter: TwitterService = Depends(lambda: TwitterService()),
    educator: DeFiEducator = Depends(lambda: DeFiEducator(twitter))
) -> Dict:
    """Create and post educational content."""
    success = await educator.create_educational_thread(topic)
    return {"success": success}

@router.get("/protocols/astroport/pools/{pool_address}")
async def get_pool_info(
    pool_address: str,
    blockchain: BlockchainService = Depends(lambda: BlockchainService()),
    tracker: AstroportTracker = Depends(lambda: AstroportTracker(blockchain))
) -> Dict:
    """Get Astroport pool information."""
    info = await tracker.get_pool_info(pool_address)
    if not info:
        raise HTTPException(status_code=404, detail="Pool not found")
    return info

@router.get("/trending/topics", response_model=Dict[str, List[Dict]])
async def get_trending_topics():
    """Get trending topics endpoint."""
    try:
        # Example response for testing
        return {
            "trending_topics": [
                {
                    "topic": "SEI",
                    "data": {
                        "mention_count": 150,
                        "avg_engagement": 45.5,
                        "mentions_per_hour": 12,
                        "sentiment_distribution": {
                            "positive": 0.6,
                            "neutral": 0.3,
                            "negative": 0.1
                        }
                    }
                }
            ]
        }
    except Exception as e:
        logger.error(f"Error getting trending topics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get trending topics")

@router.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    await service_manager.initialize()

@router.on_event("shutdown")
async def shutdown_event():
    """Cleanup services on shutdown"""
    await service_manager.cleanup()

@router.get("/analytics/network", response_model=NetworkStatus)
async def get_network_analytics():
    """Get current network analytics"""
    try:
        return await service_manager.network_analytics.get_status()
    except Exception as e:
        logger.error(f"Error getting network analytics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get network analytics")

@router.get("/analytics/social", response_model=SocialMetrics)
async def get_social_analytics():
    """Get social media analytics"""
    try:
        return await service_manager.social_analytics.get_sentiment()
    except Exception as e:
        logger.error(f"Error getting social analytics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get social analytics")

@router.post("/content/generate")
async def generate_content(content_type: str):
    """Generate content based on type"""
    try:
        content = await service_manager.content_generator.generate_hourly_content()
        return ContentResponse(content=content)
    except Exception as e:
        logger.error(f"Error generating content: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate content")

@router.get("/analytics/comprehensive")
async def get_comprehensive_analytics():
    """Get comprehensive analytics"""
    try:
        network = await service_manager.network_analytics.get_status()
        social = await service_manager.social_analytics.get_sentiment()
        return AnalyticsResponse(
            network_metrics=network,
            social_metrics=social
        )
    except Exception as e:
        logger.error(f"Error getting comprehensive analytics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get analytics")

@router.get("/engagement")
async def get_engagement_data():
    # Implement engagement data retrieval
    return {}

@router.post("/engagement")
async def post_engagement_data(data: dict):
    # Implement engagement data posting
    return {}

@router.get("/status")
async def get_status():
    try:
        return {"status": "Service is running"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Service error")

@router.get("/blockchain/latest-block")
async def get_latest_block(blockchain: BlockchainService = Depends()):
    """Get the latest block information."""
    try:
        block = await blockchain.get_latest_block()
        if block:
            return block
        raise HTTPException(status_code=404, detail="Block not found")
    except Exception as e:
        logger.error(f"Error fetching latest block: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/secure-data", dependencies=[Depends(verify_api_key)])
async def get_secure_data():
    return {"data": "This is secure data"}