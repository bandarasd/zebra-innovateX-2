#!/usr/bin/env python3
"""
Simple dashboard demo without streaming for testing React frontend.
"""

import sys
import os
import threading
import time
import signal

# Add the src directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sentinel_system import SentinelSystem
from dashboard import Dashboard

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    print('\n⏹️  Stopping dashboard...')
    sys.exit(0)

def main():
    """Run dashboard with existing data."""
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    print("🚀 Starting Project Sentinel Dashboard Demo")
    print("=" * 50)
    
    # Initialize system and process batch data to have some events
    system = SentinelSystem()
    system.process_batch_data('data/input')
    system.save_events('data/output/events.jsonl')
    
    # Start dashboard
    dashboard = Dashboard(system)
    if dashboard.start():
        print("🌐 Dashboard running at http://localhost:8080")
        print("📊 API endpoint: http://localhost:8080/api/data")
        print("⏹️  Press Ctrl+C to stop")
        
        try:
            # Keep the main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⏹️  Stopping dashboard...")
            dashboard.stop()
    else:
        print("❌ Failed to start dashboard")

if __name__ == "__main__":
    main()