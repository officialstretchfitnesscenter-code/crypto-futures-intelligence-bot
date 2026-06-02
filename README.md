# AI Crypto Futures Market Intelligence Bot

A production-grade crypto futures market intelligence bot that monitors OKX USDT perpetual futures pairs, performs multi-timeframe analysis, and sends high-confidence trading alerts to Telegram.

## Features

- ✅ Hourly market scans across all OKX USDT perpetual pairs
- ✅ Multi-timeframe analysis (15m, 1H, 4H, 1D)
- ✅ Intraday and Swing trade support
- ✅ Advanced confidence scoring (0-100 scale)
- ✅ Market structure, trend, and volume analysis
- ✅ Open Interest (OI) change tracking
- ✅ Relative Volume (RVOL) analysis
- ✅ Duplicate alert prevention with 6-hour cooldown
- ✅ SQLite database for signal history
- ✅ Telegram integration with structured alerts
- ✅ Daily market summaries
- ✅ Health monitoring and status reporting

## Important

**This bot is NOT an auto-trading bot.** It performs market analysis and sends alerts to Telegram. The user makes all final trading decisions.

## Tech Stack

- **Language:** Python 3.9+
- **Database:** SQLite
- **API Client:** OKX Public API
- **Notifications:** Telegram Bot API
- **Async:** asyncio

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the root directory:

```env
# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# OKX API
OKX_API_KEY=your_api_key
OKX_API_SECRET=your_api_secret
OKX_PASSPHRASE=your_passphrase

# Bot Configuration
SCAN_INTERVAL_HOURS=1
CONFIDENCE_THRESHOLD=88
ALERT_COOLDOWN_HOURS=6
ENABLE_DEBUG=False
```

## Usage

```bash
python main.py
```

The bot will:
1. Start scanning the market every 1 hour
2. Send Telegram alerts for high-confidence signals
3. Store all signals in the database
4. Generate daily market summaries

## Project Structure

```
crypto-futures-intelligence-bot/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── .env                    # Configuration (create this)
├── config.py              # Configuration management
├── database.py            # SQLite operations
├── core/
│   ├── __init__.py
│   ├── okx_client.py      # OKX API client
│   ├── analyzer.py        # Multi-timeframe analysis engine
│   ├── confidence.py      # Confidence scoring
│   ├── risk.py           # Risk classification
│   └── scanner.py        # Market scanner
├── models/
│   ├── __init__.py
│   ├── candle.py         # Candle data model
│   ├── signal.py         # Signal model
│   └── pair.py           # Trading pair model
├── telegram/
│   ├── __init__.py
│   ├── bot.py            # Telegram bot
│   └── formatter.py      # Alert formatting
├── utils/
│   ├── __init__.py
│   ├── logger.py         # Logging
│   ├── cache.py          # Caching mechanism
│   └── helpers.py        # Utility functions
└── tests/
    ├── __init__.py
    ├── test_analyzer.py
    └── test_signals.py
```

## Telegram Commands

- `/top` - Show top opportunities
- `/buy` - Show recent BUY LONG signals
- `/sell` - Show recent SELL SHORT signals
- `/summary` - Get daily market summary
- `/status` - Bot status and stats

## Alert Format

```
🚨 MARKET ALERT

Coin: XRPUSDT
Action: BUY LONG
Type: SWING
Confidence: 92%
Risk: LOW

Reason:
• RVOL 4.2x above average
• Open Interest +15%
• 4H resistance breakout
• Higher timeframe trend bullish

Bot View:
Current market structure favors upside continuation.

Price: 2.35
Timeframe: 4H
Time: 2026-06-02 18:00 UTC
```

## Database Schema

Signals are stored with:
- Coin
- Action (BUY LONG / SELL SHORT)
- Signal Type (INTRADAY / SWING)
- Confidence Score
- Risk Level
- Analysis Reasons
- Bot View
- Price
- Timeframe
- Timestamp
- 6-hour Cooldown

## Key Restrictions

1. ❌ Never place trades
2. ❌ Never auto-execute
3. ❌ Never claim guaranteed profits
4. ✅ User always makes final decision
5. ✅ Focus on opportunity discovery
6. ✅ Quality over quantity
7. ✅ Minimize notification noise
8. ✅ Only high-confidence alerts

## License

MIT
