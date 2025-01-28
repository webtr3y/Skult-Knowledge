from typing import Dict, Any
import re

async def handle_network_query(engine: Any, match: re.Match) -> Dict:
    """Handle network-related queries"""
    return {
        'text': "Let me fetch the latest network statistics for you...",
        'data_requirements': ['network_stats'],
        'follow_up': [
            "Would you like to know more about specific metrics?",
            "Should I explain what these numbers mean?"
        ]
    }

async def handle_defi_query(engine: Any, match: re.Match) -> Dict:
    """Handle DeFi-related queries"""
    return {
        'text': "SEI's DeFi ecosystem is growing rapidly. Here are the latest metrics...",
        'data_requirements': ['defi_stats'],
        'follow_up': [
            "Would you like to explore specific DeFi protocols?",
            "Should I show you how to get started with DeFi on SEI?"
        ]
    }

CONVERSATION_PATTERNS = {
    # Network queries
    r'(?i)how.*(network|chain|blockchain).*performing': {
        'response_func': handle_network_query,
        'context_update': {'topic': 'network'}
    },
    
    # DeFi queries
    r'(?i)(defi|trading|swap)': {
        'response_func': handle_defi_query,
        'context_update': {'topic': 'defi'}
    },
    
    # Add more patterns here...
} 