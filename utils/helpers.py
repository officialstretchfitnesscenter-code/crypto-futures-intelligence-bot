"""Utility helper functions"""

from datetime import datetime, timedelta
from typing import List, Dict
import json

def format_price(price: float, decimals: int = 8) -> str:
    """Format price to string"""
    if price >= 1:
        return f"{price:.2f}"
    return f"{price:.{decimals}f}".rstrip('0').rstrip('.')

def format_percentage(value: float, decimals: int = 2) -> str:
    """Format percentage"""
    sign = '+' if value >= 0 else ''
    return f"{sign}{value:.{decimals}f}%"

def format_volume(volume: float) -> str:
    """Format volume to readable format"""
    if volume >= 1_000_000:
        return f"{volume / 1_000_000:.2f}M"
    elif volume >= 1_000:
        return f"{volume / 1_000:.2f}K"
    return f"{volume:.2f}"

def get_relative_time(dt: datetime) -> str:
    """Get relative time string"""
    now = datetime.utcnow()
    diff = now - dt
    
    if diff < timedelta(minutes=1):
        return "just now"
    elif diff < timedelta(hours=1):
        minutes = int(diff.total_seconds() / 60)
        return f"{minutes}m ago"
    elif diff < timedelta(days=1):
        hours = int(diff.total_seconds() / 3600)
        return f"{hours}h ago"
    else:
        days = int(diff.days)
        return f"{days}d ago"

def parse_timeframe(tf: str) -> int:
    """Convert timeframe string to minutes"""
    mapping = {
        '1m': 1,
        '5m': 5,
        '15m': 15,
        '30m': 30,
        '1H': 60,
        '4H': 240,
        '1D': 1440,
    }
    return mapping.get(tf, 0)

def is_intraday_timeframe(tf: str) -> bool:
    """Check if timeframe is intraday"""
    intraday_timeframes = ['15m', '1H']
    return tf in intraday_timeframes

def is_swing_timeframe(tf: str) -> bool:
    """Check if timeframe is swing"""
    swing_timeframes = ['4H', '1D']
    return tf in swing_timeframes

def calculate_rvol(current_volume: float, avg_volume: float) -> float:
    """Calculate relative volume"""
    if avg_volume == 0:
        return 0
    return current_volume / avg_volume

def calculate_oi_change(current_oi: float, previous_oi: float) -> float:
    """Calculate OI change percentage"""
    if previous_oi == 0:
        return 0
    return ((current_oi - previous_oi) / previous_oi) * 100

def get_resistance_level(highs: List[float]) -> float:
    """Get resistance level from recent highs"""
    if not highs:
        return 0
    return max(highs[-20:]) if len(highs) >= 20 else max(highs)

def get_support_level(lows: List[float]) -> float:
    """Get support level from recent lows"""
    if not lows:
        return 0
    return min(lows[-20:]) if len(lows) >= 20 else min(lows)

def is_breakout(current_price: float, resistance: float, threshold: float = 0.001) -> bool:
    """Check if price broke above resistance"""
    return current_price > resistance * (1 + threshold)

def is_breakdown(current_price: float, support: float, threshold: float = 0.001) -> bool:
    """Check if price broke below support"""
    return current_price < support * (1 - threshold)

def moving_average(values: List[float], period: int) -> List[float]:
    """Calculate simple moving average"""
    if len(values) < period:
        return []
    
    mas = []
    for i in range(period - 1, len(values)):
        ma = sum(values[i - period + 1:i + 1]) / period
        mas.append(ma)
    
    return mas

def exponential_moving_average(values: List[float], period: int) -> List[float]:
    """Calculate exponential moving average"""
    if len(values) < period:
        return []
    
    emas = []
    multiplier = 2 / (period + 1)
    
    # Simple MA for first value
    sma = sum(values[:period]) / period
    emas.append(sma)
    
    # EMA for remaining values
    for i in range(period, len(values)):
        ema = values[i] * multiplier + emas[-1] * (1 - multiplier)
        emas.append(ema)
    
    return emas
