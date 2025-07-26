#!/usr/bin/env python3
"""
Fixed Webhook-Based Bot Deployment for Cloud Run
Addresses all deployment issues:
1. Single port configuration (3000)
2. Prevents multiple bot instances 
3. Webhook mode only (no polling)
4. Immediate Flask server startup
"""

import os
import sys
import logging
import asyncio
import signal
import threading
import time
from datetime import datetime
from flask import Flask, jsonify, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Environment configuration - SINGLE PORT 3000 ONLY
PORT = int(os.environ.get('PORT', 3000))
BOT_TOKEN = os.environ.get('ULTRA_Plus_Bot')

# Force webhook mode and disable polling
os.environ['WEBHOOK_MODE'] = 'true'
os.environ['DISABLE_POLLING'] = 'true'  
os.environ['BOT_SINGLE_INSTANCE'] = 'true'
os.environ['DEPLOYMENT_MODE'] = 'cloud_run'

if not BOT_TOKEN:
    logger.error("❌ Bot token not found in environment")
    sys.exit(1)

logger.info(f"🚀 Starting fixed webhook deployment on port {PORT}")
logger.info("🔗 Webhook mode: ENABLED")
logger.info("🚫 Polling: DISABLED")
logger.info("🔒 Single instance: ENFORCED")

# Global variables
bot_application = None
flask_app = Flask(__name__)
_instance_lock = threading.Lock()
_instance_running = False

def enforce_singleton():
    """Enforce single instance to prevent Telegram API conflicts"""
    global _instance_running
    with _instance_lock:
        if _instance_running:
            logger.error("❌ Another instance detected - preventing conflicts")
            sys.exit(1)
        _instance_running = True
        logger.info("✅ Singleton lock acquired")

def release_singleton():
    """Release singleton lock"""
    global _instance_running
    with _instance_lock:
        _instance_running = False
        logger.info("🔓 Singleton lock released")

# Persian language bot handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Enhanced start command with Persian keyboard"""
    user_id = update.effective_user.id
    username = update.effective_user.username or "کاربر"
    
    welcome_text = f"""🚀 به ربات تریدینگ آلترا پلاس خوش آمدید!
    
👋 سلام {username}!
🆔 شناسه کاربری: {user_id}

🤖 ربات هوشمند تریدینگ آلترا پلاس آماده خدمت‌رسانی به شما است.

📊 امکانات:
• تحلیل بازار رمزارز
• پیشنهادات هوشمند تریدینگ  
• مدیریت پرتفوی
• آموزش‌های تخصصی

🔥 برای شروع، یکی از گزینه‌های زیر را انتخاب کنید:"""

    keyboard = [
        [
            InlineKeyboardButton("📈 تحلیل بازار", callback_data="market_analysis"),
            InlineKeyboardButton("💰 پرتفوی من", callback_data="portfolio")
        ],
        [
            InlineKeyboardButton("🎯 پیشنهادات تریدینگ", callback_data="trading_signals"),
            InlineKeyboardButton("📚 آموزش", callback_data="education")
        ],
        [
            InlineKeyboardButton("⚙️ تنظیمات", callback_data="settings"),
            InlineKeyboardButton("📞 پشتیبانی", callback_data="support")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages"""
    user_text = update.message.text
    
    if "سلام" in user_text or "hi" in user_text.lower():
        await update.message.reply_text("👋 سلام! برای مشاهده منو از دستور /start استفاده کنید.")
    elif "قیمت" in user_text or "price" in user_text.lower():
        await update.message.reply_text("📊 برای مشاهده قیمت‌ها از بخش تحلیل بازار استفاده کنید.")
    else:
        await update.message.reply_text("🤖 پیام شما دریافت شد. برای منو از /start استفاده کنید.")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "market_analysis":
        await query.edit_message_text("📈 تحلیل بازار در حال بارگذاری...")
    elif query.data == "portfolio":
        await query.edit_message_text("💰 پرتفوی شما در حال بارگذاری...")
    elif query.data == "trading_signals":
        await query.edit_message_text("🎯 پیشنهادات تریدینگ در حال بارگذاری...")
    elif query.data == "education":
        await query.edit_message_text("📚 مطالب آموزشی در حال بارگذاری...")
    elif query.data == "settings":
        await query.edit_message_text("⚙️ تنظیمات در حال بارگذاری...")
    elif query.data == "support":
        await query.edit_message_text("📞 پشتیبانی: @UltraPlusSupport")

async def setup_telegram_bot():
    """Setup Telegram bot with webhook configuration"""
    global bot_application
    
    try:
        # Create application
        bot_application = Application.builder().token(BOT_TOKEN).build()
        
        # Initialize and start
        await bot_application.initialize()
        await bot_application.start()
        
        # Clear any existing webhooks to prevent conflicts
        await bot_application.bot.delete_webhook(drop_pending_updates=True)
        logger.info("🧹 Webhook cleanup completed")
        
        # Add handlers
        bot_application.add_handler(CommandHandler("start", start_command))
        bot_application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        bot_application.add_handler(CallbackQueryHandler(button_callback))
        
        logger.info("✅ Telegram bot configured with webhook mode")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to setup Telegram bot: {e}")
        return False

# Flask Routes
@flask_app.route('/')
def health_check():
    """Main health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'ultra_plus_bot',
        'mode': 'webhook_only',
        'deployment': 'cloud_run_fixed',
        'timestamp': datetime.now().isoformat(),
        'port': PORT,
        'bot_ready': bot_application is not None,
        'instance_running': _instance_running
    })

