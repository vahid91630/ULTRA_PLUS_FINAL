
import os
import time
import json
import psutil
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BudgetMonitor:
    def __init__(self, limit=10):
        self.monthly_limit = limit
        self.current_usage = 0
        self.alerts = {
            'warning': limit * 0.8,    # 80% = $8
            'critical': limit * 0.9,   # 90% = $9
            'emergency': limit * 0.95  # 95% = $9.5
        }
    
    def check_budget_status(self):
        """چک کردن وضعیت بودجه"""
        usage_percent = (self.current_usage / self.monthly_limit) * 100
        
        if self.current_usage >= self.alerts['emergency']:
            return {'status': 'EMERGENCY', 'action': 'IMMEDIATE_OPTIMIZE'}
        elif self.current_usage >= self.alerts['critical']:
            return {'status': 'CRITICAL', 'action': 'FORCE_OPTIMIZE'}
        elif self.current_usage >= self.alerts['warning']:
            return {'status': 'WARNING', 'action': 'MONITOR_CLOSELY'}
        else:
            return {'status': 'NORMAL', 'action': 'CONTINUE'}
    
    def optimize_for_budget(self):
        """بهینه‌سازی برای budget"""
        import gc
        import psutil
        
        # Force garbage collection
        gc.collect()
        
        # Memory optimization
        if psutil.virtual_memory().percent > 80:
            logger.warning("🚨 High memory usage - forcing optimization")
            # محدود کردن processes
            
        return True

# Global budget monitor
budget_monitor = BudgetMonitor(limit=10)
