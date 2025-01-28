from typing import Dict, List
from datetime import datetime

class BrandVoiceManager:
    def __init__(self):
        self.voice_characteristics = {
            'tone': 'professional yet approachable',
            'style': 'informative and engaging',
            'personality': 'helpful and knowledgeable'
        }
        
    def get_thread_template(self) -> Dict[str, str]:
        """Get template for Twitter threads"""
        return {
            'intro': '🔍 SEI Network Analysis\n\n',
            'body': '📊 Key Insights:\n\n',
            'conclusion': '🚀 Stay tuned for more updates!\n\n#SEI #Crypto',
            'cta': 'Follow for more SEI ecosystem insights! 🌟'
        }
    
    async def format_content(self, topic: str, data: Dict) -> str:
        """Format content according to brand voice"""
        template = self.get_content_template(topic)
        formatted_data = self.format_data_points(data)
        return self.apply_brand_voice(template, formatted_data)

    def format_data_points(self, data: Dict) -> List[str]:
        """Format data points into digestible content"""
        formatted = []
        for key, value in data.items():
            if isinstance(value, (int, float)):
                formatted.append(f"📈 {key.replace('_', ' ').title()}: {value:,}")
            else:
                formatted.append(f"💡 {key.replace('_', ' ').title()}: {value}")
        return formatted 