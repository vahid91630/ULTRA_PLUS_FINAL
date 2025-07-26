#!/usr/bin/env python3
"""
🚀 Cloud Run Production Deployment
Single-port, conflict-free deployment for ULTRA_PLUS_BOT
"""

import os
import sys
import logging
import asyncio
from datetime import datetime
from flask import Flask, jsonify, request
import threading
import time
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Global variables for health checks
app_health = {
    'status': 'starting',
    'bot_status': 'initializing',
    'timestamp': datetime.now().isoformat(),
    'version': '1.0.0',
    'port': None
}

# Create Flask app for health checks and webhooks
app = Flask(__name__)

@app.route('/health')
def health_check():
    """Health check endpoint for load balancer"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'ULTRA_PLUS_BOT',
        'version': app_health['version']
    })

@app.route('/readiness')
def readiness_check():
    """Readiness check for Kubernetes/Cloud Run"""
    return jsonify({
        'ready': app_health['status'] == 'running',
        'bot_status': app_health['bot_status'],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/liveness')
def liveness_check():
    """Liveness check for Kubernetes/Cloud Run"""
    return jsonify({
        'alive': True,
        'uptime': time.time() - start_time,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/')
def root():
    """Root endpoint with service info"""
    return jsonify({
        'service': 'ULTRA_PLUS_BOT',
        'status': app_health['status'],
        'bot_status': app_health['bot_status'],
        'version': app_health['version'],
        'port': app_health['port'],
        'timestamp': datetime.now().isoformat(),
        'health_endpoints': ['/health', '/readiness', '/liveness']
    })

# Global bot instance
bot_instance = None
start_time = time.time()

async def initialize_bot():
    """Initialize the bot in a separate thread"""
    global bot_instance, app_health
    
    try:
        logger.info("🤖 Initializing ULTRA_PLUS_BOT...")
        app_health['bot_status'] = 'initializing'
        
        # Import and initialize the bot
        from ULTRA_PLUS_BOT import UltraPlusBot
        
        # Create bot instance
        bot_instance = UltraPlusBot()
        
        # Start bot polling (non-blocking)
        await bot_instance.start_polling()
        
        app_health['bot_status'] = 'running'
        app_health['status'] = 'running'
        logger.info("✅ ULTRA_PLUS_BOT initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Bot initialization failed: {e}")
        app_health['bot_status'] = 'failed'
        app_health['status'] = 'unhealthy'
        raise

def run_bot_async():
    """Run bot in async context"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(initialize_bot())
        # Keep the loop running
        loop.run_forever()
    except Exception as e:
        logger.error(f"❌ Bot async runner failed: {e}")
    finally:
        loop.close()

def main():
    """Main deployment entry point"""
    global app_health
    
    logger.info("🚀 ULTRA_PLUS_BOT Cloud Run Production Deployment")
    logger.info("=" * 60)
    logger.info(f"Deployment Time: {datetime.now().isoformat()}")
    logger.info(f"Python Version: {sys.version}")
    logger.info(f"Working Directory: {os.getcwd()}")
    
    # Get port from environment (Cloud Run provides this)
    port = int(os.environ.get('PORT', 8080))
    app_health['port'] = port
    
    logger.info(f"📡 Server will run on port: {port}")
    
    # Check required environment variables
    required_vars = ['ULTRA_Plus_Bot']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        logger.error(f"❌ Missing required environment variables: {missing_vars}")
        app_health['status'] = 'configuration_error'
        # Don't exit - still serve health checks
    else:
        logger.info("✅ All required environment variables are set")
    
    # Set deployment mode
    os.environ['DEPLOYMENT_MODE'] = 'production'
    os.environ['SINGLE_PORT_MODE'] = 'true'
    
    # Start bot in background thread (if config is valid)
    if not missing_vars:
        try:
            logger.info("🚀 Starting bot in background thread...")
            bot_thread = threading.Thread(target=run_bot_async, daemon=True)
            bot_thread.start()
            logger.info("✅ Bot thread started successfully")
        except Exception as e:
            logger.error(f"❌ Failed to start bot thread: {e}")
            app_health['bot_status'] = 'failed'
    
    # Mark app as ready to serve requests
    app_health['status'] = 'running' if not missing_vars else 'configuration_error'
    
    # Start Flask server (this is the main process)
    logger.info(f"🌐 Starting Flask server on port {port}...")
    logger.info("✅ Health check endpoints available:")
    logger.info(f"   - http://0.0.0.0:{port}/health")
    logger.info(f"   - http://0.0.0.0:{port}/readiness")
    logger.info(f"   - http://0.0.0.0:{port}/liveness")
    
    # Run Flask app - this blocks and serves the single port
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True,
        use_reloader=False
    )

if __name__ == '__main__':
    main()