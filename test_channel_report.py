#!/usr/bin/env python3
"""
تست ارسال گزارش به کانال @CRMBATTIS
"""

import asyncio
import os
from telegram import Bot
from telegram.error import TelegramError
from datetime import datetime

async def test_channel_report():
    """تست ارسال گزارش به کانال"""
    
    # دریافت توکن ربات
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN not found")
        return
    
    # کانال هدف - کانال تلگرام برای گزارش‌دهی
    channel = "@crmbattis"  # کانال تلگرام (نه ربات)
    
    # ایجاد ربات
    bot = Bot(token=bot_token)
    
    # پیام تست
    test_message = f"""🧪 **تست سیستم گزارش‌دهی**

📢 **کانال:** {channel}
🤖 **ربات:** ULTRA_PLUS_BOT
⏰ **زمان:** {datetime.now().strftime('%Y/%m/%d - %H:%M:%S')}

✅ **سیستم گزارش‌دهی خودکار فعال است**

🔹 **گزارش‌های در دسترس:**
├── 🚀 شروع جلسات معاملات
├── 🏁 پایان جلسات و آمار نهایی
├── 💰 هشدارهای سود فوری
├── 🧠 پیشرفت یادگیری ربات
├── ⚙️ تغییرات وضعیت سیستم
├── 📊 گزارش‌های ساعتی
└── 📋 گزارش‌های روزانه

🎯 **وضعیت:** آماده خدمت‌رسانی ۲۴/۷"""

    try:
        # ارسال پیام تست
        message = await bot.send_message(
            chat_id=channel,
            text=test_message,
            parse_mode='Markdown'
        )
        
        print(f"✅ پیام تست با موفقیت ارسال شد")
        print(f"📢 کانال: {channel}")
        print(f"🆔 Message ID: {message.message_id}")
        print(f"⏰ زمان ارسال: {message.date}")
        
        return True
        
    except TelegramError as e:
        print(f"❌ خطای تلگرام: {e}")
        if "chat not found" in str(e).lower():
            print("💡 راه حل: ربات را به کانال اضافه کنید و ادمین کنید")
        elif "not enough rights" in str(e).lower():
            print("💡 راه حل: به ربات دسترسی ارسال پیام در کانال بدهید")
        return False
        
    except Exception as e:
        print(f"❌ خطای عمومی: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_channel_report())
    if result:
        print("\n🎉 تست موفق - سیستم گزارش‌دهی آماده است!")
    else:
        print("\n⚠️ تست ناموفق - نیاز به بررسی تنظیمات")