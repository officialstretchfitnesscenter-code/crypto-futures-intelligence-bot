"""Telegram message formatter"""

from datetime import datetime
from typing import Dict, List
from utils.helpers import format_price, format_percentage

def format_signal_alert(signal: Dict) -> str:
    """
    Format signal as Telegram alert message
    
    Uses exact format specification from requirements
    """
    
    message = (
        f"🚨 MARKET ALERT\n\n"
        f"Coin: {signal['coin']}\n"
        f"Action: {signal['action']}\n"
        f"Type: {signal['signal_type']}\n"
        f"Confidence: {signal['confidence']}%\n"
        f"Risk: {signal['risk_level']}\n\n"
        f"Reason:\n"
    )
    
    for reason in signal['reasons']:
        message += f"{reason}\n"
    
    message += f"\nBot View:\n{signal['bot_view']}\n\n"
    message += f"Price: {format_price(signal['price'])}\n"
    message += f"Timeframe: {signal['timeframe']}\n"
    message += f"Time: {datetime.fromisoformat(signal['timestamp']).strftime('%Y-%m-%d %H:%M')} UTC"
    
    return message

def format_daily_summary(stats: Dict, top_signals: List[Dict]) -> str:
    """Format daily market summary"""
    
    message = (
        f"📊 DAILY MARKET REPORT\n\n"
        f"Date: {stats['date']}\n\n"
        f"Pairs Scanned: {stats.get('pairs_scanned', 'N/A')}\n"
        f"Signals Generated: {stats['total_signals']}\n"
        f"BUY LONG Signals: {stats['buy_signals']}\n"
        f"SELL SHORT Signals: {stats['sell_signals']}\n\n"
    )
    
    if top_signals:
        message += "Top Opportunities:\n"
        for i, signal in enumerate(top_signals[:5], 1):
            message += (
                f"{i}. {signal['coin']} - "
                f"{signal['action']} ({signal['confidence']}%)\n"
            )
    
    return message

def format_status_message(status_data: Dict) -> str:
    """Format bot status message"""
    
    message = (
        f"🤖 BOT STATUS\n\n"
        f"Status: {status_data.get('status', 'UNKNOWN')}\n"
        f"Pairs Scanned: {status_data.get('pairs_scanned', 'N/A')}\n"
        f"Signals Today: {status_data.get('signals_today', 0)}\n"
        f"Last Scan: {status_data.get('last_scan', 'Never')}\n"
        f"Uptime: {status_data.get('uptime', 'N/A')}\n"
    )
    
    return message

def format_top_opportunities(signals: List[Dict]) -> str:
    """Format top opportunities message"""
    
    message = "🎯 TOP OPPORTUNITIES\n\n"
    
    if not signals:
        message += "No signals generated yet."
        return message
    
    for i, signal in enumerate(signals[:10], 1):
        message += (
            f"{i}. {signal['coin']}\n"
            f"   Action: {signal['action']}\n"
            f"   Confidence: {signal['confidence']}%\n"
            f"   Risk: {signal['risk_level']}\n\n"
        )
    
    return message
