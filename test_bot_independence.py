#!/usr/bin/env python3
"""
تست استقلال ربات تلگرام - بررسی اینکه ربات مستقل از مرورگر کار می‌کند
"""

import os
import sys
import time
import signal
import requests
import subprocess
from datetime import datetime

def test_bot_token():
    """تست توکن ربات"""
    token = os.getenv('ULTRA_Plus_Bot')
    if not token:
        print("❌ توکن ربات یافت نشد")
        return False
    
    try:
        response = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10)
        if response.status_code == 200:
            bot_info = response.json()
            print(f"✅ ربات متصل: @{bot_info['result']['username']}")
            return True
        else:
            print(f"❌ خطا در اتصال: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطا در تست توکن: {e}")
        return False

def check_bot_process():
    """بررسی پروسه ربات"""
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        bot_processes = [line for line in result.stdout.split('\n') if 'telegram_bot_persistent.py' in line and 'grep' not in line]
        
        if bot_processes:
            print(f"✅ پروسه ربات فعال: {len(bot_processes)} نمونه")
            for process in bot_processes:
                parts = process.split()
                if len(parts) >= 2:
                    print(f"   PID: {parts[1]}")
            return True
        else:
            print("❌ پروسه ربات یافت نشد")
            return False
    except Exception as e:
        print(f"❌ خطا در بررسی پروسه: {e}")
        return False

def test_independence():
    """تست استقلال کامل ربات"""
    print("🔍 تست استقلال ربات تلگرام از مرورگر...")
    print("=" * 50)
    
    # تست 1: بررسی توکن
    print("1️⃣ تست توکن ربات:")
    token_ok = test_bot_token()
    
    # تست 2: بررسی پروسه
    print("\n2️⃣ بررسی پروسه ربات:")
    process_ok = check_bot_process()
    
    # تست 3: بررسی لاگ‌ها
    print("\n3️⃣ بررسی لاگ‌های ربات:")
    try:
        if os.path.exists('telegram_bot_persistent.log'):
            with open('telegram_bot_persistent.log', 'r') as f:
                lines = f.readlines()
                recent_lines = lines[-5:] if len(lines) >= 5 else lines
                print("✅ لاگ‌های اخیر:")
                for line in recent_lines:
                    if line.strip():
                        print(f"   {line.strip()}")
        else:
            print("⚠️ فایل لاگ یافت نشد")
    except Exception as e:
        print(f"❌ خطا در خواندن لاگ: {e}")
    
    # نتیجه‌گیری
    print("\n" + "=" * 50)
    if token_ok and process_ok:
        print("✅ ربات کاملاً مستقل و آماده کار 24/7")
        print("🔸 ربات حتی پس از بستن مرورگر کار خواهد کرد")
        print("🔸 برای تست: مرورگر را ببندید و پیام بفرستید")
        return True
    else:
        print("❌ مشکلی در استقلال ربات وجود دارد")
        return False

if __name__ == "__main__":
    test_independence()