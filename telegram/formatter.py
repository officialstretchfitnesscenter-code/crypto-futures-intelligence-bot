"""Telegram message formatting"""

from datetime import datetime

def format_signal_alert(signal: dict) -> str:
    """Format signal alert message"""
    return f"""
🚨 <b>MARKET ALERT</b>

<b>Coin:</b> {signal.get('coin', 'N/A')}
<b>Action:</b> {signal.get('action', 'N/A')}
<b>Type:</b> {signal.get('signal_type', 'N/A')}
<b>Confidence:</b> {signal.get('confidence', 0)}%
<b>Risk:</b> {signal.get('risk_level', 'UNKNOWN')}

<b>Reason:</b>
{signal.get('reasons', 'Analysis in progress')}

<b>Price:</b> ${signal.get('price', 'N/A')}
<b>Timeframe:</b> {signal.get('timeframe', 'N/A')}
<b>Time:</b> {signal.get('timestamp', datetime.utcnow().isoformat())} UTC
    """.strip()

def format_top_opportunities(signals: list) -> str:
    """Format top opportunities"""
    if not signals:
        return "📊 No signals in database yet.\n\nUse /help for commands."
    
    message = "<b>🎯 TOP OPPORTUNITIES (Last 10)</b>\n\n"
    
    for i, signal in enumerate(signals, 1):
        emoji = "📈" if "BUY" in signal.get('action', '') else "📉"
        message += (
            f"{i}. {emoji} <b>{signal['coin']}</b>\n"
            f"   Action: {signal['action']}\n"
            f"   Confidence: {signal['confidence']}%\n"
            f"   Risk: {signal['risk_level']}\n\n"
        )
    
    return message

def format_daily_summary(stats: dict, signals: list) -> str:
    """Format daily market summary"""
    message = "<b>📊 DAILY MARKET SUMMARY</b>\n\n"
    
    message += f"<b>Total Signals Today:</b> {stats.get('total_signals', 0)}\n"
    message += f"<b>Buy Signals:</b> {stats.get('buy_signals', 0)}\n"
    message += f"<b>Sell Signals:</b> {stats.get('sell_signals', 0)}\n\n"
    
    if signals:
        message += "<b>Recent Signals:</b>\n"
        for signal in signals:
            emoji = "📈" if "BUY" in signal.get('action', '') else "📉"
            message += f"{emoji} {signal['coin']} - {signal['action']} ({signal['confidence']}%)\n"
    
    return message

def format_status_message(status_data: dict) -> str:
    """Format bot status message"""
    return f"""
<b>🤖 BOT STATUS</b>

<b>Status:</b> {status_data.get('status', 'UNKNOWN')}
<b>Uptime:</b> {status_data.get('uptime', 'N/A')}
<b>Signals Today:</b> {status_data.get('signals_today', 0)}
<b>Last Alert:</b> {status_data.get('last_alert', 'None')}

✅ Bot is running and ready for commands.
    """.strip()

def format_help_message() -> str:
    """Format help message"""
    return """
<b>📖 AVAILABLE COMMANDS</b>

<b>/start</b> - Start the bot
<b>/help</b> - Show this help message

<b>SIGNALS & ANALYSIS</b>
<b>/top</b> - Show top 10 recent signals
<b>/buy</b> - Show recent BUY LONG signals
<b>/sell</b> - Show recent SELL SHORT signals
<b>/summary</b> - Get daily market summary

<b>BOT INFO</b>
<b>/status</b> - Show bot status and uptime

<b>💡 TIPS</b>
• Signals are stored in database
• Use /top to see best opportunities
• Check /summary for daily stats
• Bot responds in real-time to commands

For more info, visit: https://github.com/yasir069-cs/crypto-futures-intelligence-bot
    """.strip()
