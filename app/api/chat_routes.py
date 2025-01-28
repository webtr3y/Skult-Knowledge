from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import logging
from ..agent.knowledge_base import SEIKnowledgeBase

router = APIRouter()
logger = logging.getLogger(__name__)
knowledge_base = SEIKnowledgeBase()

class ChatMessage(BaseModel):
    user_message: str

class ChatResponse(BaseModel):
    response: str
    suggested_actions: List[str] = []
    documentation: str = ""

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(message: ChatMessage):
    try:
        # Get contextual response
        context_response = knowledge_base.get_contextual_response(message.user_message)
        
        # Fetch documentation if needed
        documentation = ""
        if context_response['should_fetch_docs']:
            documentation = await knowledge_base.fetch_sei_docs(message.user_message)
        
        # Generate suggested actions based on context
        suggested_actions = _generate_suggested_actions(context_response['response_type'])
        
        return ChatResponse(
            response=context_response['message'],
            suggested_actions=suggested_actions,
            documentation=documentation
        )
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing chat request")

def _generate_suggested_actions(context_type: str) -> List[str]:
    """Generate context-appropriate suggested actions"""
    actions = {
        'onboarding': [
            "How to buy SEI",
            "Setup wallet",
            "Connect to DeFi"
        ],
        'technical': [
            "Common issues",
            "Network status",
            "Contact support"
        ],
        'defi': [
            "Current yields",
            "Top protocols",
            "Risk levels"
        ],
        'general': [
            "Getting started",
            "DeFi opportunities",
            "Technical help"
        ]
    }
    return actions.get(context_type, actions['general']) 