#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تست ساده ربات تلگرام
"""

import os
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class SimpleTelegramBot:
    def __init__(self):
        self.token = os.getenv('ULTRA_Plus_Bot')
        if not self.token:
            raise ValueError("❌ ULTRA_Plus_Bot token not found")
        
        logger.info(f"✅ Bot token loaded: {self.token[:10]}...")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command handler"""
        user = update.effective_user
        await update.message.reply_text(
            f"🤖 سلام {user.first_name}!\n"
            f"✅ ربات تلگرام فعال است\n"
            f"🕐 زمان: {update.message.date}\n"
            f"📱 شما: @{user.username}\n\n"
            f"دستورات:\n"
            f"/start - شروع\n"
            f"/test - تست\n"
            f"/status - وضعیت"
        )
        logger.info(f"✅ Start command از {user.username}")
    
    async def test_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Test command"""
        await update.message.reply_text(
            "✅ تست موفق!\n"
            "🤖 ربات به درستی کار می‌کند\n"
            "📡 اتصال به Telegram API فعال\n"
            "💬 پردازش پیام‌ها OK"
        )
        logger.info("✅ Test command executed")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Status command"""
        await update.message.reply_text(
            "📊 وضعیت سیستم:\n"
            "✅ ربات تلگرام: فعال\n"
            "✅ پردازش پیام: فعال\n"
            "✅ اتصال API: فعال\n"
            "🕐 آخرین بررسی: الان\n"
            "📱 شماره ربات: @ULTRA_PLUS_BOT"
        )
        logger.info("✅ Status command executed")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages"""
        user = update.effective_user
        message_text = update.message.text
        
        await update.message.reply_text(
            f"👤 سلام {user.first_name}\n"
            f"💬 پیام شما: {message_text}\n"
            f"✅ ربات فعال است و پیام شما را دریافت کرد\n\n"
            f"برای دستورات /start تایپ کنید"
        )
        logger.info(f"✅ Message from {user.username}: {message_text}")
    
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Error handler"""
        logger.error(f"❌ خطا در ربات: {context.error}")
        
        if update and hasattr(update, 'message') and update.message:
            try:
                await update.message.reply_text(
                    "❌ خطا در پردازش پیام\n"
                    "🔧 سیستم تعمیرگاهی فعال شد\n"
                    "⏳ لطفاً دوباره تلاش کنید"
                )
            except:
                pass
    
    def run(self):
        """Run the bot"""
        logger.info("🚀 شروع ربات تلگرام ساده...")
        
        # Create application
        app = Application.builder().token(self.token).build()
        
        # Add handlers
        app.add_handler(CommandHandler("start", self.start_command))
        app.add_handler(CommandHandler("test", self.test_command))
        app.add_handler(CommandHandler("status", self.status_command))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Add error handler
        app.add_error_handler(self.error_handler)
        
        logger.info("✅ Handlers اضافه شدند")
        logger.info("🔗 ربات آماده دریافت پیام: @ULTRA_PLUS_BOT")
        
        # Start the bot
        try:
            app.run_polling(drop_pending_updates=True)
        except KeyboardInterrupt:
            logger.info("🛑 ربات متوقف شد")
        except Exception as e:
            logger.error(f"❌ خطا در اجرای ربات: {e}")

def main():
    try:
        bot = SimpleTelegramBot()
        bot.run()
    except Exception as e:
        logger.error(f"❌ خطا در راه‌اندازی: {e}")

if __name__ == "__main__":
    main()