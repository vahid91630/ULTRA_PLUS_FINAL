#!/usr/bin/env python3
"""
ماژول کاری Binance با مدیریت خطا
"""

import ccxt
import os
import time
from datetime import datetime

class WorkingBinance:
    def __init__(self):
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.secret_key = os.getenv('BINANCE_SECRET_KEY')
        self.exchange = None
        self.is_connected = False
        
    def initialize(self):
        """راه‌اندازی اتصال"""
        if not self.api_key or not self.secret_key:
            return False
            
        try:
            # کانفیگ بهینه
            config = {
                'apiKey': self.api_key,
                'secret': self.secret_key,
                'sandbox': False,
                'timeout': 20000,
                'rateLimit': 2000,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot',
                    'recvWindow': 10000
                }
            }
            
            self.exchange = ccxt.binance(config)
            
            # تست اتصال
            self.exchange.fetch_status()
            self.is_connected = True
            return True
            
        except Exception as e:
            self.is_connected = False
            return False
    
    def get_price(self, symbol='BTC/USDT'):
        """دریافت قیمت"""
        if not self.is_connected:
            if not self.initialize():
                return None
                
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker['last']
        except:
            return None
    
    def get_balance(self):
        """دریافت موجودی"""
        if not self.is_connected:
            if not self.initialize():
                return None
                
        try:
            balance = self.exchange.fetch_balance()
            return balance
        except:
            return None

# نمونه استفاده
binance_client = WorkingBinance()
