#!/usr/bin/env python3
"""
🚀 BINANCE PUBLIC API TEST - بدون نیاز به Secret Key
تست اتصال با API Key موجود و endpointهای عمومی
"""

import os
import sys
import requests
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_binance_public():
    """تست endpointهای عمومی Binance"""
    
    print("🚀 BINANCE PUBLIC API TEST")
    print("=" * 50)
    
    # چک کردن API Key
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    
    print(f"🔑 BINANCE_API_KEY: {'✅ موجود' if api_key else '❌ ناموجود'}")
    print(f"🔐 BINANCE_API_SECRET: {'✅ موجود' if api_secret else '❌ ناموجود'}")
    print()
    
    base_url = 'https://api.binance.com'
    headers = {}
    
    if api_key:
        headers['X-MBX-APIKEY'] = api_key
    
    try:
        # 1. تست Ping
        print("1️⃣ تست Ping...")
        response = requests.get(f"{base_url}/api/v3/ping", headers=headers, timeout=10)
        if response.status_code == 200:
            print("✅ Binance API پینگ موفق")
        else:
            print(f"❌ پینگ ناموفق: {response.status_code}")
            
        # 2. تست Server Time
        print("\n2️⃣ تست زمان سرور...")
        response = requests.get(f"{base_url}/api/v3/time", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            server_time = datetime.fromtimestamp(data['serverTime'] / 1000)
            print(f"✅ زمان سرور: {server_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        else:
            print(f"❌ دریافت زمان ناموفق: {response.status_code}")
            
        # 3. تست Exchange Info
        print("\n3️⃣ تست اطلاعات صرافی...")
        response = requests.get(f"{base_url}/api/v3/exchangeInfo", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            symbols_count = len(data.get('symbols', []))
            print(f"✅ تعداد جفت ارزها: {symbols_count}")
            
            # نمایش چند جفت ارز محبوب
            popular_symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'DOTUSDT']
            available_symbols = [s['symbol'] for s in data.get('symbols', [])]
            
            print("📈 جفت ارزهای محبوب موجود:")
            for symbol in popular_symbols:
                status = "✅" if symbol in available_symbols else "❌"
                print(f"   {status} {symbol}")
        else:
            print(f"❌ دریافت اطلاعات صرافی ناموفق: {response.status_code}")
            
        # 4. تست قیمت Bitcoin
        print("\n4️⃣ تست قیمت Bitcoin...")
        response = requests.get(f"{base_url}/api/v3/ticker/price?symbol=BTCUSDT", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            btc_price = float(data['price'])
            print(f"✅ قیمت Bitcoin: ${btc_price:,.2f}")
        else:
            print(f"❌ دریافت قیمت Bitcoin ناموفق: {response.status_code}")
            
        # 5. تست 24h Statistics
        print("\n5️⃣ تست آمار 24 ساعته...")
        response = requests.get(f"{base_url}/api/v3/ticker/24hr?symbol=BTCUSDT", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            change_percent = float(data['priceChangePercent'])
            volume = float(data['volume'])
            high = float(data['highPrice'])
            low = float(data['lowPrice'])
            
            print(f"✅ تغییر 24h: {change_percent:+.2f}%")
            print(f"✅ حجم معاملات: {volume:,.2f} BTC")
            print(f"✅ بالاترین قیمت: ${high:,.2f}")
            print(f"✅ پایین‌ترین قیمت: ${low:,.2f}")
        else:
            print(f"❌ دریافت آمار 24h ناموفق: {response.status_code}")
            
        print("\n" + "=" * 50)
        print("✅ تست عمومی Binance کامل شد")
        
        if not api_secret:
            print("\n🔐 برای فعال‌سازی کامل:")
            print("   - BINANCE_API_SECRET را در Secrets اضافه کنید")
            print("   - IP سرور (35.190.155.7) را در Binance اضافه کنید")
            print("   - مجوزهای Reading و Spot Trading را فعال کنید")
            
    except Exception as e:
        logger.error(f"❌ خطا در تست Binance: {e}")
        return False
        
    return True

if __name__ == "__main__":
    success = test_binance_public()
    sys.exit(0 if success else 1)