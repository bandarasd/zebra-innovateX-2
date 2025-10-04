#!/usr/bin/env python3
"""
Debug dashboard to see what's causing it to crash.
"""

import sys
import os
import logging

# Add the src directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sentinel_system import SentinelSystem
from dashboard import Dashboard

def main():
    """Run dashboard with debug logging."""
    # Enable debug logging
    logging.basicConfig(level=logging.DEBUG)
    
    print("🚀 Debug Dashboard Demo")
    print("=" * 30)
    
    # Initialize system
    system = SentinelSystem()
    print("✅ System initialized")
    
    # Process some data
    system.process_batch_data('data/input')
    system.save_events('data/output/events.jsonl')
    print("✅ Data processed")
    
    # Test get_dashboard_data method
    try:
        data = system.get_dashboard_data()
        print(f"✅ Dashboard data: {len(str(data))} chars")
    except Exception as e:
        print(f"❌ Error getting dashboard data: {e}")
        return
    
    # Start dashboard
    dashboard = Dashboard(system)
    if dashboard.start():
        print("✅ Dashboard started")
        
        # Test the API manually
        print("Testing API manually...")
        import requests
        try:
            response = requests.get('http://localhost:8080/api/data', timeout=5)
            print(f"✅ API response: {response.status_code}")
        except Exception as e:
            print(f"❌ API request failed: {e}")
        
        dashboard.stop()
    else:
        print("❌ Failed to start dashboard")

if __name__ == "__main__":
    main()