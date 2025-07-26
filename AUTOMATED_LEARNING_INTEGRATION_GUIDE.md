# 🤖 Automated Daily Learning Integration Guide

## Overview
Complete automated pipeline that runs daily at 23:59 UTC, processing financial data, scoring insights, storing to MongoDB, and sending Telegram reports - all without manual intervention.

## 🎯 What It Does Automatically

### Daily Pipeline (23:59 UTC)
1. **📖 Data Collection** - Reads from daily_data.json, collected_data.json, or Replit DB
2. **🧮 Smart Scoring** - Applies weighted scoring algorithm
3. **🔍 Quality Filtering** - Keeps only entries with score ≥60
4. **💾 MongoDB Storage** - Stores qualified insights with automatic cleanup
5. **🧠 Knowledge Base** - Updates bot's learning database with top insights (score ≥80)
6. **🧹 Cleanup** - Creates backups and clears local data files
7. **📱 Telegram Report** - Sends detailed success/failure report in Persian

### Scoring Algorithm
- **+20 points** if content is <48 hours old (freshness)
- **+30 points** if from trusted source (Investopedia, CoinGecko, Binance, TradingView, etc.)
- **+10 points** per relevant tag (BTC, ETH, RSI, breakout, support, trend, volume, etc.)
- **Minimum 60** points required to qualify for storage

## 🚀 Quick Integration

### Option 1: Simple Integration (Recommended)
```python
from simple_automation_starter import add_automation_to_bot
from telegram.ext import Application

# Your existing bot
app = Application.builder().token("YOUR_BOT_TOKEN").build()

# Add your existing handlers here...

# Enable automated learning
add_automation_to_bot(app)

# Start bot
app.run_polling()
```

### Option 2: Manual Integration
```python
from automated_daily_processor import start_automated_learning

# Start automation with your bot's details
processor = start_automated_learning(
    telegram_token="YOUR_BOT_TOKEN",
    chat_id="559649958",  # Vahid's chat ID
    mongodb_uri="YOUR_MONGODB_URI"
)
```

### Option 3: Add to Existing Bot
```python
from daily_scheduler_integration import enable_daily_automation

# Add to your existing telegram application
enable_daily_automation(your_telegram_app, mongodb_uri="YOUR_MONGODB_URI")
```

## 📱 Available Telegram Commands

Once integrated, users get these commands:

- `/start_automation` - Start the daily automation system
- `/stop_automation` - Stop all automated processing  
- `/automation_status` - Check current status and next run time
- `/finalize_day` - Manually trigger processing (for testing)
- `/data_status` - Check local data and MongoDB status

## 🧪 Testing the System

### Test with Sample Data
```python
# Create sample data file
import json
sample_data = [
    {
        "content": "Bitcoin breaks resistance at $67,000 with high volume",
        "timestamp": "2025-07-21T20:00:00",
        "source": "CoinGecko",
        "tags": ["BTC", "breakout", "volume"]
    }
]

with open('daily_data.json', 'w') as f:
    json.dump(sample_data, f)

# Test the pipeline
from automated_daily_processor import AutomatedDailyProcessor
import asyncio

async def test():
    processor = AutomatedDailyProcessor()
    result = await processor._process_daily_pipeline()
    print(f"Success: {result['success']}")
    print(f"Qualified: {result['qualified_entries']}")

asyncio.run(test())
```

### Manual Trigger
```bash
# Run once manually for testing
python3 automated_daily_processor.py
```

## ⚙️ Configuration

### Environment Variables
```bash
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/trading_bot
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=559649958  # Optional, defaults to Vahid's ID
```

### Scoring Configuration
Modify these values in `AutomatedDailyProcessor`:
```python
self.scoring_config = {
    'freshness_points': 20,      # <48 hours
    'trusted_source_points': 30,  # Trusted sources
    'relevant_tag_points': 10,    # Per relevant tag
    'minimum_score': 60          # Filter threshold
}
```

### Trusted Sources
Currently includes:
- Investopedia, CoinGecko, Binance, TradingView
- CoinDesk, CoinTelegraph, MarketWatch  
- Reuters, Bloomberg, Yahoo Finance

### Relevant Tags
Key financial terms:
- Indicators: RSI, MACD, Bollinger
- Cryptocurrencies: BTC, ETH, Bitcoin, Ethereum
- Trading: breakout, support, resistance, trend, volume
- Sentiment: bullish, bearish, analysis

## 📊 MongoDB Collections

### `daily_insights`
Stores qualified daily insights:
```json
{
  "content": "Bitcoin breaks resistance...",
  "score": 80,
  "tags": ["BTC", "breakout", "volume"],
  "source": "CoinGecko", 
  "date_saved": "2025-07-21 23:59:45",
  "original_timestamp": "2025-07-21T20:00:00",
  "processed_by": "automated_daily_processor"
}
```

### `knowledge` 
High-quality insights for bot's knowledge base:
```json
{
  "insight": "Bitcoin breaks resistance...",
  "source": "CoinGecko",
  "tags": ["BTC", "breakout"],
  "confidence_score": 0.8,
  "added_date": "2025-07-21T23:59:45",
  "category": "daily_learning"
}
```

