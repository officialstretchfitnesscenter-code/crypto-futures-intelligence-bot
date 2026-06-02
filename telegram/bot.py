"""Telegram Bot Handler"""

import asyncio
from datetime import datetime
from typing import Optional
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update
from config import Config
from database import db
from utils.logger import get_logger
from telegram.formatter import (
    format_signal_alert, format_daily_summary,
    format_status_message, format_top_opportunities,
    format_help_message
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
        logger.info("Initializing Telegram bot...")
        self.app = Application.builder().token(self.token).build()
        
        # Add command handlers
        self.app.add_handler(CommandHandler('start', self.cmd_start))
        self.app.add_handler(CommandHandler('help', self.cmd_help))
        self.app.add_handler(CommandHandler('top', self.cmd_top))
        self.app.add_handler(CommandHandler('buy', self.cmd_buy))
        self.app.add_handler(CommandHandler('sell', self.cmd_sell))
        self.app.add_handler(CommandHandler('summary', self.cmd_summary))
        self.app.add_handler(CommandHandler('status', self.cmd_status))
        
        logger.info("Telegram bot initialized successfully")
    
    async def stop(self):
        """Stop Telegram bot"""
        if self.app:
            await self.app.stop()
            await self.app.shutdown()
            logger.info("Telegram bot stopped")
    
    async def run_polling(self):
        """Run bot with polling"""
        if self.app:
            await self.app.start()
            await self.app.updater.start_polling()
            try:
                # Keep running
                await asyncio.Event().wait()
            finally:
                await self.app.updater.stop()
                await self.app.stop()
    
    async def send_message(self, message: str, chat_id: Optional[str] = None):
        """Send message to Telegram"""
        try:
            from telegram import Bot
            bot = Bot(token=self.token)
            target_chat = chat_id or self.chat_id
            await bot.send_message(chat_id=target_chat, text=message, parse_mode='HTML')
            logger.debug(f"Message sent to Telegram")
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
    
    async def send_signal_alert(self, signal: dict):
        """Send signal alert to Telegram"""
        message = format_signal_alert(signal)
        await self.send_message(message)
    
    # Command Handlers
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        message = f"""
🤖 <b>Crypto Market Intelligence Bot</b>

Welcome! I'm here to help you with market analysis and trading signals.

Use /help to see all available commands.
        """.strip()
        await update.message.reply_text(message, parse_mode='HTML')
        logger.info(f"User {update.effective_user.id} started the bot")
    
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        message = format_help_message()
        await update.message.reply_text(message, parse_mode='HTML')
    
    async def cmd_top(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /top command"""
        signals = db.get_recent_signals(limit=10)
        message = format_top_opportunities(signals)
        await update.message.reply_text(message, parse_mode='HTML')
        logger.info("User requested /top command")
    
    async def cmd_buy(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /buy command"""
        signals = db.get_signals_by_action('BUY LONG', limit=20)
        
        if signals:
            message = "<b>📈 RECENT BUY LONG SIGNALS</b>\n\n"
            for signal in signals:
                message += (
                    f"<b>{signal['coin']}</b>\n"
                    f"Confidence: {signal['confidence']}%\n"
                    f"Time: {signal['timestamp']}\n\n"
                )
        else:
            message = "📈 No BUY signals in database yet."
        
        await update.message.reply_text(message, parse_mode='HTML')
        logger.info("User requested /buy command")
    
    async def cmd_sell(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /sell command"""
        signals = db.get_signals_by_action('SELL SHORT', limit=20)
        
        if signals:
            message = "<b>📉 RECENT SELL SHORT SIGNALS</b>\n\n"
            for signal in signals:
                message += (
                    f"<b>{signal['coin']}</b>\n"
                    f"Confidence: {signal['confidence']}%\n"
                    f"Time: {signal['timestamp']}\n\n"
                )
        else:
            message = "📉 No SELL signals in database yet."
        
        await update.message.reply_text(message, parse_mode='HTML')
        logger.info("User requested /sell command")
    
    async def cmd_summary(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /summary command"""
        stats = db.get_daily_stats()
        signals = db.get_recent_signals(limit=5)
        message = format_daily_summary(stats, signals)
        await update.message.reply_text(message, parse_mode='HTML')
        logger.info("User requested /summary command")
    
    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        uptime = datetime.utcnow() - self.start_time
        stats = db.get_daily_stats()
        
        status_data = {
            'status': '🟢 ONLINE',
            'uptime': f"{uptime.seconds // 3600}h {(uptime.seconds % 3600) // 60}m",
            'signals_today': stats.get('total_signals', 0),
            'last_alert': stats.get('last_signal_time', 'Never')
        }
        
        message = format_status_message(status_data)
        await update.message.reply_text(message, parse_mode='HTML')
        logger.info("User requested /status command")
