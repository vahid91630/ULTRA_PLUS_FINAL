#!/usr/bin/env python3
"""
⚡ Asynchronous Market Data Collection System
High-performance, non-blocking data collection with caching and rate limiting
"""

import asyncio
import aiohttp
import logging
import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import json
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)

class DataSource(Enum):
    BINANCE = "binance"
    COINBASE = "coinbase"
    COINGECKO = "coingecko"
    KRAKEN = "kraken"
    NEWSAPI = "newsapi"

@dataclass
class MarketDataPoint:
    symbol: str
    price: float
    volume: float
    timestamp: datetime
    source: DataSource
    bid: Optional[float] = None
    ask: Optional[float] = None
    change_24h: Optional[float] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)

class AsyncMarketDataCache:
    """High-performance in-memory cache with TTL"""
    
    def __init__(self, default_ttl: int = 30):
        self.cache: Dict[str, Tuple[Any, float]] = {}
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            data, expiry = self.cache[key]
            if time.time() < expiry:
                self.hits += 1
                return data
            else:
                del self.cache[key]
        
        self.misses += 1
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        ttl = ttl or self.default_ttl
        expiry = time.time() + ttl
        self.cache[key] = (value, expiry)
    
    def clear(self) -> None:
        self.cache.clear()
    
    def get_stats(self) -> Dict:
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'cache_size': len(self.cache)
        }

