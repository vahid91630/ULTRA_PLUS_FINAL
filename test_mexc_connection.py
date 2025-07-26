#!/usr/bin/env python3
"""
تست اتصال MEXC با کلیدهای واقعی
"""
import os
from mexc_integration import MEXCConnector

def test_mexc_with_real_keys():
    """تست کامل MEXC با کلیدهای واقعی"""
    
    print("🧪 تست اتصال MEXC با کلیدهای واقعی...")
    print("=" * 60)
    
    # دریافت کلیدها از environment
    api_key = os.getenv('MEXC_API_KEY', '')
    secret_key = os.getenv('MEXC_SECRET_KEY', '')
    
    if not api_key or not secret_key:
        print("❌ کلیدهای API در environment یافت نشد")
        return False
    
    print(f"✅ API Key: {api_key[:8]}...{api_key[-4:] if len(api_key) > 12 else 'مخفی'}")
    print(f"✅ Secret Key: {'*' * 20}")
    print()
    
    # ایجاد connector با کلیدهای واقعی
    mexc = MEXCConnector(api_key=api_key, api_secret=secret_key)
    
    # تست 1: اتصال عمومی
    print("1️⃣ تست اتصال عمومی...")
    connection_test = mexc.test_connection()
    print(f"   {connection_test['message']}")
    if not connection_test['success']:
        return False
    
    # تست 2: قیمت Bitcoin
    print("\n2️⃣ تست دریافت قیمت Bitcoin...")
    btc_test = mexc.get_btc_price()
    print(f"   {btc_test['message']}")
    if btc_test['success']:
        print(f"   قیمت فعلی: ${btc_test['price']:,.2f}")
    
    # تست 3: داده‌های بازار
    print("\n3️⃣ تست داده‌های بازار...")
    market_test = mexc.get_market_data()
    print(f"   {market_test['message']}")
    if market_test['success']:
        for symbol, price in market_test['prices'].items():
            coin_name = symbol.replace('USDT', '')
            print(f"   {coin_name}: ${price:,.2f}")
    
    # تست 4: اطلاعات حساب (با کلید واقعی)
    print("\n4️⃣ تست اطلاعات حساب...")
    account_test = mexc.get_account_info()
    print(f"   {account_test['message']}")
    
    if account_test['success']:
        balances = account_test.get('balances', {})
        if balances:
            print("   💰 موجودی‌های حساب:")
            for asset, balance_info in balances.items():
                total = balance_info['total']
                print(f"   {asset}: {total:.8f}")
        else:
            print("   📝 حساب خالی (موجودی صفر)")
    elif 'API' in account_test.get('error', ''):
        print("   ⚠️ مشکل در احراز هویت API - بررسی کلیدها")
    
    print("\n" + "=" * 60)
    
    # خلاصه نتایج
    results = {
        "connection": connection_test['success'],
        "price_data": btc_test['success'], 
        "market_data": market_test['success'],
        "account_access": account_test['success']
    }
    
    print("📊 خلاصه نتایج:")
    print(f"   اتصال عمومی: {'✅' if results['connection'] else '❌'}")
    print(f"   دریافت قیمت: {'✅' if results['price_data'] else '❌'}")
    print(f"   داده‌های بازار: {'✅' if results['market_data'] else '❌'}")
    print(f"   دسترسی حساب: {'✅' if results['account_access'] else '❌'}")
    
    # وضعیت کلی
    all_good = all(results.values())
    if all_good:
        print("\n🎉 همه تست‌ها موفق! MEXC کاملاً آماده معاملات واقعی!")
        print("💡 حالا می‌توانید معاملات واقعی انجام دهید")
    else:
        print("\n⚠️ برخی تست‌ها ناموفق - بررسی تنظیمات")
    
    return all_good

if __name__ == "__main__":
    test_mexc_with_real_keys()