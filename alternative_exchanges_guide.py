#!/usr/bin/env python3
"""
راهنمای صرافی‌های جایگزین برای وحید
"""

ALTERNATIVE_EXCHANGES = {
    "KuCoin": {
        "name": "KuCoin",
        "website": "https://www.kucoin.com",
        "restrictions": "بدون محدودیت جغرافیایی",
        "api_quality": "عالی",
        "trading_pairs": "500+",
        "advantages": [
            "بدون محدودیت IP",
            "API قدرتمند",
            "کارمزد پایین",
            "حجم معاملات بالا"
        ],
        "setup_difficulty": "آسان",
        "persian_support": "خیر",
        "recommendation": "بهترین جایگزین Binance"
    },
    
    "Coinbase_Pro": {
        "name": "Coinbase Pro",
        "website": "https://pro.coinbase.com",
        "restrictions": "قابل دسترس از همه جا",
        "api_quality": "عالی",
        "trading_pairs": "200+",
        "advantages": [
            "قانونی و مجاز",
            "امنیت بالا",
            "API مستند",
            "پشتیبانی 24/7"
        ],
        "setup_difficulty": "متوسط",
        "persian_support": "خیر",
        "recommendation": "برای معاملات حرفه‌ای"
    },
    
    "Kraken": {
        "name": "Kraken",
        "website": "https://www.kraken.com",
        "restrictions": "دسترسی جهانی",
        "api_quality": "بسیار خوب",
        "trading_pairs": "400+",
        "advantages": [
            "امنیت بسیار بالا",
            "قدیمی‌ترین صرافی",
            "API پایدار",
            "حجم بالا"
        ],
        "setup_difficulty": "متوسط",
        "persian_support": "خیر",
        "recommendation": "برای امنیت بالا"
    },
    
    "Bybit": {
        "name": "Bybit", 
        "website": "https://www.bybit.com",
        "restrictions": "بدون محدودیت",
        "api_quality": "خوب",
        "trading_pairs": "300+",
        "advantages": [
            "UI ساده",
            "معاملات futures",
            "کارمزد پایین",
            "سرعت بالا"
        ],
        "setup_difficulty": "آسان",
        "persian_support": "خیر", 
        "recommendation": "برای معاملات سریع"
    },
    
    "Gate.io": {
        "name": "Gate.io",
        "website": "https://www.gate.io",
        "restrictions": "دسترسی آزاد",
        "api_quality": "خوب",
        "trading_pairs": "1000+",
        "advantages": [
            "تنوع بالای کوین‌ها",
            "بدون KYC برای مبالغ کم",
            "API کامل",
            "کارمزد منطقی"
        ],
        "setup_difficulty": "آسان",
        "persian_support": "خیر",
        "recommendation": "برای تنوع بالا"
    }
}

def generate_exchange_comparison():
    """مقایسه صرافی‌های جایگزین"""
    
    report = """
🏪 راهنمای کامل صرافی‌های جایگزین Binance

===============================================

🥇 **پیشنهاد اول: KuCoin** (بهترین گزینه)
   • وب‌سایت: https://www.kucoin.com
   • ویژگی: بدون هیچ محدودیت جغرافیایی
   • API: قدرتمند و کامل
   • معاملات: 500+ جفت ارز
   • مزیت: دقیقاً مثل Binance اما بدون محدودیت
   • راه‌اندازی: 10 دقیقه

🥈 **پیشنهاد دوم: Coinbase Pro** (امن‌ترین)
   • وب‌سایت: https://pro.coinbase.com  
   • ویژگی: کاملاً قانونی و مجاز
   • API: عالی و مستند
   • معاملات: 200+ جفت ارز
   • مزیت: امنیت بسیار بالا
   • راه‌اندازی: 15 دقیقه (احراز هویت)

🥉 **پیشنهاد سوم: Kraken** (قدیمی‌ترین)
   • وب‌سایت: https://www.kraken.com
   • ویژگی: از 2011 فعال
   • API: بسیار پایدار
   • معاملات: 400+ جفت ارز  
   • مزیت: تجربه 12 ساله
   • راه‌اندازی: 15 دقیقه

⚡ **برای سرعت: Bybit** (سریع‌ترین)
   • وب‌سایت: https://www.bybit.com
   • ویژگی: UI بسیار ساده
   • API: سریع و قابل اعتماد
   • معاملات: 300+ جفت ارز
   • مزیت: سرعت بالا
   • راه‌اندازی: 5 دقیقه

🔥 **برای تنوع: Gate.io** (بیشترین کوین)
   • وب‌سایت: https://www.gate.io
   • ویژگی: 1000+ کوین مختلف
   • API: کامل و جامع
   • معاملات: حجم بالا
   • مزیت: تنوع فوق‌العاده
   • راه‌اندازی: 8 دقیقه

===============================================

💡 **توصیه برای وحید:**

1️⃣ شروع با KuCoin (دقیقاً مثل Binance)
2️⃣ اگر امنیت اولویت است: Coinbase Pro  
3️⃣ برای معاملات حرفه‌ای: Kraken

🚀 **مزایای استفاده از صرافی جایگزین:**
   ✅ بدون محدودیت IP
   ✅ دسترسی کامل به API
   ✅ سرعت بالاتر
   ✅ کارمزد مشابه یا کمتر
   ✅ امکان معاملات واقعی

===============================================
"""
    
    return report

def create_kucoin_setup_guide():
    """راهنمای نصب KuCoin"""
    
    guide = """
🚀 راهنمای راه‌اندازی KuCoin (10 دقیقه)

===============================================

مرحله 1️⃣: ثبت‌نام
   • برو به: https://www.kucoin.com
   • کلیک روی "Sign Up"
   • ایمیل و رمز عبور وارد کن
   • تایید ایمیل

مرحله 2️⃣: تنظیمات امنیتی
   • فعال‌سازی 2FA (Google Authenticator)
   • تنظیم رمز withdrawal
   • تایید شماره موبایل

مرحله 3️⃣: ایجاد API Key
   • برو به: Account > API Management
   • کلیک "Create API"
   • نام: "ULTRA_PLUS_BOT"
   • مجوزها: Trading + General
   • IP Whitelist: خالی بذار (برای Replit)
   • ذخیره API Key و Secret

مرحله 4️⃣: تست API
   • کپی API Key و Secret
   • تست با endpoint: /api/v1/accounts
   • تایید دسترسی

مرحله 5️⃣: واریز اولیه
   • برو به Assets > Deposit
   • انتخاب USDT یا BTC
   • واریز مبلغ دلخواه

===============================================

🔧 **API Endpoints مهم KuCoin:**

• Base URL: https://api.kucoin.com
• Price: /api/v1/market/orderbook/level1?symbol=BTC-USDT
• Balance: /api/v1/accounts
• Order: /api/v1/orders
• History: /api/v1/fills

===============================================

✅ **مزایای KuCoin:**
   🌍 بدون محدودیت جغرافیایی
   ⚡ سرعت عالی
   💰 کارمزد 0.1% (مشابه Binance)
   🔒 امنیت بالا
   📈 حجم معاملات زیاد

===============================================
"""
    
    return guide

if __name__ == "__main__":
    print(generate_exchange_comparison())
    print("\n" + "="*50 + "\n")
    print(create_kucoin_setup_guide())