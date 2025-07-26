#!/usr/bin/env python3
"""
🤖 ULTRA_PLUS_BOT - Persistent Telegram Bot Manager
مدیر مقاوم ربات تلگرام - مستقل از وضعیت مرورگر
"""

import os
import sys
import time
import signal
import logging
import subprocess
import threading
from datetime import datetime
from typing import Optional

# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('telegram_bot_persistent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PersistentTelegramBotManager:
    """مدیر مقاوم برای ربات تلگرام"""
    
    def __init__(self):
        self.bot_process: Optional[subprocess.Popen] = None
        self.is_running = True
        self.restart_count = 0
        self.max_restarts = 100
        self.restart_delay = 5
        self.last_restart_time = 0
        self.health_check_interval = 30
        self.bot_script = "simple_telegram_bot.py"
        
        # ثبت signal handlers
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
    def _signal_handler(self, signum, frame):
        """پردازش سیگنال‌های خروج"""
        logger.info(f"🛑 دریافت سیگنال {signum} - شروع خروج ایمن...")
        self.is_running = False
        if self.bot_process:
            self.bot_process.terminate()
    
    def check_bot_token(self) -> bool:
        """بررسی وجود توکن ربات"""
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token:
            logger.error("❌ توکن تلگرام (TELEGRAM_BOT_TOKEN) یافت نشد")
            return False
        
        logger.info("✅ توکن تلگرام موجود است")
        return True
    
    def start_bot_process(self) -> bool:
        """شروع پروسه ربات"""
        try:
            if not os.path.exists(self.bot_script):
                logger.error(f"❌ فایل {self.bot_script} یافت نشد")
                return False
            
            # اجرای ربات در پروسه جداگانه
            self.bot_process = subprocess.Popen(
                [sys.executable, self.bot_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1
            )
            
            logger.info(f"🚀 ربات تلگرام شروع شد (PID: {self.bot_process.pid})")
            return True
            
        except Exception as e:
            logger.error(f"❌ خطا در شروع ربات: {e}")
            return False
    
    def is_bot_alive(self) -> bool:
        """بررسی زنده بودن ربات"""
        if not self.bot_process:
            return False
        
        # بررسی وضعیت پروسه
        poll_result = self.bot_process.poll()
        return poll_result is None
    
    def stop_bot_process(self):
        """متوقف کردن پروسه ربات"""
        if self.bot_process:
            try:
                logger.info("🛑 متوقف کردن ربات...")
                self.bot_process.terminate()
                
                # انتظار برای خروج عادی
                try:
                    self.bot_process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    logger.warning("⚠️ ربات در زمان مناسب خارج نشد - کشتن اجباری...")
                    self.bot_process.kill()
                    self.bot_process.wait()
                
                logger.info("✅ ربات متوقف شد")
                
            except Exception as e:
                logger.error(f"❌ خطا در متوقف کردن ربات: {e}")
            finally:
                self.bot_process = None
    
    def restart_bot_if_needed(self) -> bool:
        """راه‌اندازی مجدد ربات در صورت نیاز"""
        current_time = time.time()
        
        # جلوگیری از restart مکرر
        if current_time - self.last_restart_time < self.restart_delay:
            return False
        
        # بررسی تعداد restart
        if self.restart_count >= self.max_restarts:
            logger.critical(f"🚨 حداکثر تعداد restart ({self.max_restarts}) رسیده")
            return False
        
        # متوقف کردن پروسه قبلی
        self.stop_bot_process()
        
        # انتظار کوتاه
        time.sleep(2)
        
        # شروع پروسه جدید
        if self.start_bot_process():
            self.restart_count += 1
            self.last_restart_time = current_time
            logger.info(f"🔄 ربات راه‌اندازی مجدد شد (تعداد: {self.restart_count})")
            return True
        
        return False
    
    def monitor_bot_output(self):
        """نمایش خروجی ربات"""
        if not self.bot_process or not self.bot_process.stdout:
            return
        
        try:
            # خواندن خروجی به صورت non-blocking
            while self.is_running and self.is_bot_alive():
                if self.bot_process and self.bot_process.stdout:
                    line = self.bot_process.stdout.readline()
                    if line:
                        print(f"[BOT] {line.strip()}")
                    else:
                        time.sleep(0.1)
                else:
                    break
                    
        except Exception as e:
            logger.error(f"❌ خطا در خواندن خروجی ربات: {e}")
    
    def run(self):
        """اجرای مدیر مقاوم"""
        logger.info("🤖 ULTRA_PLUS_BOT - مدیر مقاوم ربات تلگرام")
        logger.info("=" * 60)
        logger.info("✅ مستقل از وضعیت مرورگر")
        logger.info("🔄 راه‌اندازی مجدد خودکار")
        logger.info("🛡️ مقاوم در برابر خرابی")
        logger.info("🌐 اتصال مستقل به اینترنت")
        logger.info("=" * 60)
        
        # بررسی پیش‌نیازها
        if not self.check_bot_token():
            logger.critical("❌ پیش‌نیازهای ربات برآورده نشده")
            return
        
        # شروع ربات
        if not self.start_bot_process():
            logger.critical("❌ نتوانست ربات را شروع کند")
            return
        
        # شروع thread برای نمایش خروجی
        output_thread = threading.Thread(target=self.monitor_bot_output, daemon=True)
        output_thread.start()
        
        logger.info("🔍 شروع نظارت بر ربات...")
        
        # حلقه نظارت اصلی
        last_health_check = time.time()
        
        while self.is_running:
            try:
                current_time = time.time()
                
                # بررسی سلامت ربات
                if current_time - last_health_check >= self.health_check_interval:
                    if not self.is_bot_alive():
                        logger.warning("⚠️ ربات متوقف شده - تلاش برای راه‌اندازی مجدد...")
                        
                        if not self.restart_bot_if_needed():
                            logger.critical("❌ نتوانست ربات را مجدداً راه‌اندازی کند")
                            break
                    else:
                        logger.debug("✅ ربات سالم است")
                    
                    last_health_check = current_time
                
                # استراحت کوتاه
                time.sleep(5)
                
            except KeyboardInterrupt:
                logger.info("🛑 دریافت درخواست توقف از کاربر")
                break
            except Exception as e:
                logger.error(f"❌ خطا در حلقه نظارت: {e}")
                time.sleep(10)
        
        # پاکسازی
        logger.info("🧹 شروع پاکسازی...")
        self.stop_bot_process()
        logger.info("🏁 مدیر مقاوم ربات خاتمه یافت")
        
        # گزارش نهایی
        logger.info(f"📊 آمار نهایی: {self.restart_count} بار راه‌اندازی مجدد")

def main():
    """تابع اصلی"""
    manager = PersistentTelegramBotManager()
    
    try:
        manager.run()
    except Exception as e:
        logger.critical(f"💥 خطای مهلک در مدیر: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()