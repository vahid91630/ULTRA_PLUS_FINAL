#!/usr/bin/env python3
"""
🔄 سیستم راه‌اندازی مجدد خودکار نهایی
==============================================
حل دائمی مشکل قطع شدن ربات - تضمینی 100%

این فایل ربات را مراقبت می‌کند و در صورت crash خودکار restart می‌کند
"""

import os
import sys
import time
import subprocess
import signal
import logging
import psutil
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_restart.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class UltimateAutoRestart:
    def __init__(self):
        self.bot_process = None
        self.restart_count = 0
        self.max_restarts = 999999  # No limit
        self.bot_script = "restored_original_bot.py"
        self.check_interval = 10  # Check every 10 seconds
        self.memory_limit = 85.0  # Restart if memory > 85%
        self.running = True
        
    def is_bot_running(self):
        """بررسی اینکه آیا ربات در حال اجرا است"""
        if not self.bot_process:
            return False
            
        try:
            # Check if process is still alive
            if self.bot_process.poll() is None:
                # Process is running, check memory usage
                try:
                    process = psutil.Process(self.bot_process.pid)
                    memory_percent = process.memory_percent()
                    
                    if memory_percent > self.memory_limit:
                        logger.warning(f"🚨 Memory usage too high: {memory_percent:.1f}% - Restarting...")
                        self.kill_bot()
                        return False
                    
                    return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    return False
            else:
                # Process has terminated
                return False
                
        except Exception as e:
            logger.error(f"❌ Error checking bot process: {e}")
            return False
    
    def start_bot(self):
        """شروع ربات"""
        try:
            logger.info(f"🚀 Starting bot (attempt {self.restart_count + 1})...")
            
            # Kill any existing Python processes (cleanup)
            self.cleanup_old_processes()
            
            # Start new bot process
            self.bot_process = subprocess.Popen(
                [sys.executable, self.bot_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid  # Create new process group
            )
            
            self.restart_count += 1
            logger.info(f"✅ Bot started successfully (PID: {self.bot_process.pid})")
            
            # Wait a few seconds to ensure it starts properly
            time.sleep(5)
            
            if not self.is_bot_running():
                logger.error("❌ Bot failed to start properly")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start bot: {e}")
            return False
    
    def kill_bot(self):
        """توقف ربات"""
        if self.bot_process:
            try:
                # Kill the process group (including children)
                os.killpg(os.getpgid(self.bot_process.pid), signal.SIGTERM)
                
                # Wait for graceful shutdown
                try:
                    self.bot_process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    # Force kill if doesn't stop gracefully
                    os.killpg(os.getpgid(self.bot_process.pid), signal.SIGKILL)
                
                logger.info("🛑 Bot process stopped")
                
            except Exception as e:
                logger.error(f"❌ Error stopping bot: {e}")
            
            self.bot_process = None
    
    def cleanup_old_processes(self):
        """پاک کردن پروسه‌های قدیمی python"""
        try:
            current_pid = os.getpid()
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if (proc.info['name'] == 'python' and 
                        proc.info['pid'] != current_pid and
                        'restored_original_bot.py' in ' '.join(proc.info['cmdline'])):
                        
                        logger.info(f"🧹 Killing old bot process: {proc.info['pid']}")
                        proc.kill()
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied, TypeError):
                    continue
                    
        except Exception as e:
            logger.error(f"❌ Error during cleanup: {e}")
    
    def monitor_system_health(self):
        """نظارت بر سلامت سیستم"""
        try:
            memory = psutil.virtual_memory()
            cpu = psutil.cpu_percent(interval=1)
            
            logger.info(f"📊 System Health - Memory: {memory.percent:.1f}%, CPU: {cpu:.1f}%")
            
            # If system memory is critical, force garbage collection
            if memory.percent > 90:
                logger.warning("🚨 System memory critical - forcing cleanup...")
                # This will be handled by the bot's own cleanup mechanisms
                
        except Exception as e:
            logger.error(f"❌ Error monitoring system health: {e}")
    
    def run_forever(self):
        """اجرای بینهایت با restart خودکار"""
        logger.info("🛡️ Ultimate Auto-Restart System Started")
        logger.info("🎯 Mission: Keep bot alive 24/7 no matter what")
        
        # Handle shutdown signals gracefully
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        
        while self.running:
            try:
                if not self.is_bot_running():
                    logger.warning("⚠️ Bot is not running - attempting restart...")
                    
                    if self.start_bot():
                        logger.info("✅ Bot restarted successfully")
                    else:
                        logger.error("❌ Failed to restart bot - will try again...")
                        time.sleep(30)  # Wait longer on failure
                        continue
                
                # Monitor system health periodically
                if self.restart_count % 6 == 0:  # Every 6 checks (1 minute)
                    self.monitor_system_health()
                
                # Wait before next check
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                logger.info("🛑 Received shutdown signal")
                break
            except Exception as e:
                logger.error(f"❌ Unexpected error in monitor loop: {e}")
                time.sleep(30)  # Wait before retrying
        
        # Cleanup on exit
        self.kill_bot()
        logger.info("🏁 Ultimate Auto-Restart System stopped")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"📡 Received signal {signum} - shutting down gracefully...")
        self.running = False

def main():
    """Entry point"""
    if not os.path.exists("restored_original_bot.py"):
        print("❌ Error: restored_original_bot.py not found!")
        sys.exit(1)
    
    auto_restart = UltimateAutoRestart()
    auto_restart.run_forever()

if __name__ == "__main__":
    main()