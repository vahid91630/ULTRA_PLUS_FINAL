#!/usr/bin/env python3
"""
🤖 Telegram Integration for Daily Learning Engine
Commands and scheduling integration with existing Telegram bot
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from daily_learning_engine import DailyLearningEngine

logger = logging.getLogger(__name__)

class TelegramLearningIntegration:
    """
    Integration layer between Telegram bot and Daily Learning Engine
    """
    
    def __init__(self, learning_engine: DailyLearningEngine):
        self.learning_engine = learning_engine
        self.is_initialized = False
    
    async def initialize(self):
        """Initialize the learning engine"""
        if not self.is_initialized:
            await self.learning_engine.initialize()
            self.is_initialized = True
    
    async def handle_update_knowledge_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /update_knowledge command"""
        await self.initialize()
        
        message = await update.message.reply_text(
            "🎓 شروع چرخه یادگیری روزانه...\nلطفاً منتظر بمانید..."
        )
        
        try:
            # Run learning cycle
            result = await self.learning_engine.run_daily_learning_cycle()
            
            # Format result for Telegram
            if result.get('error'):
                response = f"❌ خطا در یادگیری: {result['error']}"
            else:
                insights_count = result.get('insights_learned', 0)
                duration = result.get('duration_seconds', 0)
                
                response = f"""
✅ **چرخه یادگیری تکمیل شد**

📊 **آمار یادگیری:**
• بینش‌های جدید: {insights_count}
• مدت زمان: {duration:.1f} ثانیه
• وضعیت: {result.get('status', 'نامشخص')}

📈 **تحلیل بر اساس نوع:**
"""
                
                insights_by_type = result.get('insights_by_type', {})
                for insight_type, count in insights_by_type.items():
                    type_name = {
                        'news': 'اخبار',
                        'education': 'آموزش',
                        'strategy': 'استراتژی'
                    }.get(insight_type, insight_type)
                    response += f"• {type_name}: {count}\n"
                
                top_tags = result.get('top_tags', [])
                if top_tags:
                    response += f"\n🏷️ **موضوعات پرتکرار:** {', '.join(top_tags[:5])}"
            
            await message.edit_text(response, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Learning command error: {e}")
            await message.edit_text(f"❌ خطا در اجرای یادگیری: {str(e)}")
    
    async def handle_learning_status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /learning_status command"""
        await self.initialize()
        
        try:
            stats = await self.learning_engine.get_learning_statistics()
            
            if stats.get('error'):
                response = f"❌ خطا در دریافت آمار: {stats['error']}"
            else:
                response = f"""
📚 **وضعیت سیستم یادگیری**

📊 **آمار کلی:**
• مجموع بینش‌ها: {stats.get('total_insights', 0):,}
• بینش‌های هفته گذشته: {stats.get('recent_7_days', 0)}
• میانگین مرتبط بودن: {stats.get('average_relevance', 0):.2f}
• میانگین احساسات: {stats.get('average_sentiment', 0):+.2f}

📈 **تحلیل بر اساس نوع:**
"""
                
                insights_by_type = stats.get('insights_by_type', {})
                for insight_type, count in insights_by_type.items():
                    type_name = {
                        'news': 'اخبار',
                        'education': 'آموزش',
                        'strategy': 'استراتژی'
                    }.get(insight_type, insight_type)
                    response += f"• {type_name}: {count:,}\n"
                
                top_tags = stats.get('top_tags', [])[:5]
                if top_tags:
                    response += f"\n🏷️ **موضوعات پربحث:** {', '.join(top_tags)}"
                
                response += f"\n\n⏰ **آخرین بروزرسانی:** {datetime.now().strftime('%H:%M:%S')}"
            
            await update.message.reply_text(response, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Learning status error: {e}")
            await update.message.reply_text(f"❌ خطا در دریافت وضعیت: {str(e)}")
    
    async def handle_search_insights_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /search_insights command with arguments"""
        await self.initialize()
        
        # Get search query from command arguments
        args = context.args
        if not args:
            await update.message.reply_text(
                "🔍 **جستجو در بینش‌ها**\n\n"
                "استفاده: `/search_insights کلمه_جستجو`\n"
                "مثال: `/search_insights bitcoin` یا `/search_insights RSI`",
                parse_mode='Markdown'
            )
            return
        
        query = ' '.join(args)
        
        try:
            insights = await self.learning_engine.search_insights(query, limit=5)
            
            if not insights:
                response = f"🔍 هیچ بینشی برای '{query}' یافت نشد."
            else:
                response = f"🔍 **نتایج جستجو برای '{query}':**\n\n"
                
                for i, insight in enumerate(insights, 1):
                    source = insight.get('source', 'نامشخص')
                    summary = insight.get('summary', insight.get('content', ''))[:100]
                    relevance = insight.get('relevance_score', 0)
                    tags = insight.get('tags', [])[:3]
                    
                    response += f"**{i}. {source}** (مرتبط: {relevance:.1f})\n"
                    response += f"{summary}...\n"
                    if tags:
                        response += f"🏷️ {', '.join(tags)}\n"
                    response += "\n"
            
            await update.message.reply_text(response, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Search insights error: {e}")
            await update.message.reply_text(f"❌ خطا در جستجو: {str(e)}")
    
    async def handle_recent_insights_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /recent_insights command"""
        await self.initialize()
        
        # Create inline keyboard for insight types
        keyboard = [
            [
                InlineKeyboardButton("📰 اخبار", callback_data="recent_news"),
                InlineKeyboardButton("📚 آموزش", callback_data="recent_education")
            ],
            [
                InlineKeyboardButton("📈 استراتژی", callback_data="recent_strategy"),
                InlineKeyboardButton("🔄 همه", callback_data="recent_all")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "📖 **بینش‌های اخیر**\n\nنوع بینش مورد نظر را انتخاب کنید:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def handle_recent_insights_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle recent insights callback queries"""
        await self.initialize()
        
        query = update.callback_query
        await query.answer()
        
        callback_data = query.data
        insight_type_map = {
            'recent_news': 'news',
            'recent_education': 'education', 
            'recent_strategy': 'strategy',
            'recent_all': None
        }
        
        insight_type = insight_type_map.get(callback_data)
        
        try:
            insights = await self.learning_engine.get_recent_insights(
                hours=24, 
                insight_type=insight_type, 
                limit=5
            )
            
            if not insights:
                response = "📖 بینش جدیدی در ۲۴ ساعت گذشته یافت نشد."
            else:
                type_names = {
                    'news': 'اخبار',
                    'education': 'آموزش',
                    'strategy': 'استراتژی'
                }
                
                type_name = type_names.get(insight_type, 'همه موارد')
                response = f"📖 **بینش‌های اخیر - {type_name}:**\n\n"
                
                for i, insight in enumerate(insights, 1):
                    source = insight.get('source', 'نامشخص')
                    summary = insight.get('summary', insight.get('content', ''))[:100]
                    relevance = insight.get('relevance_score', 0)
                    sentiment = insight.get('sentiment_score', 0)
                    risk = insight.get('risk_level', 'LOW')
                    
                    risk_emoji = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}.get(risk, '⚪')
                    sentiment_emoji = '📈' if sentiment > 0 else '📉' if sentiment < 0 else '➡️'
                    
                    response += f"**{i}. {source}** {risk_emoji}\n"
                    response += f"{summary}...\n"
                    response += f"{sentiment_emoji} احساسات: {sentiment:+.2f} | مرتبط: {relevance:.1f}\n\n"
            
            await query.edit_message_text(response, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Recent insights callback error: {e}")
            await query.edit_message_text(f"❌ خطا در دریافت بینش‌ها: {str(e)}")
    
    async def handle_learning_menu_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle learning menu from main bot menu"""
        await self.initialize()
        
        query = update.callback_query
        await query.answer()
        
        # Create learning submenu
        keyboard = [
            [InlineKeyboardButton("🎓 شروع یادگیری", callback_data="start_learning")],
            [InlineKeyboardButton("📊 وضعیت یادگیری", callback_data="learning_stats")],
            [InlineKeyboardButton("📖 بینش‌های اخیر", callback_data="recent_insights_menu")],
            [InlineKeyboardButton("🔍 جستجو در دانش", callback_data="search_knowledge")],
            [InlineKeyboardButton("🔙 بازگشت به منو", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🧠 **سیستم یادگیری ULTRA_PLUS_BOT**\n\n"
            "سیستم یادگیری خودکار از منابع معتبر مالی:\n"
            "• تحلیل اخبار بازارهای مالی\n"
            "• استخراج استراتژی‌های معاملاتی\n"
            "• جمع‌آوری محتوای آموزشی\n\n"
            "گزینه مورد نظر را انتخاب کنید:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    def get_learning_commands(self) -> List[Dict[str, str]]:
        """Get list of learning-related commands"""
        return [
            {
                'command': 'update_knowledge',
                'description': 'شروع چرخه یادگیری روزانه'
            },
            {
                'command': 'learning_status', 
                'description': 'نمایش وضعیت سیستم یادگیری'
            },
            {
                'command': 'search_insights',
                'description': 'جستجو در بینش‌های یادگیری شده'
            },
            {
                'command': 'recent_insights',
                'description': 'نمایش بینش‌های اخیر'
            }
        ]
    
    async def schedule_automatic_learning(self):
        """Schedule automatic learning cycles"""
        """Schedule automatic learning - runs in background"""
        learning_times = ["06:00", "12:00", "18:00", "23:00"]
        
        while True:
            try:
                current_time = datetime.now().strftime("%H:%M")
                
                if current_time in learning_times:
                    logger.info(f"🎓 Starting scheduled learning cycle at {current_time}")
                    await self.learning_engine.run_daily_learning_cycle()
                    
                    # Wait 61 seconds to avoid duplicate runs
                    await asyncio.sleep(61)
                else:
                    # Check every minute
                    await asyncio.sleep(60)
                    
            except Exception as e:
                logger.error(f"Scheduled learning error: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error

# Integration function for existing bot
def integrate_learning_with_bot(application, learning_engine: DailyLearningEngine):
    """
    Integrate learning commands with existing Telegram bot
    """
    from telegram.ext import CommandHandler, CallbackQueryHandler
    
    integration = TelegramLearningIntegration(learning_engine)
    
    # Add command handlers
    application.add_handler(CommandHandler("update_knowledge", integration.handle_update_knowledge_command))
    application.add_handler(CommandHandler("learning_status", integration.handle_learning_status_command))
    application.add_handler(CommandHandler("search_insights", integration.handle_search_insights_command))
    application.add_handler(CommandHandler("recent_insights", integration.handle_recent_insights_command))
    
    # Add callback handlers for inline keyboards
    application.add_handler(CallbackQueryHandler(
        integration.handle_recent_insights_callback, 
        pattern="^recent_(news|education|strategy|all)$"
    ))
    
    application.add_handler(CallbackQueryHandler(
        integration.handle_learning_menu_callback,
        pattern="^learning_menu$"
    ))
    
    # Start automatic learning scheduler
    asyncio.create_task(integration.schedule_automatic_learning())
    
    return integration