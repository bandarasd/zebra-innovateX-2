#!/usr/bin/env python3
"""
Streaming dashboard for Project Sentinel.
Connects to running sentinel system and serves API data for React frontend.
"""

import json
import logging
import threading
import time
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from sentinel_system import SentinelSystem

# Global sentinel system instance
sentinel_system = None

class StreamingDashboardHandler(BaseHTTPRequestHandler):
    """HTTP handler for the streaming dashboard API."""
    
    def do_GET(self):
        """Handle GET requests."""
        try:
            parsed_path = urlparse(self.path)
            
            if parsed_path.path == '/':
                self._serve_info()
            elif parsed_path.path == '/api/data':
                self._serve_api_data()
            elif parsed_path.path == '/api/events':
                self._serve_events()
            else:
                self._serve_404()
                
        except Exception as e:
            logging.error(f"Dashboard error: {e}")
            self._serve_error()
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _serve_info(self):
        """Serve basic info about the API."""
        info = {
            'name': 'Project Sentinel Streaming API',
            'version': '1.0',
            'endpoints': [
                '/api/data - Dashboard data',
                '/api/events - Recent events'
            ],
            'status': 'running',
            'timestamp': datetime.now().isoformat()
        }
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(info, indent=2).encode('utf-8'))
    
    def _serve_api_data(self):
        """Serve API data for dashboard."""
        try:
            global sentinel_system
            if sentinel_system:
                data = sentinel_system.get_dashboard_data()
            else:
                data = {
                    'timestamp': datetime.now().isoformat(),
                    'stations': {},
                    'summary': {
                        'total_stations': 0, 
                        'active_stations': 0, 
                        'total_customers': 0, 
                        'total_events': 0
                    },
                    'recent_events': [],
                    'event_summary': {}
                }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps(data, default=str).encode('utf-8'))
            
        except Exception as e:
            logging.error(f"API data error: {e}")
            self._serve_error()
    
    def _serve_events(self):
        """Serve recent events API."""
        try:
            global sentinel_system
            if sentinel_system:
                events = sentinel_system.event_generator.get_events()[-50:]  # Last 50 events
            else:
                events = []
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(events, default=str).encode('utf-8'))
            
        except Exception as e:
            logging.error(f"Events API error: {e}")
            self._serve_error()
    
    def _serve_404(self):
        """Serve 404 error."""
        self.send_response(404)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b'404 Not Found')
    
    def _serve_error(self):
        """Serve 500 error."""
        self.send_response(500)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b'500 Internal Server Error')

def start_dashboard_server(port=8081):
    """Start the dashboard server."""
    try:
        server = HTTPServer(('localhost', port), StreamingDashboardHandler)
        print(f"🌐 Streaming Dashboard API started at http://localhost:{port}")
        print(f"📊 API Endpoints:")
        print(f"  • http://localhost:{port}/api/data - Dashboard data")
        print(f"  • http://localhost:{port}/api/events - Recent events")
        print("Press Ctrl+C to stop...")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\\n⏹️ Dashboard server stopped")
    except Exception as e:
        print(f"❌ Dashboard server error: {e}")

def connect_to_sentinel():
    """Try to connect to running sentinel system or create a new one."""
    global sentinel_system
    
    # For now, create a new system that will connect to the streaming server
    try:
        print("🔗 Creating sentinel system connection...")
        sentinel_system = SentinelSystem()
        
        # Start streaming in background
        def start_streaming():
            try:
                sentinel_system.start_real_time_processing()
            except Exception as e:
                logging.error(f"Streaming error: {e}")
        
        # Start periodic event saving
        def save_events_periodically():
            import os
            while True:
                try:
                    time.sleep(10)  # Save every 10 seconds
                    if sentinel_system and sentinel_system.event_generator:
                        # Save to test/events.json
                        test_events_path = "/Users/dananjaya/Downloads/zebra/submission-structure/Team##_sentinel/evidence/output/test/events.json"
                        sentinel_system.event_generator.save_events_json(test_events_path)
                        
                        # Also save to other output directories for compatibility
                        output_paths = [
                            "/Users/dananjaya/Downloads/zebra/data/output/events.json",
                            "/Users/dananjaya/Downloads/zebra/evidence/output/test/events.json",
                            "/Users/dananjaya/Downloads/zebra/evidence/output/final/events.json"
                        ]
                        
                        for path in output_paths:
                            try:
                                os.makedirs(os.path.dirname(path), exist_ok=True)
                                sentinel_system.event_generator.save_events_json(path)
                            except Exception as e:
                                logging.debug(f"Could not save to {path}: {e}")
                                
                except Exception as e:
                    logging.error(f"Error saving events: {e}")
        
        streaming_thread = threading.Thread(target=start_streaming, daemon=True)
        streaming_thread.start()
        
        # Start event saving thread
        save_thread = threading.Thread(target=save_events_periodically, daemon=True)
        save_thread.start()
        
        print("✅ Connected to sentinel system")
        print("📁 Auto-saving events to test/events.json every 10 seconds")
        return True
    except Exception as e:
        print(f"❌ Failed to connect to sentinel system: {e}")
        return False

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🚀 Starting Project Sentinel Streaming Dashboard")
    print("=" * 50)
    
    # Connect to sentinel system
    if connect_to_sentinel():
        # Give it a moment to start processing
        time.sleep(2)
        
        # Start dashboard server
        start_dashboard_server(port=8081)
    else:
        print("❌ Could not start dashboard - sentinel system unavailable")