#!/usr/bin/env python3
"""
🔐 Advanced Security & Risk Management System
Comprehensive security, risk controls, and capital protection
"""

import os
import logging
import hashlib
import hmac
import time
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import asyncio

logger = logging.getLogger(__name__)

@dataclass
class SecurityAlert:
    """Security alert structure"""
    alert_type: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    message: str
    timestamp: str
    resolved: bool = False

@dataclass
class RiskMetrics:
    """Risk assessment metrics"""
    portfolio_risk_score: float
    daily_var: float  # Value at Risk
    maximum_exposure: float
    current_exposure: float
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL

class AdvancedSecurityManager:
    """Advanced security and risk management system"""
    
    def __init__(self, initial_budget: float):
        self.initial_budget = initial_budget
        self.security_config = self._load_security_config()
        self.alerts = []
        self.risk_metrics = RiskMetrics(0, 0, 0, 0, "LOW")
        self.failed_attempts = {}
        self.emergency_stop = False
        
        # Capital protection limits
        self.protection_limits = {
            'max_daily_loss_percent': 5.0,      # Max 5% daily loss
            'max_weekly_loss_percent': 15.0,    # Max 15% weekly loss
            'max_monthly_loss_percent': 30.0,   # Max 30% monthly loss
            'max_position_size_percent': 10.0,   # Max 10% per position
            'max_correlation_risk': 0.7,         # Max correlation between positions
            'min_liquidity_reserve': 20.0        # Keep 20% in cash
        }
        
        # API security
        self.api_rate_limits = {
            'binance': {'calls_per_minute': 1200, 'weight_per_minute': 6000},
            'coinbase': {'calls_per_minute': 10, 'weight_per_minute': 100},
            'alpha_vantage': {'calls_per_day': 500, 'weight_per_day': 500}
        }
        
        logger.info("🔐 Advanced Security Manager initialized")
    
    def _load_security_config(self) -> Dict:
        """Load security configuration"""
        return {
            'enable_2fa': True,
            'api_key_rotation_days': 30,
            'max_concurrent_sessions': 1,
            'ip_whitelist': [],
            'suspicious_activity_threshold': 5,
            'emergency_contacts': [],
            'auto_stop_loss_enabled': True,
            'position_size_validation': True,
            'api_response_validation': True
        }
    
    def validate_trading_decision(self, decision: Dict, current_portfolio: Dict) -> Tuple[bool, str]:
        """Comprehensive validation of trading decisions"""
        try:
            # 1. Budget validation
            if not self._validate_budget_limits(decision, current_portfolio):
                return False, "Budget limits exceeded"
            
            # 2. Position size validation
            if not self._validate_position_size(decision, current_portfolio):
                return False, "Position size limits exceeded"
            
            # 3. Risk concentration validation
            if not self._validate_risk_concentration(decision, current_portfolio):
                return False, "Risk concentration limits exceeded"
            
            # 4. Market conditions validation
            if not self._validate_market_conditions(decision):
                return False, "Adverse market conditions detected"
            
            # 5. API input validation
            if not self._validate_api_inputs(decision):
                return False, "Invalid API inputs detected"
            
            return True, "Validation passed"
            
        except Exception as e:
            logger.error(f"❌ Validation error: {e}")
            return False, f"Validation error: {e}"
    
    def _validate_budget_limits(self, decision: Dict, portfolio: Dict) -> bool:
        """Validate budget and loss limits"""
        try:
            current_value = portfolio.get('total_value', self.initial_budget)
            daily_pnl = current_value - self.initial_budget
            
            # Check daily loss limit
            daily_loss_percent = abs(daily_pnl / self.initial_budget * 100) if daily_pnl < 0 else 0
            if daily_loss_percent > self.protection_limits['max_daily_loss_percent']:
                self._create_alert("CRITICAL", f"Daily loss limit exceeded: {daily_loss_percent:.1f}%")
                return False
            
            # Check if trade amount exceeds limits
            trade_amount = decision.get('amount', 0)
            max_trade_amount = self.initial_budget * (self.protection_limits['max_position_size_percent'] / 100)
            
            if trade_amount > max_trade_amount:
                self._create_alert("HIGH", f"Trade amount {trade_amount} exceeds limit {max_trade_amount}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Budget validation error: {e}")
            return False
    
    def _validate_position_size(self, decision: Dict, portfolio: Dict) -> bool:
        """Validate position sizing rules"""
        try:
            position_size = decision.get('amount', 0)
            total_portfolio_value = portfolio.get('total_value', self.initial_budget)
            
            # Calculate position size as percentage of portfolio
            position_percent = (position_size / total_portfolio_value) * 100
            
            if position_percent > self.protection_limits['max_position_size_percent']:
                self._create_alert("HIGH", f"Position size {position_percent:.1f}% exceeds {self.protection_limits['max_position_size_percent']}%")
                return False
            
            # Check for over-leveraging
            total_exposure = sum(pos.get('value', 0) for pos in portfolio.get('positions', []))
            total_exposure += position_size
            
            exposure_ratio = total_exposure / total_portfolio_value
            if exposure_ratio > 1.5:  # No more than 150% exposure
                self._create_alert("HIGH", f"Total exposure ratio {exposure_ratio:.1f} too high")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Position size validation error: {e}")
            return False
    
    def _validate_risk_concentration(self, decision: Dict, portfolio: Dict) -> bool:
        """Validate risk concentration and correlation"""
        try:
            new_symbol = decision.get('symbol', '')
            positions = portfolio.get('positions', [])
            
            # Check sector/asset concentration
            asset_exposure = {}
            for pos in positions:
                asset_type = self._get_asset_type(pos.get('symbol', ''))
                asset_exposure[asset_type] = asset_exposure.get(asset_type, 0) + pos.get('value', 0)
            
            new_asset_type = self._get_asset_type(new_symbol)
            new_exposure = asset_exposure.get(new_asset_type, 0) + decision.get('amount', 0)
            
            total_value = portfolio.get('total_value', self.initial_budget)
            concentration_percent = (new_exposure / total_value) * 100
            
            # Maximum 40% in any single asset class
            if concentration_percent > 40:
                self._create_alert("MEDIUM", f"Asset concentration in {new_asset_type}: {concentration_percent:.1f}%")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Risk concentration validation error: {e}")
            return False
    
    def _get_asset_type(self, symbol: str) -> str:
        """Classify asset type from symbol"""
        if any(crypto in symbol.upper() for crypto in ['BTC', 'ETH', 'BNB', 'ADA']):
            return 'CRYPTO'
        elif '/' in symbol and 'USD' in symbol:
            return 'FOREX'
        elif len(symbol) <= 5 and symbol.isupper():
            return 'STOCKS'
        else:
            return 'OTHER'
    
    def _validate_market_conditions(self, decision: Dict) -> bool:
        """Validate market conditions for trading"""
        try:
            # Check for emergency stop
            if self.emergency_stop:
                self._create_alert("CRITICAL", "Emergency stop activated")
                return False
            
            # Check market volatility (simplified)
            symbol = decision.get('symbol', '')
            if 'BTC' in symbol and hasattr(self, 'market_volatility'):
                if self.market_volatility > 0.1:  # >10% volatility
                    self._create_alert("MEDIUM", f"High volatility detected: {self.market_volatility*100:.1f}%")
                    # Still allow trading but with warning
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Market conditions validation error: {e}")
            return False
    
    def _validate_api_inputs(self, decision: Dict) -> bool:
        """Validate API inputs for security"""
        try:
            # Check for required fields
            required_fields = ['action', 'symbol', 'amount']
            for field in required_fields:
                if field not in decision or decision[field] is None:
                    return False
            
            # Validate action
            valid_actions = ['BUY', 'SELL', 'HOLD']
            if decision['action'] not in valid_actions:
                return False
            
            # Validate amount
            amount = decision.get('amount', 0)
            if not isinstance(amount, (int, float)) or amount <= 0:
                return False
            
            # Validate symbol format
            symbol = decision.get('symbol', '')
            if len(symbol) < 3 or len(symbol) > 10:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ API input validation error: {e}")
            return False
    
    def monitor_api_usage(self, api_name: str, endpoint: str) -> bool:
        """Monitor and enforce API rate limits"""
        try:
            current_time = time.time()
            key = f"{api_name}_{endpoint}"
            
            # Initialize tracking if not exists
            if not hasattr(self, 'api_usage'):
                self.api_usage = {}
            
            if key not in self.api_usage:
                self.api_usage[key] = {'calls': [], 'last_reset': current_time}
            
            # Clean old calls (older than 1 minute)
            minute_ago = current_time - 60
            self.api_usage[key]['calls'] = [
                call_time for call_time in self.api_usage[key]['calls'] 
                if call_time > minute_ago
            ]
            
            # Check rate limit
            limits = self.api_rate_limits.get(api_name, {'calls_per_minute': 100})
            current_calls = len(self.api_usage[key]['calls'])
            
            if current_calls >= limits['calls_per_minute']:
                self._create_alert("HIGH", f"API rate limit exceeded for {api_name}")
                return False
            
            # Record this call
            self.api_usage[key]['calls'].append(current_time)
            return True
            
        except Exception as e:
            logger.error(f"❌ API monitoring error: {e}")
            return True  # Allow on error to avoid blocking
    
    def validate_api_response(self, api_name: str, response: Dict) -> bool:
        """Validate API response for security and integrity"""
        try:
            # Check for common error indicators
            if 'error' in response:
                self._create_alert("MEDIUM", f"API error from {api_name}: {response['error']}")
                return False
            
            # Check response structure
            if not isinstance(response, dict):
                return False
            
            # Validate price data if present
            if 'price' in response:
                price = response['price']
                if not isinstance(price, (int, float)) or price <= 0:
                    return False
            
            # Check for suspicious data patterns
            if self._detect_suspicious_data_patterns(response):
                self._create_alert("HIGH", f"Suspicious data pattern detected from {api_name}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ API response validation error: {e}")
            return False
    
    def _detect_suspicious_data_patterns(self, data: Dict) -> bool:
        """Detect suspicious patterns in API data"""
        try:
            # Check for unrealistic price movements
            if 'price' in data and 'previous_price' in data:
                current = data['price']
                previous = data['previous_price']
                if previous > 0:
                    change_percent = abs((current - previous) / previous)
                    if change_percent > 0.5:  # >50% change is suspicious
                        return True
            
            # Check for repeated identical values (could indicate stale data)
            if 'price_history' in data:
                prices = data['price_history']
                if len(set(prices)) == 1 and len(prices) > 5:  # All same values
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Suspicious pattern detection error: {e}")
            return False
    
    def calculate_portfolio_risk(self, portfolio: Dict) -> RiskMetrics:
        """Calculate comprehensive portfolio risk metrics"""
        try:
            positions = portfolio.get('positions', [])
            total_value = portfolio.get('total_value', self.initial_budget)
            
            # Calculate Value at Risk (simplified)
            position_risks = []
            total_exposure = 0
            
            for position in positions:
                pos_value = position.get('value', 0)
                volatility = position.get('volatility', 0.02)  # Default 2% daily volatility
                
                # 95% VaR calculation
                var_95 = pos_value * volatility * 1.645  # Z-score for 95%
                position_risks.append(var_95)
                total_exposure += pos_value
            
            # Portfolio VaR (simplified - assumes no correlation)
            portfolio_var = sum(position_risks)
            
            # Risk score (0-100)
            risk_score = min(100, (portfolio_var / total_value) * 100)
            
            # Determine risk level
            if risk_score < 5:
                risk_level = "LOW"
            elif risk_score < 15:
                risk_level = "MEDIUM"
            elif risk_score < 30:
                risk_level = "HIGH"
            else:
                risk_level = "CRITICAL"
            
            self.risk_metrics = RiskMetrics(
                portfolio_risk_score=risk_score,
                daily_var=portfolio_var,
                maximum_exposure=total_value,
                current_exposure=total_exposure,
                risk_level=risk_level
            )
            
            return self.risk_metrics
            
        except Exception as e:
            logger.error(f"❌ Risk calculation error: {e}")
            return RiskMetrics(0, 0, 0, 0, "UNKNOWN")
    
    def emergency_stop_trading(self, reason: str):
        """Emergency stop all trading activities"""
        self.emergency_stop = True
        self._create_alert("CRITICAL", f"EMERGENCY STOP ACTIVATED: {reason}")
        logger.critical(f"🚨 EMERGENCY STOP: {reason}")
    
    def _create_alert(self, severity: str, message: str):
        """Create security alert"""
        alert = SecurityAlert(
            alert_type="SECURITY",
            severity=severity,
            message=message,
            timestamp=datetime.now().isoformat()
        )
        
        self.alerts.append(alert)
        
        # Log based on severity
        if severity == "CRITICAL":
            logger.critical(f"🚨 CRITICAL ALERT: {message}")
        elif severity == "HIGH":
            logger.error(f"⚠️ HIGH ALERT: {message}")
        elif severity == "MEDIUM":
            logger.warning(f"⚠️ MEDIUM ALERT: {message}")
        else:
            logger.info(f"ℹ️ LOW ALERT: {message}")
    
    def get_security_status(self) -> Dict:
        """Get comprehensive security status"""
        recent_alerts = [a for a in self.alerts if not a.resolved]
        
        return {
            'emergency_stop_active': self.emergency_stop,
            'active_alerts': len(recent_alerts),
            'critical_alerts': len([a for a in recent_alerts if a.severity == "CRITICAL"]),
            'high_alerts': len([a for a in recent_alerts if a.severity == "HIGH"]),
            'risk_metrics': {
                'portfolio_risk_score': self.risk_metrics.portfolio_risk_score,
                'risk_level': self.risk_metrics.risk_level,
                'daily_var': self.risk_metrics.daily_var,
                'exposure_ratio': (self.risk_metrics.current_exposure / max(self.risk_metrics.maximum_exposure, 1)) * 100
            },
            'protection_status': {
                'daily_loss_protection': f"{self.protection_limits['max_daily_loss_percent']}%",
                'position_size_limit': f"{self.protection_limits['max_position_size_percent']}%",
                'liquidity_reserve': f"{self.protection_limits['min_liquidity_reserve']}%"
            },
            'last_update': datetime.now().isoformat()
        }
    
    def resolve_alert(self, alert_index: int):
        """Resolve a security alert"""
        if 0 <= alert_index < len(self.alerts):
            self.alerts[alert_index].resolved = True
            logger.info(f"✅ Alert resolved: {self.alerts[alert_index].message}")

# Global instance placeholder - will be initialized with actual budget
advanced_security_manager = None

def initialize_security_manager(initial_budget: float) -> AdvancedSecurityManager:
    """Initialize security manager with budget"""
    global advanced_security_manager
    advanced_security_manager = AdvancedSecurityManager(initial_budget)
    return advanced_security_manager