# 🎯 مراحل فوری Deploy به Railway

## **مرحله 1: GitHub Repository (2 دقیقه)**

### **گام اول: ساخت Repository**
1. برو به `github.com`
2. کلیک `New repository`
3. نام: `ultra-plus-bot-railway`
4. انتخاب Public یا Private
5. کلیک `Create repository`

### **گام دوم: آپلود فایل‌ها**
فایل‌های زیر را در repository آپلود کنید:

**فایل‌های اصلی (کپی از Replit):**
- `restored_original_bot.py`
- `demo_trading_engine.py`

**فایل‌های Deploy (آماده شده):**
- `requirements.txt` (از فولدر railway_deployment_files)
- `Procfile` (از فولدر railway_deployment_files)
- `railway.toml` (از فولدر railway_deployment_files)
- `runtime.txt` (از فولدر railway_deployment_files)

---

## **مرحله 2: Railway Setup (3 دقیقه)**

### **ثبت‌نام Railway:**
1. برو به `railway.app`
2. کلیک `Login with GitHub`
3. اجازه دسترسی بده
4. $5 رایگان خودکار فعال می‌شود

### **Connect Repository:**
1. کلیک `New Project`
2. انتخاب `Deploy from GitHub repo`
3. انتخاب `ultra-plus-bot-railway`
4. کلیک `Deploy Now`

---

## **مرحله 3: Environment Variables (2 دقیقه)**

### **Variables لازم:**
```
ULTRA_Plus_Bot = 7978020048:AAGaNxhYpyPmJ1NUGCY7woyGYCninJVaN9Y
PORT = 5000
```

### **نحوه اضافه کردن:**
1. Railway Dashboard → Variables tab
2. کلیک `New Variable`
3. Name: `ULTRA_Plus_Bot`
4. Value: `7978020048:AAGaNxhYpyPmJ1NUGCY7woyGYCninJVaN9Y`
5. کلیک `Add`
6. همین کار برای PORT (اگر نیاز بود)

---

## **مرحله 4: تست (1 دقیقه)**

### **بررسی Deploy:**
1. Railway Dashboard → Logs
2. مطمئن شوید "Application started" ببینید
3. URL شما: `https://yourapp.railway.app`
4. Health check: `https://yourapp.railway.app/health`

### **تست Telegram:**
1. در تلگرام /start بفرستید
2. باید منوی فارسی جواب دهد
3. تست دکمه‌ها

---

## **زمان کل: 8 دقیقه**
## **نتیجه: ربات 24/7 روی Railway**

---

## **اگر مشکلی پیش آمد:**

### **Deploy ناموفق:**
- بررسی Logs در Railway
- مطمئن شوید requirements.txt کامل است
- Environment Variables چک کنید

### **Bot جواب نمی‌دهد:**
- Bot token را دوباره بررسی کنید
- Health endpoint تست کنید
- Telegram API limits چک کنید

### **سرعت کم:**
- منتظر باشید تا auto-scaling فعال شود
- معمولاً 2-3 دقیقه طول می‌کشد

---

## **پس از Deploy موفق:**

✅ ربات 24/7 کار می‌کند  
✅ آدرس دائمی دارید  
✅ Auto-restart فعال  
✅ Monitoring در Railway Dashboard  
✅ $5 رایگان ماهانه  
✅ Performance بهتر از Replit  

**آماده شروع؟**