"""Confidence Scoring Engine"""

from typing import Dict
from config import Config
from utils.logger import get_logger

logger = get_logger(__name__)

class ConfidenceEngine:
    """Calculate signal confidence scores"""
    
    def __init__(self):
        self.weights = Config.CONFIDENCE_WEIGHTS
        self.threshold = Config.CONFIDENCE_THRESHOLD
    
    def calculate_confidence(
        self,
        price_expansion: float,
        relative_volume: float,
        open_interest: float,
        trend: float,
        market_structure: float,
        breakout_strength: float,
        multi_timeframe: float
    ) -> int:
        """
        Calculate overall confidence score (0-100)
        
        Factors:
        - Price Expansion (15%)
        - Relative Volume (20%)
        - Open Interest (15%)
        - Trend (15%)
        - Market Structure (20%)
        - Breakout Strength (10%)
        - Multi-Timeframe Alignment (5%)
        """
        
        score = (
            price_expansion * self.weights['price_expansion'] +
            relative_volume * self.weights['relative_volume'] +
            open_interest * self.weights['open_interest'] +
            trend * self.weights['trend'] +
            market_structure * self.weights['market_structure'] +
            breakout_strength * self.weights['breakout_strength'] +
            multi_timeframe * self.weights['multi_timeframe']
        )
        
        # Normalize to 0-100
        score = min(100, max(0, int(score)))
        
        return score
    
    def meets_threshold(self, confidence: int) -> bool:
        """Check if confidence meets alert threshold"""
        return confidence >= self.threshold
