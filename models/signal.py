"""Signal data model"""

from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Signal:
    """Trading signal model"""
    
    coin: str
    action: str  # BUY LONG or SELL SHORT
    signal_type: str  # INTRADAY or SWING
    confidence: int  # 0-100
    risk_level: str  # LOW, MEDIUM, HIGH
    reasons: List[str]
    bot_view: str
    price: float
    timeframe: str
    timestamp: datetime
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'coin': self.coin,
            'action': self.action,
            'signal_type': self.signal_type,
            'confidence': self.confidence,
            'risk_level': self.risk_level,
            'reasons': self.reasons,
            'bot_view': self.bot_view,
            'price': self.price,
            'timeframe': self.timeframe,
            'timestamp': self.timestamp.isoformat()
        }