class AsyncMarketDataCollector:
    """Asynchronous market data collector with multiple sources and caching"""
    
    def __init__(self, max_concurrent_requests: int = 20):
        self.session: Optional[aiohttp.ClientSession] = None
        self.cache = AsyncMarketDataCache()
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)
        self.rate_limits = {
            DataSource.BINANCE: 1200,  # requests per minute
            DataSource.COINBASE: 10,
            DataSource.COINGECKO: 50,
            DataSource.KRAKEN: 60,
            DataSource.NEWSAPI: 100
        }
        self.request_times = {source: [] for source in DataSource}
        
    async def __aenter__(self):
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def initialize(self):
        """Initialize async session and components"""
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
        
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            connector=connector,
            headers={
                'User-Agent': 'ULTRA_PLUS_BOT/1.0 (High-Performance Trading Bot)'
            }
        )
        
        logger.info("🚀 AsyncMarketDataCollector initialized")
    
    async def close(self):
        """Close async session"""
        if self.session:
            await self.session.close()
            logger.info("🔒 AsyncMarketDataCollector closed")
    
    async def _check_rate_limit(self, source: DataSource) -> bool:
        """Check if request is within rate limit"""
        now = time.time()
        minute_ago = now - 60
        
        # Clean old requests
        self.request_times[source] = [
            t for t in self.request_times[source] if t > minute_ago
        ]
        
        # Check if under limit
        if len(self.request_times[source]) >= self.rate_limits[source]:
            return False
        
        self.request_times[source].append(now)
        return True
    
    async def _make_request(self, url: str, source: DataSource, 
                          params: Optional[Dict] = None) -> Optional[Dict]:
        """Make rate-limited HTTP request"""
        async with self.semaphore:
            # Check rate limit
            if not await self._check_rate_limit(source):
                logger.warning(f"Rate limit exceeded for {source.value}")
                return None
            
            try:
                if not self.session:
                    return None
                async with self.session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.warning(f"HTTP {response.status} from {source.value}: {url}")
                        return None
            except Exception as e:
                logger.error(f"Request failed for {source.value}: {e}")
                return None
    
    async def get_binance_data(self, symbol: str) -> Optional[MarketDataPoint]:
        """Get data from Binance API"""
        cache_key = f"binance_{symbol}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        url = "https://api.binance.com/api/v3/ticker/24hr"
        params = {"symbol": symbol.upper().replace('/', '')}
        
        data = await self._make_request(url, DataSource.BINANCE, params)
        if not data:
            return None
        
        try:
            market_data = MarketDataPoint(
                symbol=symbol,
                price=float(data['lastPrice']),
                volume=float(data['volume']),
                timestamp=datetime.now(),
                source=DataSource.BINANCE,
                bid=float(data.get('bidPrice', 0)),
                ask=float(data.get('askPrice', 0)),
                change_24h=float(data.get('priceChangePercent', 0))
            )
            
            self.cache.set(cache_key, market_data, ttl=30)
            return market_data
            
        except (KeyError, ValueError) as e:
            logger.error(f"Error parsing Binance data: {e}")
            return None
    
    async def get_coingecko_data(self, symbol: str) -> Optional[MarketDataPoint]:
        """Get data from CoinGecko API"""
        cache_key = f"coingecko_{symbol}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        # Map common symbols to CoinGecko IDs
        symbol_map = {
            'BTC': 'bitcoin',
            'ETH': 'ethereum',
            'ADA': 'cardano',
            'DOT': 'polkadot',
            'LINK': 'chainlink'
        }
        
        coin_id = symbol_map.get(symbol.upper(), symbol.lower())
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': coin_id,
            'vs_currencies': 'usd',
            'include_24hr_change': 'true',
            'include_24hr_vol': 'true'
        }
        
        data = await self._make_request(url, DataSource.COINGECKO, params)
        if not data or coin_id not in data:
            return None
        
        try:
            coin_data = data[coin_id]
            market_data = MarketDataPoint(
                symbol=symbol,
                price=float(coin_data['usd']),
                volume=float(coin_data.get('usd_24h_vol', 0)),
                timestamp=datetime.now(),
                source=DataSource.COINGECKO,
                change_24h=float(coin_data.get('usd_24h_change', 0))
            )
            
            self.cache.set(cache_key, market_data, ttl=60)
            return market_data
            
        except (KeyError, ValueError) as e:
            logger.error(f"Error parsing CoinGecko data: {e}")
            return None
    
    async def get_coinbase_data(self, symbol: str) -> Optional[MarketDataPoint]:
        """Get data from Coinbase Pro API"""
        cache_key = f"coinbase_{symbol}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        product_id = symbol.upper().replace('/', '-')
        url = f"https://api.pro.coinbase.com/products/{product_id}/ticker"
        
        data = await self._make_request(url, DataSource.COINBASE)
        if not data:
            return None
        
        try:
            market_data = MarketDataPoint(
                symbol=symbol,
                price=float(data['price']),
                volume=float(data['volume']),
                timestamp=datetime.now(),
                source=DataSource.COINBASE,
                bid=float(data.get('bid', 0)),
                ask=float(data.get('ask', 0))
            )
            
            self.cache.set(cache_key, market_data, ttl=30)
            return market_data
            
        except (KeyError, ValueError) as e:
            logger.error(f"Error parsing Coinbase data: {e}")
            return None
    
    async def get_aggregated_data(self, symbol: str, 
                                sources: Optional[List[DataSource]] = None) -> Dict[str, MarketDataPoint]:
        """Get aggregated data from multiple sources concurrently"""
        if sources is None:
            sources = [DataSource.BINANCE, DataSource.COINGECKO, DataSource.COINBASE]
        
        tasks = []
        for source in sources:
            if source == DataSource.BINANCE:
                tasks.append(self.get_binance_data(symbol))
            elif source == DataSource.COINGECKO:
                tasks.append(self.get_coingecko_data(symbol))
            elif source == DataSource.COINBASE:
                tasks.append(self.get_coinbase_data(symbol))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        aggregated_data = {}
        for i, result in enumerate(results):
            if isinstance(result, MarketDataPoint):
                aggregated_data[sources[i].value] = result
            elif isinstance(result, Exception):
                logger.error(f"Error from {sources[i].value}: {result}")
        
        return aggregated_data
    
    async def get_multiple_symbols(self, symbols: List[str]) -> Dict[str, Dict[str, MarketDataPoint]]:
        """Get data for multiple symbols concurrently"""
        tasks = [self.get_aggregated_data(symbol) for symbol in symbols]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        symbol_data = {}
        for i, result in enumerate(results):
            if isinstance(result, dict):
                symbol_data[symbols[i]] = result
            elif isinstance(result, Exception):
                logger.error(f"Error for symbol {symbols[i]}: {result}")
                symbol_data[symbols[i]] = {}
        
        return symbol_data
    
    def get_cache_stats(self) -> Dict:
        """Get cache performance statistics"""
        return self.cache.get_stats()
    
    def clear_cache(self) -> None:
        """Clear all cached data"""
        self.cache.clear()
        logger.info("🧹 Market data cache cleared")

