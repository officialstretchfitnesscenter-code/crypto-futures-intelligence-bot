import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class Config:
    """Base configuration"""
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
    
    # OKX API
    OKX_API_KEY = os.getenv('OKX_API_KEY', '')
    OKX_API_SECRET = os.getenv('OKX_API_SECRET', '')
    OKX_PASSPHRASE = os.getenv('OKX_PASSPHRASE', '')
    OKX_BASE_URL = 'https://www.okx.com/api/v5'
    
    # Bot Configuration
    SCAN_INTERVAL_HOURS = int(os.getenv('SCAN_INTERVAL_HOURS', 1))
    CONFIDENCE_THRESHOLD = int(os.getenv('CONFIDENCE_THRESHOLD', 88))
    ALERT_COOLDOWN_HOURS = int(os.getenv('ALERT_COOLDOWN_HOURS', 6))
    ENABLE_DEBUG = os.getenv('ENABLE_DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Database
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/signals.db')
    
    # Market Configuration
    MAX_PAIRS_SCAN = int(os.getenv('MAX_PAIRS_SCAN', 500))
    TIMEFRAMES_INTRADAY = ['15m', '1H']
    TIMEFRAMES_SWING = ['4H', '1D']
    
    # Analysis Parameters
    RVOL_THRESHOLD_STRONG = 3.0
    RVOL_THRESHOLD_VERY_STRONG = 5.0
    OI_CHANGE_THRESHOLD = 10.0  # percent
    
    # Confidence Scoring Weights
    CONFIDENCE_WEIGHTS = {
        'price_expansion': 15,
        'relative_volume': 20,
        'open_interest': 15,
        'trend': 15,
        'market_structure': 20,
        'breakout_strength': 10,
        'multi_timeframe': 5
    }
    
    # Risk Levels
    RISK_LEVELS = {
        'low': {'min': 0.75, 'max': 1.0},
        'medium': {'min': 0.5, 'max': 0.75},
        'high': {'min': 0, 'max': 0.5}
    }
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        required = ['TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID', 'OKX_API_KEY', 'OKX_API_SECRET', 'OKX_PASSPHRASE']
        missing = [key for key in required if not getattr(cls, key)]
        if missing:
            raise ValueError(f"Missing configuration: {', '.join(missing)}")
        
        # Create data directory if it doesn't exist
        Path(cls.DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
        
        return True

class DevelopmentConfig(Config):
    """Development configuration"""
    ENABLE_DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    ENABLE_DEBUG = False
    LOG_LEVEL = 'INFO'

def get_config():
    """Get config based on environment"""
    env = os.getenv('ENVIRONMENT', 'production').lower()
    if env == 'development':
        return DevelopmentConfig()
    return ProductionConfig()
