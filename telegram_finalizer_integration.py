#!/usr/bin/env python3
"""
📱 Telegram Integration for Daily Data Finalizer
Lightweight integration for /finalize_day command
"""

import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from daily_data_finalizer import DailyDataFinalizer

logger = logging.getLogger(__name__)

class TelegramFinalizerIntegration:
    """
    Lightweight Telegram integration for daily data finalization
    """
    
    def __init__(self, mongodb_uri: str = None):
        self.finalizer = DailyDataFinalizer(mongodb_uri)
        logger.info("📱 Telegram Finalizer Integration initialized")
    
    async def handle_finalize_day_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /finalize_day command"""
        # Show confirmation first
        keyboard = [
            [InlineKeyboardButton("✅ تأیید و اجرا", callback_data="confirm_finalize")],
            [InlineKeyboardButton("❌ لغو", callback_data="cancel_finalize")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🧠 **پردازش و ذخیره داده‌های روزانه**\n\n"
            "این عملیات موارد زیر را انجام می‌دهد:\n"
            "• خواندن داده‌های جمع‌آوری شده از daily_data.json\n"
            "• امتیازدهی بر اساس تازگی، منبع و برچسب‌ها\n"
            "• نگهداری فقط ورودی‌های با امتیاز ≥60\n"
            "• ذخیره در MongoDB و پاکسازی فایل‌های محلی\n\n"
            "ادامه می‌دهید؟",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def handle_finalize_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle finalization confirmation callback"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "cancel_finalize":
            await query.edit_message_text("❌ عملیات لغو شد.")
            return
        
        if query.data == "confirm_finalize":
            # Start processing
            await query.edit_message_text("🧠 در حال پردازش داده‌های روزانه... لطفاً صبر کنید...")
            
            try:
                # Run finalization
                results = self.finalizer.finalize_daily_data()
                
                # Format results
                response = self._format_finalization_results(results)
                
                # Create stats keyboard
                keyboard = [
                    [InlineKeyboardButton("📊 آمار کلی", callback_data="show_stats")],
                    [InlineKeyboardButton("🔙 منوی اصلی", callback_data="main_menu")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(
                    response, 
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
                
            except Exception as e:
                logger.error(f"Finalization error: {e}")
                await query.edit_message_text(f"❌ خطای غیرمنتظره: {str(e)}")
    
    def _format_finalization_results(self, results: dict) -> str:
        """Format finalization results for Telegram"""
        if results['success']:
            response = f"""
✅ **پردازش روزانه تکمیل شد**

📊 **نتایج پردازش:**
• مجموع ورودی‌ها: {results['total_entries']:,}
• ورودی‌های واجد شرایط: {results['qualified_entries']:,}
• ذخیره شده در MongoDB: {results['stored_entries']:,}

🎯 **سیستم امتیازدهی:**
• تازگی محتوا (<48 ساعت): +20 امتیاز
• منبع معتبر: +30 امتیاز
• برچسب‌های مرتبط: +10 امتیاز هر تگ
• حداقل امتیاز برای ذخیره: 60

💾 **وضعیت ذخیره‌سازی:**
✅ داده‌ها در MongoDB ذخیره شدند
✅ فایل‌های محلی پاکسازی شدند
✅ بک‌آپ امنیتی ایجاد شد
            """.strip()
        else:
            errors = '\n'.join(f"• {error}" for error in results.get('errors', []))
            response = f"""
❌ **خطا در پردازش روزانه**

📊 **آمار پردازش:**
• مجموع ورودی‌ها: {results['total_entries']:,}
• ورودی‌های واجد شرایط: {results['qualified_entries']:,}

🚨 **مشکلات شناسایی شده:**
{errors}

💡 **پیشنهاد:** بررسی اتصال MongoDB و وجود فایل daily_data.json
            """.strip()
        
        return response
    
    async def handle_show_stats_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle show statistics callback"""
        query = update.callback_query
        await query.answer()
        
        # Get statistics
        stats = self.finalizer.get_statistics()
        
        if 'error' in stats:
            response = f"❌ خطا در دریافت آمار: {stats['error']}"
        else:
            top_sources = '\n'.join(f"• {item['source']}: {item['count']}" for item in stats['top_sources'][:5])
            
            response = f"""
📊 **آمار کلی سیستم یادگیری**

💾 **وضعیت پایگاه داده:**
• مجموع بینش‌های ذخیره شده: {stats['total_insights']:,}
• بینش‌های امروز: {stats['today_insights']:,}
• میانگین امتیاز: {stats['average_score']}/100

📈 **منابع برتر:**
{top_sources}

⏰ **آخرین بروزرسانی:** {stats['last_updated'][:19].replace('T', ' ')}
            """.strip()
        
        keyboard = [
            [InlineKeyboardButton("🔄 بروزرسانی آمار", callback_data="show_stats")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="finalize_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            response,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def handle_manual_finalize_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /manual_finalize command for testing"""
        await update.message.reply_text("🧠 اجرای پردازش دستی...")
        
        try:
            results = self.finalizer.finalize_daily_data()
            response = self._format_finalization_results(results)
            
            await update.message.reply_text(response, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"❌ خطا در پردازش: {str(e)}")
    
    async def handle_data_status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /data_status command"""
        try:
            # Check local data
            import os
            local_data_exists = os.path.exists('daily_data.json')
            
            # Get MongoDB stats
            stats = self.finalizer.get_statistics()
            
            response = f"""
📋 **وضعیت سیستم داده‌ها**

📁 **داده‌های محلی:**
{"✅ فایل daily_data.json موجود است" if local_data_exists else "❌ فایل daily_data.json یافت نشد"}

💾 **پایگاه داده MongoDB:**
{"✅ متصل" if 'error' not in stats else f"❌ خطا: {stats.get('error', 'نامشخص')}"}

📊 **آمار کلی:**
• مجموع بینش‌ها: {stats.get('total_insights', 0):,}
• بینش‌های امروز: {stats.get('today_insights', 0):,}
• میانگین امتیاز: {stats.get('average_score', 0)}
            """.strip()
            
            await update.message.reply_text(response, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"❌ خطا در دریافت وضعیت: {str(e)}")

def add_finalizer_commands(application, mongodb_uri: str = None):
    """Add finalizer commands to existing Telegram application"""
    integration = TelegramFinalizerIntegration(mongodb_uri)
    
    # Add command handlers
    application.add_handler(CommandHandler("finalize_day", integration.handle_finalize_day_command))
    application.add_handler(CommandHandler("manual_finalize", integration.handle_manual_finalize_command))
    application.add_handler(CommandHandler("data_status", integration.handle_data_status_command))
    
    # Add callback handlers
    application.add_handler(CallbackQueryHandler(
        integration.handle_finalize_callback,
        pattern="^(confirm_finalize|cancel_finalize)$"
    ))
    
    application.add_handler(CallbackQueryHandler(
        integration.handle_show_stats_callback,
        pattern="^show_stats$"
    ))
    
    logger.info("📱 Finalizer commands added to Telegram application")
    return integration

# Standalone testing
async def test_integration():
    """Test the integration components"""
    integration = TelegramFinalizerIntegration()
    
    print("🧪 Testing finalization process...")
    results = integration.finalizer.finalize_daily_data()
    
    print("\n📊 Results:")
    response = integration._format_finalization_results(results)
    print(response)
    
    print("\n📈 Statistics:")
    stats = integration.finalizer.get_statistics()
    if 'error' not in stats:
        print(f"Total insights: {stats['total_insights']}")
        print(f"Today's insights: {stats['today_insights']}")
        print(f"Average score: {stats['average_score']}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(test_integration())