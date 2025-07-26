#!/usr/bin/env python3
"""
📡 Connection Monitor
Real-time monitoring of system connections and health
"""

import asyncio
import logging
import os
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import aiohttp
import json
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class ServiceStatus(Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    OFFLINE = "offline"

@dataclass
class HealthCheck:
    service_name: str
    status: ServiceStatus
    response_time: float
    last_check: datetime
    error_message: Optional[str] = None
    details: Optional[Dict] = None

class ConnectionMonitor:
    """Monitor system connections and service health"""
    
    def __init__(self):
        self.health_checks: Dict[str, HealthCheck] = {}
        self.monitoring_active = False
        self.check_interval = 30  # seconds
        self.timeout = 10  # seconds
        
        # Define services to monitor
        self.services = {
            'telegram_api': 'https://api.telegram.org/bot{token}/getMe',
            'openai_api': 'https://api.openai.com/v1/models',
            'binance_api': 'https://api.binance.com/api/v3/ping',
            'coingecko_api': 'https://api.coingecko.com/api/v3/ping',
            'coinbase_api': 'https://api.pro.coinbase.com/products',
        }
        
        # Alert thresholds
        self.response_time_warning = 2.0  # seconds
        self.response_time_critical = 5.0  # seconds
    
    async def start_monitoring(self):
        """Start continuous monitoring"""
        self.monitoring_active = True
        logger.info("🔄 Starting connection monitoring...")
        
        while self.monitoring_active:
            try:
                await self._check_all_services()
                await asyncio.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"❌ Monitoring error: {e}")
                await asyncio.sleep(self.check_interval)
    
    async def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring_active = False
        logger.info("⏹️ Connection monitoring stopped")
    
    async def _check_all_services(self):
        """Check all services concurrently"""
        tasks = []
        
        for service_name, url in self.services.items():
            task = asyncio.create_task(self._check_service(service_name, url))
            tasks.append(task)
        
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _check_service(self, service_name: str, url: str):
        """Check individual service health"""
        start_time = time.time()
        
        try:
            headers = {}
            
            # Handle special cases
            if service_name == 'telegram_api':
                token = os.environ.get('ULTRA_Plus_Bot')
                if not token:
                    self._update_health_check(service_name, ServiceStatus.CRITICAL, 0, "Missing token")
                    return
                url = url.format(token=token)
            
            elif service_name == 'openai_api':
                api_key = os.environ.get('OPENAI_API_KEY')
                if not api_key:
                    self._update_health_check(service_name, ServiceStatus.WARNING, 0, "Missing API key")
                    return
                headers = {'Authorization': f'Bearer {api_key}'}
            
            # Make request
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, headers=headers) as response:
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        status = self._determine_status(response_time)
                        self._update_health_check(service_name, status, response_time)
                    else:
                        self._update_health_check(
                            service_name, 
                            ServiceStatus.CRITICAL, 
                            response_time,
                            f"HTTP {response.status}"
                        )
        
        except asyncio.TimeoutError:
            response_time = time.time() - start_time
            self._update_health_check(service_name, ServiceStatus.CRITICAL, response_time, "Timeout")
        
        except Exception as e:
            response_time = time.time() - start_time
            self._update_health_check(service_name, ServiceStatus.OFFLINE, response_time, str(e))
    
    def _determine_status(self, response_time: float) -> ServiceStatus:
        """Determine service status based on response time"""
        if response_time > self.response_time_critical:
            return ServiceStatus.CRITICAL
        elif response_time > self.response_time_warning:
            return ServiceStatus.WARNING
        else:
            return ServiceStatus.HEALTHY
    
    def _update_health_check(self, service_name: str, status: ServiceStatus, 
                           response_time: float, error_message: str = None):
        """Update health check results"""
        health_check = HealthCheck(
            service_name=service_name,
            status=status,
            response_time=response_time,
            last_check=datetime.now(),
            error_message=error_message
        )
        
        self.health_checks[service_name] = health_check
        
        # Log status changes
        if status != ServiceStatus.HEALTHY:
            logger.warning(f"⚠️ {service_name}: {status.value} ({response_time:.2f}s) - {error_message}")
        else:
            logger.debug(f"✅ {service_name}: {status.value} ({response_time:.2f}s)")
    
    def get_health_summary(self) -> Dict:
        """Get comprehensive health summary"""
        if not self.health_checks:
            return {'status': 'no_data', 'services': {}}
        
        service_summary = {}
        overall_status = ServiceStatus.HEALTHY
        
        for service_name, check in self.health_checks.items():
            service_summary[service_name] = {
                'status': check.status.value,
                'response_time': check.response_time,
                'last_check': check.last_check.isoformat(),
                'error_message': check.error_message
            }
            
            # Determine overall status
            if check.status == ServiceStatus.CRITICAL:
                overall_status = ServiceStatus.CRITICAL
            elif check.status == ServiceStatus.WARNING and overall_status == ServiceStatus.HEALTHY:
                overall_status = ServiceStatus.WARNING
        
        return {
            'overall_status': overall_status.value,
            'services': service_summary,
            'monitoring_active': self.monitoring_active,
            'last_update': datetime.now().isoformat()
        }
    
    def get_menu_status_text(self):
        """Get status text for bot menu"""
        if not self.health_checks:
            return "🔄 در حال بررسی..."
            
        healthy_count = sum(1 for check in self.health_checks.values() 
                          if check.status == ServiceStatus.HEALTHY)
        total_count = len(self.health_checks)
        
        if healthy_count == total_count:
            return "🟢 همه سرویس‌ها سالم"
        elif healthy_count > total_count // 2:
            return f"🟡 {healthy_count}/{total_count} سرویس سالم"
        else:
            return f"🔴 {healthy_count}/{total_count} سرویس با مشکل"
    
    def get_detailed_status_message(self):
        """Get detailed status message for server status command"""
        if not self.health_checks:
            return "📊 سیستم در حال بررسی وضعیت سرویس‌ها...\n\n🔄 لطفاً چند ثانیه صبر کنید."
        
        status_lines = []
        status_lines.append("📊 وضعیت سرویس‌های سیستم:")
        status_lines.append("=" * 30)
        
        for service_name, check in self.health_checks.items():
            if check.status == ServiceStatus.HEALTHY:
                emoji = "🟢"
            elif check.status == ServiceStatus.WARNING:
                emoji = "🟡"
            else:
                emoji = "🔴"
            
            service_display = service_name.replace('_', ' ').title()
            response_time_ms = int(check.response_time * 1000)
            status_lines.append(f"{emoji} {service_display}: {response_time_ms}ms")
            
            if check.error_message and check.status != ServiceStatus.HEALTHY:
                status_lines.append(f"   ↳ {check.error_message}")
        
        status_lines.append("")
        status_lines.append(f"🕐 آخرین بررسی: {datetime.now().strftime('%H:%M:%S')}")
        
        return "\n".join(status_lines)
    
    def get_critical_services(self) -> List[str]:
        """Get list of services in critical state"""
        return [
            name for name, check in self.health_checks.items()
            if check.status == ServiceStatus.CRITICAL
        ]
    
    async def run_health_check(self) -> Dict:
        """Run immediate health check on all services"""
        logger.info("🔍 Running immediate health check...")
        await self._check_all_services()
        return self.get_health_summary()

