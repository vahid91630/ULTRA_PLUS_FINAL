"""
🧠 AI Trading Engine - GPT-4 Powered Decision Making
Advanced market analysis and trading strategy selection
Enhanced with ULTRA_PLUS_PRO_MAX Reinforcement Learning
"""

import asyncio
import logging
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import aiohttp

try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

logger = logging.getLogger(__name__)

class AITradingEngine:
    """GPT-4 powered AI trading engine with advanced market analysis"""

    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.client = None
        self.model = "gpt-4o"  # Latest OpenAI model

        # AI state
        self.learning_data = []
        self.strategy_performance = {}
        self.market_memory = {}
        self.prediction_history = []

        # Learning acceleration
        self.learning_rate = 0.01
        self.batch_size = 64
        self.memory_size = 10000
        self.update_frequency = 5  # minutes
        self.parallel_learning = True

        # Trading strategies
        self.strategies = {
            'scalping': {'timeframe': '1m', 'risk': 0.5, 'profit_target': 0.8},
            'swing': {'timeframe': '4h', 'risk': 1.5, 'profit_target': 3.0},
            'trend_following': {'timeframe': '1d', 'risk': 2.0, 'profit_target': 5.0},
            'mean_reversion': {'timeframe': '1h', 'risk': 1.0, 'profit_target': 2.0},
            'breakout': {'timeframe': '15m', 'risk': 1.2, 'profit_target': 2.5}
        }

        self.current_strategy = 'adaptive'
        self.confidence_threshold = 0.7

        # ULTRA_PLUS_PRO_MAX Integration
        self.rl_engine = None
        self.adaptation_enabled = True
        self.market_regime = "unknown"  # volatile, trending, sideways
        self.ultra_plus_mode = True

        # Rapid Learning Integration
        try:
            from rapid_learning_engine import RapidLearningEngine
            self.rapid_learner = RapidLearningEngine()
        except ImportError:
            logger.warning("⚠️ Rapid Learning Engine not available")
            self.rapid_learner = None
        self.adaptive_confidence = 1.0
        self.learning_acceleration_active = False

        if self.openai_api_key and OPENAI_AVAILABLE:
            self.client = OpenAI(api_key=self.openai_api_key)
            logger.info("✅ AI Engine initialized with GPT-4")
        else:
            logger.warning("⚠️ OpenAI API key not available - AI features limited")

    async def initialize(self):
        """Initialize AI engine"""
        try:
            if self.client:
                # Test OpenAI connection
                await self.test_ai_connection()

                # Load previous learning data
                await self.load_learning_data()

                logger.info("✅ AI Engine fully initialized")
            else:
                logger.warning("⚠️ AI Engine initialized without OpenAI")

        except Exception as e:
            logger.error(f"❌ AI Engine initialization failed: {e}")

    async def test_ai_connection(self):
        """Test OpenAI API connection"""
        try:
            if not self.client:
                return False

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Test connection"}],
                max_tokens=10
            )

            logger.info("✅ OpenAI connection successful")
            return True

        except Exception as e:
            logger.error(f"❌ OpenAI connection failed: {e}")
            return False

    async def analyze_market(self, market_data: Dict = None) -> Dict:
        """Comprehensive AI market analysis"""
        try:
            if not self.client:
                return self._get_fallback_analysis()

            # Prepare market data for AI
            market_context = await self._prepare_market_context(market_data)

            # Create AI prompt
            prompt = self._create_analysis_prompt(market_context)

            # Get AI analysis
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                max_tokens=2000
            )

            # Parse AI response
            ai_analysis = json.loads(response.choices[0].message.content)

            # Enhance with technical analysis
            enhanced_analysis = await self._enhance_with_technical_analysis(ai_analysis, market_data)

            # Store for learning
            await self._store_analysis_for_learning(enhanced_analysis)

            return enhanced_analysis

        except Exception as e:
            logger.error(f"❌ AI market analysis failed: {e}")
            return self._get_fallback_analysis()

    def _get_system_prompt(self) -> str:
        """Get system prompt for AI"""
        return """
        You are an expert cryptocurrency trading AI with advanced market analysis capabilities.
        Your goal is to provide accurate, data-driven trading insights while prioritizing capital protection.

        Key principles:
        1. Capital preservation is paramount
        2. Risk management is essential
        3. Provide confidence scores for all recommendations
        4. Consider both technical and fundamental factors
        5. Acknowledge uncertainty when markets are unpredictable

        Always respond in JSON format with the following structure:
        {
            "main_trend": "bullish/bearish/neutral",
            "trend_strength": 0-100,
            "reversal_probability": 0-100,
            "btc_prediction": price_prediction,
            "eth_prediction": price_prediction,
            "prediction_confidence": 0-100,
            "recommended_strategy": "strategy_name",
            "entry_point": "price_level",
            "stop_loss": "price_level",
            "take_profit": "price_level",
            "rsi": 0-100,
            "macd_signal": "bullish/bearish/neutral",
            "volume_analysis": "high/medium/low",
            "ai_signal": "strong_buy/buy/hold/sell/strong_sell",
            "overall_confidence": 0-100,
            "risk_level": "low/medium/high",
            "reasoning": "detailed_explanation"
        }
        """

    def _create_analysis_prompt(self, market_context: Dict) -> str:
        """Create analysis prompt for AI"""
        return f"""
        Analyze the current cryptocurrency market based on the following data:

        Market Data:
        - BTC Price: ${market_context.get('btc_price', 0):,.2f}
        - BTC 24h Change: {market_context.get('btc_change', 0):.2f}%
        - ETH Price: ${market_context.get('eth_price', 0):,.2f}
        - ETH 24h Change: {market_context.get('eth_change', 0):.2f}%
        - Market Cap: ${market_context.get('total_market_cap', 0):,.0f}
        - Volume: ${market_context.get('total_volume', 0):,.0f}
        - Fear & Greed Index: {market_context.get('fear_greed_index', 50)}

        Technical Indicators:
        - RSI (14): {market_context.get('rsi', 50):.1f}
        - MACD: {market_context.get('macd', 'neutral')}
        - Volume Profile: {market_context.get('volume_profile', 'average')}

        Recent News Sentiment: {market_context.get('news_sentiment', 'neutral')}

        Historical Performance:
        - Our bot's recent accuracy: {market_context.get('bot_accuracy', 0):.1f}%
        - Recent successful strategies: {market_context.get('successful_strategies', [])}

        Please provide a comprehensive analysis with specific trading recommendations.
        Focus on risk management and capital preservation.
        """

    async def _prepare_market_context(self, market_data: Dict = None) -> Dict:
        """Prepare market context for AI analysis"""
        try:
            from market_data import MarketDataCollector

            if not market_data:
                market_collector = MarketDataCollector()
                market_data = await market_collector.get_comprehensive_market_data()

            # Add historical context
            context = {
                'timestamp': datetime.now().isoformat(),
                'btc_price': market_data.get('btc_price', 0),
                'btc_change': market_data.get('btc_change_24h', 0),
                'eth_price': market_data.get('eth_price', 0),
                'eth_change': market_data.get('eth_change_24h', 0),
                'total_market_cap': market_data.get('total_market_cap', 0),
                'total_volume': market_data.get('total_volume', 0),
                'fear_greed_index': market_data.get('fear_greed_index', 50),
                'rsi': market_data.get('rsi', 50),
                'macd': market_data.get('macd_signal', 'neutral'),
                'volume_profile': market_data.get('volume_profile', 'average'),
                'news_sentiment': market_data.get('news_sentiment', 'neutral'),
                'bot_accuracy': await self._get_recent_accuracy(),
                'successful_strategies': await self._get_successful_strategies()
            }

            return context

        except Exception as e:
            logger.error(f"❌ Failed to prepare market context: {e}")
            return {}

    async def _enhance_with_technical_analysis(self, ai_analysis: Dict, market_data: Dict) -> Dict:
        """Enhance AI analysis with technical indicators"""
        try:
            # Add technical enhancements
            enhanced = ai_analysis.copy()

            # Calculate confidence adjustments
            confidence_adjustments = []

            # RSI confirmation
            rsi = market_data.get('rsi', 50) if market_data else 50
            if rsi > 70 and ai_analysis.get('ai_signal') in ['strong_buy', 'buy']:
                confidence_adjustments.append(-10)  # Reduce confidence in overbought
            elif rsi < 30 and ai_analysis.get('ai_signal') in ['strong_sell', 'sell']:
                confidence_adjustments.append(-10)  # Reduce confidence in oversold

            # Volume confirmation
            volume_profile = market_data.get('volume_profile', 'average') if market_data else 'average'
            if volume_profile == 'high' and ai_analysis.get('ai_signal') != 'hold':
                confidence_adjustments.append(5)  # Increase confidence with volume
            elif volume_profile == 'low' and ai_analysis.get('ai_signal') != 'hold':
                confidence_adjustments.append(-5)  # Reduce confidence without volume

            # Apply confidence adjustments
            original_confidence = enhanced.get('overall_confidence', 50)
            adjusted_confidence = max(0, min(100, original_confidence + sum(confidence_adjustments)))
            enhanced['overall_confidence'] = adjusted_confidence

            # Add technical details
            enhanced['technical_details'] = {
                'rsi_level': rsi,
                'volume_confirmation': volume_profile == 'high',
                'confidence_adjustments': confidence_adjustments,
                'technical_score': self._calculate_technical_score(market_data)
            }

            return enhanced

        except Exception as e:
            logger.error(f"❌ Technical analysis enhancement failed: {e}")
            return ai_analysis

    def _calculate_technical_score(self, market_data: Dict) -> float:
        """Calculate technical analysis score"""
        try:
            if not market_data:
                return 50.0

            score = 0
            factors = 0

            # RSI scoring
            rsi = market_data.get('rsi', 50)
            if 30 <= rsi <= 70:
                score += 20
            elif 20 <= rsi <= 80:
                score += 10
            factors += 1

            # Volume scoring
            volume_profile = market_data.get('volume_profile', 'average')
            if volume_profile == 'high':
                score += 15
            elif volume_profile == 'average':
                score += 10
            factors += 1

            # MACD scoring
            macd = market_data.get('macd_signal', 'neutral')
            if macd in ['bullish', 'bearish']:
                score += 15
            elif macd == 'neutral':
                score += 10
            factors += 1

            return (score / factors) * 5 if factors > 0 else 50.0

        except Exception as e:
            logger.error(f"❌ Technical score calculation failed: {e}")
            return 50.0

    async def _store_analysis_for_learning(self, analysis: Dict):
        """Store analysis for machine learning"""
        try:
            learning_record = {
                'timestamp': datetime.now().isoformat(),
                'analysis': analysis,
                'market_conditions': {
                    'btc_price': analysis.get('btc_prediction', 0),
                    'eth_price': analysis.get('eth_prediction', 0),
                    'confidence': analysis.get('overall_confidence', 0),
                    'signal': analysis.get('ai_signal', 'hold')
                }
            }

            self.learning_data.append(learning_record)

            # Keep only last 1000 records
            if len(self.learning_data) > 1000:
                self.learning_data = self.learning_data[-1000:]

            logger.debug(f"📚 Stored analysis for learning: {analysis.get('ai_signal', 'unknown')}")

        except Exception as e:
            logger.error(f"❌ Failed to store analysis for learning: {e}")

    async def _get_recent_accuracy(self) -> float:
        """Get recent prediction accuracy"""
        try:
            from database import SecureDatabase

            db = SecureDatabase()
            return await db.get_recent_accuracy()

        except Exception as e:
            logger.error(f"❌ Failed to get recent accuracy: {e}")
            return 0.0

    async def _get_successful_strategies(self) -> List[str]:
        """Get list of recently successful strategies"""
        try:
            from database import SecureDatabase

            db = SecureDatabase()
            return await db.get_successful_strategies()

        except Exception as e:
            logger.error(f"❌ Failed to get successful strategies: {e}")
            return []

    def _get_fallback_analysis(self) -> Dict:
        """Get fallback analysis when AI is not available"""
        return {
            'main_trend': 'neutral',
            'trend_strength': 50,
            'reversal_probability': 50,
            'btc_prediction': 0,
            'eth_prediction': 0,
            'prediction_confidence': 30,
            'recommended_strategy': 'hold',
            'entry_point': 'wait',
            'stop_loss': 'manual',
            'take_profit': 'manual',
            'rsi': 50,
            'macd_signal': 'neutral',
            'volume_analysis': 'average',
            'ai_signal': 'hold',
            'overall_confidence': 30,
            'risk_level': 'medium',
            'reasoning': 'AI engine not available - using conservative approach'
        }

    async def get_trading_signal(self, symbol: str = 'BTC') -> Dict:
        """Get specific trading signal for a symbol"""
        try:
            # Get comprehensive market analysis
            market_analysis = await self.analyze_market()

            # Extract signal for specific symbol
            signal = {
                'symbol': symbol,
                'signal': market_analysis.get('ai_signal', 'hold'),
                'confidence': market_analysis.get('overall_confidence', 50),
                'entry_price': market_analysis.get('entry_point', 'current'),
                'stop_loss': market_analysis.get('stop_loss', '2%'),
                'take_profit': market_analysis.get('take_profit', '4%'),
                'risk_level': market_analysis.get('risk_level', 'medium'),
                'strategy': market_analysis.get('recommended_strategy', 'hold'),
                'timestamp': datetime.now().isoformat(),
                'reasoning': market_analysis.get('reasoning', 'AI analysis')
            }

            return signal

        except Exception as e:
            logger.error(f"❌ Failed to get trading signal: {e}")
            return {
                'symbol': symbol,
                'signal': 'hold',
                'confidence': 0,
                'error': str(e)
            }

    async def get_tomorrow_prediction(self) -> str:
        """Get AI prediction for tomorrow"""
        try:
            if not self.client:
                return "⚠️ پیش‌بینی هوش مصنوعی در دسترس نیست"

            prompt = """
            Based on current market conditions and trends, provide a brief prediction for tomorrow's cryptocurrency market.
            Focus on BTC and ETH movements, key levels to watch, and overall market sentiment.
            Respond in Persian (Farsi) and keep it concise but informative.
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a cryptocurrency market analyst. Respond in Persian."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )

            prediction = response.choices[0].message.content.strip()
            return prediction

        except Exception as e:
            logger.error(f"❌ Failed to get tomorrow prediction: {e}")
            return "⚠️ خطا در دریافت پیش‌بینی"

    async def learn_from_outcome(self, prediction: Dict, actual_outcome: Dict):
        """Learn from trading outcome"""
        try:
            learning_record = {
                'timestamp': datetime.now().isoformat(),
                'prediction': prediction,
                'actual_outcome': actual_outcome,
                'accuracy': self._calculate_prediction_accuracy(prediction, actual_outcome),
                'lessons_learned': await self._extract_lessons(prediction, actual_outcome)
            }

            self.prediction_history.append(learning_record)

            # Update strategy performance
            strategy = prediction.get('strategy', 'unknown')
            if strategy not in self.strategy_performance:
                self.strategy_performance[strategy] = {'total': 0, 'successful': 0}

            self.strategy_performance[strategy]['total'] += 1
            if learning_record['accuracy'] > 0.7:
                self.strategy_performance[strategy]['successful'] += 1

            logger.info(f"📚 Learned from outcome: {learning_record['accuracy']:.2f} accuracy")

        except Exception as e:
            logger.error(f"❌ Failed to learn from outcome: {e}")

    def _calculate_prediction_accuracy(self, prediction: Dict, actual: Dict) -> float:
        """Calculate prediction accuracy"""
        try:
            predicted_signal = prediction.get('signal', 'hold')
            actual_result = actual.get('result', 'neutral')

            # Simple accuracy calculation
            if predicted_signal == 'buy' and actual_result == 'profit':
                return 1.0
            elif predicted_signal == 'sell' and actual_result == 'loss_avoided':
                return 1.0
            elif predicted_signal == 'hold' and actual_result == 'neutral':
                return 0.8
            else:
                return 0.2

        except Exception as e:
            logger.error(f"❌ Accuracy calculation failed: {e}")
            return 0.0

    async def _extract_lessons(self, prediction: Dict, actual: Dict) -> List[str]:
        """Extract lessons from trading outcome"""
        lessons = []

        try:
            # Confidence vs accuracy lesson
            confidence = prediction.get('confidence', 50)
            accuracy = self._calculate_prediction_accuracy(prediction, actual)

            if confidence > 80 and accuracy < 0.5:
                lessons.append("High confidence prediction failed - review analysis method")
            elif confidence < 50 and accuracy > 0.8:
                lessons.append("Low confidence prediction succeeded - consider being more confident")

            # Market condition lessons
            market_condition = prediction.get('market_condition', 'normal')
            if market_condition == 'volatile' and accuracy < 0.5:
                lessons.append("Volatile market prediction failed - adjust strategy for volatility")

            return lessons

        except Exception as e:
            logger.error(f"❌ Lesson extraction failed: {e}")
            return []

    async def load_learning_data(self):
        """Load previous learning data"""
        try:
            from database import SecureDatabase

            db = SecureDatabase()
            learning_data = db.get_learning_data()
            self.learning_data = learning_data.get('learning_history', [])
            self.strategy_performance = learning_data.get('performance_metrics', {})

            logger.info(f"📚 Loaded {len(self.learning_data)} learning records")

        except Exception as e:
            logger.error(f"❌ Failed to load learning data: {e}")

    async def save_learning_data(self):
        """Save learning data to database"""
        try:
            from database import SecureDatabase

            db = SecureDatabase()
            await db.save_learning_data(self.learning_data)
            await db.save_strategy_performance(self.strategy_performance)

            logger.info("💾 Learning data saved successfully")

        except Exception as e:
            logger.error(f"❌ Failed to save learning data: {e}")

    async def get_ai_health_status(self) -> Dict:
        """Get AI engine health status"""
        return {
            'openai_available': self.client is not None,
            'learning_records': len(self.learning_data),
            'strategy_performance': self.strategy_performance,
            'current_strategy': self.current_strategy,
            'confidence_threshold': self.confidence_threshold,
            'last_analysis': datetime.now().isoformat()
        }