#!/usr/bin/env python3
"""
تست اتصال به صرافی Binance
"""
import os
import sys
from datetime import datetime

def test_binance_connection():
    """تست کامل اتصال به Binance"""
    
    print("🔍 شروع تست اتصال به صرافی Binance...")
    print("=" * 50)
    
    # بررسی کلیدهای API
    api_key = os.getenv('BINANCE_API_KEY')
    secret_key = os.getenv('BINANCE_SECRET_KEY')
    
    if not api_key:
        print("❌ BINANCE_API_KEY یافت نشد")
        return False
    
    if not secret_key:
        print("❌ BINANCE_SECRET_KEY یافت نشد")
        return False
        
    print(f"✅ API Key: {api_key[:8]}***{api_key[-4:]}")
    print(f"✅ Secret Key: {secret_key[:8]}***{secret_key[-4:]}")
    print()
    
    # تست اتصال
    try:
        from binance.client import Client
        from binance.exceptions import BinanceAPIException
        
        print("📦 ماژول python-binance بارگذاری شد")
        
        # ایجاد کلاینت
        client = Client(api_key, secret_key, testnet=False)
        print("🔗 کلاینت Binance ایجاد شد")
        
        # تست 1: دریافت وضعیت سرور
        print("\n🧪 تست 1: وضعیت سرور Binance")
        try:
            server_time = client.get_server_time()
            print(f"✅ سرور Binance فعال: {datetime.fromtimestamp(server_time['serverTime']/1000)}")
        except Exception as e:
            print(f"❌ خطا در تست سرور: {e}")
            return False
        
        # تست 2: دریافت اطلاعات حساب
        print("\n🧪 تست 2: اطلاعات حساب")
        try:
            account_info = client.get_account()
            print(f"✅ حساب معتبر - نوع: {account_info.get('accountType', 'نامشخص')}")
            print(f"✅ وضعیت معاملات: {'فعال' if account_info.get('canTrade', False) else 'غیرفعال'}")
            
            # نمایش موجودی‌ها (فقط موجودی‌های غیرصفر)
            balances = [b for b in account_info['balances'] if float(b['free']) > 0 or float(b['locked']) > 0]
            if balances:
                print(f"✅ موجودی‌های حساب ({len(balances)} ارز):")
                for balance in balances[:5]:  # نمایش 5 ارز اول
                    asset = balance['asset']
                    free = float(balance['free'])
                    locked = float(balance['locked'])
                    total = free + locked
                    if total > 0:
                        print(f"   • {asset}: {total:.8f} (آزاد: {free:.8f}, قفل: {locked:.8f})")
            else:
                print("⚠️ موجودی در حساب یافت نشد")
                
        except BinanceAPIException as e:
            print(f"❌ خطا در API: {e.message}")
            if e.code == -2014:
                print("💡 احتمالاً API key نیاز به فعال‌سازی Spot Trading دارد")
            elif e.code == -1022:
                print("💡 احتمالاً IP محدودیت دارد یا signature اشتباه است")
            return False
        except Exception as e:
            print(f"❌ خطای غیرمنتظره: {e}")
            return False
        
        # تست 3: دریافت قیمت Bitcoin
        print("\n🧪 تست 3: دریافت قیمت‌های بازار")
        try:
            btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
            print(f"✅ قیمت BTC/USDT: ${float(btc_price['price']):,.2f}")
            
            eth_price = client.get_symbol_ticker(symbol="ETHUSDT")
            print(f"✅ قیمت ETH/USDT: ${float(eth_price['price']):,.2f}")
            
        except Exception as e:
            print(f"❌ خطا در دریافت قیمت: {e}")
            return False
        
        print("\n" + "=" * 50)
        print("🎉 تست اتصال به Binance موفقیت‌آمیز بود!")
        print("✅ همه API ها کار می‌کنند")
        print("✅ حساب معتبر و قابل دسترسی است")
        print("✅ آماده برای معاملات واقعی")
        return True
        
    except ImportError:
        print("❌ ماژول python-binance نصب نشده")
        print("💡 برای نصب: pip install python-binance")
        return False
    except Exception as e:
        print(f"❌ خطای کلی: {e}")
        return False

if __name__ == "__main__":
    success = test_binance_connection()
    sys.exit(0 if success else 1)