# Global async market data collector
_async_collector = None

async def get_async_market_data_collector() -> AsyncMarketDataCollector:
    """Get global async market data collector"""
    global _async_collector
    if _async_collector is None:
        _async_collector = AsyncMarketDataCollector()
        await _async_collector.initialize()
    return _async_collector

# High-level async functions for easy integration
async def get_real_time_price(symbol: str) -> Optional[float]:
    """Get real-time price with caching"""
    async with AsyncMarketDataCollector() as collector:
        data = await collector.get_aggregated_data(symbol)
        
        # Return price from most reliable source
        for source in [DataSource.BINANCE, DataSource.COINBASE, DataSource.COINGECKO]:
            if source.value in data:
                return data[source.value].price
        
        return None

async def get_market_overview(symbols: List[str]) -> Dict[str, float]:
    """Get market overview for multiple symbols"""
    async with AsyncMarketDataCollector() as collector:
        symbol_data = await collector.get_multiple_symbols(symbols)
        
        overview = {}
        for symbol, data in symbol_data.items():
            if data:
                # Get price from best available source
                for source in [DataSource.BINANCE, DataSource.COINBASE, DataSource.COINGECKO]:
                    if source.value in data:
                        overview[symbol] = data[source.value].price
                        break
        
        return overview

# Performance benchmark function
async def benchmark_performance():
    """Benchmark the async market data collection performance"""
    symbols = ['BTC/USD', 'ETH/USD', 'ADA/USD', 'DOT/USD', 'LINK/USD']
    
    logger.info("🏃 Starting performance benchmark...")
    
    start_time = time.time()
    
    async with AsyncMarketDataCollector() as collector:
        # Test concurrent collection
        symbol_data = await collector.get_multiple_symbols(symbols)
        
        # Test cache performance
        cache_stats = collector.get_cache_stats()
        
        # Test single symbol performance
        single_start = time.time()
        btc_data = await collector.get_aggregated_data('BTC/USD')
        single_end = time.time()
        
    end_time = time.time()
    
    # Calculate metrics
    total_time = end_time - start_time
    single_time = single_end - single_start
    symbols_collected = len([s for s in symbol_data.values() if s])
    
    benchmark_results = {
        'total_time': total_time,
        'single_symbol_time': single_time,
        'symbols_processed': symbols_collected,
        'avg_time_per_symbol': total_time / len(symbols) if symbols else 0,
        'cache_stats': cache_stats,
        'throughput': symbols_collected / total_time if total_time > 0 else 0
    }
    
    logger.info(f"📊 Benchmark Results:")
    logger.info(f"  Total time: {total_time:.2f}s")
    logger.info(f"  Single symbol time: {single_time:.2f}s")
    logger.info(f"  Symbols processed: {symbols_collected}")
    logger.info(f"  Average time per symbol: {benchmark_results['avg_time_per_symbol']:.2f}s")
    logger.info(f"  Cache hit rate: {cache_stats['hit_rate']:.1f}%")
    logger.info(f"  Throughput: {benchmark_results['throughput']:.2f} symbols/second")
    
    return benchmark_results

if __name__ == "__main__":
    # Test the async market data collector
    async def test_collector():
        async with AsyncMarketDataCollector() as collector:
            # Test single symbol
            btc_data = await collector.get_aggregated_data('BTC/USD')
            print(f"BTC Data: {btc_data}")
            
            # Test multiple symbols
            symbols = ['BTC/USD', 'ETH/USD', 'ADA/USD']
            multi_data = await collector.get_multiple_symbols(symbols)
            print(f"Multi Data: {multi_data}")
            
            # Performance benchmark
            await benchmark_performance()
    
    asyncio.run(test_collector())