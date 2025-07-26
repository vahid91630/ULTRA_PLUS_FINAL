#!/usr/bin/env python3
"""
مدیریت ریسک پیشرفته برای ULTRA_PLUS_BOT
پیاده‌سازی استراتژی‌های Kelly Criterion و Dynamic Stop Loss
"""

import math
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class AdvancedRiskManager:
    def __init__(self):
        """مدیر ریسک پیشرفته با قابلیت‌های هوشمند"""
        self.risk_settings = {
            'max_portfolio_risk': 0.02,      # حداکثر 2% کل پورتفولیو در هر معامله
            'max_concurrent_trades': 15,      # افزایش از 5 به 15
            'dynamic_stop_loss': True,        # Stop loss پویا
            'kelly_position_sizing': True,    # اندازه پوزیشن بر اساس Kelly
            'correlation_check': True,        # بررسی همبستگی دارایی‌ها
            'volatility_adjustment': True     # تنظیم بر اساس نوسانات
        }
        
        self.trade_history = []
        self.correlation_matrix = {}
        self.volatility_cache = {}
        
        logger.info("🛡️ Advanced Risk Manager initialized")
    
    def calculate_optimal_position_size(self, 
                                      win_probability: float,
                                      avg_win: float,
                                      avg_loss: float,
                                      account_balance: float) -> float:
        """محاسبه اندازه بهینه پوزیشن با Kelly Criterion"""
        try:
            # Kelly Criterion: f = (bp - q) / b
            # f = fraction of capital to wager
            # b = odds received (avg_win / avg_loss)
            # p = probability of winning
            # q = probability of losing (1 - p)
            
            if avg_loss <= 0 or win_probability <= 0 or win_probability >= 1:
                return 0.01  # حداقل 1% در صورت داده‌های نامعتبر
            
            b = avg_win / avg_loss  # نسبت سود به ضرر
            p = win_probability
            q = 1 - p
            
            kelly_fraction = (b * p - q) / b
            
            # محدود کردن Kelly fraction به حداکثر 5% برای امنیت
            kelly_fraction = max(0.001, min(kelly_fraction, 0.05))
            
            # تنظیم بر اساس تنظیمات ریسک
            adjusted_fraction = kelly_fraction * self.risk_settings['max_portfolio_risk'] / 0.02
            
            position_size = account_balance * adjusted_fraction
            
            logger.info(f"📊 Kelly position size: {position_size:.2f} (fraction: {kelly_fraction:.3f})")
            return position_size
            
        except Exception as e:
            logger.error(f"❌ خطا در محاسبه Kelly: {e}")
            return account_balance * 0.01  # fallback به 1%
    
    def calculate_dynamic_stop_loss(self, 
                                  asset: str,
                                  entry_price: float,
                                  volatility: float,
                                  timeframe: str = "1h") -> float:
        """محاسبه stop loss پویا بر اساس نوسانات"""
        try:
            # پایه stop loss بر اساس نوع دارایی
            base_stop_loss = {
                'crypto': 0.015,    # 1.5%
                'forex': 0.008,     # 0.8%
                'stock': 0.012,     # 1.2%
                'commodity': 0.02   # 2%
            }
            
            # تشخیص نوع دارایی
            asset_type = self.detect_asset_type(asset)
            base_sl = base_stop_loss.get(asset_type, 0.015)
            
            # تنظیم بر اساس نوسانات
            volatility_multiplier = max(0.5, min(volatility / 0.02, 3.0))  # 0.5x تا 3x
            
            # تنظیم بر اساس timeframe
            timeframe_multipliers = {
                '1m': 0.3, '5m': 0.5, '15m': 0.7, '30m': 0.8,
                '1h': 1.0, '4h': 1.5, '1d': 2.0
            }
            
            timeframe_mult = timeframe_multipliers.get(timeframe, 1.0)
            
            # محاسبه نهایی
            dynamic_sl = base_sl * volatility_multiplier * timeframe_mult
            
            # محدود کردن بین 0.3% تا 5%
            dynamic_sl = max(0.003, min(dynamic_sl, 0.05))
            
            stop_loss_price = entry_price * (1 - dynamic_sl)
            
            logger.info(f"🎯 Dynamic stop loss for {asset}: {dynamic_sl*100:.2f}% at ${stop_loss_price:.4f}")
            return dynamic_sl
            
        except Exception as e:
            logger.error(f"❌ خطا در محاسبه stop loss: {e}")
            return 0.015  # fallback
    
    def detect_asset_type(self, asset: str) -> str:
        """تشخیص نوع دارایی"""
        asset = asset.upper()
        
        if any(crypto in asset for crypto in ['BTC', 'ETH', 'BNB', 'ADA', 'SOL', 'DOGE']):
            return 'crypto'
        elif '/' in asset and len(asset) == 7:  # مثل EUR/USD
            return 'forex'
        elif asset in ['AAPL', 'TSLA', 'AMZN', 'GOOGL', 'MSFT', 'NVDA']:
            return 'stock'
        elif asset in ['GOLD', 'OIL', 'SILVER']:
            return 'commodity'
        else:
            return 'crypto'  # default
    
    def check_portfolio_correlation(self, 
                                  new_asset: str,
                                  current_positions: List[Dict]) -> bool:
        """بررسی همبستگی با پوزیشن‌های فعلی"""
        try:
            if not self.risk_settings['correlation_check']:
                return True
            
            # اگر پوزیشن کمتر از 3 داریم، مجاز است
            if len(current_positions) < 3:
                return True
            
            # بررسی همبستگی با دارایی‌های موجود
            high_correlation_count = 0
            
            for position in current_positions:
                correlation = self.get_asset_correlation(new_asset, position['asset'])
                
                if correlation > 0.7:  # همبستگی بالا
                    high_correlation_count += 1
            
            # اجازه حداکثر 2 دارایی با همبستگی بالا
            if high_correlation_count >= 2:
                logger.warning(f"⚠️ پوزیشن {new_asset} رد شد: همبستگی بالا با {high_correlation_count} دارایی")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ خطا در بررسی همبستگی: {e}")
            return True  # در صورت خطا، اجازه می‌دهیم
    
    def get_asset_correlation(self, asset1: str, asset2: str) -> float:
        """دریافت همبستگی بین دو دارایی"""
        # شبیه‌سازی ماتریس همبستگی (در پیاده‌سازی واقعی از داده‌های تاریخی استفاده کنید)
        correlation_map = {
            ('BTC', 'ETH'): 0.85,
            ('EUR/USD', 'GBP/USD'): 0.72,
            ('AAPL', 'MSFT'): 0.65,
            ('GOLD', 'SILVER'): 0.78,
            ('BTC', 'GOLD'): -0.15,  # همبستگی منفی
            ('USD/JPY', 'EUR/USD'): -0.68
        }
        
        # ترتیب نام‌ها
        key1 = (asset1, asset2)
        key2 = (asset2, asset1)
        
        if key1 in correlation_map:
            return correlation_map[key1]
        elif key2 in correlation_map:
            return correlation_map[key2]
        else:
            # اگر دارایی‌ها از نوع مشابه باشند، همبستگی متوسط
            type1 = self.detect_asset_type(asset1)
            type2 = self.detect_asset_type(asset2)
            
            if type1 == type2:
                return 0.4  # همبستگی متوسط
            else:
                return 0.1  # همبستگی پایین
    
    def calculate_trailing_stop(self,
                              entry_price: float,
                              current_price: float,
                              signal_direction: str,
                              trail_distance: float = 0.01) -> float:
        """محاسبه trailing stop loss"""
        try:
            if signal_direction.upper() == 'BUY':
                # برای خرید، trailing stop پایین‌تر از قیمت فعلی
                trailing_stop = current_price * (1 - trail_distance)
                # اطمینان از اینکه trailing stop بالاتر از entry نباشد
                min_stop = entry_price * (1 - trail_distance * 2)
                return max(trailing_stop, min_stop)
                
            else:  # SELL
                # برای فروش، trailing stop بالاتر از قیمت فعلی
                trailing_stop = current_price * (1 + trail_distance)
                # اطمینان از اینکه trailing stop پایین‌تر از entry نباشد
                max_stop = entry_price * (1 + trail_distance * 2)
                return min(trailing_stop, max_stop)
                
        except Exception as e:
            logger.error(f"❌ خطا در محاسبه trailing stop: {e}")
            return entry_price
    
    def assess_market_risk(self, market_conditions: Dict) -> Dict:
        """ارزیابی ریسک کلی بازار"""
        try:
            risk_factors = {
                'volatility_risk': 0,
                'correlation_risk': 0,
                'concentration_risk': 0,
                'market_sentiment_risk': 0
            }
            
            # ریسک نوسانات
            avg_volatility = market_conditions.get('avg_volatility', 0.02)
            if avg_volatility > 0.05:
                risk_factors['volatility_risk'] = 0.8
            elif avg_volatility > 0.03:
                risk_factors['volatility_risk'] = 0.4
            else:
                risk_factors['volatility_risk'] = 0.1
            
            # ریسک تمرکز
            active_markets = market_conditions.get('active_markets', 1)
            if active_markets < 3:
                risk_factors['concentration_risk'] = 0.7
            elif active_markets < 5:
                risk_factors['concentration_risk'] = 0.3
            else:
                risk_factors['concentration_risk'] = 0.1
            
            # محاسبه ریسک کلی
            overall_risk = sum(risk_factors.values()) / len(risk_factors)
            
            # توصیه‌های بر اساس ریسک
            if overall_risk > 0.6:
                recommendation = "HIGH_RISK: کاهش اندازه پوزیشن‌ها"
                position_multiplier = 0.5
            elif overall_risk > 0.3:
                recommendation = "MEDIUM_RISK: احتیاط معمولی"
                position_multiplier = 0.8
            else:
                recommendation = "LOW_RISK: عملیات عادی"
                position_multiplier = 1.0
            
            return {
                'overall_risk': overall_risk,
                'risk_factors': risk_factors,
                'recommendation': recommendation,
                'position_multiplier': position_multiplier,
                'max_concurrent_trades': int(self.risk_settings['max_concurrent_trades'] * position_multiplier)
            }
            
        except Exception as e:
            logger.error(f"❌ خطا در ارزیابی ریسک بازار: {e}")
            return {'overall_risk': 0.5, 'position_multiplier': 0.8}
    
    def generate_risk_report(self) -> Dict:
        """تولید گزارش جامع ریسک"""
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'risk_settings': self.risk_settings,
                'active_protections': [
                    'Kelly Criterion Position Sizing',
                    'Dynamic Stop Loss',
                    'Correlation-Based Diversification',
                    'Volatility-Adjusted Risk',
                    'Trailing Stop Loss'
                ],
                'risk_metrics': {
                    'max_single_trade_risk': f"{self.risk_settings['max_portfolio_risk']*100:.1f}%",
                    'max_concurrent_trades': self.risk_settings['max_concurrent_trades'],
                    'protection_systems': len(self.risk_settings)
                },
                'recommendations': [
                    "نظارت مداوم بر همبستگی دارایی‌ها",
                    "تنظیم خودکار stop loss بر اساس نوسانات",
                    "استفاده از Kelly Criterion برای اندازه‌گیری پوزیشن",
                    "اعمال trailing stop برای حفظ سود"
                ]
            }
            
            logger.info("📊 گزارش ریسک تولید شد")
            return report
            
        except Exception as e:
            logger.error(f"❌ خطا در تولید گزارش ریسک: {e}")
            return {}

