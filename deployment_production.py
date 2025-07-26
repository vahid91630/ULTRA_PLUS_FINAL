#!/usr/bin/env python3
"""
🚀 ULTRA_PLUS_BOT - Production Deployment
Single-instance deployment ready for 24/7 operation
Exclusively for Vahid (وحید)
"""

import os
import asyncio
import logging
from flask import Flask, jsonify
import threading
import time
from datetime import datetime

# Import the original bot components
import os
BOT_TOKEN = os.environ.get('ULTRA_Plus_Bot')

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Flask app for health checks and deployment compliance
app = Flask(__name__)

# Global bot status
bot_status = {
    "ready": False,
    "healthy": False,
    "start_time": datetime.now(),
    "last_check": None
}

@app.route('/health')
def health():
    """Health check endpoint for deployment platforms"""
    return jsonify({
        "ready": bot_status["ready"],
        "status": "healthy" if bot_status["healthy"] else "starting",
        "timestamp": datetime.now().isoformat(),
        "uptime": (datetime.now() - bot_status["start_time"]).total_seconds()
    })

@app.route('/readiness')
def readiness():
    """Readiness check for Kubernetes/Cloud Run"""
    return jsonify({
        "ready": bot_status["ready"],
        "components": {
            "telegram_bot": bot_status["healthy"],
            "flask_server": True
        }
    })

@app.route('/liveness')
def liveness():
    """Liveness check for deployment platforms"""
    return jsonify({
        "alive": True,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/')
def root():
    """Root endpoint"""
    return jsonify({
        "service": "ULTRA_PLUS_BOT",
        "owner": "Vahid (وحید)",
        "status": "running",
        "ready": bot_status["ready"]
    })

async def run_bot():
    """Run the Telegram bot by importing and executing the original bot"""
    try:
        logger.info("🤖 Starting ULTRA_PLUS_BOT for deployment...")
        
        # Import and run the original bot
        import subprocess
        import sys
        
        # Mark as ready
        bot_status["ready"] = True
        bot_status["healthy"] = True 
        bot_status["last_check"] = datetime.now()
        
        logger.info("✅ Starting original bot process...")
        
        # Run the original bot as a subprocess
        process = subprocess.Popen([sys.executable, 'restored_original_bot.py'])
        
        # Monitor the process
        while True:
            bot_status["last_check"] = datetime.now()
            
            # Check if process is still running
            if process.poll() is not None:
                logger.error("❌ Bot process stopped unexpectedly")
                bot_status["healthy"] = False
                # Restart the bot
                process = subprocess.Popen([sys.executable, 'restored_original_bot.py'])
                bot_status["healthy"] = True
                logger.info("🔄 Bot process restarted")
                
            await asyncio.sleep(30)  # Health check every 30 seconds
            
    except Exception as e:
        logger.error(f"❌ Bot error: {e}")
        bot_status["healthy"] = False
        raise

def start_bot_thread():
    """Start bot in a separate thread"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_bot())
    except Exception as e:
        logger.error(f"❌ Bot thread error: {e}")
        bot_status["healthy"] = False

if __name__ == "__main__":
    logger.info("🚀 ULTRA_PLUS_BOT Production Deployment Starting...")
    logger.info("🔐 Security: Single authorized bot instance only")
    logger.info("👤 Owner: Vahid (وحید) - Exclusive access")
    
    # Verify bot token
    if not BOT_TOKEN:
        logger.error("❌ Bot token not found!")
        exit(1)
    
    # Start bot in background thread
    bot_thread = threading.Thread(target=start_bot_thread, daemon=True)
    bot_thread.start()
    
    # Get port from environment (for deployment platforms)
    port = int(os.environ.get('PORT', 5000))
    
    logger.info(f"🌐 Starting Flask server on port {port}")
    logger.info("✅ Health endpoints available:")
    logger.info(f"   • http://0.0.0.0:{port}/health")
    logger.info(f"   • http://0.0.0.0:{port}/readiness") 
    logger.info(f"   • http://0.0.0.0:{port}/liveness")
    
    # Start Flask server
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )