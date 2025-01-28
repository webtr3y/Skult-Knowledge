"""
Enhanced ELIZA patterns for blockchain education and engagement.
Original ELIZA concepts by Joseph Weizenbaum (MIT, 1966)
"""

from typing import Dict, List, Pattern
import re
from datetime import datetime

class ElizaPatternMatcher:
    def __init__(self):
        # Core ELIZA-style reflections
        self.reflection_map = {
            "am": "are",
            "i": "you",
            "my": "your",
            "was": "were",
            "i'm": "you're",
            "i'd": "you'd",
            "i've": "you've",
            "i'll": "you'll",
            "mine": "yours",
            "myself": "yourself",
            "you": "I",
            "your": "my"
        }

        # Educational scaffolding levels
        self.expertise_levels = {
            'beginner': ['basics', 'fundamentals', 'getting started'],
            'intermediate': ['trading', 'defi', 'staking'],
            'advanced': ['development', 'technical', 'architecture']
        }

        # ELIZA-style patterns with blockchain focus
        self.patterns = {
            # Learning patterns
            r'.*how (do|can) i (learn|understand) (about )?(.*?)\??$': {
                'decomposition': ['intent', 'action', 'topic'],
                'reassembly': [
                    "I see you're interested in {topic}. Let's start with the fundamentals. What do you already know about it?",
                    "Learning {topic} is exciting! Would you like me to explain the basics first?",
                    "I can help you understand {topic}. Should we begin with a simple overview or dive deeper?"
                ],
                'follow_up': ['basics', 'examples', 'practical_application']
            },

            # Problem-solving patterns
            r'.*having (trouble|problems|issues) with (.*?)\??$': {
                'decomposition': ['problem_type', 'topic'],
                'reassembly': [
                    "I understand {topic} can be challenging. Could you tell me more about what's troubling you?",
                    "Let's solve this {topic} issue together. What specific difficulty are you experiencing?",
                    "Many people face challenges with {topic}. Would you like me to walk you through it step by step?"
                ],
                'follow_up': ['troubleshooting', 'examples', 'documentation']
            },

            # Market sentiment patterns
            r'.*(worried|concerned|excited|bullish|bearish) about (.*?)\??$': {
                'decomposition': ['sentiment', 'topic'],
                'reassembly': [
                    "I notice you're feeling {sentiment} about {topic}. Let me share some current data to help inform your perspective.",
                    "Your {sentiment} view on {topic} is interesting. Would you like to see the latest analytics?",
                    "Let's analyze {topic} together. I can show you some key metrics that might help."
                ],
                'follow_up': ['market_data', 'analysis', 'historical_context']
            },

            # Technical questions
            r'.*what.?s the (difference|relationship) between (.*?) and (.*?)\??$': {
                'decomposition': ['comparison_type', 'first_term', 'second_term'],
                'reassembly': [
                    "Let me explain how {first_term} and {second_term} relate to each other...",
                    "The relationship between {first_term} and {second_term} is interesting. Would you like a detailed comparison?",
                    "I can help clarify the distinction between {first_term} and {second_term}. Where should we start?"
                ],
                'follow_up': ['comparison', 'examples', 'use_cases']
            }
        }

    def get_expertise_level(self, message: str) -> str:
        """Determine user's expertise level from message content"""
        message = message.lower()
        for level, keywords in self.expertise_levels.items():
            if any(keyword in message for keyword in keywords):
                return level
        return 'beginner'

    def generate_follow_up(self, variables: Dict, expertise_level: str) -> List[str]:
        """Generate contextual follow-up questions"""
        topic = variables.get('topic', '')
        if expertise_level == 'beginner':
            return [
                f"Would you like me to explain {topic} in simpler terms?",
                f"Should we start with the basics of {topic}?",
                "Would you prefer to see some real-world examples?"
            ]
        elif expertise_level == 'advanced':
            return [
                f"Would you like to dive into the technical aspects of {topic}?",
                f"Should we look at some advanced metrics for {topic}?",
                "Would you like to see the underlying data?"
            ]
        return [
            f"What specific aspect of {topic} interests you most?",
            f"Would you like to see some practical applications of {topic}?",
            "Should we explore this topic with some current market data?"
        ]

    def enhance_response(self, response: str, data: Dict) -> str:
        """Enhance response with real-time data"""
        if 'price' in data:
            response += f"\n\nCurrent price: ${data['price']:.2f}"
        if 'sentiment' in data:
            response += f"\nCommunity sentiment: {data['sentiment']}"
        return response

    def reflect(self, text: str) -> str:
        """
        ELIZA-style word reflection (e.g., "I am" -> "you are")
        """
        words = text.lower().split()
        return ' '.join(self.reflection_map.get(word, word) for word in words)

    def match_pattern(self, input_text: str) -> Dict:
        """
        Enhanced ELIZA-style pattern matching with blockchain context
        """
        for pattern, response_data in self.patterns.items():
            if match := re.match(pattern, input_text, re.I):
                return {
                    'match': match,
                    'response_template': response_data['reassembly'],
                    'variables': dict(zip(response_data['decomposition'], match.groups()))
                }
        return None 