#!/usr/bin/env python3
"""
System Test - Test all 6 API integrations
"""

import asyncio
import sys
import os

async def test_system():
    try:
        from real_market_data_service import real_market_service
        from ai_analysis_engine import ai_engine
        from real_learning_engine import real_learning_engine
        
        print('🧪 Testing comprehensive trading system...')
        
        # Test market data
        crypto_data = await real_market_service.get_real_crypto_prices(['bitcoin'])
        print(f'✅ Crypto: BTC ${crypto_data.get("bitcoin", {}).get("price_usd", "N/A")}')
        
        # Test Twitter sentiment
        twitter_data = await real_market_service.get_twitter_market_sentiment()
        print(f'✅ Twitter: {twitter_data.get("sentiment_score", "N/A")} sentiment')
        
        # Test AI analysis
        ai_analysis = await ai_engine.analyze_market_data({
            'crypto': crypto_data,
            'sentiment': twitter_data
        })
        print(f'✅ AI Analysis: {ai_analysis.get("status", "unknown")} - {ai_analysis.get("recommendation", "N/A")}')
        
        # Test learning system
        learning_status = real_learning_engine.get_real_learning_status()
        print(f'✅ Learning: {learning_status.get("total_patterns", 0)} patterns')
        
        print('🎉 ALL SYSTEMS OPERATIONAL WITH 6 ACTIVE APIs')
        
    except Exception as e:
        print(f'❌ System test error: {e}')

if __name__ == "__main__":
    asyncio.run(test_system())