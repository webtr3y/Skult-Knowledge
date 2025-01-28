"""
Educational scaffolding system inspired by ELIZA's contextual awareness.
"""

from typing import Dict, List
from datetime import datetime

class EducationalScaffold:
    def __init__(self):
        self.learning_paths = {
            'trading': [
                'market_basics',
                'technical_analysis',
                'risk_management',
                'advanced_strategies'
            ],
            'defi': [
                'defi_fundamentals',
                'protocols',
                'yield_farming',
                'risk_assessment'
            ],
            'development': [
                'smart_contracts',
                'architecture',
                'security',
                'optimization'
            ]
        }
        
        self.user_progress = {}

    def track_progress(self, user_id: str, topic: str, subtopic: str):
        """Track user's learning progress"""
        if user_id not in self.user_progress:
            self.user_progress[user_id] = {}
        
        if topic not in self.user_progress[user_id]:
            self.user_progress[user_id][topic] = {
                'current_level': 0,
                'completed_topics': set(),
                'last_interaction': None
            }
            
        self.user_progress[user_id][topic]['completed_topics'].add(subtopic)
        self.user_progress[user_id][topic]['last_interaction'] = datetime.now()

    def get_next_topic(self, user_id: str, path: str) -> str:
        """Get next topic in learning path"""
        progress = self.user_progress.get(user_id, {}).get(path, {})
        completed = progress.get('completed_topics', set())
        all_topics = self.learning_paths[path]
        
        for topic in all_topics:
            if topic not in completed:
                return topic
                
        return all_topics[-1]  # Review mode if all completed 