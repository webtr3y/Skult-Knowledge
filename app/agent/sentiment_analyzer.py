from transformers import pipeline
from typing import Dict, List
import logging

class SentimentAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            # Using FinBERT, which is specifically trained for financial text
            self.analyzer = pipeline(
                "sentiment-analysis",
                model="ProsusAI/finbert",
                max_length=512
            )
        except Exception as e:
            self.logger.error(f"Error initializing sentiment analyzer: {str(e)}")
            raise

    def analyze_text(self, text: str) -> Dict:
        """
        Analyze the sentiment of a given text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict: Sentiment analysis result
        """
        try:
            result = self.analyzer(text)[0]
            return {
                'label': result['label'],
                'score': result['score']
            }
        except Exception as e:
            self.logger.error(f"Error analyzing sentiment: {str(e)}")
            return {'label': 'neutral', 'score': 0.0}

    def analyze_batch(self, texts: List[str]) -> List[Dict]:
        """
        Analyze sentiment for a batch of texts
        
        Args:
            texts (List[str]): List of texts to analyze
            
        Returns:
            List[Dict]: List of sentiment analysis results
        """
        try:
            results = self.analyzer(texts)
            return [{'label': r['label'], 'score': r['score']} for r in results]
        except Exception as e:
            self.logger.error(f"Error analyzing batch sentiment: {str(e)}")
            return [{'label': 'neutral', 'score': 0.0} for _ in texts] 