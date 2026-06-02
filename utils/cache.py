"""Caching utility"""

from datetime import datetime, timedelta
from typing import Any, Optional, Dict
from utils.logger import get_logger

logger = get_logger(__name__)

class Cache:
    """Simple in-memory cache with TTL"""
    
    def __init__(self):
        self.data: Dict[str, Dict[str, Any]] = {}
    
    def set(self, key: str, value: Any, ttl_seconds: int = 3600):
        """Set cache value with TTL"""
        expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)
        self.data[key] = {
            'value': value,
            'expires_at': expires_at
        }
        logger.debug(f"Cache set: {key} (TTL: {ttl_seconds}s)")
    
    def get(self, key: str) -> Optional[Any]:
        """Get cache value"""
        if key not in self.data:
            return None
        
        entry = self.data[key]
        if datetime.utcnow() > entry['expires_at']:
            del self.data[key]
            logger.debug(f"Cache expired: {key}")
            return None
        
        logger.debug(f"Cache hit: {key}")
        return entry['value']
    
    def delete(self, key: str):
        """Delete cache entry"""
        if key in self.data:
            del self.data[key]
            logger.debug(f"Cache deleted: {key}")
    
    def clear(self):
        """Clear all cache"""
        self.data.clear()
        logger.debug("Cache cleared")
    
    def cleanup(self):
        """Remove expired entries"""
        now = datetime.utcnow()
        expired_keys = [
            key for key, entry in self.data.items()
            if now > entry['expires_at']
        ]
        
        for key in expired_keys:
            del self.data[key]
        
        if expired_keys:
            logger.debug(f"Cache cleanup: removed {len(expired_keys)} expired entries")

# Global cache instance
cache = Cache()
