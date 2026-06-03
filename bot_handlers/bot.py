from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
import asyncio
from datetime import datetime
from config import Config
from bot_handlers.handlers import handlers
from core.alert_scheduler import alert_scheduler
from utils.logger import get_logger

logger = get_logger(__name__)

class TelegramBot:
    """Main Telegram bot class"""
    
    def __init__(self):
        self.app = None
        self.running = False
    
    async def initialize(self):
        """Initialize the bot"""
        self.app = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
        
        # Register command handlers
        self.app.add_handler(CommandHandler("start", handlers.start))
        self.app.add_handler(CommandHandler("help", handlers.help_command))
        self.app.add_handler(CommandHandler("summary", handlers.summary))
        self.app.add_handler(CommandHandler("top", handlers.top_opportunities))
        self.app.add_handler(CommandHandler("buy", handlers.buy_signal))
        self.app.add_handler(CommandHandler("portfolio", handlers.portfolio))
        self.app.add_handler(CommandHandler("news", handlers.news))
        self.app.add_handler(CommandHandler("status", handlers.status))
        self.app.add_handler(CommandHandler("language", handlers.language_command))
        
        self.running = True
        logger.info("Bot initialized successfully")
    
    async def run_polling(self):
        """Run the bot with polling"""
        if not self.app:
            raise RuntimeError("Bot not initialized")
        
        try:
            # Start background alert scheduler
            asyncio.create_task(self.start_background_tasks())
            
            # Start polling
            await self.app.run_polling(allowed_updates=Update.ALL_TYPES)
        except Exception as e:
            logger.error(f"Error in polling: {e}")
            raise
    
    async def start_background_tasks(self):
        """Start background tasks"""
        while self.running:
            try:
                # Could add background scan tasks here
                await asyncio.sleep(60)
            except Exception as e:
                logger.error(f"Error in background tasks: {e}")
                await asyncio.sleep(60)
    
    async def send_message(self, chat_id: str, message: str):
        """Send message to user"""
        try:
            if self.app:
                await self.app.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
                logger.info(f"Message sent to {chat_id}")
        except Exception as e:
            logger.error(f"Error sending message: {e}")
    
    async def stop(self):
        """Stop the bot"""
        self.running = False
        if self.app:
            await self.app.stop()
        logger.info("Bot stopped")
