#!/usr/bin/env python3
"""
AI Crypto Futures Market Intelligence Bot

Main entry point for the bot.
"""

import asyncio
import signal
import sys
from datetime import datetime
from config import Config, get_config
from utils.logger import get_logger, setup_logging
from telegram.bot import TelegramBot
from core.scanner import Scanner

logger = None
bot = None
scanner = None

async def main():
    """Main entry point"""
    global logger, bot, scanner
    
    # Setup logging
    setup_logging(Config.LOG_LEVEL)
    logger = get_logger(__name__)
    
    logger.info("="*60)
    logger.info("AI Crypto Futures Market Intelligence Bot")
    logger.info(f"Started at {datetime.utcnow().isoformat()} UTC")
    logger.info("="*60)
    
    try:
        # Validate configuration
        Config.validate()
        logger.info("Configuration validated successfully")
        
        # Initialize Telegram bot
        bot = TelegramBot()
        await bot.initialize()
        logger.info("Telegram bot initialized")
        
        # Initialize scanner
        scanner = Scanner(bot)
        logger.info("Market scanner initialized")
        
        # Start scanning
        await scanner.start()
        
    except KeyboardInterrupt:
        logger.info("Bot interrupted by user")
        await shutdown()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        await shutdown()
        sys.exit(1)

async def shutdown():
    """Graceful shutdown"""
    global bot, scanner
    
    logger.info("Shutting down bot...")
    
    if scanner:
        await scanner.stop()
    
    if bot:
        await bot.stop()
    
    logger.info("Bot shutdown complete")

def handle_signal(signum, frame):
    """Handle system signals"""
    logger.info(f"Received signal {signum}")
    asyncio.create_task(shutdown())

if __name__ == '__main__':
    # Register signal handlers
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    
    # Run bot
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        sys.exit(0)
