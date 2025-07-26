#!/usr/bin/env python3
"""
اتصال پیشرفته به بازارهای مختلف برای افزایش سود
"""

import requests
import yfinance as yf
import json
import asyncio
import aiohttp
from datetime import datetime, timedelta
import time

class AdvancedMarketConnector:
    def __init__(self):
        self.apis = {
            'alpha_vantage': 'demo',  # Replace with real key
            'polygon': 'demo',
            'iex_cloud': 'demo',
            'coinapi': 'demo'
        }
        self.cache = {}
        self.cache_duration = 300  # 5 minutes
    
    async def get_forex_opportunities(self):
        """شناسایی فرصت‌های معاملاتی فارکس"""
        pairs = ['EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD']
        opportunities = []
        
        for pair in pairs:
            try:
                # Alpha Vantage API call
                symbol = pair.replace('/', '')
                url = f"https://www.alphavantage.co/query"
                params = {
                    'function': 'FX_INTRADAY',
                    'from_symbol': symbol[:3],
                    'to_symbol': symbol[3:],
                    'interval': '5min',
                    'apikey': self.apis['alpha_vantage']
                }
                
                # Simulated response for demo
                opportunity = self.analyze_forex_opportunity(pair)
                if opportunity['signal_strength'] > 0.7:
                    opportunities.append(opportunity)
                    
            except Exception as e:
                print(f"❌ خطا در دریافت داده‌های {pair}: {e}")
                
        return opportunities
    
    def analyze_forex_opportunity(self, pair):
        """تحلیل فرصت معاملاتی فارکس"""
        # شبیه‌سازی تحلیل واقعی
        import random
        
        signal_strength = random.uniform(0.3, 0.95)
        trend = random.choice(['BUY', 'SELL'])
        
        return {
            'pair': pair,
            'signal': trend,
            'signal_strength': signal_strength,
            'entry_price': random.uniform(1.0500, 1.0800) if 'EUR' in pair else random.uniform(1.2000, 1.3000),
            'stop_loss': 0.01,  # 1%
            'take_profit': 0.025,  # 2.5%
            'confidence': signal_strength * 100,
            'timeframe': '5min-1hour',
            'risk_reward_ratio': 2.5
        }
    
    async def get_stock_opportunities(self):
        """شناسایی فرصت‌های معاملاتی سهام"""
        stocks = ['AAPL', 'TSLA', 'AMZN', 'GOOGL', 'MSFT']
        opportunities = []
        
        for symbol in stocks:
            try:
                # Yahoo Finance data
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="5d", interval="1h")
                
                if not hist.empty:
                    opportunity = self.analyze_stock_opportunity(symbol, hist)
                    if opportunity['signal_strength'] > 0.6:
                        opportunities.append(opportunity)
                        
            except Exception as e:
                print(f"❌ خطا در تحلیل {symbol}: {e}")
                
        return opportunities
    
    def analyze_stock_opportunity(self, symbol, data):
        """تحلیل فرصت معاملاتی سهام"""
        current_price = data['Close'].iloc[-1]
        
        # Simple moving averages
        sma_20 = data['Close'].rolling(20).mean().iloc[-1]
        sma_50 = data['Close'].rolling(50).mean().iloc[-1] if len(data) >= 50 else sma_20
        
        # Volume analysis
        avg_volume = data['Volume'].mean()
        current_volume = data['Volume'].iloc[-1]
        
        # Signal calculation
        price_momentum = (current_price - sma_20) / sma_20
        volume_factor = current_volume / avg_volume
        
        signal_strength = abs(price_momentum) * min(volume_factor, 2.0)
        signal = 'BUY' if price_momentum > 0 else 'SELL'
        
        return {
            'symbol': symbol,
            'current_price': current_price,
            'signal': signal,
            'signal_strength': min(signal_strength, 1.0),
            'price_momentum': price_momentum,
            'volume_factor': volume_factor,
            'sma_20': sma_20,
            'sma_50': sma_50,
            'stop_loss_pct': 0.02,  # 2%
            'take_profit_pct': 0.04,  # 4%
            'confidence': min(signal_strength * 100, 95)
        }
    
    async def get_crypto_arbitrage_opportunities(self):
        """شناسایی فرصت‌های آربیتراژ کریپتو"""
        symbols = ['BTC', 'ETH', 'BNB']
        exchanges = ['binance', 'coinbase', 'kraken']
        opportunities = []
        
        for symbol in symbols:
            prices = {}
            
            # شبیه‌سازی قیمت‌های مختلف صرافی‌ها
            base_price = 50000 if symbol == 'BTC' else 3000 if symbol == 'ETH' else 300
            
            for exchange in exchanges:
                # شبیه‌سازی اختلاف قیمت کوچک
                import random
                price_variation = random.uniform(-0.005, 0.005)  # ±0.5%
                prices[exchange] = base_price * (1 + price_variation)
            
            # پیدا کردن بهترین فرصت آربیتراژ
            min_price = min(prices.values())
            max_price = max(prices.values())
            profit_margin = (max_price - min_price) / min_price
            
            if profit_margin > 0.002:  # حداقل 0.2% سود
                buy_exchange = [ex for ex, price in prices.items() if price == min_price][0]
                sell_exchange = [ex for ex, price in prices.items() if price == max_price][0]
                
                opportunities.append({
                    'symbol': symbol,
                    'buy_exchange': buy_exchange,
                    'sell_exchange': sell_exchange,
                    'buy_price': min_price,
                    'sell_price': max_price,
                    'profit_margin': profit_margin,
                    'profit_percentage': profit_margin * 100,
                    'estimated_profit': profit_margin * 1000,  # برای $1000
                    'execution_time': '< 30 seconds',
                    'risk_level': 'VERY_LOW'
                })
        
        return opportunities
    
    async def get_commodities_signals(self):
        """سیگنال‌های معاملاتی کالاها"""
        commodities = ['GOLD', 'OIL', 'SILVER']
        signals = []
        
        for commodity in commodities:
            # شبیه‌سازی تحلیل کالا
            import random
            
            signal = {
                'commodity': commodity,
                'signal': random.choice(['BUY', 'SELL']),
                'strength': random.uniform(0.4, 0.9),
                'current_price': 2000 if commodity == 'GOLD' else 80 if commodity == 'OIL' else 25,
                'target_price': 0,
                'stop_loss': 0.015,  # 1.5%
                'take_profit': 0.03,  # 3%
                'timeframe': '1-3 days',
                'fundamental_factors': [
                    'Inflation data',
                    'USD strength',
                    'Geopolitical events'
                ]
            }
            
            signals.append(signal)
        
        return signals
    
    async def scan_all_markets(self):
        """اسکن همزمان تمام بازارها"""
        print("🔍 اسکن فرصت‌های معاملاتی در تمام بازارها...")
        
        # اجرای همزمان تمام تحلیل‌ها
        forex_task = self.get_forex_opportunities()
        stock_task = self.get_stock_opportunities() 
        crypto_arbitrage_task = self.get_crypto_arbitrage_opportunities()
        commodities_task = self.get_commodities_signals()
        
        forex_ops, stock_ops, arbitrage_ops, commodity_signals = await asyncio.gather(
            forex_task, stock_task, crypto_arbitrage_task, commodities_task
        )
        
        # ترکیب و رتبه‌بندی فرصت‌ها
        all_opportunities = {
            'forex': forex_ops,
            'stocks': stock_ops,
            'crypto_arbitrage': arbitrage_ops,
            'commodities': commodity_signals,
            'total_opportunities': len(forex_ops) + len(stock_ops) + len(arbitrage_ops) + len(commodity_signals),
            'scan_time': datetime.now().isoformat(),
            'best_opportunities': self.rank_opportunities(forex_ops, stock_ops, arbitrage_ops, commodity_signals)
        }
        
        return all_opportunities
    
    def rank_opportunities(self, forex, stocks, arbitrage, commodities):
        """رتبه‌بندی بهترین فرصت‌ها"""
        ranked = []
        
        # فرصت‌های فارکس
        for opp in forex:
            if opp['signal_strength'] > 0.8:
                ranked.append({
                    'type': 'FOREX',
                    'asset': opp['pair'],
                    'signal': opp['signal'],
                    'score': opp['signal_strength'],
                    'potential_profit': f"{opp['take_profit']*100:.1f}%",
                    'risk': f"{opp['stop_loss']*100:.1f}%",
                    'timeframe': opp['timeframe']
                })
        
        # فرصت‌های آربیتراژ
        for arb in arbitrage:
            if arb['profit_margin'] > 0.003:  # بیش از 0.3%
                ranked.append({
                    'type': 'ARBITRAGE',
                    'asset': arb['symbol'],
                    'signal': 'BUY_SELL',
                    'score': min(arb['profit_margin'] * 100, 1.0),
                    'potential_profit': f"{arb['profit_percentage']:.2f}%",
                    'risk': 'VERY_LOW',
                    'timeframe': arb['execution_time']
                })
        
        # مرتب‌سازی بر اساس امتیاز
        ranked.sort(key=lambda x: x['score'], reverse=True)
        
        return ranked[:5]  # 5 فرصت برتر

# تست سیستم
async def test_market_scanner():
    """تست اسکنر بازار"""
    scanner = AdvancedMarketConnector()
    results = await scanner.scan_all_markets()
    
    print("\n📊 نتایج اسکن بازار:")
    print(f"🔍 کل فرصت‌ها: {results['total_opportunities']}")
    
    print("\n🏆 5 فرصت برتر:")
    for i, opp in enumerate(results['best_opportunities'], 1):
        print(f"{i}. {opp['type']} - {opp['asset']}")
        print(f"   سیگنال: {opp['signal']} | سود: {opp['potential_profit']} | ریسک: {opp['risk']}")
        print(f"   زمان: {opp['timeframe']} | امتیاز: {opp['score']:.2f}")
        print()

if __name__ == "__main__":
    asyncio.run(test_market_scanner())