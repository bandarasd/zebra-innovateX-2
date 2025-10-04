#!/usr/bin/env python3
"""
Test script to verify Project Sentinel backend-frontend integration.
"""

import requests
import json
import time
from datetime import datetime

def test_backend_api():
    """Test the backend API endpoint."""
    print("🧪 Testing Project Sentinel Backend API Integration")
    print("=" * 60)
    
    try:
        # Test API endpoint
        print("📡 Testing API endpoint: http://localhost:8080/api/data")
        response = requests.get("http://localhost:8080/api/data", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Response successful!")
            print(f"📊 Timestamp: {data.get('timestamp', 'N/A')}")
            print(f"🏪 Total Stations: {data.get('summary', {}).get('total_stations', 0)}")
            print(f"🟢 Active Stations: {data.get('summary', {}).get('active_stations', 0)}")
            print(f"👥 Total Customers: {data.get('summary', {}).get('total_customers', 0)}")
            print(f"⚠️  Total Events: {data.get('summary', {}).get('total_events', 0)}")
            
            # Show recent events
            events = data.get('recent_events', [])
            print(f"\n📋 Recent Events ({len(events)}):")
            for i, event in enumerate(events[:3], 1):
                event_data = event.get('event_data', {})
                print(f"  {i}. {event_data.get('event_name', 'Unknown')} at {event_data.get('station_id', 'Unknown')}")
            
            # Show event summary
            event_summary = data.get('event_summary', {})
            print(f"\n📈 Event Summary:")
            for event_type, count in event_summary.items():
                print(f"  • {event_type}: {count}")
            
            print(f"\n🔄 CORS Headers: {'Access-Control-Allow-Origin' in response.headers}")
            print(f"📝 Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
            
            return True
            
        else:
            print(f"❌ API request failed with status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Failed to connect to backend API")
        print("💡 Make sure the Python backend is running on port 8080")
        return False
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def test_frontend_accessibility():
    """Test if the frontend is accessible."""
    print(f"\n🌐 Testing Frontend Accessibility")
    print("-" * 40)
    
    try:
        # Test frontend endpoint
        print("📱 Testing frontend: http://localhost:5175")
        response = requests.get("http://localhost:5175", timeout=5)
        
        if response.status_code == 200:
            print("✅ Frontend is accessible!")
            print(f"📝 Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
            return True
        else:
            print(f"❌ Frontend request failed with status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Failed to connect to frontend")
        print("💡 Make sure the React dashboard is running on port 5175")
        return False
    except Exception as e:
        print(f"❌ Error testing frontend: {e}")
        return False

def main():
    """Run all integration tests."""
    print(f"🚀 Project Sentinel Integration Test")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    backend_ok = test_backend_api()
    frontend_ok = test_frontend_accessibility()
    
    print(f"\n📊 Integration Test Results:")
    print("-" * 30)
    print(f"Backend API:  {'✅ PASS' if backend_ok else '❌ FAIL'}")
    print(f"Frontend:     {'✅ PASS' if frontend_ok else '❌ FAIL'}")
    print(f"Integration:  {'✅ SUCCESS' if backend_ok and frontend_ok else '❌ ISSUES'}")
    
    if backend_ok and frontend_ok:
        print(f"\n🎉 Full stack integration successful!")
        print(f"🌐 Frontend: http://localhost:5175")
        print(f"📡 Backend API: http://localhost:8080/api/data")
        print(f"📊 Python Dashboard: http://localhost:8080")
    else:
        print(f"\n⚠️  Integration issues detected. Check the services above.")

if __name__ == "__main__":
    main()