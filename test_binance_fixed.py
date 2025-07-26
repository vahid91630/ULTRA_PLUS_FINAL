
# اضافه کردن به سیستم‌های موجود
try:
    from binance_fixed import binance_fixed
    
    # تست اتصال
    if binance_fixed.is_working():
        print("✅ Binance Fixed کار می‌کند")
        
        # دریافت قیمت نمونه
        btc_price = binance_fixed.get_price('BTCUSDT')
        eth_price = binance_fixed.get_price('ETHUSDT')
        
        print(f"💰 BTC: ${btc_price}")
        print(f"💰 ETH: ${eth_price}")
        
    else:
        print("❌ Binance Fixed کار نمی‌کند")
        
except Exception as e:
    print(f"خطا در import: {e}")
