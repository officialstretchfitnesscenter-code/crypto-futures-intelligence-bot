import aiohttp
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from utils.logger import get_logger

logger = get_logger(__name__)

class NewsAggregator:
    """Aggregate crypto news from multiple sources"""
    
    def __init__(self):
        self.rss_feeds = [
            'https://feeds.bloomberg.com/markets/cryptocurrency.rss',
            'https://cointelegraph.com/feed/',
            'https://bitcoinmagazine.com/feed',
            'https://www.coindesk.com/arc/outboundfeeds/rss/',
            'https://messari.io/news/feed'
        ]
        self.news_cache = []
        self.last_update = None
    
    async def fetch_news(self, query: str = 'crypto', limit: int = 10) -> List[Dict]:
        """Fetch latest crypto news"""
        news = []
        
        try:
            async with aiohttp.ClientSession() as session:
                for feed_url in self.rss_feeds:
                    try:
                        async with session.get(feed_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                            if response.status == 200:
                                feed_data = await response.text()
                                feed = feedparser.parse(feed_data)
                                
                                for entry in feed.entries[:5]:
                                    news.append({
                                        'title': entry.get('title', ''),
                                        'link': entry.get('link', ''),
                                        'published': entry.get('published', ''),
                                        'summary': entry.get('summary', '')[:200],
                                        'source': feed.feed.get('title', 'Unknown')
                                    })
                    except Exception as e:
                        logger.warning(f"Error fetching from {feed_url}: {e}")
                        continue
            
            # Remove duplicates
            unique_news = []
            seen_titles = set()
            for item in news:
                if item['title'] not in seen_titles:
                    unique_news.append(item)
                    seen_titles.add(item['title'])
            
            self.news_cache = sorted(unique_news, key=lambda x: x.get('published', ''), reverse=True)[:limit]
            self.last_update = datetime.utcnow()
            
            return self.news_cache
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return []
    
    async def get_coin_news(self, coin: str, limit: int = 5) -> List[Dict]:
        """Get news for specific coin"""
        news = await self.fetch_news(query=coin, limit=limit*2)
        return [n for n in news if coin.lower() in n['title'].lower()][:limit]
    
    def get_cached_news(self) -> List[Dict]:
        """Get cached news"""
        return self.news_cache

news_aggregator = NewsAggregator()
