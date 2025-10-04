#!/usr/bin/env python3
"""
Simple web dashboard for Project Sentinel.
Displays real-time store status and events.
"""

import json
import threading
import time
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import logging

class DashboardHandler(BaseHTTPRequestHandler):
    """HTTP handler for the dashboard web interface."""
    
    def do_GET(self):
        """Handle GET requests."""
        try:
            parsed_path = urlparse(self.path)
            
            if parsed_path.path == '/':
                self._serve_dashboard()
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
    
    def _serve_dashboard(self):
        """Serve the main dashboard HTML."""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Sentinel - Retail Analytics Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .card h3 {
            margin-top: 0;
            color: #333;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }
        .metric:last-child {
            border-bottom: none;
        }
        .metric-value {
            font-weight: bold;
            font-size: 1.2em;
        }
        .status-active { color: #28a745; }
        .status-error { color: #dc3545; }
        .status-warning { color: #ffc107; }
        .event-list {
            max-height: 400px;
            overflow-y: auto;
        }
        .event-item {
            padding: 10px;
            margin: 5px 0;
            border-left: 4px solid #007bff;
            background: #f8f9fa;
            border-radius: 5px;
        }
        .event-high { border-left-color: #dc3545; }
        .event-medium { border-left-color: #ffc107; }
        .event-low { border-left-color: #28a745; }
        .timestamp {
            font-size: 0.8em;
            color: #666;
        }
        .station-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 10px;
        }
        .station-card {
            padding: 15px;
            border-radius: 8px;
            border: 2px solid #ddd;
        }
        .station-active { border-color: #28a745; background: #f8fff8; }
        .station-error { border-color: #dc3545; background: #fff8f8; }
        .station-inactive { border-color: #6c757d; background: #f8f9fa; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🛒 Project Sentinel Dashboard</h1>
        <p>Real-time Retail Analytics & Optimization</p>
        <div id="last-update">Last updated: <span id="timestamp">--</span></div>
    </div>

    <div class="grid">
        <div class="card">
            <h3>📊 Store Overview</h3>
            <div class="metric">
                <span>Total Stations:</span>
                <span class="metric-value" id="total-stations">--</span>
            </div>
            <div class="metric">
                <span>Active Stations:</span>
                <span class="metric-value status-active" id="active-stations">--</span>
            </div>
            <div class="metric">
                <span>Total Customers:</span>
                <span class="metric-value" id="total-customers">--</span>
            </div>
            <div class="metric">
                <span>Total Events:</span>
                <span class="metric-value" id="total-events">--</span>
            </div>
        </div>

        <div class="card">
            <h3>🎯 Event Summary</h3>
            <div id="event-summary">
                <div class="metric">
                    <span>Scanner Avoidance:</span>
                    <span class="metric-value status-error" id="scanner-avoidance">0</span>
                </div>
                <div class="metric">
                    <span>Barcode Switching:</span>
                    <span class="metric-value status-error" id="barcode-switching">0</span>
                </div>
                <div class="metric">
                    <span>Weight Discrepancies:</span>
                    <span class="metric-value status-warning" id="weight-discrepancies">0</span>
                </div>
                <div class="metric">
                    <span>System Crashes:</span>
                    <span class="metric-value status-error" id="system-crashes">0</span>
                </div>
                <div class="metric">
                    <span>Queue Issues:</span>
                    <span class="metric-value status-warning" id="queue-issues">0</span>
                </div>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="card">
            <h3>🏪 Station Status</h3>
            <div class="station-grid" id="station-status">
                <div class="station-card station-inactive">
                    <strong>Loading...</strong><br>
                    <small>Connecting to system...</small>
                </div>
            </div>
        </div>

        <div class="card">
            <h3>📋 Recent Events</h3>
            <div class="event-list" id="recent-events">
                <div class="event-item">
                    <strong>System Starting</strong><br>
                    <small class="timestamp">Initializing dashboard...</small>
                </div>
            </div>
        </div>
    </div>

    <script>
        let eventCount = 0;

        function updateDashboard() {
            fetch('/api/data')
                .then(response => response.json())
                .then(data => {
                    // Update timestamp
                    document.getElementById('timestamp').textContent = new Date(data.timestamp).toLocaleString();
                    
                    // Update summary metrics
                    document.getElementById('total-stations').textContent = data.summary.total_stations;
                    document.getElementById('active-stations').textContent = data.summary.active_stations;
                    document.getElementById('total-customers').textContent = data.summary.total_customers;
                    document.getElementById('total-events').textContent = data.summary.total_events;
                    
                    // Update event summary
                    const eventSummary = data.event_summary || {};
                    document.getElementById('scanner-avoidance').textContent = eventSummary['Scanner Avoidance'] || 0;
                    document.getElementById('barcode-switching').textContent = eventSummary['Barcode Switching'] || 0;
                    document.getElementById('weight-discrepancies').textContent = eventSummary['Weight Discrepancies'] || 0;
                    document.getElementById('system-crashes').textContent = eventSummary['Unexpected Systems Crash'] || 0;
                    
                    const queueIssues = (eventSummary['Long Queue Length'] || 0) + (eventSummary['Long Wait Time'] || 0);
                    document.getElementById('queue-issues').textContent = queueIssues;
                    
                    // Update station status
                    updateStationStatus(data.stations);
                    
                    // Update recent events
                    updateRecentEvents(data.recent_events);
                })
                .catch(error => {
                    console.error('Error updating dashboard:', error);
                    document.getElementById('timestamp').textContent = 'Error connecting to system';
                });
        }

        function updateStationStatus(stations) {
            const container = document.getElementById('station-status');
            container.innerHTML = '';
            
            for (const [stationId, stationData] of Object.entries(stations)) {
                const stationCard = document.createElement('div');
                stationCard.className = 'station-card';
                
                let statusClass = 'station-inactive';
                let statusText = 'Inactive';
                
                if (stationData.status === 'Active') {
                    statusClass = 'station-active';
                    statusText = 'Active';
                } else if (stationData.status === 'System Crash' || stationData.status === 'Read Error') {
                    statusClass = 'station-error';
                    statusText = 'Error';
                }
                
                stationCard.className += ' ' + statusClass;
                
                stationCard.innerHTML = `
                    <strong>${stationId}</strong><br>
                    <small>Status: ${statusText}</small><br>
                    <small>Customers: ${stationData.customer_count}</small><br>
                    <small>Wait: ${Math.round(stationData.average_dwell_time)}s</small>
                `;
                
                container.appendChild(stationCard);
            }
        }

        function updateRecentEvents(events) {
            const container = document.getElementById('recent-events');
            
            if (events && events.length > 0) {
                // Only show new events to avoid flicker
                const newEvents = events.slice(eventCount);
                eventCount = events.length;
                
                for (const event of newEvents) {
                    const eventItem = document.createElement('div');
                    eventItem.className = 'event-item';
                    
                    const eventName = event.event_data.event_name;
                    let priority = 'event-low';
                    
                    if (['Scanner Avoidance', 'Barcode Switching', 'Unexpected Systems Crash'].includes(eventName)) {
                        priority = 'event-high';
                    } else if (['Weight Discrepancies', 'Long Queue Length', 'Long Wait Time'].includes(eventName)) {
                        priority = 'event-medium';
                    }
                    
                    eventItem.className += ' ' + priority;
                    
                    eventItem.innerHTML = `
                        <strong>${eventName}</strong><br>
                        <small>Station: ${event.event_data.station_id || 'N/A'}</small><br>
                        <small class="timestamp">${new Date(event.timestamp).toLocaleString()}</small>
                    `;
                    
                    container.insertBefore(eventItem, container.firstChild);
                }
                
                // Keep only last 20 events
                while (container.children.length > 20) {
                    container.removeChild(container.lastChild);
                }
            }
        }

        // Update dashboard every 2 seconds
        setInterval(updateDashboard, 2000);
        updateDashboard(); // Initial load
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def _serve_api_data(self):
        """Serve API data for dashboard."""
        try:
            # Get data from the global system instance
            if hasattr(self.server, 'sentinel_system'):
                data = self.server.sentinel_system.get_dashboard_data()
            else:
                data = {
                    'timestamp': datetime.now().isoformat(),
                    'stations': {},
                    'summary': {'total_stations': 0, 'active_stations': 0, 'total_customers': 0, 'total_events': 0},
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
            if hasattr(self.server, 'sentinel_system'):
                events = self.server.sentinel_system.event_generator.get_events()[-50:]  # Last 50 events
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
        self.end_headers()
        self.wfile.write(b'404 Not Found')
    
    def _serve_error(self):
        """Serve 500 error."""
        self.send_response(500)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'500 Internal Server Error')
    
    def log_message(self, format, *args):
        """Override to reduce log spam."""
        pass


class Dashboard:
    """Web dashboard for Project Sentinel."""
    
    def __init__(self, sentinel_system, port=8080):
        self.sentinel_system = sentinel_system
        self.port = port
        self.server = None
        self.server_thread = None
        self.logger = logging.getLogger(__name__)
    
    def start(self):
        """Start the dashboard web server."""
        try:
            self.server = HTTPServer(('localhost', self.port), DashboardHandler)
            self.server.sentinel_system = self.sentinel_system
            
            self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.server_thread.start()
            
            self.logger.info(f"Dashboard started at http://localhost:{self.port}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start dashboard: {e}")
            return False
    
    def stop(self):
        """Stop the dashboard web server."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.logger.info("Dashboard stopped")


if __name__ == "__main__":
    # Simple test
    from sentinel_system import SentinelSystem
    
    logging.basicConfig(level=logging.INFO)
    
    system = SentinelSystem()
    dashboard = Dashboard(system)
    
    if dashboard.start():
        print("Dashboard running at http://localhost:8080")
        print("Press Ctrl+C to stop...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            dashboard.stop()
    else:
        print("Failed to start dashboard")