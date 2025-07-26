import pandas as pd
import numpy as np
from typing import Union, Optional

class TechnicalIndicators:
    """Class containing various technical indicator calculations."""
    
    @staticmethod
    def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Relative Strength Index (RSI).
        
        Args:
            prices: Series of prices
            period: RSI period (default 14)
            
        Returns:
            Series of RSI values
        """
        try:
            if len(prices) < period:
                return pd.Series([50] * len(prices), index=prices.index)
            
            delta = prices.diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            
            avg_gain = gain.rolling(window=period).mean()
            avg_loss = loss.rolling(window=period).mean()
            
            # Avoid division by zero
            rs = avg_gain / avg_loss.replace(0, np.inf)
            rsi = 100 - (100 / (1 + rs))
            
            # Fill NaN values with 50 (neutral)
            rsi = rsi.fillna(50)
            
            return rsi
            
        except Exception as e:
            print(f"Error calculating RSI: {str(e)}")
            return pd.Series([50] * len(prices), index=prices.index)
    
    @staticmethod
    def calculate_moving_average(prices: pd.Series, period: int) -> pd.Series:
        """
        Calculate Simple Moving Average (SMA).
        
        Args:
            prices: Series of prices
            period: Moving average period
            
        Returns:
            Series of moving average values
        """
        try:
            return prices.rolling(window=period).mean()
        except Exception as e:
            print(f"Error calculating moving average: {str(e)}")
            return pd.Series([np.nan] * len(prices), index=prices.index)
    
    @staticmethod
    def calculate_ema(prices: pd.Series, period: int) -> pd.Series:
        """
        Calculate Exponential Moving Average (EMA).
        
        Args:
            prices: Series of prices
            period: EMA period
            
        Returns:
            Series of EMA values
        """
        try:
            return prices.ewm(span=period).mean()
        except Exception as e:
            print(f"Error calculating EMA: {str(e)}")
            return pd.Series([np.nan] * len(prices), index=prices.index)
    
    @staticmethod
    def calculate_macd(prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """
        Calculate MACD (Moving Average Convergence Divergence).
        
        Args:
            prices: Series of prices
            fast: Fast EMA period (default 12)
            slow: Slow EMA period (default 26)
            signal: Signal line EMA period (default 9)
            
        Returns:
            DataFrame with MACD, Signal, and Histogram
        """
        try:
            ema_fast = TechnicalIndicators.calculate_ema(prices, fast)
            ema_slow = TechnicalIndicators.calculate_ema(prices, slow)
            
            macd_line = ema_fast - ema_slow
            signal_line = TechnicalIndicators.calculate_ema(macd_line, signal)
            histogram = macd_line - signal_line
            
            return pd.DataFrame({
                'macd': macd_line,
                'signal': signal_line,
                'histogram': histogram
            })
            
        except Exception as e:
            print(f"Error calculating MACD: {str(e)}")
            return pd.DataFrame({
                'macd': [0] * len(prices),
                'signal': [0] * len(prices),
                'histogram': [0] * len(prices)
            }, index=prices.index)
    
    @staticmethod
    def calculate_bollinger_bands(prices: pd.Series, period: int = 20, std_dev: float = 2) -> pd.DataFrame:
        """
        Calculate Bollinger Bands.
        
        Args:
            prices: Series of prices
            period: Moving average period (default 20)
            std_dev: Number of standard deviations (default 2)
            
        Returns:
            DataFrame with Upper, Middle, and Lower bands
        """
        try:
            middle_band = TechnicalIndicators.calculate_moving_average(prices, period)
            std = prices.rolling(window=period).std()
            
            upper_band = middle_band + (std * std_dev)
            lower_band = middle_band - (std * std_dev)
            
            return pd.DataFrame({
                'upper': upper_band,
                'middle': middle_band,
                'lower': lower_band
            })
            
        except Exception as e:
            print(f"Error calculating Bollinger Bands: {str(e)}")
            return pd.DataFrame({
                'upper': prices,
                'middle': prices,
                'lower': prices
            })
    
    @staticmethod
    def calculate_stochastic(high: pd.Series, low: pd.Series, close: pd.Series, 
                           k_period: int = 14, d_period: int = 3) -> pd.DataFrame:
        """
        Calculate Stochastic Oscillator.
        
        Args:
            high: Series of high prices
            low: Series of low prices
            close: Series of close prices
            k_period: %K period (default 14)
            d_period: %D period (default 3)
            
        Returns:
            DataFrame with %K and %D values
        """
        try:
            lowest_low = low.rolling(window=k_period).min()
            highest_high = high.rolling(window=k_period).max()
            
            k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
            d_percent = k_percent.rolling(window=d_period).mean()
            
            return pd.DataFrame({
                'k_percent': k_percent,
                'd_percent': d_percent
            })
            
        except Exception as e:
            print(f"Error calculating Stochastic: {str(e)}")
            return pd.DataFrame({
                'k_percent': [50] * len(close),
                'd_percent': [50] * len(close)
            }, index=close.index)
    
    @staticmethod
    def calculate_williams_r(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Williams %R.
        
        Args:
            high: Series of high prices
            low: Series of low prices
            close: Series of close prices
            period: Calculation period (default 14)
            
        Returns:
            Series of Williams %R values
        """
        try:
            highest_high = high.rolling(window=period).max()
            lowest_low = low.rolling(window=period).min()
            
            williams_r = -100 * ((highest_high - close) / (highest_high - lowest_low))
            
            return williams_r.fillna(-50)
            
        except Exception as e:
            print(f"Error calculating Williams %R: {str(e)}")
            return pd.Series([-50] * len(close), index=close.index)
    
    @staticmethod
    def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Average True Range (ATR).
        
        Args:
            high: Series of high prices
            low: Series of low prices
            close: Series of close prices
            period: ATR period (default 14)
            
        Returns:
            Series of ATR values
        """
        try:
            prev_close = close.shift(1)
            
            tr1 = high - low
            tr2 = abs(high - prev_close)
            tr3 = abs(low - prev_close)
            
            true_range = pd.DataFrame({'tr1': tr1, 'tr2': tr2, 'tr3': tr3}).max(axis=1)
            atr = true_range.rolling(window=period).mean()
            
            return atr.fillna(0)
            
        except Exception as e:
            print(f"Error calculating ATR: {str(e)}")
            return pd.Series([0] * len(close), index=close.index)
    
    @staticmethod
    def calculate_momentum(prices: pd.Series, period: int = 10) -> pd.Series:
        """
        Calculate Price Momentum.
        
        Args:
            prices: Series of prices
            period: Momentum period (default 10)
            
        Returns:
            Series of momentum values
        """
        try:
            momentum = prices / prices.shift(period) - 1
            return momentum.fillna(0)
            
        except Exception as e:
            print(f"Error calculating momentum: {str(e)}")
            return pd.Series([0] * len(prices), index=prices.index)
    
    @staticmethod
    def calculate_roc(prices: pd.Series, period: int = 12) -> pd.Series:
        """
        Calculate Rate of Change (ROC).
        
        Args:
            prices: Series of prices
            period: ROC period (default 12)
            
        Returns:
            Series of ROC values
        """
        try:
            roc = ((prices - prices.shift(period)) / prices.shift(period)) * 100
            return roc.fillna(0)
            
        except Exception as e:
            print(f"Error calculating ROC: {str(e)}")
            return pd.Series([0] * len(prices), index=prices.index)
