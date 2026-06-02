"""Telegram Bot Handler"""

import asyncio
from datetime import datetime
from typing import Optional, Dict
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update
from config import Config
from database import db
from utils.logger import get_logger
from telegram.formatter import (
    format_signal_alert, format_daily_summary,
    format_status_message, format_top_opportunities
)

logger = get_logger(__name__)

class TelegramBot:
    """Telegram bot for alerts and commands"""
    
    def __init__(self):
        self.token = Config.TELEGRAM_BOT_TOKEN
        self.chat_id = Config.TELEGRAM_CHAT_ID
        self.app: Optional[Application] = None
        self.start_time = datetime.utcnow()
    
    async def initialize(self):
        """Initialize Telegram bot"""
        self.app = Application.builder().token(self.token).build()
        
        # Add command handlers
        self.app.add_handler(CommandHandler('top', self.cmd_top))
        self.app.add_handler(CommandHandler('buy', self.cmd_buy))
        self.app.add_handler(CommandHandler('sell', self.cmd_sell))
        self.app.add_handler(CommandHandler('summary', self.cmd_summary))
        self.app.add_handler(CommandHandler('status', self.cmd_status))
        
        # Start bot
        await self.app.initialize()
        await self.app.start()
        logger.info("Telegram bot initialized")
    
    async def stop(self):
        """Stop Telegram bot"""
        if self.app:
            await self.app.stop()
            await self.app.shutdown()
            logger.info("Telegram bot stopped")
    
    async def send_message(self, message: str):
        """Send message to Telegram"""
        try:
            async with self.app._client.session:
                from telegram import Bot
                bot = Bot(token=self.token)
                await bot.send_message(chat_id=self.chat_id, text=message)
            logger.debug(f"Message sent to Telegram")
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
    
    async def send_signal_alert(self, signal: Dict):
        """Send signal alert to Telegram"""
        message = format_signal_alert(signal)
        await self.send_message(message)
    
    async def cmd_top(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /top command"""
        signals = db.get_recent_signals(limit=10)
        message = format_top_opportunities(signals)
        await update.message.reply_text(message)
    
    async def cmd_buy(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /buy command"""
        signals = db.get_signals_by_action('BUY LONG', limit=20)
        message = f"📈 RECENT BUY LONG SIGNALS\n\n"
        
        if signals:
            for signal in signals:
                message += (
                    f"• {signal['coin']}: {signal['confidence']}% confidence\n"
                )
        else:
            message += "No BUY signals generated yet."
        
        await update.message.reply_text(message)
    
    async def cmd_sell(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /sell command"""
        signals = db.get_signals_by_action('SELL SHORT', limit=20)
        message = f"📉 RECENT SELL SHORT SIGNALS\n\n"
        
        if signals:
            for signal in signals:
                message += (
                    f"• {signal['coin']}: {signal['confidence']}% confidence\n"
                )
        else:
            message += "No SELL signals generated yet."
        
        await update.message.reply_text(message)
    
    async def cmd_summary(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /summary command"""
        stats = db.get_daily_stats()
        signals = db.get_recent_signals(limit=5)
        message = format_daily_summary(stats, signals)
        await update.message.reply_text(message)
    
    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        uptime = datetime.utcnow() - self.start_time
        stats = db.get_daily_stats()
        
        status_data = {
            'status': 'ONLINE',
            'pairs_scanned': 'XXX',
            'signals_today': stats['total_signals'],
            'last_scan': 'In progress' if hasattr(self, 'scanner') else 'Never',
            'uptime': f"{uptime.seconds // 3600}h {(uptime.seconds % 3600) // 60}m"
        }
        
        message = format_status_message(status_data)
        await update.message.reply_text(message)
