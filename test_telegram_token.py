#!/usr/bin/env python3
"""
تست سریع توکن تلگرام
"""
import os
import requests

def test_telegram_token():
    """تست توکن تلگرام"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("❌ توکن تلگرام یافت نشد")
        return False
    
    print(f"🔑 توکن دریافت شد: {token[:10]}...{token[-5:]}")
    
    try:
        url = f"https://api.telegram.org/bot{token}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data['ok']:
                bot_info = data['result']
                print(f"✅ ربات معتبر: @{bot_info['username']}")
                print(f"📱 نام ربات: {bot_info['first_name']}")
                print(f"🆔 ID ربات: {bot_info['id']}")
                return True
        
        print(f"❌ خطا: {response.status_code} - {response.text}")
        return False
        
    except Exception as e:
        print(f"❌ خطای اتصال: {e}")
        return False

if __name__ == "__main__":
    print("🚀 تست توکن تلگرام...")
    if test_telegram_token():
        print("✅ توکن معتبر است - ربات آماده کار!")
    else:
        print("❌ مشکل در توکن - لطفاً بررسی کنید")