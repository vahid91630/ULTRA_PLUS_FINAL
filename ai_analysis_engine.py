#!/usr/bin/env python3
"""
🧠 AI Analysis Engine - OpenAI GPT-4 Integration
Advanced AI-powered market analysis and decision making system
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
from openai import OpenAI

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class AIAnalysisEngine:
    """هوش مصنوعی پیشرفته برای تحلیل بازار و تصمیم‌گیری"""
    
    def __init__(self):
        self.client = None
        self.analysis_cache = {}
        self.cache_duration = 300  # 5 minutes cache
        
        if OPENAI_API_KEY:
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            logger.info("🧠 OpenAI AI Engine initialized successfully")
        else:
            logger.warning("⚠️ OPENAI_API_KEY not found - AI features disabled")
    
    async def analyze_market_data(self, market_data: Dict) -> Dict:
        """تحلیل هوشمند داده‌های بازار"""
        if not self.client:
            return self._get_fallback_analysis("AI engine not available")
        
        try:
            # Prepare market data for AI analysis
            data_summary = self._prepare_market_summary(market_data)
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an elite financial AI analyst with expertise in cryptocurrency, forex, stocks, and commodities trading. 
                        Analyze the provided market data and give precise trading recommendations.
                        Respond in JSON format with Persian translations for user interface.
                        Focus on: trend analysis, risk assessment, entry/exit points, profit potential."""
                    },
                    {
                        "role": "user", 
                        "content": f"Analyze this market data and provide trading recommendations: {data_summary}"
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=1500
            )
            
            content = response.choices[0].message.content
            if content:
                analysis_result = json.loads(content)
            else:
                raise ValueError("Empty response from AI")
            
            # Add metadata
            analysis_result.update({
                'timestamp': datetime.now().isoformat(),
                'ai_engine': 'gpt-4o',
                'analysis_type': 'comprehensive_market_analysis',
                'status': 'success'
            })
            
            logger.info("🧠 AI market analysis completed successfully")
            return analysis_result
            
        except Exception as e:
            logger.error(f"AI analysis error: {e}")
            return self._get_fallback_analysis(f"Analysis error: {e}")
    
    async def generate_trading_strategy(self, market_conditions: Dict, risk_level: str = "balanced") -> Dict:
        """تولید استراتژی معاملاتی هوشمند"""
        if not self.client:
            return self._get_fallback_strategy("AI engine not available")
        
        try:
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are an expert algorithmic trading strategist. 
                        Create a detailed trading strategy based on current market conditions.
                        Risk level: {risk_level}
                        Provide entry points, stop losses, take profits, and position sizing.
                        Include Persian descriptions for user interface.
                        Respond in JSON format with actionable trading instructions."""
                    },
                    {
                        "role": "user",
                        "content": f"Market conditions: {json.dumps(market_conditions)}"
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=1200
            )
            
            content = response.choices[0].message.content
            if content:
                strategy = json.loads(content)
            else:
                raise ValueError("Empty strategy response from AI")
            strategy.update({
                'created_at': datetime.now().isoformat(),
                'risk_level': risk_level,
                'ai_engine': 'gpt-4o',
                'strategy_type': 'ai_generated',
                'status': 'success'
            })
            
            logger.info(f"🧠 AI trading strategy generated for {risk_level} risk level")
            return strategy
            
        except Exception as e:
            logger.error(f"Strategy generation error: {e}")
            return self._get_fallback_strategy(f"Strategy error: {e}")
    
    async def analyze_news_sentiment(self, news_articles: List[Dict]) -> Dict:
        """تحلیل احساسات اخبار مالی"""
        if not self.client or not news_articles:
            return self._get_fallback_sentiment("No news data or AI unavailable")
        
        try:
            # Prepare news summary
            news_text = "\n".join([
                f"Title: {article.get('title', '')}\nContent: {article.get('description', '')[:200]}"
                for article in news_articles[:10]  # Limit to 10 articles
            ])
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a financial sentiment analysis expert.
                        Analyze the sentiment of financial news and its potential market impact.
                        Provide sentiment score (-1 to +1), confidence level, and key insights.
                        Include Persian translations for the user interface.
                        Respond in JSON format with detailed sentiment analysis."""
                    },
                    {
                        "role": "user",
                        "content": f"Analyze sentiment of these financial news: {news_text}"
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=800
            )
            
            content = response.choices[0].message.content
            if content:
                sentiment_analysis = json.loads(content)
            else:
                raise ValueError("Empty sentiment response from AI")
            sentiment_analysis.update({
                'analyzed_articles': len(news_articles),
                'analysis_time': datetime.now().isoformat(),
                'ai_engine': 'gpt-4o',
                'status': 'success'
            })
            
            logger.info(f"🧠 News sentiment analyzed: {len(news_articles)} articles")
            return sentiment_analysis
            
        except Exception as e:
            logger.error(f"News sentiment analysis error: {e}")
            return self._get_fallback_sentiment(f"Sentiment error: {e}")
    
    async def make_trading_decision(self, 
                                  market_data: Dict, 
                                  sentiment_data: Dict, 
                                  risk_parameters: Dict) -> Dict:
        """تصمیم‌گیری هوشمند برای معاملات"""
        if not self.client:
            return self._get_fallback_decision("AI engine not available")
        
        try:
            # Combine all data for decision making
            decision_data = {
                'market_data': market_data,
                'sentiment': sentiment_data,
                'risk_params': risk_parameters,
                'timestamp': datetime.now().isoformat()
            }
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an elite AI trading decision maker.
                        Based on market data, sentiment analysis, and risk parameters, make precise trading decisions.
                        Provide: BUY/SELL/HOLD recommendation, confidence level, entry price, stop loss, take profit.
                        Include reasoning in both English and Persian.
                        Respond in JSON format with actionable trading decision."""
                    },
                    {
                        "role": "user",
                        "content": f"Make trading decision based on this data: {json.dumps(decision_data)}"
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            if content:
                decision = json.loads(content)
            else:
                raise ValueError("Empty decision response from AI")
            decision.update({
                'decision_time': datetime.now().isoformat(),
                'ai_engine': 'gpt-4o',
                'decision_type': 'ai_powered',
                'status': 'success'
            })
            
            logger.info(f"🧠 AI trading decision: {decision.get('action', 'UNKNOWN')}")
            return decision
            
        except Exception as e:
            logger.error(f"Trading decision error: {e}")
            return self._get_fallback_decision(f"Decision error: {e}")
    
    def _prepare_market_summary(self, market_data: Dict) -> str:
        """آماده‌سازی خلاصه داده‌های بازار"""
        summary_parts = []
        
        # Add crypto data if available
        if 'crypto' in market_data:
            crypto = market_data['crypto']
            summary_parts.append(f"Crypto: BTC ${crypto.get('btc_price', 'N/A')}, 24h change: {crypto.get('btc_change', 'N/A')}%")
        
        # Add forex data if available
        if 'forex' in market_data:
            forex = market_data['forex']
            summary_parts.append(f"Forex: EUR/USD {forex.get('eur_usd', 'N/A')}")
        
        # Add stocks data if available
        if 'stocks' in market_data:
            stocks = market_data['stocks']
            summary_parts.append(f"Stocks: AAPL ${stocks.get('aapl_price', 'N/A')}")
        
        return "; ".join(summary_parts) if summary_parts else "Limited market data available"
    
    def _get_fallback_analysis(self, reason: str) -> Dict:
        """تحلیل پشتیبان در صورت عدم دسترسی به AI"""
        return {
            'trend': 'neutral',
            'recommendation': 'HOLD',
            'confidence': 0.3,
            'reason': reason,
            'persian_summary': 'تحلیل AI در دسترس نیست - از داده‌های پشتیبان استفاده شده',
            'status': 'fallback',
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_fallback_strategy(self, reason: str) -> Dict:
        """استراتژی پشتیبان"""
        return {
            'strategy_name': 'Conservative Hold',
            'action': 'HOLD',
            'confidence': 0.3,
            'reason': reason,
            'persian_description': 'استراتژی محافظه‌کارانه - AI در دسترس نیست',
            'status': 'fallback',
            'created_at': datetime.now().isoformat()
        }
    
    def _get_fallback_sentiment(self, reason: str) -> Dict:
        """احساسات پشتیبان"""
        return {
            'sentiment_score': 0.0,
            'confidence': 0.3,
            'market_impact': 'neutral',
            'reason': reason,
            'persian_summary': 'تحلیل احساسات در دسترس نیست',
            'status': 'fallback',
            'analysis_time': datetime.now().isoformat()
        }
    
    def _get_fallback_decision(self, reason: str) -> Dict:
        """تصمیم پشتیبان"""
        return {
            'action': 'HOLD',
            'confidence': 0.3,
            'reasoning': reason,
            'persian_reasoning': 'سیستم تصمیم‌گیری AI در دسترس نیست',
            'status': 'fallback',
            'decision_time': datetime.now().isoformat()
        }

# Global instance
ai_engine = AIAnalysisEngine()