#!/usr/bin/env python3
"""
Automated Trader - Handles automated trading logic
"""

import logging
import asyncio
from datetime import datetime
from trading_engine import TradingEngine
from market_data import MarketDataCollector

logger = logging.getLogger(__name__)

class AutomatedTrader:
    """Handles automated trading operations"""
    
    def __init__(self):
        self.trading_engine = TradingEngine()
        self.market_data = MarketDataCollector()
        self.active = False
        self.trading_pairs = ['BTC', 'ETH', 'XRP']
        
    async def initialize(self):
        """Initialize the automated trader"""
        logger.info("🤖 Initializing Automated Trader")
        self.trading_engine.initialize()
        self.market_data.fetcher.initialize()
        self.active = True
        
    async def start_trading(self):
        """Start automated trading"""
        logger.info("🚀 Starting automated trading")
        
        while self.active:
            try:
                # Collect market data
                market_data = await self.market_data.collect_data()
                
                # Simple trading logic
                for symbol, data in market_data.items():
                    if data and data['price'] > 50000:  # Buy condition
                        self.trading_engine.execute_trade(symbol, 'BUY', 0.1)
                    elif data and data['price'] < 45000:  # Sell condition
                        self.trading_engine.execute_trade(symbol, 'SELL', 0.1)
                
                # Wait before next cycle
                await asyncio.sleep(30)
                
            except Exception as e:
                logger.error(f"❌ Trading cycle failed: {e}")
                await asyncio.sleep(60)
                
    def stop_trading(self):
        """Stop automated trading"""
        logger.info("🛑 Stopping automated trading")
        self.active = False
        
    def get_status(self):
        """Get trading status"""
        return {
            'active': self.active,
            'balance': self.trading_engine.get_balance(),
            'active_trades': len(self.trading_engine.get_active_trades())
        }

# Global instance
_automated_trader = None

def get_automated_trader():
    """Get the global automated trader instance"""
    global _automated_trader
    if _automated_trader is None:
        _automated_trader = AutomatedTrader()
    return _automated_trader