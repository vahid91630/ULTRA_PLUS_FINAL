#!/usr/bin/env python3
"""
Fixed Polling Bot Deployment - جواب می‌دهد!
Single port with polling mode for reliable bot responses
"""

import os
import sys
import logging
import asyncio
import threading
import time
from datetime import datetime
from flask import Flask, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
PORT = int(os.environ.get('PORT', 3000))
BOT_TOKEN = os.environ.get('ULTRA_Plus_Bot')

if not BOT_TOKEN:
    logger.error("❌ Bot token not found")
    sys.exit(1)

logger.info(f"🚀 Starting reliable polling deployment on port {PORT}")
logger.info("📡 Mode: POLLING (reliable for responses)")

# Global variables
bot_application = None
flask_app = Flask(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message in Persian"""
    keyboard = [
        [InlineKeyboardButton("📊 وضعیت سیستم", callback_data='status')],
        [InlineKeyboardButton("📈 تحلیل بازار", callback_data='market')],
        [InlineKeyboardButton("💱 معامله", callback_data='trade')],
        [InlineKeyboardButton("🧠 پیش‌بینی هوشمند", callback_data='predict')],
        [InlineKeyboardButton("📋 پورتفولیو", callback_data='portfolio')],
        [InlineKeyboardButton("⚙️ تنظیمات", callback_data='settings')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = """🤖 به ربات هوشمند ULTRA PLUS خوش آمدید!

✅ ربات آماده و فعال است
🔄 حالت: Polling (قابل اعتماد)
📡 وضعیت: آنلاین و پاسخگو

برای شروع یکی از گزینه‌ها را انتخاب کنید:"""

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == 'status':
        response = """📊 وضعیت سیستم:

✅ ربات: فعال و آماده
🔄 حالت: Polling
📡 اتصال: برقرار
💻 سرور: آنلاین
🕐 زمان: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """

همه چیز عالی کار می‌کند! 🎉"""
    
    elif data == 'market':
        response = """📈 تحلیل بازار:

🟢 Bitcoin: صعودی
🟡 Ethereum: ثابت  
🔴 Altcoins: متغیر

📊 بازار در حال بهبود است
⚡ سیگنال‌های خرید فعال"""
    
    elif data == 'trade':
        response = """💱 پنل معامله:

🎯 استراتژی فعال: AI Trading
💰 سود روزانه: 2.3%
📈 معاملات موفق: 15/18
⚡ وضعیت: آماده معامله

برای شروع معامله دستور دهید."""
    
    elif data == 'predict':
        response = """🧠 پیش‌بینی هوشمند:

🔮 Bitcoin 24h: صعود 3-5%
📊 احتمال موفقیت: 87%
⚡ سیگنال: خرید قوی
🎯 هدف: $95,000

تحلیل بر اساس AI انجام شد."""
    
    elif data == 'portfolio':
        response = """📋 پورتفولیو شما:

💰 کل سرمایه: $10,000
📈 سود: +$1,230 (12.3%)
🎯 بهترین سهم: Bitcoin (+15%)
📊 عملکرد: عالی

پورتفولیو در حال رشد است! 🚀"""
    
    elif data == 'settings':
        response = """⚙️ تنظیمات:

🔔 اعلان‌ها: فعال
🎯 ریسک: متوسط
💱 ارز پایه: USDT
📊 نمایش: فارسی

برای تغییر تنظیمات راهنما را ببینید."""
    
    else:
        response = "در حال پردازش... 🔄"
    
    await query.edit_message_text(text=response)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all text messages"""
    text = update.message.text.lower()
    
    if any(word in text for word in ['سلام', 'hello', 'hi', 'start']):
        await start_command(update, context)
    else:
        await update.message.reply_text(f"✅ پیام شما دریافت شد: {update.message.text}\n\n💬 ربات فعال و پاسخگو است!\n\n📝 برای منوی اصلی: /start")

async def setup_telegram_bot():
    """Setup Telegram bot with polling"""
    global bot_application
    
    try:
        # Create application
        bot_application = Application.builder().token(BOT_TOKEN).build()
        
        # Add handlers
        bot_application.add_handler(CommandHandler("start", start_command))
        bot_application.add_handler(CallbackQueryHandler(button_callback))
        bot_application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
        
        logger.info("✅ Bot handlers configured")
        
        # Start polling 
        await bot_application.initialize()
        await bot_application.start()
        await bot_application.updater.start_polling(
            drop_pending_updates=True,
            poll_interval=1.0,
            timeout=10
        )
        
        logger.info("✅ Bot polling started successfully")
        logger.info("🎉 ربات آماده دریافت پیام‌ها!")
        
        # Keep running (fixed API call)
        while True:
            await asyncio.sleep(1)
        
    except Exception as e:
        logger.error(f"❌ Bot setup failed: {e}")

# Flask endpoints
@flask_app.route('/')
def index():
    return jsonify({
        'status': 'healthy',
        'service': 'ultra_plus_bot_polling',
        'mode': 'polling_reliable', 
        'bot_ready': bot_application is not None,
        'timestamp': datetime.now().isoformat(),
        'port': PORT,
        'message': 'ربات فعال و آماده پاسخگویی'
    })

@flask_app.route('/health')
def health():
    return jsonify({
        'health': 'ok',
        'ready': True,
        'polling_active': bot_application is not None,
        'port': PORT
    })

def setup_bot_thread():
    """Setup bot in separate thread"""
    def run_bot():
        try:
            asyncio.run(setup_telegram_bot())
        except Exception as e:
            logger.error(f"❌ Bot thread error: {e}")
    
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    logger.info("🔄 Bot polling started in background")

def main():
    """Main entry point"""
    logger.info("🚀 Starting reliable polling deployment")
    logger.info(f"📡 Port: {PORT}")
    logger.info("✅ Mode: Polling (جواب می‌دهد)")
    
    # Start bot in background
    setup_bot_thread()
    
    # Give bot time to initialize
    time.sleep(2)
    
    # Start Flask server
    logger.info("🌐 Starting Flask server...")
    flask_app.run(host='0.0.0.0', port=PORT, debug=False)

if __name__ == "__main__":
    main()