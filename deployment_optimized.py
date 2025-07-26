#!/usr/bin/env python3
"""
Ultra-Minimal Cloud Run Deployment Entry Point
Optimized for <300MB image size with essential functionality only
No external dependencies beyond core bot
"""

import os
import sys
import time
import logging
from datetime import datetime
from flask import Flask, jsonify

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UltraMinimalBot:
    """Ultra-minimal bot for Cloud Run deployment with no external dependencies"""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        
    def setup_routes(self):
        """Setup minimal health check routes"""
        
        @self.app.route('/')
        def health_check():
            return jsonify({
                "status": "healthy",
                "service": "ULTRA_PLUS_BOT_MINIMAL",
                "deployment": "cloud_run_optimized",
                "timestamp": datetime.now().isoformat(),
                "version": "ultra-minimal-1.0",
                "port": os.environ.get('PORT', 8080)
            })
        
        @self.app.route('/health')
        def health():
            return jsonify({"health": "ok", "ready": True})
        
        @self.app.route('/readiness')
        def readiness():
            return jsonify({"ready": True})
        
        @self.app.route('/liveness')
        def liveness():
            return jsonify({"alive": True})
    
    def run(self):
        """Run the ultra-minimal Cloud Run service - Single Port Optimized"""
        port = int(os.environ.get('PORT', 8080))
        
        logger.info(f"🚀 Ultra-minimal Cloud Run service starting on port {port}")
        logger.info("📊 Target: <300MB image, essential functionality only")
        
        # Run Flask server with Cloud Run optimizations
        self.app.run(
            host='0.0.0.0',
            port=port,
            debug=False,
            threaded=True,
            use_reloader=False
        )

def main():
    """Main entry point for ultra-minimal Cloud Run deployment"""
    
    print("=" * 60)
    print("ULTRA_PLUS_BOT - ULTRA-MINIMAL CLOUD RUN DEPLOYMENT")
    print("=" * 60)
    print(f"Start Time: {datetime.now().isoformat()}")
    print(f"Python: {sys.version}")
    print(f"Working Dir: {os.getcwd()}")
    print(f"Port: {os.environ.get('PORT', 8080)}")
    print("=" * 60)
    
    # Set environment
    os.environ['DEPLOYMENT_MODE'] = 'ultra_minimal'
    os.environ['PORT'] = str(os.environ.get('PORT', 8080))
    
    try:
        # Create and run ultra-minimal bot
        ultra_minimal_bot = UltraMinimalBot()
        ultra_minimal_bot.run()
        
    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()