#!/usr/bin/env python3
"""
راه‌اندازی صرافی‌های جایگزین برای معاملات واقعی
"""
import os
import sys
import requests
from datetime import datetime

class AlternativeExchangeManager:
    """مدیریت صرافی‌های جایگزین"""
    
    def __init__(self):
        self.exchanges = {
            'kucoin': {
                'name': 'KuCoin',
                'base_url': 'https://api.kucoin.com',
                'features': ['No geo restrictions', 'Strong API', 'High liquidity'],
                'api_docs': 'https://docs.kucoin.com/',
                'registration': 'https://www.kucoin.com/ucenter/signup'
            },
            'coinbase': {
                'name': 'Coinbase Pro',
                'base_url': 'https://api.pro.coinbase.com',
                'features': ['US compliant', 'Professional trading', 'Stable API'],
                'api_docs': 'https://docs.pro.coinbase.com/',
                'registration': 'https://pro.coinbase.com/'
            },
            'kraken': {
                'name': 'Kraken',
                'base_url': 'https://api.kraken.com',
                'features': ['Global access', 'Security focused', 'Advanced features'],
                'api_docs': 'https://www.kraken.com/features/api',
                'registration': 'https://www.kraken.com/sign-up'
            }
        }
    
    def test_exchange_access(self, exchange_key):
        """تست دسترسی به صرافی"""
        exchange = self.exchanges.get(exchange_key)
        if not exchange:
            return False, "صرافی یافت نشد"
        
        try:
            # تست اتصال عمومی
            if exchange_key == 'kucoin':
                url = f"{exchange['base_url']}/api/v1/timestamp"
            elif exchange_key == 'coinbase':
                url = f"{exchange['base_url']}/time"
            elif exchange_key == 'kraken':
                url = f"{exchange['base_url']}/0/public/Time"
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return True, f"✅ {exchange['name']} در دسترس"
            else:
                return False, f"❌ HTTP {response.status_code}"
                
        except Exception as e:
            return False, f"❌ خطا: {str(e)}"
    
    def get_setup_instructions(self, exchange_key):
        """دستورالعمل راه‌اندازی"""
        exchange = self.exchanges.get(exchange_key)
        if not exchange:
            return None
        
        instructions = {
            'exchange': exchange['name'],
            'steps': [
                f"1. ثبت نام در {exchange['registration']}",
                "2. تکمیل احراز هویت (KYC)",
                "3. فعال‌سازی Two-Factor Authentication",
                "4. ایجاد API Key در بخش Settings > API",
                "5. فعال‌سازی مجوزهای Trading",
                "6. افزودن IP Whitelist (اختیاری)",
                "7. تست API با کلیدهای جدید"
            ],
            'features': exchange['features'],
            'api_docs': exchange['api_docs']
        }
        
        return instructions

def main():
    """راه‌اندازی صرافی‌های جایگزین"""
    print("🔄 راه‌اندازی صرافی‌های جایگزین...")
    print("=" * 60)
    
    manager = AlternativeExchangeManager()
    
    print("📍 مشکل فعلی:")
    print("   • Binance در IP آمریکایی محدود است")
    print("   • نیاز به صرافی جایگزین برای معاملات واقعی")
    print("   • داده‌ها از منابع رایگان دریافت می‌شود")
    
    print("\n🧪 تست دسترسی صرافی‌ها:")
    
    for key, exchange in manager.exchanges.items():
        success, message = manager.test_exchange_access(key)
        icon = "✅" if success else "❌"
        print(f"   {icon} {exchange['name']}: {message}")
    
    print("\n💡 توصیه‌های راه‌اندازی:")
    
    # KuCoin - بهترین گزینه
    kucoin_setup = manager.get_setup_instructions('kucoin')
    print(f"\n🏆 توصیه اول: {kucoin_setup['exchange']}")
    print("   ویژگی‌ها:")
    for feature in kucoin_setup['features']:
        print(f"     • {feature}")
    print(f"   لینک ثبت نام: {manager.exchanges['kucoin']['registration']}")
    
    # Coinbase Pro - گزینه آمریکایی
    coinbase_setup = manager.get_setup_instructions('coinbase')
    print(f"\n🇺🇸 گزینه آمریکایی: {coinbase_setup['exchange']}")
    print("   ویژگی‌ها:")
    for feature in coinbase_setup['features']:
        print(f"     • {feature}")
    print(f"   لینک ثبت نام: {manager.exchanges['coinbase']['registration']}")
    
    print("\n📋 مراحل عملی:")
    print("1. انتخاب یکی از صرافی‌های بالا")
    print("2. ثبت نام و احراز هویت")
    print("3. ایجاد API کلید")
    print("4. اضافه کردن کلیدها به secrets")
    print("5. تست اتصال و معاملات")
    
    print("\n🎯 نتیجه:")
    print("   • برای فعلاً: ربات با داده‌های رایگان کار می‌کند")
    print("   • برای معاملات: نیاز به صرافی جایگزین")
    print("   • توصیه: KuCoin برای بین‌المللی، Coinbase Pro برای آمریکا")

if __name__ == "__main__":
    main()