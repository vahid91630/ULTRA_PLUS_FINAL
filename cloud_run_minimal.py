#!/usr/bin/env python3
"""
Ultra-Minimal Cloud Run Deployment
Single port, minimal dependencies, optimized for deployment
"""

import os
import sys
import logging
import json
from datetime import datetime

# Import HTTP server components with global scope
try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
    SERVER_AVAILABLE = True
except ImportError:
    try:
        # Fallback for older Python versions
        from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
        SERVER_AVAILABLE = True
    except ImportError:
        SERVER_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MinimalHandler(BaseHTTPRequestHandler):
    """Ultra-minimal HTTP handler for Cloud Run deployment"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path in ['/', '/health', '/readiness', '/liveness']:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            
            response = {
                'status': 'healthy',
                'service': 'ultra_plus_bot_minimal',
                'timestamp': datetime.now().isoformat(),
                'mode': 'cloud_run_optimized',
                'port': os.environ.get('PORT', '5000'),
                'deployment': 'minimal_single_port'
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {'error': 'Not Found', 'path': self.path}
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_POST(self):
        """Handle POST requests (webhook endpoint)"""
        if self.path == '/webhook':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Read and log webhook data
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                logger.info(f"Webhook received: {len(post_data)} bytes")
            
            response = {'status': 'ok', 'webhook': 'processed'}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(405)  # Method Not Allowed
            self.end_headers()
    
    def log_message(self, format, *args):
        """Custom logging to reduce noise"""
        logger.info(f"Request: {format % args}")

def main():
    """Main entry point for minimal Cloud Run deployment"""
    
    # Environment setup
    port = int(os.environ.get('PORT', 5000))
    
    # Disable package caching for deployment
    os.environ['PIP_NO_CACHE_DIR'] = '1'
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    
    print("=" * 50)
    print("🚀 ULTRA PLUS BOT - MINIMAL CLOUD RUN")
    print("=" * 50)
    print(f"📅 Start Time: {datetime.now()}")
    print(f"🌐 Port: {port}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"📁 Working Directory: {os.getcwd()}")
    print("🔧 Mode: Single Port Optimized")
    print("📦 Dependencies: Minimal (stdlib only)")
    print("=" * 50)
    
    try:
        if not SERVER_AVAILABLE:
            logger.error("❌ HTTP server not available, using Flask fallback")
            create_flask_fallback(port)
            return
            
        # Create and start HTTP server
        server = HTTPServer(('0.0.0.0', port), MinimalHandler)
        logger.info(f"✅ Minimal HTTP server started on 0.0.0.0:{port}")
        logger.info("🎯 Ready for Cloud Run deployment")
        logger.info("📊 Health endpoints: /, /health, /readiness, /liveness")
        logger.info("🔗 Webhook endpoint: /webhook")
        
        # Start server
        server.serve_forever()
        
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
        if 'server' in locals():
            server.shutdown()
    except Exception as e:
        logger.error(f"❌ Server failed: {e}")
        logger.info("🔄 Attempting Flask fallback...")
        create_flask_fallback(port)

def create_flask_fallback(port):
    """Fallback Flask server if HTTPServer fails"""
    try:
        from flask import Flask, jsonify
        
        app = Flask(__name__)
        
        @app.route('/')
        @app.route('/health')
        @app.route('/readiness')
        @app.route('/liveness')
        def health():
            return jsonify({
                'status': 'healthy',
                'service': 'ultra_plus_bot_flask_fallback',
                'timestamp': datetime.now().isoformat(),
                'mode': 'cloud_run_optimized',
                'port': str(port)
            })
        
        @app.route('/webhook', methods=['POST'])
        def webhook():
            return jsonify({'status': 'ok', 'webhook': 'processed'})
        
        logger.info(f"✅ Flask fallback server starting on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
        
    except Exception as e:
        logger.error(f"❌ Flask fallback failed: {e}")
        logger.info("🔄 Starting emergency mode...")
        create_emergency_mode(port)

def create_emergency_mode(port):
    """Emergency minimal server using only built-in modules"""
    import socket
    import threading
    
    def handle_request(conn, addr):
        try:
            data = conn.recv(1024).decode()
            if data:
                # Simple HTTP response
                response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n"
                response += '{"status": "emergency_mode", "service": "ultra_plus_bot"}'
                conn.send(response.encode())
        except:
            pass
        finally:
            conn.close()
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', port))
        sock.listen(5)
        logger.info(f"🚨 Emergency mode server started on port {port}")
        
        while True:
            conn, addr = sock.accept()
            thread = threading.Thread(target=handle_request, args=(conn, addr))
            thread.daemon = True
            thread.start()
            
    except Exception as e:
        logger.error(f"❌ Emergency mode failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()