## 📱 Telegram Report Format

### Success Report (Persian)
```
🤖 گزارش خودکار یادگیری روزانه
⏰ زمان: 2025-07-21 23:59 UTC

📊 نتایج پردازش:
• مجموع ورودی‌ها: 15
• ورودی‌های واجد شرایط: 8  
• ذخیره شده در MongoDB: 8

🏆 برترین بینش (امتیاز: 90):
Bitcoin breaks key resistance at $68,000...

✅ وضعیت: پردازش خودکار با موفقیت تکمیل شد
🧠 پایگاه دانش: بروزرسانی شد با بینش‌های عالی

📅 بعدی: فردا در ساعت 23:59 UTC
```

### Error Report (Persian)
```
🤖 گزارش خودکار یادگیری روزانه  
⏰ زمان: 2025-07-21 23:59 UTC

❌ خطا در پردازش خودکار

📊 آمار:
• مجموع ورودی‌ها: 15
• ورودی‌های واجد شرایط: 8

🚨 مشکلات:
• Failed to connect to MongoDB
• No daily data found

🔧 توصیه: بررسی اتصال MongoDB و فایل‌های داده
```

## 🔧 Troubleshooting

### Common Issues

#### 1. MongoDB Connection Failed
```
Error: Invalid URI scheme: URI must begin with 'mongodb://'
```
**Solution:** Set proper DATABASE_URL environment variable:
```bash
export DATABASE_URL="mongodb+srv://username:password@cluster.mongodb.net/trading_bot"
```

#### 2. No Data Found
```
Error: No daily data found
```
**Solution:** Ensure your bot creates daily_data.json during the day or use sample data for testing

#### 3. Telegram Reports Not Sent
```
Warning: No Telegram bot or chat_id configured
```
**Solution:** Provide bot token and chat ID:
```python
processor = start_automated_learning(
    telegram_token="YOUR_BOT_TOKEN",
    chat_id="559649958"
)
```

### Debug Mode
Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Manual Testing
Test individual components:
```python
# Test scoring
from automated_daily_processor import AutomatedDailyProcessor
processor = AutomatedDailyProcessor()

sample_entry = {
    "content": "BTC shows bullish RSI divergence",
    "timestamp": "2025-07-21T20:00:00",
    "source": "TradingView", 
    "tags": ["BTC", "RSI", "bullish"]
}

score = processor._calculate_score(sample_entry)
print(f"Score: {score}")  # Should be 70 (20+30+20)
```

## 🚀 Production Deployment

### For Replit
1. Set environment variables in Replit Secrets
2. Add automation to your existing bot
3. The system runs automatically - no manual intervention needed

### For Railway/Heroku
1. Set environment variables in platform settings
2. Ensure your app runs 24/7 (not just on requests)
3. System will schedule and run automatically

## 📈 Performance Considerations

### Memory Optimization (Replit Free Tier)
- Processes data in small batches (20-25 items)
- Automatic cleanup of old backups
- Limits content and tags to prevent memory bloat
- Uses frozenset for constant lookups

### Storage Optimization
- Deletes previous day's data automatically
- Keeps knowledge base under 1000 entries
- Creates timestamped backups, keeps only 3 recent

### Network Optimization
- Minimal MongoDB connection pool
- Short connection timeouts
- Batch operations for efficiency

## 🔄 Customization

### Change Schedule
Modify the cron trigger:
```python
# Daily at different time
trigger=CronTrigger(hour=22, minute=0, timezone='UTC')

# Multiple times per day  
trigger=CronTrigger(hour='6,12,18,23', minute=59)

# Weekly only
trigger=CronTrigger(day_of_week='sun', hour=23, minute=59)
```

### Custom Scoring
Override the scoring method:
```python
class CustomProcessor(AutomatedDailyProcessor):
    def _calculate_score(self, entry):
        # Your custom scoring logic
        return super()._calculate_score(entry) + custom_boost
```

### Additional Data Sources
Add more input files:
```python
json_files = ['daily_data.json', 'news_data.json', 'market_data.json']
```

## 📋 Integration Checklist

- [ ] Install apscheduler: `pip install apscheduler`
- [ ] Set DATABASE_URL environment variable
- [ ] Set TELEGRAM_BOT_TOKEN (optional but recommended)
- [ ] Import and add to your existing bot
- [ ] Test with sample data
- [ ] Verify MongoDB connection
- [ ] Check Telegram reports
- [ ] Confirm 23:59 UTC scheduling
- [ ] Monitor first automated run

## ✅ Success Indicators

Your automation is working correctly when you see:
1. Daily Telegram reports at 23:59 UTC
2. New entries in MongoDB `daily_insights` collection  
3. Knowledge base updates with high-quality insights
4. Local data files cleaned up with backups created
5. No errors in bot logs during processing

The system is now fully autonomous and will continuously learn and improve your bot's knowledge base without any manual intervention.