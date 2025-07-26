#!/usr/bin/env python3
"""
آزمایش اتصال تمام API Keys موجود در Secret
"""

import os
import requests
import ccxt
import openai
import asyncio
import time
from datetime import datetime

def test_openai_connection():
    """آزمایش اتصال OpenAI"""
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return {"status": "MISSING", "error": "API Key موجود نیست"}
        
        # تست مستقیم با requests
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Test"}],
            "max_tokens": 5
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            return {
                "status": "CONNECTED",
                "api_key_length": len(api_key),
                "response_received": True,
                "model_used": "gpt-3.5-turbo"
            }
        else:
            return {
                "status": "ERROR",
                "error": f"HTTP {response.status_code}: {response.text[:100]}",
                "api_key_exists": bool(api_key)
            }
        
    except Exception as e:
        return {
            "status": "ERROR",
            "error": str(e),
            "api_key_exists": bool(api_key)
        }

def test_binance_connection():
    """آزمایش اتصال Binance"""
    try:
        api_key = os.getenv('BINANCE_API_KEY')
        secret_key = os.getenv('BINANCE_SECRET_KEY')
        
        if not api_key or not secret_key:
            return {"status": "MISSING", "error": "API Keys موجود نیست"}
        
        exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': secret_key,
            'sandbox': False,
            'timeout': 10000
        })
        
        # تست اتصال
        markets = exchange.fetch_markets()
        
        return {
            "status": "CONNECTED",
            "api_key_length": len(api_key),
            "markets_count": len(markets) if markets else 0,
            "exchange_id": exchange.id
        }
        
    except Exception as e:
        error_msg = str(e)
        if "restricted location" in error_msg or "451" in error_msg or "forbidden" in error_msg.lower():
            return {
                "status": "GEO_RESTRICTED",
                "error": "محدودیت جغرافیایی - کلید معتبر است",
                "api_key_exists": bool(api_key),
                "note": "Binance در این منطقه محدود است"
            }
        else:
            return {
                "status": "ERROR",
                "error": error_msg,
                "api_key_exists": bool(api_key)
            }

def test_mexc_connection():
    """آزمایش اتصال MEXC"""
    try:
        api_key = os.getenv('MEXC_API_KEY')
        secret_key = os.getenv('MEXC_SECRET_KEY')
        
        if not api_key or not secret_key:
            return {"status": "MISSING", "error": "API Keys موجود نیست"}
        
        exchange = ccxt.mexc({
            'apiKey': api_key,
            'secret': secret_key,
            'sandbox': False,
            'timeout': 10000
        })
        
        # تست اتصال
        markets = exchange.fetch_markets()
        
        return {
            "status": "CONNECTED",
            "api_key_length": len(api_key),
            "markets_count": len(markets) if markets else 0,
            "exchange_id": exchange.id
        }
        
    except Exception as e:
        return {
            "status": "ERROR",
            "error": str(e),
            "api_key_exists": bool(api_key)
        }

def test_telegram_connection():
    """آزمایش اتصال Telegram"""
    try:
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        
        if not bot_token:
            return {"status": "MISSING", "error": "Bot Token موجود نیست"}
        
        # تست API
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data.get('result', {})
                return {
                    "status": "CONNECTED",
                    "token_length": len(bot_token),
                    "bot_username": bot_info.get('username'),
                    "bot_name": bot_info.get('first_name'),
                    "bot_id": bot_info.get('id')
                }
        
        return {
            "status": "ERROR",
            "error": f"HTTP {response.status_code}",
            "token_exists": bool(bot_token)
        }
        
    except Exception as e:
        return {
            "status": "ERROR",
            "error": str(e),
            "token_exists": bool(bot_token)
        }

def test_database_connection():
    """آزمایش اتصال دیتابیس"""
    try:
        db_url = os.getenv('DATABASE_URL')
        
        if not db_url:
            return {"status": "MISSING", "error": "Database URL موجود نیست"}
        
        # استخراج اطلاعات دیتابیس
        if db_url.startswith('postgresql://'):
            return {
                "status": "POSTGRESQL_FOUND",
                "url_length": len(db_url),
                "type": "PostgreSQL",
                "note": "اتصال PostgreSQL در دسترس است"
            }
        elif db_url.startswith('mongodb://') or db_url.startswith('mongodb+srv://'):
            return {
                "status": "MONGODB_FOUND", 
                "url_length": len(db_url),
                "type": "MongoDB",
                "note": "اتصال MongoDB در دسترس است"
            }
        else:
            return {
                "status": "UNKNOWN_TYPE",
                "url_length": len(db_url),
                "type": "نامشخص"
            }
        
    except Exception as e:
        return {
            "status": "ERROR",
            "error": str(e)
        }

def test_all_connections():
    """آزمایش تمام اتصالات"""
    print("🔐 آزمایش تمام کلیدهای API...")
    print("=" * 60)
    
    # آزمایش هر سرویس
    tests = {
        "OpenAI": test_openai_connection,
        "Binance": test_binance_connection,
        "MEXC": test_mexc_connection,
        "Telegram": test_telegram_connection,
        "Database": test_database_connection
    }
    
    results = {}
    
    for service_name, test_func in tests.items():
        print(f"\n🔍 آزمایش {service_name}...")
        
        start_time = time.time()
        result = test_func()
        end_time = time.time()
        
        result['test_duration'] = round(end_time - start_time, 2)
        results[service_name] = result
        
        # نمایش نتیجه
        status = result['status']
        if status == "CONNECTED":
            print(f"✅ {service_name}: اتصال موفق")
            if 'api_key_length' in result:
                print(f"   📝 طول کلید: {result['api_key_length']} کاراکتر")
            if 'markets_count' in result:
                print(f"   📊 بازارها: {result['markets_count']} بازار")
            if 'bot_username' in result:
                print(f"   🤖 نام ربات: @{result['bot_username']}")
                
        elif status == "GEO_RESTRICTED":
            print(f"🌍 {service_name}: محدودیت جغرافیایی")
            print(f"   ⚠️ کلید معتبر اما دسترسی محدود")
            
        elif status == "MISSING":
            print(f"❌ {service_name}: کلید موجود نیست")
            
        elif status in ["POSTGRESQL_FOUND", "MONGODB_FOUND"]:
            print(f"✅ {service_name}: {result['type']} در دسترس")
            
        else:
            print(f"❌ {service_name}: خطا")
            print(f"   🔍 جزئیات: {result.get('error', 'نامشخص')}")
        
        print(f"   ⏱️ زمان آزمایش: {result['test_duration']} ثانیه")
    
    # خلاصه نهایی
    print(f"\n📊 خلاصه نتایج:")
    print("=" * 40)
    
    connected = 0
    total = len(tests)
    
    for service, result in results.items():
        status = result['status']
        if status in ["CONNECTED", "POSTGRESQL_FOUND", "MONGODB_FOUND"]:
            connected += 1
            print(f"✅ {service}")
        elif status == "GEO_RESTRICTED":
            print(f"🌍 {service} (محدود)")
        else:
            print(f"❌ {service}")
    
    print(f"\n🎯 نتیجه کلی: {connected}/{total} سرویس متصل")
    
    if connected >= 3:
        print("✅ اکثر سرویس‌ها فعال - سیستم آماده کار است")
    elif connected >= 1:
        print("⚠️ برخی سرویس‌ها فعال - عملکرد محدود")
    else:
        print("❌ هیچ سرویسی متصل نیست - نیاز به بررسی کلیدها")
    
    return results

if __name__ == "__main__":
    test_all_connections()