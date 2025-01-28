import requests
from typing import Dict, List
import logging
from bs4 import BeautifulSoup
import json

class SEIKnowledgeBase:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Cache for documentation
        self.doc_cache = {}
        
        # Eliza-inspired response patterns
        self.conversation_patterns = {
            'onboarding': {
                'triggers': ['how do i start', 'getting started', 'begin', 'new to sei'],
                'responses': [
                    "I see you're interested in getting started with SEI! Let me help break it down:",
                    "Welcome to SEI! Here's what you need to know first:",
                    "Getting started is easy! Here's your roadmap:"
                ]
            },
            'technical': {
                'triggers': ['error', 'problem', 'help', 'stuck'],
                'responses': [
                    "I understand you're having some trouble. Let's solve this step by step:",
                    "Don't worry, I can help you with that. First, let me check the docs:",
                ]
            },
            'defi': {
                'triggers': ['yield', 'apy', 'stake', 'farm'],
                'responses': [
                    "Ah, you're interested in DeFi opportunities! Here's what's hot right now:",
                    "Let me check the latest yields for you:",
                ]
            },
            'yield_farming': {
                'triggers': ['farm', 'yield', 'apy', 'returns', 'earning'],
                'responses': [
                    "Let me check the latest yield opportunities on SEI for you:",
                    "Here are the current top farming opportunities:",
                    "I'll fetch the most profitable yields right now:"
                ]
            },
            'market_analysis': {
                'triggers': ['price', 'market', 'prediction', 'analysis', 'trend'],
                'responses': [
                    "Here's what I'm seeing in the SEI markets:",
                    "Let me analyze the current market conditions:",
                    "Based on recent data, here's the market overview:"
                ]
            },
            'security': {
                'triggers': ['safe', 'security', 'risk', 'protect', 'secure'],
                'responses': [
                    "Security is crucial! Here are the best practices for SEI:",
                    "Let me share some security tips for your SEI journey:",
                    "Here's how to keep your assets safe on SEI:"
                ]
            },
            'nft_info': {
                'triggers': ['nft', 'cappys', 'fuckers', 'collection'],
                'responses': [
                    "Let me check the latest NFT stats for you:",
                    "Here's what's happening in SEI's NFT space:",
                    "I'll fetch the current NFT market data:"
                ]
            }
        }

        # Add protocol-specific information
        self.protocol_info = {
            'dragonswap': {
                'type': 'DEX',
                'features': ['Swap', 'Liquidity Provision', 'Yield Farming'],
                'key_metrics': ['TVL', '24h Volume', 'APR'],
                'website': 'https://dragonswap.sei',
                'description': "DragonSwap is SEI's leading DEX for trading and liquidity provision."
            },
            'yei_finance': {
                'type': 'Lending',
                'features': ['Lending', 'Borrowing', 'Yield Generation'],
                'key_metrics': ['TVL', 'Total Borrowed', 'Lending APY'],
                'website': 'https://yei.finance',
                'description': "YEI Finance provides lending and borrowing services on SEI."
            },
            'silo_stake': {
                'type': 'Staking',
                'features': ['Staking', 'Liquid Staking', 'Governance'],
                'key_metrics': ['TVL', 'Staking APR', 'Total Stakers'],
                'website': 'https://silostake.sei',
                'description': "Silo Stake is the premier staking solution on SEI."
            }
        }

    async def fetch_sei_docs(self, topic: str) -> str:
        """Fetch and cache SEI documentation"""
        if topic in self.doc_cache:
            return self.doc_cache[topic]

        try:
            # Base URL for SEI docs
            base_url = "https://docs.sei.io"
            
            # Example of fetching and parsing documentation
            response = requests.get(f"{base_url}/api/search?query={topic}")
            if response.status_code == 200:
                content = response.json()
                
                # Process and cache the content
                processed_content = self._process_doc_content(content)
                self.doc_cache[topic] = processed_content
                return processed_content
            
            return "I couldn't find specific documentation for that topic."
            
        except Exception as e:
            self.logger.error(f"Error fetching docs: {e}")
            return "Sorry, I'm having trouble accessing the documentation right now."

    async def get_protocol_info(self, protocol_name: str) -> Dict:
        """Get detailed protocol information and live metrics"""
        try:
            base_info = self.protocol_info.get(protocol_name.lower(), {})
            if not base_info:
                return None
                
            # Fetch live metrics (implement API calls here)
            live_metrics = await self._fetch_protocol_metrics(protocol_name)
            
            return {
                **base_info,
                'metrics': live_metrics
            }
        except Exception as e:
            self.logger.error(f"Error fetching protocol info: {e}")
            return None

    def _process_doc_content(self, content: Dict) -> str:
        """Enhanced documentation processing"""
        try:
            if 'hits' in content:
                processed = []
                for hit in content['hits'][:2]:
                    # Clean and format the content
                    title = hit['title'].strip()
                    excerpt = hit['excerpt'].strip()
                    
                    # Break down complex information
                    bullet_points = self._break_down_content(excerpt)
                    
                    processed.append(f"📌 {title}\n{bullet_points}")
                
                return "\n\n".join(processed)
            return "No relevant information found."
        except Exception as e:
            self.logger.error(f"Error processing content: {e}")
            return "Error processing documentation content."

    def _break_down_content(self, content: str) -> str:
        """Break down complex content into digestible points"""
        sentences = content.split('. ')
        if len(sentences) > 1:
            return '\n'.join(f"• {sentence.strip()}" for sentence in sentences if sentence)
        return content

    def get_contextual_response(self, user_input: str) -> Dict:
        """Generate contextual responses using Eliza-inspired patterns"""
        user_input = user_input.lower()
        
        for context, data in self.conversation_patterns.items():
            if any(trigger in user_input for trigger in data['triggers']):
                return {
                    'response_type': context,
                    'message': self._select_response(data['responses']),
                    'should_fetch_docs': True if context in ['technical', 'onboarding'] else False
                }
        
        return {
            'response_type': 'general',
            'message': "I'm here to help! Ask me about getting started with SEI, DeFi opportunities, or any technical questions.",
            'should_fetch_docs': False
        } 