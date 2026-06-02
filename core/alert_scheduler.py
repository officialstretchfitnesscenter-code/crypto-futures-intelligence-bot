import asyncio
from datetime import datetime, timedelta
from typing import Callable, Dict, List
from utils.logger import get_logger
from core.market_analyzer import market_analyzer

logger = get_logger(__name__)

class AlertScheduler:
    """Schedule and manage market alerts"""
    
    def __init__(self):
        self.alerts = {}
        self.active_scans = {}
        self.price_thresholds = {}
    
    async def start_hourly_scan(self, coins: List[str], callback: Callable):
        """Start hourly market scan"""
        while True:
            try:
                logger.info(f"Starting hourly scan for {len(coins)} coins")
                
                for coin in coins:
                    analysis = await market_analyzer.analyze_coin(coin)
                    
                    if analysis:
                        # Check for significant movements
                        price_change = analysis.get('price_change_24h', 0)
                        volatility = analysis.get('volatility', 0)
                        
                        if abs(price_change) > 5 or volatility > 5:
                            await callback({
                                'type': 'PRICE_ALERT',
                                'coin': coin,
                                'price': analysis.get('current_price'),
                                'change': price_change,
                                'volatility': volatility,
                                'timestamp': datetime.utcnow().isoformat()
                            })
                
                # Sleep for 1 hour
                await asyncio.sleep(3600)
            except Exception as e:
                logger.error(f"Error in hourly scan: {e}")
                await asyncio.sleep(300)  # Retry after 5 minutes
    
    async def start_price_threshold_monitor(self, coin: str, buy_price: float, sell_price: float, callback: Callable):
        """Monitor price thresholds"""
        logger.info(f"Starting price threshold monitor for {coin}: BUY=${buy_price}, SELL=${sell_price}")
        
        while True:
            try:
                analysis = await market_analyzer.analyze_coin(coin)
                current_price = analysis.get('current_price', 0)
                
                if current_price >= sell_price:
                    await callback({
                        'type': 'SELL_ALERT',
                        'coin': coin,
                        'current_price': current_price,
                        'target_price': sell_price,
                        'message': f'Sell alert: {coin} reached ${current_price:.2f}'
                    })
                
                elif current_price <= buy_price:
                    await callback({
                        'type': 'BUY_ALERT',
                        'coin': coin,
                        'current_price': current_price,
                        'target_price': buy_price,
                        'message': f'Buy alert: {coin} reached ${current_price:.2f}'
                    })
                
                await asyncio.sleep(300)  # Check every 5 minutes
            except Exception as e:
                logger.error(f"Error monitoring {coin}: {e}")
                await asyncio.sleep(300)
    
    async def check_high_volatility(self, coins: List[str], threshold: float = 5.0, callback: Callable = None):
        """Check for high volatility coins"""
        volatile_coins = []
        
        for coin in coins:
            analysis = await market_analyzer.analyze_coin(coin)
            if analysis and analysis.get('volatility', 0) > threshold:
                volatile_coins.append({
                    'coin': coin,
                    'volatility': analysis.get('volatility'),
                    'price': analysis.get('current_price'),
                    'signal': analysis.get('signal')
                })
        
        if callback and volatile_coins:
            await callback(volatile_coins)
        
        return volatile_coins

alert_scheduler = AlertScheduler()
