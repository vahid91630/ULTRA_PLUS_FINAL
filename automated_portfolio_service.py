#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سرویس خودکار مدیریت پورتفولیو
اجرای مداوم چک‌های هوشمند و ارسال پیام‌های نگهداری
"""

import asyncio
import time
from datetime import datetime
import logging
from smart_portfolio_manager import SmartPortfolioManager
from portfolio_notification_system import PortfolioNotificationSystem

# تنظیم لاگینگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class AutomatedPortfolioService:
    def __init__(self):
        """راه‌اندازی سرویس خودکار پورتفولیو"""
        
        self.portfolio_manager = SmartPortfolioManager()
        self.notification_system = PortfolioNotificationSystem()
        
        # تنظیمات زمان‌بندی
        self.check_intervals = {
            'portfolio_check': 300,      # هر 5 دقیقه بررسی کلی پورتفولیو
            'notification_cycle': 1800,  # هر 30 دقیقه بررسی پیام‌ها
            'position_analysis': 900,    # هر 15 دقیقه تحلیل موقعیت‌ها
            'market_opportunity': 600    # هر 10 دقیقه بررسی فرصت‌ها
        }
        
        # آخرین زمان اجرای هر وظیفه
        self.last_execution = {
            'portfolio_check': 0,
            'notification_cycle': 0,
            'position_analysis': 0,
            'market_opportunity': 0
        }
        
        # آمار عملکرد
        self.performance_stats = {
            'total_cycles': 0,
            'notifications_sent': 0,
            'positions_analyzed': 0,
            'wallet_checks': 0,
            'start_time': datetime.now(),
            'uptime_seconds': 0
        }
        
        self.is_running = False
        
        logger.info("🚀 سرویس خودکار پورتفولیو آماده شد")

    async def check_portfolio_status(self) -> dict:
        """بررسی وضعیت کلی پورتفولیو"""
        
        try:
            # اجرای چرخه معاملاتی هوشمند
            result = await self.portfolio_manager.execute_smart_trading_cycle()
            
            self.performance_stats['wallet_checks'] += 1
            
            logger.info(f"💼 بررسی پورتفولیو: ${result['wallet_summary']['total_usd']:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ خطا در بررسی پورتفولیو: {e}")
            return {'error': str(e)}

    async def run_notification_cycle(self, wallet_data: dict = None) -> dict:
        """اجرای چرخه اطلاع‌رسانی"""
        
        try:
            result = await self.notification_system.run_notification_cycle(wallet_data)
            
            self.performance_stats['notifications_sent'] += result['total_notifications']
            
            if result['total_notifications'] > 0:
                logger.info(f"📨 {result['total_notifications']} پیام جدید ایجاد شد")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ خطا در چرخه اطلاع‌رسانی: {e}")
            return {'error': str(e)}

    async def analyze_positions(self) -> dict:
        """تحلیل موقعیت‌های فعال"""
        
        try:
            notifications = await self.portfolio_manager.check_active_positions()
            
            self.performance_stats['positions_analyzed'] += len(notifications)
            
            if notifications:
                logger.info(f"📊 {len(notifications)} موقعیت فعال تحلیل شد")
            
            return {
                'positions_checked': len(notifications),
                'notifications': notifications,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ خطا در تحلیل موقعیت‌ها: {e}")
            return {'error': str(e)}

    def should_execute_task(self, task_name: str) -> bool:
        """بررسی اینکه آیا وقت اجرای وظیفه رسیده یا نه"""
        
        current_time = time.time()
        last_time = self.last_execution[task_name]
        interval = self.check_intervals[task_name]
        
        return (current_time - last_time) >= interval

    async def execute_scheduled_tasks(self):
        """اجرای وظایف زمان‌بندی شده"""
        
        current_time = time.time()
        tasks_executed = []
        
        # بررسی پورتفولیو
        if self.should_execute_task('portfolio_check'):
            portfolio_result = await self.check_portfolio_status()
            tasks_executed.append('portfolio_check')
            self.last_execution['portfolio_check'] = current_time
            
            # اگر بررسی پورتفولیو موفق بود، چرخه اطلاع‌رسانی اجرا کن
            if 'wallet_summary' in portfolio_result:
                if self.should_execute_task('notification_cycle'):
                    await self.run_notification_cycle(portfolio_result['wallet_summary'])
                    tasks_executed.append('notification_cycle')
                    self.last_execution['notification_cycle'] = current_time
        
        # تحلیل موقعیت‌ها
        if self.should_execute_task('position_analysis'):
            await self.analyze_positions()
            tasks_executed.append('position_analysis')
            self.last_execution['position_analysis'] = current_time
        
        return tasks_executed

    def update_performance_stats(self):
        """به‌روزرسانی آمار عملکرد"""
        
        self.performance_stats['total_cycles'] += 1
        self.performance_stats['uptime_seconds'] = (
            datetime.now() - self.performance_stats['start_time']
        ).total_seconds()

    def get_service_status(self) -> dict:
        """دریافت وضعیت سرویس"""
        
        uptime_hours = self.performance_stats['uptime_seconds'] / 3600
        
        return {
            'service_status': 'RUNNING' if self.is_running else 'STOPPED',
            'uptime_hours': uptime_hours,
            'total_cycles': self.performance_stats['total_cycles'],
            'wallet_checks': self.performance_stats['wallet_checks'],
            'positions_analyzed': self.performance_stats['positions_analyzed'],
            'notifications_sent': self.performance_stats['notifications_sent'],
            'average_cycle_time': uptime_hours / max(1, self.performance_stats['total_cycles']),
            'last_execution_times': {
                task: datetime.fromtimestamp(time_val).strftime('%H:%M:%S') if time_val > 0 else 'هرگز'
                for task, time_val in self.last_execution.items()
            },
            'next_execution_times': {
                task: datetime.fromtimestamp(
                    self.last_execution[task] + self.check_intervals[task]
                ).strftime('%H:%M:%S') if self.last_execution[task] > 0 else 'هرگز'
                for task in self.check_intervals.keys()
            }
        }

    async def run_service(self):
        """اجرای اصلی سرویس"""
        
        logger.info("🚀 شروع سرویس خودکار پورتفولیو...")
        logger.info("=" * 60)
        logger.info("📊 برنامه زمان‌بندی:")
        logger.info(f"  • بررسی پورتفولیو: هر {self.check_intervals['portfolio_check']//60} دقیقه")
        logger.info(f"  • چرخه اطلاع‌رسانی: هر {self.check_intervals['notification_cycle']//60} دقیقه")
        logger.info(f"  • تحلیل موقعیت‌ها: هر {self.check_intervals['position_analysis']//60} دقیقه")
        logger.info("=" * 60)
        
        self.is_running = True
        
        try:
            while self.is_running:
                # اجرای وظایف زمان‌بندی شده
                executed_tasks = await self.execute_scheduled_tasks()
                
                # به‌روزرسانی آمار
                self.update_performance_stats()
                
                # نمایش آمار هر 50 چرخه
                if self.performance_stats['total_cycles'] % 50 == 0:
                    status = self.get_service_status()
                    logger.info(f"📊 آمار سرویس: {status['total_cycles']} چرخه، "
                              f"{status['uptime_hours']:.1f} ساعت فعال، "
                              f"{status['notifications_sent']} پیام ارسال شده")
                
                # استراحت 30 ثانیه
                await asyncio.sleep(30)
                
        except KeyboardInterrupt:
            logger.info("⏹️ توقف سرویس توسط کاربر")
        except Exception as e:
            logger.error(f"❌ خطای غیرمنتظره در سرویس: {e}")
        finally:
            self.is_running = False
            logger.info("🔴 سرویس خودکار پورتفولیو متوقف شد")

    def stop_service(self):
        """توقف سرویس"""
        self.is_running = False
        logger.info("🔴 درخواست توقف سرویس دریافت شد")

# اجرای مستقل سرویس
async def main():
    """اجرای اصلی سرویس"""
    
    service = AutomatedPortfolioService()
    
    print("🔄 راه‌اندازی سرویس خودکار مدیریت پورتفولیو...")
    print("=" * 60)
    print("🎯 این سرویس کارهای زیر را انجام می‌دهد:")
    print("  ✅ مدیریت هوشمند ولت و تقسیم‌بندی سرمایه")
    print("  ✅ بررسی موقعیت‌های فعال و ارسال هشدار نگهداری") 
    print("  ✅ پیشنهاد افزایش سرمایه در فرصت‌های مناسب")
    print("  ✅ تحلیل AI برای بهترین زمان فروش/نگهداری")
    print("  ✅ محدودیت پیام روزانه برای جلوگیری از اسپم")
    print("=" * 60)
    print("💡 برای توقف: Ctrl+C")
    print()
    
    await service.run_service()

if __name__ == "__main__":
    asyncio.run(main())