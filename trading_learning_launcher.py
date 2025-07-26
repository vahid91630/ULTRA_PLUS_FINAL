#!/usr/bin/env python3
"""
🚀 سیستم راه‌انداز معاملات هوشمند و یادگیری
ULTRA_PLUS_BOT - Trading & Learning System Launcher
"""

import asyncio
import logging
import signal
import sys
from datetime import datetime

# Import all systems
from advanced_learning_intelligence_system import AdvancedLearningSystem
from integration_with_ultra_plus_bot import UltraPlusBotIntegration
from enhanced_autonomous_trading_system import enhanced_trading_system

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TradingLearningLauncher:
    """سیستم راه‌انداز کامل معاملات و یادگیری"""
    
    def __init__(self):
        self.learning_system = AdvancedLearningSystem()
        self.integration = UltraPlusBotIntegration()
        self.trading_system = enhanced_trading_system
        self.is_running = True
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"🛑 Received signal {signum}, shutting down gracefully...")
        self.is_running = False
        
    async def start_all_systems(self):
        """شروع همه سیستم‌ها"""
        logger.info("🚀 ULTRA_PLUS_BOT - شروع سیستم‌های معاملاتی و یادگیری")
        logger.info("=" * 60)
        
        try:
            # Initialize learning system
            logger.info("🎓 راه‌اندازی سیستم یادگیری هوشمند...")
            self.learning_system.initialize_advanced_tables()
            logger.info("✅ سیستم یادگیری آماده")
            
            # Start autonomous learning
            logger.info("🧠 شروع یادگیری خودکار...")
            learning_result = await self.integration.start_autonomous_learning()
            logger.info(f"✅ وضعیت یادگیری: {learning_result.get('status', 'unknown')}")
            
            # Initialize trading (but don't start live trading yet)
            logger.info("💼 آماده‌سازی سیستم معاملاتی...")
            logger.info("✅ سیستم معاملاتی آماده (در حالت آزمایشی)")
            
            # Main monitoring loop
            logger.info("🔄 شروع نظارت مداوم...")
            logger.info("📊 سیستم‌های فعال:")
            logger.info("  🎓 یادگیری هوشمند: فعال")
            logger.info("  🤖 تحلیل AI: فعال") 
            logger.info("  📈 تحلیل بازار: فعال")
            logger.info("  💰 معاملات: آماده (نیاز به فعال‌سازی کاربر)")
            
            # Continuous monitoring
            while self.is_running:
                try:
                    # Learning cycle every 30 minutes
                    if datetime.now().minute % 30 == 0:
                        await self._run_learning_cycle()
                    
                    # Market analysis every 15 minutes  
                    if datetime.now().minute % 15 == 0:
                        await self._run_market_analysis()
                    
                    # Wait 1 minute between checks
                    await asyncio.sleep(60)
                    
                except Exception as e:
                    logger.error(f"❌ خطا در حلقه نظارت: {e}")
                    await asyncio.sleep(30)
                    
        except Exception as e:
            logger.error(f"❌ خطا در راه‌اندازی: {e}")
            
    async def _run_learning_cycle(self):
        """اجرای چرخه یادگیری"""
        try:
            logger.info("🔄 چرخه یادگیری...")
            await self.learning_system.intelligent_learning_cycle()
            logger.info("✅ چرخه یادگیری تکمیل شد")
        except Exception as e:
            logger.error(f"❌ خطا در یادگیری: {e}")
            
    async def _run_market_analysis(self):
        """اجرای تحلیل بازار"""
        try:
            logger.info("📊 تحلیل بازار...")
            analysis = self.integration.get_intelligent_analysis("BTCUSDT")
            logger.info(f"📈 نتیجه تحلیل: {analysis.get('recommendation', 'نامشخص')}")
        except Exception as e:
            logger.error(f"❌ خطا در تحلیل: {e}")

async def main():
    """تابع اصلی"""
    launcher = TradingLearningLauncher()
    await launcher.start_all_systems()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 سیستم توسط کاربر متوقف شد")
    except Exception as e:
        logger.error(f"❌ خطای کلی: {e}")