#!/usr/bin/env python3
"""
مانیتور وب - نمایش وضعیت از طریق وب
"""

from flask import Flask, render_template_string, jsonify
import requests
import subprocess
import json
from datetime import datetime
import threading
import time

app = Flask(__name__)

# Global status
monitor_status = {
    'last_update': None,
    'keeper_running': False,
    'bot_running': False, 
    'bot_healthy': False,
    'bot_uptime': 0,
    'checks_count': 0,
    'restarts_count': 0
}

def update_status():
    """بروزرسانی وضعیت"""
    global monitor_status
    
    while True:
        try:
            # Check processes
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            
            monitor_status['keeper_running'] = 'final_bot_keeper.py' in result.stdout
            monitor_status['bot_running'] = 'restored_original_bot.py' in result.stdout
            
            # Check bot health
            try:
                response = requests.get('http://localhost:5000/health', timeout=3)
                if response.status_code == 200:
                    data = response.json()
                    monitor_status['bot_healthy'] = data.get('ready', False)
                    monitor_status['bot_uptime'] = round(data.get('uptime', 0), 1)
                else:
                    monitor_status['bot_healthy'] = False
            except:
                monitor_status['bot_healthy'] = False
                
            monitor_status['checks_count'] += 1
            monitor_status['last_update'] = datetime.now().strftime('%H:%M:%S')
            
        except Exception as e:
            print(f"Status update error: {e}")
            
        time.sleep(10)  # Update every 10 seconds

# Start status updater thread
status_thread = threading.Thread(target=update_status, daemon=True)
status_thread.start()