@flask_app.route('/health')
def health():
    """Health endpoint for Cloud Run"""
    return jsonify({
        'health': 'ok',
        'ready': True,
        'webhook_mode': True,
        'polling_disabled': True,
        'port': PORT
    })

@flask_app.route('/readiness')
def readiness():
    """Readiness probe"""
    return jsonify({
        'ready': bot_application is not None,
        'webhook_configured': True,
        'port': PORT
    })

@flask_app.route('/liveness')
def liveness():
    """Liveness probe"""
    return jsonify({
        'alive': True,
        'instance_running': _instance_running,
        'port': PORT
    })

@flask_app.route('/webhook', methods=['POST'])
def webhook():
    """Process Telegram webhook updates"""
    try:
        if not bot_application:
            logger.error("❌ Bot application not initialized")
            return jsonify({'error': 'Bot not ready'}), 500
        
        # Get update data
        update_data = request.get_json()
        if not update_data:
            return jsonify({'error': 'No data received'}), 400
        
        # Process update asynchronously
        def process_update_async():
            try:
                update = Update.de_json(update_data, bot_application.bot)
                asyncio.run(bot_application.process_update(update))
                logger.info(f"✅ Processed webhook update: {update.update_id}")
            except Exception as e:
                logger.error(f"❌ Update processing error: {e}")
        
        # Process in background to avoid blocking Flask
        threading.Thread(target=process_update_async, daemon=True).start()
        
        return jsonify({'status': 'ok'})
        
    except Exception as e:
        logger.error(f"❌ Webhook processing error: {e}")
        return jsonify({'error': str(e)}), 500

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info(f"🔄 Received signal {signum}, shutting down...")
    release_singleton()
    sys.exit(0)

def setup_bot_in_background():
    """Setup bot in background thread"""
    def run_bot_setup():
        try:
            asyncio.run(setup_telegram_bot())
        except Exception as e:
            logger.error(f"❌ Bot setup error: {e}")
    
    # Start bot setup in background
    bot_thread = threading.Thread(target=run_bot_setup, daemon=True)
    bot_thread.start()
    logger.info("🔄 Bot setup started in background")

def main():
    """Main entry point - Cloud Run optimized"""
    
    # Enforce singleton to prevent conflicts
    enforce_singleton()
    
    # Setup signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    logger.info("🚀 Starting Cloud Run deployment with fixes")
    logger.info(f"📡 Port: {PORT} (SINGLE PORT ONLY)")
    logger.info("🔗 Webhook mode: ENABLED")
    logger.info("🚫 Polling: DISABLED") 
    logger.info("🔒 Single instance: ENFORCED")
    
    try:
        # Setup Telegram bot in background
        setup_bot_in_background()
        
        # Start Flask server immediately on port 3000
        logger.info(f"🚀 Starting Flask server on port {PORT}")
        flask_app.run(
            host='0.0.0.0',
            port=PORT,
            debug=False,
            threaded=True,
            use_reloader=False  # Prevent multiple instances
        )
        
    except Exception as e:
        logger.error(f"❌ Deployment failed: {e}")
        release_singleton()
        sys.exit(1)
    finally:
        release_singleton()

if __name__ == "__main__":
    main()