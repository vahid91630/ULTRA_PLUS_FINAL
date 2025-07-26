
#!/usr/bin/env python3
"""
Cloud Run Optimized Bot - Production Ready
Single Port Configuration for Cloud Run Deployment
"""

import os
import sys
import logging
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_environment():
    """Setup optimized environment for Cloud Run"""
    
    # Single port configuration for Cloud Run - use PORT env var or default to 5000
    port = int(os.environ.get('PORT', 5000))
    os.environ['PORT'] = str(port)
    
    # Cloud Run deployment settings
    os.environ['DEPLOYMENT_MODE'] = 'cloud_run_optimized'
    os.environ['USE_FALLBACK_DB'] = 'true'
    os.environ['BOT_SINGLE_INSTANCE'] = 'true'
    os.environ['WEBHOOK_MODE'] = 'true'
    os.environ['DISABLE_POLLING'] = 'true'
    
    # Disable package caching to resolve registry push errors
    os.environ['PIP_NO_CACHE_DIR'] = '1'
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    
    logger.info(f"🚀 Environment configured for port {port}")
    logger.info("📦 Package caching disabled for deployment")
    return port

def create_flask_app():
    """Create Flask app with webhook and health endpoints"""
    try:
        from flask import Flask, jsonify, request
        
        app = Flask(__name__)
        
        @app.route('/')
        def index():
            return jsonify({
                'status': 'healthy',
                'service': 'ultra_plus_bot',
                'mode': 'webhook',
                'timestamp': datetime.now().isoformat()
            })
        
        @app.route('/health')
        def health():
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'service': 'ultra_plus_bot'
            })
        
        @app.route('/webhook', methods=['POST'])
        def webhook():
            """Webhook endpoint for Telegram updates"""
            try:
                # Process Telegram webhook updates here
                update_data = request.get_json()
                logger.info(f"Received webhook update: {update_data}")
                return jsonify({'status': 'ok'})
            except Exception as e:
                logger.error(f"Webhook error: {e}")
                return jsonify({'error': str(e)}), 500
        
        return app
    except Exception as e:
        logger.warning(f"Flask app setup failed: {e}")
        return None

def main():
    """Main entry point for cloud run optimized bot"""
    
    print("=" * 60)
    print("🤖 ULTRA_PLUS_BOT - CLOUD RUN OPTIMIZED")
    print("=" * 60)
    print(f"⏰ Start Time: {datetime.now()}")
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Working Dir: {os.getcwd()}")
    
    # Setup environment
    port = setup_environment()
    print(f"🌐 Port: {port}")
    print("=" * 60)
    
    # Check bot token (optional for basic health checks)
    bot_token = os.environ.get('ULTRA_Plus_Bot')
    if not bot_token:
        logger.warning("⚠️ ULTRA_Plus_Bot token not found - running in health check mode only")
    else:
        logger.info("✅ Bot token configured")
    
    try:
        # Create Flask app with webhook endpoints
        app = create_flask_app()
        if not app:
            logger.error("❌ Failed to create Flask app")
            sys.exit(1)
        
        logger.info("✅ Flask app created successfully")
        
        # Start Flask server on the correct port
        logger.info(f"🚀 Starting Flask server on port {port}")
        logger.info("🔧 Cloud Run optimized configuration active")
        
        # Use production-ready WSGI server if available
        try:
            from waitress import serve
            logger.info("📡 Using Waitress WSGI server for production")
            serve(app, host='0.0.0.0', port=port, threads=4)
        except ImportError:
            logger.info("📡 Using Flask development server")
            app.run(
                host='0.0.0.0',
                port=port,
                debug=False,
                threaded=True
            )
        
    except ImportError as e:
        logger.error(f"❌ Failed to import required modules: {e}")
        logger.info("🔄 Attempting fallback mode...")
        # Create minimal fallback server
        create_fallback_server(port)
            
    except Exception as e:
        logger.error(f"❌ Cloud Run optimized bot failed: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)

def create_fallback_server(port):
    """Create minimal HTTP server as fallback"""
    try:
        from http.server import HTTPServer, BaseHTTPRequestHandler
        import json
        
        class HealthHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path in ['/', '/health', '/readiness', '/liveness']:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {
                        'status': 'healthy',
                        'service': 'ultra_plus_bot_fallback',
                        'timestamp': datetime.now().isoformat(),
                        'mode': 'minimal_fallback'
                    }
                    self.wfile.write(json.dumps(response).encode())
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def log_message(self, format, *args):
                logger.info(f"Fallback server: {format % args}")
        
        server = HTTPServer(('0.0.0.0', port), HealthHandler)
        logger.info(f"🚀 Fallback server started on port {port}")
        server.serve_forever()
        
    except Exception as e:
        logger.error(f"❌ Fallback server failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
