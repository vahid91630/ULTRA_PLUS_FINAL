# 🔑 راهنمای تنظیم API Keys برای معاملات واقعی

## 🚨 هشدار مهم: 
ربات شما اکنون قدرت معاملات واقعی دارد. تنظیم API Key ها برای فعال‌سازی قدرت خرید و فروش ضروری است.

---

## 🏪 **صرافی‌های پشتیبانی شده:**

### 1. 🟡 **Binance (پیشنهادی اول)**

**مراحل تنظیم:**
1. وارد حساب Binance خود شوید
2. برو به: Profile → API Management
3. Create API → نام دلخواه بنویسید
4. ✅ فعال کنید: **Spot & Margin Trading**
5. ✅ فعال کنید: **Futures Trading** (اختیاری)
6. ❌ غیرفعال: **Withdrawals** (امنیت)

**Environment Variables:**
```
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_SECRET=your_binance_secret_here
```

---

### 2. 🔵 **Coinbase Pro**

**مراحل تنظیم:**
1. وارد Coinbase Pro شوید  
2. Settings → API
3. New API Key → نام: "ULTRA_PLUS_BOT"
4. ✅ Permissions: **View + Trade**
5. ❌ غیرفعال: **Transfer** (امنیت)
6. Passphrase را یادداشت کنید

**Environment Variables:**
```
COINBASE_API_KEY=your_coinbase_api_key
COINBASE_SECRET=your_coinbase_secret  
COINBASE_PASSPHRASE=your_passphrase
```

---

### 3. 🟢 **KuCoin**

**مراحل تنظیم:**
1. وارد KuCoin شوید
2. API Management → Create API
3. نام: "UltraPlusBot"
4. ✅ Permissions: **General + Trade**
5. ❌ غیرفعال: **Withdraw + Transfer**
6. IP Restriction: اختیاری

**Environment Variables:**
```
KUCOIN_API_KEY=your_kucoin_api_key
KUCOIN_SECRET=your_kucoin_secret
KUCOIN_PASSPHRASE=your_kucoin_passphrase
```

---

## 🛡️ **تنظیمات امنیتی (بسیار مهم):**

### ✅ **موارد ضروری:**
1. **فقط Trading Permission** - هیچ‌گاه Withdrawal فعال نکنید
2. **IP Whitelist** - IP سرور را محدود کنید
3. **Sandbox Mode** - ابتدا حتماً تست کنید
4. **Small Amounts** - با مبالغ کم شروع کنید

### ❌ **هرگز فعال نکنید:**
- Withdrawal Permission
- Margin Trading (در ابتدا)
- Futures Trading (اختیاری)
- Transfer Permission

---

## 🔧 **تنظیم در Replit:**

### **روش 1: Environment Variables (امن)**
```bash
# در terminal Replit:
export BINANCE_API_KEY="your_key_here"
export BINANCE_SECRET="your_secret_here"
```

### **روش 2: Secrets (بهترین)**
1. در Replit: Tools → Secrets
2. اضافه کردن:
   - Name: `BINANCE_API_KEY`, Value: `your_key`
   - Name: `BINANCE_SECRET`, Value: `your_secret`

---

## 🧪 **تست اولیه (Sandbox Mode):**

```python
# تست اتصال
from real_trading_engine import trading_engine, initialize_trading_engine

# راه‌اندازی
await initialize_trading_engine()

# تست موجودی
balance = await trading_engine.get_account_balance()
print(f"Total Balance: ${balance['total_usd']}")
```

---

## 📊 **نحوه کار ربات با API Keys:**

### **هنگام فعال‌سازی:**
1. ربات به صرافی‌ها متصل می‌شود
2. موجودی واقعی را چک می‌کند
3. فرصت‌های معاملاتی را پیدا می‌کند
4. با اطمینان 80%+ معامله می‌کند

### **محدودیت‌های امنیتی:**
- حداکثر $1,000 هر معامله
- حداکثر $500 ضرر روزانه  
- حداکثر 5 معامله همزمان
- فقط معاملات Spot (نه Futures)

---

## 🎯 **نتیجه:**

بعد از تنظیم API Key ها:
- ✅ ربات قدرت خرید و فروش واقعی دارد
- ✅ تحلیل → تصمیم → اجرا (همه خودکار)
- ✅ گزارش لحظه‌ای تمام معاملات
- ✅ کنترل کامل توسط شما

---

## 🆘 **در صورت مشکل:**

1. **API Key کار نمی‌کند:**
   - Permissions را چک کنید
   - IP Restrictions را بررسی کنید
   - API Key را دوباره بسازید

2. **ربات معامله نمی‌کند:**
   - موجودی کافی داشته باشید
   - Sandbox mode را غیرفعال کنید
   - تنظیمات Trading Permission

3. **خطاهای اتصال:**
   - اتصال اینترنت بررسی کنید
   - Rate limiting ممکن است فعال باشد

---

**🎖️ بعد از تنظیم API Keys، ربات شما قدرت کامل معاملات واقعی خواهد داشت!**