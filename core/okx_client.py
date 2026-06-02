"""OKX API Client"""

import hmac
import base64
import hashlib
import json
from datetime import datetime
from typing import Dict, List, Optional
import aiohttp
from config import Config
from utils.logger import get_logger

logger = get_logger(__name__)

class OKXClient:
    """OKX API client for fetching market data"""
    
    def __init__(self):
        self.base_url = Config.OKX_BASE_URL
        self.api_key = Config.OKX_API_KEY
        self.api_secret = Config.OKX_API_SECRET
        self.passphrase = Config.OKX_PASSPHRASE
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def _generate_signature(self, message: str) -> str:
        """Generate OKX API signature"""
        mac = hmac.new(
            bytes(self.api_secret, encoding='utf8'),
            bytes(message, encoding='utf-8'),
            digestmod=hashlib.sha256
        )
        return base64.b64encode(mac.digest()).decode()
    
    def _get_headers(self, method: str, path: str, body: str = '') -> Dict:
        """Get request headers with signature"""
        timestamp = datetime.utcnow().isoformat() + 'Z'
        message = timestamp + method + path + body
        signature = self._generate_signature(message)
        
        return {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': signature,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        }
    
    async def get_instruments(self, inst_type: str = 'SWAP') -> List[Dict]:
        """Get available instruments"""
        if not self.session:
            raise RuntimeError("Session not initialized. Use 'async with' context.")
        
        path = '/market/instruments'
        url = self.base_url + path
        
        params = {
            'instType': inst_type,
            'instFamily': 'USDT-SWAP'
        }
        
        try:
            headers = self._get_headers('GET', path)
            async with self.session.get(url, params=params, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    logger.debug(f"Fetched {len(data.get('data', []))} instruments")
                    return data.get('data', [])
                else:
                    logger.error(f"Failed to get instruments: {resp.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching instruments: {e}")
            return []
    
    async def get_candles(
        self,
        inst_id: str,
        bar: str = '1H',
        limit: int = 100
    ) -> List[Dict]:
        """Get candlestick data"""
        if not self.session:
            raise RuntimeError("Session not initialized. Use 'async with' context.")
        
        path = f'/market/candles'
        url = self.base_url + path
        
        params = {
            'instId': inst_id,
            'bar': bar,
            'limit': limit
        }
        
        try:
            headers = self._get_headers('GET', path)
            async with self.session.get(url, params=params, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    candles = data.get('data', [])
                    logger.debug(f"Fetched {len(candles)} candles for {inst_id} {bar}")
                    return candles
                else:
                    logger.error(f"Failed to get candles: {resp.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching candles: {e}")
            return []
    
    async def get_ticker(self, inst_id: str) -> Optional[Dict]:
        """Get ticker data"""
        if not self.session:
            raise RuntimeError("Session not initialized. Use 'async with' context.")
        
        path = f'/market/ticker'
        url = self.base_url + path
        
        params = {'instId': inst_id}
        
        try:
            headers = self._get_headers('GET', path)
            async with self.session.get(url, params=params, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    ticker = data.get('data', [{}])[0]
                    logger.debug(f"Fetched ticker for {inst_id}")
                    return ticker
                else:
                    logger.error(f"Failed to get ticker: {resp.status}")
                    return None
        except Exception as e:
            logger.error(f"Error fetching ticker: {e}")
            return None
    
    async def get_open_interest(self, inst_id: str) -> Optional[Dict]:
        """Get open interest data"""
        if not self.session:
            raise RuntimeError("Session not initialized. Use 'async with' context.")
        
        path = f'/public/open-interest'
        url = self.base_url + path
        
        params = {'instId': inst_id}
        
        try:
            headers = self._get_headers('GET', path)
            async with self.session.get(url, params=params, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    oi = data.get('data', [{}])[0]
                    logger.debug(f"Fetched OI for {inst_id}")
                    return oi
                else:
                    logger.error(f"Failed to get OI: {resp.status}")
                    return None
        except Exception as e:
            logger.error(f"Error fetching OI: {e}")
            return None
