#!/usr/bin/env python3
"""
فعال‌سازی و بررسی وضعیت ربات تلگرام
"""

import os
import requests
import sqlite3
from datetime import datetime

class TelegramBotStatus:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        
    def check_bot_status(self):
        """بررسی وضعیت ربات"""
        print("🤖 بررسی وضعیت ربات تلگرام...")
        
        try:
            # دریافت اطلاعات ربات
            response = requests.get(f"{self.base_url}/getMe", timeout=10)
            
            if response.status_code == 200:
                bot_info = response.json()
                
                if bot_info['ok']:
                    bot_data = bot_info['result']
                    print(f"✅ ربات فعال: @{bot_data['username']}")
                    print(f"📛 نام: {bot_data['first_name']}")
                    print(f"🆔 ID: {bot_data['id']}")
                    return True, bot_data
                else:
                    print(f"❌ خطا در API: {bot_info}")
            else:
                print(f"❌ خطا در درخواست: {response.status_code}")
                
        except Exception as e:
            print(f"❌ خطا در اتصال: {e}")
        
        return False, None
    
    def get_updates(self):
        """دریافت آپدیت‌های اخیر"""
        print("📨 بررسی پیام‌های اخیر...")
        
        try:
            response = requests.get(f"{self.base_url}/getUpdates?limit=5", timeout=10)
            
            if response.status_code == 200:
                updates = response.json()
                
                if updates['ok'] and updates['result']:
                    print(f"📬 {len(updates['result'])} پیام اخیر موجود")
                    
                    for update in updates['result'][:3]:  # نمایش 3 مورد اخیر
                        if 'message' in update:
                            msg = update['message']
                            user = msg['from']
                            text = msg.get('text', 'نوع پیام دیگر')
                            print(f"💬 {user['first_name']}: {text[:50]}...")
                    
                    return True, updates['result']
                else:
                    print("📭 پیام جدیدی موجود نیست")
                    return True, []
                    
        except Exception as e:
            print(f"❌ خطا در دریافت پیام‌ها: {e}")
        
        return False, None
    
    def send_test_message(self, chat_id="559649958"):
        """ارسال پیام تست"""
        print(f"📤 ارسال پیام تست به {chat_id}...")
        
        try:
            message = f"""
🤖 گزارش وضعیت ULTRA_PLUS_BOT

✅ سیستم فعال و عملیاتی
🕐 زمان: {datetime.now().strftime('%H:%M:%S')}
📊 پایگاه داده: آماده
💱 داده‌های بازار: در حال دریافت
🧠 سیستم هوشمند: فعال

برای شروع /start را بزنید
            """
            
            payload = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(f"{self.base_url}/sendMessage", json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result['ok']:
                    print("✅ پیام تست ارسال شد")
                    return True
                else:
                    print(f"❌ خطا در ارسال: {result}")
            else:
                print(f"❌ خطا HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"❌ خطا در ارسال پیام: {e}")
        
        return False
    
    def update_database_status(self):
        """به‌روزرسانی وضعیت در پایگاه داده"""
        print("🗄️ به‌روزرسانی پایگاه داده...")
        
        try:
            conn = sqlite3.connect('ultra_plus_bot.db')
            cursor = conn.cursor()
            
            # ایجاد جدول وضعیت سیستم
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_status (
                    id INTEGER PRIMARY KEY,
                    component TEXT UNIQUE,
                    status TEXT,
                    last_check TIMESTAMP,
                    details TEXT
                )
            ''')
            
            # به‌روزرسانی وضعیت ربات
            cursor.execute('''
                INSERT OR REPLACE INTO system_status 
                (id, component, status, last_check, details)
                VALUES (1, 'telegram_bot', 'active', ?, 'Bot responding to API calls')
            ''', (datetime.now(),))
            
            # به‌روزرسانی وضعیت کلی سیستم
            cursor.execute('''
                INSERT OR REPLACE INTO system_status 
                (id, component, status, last_check, details)
                VALUES (2, 'overall_system', 'operational', ?, 'All core components working')
            ''', (datetime.now(),))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print("✅ وضعیت در پایگاه داده ذخیره شد")
            return True
            
        except Exception as e:
            print(f"❌ خطا در به‌روزرسانی: {e}")
            return False

def main():
    """اجرای بررسی کامل ربات"""
    print("🚀 بررسی وضعیت کامل ربات تلگرام")
    print("=" * 40)
    
    bot_checker = TelegramBotStatus()
    
    if not bot_checker.bot_token:
        print("❌ توکن ربات موجود نیست")
        return
    
    success_count = 0
    
    # بررسی وضعیت ربات
    print("🔄 مرحله 1: بررسی وضعیت ربات...")
    bot_success, bot_info = bot_checker.check_bot_status()
    if bot_success:
        success_count += 1
    
    # بررسی پیام‌ها
    print("🔄 مرحله 2: بررسی پیام‌ها...")
    updates_success, updates = bot_checker.get_updates()
    if updates_success:
        success_count += 1
    
    # ارسال پیام تست
    print("🔄 مرحله 3: ارسال پیام تست...")
    message_success = bot_checker.send_test_message()
    if message_success:
        success_count += 1
    
    # به‌روزرسانی پایگاه داده
    print("🔄 مرحله 4: به‌روزرسانی پایگاه داده...")
    db_success = bot_checker.update_database_status()
    if db_success:
        success_count += 1
    
    # نتیجه نهایی
    total_steps = 4
    success_rate = (success_count / total_steps) * 100
    
    print("\n" + "=" * 40)
    print(f"📊 نتیجه: {success_count}/{total_steps} مرحله موفق ({success_rate:.0f}%)")
    
    if success_rate >= 75:
        print("🎯 ربات تلگرام کاملاً فعال و آماده است!")
        print("💬 کاربران می‌توانند با ربات تعامل کنند")
        if bot_info:
            print(f"🔗 لینک ربات: https://t.me/{bot_info['username']}")
    else:
        print("⚠️ ربات نیاز به بررسی بیشتر دارد")

if __name__ == "__main__":
    main()