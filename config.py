import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class Config:
    """Base configuration"""
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8816616926:AAHqoXYMbo5kGtXHrBidI8Oha2RvLaK86uM')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '1490359174')
    
    # Bot Configuration
    ENABLE_DEBUG = os.getenv('ENABLE_DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Database
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/signals.db')
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        required = ['TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID']
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