# Global connection monitor instance
_connection_monitor = None

def get_connection_monitor() -> ConnectionMonitor:
    """Get global connection monitor instance"""
    global _connection_monitor
    if _connection_monitor is None:
        _connection_monitor = ConnectionMonitor()
    return _connection_monitor

# Convenience functions
async def start_connection_monitoring():
    """Start connection monitoring"""
    monitor = get_connection_monitor()
    await monitor.start_monitoring()

async def stop_connection_monitoring():
    """Stop connection monitoring"""
    monitor = get_connection_monitor()
    await monitor.stop_monitoring()

async def get_system_health() -> Dict:
    """Get current system health"""
    monitor = get_connection_monitor()
    return monitor.get_health_summary()

if __name__ == "__main__":
    # Test connection monitoring
    async def test_monitor():
        monitor = ConnectionMonitor()
        
        # Run immediate health check
        health = await monitor.run_health_check()
        print("Health Summary:")
        print(json.dumps(health, indent=2))
        
        # Test continuous monitoring for a short period
        print("\nStarting continuous monitoring for 60 seconds...")
        monitor_task = asyncio.create_task(monitor.start_monitoring())
        
        await asyncio.sleep(60)
        await monitor.stop_monitoring()
        
        # Final health summary
        final_health = monitor.get_health_summary()
        print("\nFinal Health Summary:")
        print(json.dumps(final_health, indent=2))
    
    import os
    asyncio.run(test_monitor())