@app.route('/')
def dashboard():
    """صفحه اصلی مانیتور"""
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>ULTRA_PLUS_BOT Monitor</title>
        <meta charset="utf-8">
        <meta http-equiv="refresh" content="10">
        <style>
            body { font-family: Arial, sans-serif; background: #1a1a1a; color: white; margin: 20px; }
            .container { max-width: 800px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 30px; }
            .status-card { background: #2d2d2d; padding: 20px; margin: 10px 0; border-radius: 8px; }
            .status-ok { border-left: 5px solid #4CAF50; }
            .status-error { border-left: 5px solid #f44336; }
            .metric { display: inline-block; margin: 10px 20px; }
            .metric-value { font-size: 24px; font-weight: bold; }
            .metric-label { font-size: 14px; color: #aaa; }
            .action-buttons { text-align: center; margin: 20px 0; }
            .btn { 
                background: #2196F3; 
                color: white; 
                border: none; 
                padding: 10px 20px; 
                margin: 5px; 
                border-radius: 5px; 
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
            }
            .btn:hover { background: #1976D2; }
            .btn-success { background: #4CAF50; }
            .btn-success:hover { background: #45a049; }
            .btn-warning { background: #ff9800; }
            .btn-warning:hover { background: #e68900; }
            .btn-danger { background: #f44336; }
            .btn-danger:hover { background: #da190b; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🛡️ ULTRA_PLUS_BOT Monitor</h1>
                <p>Last Update: {{ status.last_update }}</p>
            </div>
            
            <div class="status-card {{ 'status-ok' if status.keeper_running else 'status-error' }}">
                <h3>{{ '✅' if status.keeper_running else '❌' }} Monitor Status</h3>
                <p>{{ 'Running and monitoring' if status.keeper_running else 'Monitor process not found' }}</p>
            </div>
            
            <div class="status-card {{ 'status-ok' if status.bot_running else 'status-error' }}">
                <h3>{{ '✅' if status.bot_running else '❌' }} Bot Process</h3>
                <p>{{ 'Process is running' if status.bot_running else 'Bot process not found' }}</p>
            </div>
            
            <div class="status-card {{ 'status-ok' if status.bot_healthy else 'status-error' }}">
                <h3>{{ '✅' if status.bot_healthy else '❌' }} Bot Health</h3>
                <p>{{ 'Health check passing' if status.bot_healthy else 'Health check failing' }}</p>
            </div>
            
            <div class="status-card status-ok">
                <h3>📊 Metrics</h3>
                <div class="metric">
                    <div class="metric-value">{{ status.bot_uptime }}s</div>
                    <div class="metric-label">Bot Uptime</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{{ status.checks_count }}</div>
                    <div class="metric-label">Health Checks</div>
                </div>
            </div>
            
            <div class="status-card {{ 'status-ok' if (status.keeper_running and status.bot_running and status.bot_healthy) else 'status-error' }}">
                <h3>🎯 Overall Status</h3>
                <p>
                {% if status.keeper_running and status.bot_running and status.bot_healthy %}
                    <strong>ALL SYSTEMS OPERATIONAL</strong><br>
                    مانیتور فعال است و ربات سالم کار می‌کند
                {% else %}
                    <strong>SYSTEM ISSUES DETECTED</strong><br>
                    {% if not status.keeper_running %}• Monitor not running<br>{% endif %}
                    {% if not status.bot_running %}• Bot process not found<br>{% endif %}
                    {% if not status.bot_healthy %}• Bot health check failed<br>{% endif %}
                {% endif %}
                </p>
            </div>
            
            <div class="action-buttons">
                <h3>🎮 کنترل‌های مانیتور</h3>
                <a href="/restart_bot" class="btn btn-warning">🔄 راه‌اندازی مجدد ربات</a>
                <a href="/stop_bot" class="btn btn-danger">⏹️ توقف ربات</a>
                <a href="/start_bot" class="btn btn-success">▶️ شروع ربات</a>
                <a href="/api/status" class="btn">📊 API Status</a>
                <a href="/logs" class="btn">📝 مشاهده Logs</a>
                <a href="/clear_logs" class="btn btn-warning">🧹 پاک کردن Logs</a>
            </div>
            
            <div class="status-card">
                <h3>📋 دستورات سریع</h3>
                <p>
                    • <strong>🔄 راه‌اندازی مجدد:</strong> restart کامل سیستم<br>
                    • <strong>⏹️ توقف:</strong> خاموش کردن ربات<br>
                    • <strong>▶️ شروع:</strong> روشن کردن ربات<br>
                    • <strong>📊 API Status:</strong> داده‌های JSON<br>
                    • <strong>📝 Logs:</strong> فایل‌های گزارش<br>
                    • <strong>🧹 پاک کردن:</strong> حذف logs قدیمی
                </p>
            </div>
        </div>
    </body>
    </html>
    '''
    
    return render_template_string(template, status=monitor_status)

@app.route('/api/status')
def api_status():
    """API وضعیت"""
    return jsonify(monitor_status)

@app.route('/restart_bot')
def restart_bot():
    """راه‌اندازی مجدد ربات"""
    try:
        import subprocess
        import os
        
        # Kill existing bot processes
        subprocess.run(['pkill', '-f', 'restored_original_bot.py'], capture_output=True)
        
        # Wait a moment
        import time
        time.sleep(2)
        
        # Start new process
        subprocess.Popen(['python', 'restored_original_bot.py'], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        
        return """
        <html><body style="background:#1a1a1a;color:white;font-family:Arial;text-align:center;padding:50px;">
        <h1>🔄 ربات در حال راه‌اندازی مجدد</h1>
        <p>صبر کنید، ربات در 30 ثانیه آماده خواهد بود</p>
        <script>setTimeout(function(){window.location.href='/';}, 5000);</script>
        <a href="/" style="color:#2196F3;">بازگشت به مانیتور</a>
        </body></html>
        """
    except Exception as e:
        return f"""
        <html><body style="background:#1a1a1a;color:white;font-family:Arial;text-align:center;padding:50px;">
        <h1>❌ خطا در راه‌اندازی مجدد</h1>
        <p>{str(e)}</p>
        <a href="/" style="color:#2196F3;">بازگشت به مانیتور</a>
        </body></html>
        """

@app.route('/stop_bot')
def stop_bot():
    """توقف ربات"""
    try:
        import subprocess
        
        # Kill bot processes
        result = subprocess.run(['pkill', '-f', 'restored_original_bot.py'], capture_output=True, text=True)
        
        return """
        <html><body style="background:#1a1a1a;color:white;font-family:Arial;text-align:center;padding:50px;">
        <h1>⏹️ ربات متوقف شد</h1>
        <p>تمام فرآیندهای ربات خاموش شدند</p>
        <script>setTimeout(function(){window.location.href='/';}, 3000);</script>
        <a href="/" style="color:#2196F3;">بازگشت به مانیتور</a>
        </body></html>
        """
    except Exception as e:
        return f"""
        <html><body style="background:#1a1a1a;color:white;font-family:Arial;text-align:center;padding:50px;">
        <h1>❌ خطا در توقف ربات</h1>
        <p>{str(e)}</p>
        <a href="/" style="color:#2196F3;">بازگشت به مانیتور</a>
        </body></html>
        """

@app.route('/start_bot')
def start_bot():
    """شروع ربات"""
    try:
        import subprocess
        
        # Start bot
        subprocess.Popen(['python', 'restored_original_bot.py'], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        
        return """
        <html><body style="background:#1a1a1a;color:white;font-family:Arial;text-align:center;padding:50px;">
        <h1>▶️ ربات شروع شد</h1>
        <p>ربات در حال راه‌اندازی است</p>
        <script>setTimeout(function(){window.location.href='/';}, 5000);</script>
        <a href="/" style="color:#2196F3;">بازگشت به مانیتور</a>
        </body></html>
        """
    except Exception as e:
        return f"""
        <html><body style="background:#1a1a1a;color:white;font-family:Arial;text-align:center;padding:50px;">
        <h1>❌ خطا در شروع ربات</h1>
        <p>{str(e)}</p>
        <a href="/" style="color:#2196F3;">بازگشت به مانیتور</a>
        </body></html>
        """

@app.route('/logs')
def view_logs():
    """مشاهده logs"""
    try:
        logs_content = ""
        
        # Read keeper.log
        try:
            with open('keeper.log', 'r') as f:
                keeper_logs = f.read()[-2000:]  # Last 2000 chars
                logs_content += f"=== KEEPER LOG ===\n{keeper_logs}\n\n"
        except:
            logs_content += "=== KEEPER LOG ===\nFile not found\n\n"
        
        # Read bot_output.log
        try:
            with open('bot_output.log', 'r') as f:
                bot_logs = f.read()[-2000:]  # Last 2000 chars
                logs_content += f"=== BOT OUTPUT LOG ===\n{bot_logs}\n\n"
        except:
            logs_content += "=== BOT OUTPUT LOG ===\nFile not found\n\n"
        
        return f"""
        <html><body style="background:#1a1a1a;color:white;font-family:monospace;padding:20px;">
        <h1>📝 System Logs</h1>
        <a href="/" style="color:#2196F3;">بازگشت به مانیتور</a> | 
        <a href="/logs" style="color:#2196F3;">🔄 تازه‌سازی</a>
        <hr>
        <pre style="background:#2d2d2d;padding:15px;border-radius:5px;overflow-x:auto;">
{logs_content}
        </pre>
        </body></html>
        """
    except Exception as e:
        return f"""
        <html><body style="background:#1a1a1a;color:white;font-family:Arial;text-align:center;padding:50px;">
        <h1>❌ خطا در خواندن Logs</h1>
        <p>{str(e)}</p>
        <a href="/" style="color:#2196F3;">بازگشت به مانیتور</a>
        </body></html>
        """

@app.route('/clear_logs')
def clear_logs():
    """پاک کردن logs"""
    try:
        import os
        
        # Clear log files
        log_files = ['keeper.log', 'bot_output.log', 'bot_errors.log']
        cleared = []
        
        for log_file in log_files:
            try:
                if os.path.exists(log_file):
                    with open(log_file, 'w') as f:
                        f.write("")
                    cleared.append(log_file)
            except:
                pass
        
        return f"""
        <html><body style="background:#1a1a1a;color:white;font-family:Arial;text-align:center;padding:50px;">
        <h1>🧹 Logs پاک شد</h1>
        <p>فایل‌های پاک شده: {', '.join(cleared)}</p>
        <script>setTimeout(function(){{window.location.href='/'}}, 3000);</script>
        <a href="/" style="color:#2196F3;">بازگشت به مانیتور</a>
        </body></html>
        """
    except Exception as e:
        return f"""
        <html><body style="background:#1a1a1a;color:white;font-family:Arial;text-align:center;padding:50px;">
        <h1>❌ خطا در پاک کردن Logs</h1>
        <p>{str(e)}</p>
        <a href="/" style="color:#2196F3;">بازگشت به مانیتور</a>
        </body></html>
        """

if __name__ == "__main__":
    print("🌐 Starting Web Monitor on http://localhost:8888")
    app.run(host='0.0.0.0', port=8888, debug=False)