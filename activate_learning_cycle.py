#!/usr/bin/env python3
"""
فعال‌سازی چرخه یادگیری مداوم
"""

import os
import asyncio
import schedule
import time
import threading
from intelligent_trading_bot import IntelligentTradingBot
from integration_with_ultra_plus_bot import UltraPlusBotIntegration

# منابع آموزشی مالی
EDUCATIONAL_SOURCES = [
    "https://api.coingecko.com/api/v3/global",
    "https://api.coingecko.com/api/v3/trending",
    "https://api.coingecko.com/api/v3/search/trending",
    "https://api.mexc.com/api/v3/ticker/24hr",
    "https://api.mexc.com/api/v3/ticker/price"
]

class ContinuousLearningSystem:
    def __init__(self):
        self.bot = IntelligentTradingBot()
        self.integration = UltraPlusBotIntegration()
        self.is_running = False
        
    async def collect_real_market_data(self):
        """جمع‌آوری داده‌های واقعی بازار"""
        print("📊 جمع‌آوری داده‌های بازار...")
        
        try:
            # دریافت داده‌های قیمت
            market_data = self.bot.get_market_data("BTCUSDT")
            
            if "price" in market_data:
                # ایجاد محتوای آموزشی از داده‌های بازار
                content_text = f"""
                Bitcoin Market Analysis - {market_data['timestamp']}
                Current Price: ${market_data['price']:,.2f}
                24h Change: {market_data['change_24h']:.2f}%
                Volume: {market_data['volume']:,.0f}
                High 24h: ${market_data['high_24h']:,.2f}
                Low 24h: ${market_data['low_24h']:,.2f}
                
                Market Analysis:
                {"Bullish momentum detected" if market_data['change_24h'] > 0 else "Bearish pressure observed"}
                Volume indicates {"high" if market_data['volume'] > 1000000 else "moderate"} market activity.
                """
                
                # ذخیره محتوا در پایگاه داده
                await self.store_educational_content("Market Analysis", content_text, "Real-time data")
                print(f"✅ داده‌های بازار ذخیره شد - قیمت BTC: ${market_data['price']:,.2f}")
                return True
            
        except Exception as e:
            print(f"❌ خطا در جمع‌آوری داده‌ها: {e}")
        
        return False
    
    async def store_educational_content(self, title, content, source):
        """ذخیره محتوای آموزشی"""
        from intelligent_trading_bot import EducationalContent
        from datetime import datetime
        import hashlib
        
        try:
            # ایجاد شناسه منحصربه‌فرد
            content_id = hashlib.md5(f"{title}{content}".encode()).hexdigest()
            
            # ایجاد محتوای آموزشی
            educational_content = EducationalContent(
                id=content_id,
                title=title,
                source=source,
                url=source,
                content=content,
                summary="",
                extracted_insights=[],
                relevance_score=0.8,  # امتیاز بالا برای داده‌های واقعی
                timestamp=datetime.now(),
                tags=["market_data", "real_time"],
                sentiment_score=0.0,
                trading_signals=["ANALYZE"],
                market_indicators=["PRICE", "VOLUME"]
            )
            
            # تحلیل با هوش مصنوعی
            analyzed_content = self.bot.analyze_content_with_ai(educational_content)
            
            # ذخیره در پایگاه داده
            self.bot.save_content_to_database(analyzed_content)
            
            print(f"💾 محتوا ذخیره شد: {title}")
            return True
            
        except Exception as e:
            print(f"❌ خطا در ذخیره محتوا: {e}")
            return False
    
    async def learning_cycle(self):
        """چرخه یادگیری"""
        print("🎓 شروع چرخه یادگیری...")
        
        # جمع‌آوری داده‌های بازار
        await self.collect_real_market_data()
        
        # اندازه‌گیری هوش
        intelligence = self.bot.measure_intelligence()
        
        print(f"🧠 وضعیت هوش: {intelligence.accuracy_score:.1%}")
        print(f"📚 دانش: {intelligence.knowledge_base_size} مورد")
        
        # بررسی آمادگی برای معامله
        if intelligence.accuracy_score >= 0.8:
            print("🚀 سیستم آماده معامله واقعی است!")
            return True
        
        return False
    
    def start_continuous_learning(self):
        """شروع یادگیری مداوم"""
        print("🔄 فعال‌سازی یادگیری مداوم...")
        
        # تنظیم برنامه یادگیری
        schedule.every(30).minutes.do(self.run_learning_cycle)
        
        # اجرای فوری
        self.run_learning_cycle()
        
        # حلقه اجرا
        self.is_running = True
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # چک کردن هر دقیقه
    
    def run_learning_cycle(self):
        """اجرای چرخه یادگیری"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(self.learning_cycle())
            return result
        except Exception as e:
            print(f"❌ خطا در چرخه یادگیری: {e}")
            return False
        finally:
            loop.close()

def main():
    """اجرای اصلی"""
    print("🚀 فعال‌سازی سیستم یادگیری مداوم ULTRA_PLUS_BOT")
    print("=" * 60)
    
    learning_system = ContinuousLearningSystem()
    
    # شروع یادگیری در thread جداگانه
    learning_thread = threading.Thread(target=learning_system.start_continuous_learning)
    learning_thread.daemon = True
    learning_thread.start()
    
    print("✅ سیستم یادگیری فعال شد")
    print("📊 هر 30 دقیقه یک‌بار داده‌های جدید جمع‌آوری می‌شود")
    print("🎯 هدف: رسیدن به 80% دقت برای فعال‌سازی معامله واقعی")
    
    # نگه‌داشتن برنامه زنده
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n⏹️ متوقف کردن سیستم...")
        learning_system.is_running = False

if __name__ == "__main__":
    main()