# تست سیستم
def test_risk_manager():
    """تست مدیر ریسک پیشرفته"""
    risk_manager = AdvancedRiskManager()
    
    print("🛡️ تست مدیر ریسک پیشرفته")
    print("=" * 50)
    
    # تست Kelly position sizing
    position_size = risk_manager.calculate_optimal_position_size(
        win_probability=0.65,
        avg_win=0.025,
        avg_loss=0.012,
        account_balance=10000
    )
    print(f"💰 Kelly position size: ${position_size:.2f}")
    
    # تست dynamic stop loss
    stop_loss = risk_manager.calculate_dynamic_stop_loss(
        asset="BTC",
        entry_price=50000,
        volatility=0.035
    )
    print(f"🎯 Dynamic stop loss: {stop_loss*100:.2f}%")
    
    # تست ارزیابی ریسک بازار
    market_risk = risk_manager.assess_market_risk({
        'avg_volatility': 0.04,
        'active_markets': 4
    })
    print(f"📊 Market risk: {market_risk['overall_risk']:.2f}")
    print(f"💡 Recommendation: {market_risk['recommendation']}")
    
    # گزارش کامل
    report = risk_manager.generate_risk_report()
    print(f"\n📋 Active protections: {len(report['active_protections'])}")
    
if __name__ == "__main__":
    test_risk_manager()