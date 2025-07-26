#!/usr/bin/env python3
"""
تایید نهایی سیستم معاملات واقعی
"""
import os
from real_trading_engine import RealTradingEngine
from mexc_integration import MEXCConnector

def validate_complete_system():
    """تایید کامل سیستم"""
    
    print("🔍 بررسی کامل سیستم معاملات واقعی...")
    print("=" * 70)
    
    # 1. بررسی Environment Variables
    print("1️⃣ بررسی کلیدهای API...")
    mexc_api = os.getenv('MEXC_API_KEY', '')
    mexc_secret = os.getenv('MEXC_SECRET_KEY', '')
    binance_api = os.getenv('BINANCE_API_KEY', '')
    binance_secret = os.getenv('BINANCE_SECRET_KEY', '')
    
    print(f"   MEXC API: {'✅' if mexc_api else '❌'} ({mexc_api[:8] + '...' if mexc_api else 'غیرفعال'})")
    print(f"   MEXC Secret: {'✅' if mexc_secret else '❌'}")
    print(f"   Binance API: {'✅' if binance_api else '❌'} ({binance_api[:8] + '...' if binance_api else 'غیرفعال'})")
    print(f"   Binance Secret: {'✅' if binance_secret else '❌'}")
    
    # 2. تست MEXC Connector
    print("\n2️⃣ تست MEXC Connector...")
    mexc = MEXCConnector(api_key=mexc_api, api_secret=mexc_secret)
    
    connection_test = mexc.test_connection()
    print(f"   اتصال: {'✅' if connection_test['success'] else '❌'} - {connection_test['message']}")
    
    price_test = mexc.get_btc_price()
    print(f"   قیمت BTC: {'✅' if price_test['success'] else '❌'} - ${price_test.get('price', 'N/A')}")
    
    account_test = mexc.get_account_info()
    print(f"   دسترسی حساب: {'✅' if account_test['success'] else '❌'}")
    
    # 3. تست Real Trading Engine
    print("\n3️⃣ تست Real Trading Engine...")
    engine = RealTradingEngine()
    
    # بررسی شرایط
    conditions = engine.validate_trading_conditions()
    print("   شرایط معاملات:")
    for condition, status in conditions.items():
        print(f"     {condition}: {'✅' if status else '❌'}")
    
    # دریافت وضعیت
    status = engine.get_real_trading_status()
    print(f"   وضعیت سیستم: {'✅' if status['success'] else '❌'}")
    
    if status['success']:
        print(f"   فعالیت معاملات: {'🟢' if status['trading_active'] else '🔴'}")
        print(f"   تعداد موجودی‌ها: {len(status['balances'])}")
        print(f"   قیمت‌های فعلی: {len(status['current_prices'])}")
    
    # 4. بررسی آمادگی برای فعال‌سازی
    print("\n4️⃣ بررسی آمادگی فعال‌سازی...")
    
    ready_count = sum(1 for status in conditions.values() if status)
    total_conditions = len(conditions)
    
    print(f"   شرایط برقرار: {ready_count}/{total_conditions}")
    
    if ready_count == total_conditions:
        print("   ✅ همه شرایط برقرار - آماده فعال‌سازی معاملات واقعی!")
        print("   🚀 می‌توانید از طریق ربات تلگرام فعال کنید")
    else:
        missing = [k for k, v in conditions.items() if not v]
        print(f"   ❌ شرایط ناکافی: {', '.join(missing)}")
        
        # راهنمایی برای رفع مشکلات
        if not conditions['mexc_connection']:
            print("     💡 بررسی اتصال اینترنت و API Keys")
        if not conditions['account_access']:
            print("     💡 بررسی صحت کلیدهای API")
        if not conditions['trading_permissions']:
            print("     💡 فعال‌سازی SPOT trading در MEXC")
        if not conditions['balance_sufficient']:
            print("     💡 واریز حداقل 10 USDT به حساب MEXC")
    
    # 5. خلاصه وضعیت
    print("\n5️⃣ خلاصه وضعیت سیستم:")
    
    all_keys_present = all([mexc_api, mexc_secret, binance_api, binance_secret])
    mexc_working = connection_test['success'] and price_test['success']
    engine_ready = status['success']
    can_activate = all(conditions.values())
    
    print(f"   🔑 کلیدهای API: {'✅' if all_keys_present else '⚠️'}")
    print(f"   🌐 اتصال MEXC: {'✅' if mexc_working else '❌'}")  
    print(f"   ⚙️ موتور معاملات: {'✅' if engine_ready else '❌'}")
    print(f"   🚀 آماده فعال‌سازی: {'✅' if can_activate else '❌'}")
    
    print("\n" + "=" * 70)
    
    if all([all_keys_present, mexc_working, engine_ready]):
        if can_activate:
            print("🎉 سیستم کاملاً آماده! می‌توانید معاملات واقعی را فعال کنید!")
            print("📱 از طریق ربات تلگرام دکمه '🚀 معاملات واقعی' را انتخاب کنید")
        else:
            print("⚠️ سیستم تقریباً آماده، فقط نیاز به رفع مشکلات جزئی")
    else:
        print("❌ سیستم نیاز به تکمیل دارد")
    
    return {
        "keys_present": all_keys_present,
        "mexc_working": mexc_working,
        "engine_ready": engine_ready,
        "can_activate": can_activate,
        "conditions": conditions
    }

if __name__ == "__main__":
    validate_complete_system()