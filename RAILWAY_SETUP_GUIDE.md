# 🚂 راهنمای کامل Railway Deploy - 24/7 امن و سریع

## 🎯 **مراحل Deploy به Railway (10 دقیقه)**

### **مرحله 1: آماده‌سازی GitHub Repository**

#### **گام 1: ساخت Repository**
1. برو به `github.com`
2. کلیک `New repository`
3. نام: `ultra-plus-bot-railway`
4. Public یا Private (هر کدام)
5. کلیک `Create repository`

#### **گام 2: آپلود فایل‌های آماده شده**
فایل‌های زیر را در repository قرار دهید:

```
📁 Repository Structure:
├── restored_original_bot.py     (main bot file)
├── demo_trading_engine.py       (trading system)
├── requirements.txt             (dependencies - آماده شده)
├── Procfile                     (railway config - آماده شده)
├── railway.toml                 (deployment config - آماده شده)
├── runtime.txt                  (python version - آماده شده)
└── README.md                    (توضیحات)
```

---

### **مرحله 2: فعال‌سازی Railway**

#### **گام 1: ثبت‌نام Railway**
1. برو به `railway.app`
2. کلیک `Login with GitHub`
3. اجازه دسترسی به GitHub بده
4. $5 credit رایگان خودکار فعال می‌شود

#### **گام 2: Deploy پروژه**
1. کلیک `New Project`
2. انتخاب `Deploy from GitHub repo`
3. انتخاب repository ربات (`ultra-plus-bot-railway`)
4. کلیک `Deploy Now`

---

### **مرحله 3: تنظیمات Environment Variables**

#### **Variables مورد نیاز:**
```bash
# Telegram Bot
ULTRA_Plus_Bot = 7978020048:AAGaNxhYpyPmJ1NUGCY7woyGYCninJVaN9Y

# Port (خودکار تنظیم می‌شود)
PORT = 5000

# OpenAI (اختیاری - اگر دارید)
OPENAI_API_KEY = your_openai_key_here

# MongoDB (اختیاری - اگر استفاده می‌کنید)
MONGODB_URI = your_mongodb_connection_string
```

#### **نحوه تنظیم Variables:**
1. در Railway Dashboard → Variables tab
2. کلیک `New Variable`
3. برای هر variable:
   - Name: نام variable
   - Value: مقدار آن
4. کلیک `Add`
5. Redeploy خودکار انجام می‌شود

---

### **مرحله 4: تست و تأیید Deploy**

#### **بررسی موفقیت:**

1. **Deploy Logs بررسی کنید:**
```
✅ نباید خطایی باشد
✅ باید "Application started" نمایش دهد
✅ باید "Telegram bot initialized" ببینید
```

2. **URL Health Check:**
```
https://yourapp.railway.app/health
Response باید باشد: {"status": "healthy", "bot": "active"}
```

3. **Telegram Bot Test:**
```
در تلگرام:
- ربات را پیدا کنید
- /start بفرستید
- باید منوی فارسی جواب دهد
```

---

## 🔧 **فایل‌های آماده Deploy:**

### **✅ requirements.txt (آماده شده):**
```python
python-telegram-bot==20.7
openai==1.3.7
flask==3.0.0
requests==2.31.0
pymongo==4.6.0
motor==3.3.2
asyncio
aiohttp
ccxt
psutil
python-dotenv
gunicorn==21.2.0
```

### **✅ Procfile (آماده شده):**
```
web: gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 0 restored_original_bot:app
```

### **✅ railway.toml (آماده شده):**
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 0 restored_original_bot:app"
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 10

[[services]]
serviceName = "ultra-plus-bot"

[env]
PORT = "5000"
```

### **✅ runtime.txt (آماده شده):**
```
python-3.11.6
```

---

## 💰 **هزینه‌ها و مزایا:**

### **Railway Pricing:**
- **رایگان**: $5 credit ماهانه
- **Usage**: معمولاً $3-5 برای ربات متوسط
- **Unlimited**: بدون محدودیت ساعت

### **مزایای Railway:**
```
✅ 24/7 Always-On بدون خوابیدن
✅ Auto-scaling خودکار
✅ SSL Certificate رایگان
✅ Custom Domain پشتیبانی
✅ GitHub Auto-Deploy
✅ Real-time Logs
✅ Database Add-ons
✅ 99.9% Uptime SLA
```

---

## 🔒 **ویژگی‌های امنیتی:**

### **امنیت Railway:**
- **SOC 2 Type II Compliance**
- **AWS Infrastructure** (همان Netflix)
- **DDoS Protection** خودکار
- **Environment Variables Encryption**
- **Network Isolation**
- **Regular Security Updates**

### **SSL/TLS:**
- **Automatic HTTPS** برای تمام domains
- **Certificate Management** خودکار
- **TLS 1.3 Support**

---

## 🚀 **پس از Deploy:**

### **URL‌های مفید:**
```
Main URL: https://yourapp.railway.app/
Health: https://yourapp.railway.app/health
Logs: Railway Dashboard → Logs tab
Metrics: Railway Dashboard → Metrics tab
```

### **Monitoring:**
- **Real-time Logs** در Railway Dashboard
- **CPU/Memory Usage** charts
- **Request/Response** metrics
- **Error Tracking** خودکار

---

## 🆘 **Troubleshooting:**

### **اگر Deploy ناموفق:**
1. **بررسی Deploy Logs** در Railway Dashboard
2. **مطمئن شوید requirements.txt کامل** است
3. **Environment Variables** را بررسی کنید
4. **Port settings** را چک کنید

### **اگر Bot جواب نمی‌دهد:**
1. **Bot Token** در Variables بررسی کنید
2. **Health endpoint** تست کنید
3. **Logs** را برای خطاها بررسی کنید
4. **Telegram API** limits چک کنید

### **اگر سرعت کم:**
1. **Region** را تغییر دهید (اگر ممکن است)
2. **Workers** تعداد را افزایش دهید
3. **Database** connection pool بهینه کنید

---

## 📋 **Checklist Deploy:**

### **قبل از Deploy:**
- [ ] GitHub repository آماده
- [ ] تمام فایل‌ها آپلود شده
- [ ] Bot token آماده
- [ ] Railway account ساخته شده

### **حین Deploy:**
- [ ] Repository به Railway متصل شده
- [ ] Environment variables تنظیم شده
- [ ] Deploy logs موفق
- [ ] Health endpoint پاسخ می‌دهد

### **بعد از Deploy:**
- [ ] Bot در تلگرام جواب می‌دهد
- [ ] /start کار می‌کند
- [ ] تمام menu items فعال
- [ ] 24/7 operation تأیید شده

---

## 🎯 **آماده شروع؟**

فایل‌های deploy آماده شده‌اند. مراحل:

1. **GitHub Repository** بسازید
2. **فایل‌های آماده شده** را آپلود کنید
3. **Railway** وصل کنید
4. **Environment Variables** تنظیم کنید
5. **Deploy** کنید!

**زمان کل: ~10 دقیقه**
**نتیجه: ربات 24/7 امن و سریع!**