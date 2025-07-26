#!/usr/bin/env python3
"""
تست اتصال به صرافی‌های جایگزین و منابع داده
"""
import os
import sys
import requests
from datetime import datetime

def test_coingecko():
    """تست API کوین‌گکو"""
    print("🧪 تست CoinGecko API...")
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'bitcoin,ethereum',
            'vs_currencies': 'usd'
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            btc_price = data['bitcoin']['usd']
            eth_price = data['ethereum']['usd']
            print(f"✅ CoinGecko: BTC=${btc_price:,}, ETH=${eth_price:,}")
            return True
        else:
            print(f"❌ CoinGecko: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ CoinGecko خطا: {e}")
        return False

def test_cryptocompare():
    """تست API کریپتوکمپر"""
    print("🧪 تست CryptoCompare API...")
    try:
        url = "https://min-api.cryptocompare.com/data/price"
        params = {
            'fsym': 'BTC',
            'tsyms': 'USD,EUR'
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'USD' in data:
                btc_usd = data['USD']
                btc_eur = data.get('EUR', 0)
                print(f"✅ CryptoCompare: BTC=${btc_usd:,}, €{btc_eur:,}")
                return True
            else:
                print(f"❌ CryptoCompare: داده نامعتبر {data}")
                return False
        else:
            print(f"❌ CryptoCompare: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ CryptoCompare خطا: {e}")
        return False

def test_exchangerate():
    """تست API نرخ ارز"""
    print("🧪 تست ExchangeRate API...")
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            eur_rate = data['rates'].get('EUR', 0)
            gbp_rate = data['rates'].get('GBP', 0)
            print(f"✅ ExchangeRate: USD/EUR={eur_rate:.4f}, USD/GBP={gbp_rate:.4f}")
            return True
        else:
            print(f"❌ ExchangeRate: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ExchangeRate خطا: {e}")
        return False

def test_alpha_vantage():
    """تست Alpha Vantage API"""
    print("🧪 تست Alpha Vantage API...")
    try:
        # بدون API key - تست basic
        url = "https://www.alphavantage.co/query"
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': 'IBM',
            'apikey': 'demo'
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'Global Quote' in data:
                price = data['Global Quote'].get('05. price', 'N/A')
                print(f"✅ Alpha Vantage: IBM stock=${price}")
                return True
            else:
                print(f"⚠️ Alpha Vantage: نیاز به API key معتبر - {data}")
                return False
        else:
            print(f"❌ Alpha Vantage: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Alpha Vantage خطا: {e}")
        return False

def test_coinbase_public():
    """تست Coinbase API عمومی"""
    print("🧪 تست Coinbase Public API...")
    try:
        url = "https://api.coinbase.com/v2/exchange-rates"
        params = {'currency': 'BTC'}
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'rates' in data['data']:
                usd_rate = data['data']['rates'].get('USD', 0)
                eur_rate = data['data']['rates'].get('EUR', 0)
                print(f"✅ Coinbase: BTC=${float(usd_rate):,.0f}, €{float(eur_rate):,.0f}")
                return True
            else:
                print(f"❌ Coinbase: داده نامعتبر")
                return False
        else:
            print(f"❌ Coinbase: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Coinbase خطا: {e}")
        return False

def main():
    """تست کامل همه منابع"""
    print("🔍 شروع تست اتصال به صرافی‌ها و منابع داده...")
    print("=" * 60)
    
    results = {}
    
    # تست منابع مختلف
    results['CoinGecko'] = test_coingecko()
    results['CryptoCompare'] = test_cryptocompare()
    results['ExchangeRate'] = test_exchangerate()
    results['Alpha Vantage'] = test_alpha_vantage()
    results['Coinbase'] = test_coinbase_public()
    
    print("\n" + "=" * 60)
    print("📊 خلاصه نتایج:")
    
    successful = 0
    total = len(results)
    
    for service, status in results.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {service}: {'موفق' if status else 'ناموفق'}")
        if status:
            successful += 1
    
    print(f"\n📈 نرخ موفقیت: {successful}/{total} ({successful/total*100:.1f}%)")
    
    if successful >= 3:
        print("🎉 سیستم با منابع جایگزین قابل اجرا است!")
        print("💡 توصیه: استفاده از ترکیب CoinGecko + CryptoCompare + ExchangeRate")
    else:
        print("⚠️ تعداد منابع معتبر کافی نیست")
    
    print("\n📋 راه‌حل Binance:")
    print("• Binance در این منطقه محدودیت دارد")
    print("• منابع جایگزین: CoinGecko, Coinbase, CryptoCompare")
    print("• برای معاملات واقعی: استفاده از VPN یا صرافی‌های دیگر")
    
    return successful >= 3

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)