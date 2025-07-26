#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تست سلامت ربات تلگرام
"""

import os
import requests
import json
from datetime import datetime

def check_telegram_bot():
    """بررسی کامل سلامت ربات تلگرام"""
    
    bot_token = os.getenv('ULTRA_Plus_Bot')
    
    if not bot_token:
        print("❌ Bot token موجود نیست")
        return False
    
    print("🔍 بررسی سلامت ربات تلگرام...")
    print("=" * 50)
    
    # Test 1: Bot Info
    try:
        response = requests.get(f"https://api.telegram.org/bot{bot_token}/getMe")
        data = response.json()
        
        if data.get('ok'):
            bot_info = data['result']
            print(f"✅ نام ربات: {bot_info['first_name']}")
            print(f"✅ نام کاربری: @{bot_info['username']}")
            print(f"✅ ID ربات: {bot_info['id']}")
        else:
            print(f"❌ خطا در getMe: {data.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ خطا در اتصال: {e}")
        return False
    
    # Test 2: Webhook Status
    try:
        response = requests.get(f"https://api.telegram.org/bot{bot_token}/getWebhookInfo")
        webhook_data = response.json()
        
        if webhook_data.get('ok'):
            webhook_info = webhook_data['result']
            webhook_url = webhook_info.get('url', 'هیچ')
            print(f"🔗 Webhook: {webhook_url}")
            
            if webhook_url:
                print("⚠️ ربات در حالت webhook است")
            else:
                print("✅ ربات در حالت polling است")
                
    except Exception as e:
        print(f"⚠️ خطا در بررسی webhook: {e}")
    
    # Test 3: Recent Updates
    try:
        response = requests.get(f"https://api.telegram.org/bot{bot_token}/getUpdates?limit=5")
        updates_data = response.json()
        
        if updates_data.get('ok'):
            updates = updates_data['result']
            print(f"📨 تعداد updates اخیر: {len(updates)}")
            
            if updates:
                last_update = updates[-1]
                update_id = last_update.get('update_id')
                print(f"🆔 آخرین update ID: {update_id}")
                
                if 'message' in last_update:
                    msg = last_update['message']
                    user = msg.get('from', {})
                    username = user.get('username', 'ناشناس')
                    text = msg.get('text', 'متن خاص')
                    date = datetime.fromtimestamp(msg.get('date', 0))
                    print(f"👤 آخرین پیام از: @{username}")
                    print(f"💬 متن: {text[:50]}...")
                    print(f"🕐 زمان: {date}")
            else:
                print("⚠️ هیچ پیام اخیری موجود نیست")
                
    except Exception as e:
        print(f"⚠️ خطا در بررسی updates: {e}")
    
    print("=" * 50)
    print("✅ بررسی سلامت کامل شد")
    
    return True

if __name__ == "__main__":
    check_telegram_bot()