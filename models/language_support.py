from typing import Dict

class LanguageSupport:
    """Multi-language support for bot messages"""
    
    LANGUAGES = {
        'en': 'English',
        'ur': 'اردو',
        'hi': 'हिन्दी',
        'ar': 'العربية',
        'zh': '中文',
        'es': 'Español',
        'fr': 'Français'
    }
    
    MESSAGES = {
        'en': {
            'welcome': '👋 Welcome to Crypto Intelligence Bot!',
            'help': '''📚 Available Commands:
/start - Start the bot
/status - Check bot status
/summary - Market summary
/top - Top opportunities
/buy <coin> - Get buy signals
/sell <coin> - Get sell signals
/portfolio - View your portfolio
/news - Latest crypto news
/analysis <coin> - Detailed analysis
/alerts - Set price alerts
/language - Change language
/help - Show this help''',
            'portfolio_empty': '📭 Your portfolio is empty',
            'buy_signal': '🟢 STRONG BUY SIGNAL',
            'sell_signal': '🔴 STRONG SELL SIGNAL',
            'neutral': '⚪ NEUTRAL',
        },
        'ur': {
            'welcome': '👋 کریپٹو انٹیلیجنس بوٹ میں خوش آمدید!',
            'help': '''📚 دستیاب کمانڈز:
/start - بوٹ شروع کریں
/status - بوٹ کی حالت چیک کریں
/summary - مارکیٹ خلاصہ
/top - بہترین مواقع
/buy - خریدنے کی سگنلز
/sell - فروخت سگنلز
/portfolio - اپنا پورٹ فولیو دیکھیں
/news - تازہ ترین اخبارات
/analysis - تفصیلی تجزیہ
/alerts - قیمت کی الرٹس
/language - زبان تبدیل کریں
/help - مدد دکھائیں''',
            'portfolio_empty': '📭 آپ کا پورٹ فولیو خالی ہے',
            'buy_signal': '🟢 مضبوط خریدنے کی سگنل',
            'sell_signal': '🔴 مضبوط فروخت کی سگنل',
            'neutral': '⚪ غیر متعین',
        },
        'hi': {
            'welcome': '👋 क्रिप्टो इंटेलिजेंस बॉट में स्वागत है!',
            'help': '''📚 उपलब्ध कमांड:
/start - बॉट शुरू करें
/status - बॉट की स्थिति जांचें
/summary - बाजार सारांश
/top - शीर्ष अवसर
/buy - खरीद संकेत
/sell - बिक्री संकेत
/portfolio - अपना पोर्टफोलियो देखें
/news - नवीनतम समाचार
/analysis - विस्तृत विश्लेषण
/alerts - मूल्य अलर्ट
/language - भाषा बदलें
/help - मदद दिखाएं''',
            'portfolio_empty': '📭 आपका पोर्टफोलियो खाली है',
            'buy_signal': '🟢 मजबूत खरीद संकेत',
            'sell_signal': '🔴 मजबूत बिक्री संकेत',
            'neutral': '⚪ तटस्थ',
        },
        'ar': {
            'welcome': '👋 مرحبا بك في بوت الذكاء الاصطناعي للعملات المشفرة!',
            'help': '''📚 الأوامر المتاحة:
/start - بدء البوت
/status - التحقق من حالة البوت
/summary - ملخص السوق
/top - أفضل الفرص
/buy - إشارات الشراء
/sell - إشارات البيع
/portfolio - عرض محفظتك
/news - أحدث الأخبار
/analysis - التحليل التفصيلي
/alerts - تنبيهات الأسعار
/language - تغيير اللغة
/help - عرض المساعدة''',
            'portfolio_empty': '📭 محفظتك فارغة',
            'buy_signal': '🟢 إشارة شراء قوية',
            'sell_signal': '🔴 إشارة بيع قوية',
            'neutral': '⚪ محايد',
        }
    }
    
    def __init__(self, language: str = 'en'):
        self.language = language if language in self.LANGUAGES else 'en'
    
    def set_language(self, language: str):
        """Set user language"""
        if language in self.LANGUAGES:
            self.language = language
            return True
        return False
    
    def get_message(self, key: str, default: str = '') -> str:
        """Get message in current language"""
        return self.MESSAGES.get(self.language, {}).get(key, default)
    
    def get_all_languages(self) -> Dict:
        """Get all available languages"""
        return self.LANGUAGES

language_support = LanguageSupport()
