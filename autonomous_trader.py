#!/usr/bin/env python3
"""
Autonomous Trader - معاملات خودکار با قدرت خرید و فروش واقعی
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List
import random

from real_trading_engine import trading_engine, execute_ai_trading_decision

logger = logging.getLogger(__name__)

class AutonomousTrader:
    """سیستم معاملات خودکار با تصمیم‌گیری مستقل"""
    
    def __init__(self):
        self.active = False
        self.trading_session = None
        self.last_trade_time = None
        self.session_profits = 0
        self.trade_count = 0
        
    async def start_autonomous_trading(self, user_id: int) -> Dict:
        """شروع معاملات خودکار"""
        try:
            if not trading_engine.active:
                return {"success": False, "error": "Trading engine not initialized"}
                
            self.active = True
            self.trading_session = {
                'start_time': datetime.now(),
                'user_id': user_id,
                'initial_balance': 0,
                'trades': []
            }
            
            # Start trading loop
            asyncio.create_task(self._trading_loop())
            
            logger.info(f"🚀 Autonomous trading started for user {user_id}")
            return {
                "success": True,
                "message": "Autonomous trading activated",
                "session_id": id(self.trading_session)
            }
            
        except Exception as e:
            logger.error(f"Failed to start autonomous trading: {e}")
            return {"success": False, "error": str(e)}
    
    async def _trading_loop(self):
        """حلقه اصلی معاملات خودکار"""
        while self.active:
            try:
                # Wait 1-5 minutes between analyses
                wait_time = random.randint(60, 300)
                await asyncio.sleep(wait_time)
                
                if not self.active:
                    break
                    
                # Analyze market and make trading decisions
                await self._analyze_and_trade()
                
            except Exception as e:
                logger.error(f"Trading loop error: {e}")
                await asyncio.sleep(60)  # Wait before retrying
    
    async def _analyze_and_trade(self):
        """تحلیل بازار و اجرای معاملات"""
        try:
            # Get trading opportunities
            opportunities = await trading_engine.get_trading_opportunities()
            
            if not opportunities:
                logger.info("📊 No trading opportunities found")
                return
            
            # Filter high-confidence opportunities
            high_confidence_ops = [op for op in opportunities if op.get('confidence', 0) >= 0.75]
            
            if not high_confidence_ops:
                logger.info("📊 No high-confidence opportunities found")
                return
            
            # Select best opportunity
            best_opportunity = max(high_confidence_ops, key=lambda x: x.get('confidence', 0))
            
            # Calculate trade amount based on confidence and risk
            base_amount = 100  # Base $100
            confidence_multiplier = best_opportunity.get('confidence', 0.5)
            trade_amount = base_amount * (0.5 + confidence_multiplier)
            
            # Execute the trade
            logger.info(f"🎯 Executing opportunity: {best_opportunity['symbol']} {best_opportunity['action']} (confidence: {confidence_multiplier:.1%})")
            
            result = await trading_engine.execute_opportunity(best_opportunity, trade_amount)
            
            if result.get('success'):
                self.trade_count += 1
                self.last_trade_time = datetime.now()
                
                trade_record = {
                    'timestamp': self.last_trade_time,
                    'symbol': best_opportunity['symbol'],
                    'action': best_opportunity['action'],
                    'amount': trade_amount,
                    'confidence': confidence_multiplier,
                    'result': result
                }
                
                if self.trading_session:
                    self.trading_session['trades'].append(trade_record)
                
                logger.info(f"✅ Trade executed: {best_opportunity['symbol']} ${trade_amount:.2f}")
                
                # Send notification to user (if needed)
                await self._notify_trade_executed(trade_record)
                
            else:
                logger.warning(f"❌ Trade failed: {result.get('error')}")
                
        except Exception as e:
            logger.error(f"Analysis and trading error: {e}")
    
    async def _notify_trade_executed(self, trade_record: Dict):
        """اطلاع‌رسانی اجرای معامله به کاربر"""
        try:
            # This would send notification via telegram bot
            notification = f"""
🚨 **معامله خودکار انجام شد!**

📊 **جزئیات:**
💰 نماد: {trade_record['symbol']}
⚡ عمل: {trade_record['action'].upper()}
💵 مبلغ: ${trade_record['amount']:.2f}
🎯 اطمینان: {trade_record['confidence']:.1%}
⏰ زمان: {trade_record['timestamp'].strftime('%H:%M:%S')}

📈 **نتیجه:** ✅ موفق
            """
            
            logger.info(f"📢 Trade notification: {trade_record['symbol']}")
            
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
    
    async def stop_autonomous_trading(self) -> Dict:
        """توقف معاملات خودکار"""
        try:
            self.active = False
            
            if self.trading_session:
                session_duration = datetime.now() - self.trading_session['start_time']
                total_trades = len(self.trading_session.get('trades', []))
                
                summary = {
                    'session_duration': str(session_duration),
                    'total_trades': total_trades,
                    'last_trade': self.last_trade_time.isoformat() if self.last_trade_time else None
                }
                
                logger.info(f"🛑 Autonomous trading stopped. Duration: {session_duration}, Trades: {total_trades}")
                
                return {
                    "success": True,
                    "message": "Autonomous trading stopped",
                    "summary": summary
                }
            
            return {"success": True, "message": "Autonomous trading stopped"}
            
        except Exception as e:
            logger.error(f"Failed to stop autonomous trading: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_trading_status(self) -> Dict:
        """دریافت وضعیت معاملات"""
        try:
            if not self.active:
                return {
                    "active": False,
                    "message": "Autonomous trading is not active"
                }
            
            current_time = datetime.now()
            session_duration = current_time - self.trading_session['start_time'] if self.trading_session else timedelta(0)
            
            status = {
                "active": True,
                "session_duration": str(session_duration),
                "total_trades": self.trade_count,
                "last_trade": self.last_trade_time.isoformat() if self.last_trade_time else None,
                "session_profits": self.session_profits,
                "trading_engine_active": trading_engine.active,
                "connected_exchanges": len(trading_engine.exchanges)
            }
            
            return status
            
        except Exception as e:
            logger.error(f"Failed to get trading status: {e}")
            return {"error": str(e)}

# Global autonomous trader instance
autonomous_trader = AutonomousTrader()

async def start_real_autonomous_trading(user_id: int) -> Dict:
    """شروع معاملات خودکار واقعی"""
    return await autonomous_trader.start_autonomous_trading(user_id)

async def stop_real_autonomous_trading() -> Dict:
    """توقف معاملات خودکار واقعی"""
    return await autonomous_trader.stop_autonomous_trading()

async def get_autonomous_trading_status() -> Dict:
    """وضعیت معاملات خودکار"""
    return await autonomous_trader.get_trading_status()