# 🔄 راهنمای کامل نصب UptimeRobot برای ULTRA_PLUS_BOT

## 📋 مرحله 1: آماده‌سازی پروژه

### 1.1 اضافه کردن Keep-Alive به پروژه‌تان

```python
# در فایل اصلی ربات‌تان (مثلاً main.py یا bot.py)
from keep_alive import keep_alive

def main():
    # شروع keep-alive در ابتدای برنامه
    keep_alive()
    
    # کدهای اصلی ربات‌تان
    # ...
```

### 1.2 تست کردن Keep-Alive

پس از اجرای پروژه، این لینک‌ها باید کار کنند:
- `https://your-username.your-repl-name.repl.co/` - صفحه اصلی
- `https://your-username.your-repl-name.repl.co/ping` - برای UptimeRobot
- `https://your-username.your-repl-name.repl.co/health` - بررسی سلامت

## 🌐 مرحله 2: پیدا کردن URL پروژه Replit

### 2.1 روش‌های پیدا کردن URL:

1. **از داخل Replit:**
   - پروژه‌تان را اجرا کنید
   - روی دکمه "Open in new tab" کنار آدرس کلیک کنید
   - URL به شکل: `https://your-username.your-repl-name.repl.co` خواهد بود

2. **فرمت استاندارد:**
   ```
   https://[نام-کاربری-شما].[نام-پروژه].repl.co
   ```

## 🤖 مرحله 3: ثبت‌نام در UptimeRobot

### 3.1 ایجاد حساب کاربری:

1. به سایت [UptimeRobot.com](https://uptimerobot.com) بروید
2. روی "Sign Up Free" کلیک کنید
3. اطلاعات خود را وارد کنید:
   - ایمیل
   - رمز عبور
   - نام و نام خانوادگی

### 3.2 تأیید ایمیل:
- ایمیل تأیید را چک کنید
- روی لینک تأیید کلیک کنید

## ⚙️ مرحله 4: تنظیم Monitor در UptimeRobot

### 4.1 ایجاد Monitor جدید:

1. وارد پنل UptimeRobot شوید
2. روی "+ Add New Monitor" کلیک کنید

### 4.2 تنظیمات Monitor:

```
Monitor Type: HTTP(s)
Friendly Name: ULTRA_PLUS_BOT Keep-Alive
URL (or IP): https://your-username.your-repl-name.repl.co/ping
Monitoring Interval: 5 minutes
```

### 4.3 تنظیمات پیشرفته:

- **HTTP Method:** GET
- **HTTP Status Codes:** 200
- **Keyword Monitoring:** فعال نکنید (اختیاری)
- **Timeout:** 30 seconds

## 📱 مرحله 5: تنظیم هشدارها (اختیاری)

### 5.1 انواع هشدار:

1. **Email Alert:**
   - ایمیل خود را وارد کنید
   - نوع هشدار: Down & Up

2. **Telegram Alert:**
   - ربات UptimeRobot را در تلگرام پیدا کنید: `@UptimeRobotBot`
   - `/start` را بزنید و Chat ID دریافت کنید

## 🎯 مرحله 6: تست و راه‌اندازی نهایی

### 6.1 تست Monitor:

1. Monitor ایجاد شده را انتخاب کنید
2. روی "Test" کلیک کنید
3. باید پیام موفقیت دریافت کنید

### 6.2 بررسی عملکرد:

```bash
# تست دستی از terminal
curl -s https://your-username.your-repl-name.repl.co/ping

# خروجی انتظاری:
{
  "status": "alive",
  "message": "I'm alive!",
  "timestamp": "2025-07-24T...",
  "bot": "ULTRA_PLUS_BOT"
}
```

## 🔧 رفع مشکلات رایج

### مشکل 1: URL کار نمی‌کند
**علت:** پروژه در حال اجرا نیست
**راه‌حل:** پروژه را در Replit اجرا کنید

### مشکل 2: Monitor Failed می‌شود
**علت:** Keep-Alive درست اجرا نشده
**راه‌حل:** 
```python
# اطمینان از اجرای keep_alive() در ابتدای برنامه
from keep_alive import keep_alive
keep_alive()
```

### مشکل 3: پورت 8080 اشغال است
**علت:** چندین instance از keep-alive اجرا شده
**راه‌حل:**
```bash
# متوقف کردن فرآیندهای قبلی
pkill -f "keep_alive"
```

## 📊 مزایای استفاده از UptimeRobot

✅ **رایگان:** تا 50 monitor رایگان
✅ **قابل اعتماد:** بررسی هر 5 دقیقه
✅ **هشدار فوری:** اطلاع از قطعی فوری
✅ **آمار کامل:** Uptime آمار و گزارش‌ها
✅ **API:** امکان مدیریت از طریق API

## 🚀 نکات بهینه‌سازی

### 1. بهبود Performance:
```python
# در keep_alive.py تنظیمات بهینه شده
app.run(
    host='0.0.0.0',
    port=8080,
    debug=False,        # حتماً False
    use_reloader=False, # جلوگیری از restart
    threaded=True       # پردازش موازی
)
```

### 2. Monitoring بیشتر:
- Health endpoint: `/health`
- Status endpoint: برای اطلاعات کامل سیستم

### 3. لاگ‌گیری:
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## 🔐 نکات امنیتی

1. **محدود کردن دسترسی:** فقط endpoint های ضروری را expose کنید
2. **Rate Limiting:** در production محدودیت درخواست اعمال کنید
3. **HTTPS:** همیشه از HTTPS استفاده کنید (Replit خودکار فراهم می‌کند)

---

## ✅ چک‌لیست نهایی

- [ ] فایل `keep_alive.py` ایجاد شد
- [ ] `keep_alive()` در فایل اصلی اضافه شد  
- [ ] پروژه اجرا شد و `/ping` کار می‌کند
- [ ] URL پروژه Replit پیدا شد
- [ ] حساب UptimeRobot ایجاد شد
- [ ] Monitor با تنظیمات صحیح اضافه شد
- [ ] تست Monitor موفق بود
- [ ] هشدارها تنظیم شدند (اختیاری)

**🎉 تبریک! ربات شما حالا 24/7 زنده خواهد ماند!**