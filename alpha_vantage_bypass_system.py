#!/usr/bin/env python3
"""
سیستم دور زدن محدودیت Alpha Vantage - مشابه راه‌حل Binance
"""

import requests
import json
import time
import os
from typing import Dict, List, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlphaVantageBypass:
    """سیستم دور زدن محدودیت Alpha Vantage با منابع جایگزین"""
    
    def __init__(self):
        self.alpha_vantage_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.alternative_apis = [
            {
                'name': 'Yahoo Finance',
                'base_url': 'https://query1.finance.yahoo.com/v8/finance/chart/',
                'requires_key': False
            },
            {
                'name': 'Financial Modeling Prep',
                'base_url': 'https://financialmodelingprep.com/api/v3/',
                'requires_key': False  # Free tier available
            },
            {
                'name': 'Twelve Data',
                'base_url': 'https://api.twelvedata.com/',
                'requires_key': False  # Free tier
            },
            {
                'name': 'Polygon.io',
                'base_url': 'https://api.polygon.io/v2/',
                'requires_key': True,
                'key': os.getenv('POLYGON_API_KEY')
            }
        ]
        
    def get_stock_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        """دریافت قیمت سهام با دور زدن محدودیت Alpha Vantage"""
        
        # تلاش اول: Alpha Vantage اصلی
        try:
            if self.alpha_vantage_key:
                av_data = self._try_alpha_vantage(symbol)
                if av_data:
                    logger.info(f"✅ Alpha Vantage اصلی: {symbol} = ${av_data['price']}")
                    return av_data
        except Exception as e:
            logger.warning(f"⚠️ Alpha Vantage محدود شد: {e}")
        
        # جایگزین 1: Yahoo Finance
        try:
            yahoo_data = self._get_yahoo_finance(symbol)
            if yahoo_data:
                logger.info(f"✅ Yahoo Finance: {symbol} = ${yahoo_data['price']}")
                return yahoo_data
        except Exception as e:
            logger.warning(f"خطا در Yahoo Finance: {e}")
        
        # جایگزین 2: Financial Modeling Prep
        try:
            fmp_data = self._get_financial_modeling_prep(symbol)
            if fmp_data:
                logger.info(f"✅ Financial Modeling Prep: {symbol} = ${fmp_data['price']}")
                return fmp_data
        except Exception as e:
            logger.warning(f"خطا در FMP: {e}")
        
        # جایگزین 3: Polygon.io
        try:
            polygon_data = self._get_polygon_data(symbol)
            if polygon_data:
                logger.info(f"✅ Polygon.io: {symbol} = ${polygon_data['price']}")
                return polygon_data
        except Exception as e:
            logger.warning(f"خطا در Polygon: {e}")
        
        # جایگزین 4: Twelve Data
        try:
            twelve_data = self._get_twelve_data(symbol)
            if twelve_data:
                logger.info(f"✅ Twelve Data: {symbol} = ${twelve_data['price']}")
                return twelve_data
        except Exception as e:
            logger.warning(f"خطا در Twelve Data: {e}")
        
        logger.error(f"❌ همه منابع برای {symbol} ناکام")
        return None
    
    def _try_alpha_vantage(self, symbol: str) -> Optional[Dict[str, Any]]:
        """تلاش برای استفاده از Alpha Vantage اصلی"""
        url = f"https://www.alphavantage.co/query"
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': self.alpha_vantage_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            if 'Global Quote' in data:
                quote = data['Global Quote']
                return {
                    'symbol': symbol,
                    'price': float(quote['05. price']),
                    'change': float(quote['09. change']),
                    'change_percent': quote['10. change percent'].replace('%', ''),
                    'volume': int(quote['06. volume']),
                    'source': 'Alpha Vantage'
                }
        
        return None
    
    def _get_yahoo_finance(self, symbol: str) -> Optional[Dict[str, Any]]:
        """دریافت داده از Yahoo Finance"""
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            if 'chart' in data and data['chart']['result']:
                result = data['chart']['result'][0]
                meta = result['meta']
                
                return {
                    'symbol': symbol,
                    'price': float(meta['regularMarketPrice']),
                    'change': float(meta.get('regularMarketPrice', 0) - meta.get('previousClose', 0)),
                    'change_percent': f"{((meta.get('regularMarketPrice', 0) / meta.get('previousClose', 1) - 1) * 100):.2f}%",
                    'volume': int(meta.get('regularMarketVolume', 0)),
                    'source': 'Yahoo Finance'
                }
        
        return None
    
    def _get_financial_modeling_prep(self, symbol: str) -> Optional[Dict[str, Any]]:
        """دریافت داده از Financial Modeling Prep"""
        url = f"https://financialmodelingprep.com/api/v3/quote-short/{symbol}"
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            if data and len(data) > 0:
                quote = data[0]
                return {
                    'symbol': symbol,
                    'price': float(quote['price']),
                    'change': 0,  # FMP free tier doesn't include change
                    'change_percent': '0%',
                    'volume': int(quote.get('volume', 0)),
                    'source': 'Financial Modeling Prep'
                }
        
        return None
    
    def _get_polygon_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """دریافت داده از Polygon.io"""
        polygon_key = os.getenv('POLYGON_API_KEY')
        if not polygon_key:
            return None
        
        url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/prev"
        params = {'apikey': polygon_key}
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            if 'results' in data and data['results']:
                result = data['results'][0]
                return {
                    'symbol': symbol,
                    'price': float(result['c']),  # close price
                    'change': float(result['c'] - result['o']),  # close - open
                    'change_percent': f"{((result['c'] / result['o'] - 1) * 100):.2f}%",
                    'volume': int(result['v']),
                    'source': 'Polygon.io'
                }
        
        return None
    
    def _get_twelve_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """دریافت داده از Twelve Data"""
        url = f"https://api.twelvedata.com/price"
        params = {
            'symbol': symbol,
            'apikey': 'demo'  # Free tier
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            if 'price' in data:
                return {
                    'symbol': symbol,
                    'price': float(data['price']),
                    'change': 0,
                    'change_percent': '0%',
                    'volume': 0,
                    'source': 'Twelve Data'
                }
        
        return None
    
    def get_forex_rate(self, from_currency: str, to_currency: str) -> Optional[Dict[str, Any]]:
        """دریافت نرخ ارز با دور زدن محدودیت"""
        
        # جایگزین 1: ExchangeRate API (رایگان)
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if to_currency in data['rates']:
                    rate = data['rates'][to_currency]
                    logger.info(f"✅ ExchangeRate API: {from_currency}/{to_currency} = {rate}")
                    return {
                        'from': from_currency,
                        'to': to_currency,
                        'rate': float(rate),
                        'source': 'ExchangeRate API'
                    }
        except Exception as e:
            logger.warning(f"خطا در ExchangeRate API: {e}")
        
        # جایگزین 2: Fixer.io (رایگان)
        try:
            url = f"https://api.fixer.io/latest"
            params = {
                'base': from_currency,
                'symbols': to_currency
            }
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'rates' in data and to_currency in data['rates']:
                    rate = data['rates'][to_currency]
                    logger.info(f"✅ Fixer.io: {from_currency}/{to_currency} = {rate}")
                    return {
                        'from': from_currency,
                        'to': to_currency,
                        'rate': float(rate),
                        'source': 'Fixer.io'
                    }
        except Exception as e:
            logger.warning(f"خطا در Fixer.io: {e}")
        
        return None
    
    def get_market_data_comprehensive(self, symbols: List[str]) -> Dict[str, Any]:
        """دریافت داده‌های جامع بازار با دور زدن تمام محدودیت‌ها"""
        results = {
            'stocks': {},
            'forex': {},
            'status': {
                'successful': 0,
                'failed': 0,
                'sources_used': []
            }
        }
        
        # دریافت قیمت سهام
        for symbol in symbols:
            stock_data = self.get_stock_price(symbol)
            if stock_data:
                results['stocks'][symbol] = stock_data
                results['status']['successful'] += 1
                if stock_data['source'] not in results['status']['sources_used']:
                    results['status']['sources_used'].append(stock_data['source'])
            else:
                results['status']['failed'] += 1
        
        # دریافت نرخ ارز
        forex_pairs = [
            ('USD', 'EUR'),
            ('USD', 'GBP'),
            ('USD', 'JPY'),
            ('EUR', 'USD')
        ]
        
        for from_curr, to_curr in forex_pairs:
            forex_data = self.get_forex_rate(from_curr, to_curr)
            if forex_data:
                pair_name = f"{from_curr}{to_curr}"
                results['forex'][pair_name] = forex_data
                if forex_data['source'] not in results['status']['sources_used']:
                    results['status']['sources_used'].append(forex_data['source'])
        
        logger.info(f"✅ داده‌های بازار: {results['status']['successful']} موفق، {results['status']['failed']} ناکام")
        logger.info(f"📊 منابع استفاده شده: {', '.join(results['status']['sources_used'])}")
        
        return results

# تابع اصلی برای تست
def main():
    """تست سیستم دور زدن محدودیت"""
    bypass = AlphaVantageBypass()
    
    # تست سهام
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA']
    print("🔄 تست دور زدن محدودیت Alpha Vantage...")
    
    results = bypass.get_market_data_comprehensive(symbols)
    
    print(f"\n✅ نتایج:")
    print(f"📈 سهام: {len(results['stocks'])} موفق")
    print(f"💱 فارکس: {len(results['forex'])} نرخ")
    print(f"🔗 منابع: {', '.join(results['status']['sources_used'])}")
    
    # نمایش جزئیات
    for symbol, data in results['stocks'].items():
        print(f"  {symbol}: ${data['price']} ({data['source']})")

if __name__ == "__main__":
    main()