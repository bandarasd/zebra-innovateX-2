#!/usr/bin/env python3
"""
Project Sentinel - Run Demo Script

This script demonstrates the Project Sentinel system in both batch and streaming modes.
It processes retail data streams and generates events for suspicious activities.
"""

import sys
import os
import threading
import time
import logging
import subprocess
import signal
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sentinel_system import SentinelSystem
from dashboard import Dashboard

def run_batch_demo():
    """Run batch processing demo."""
    print("🚀 Starting Project Sentinel - Batch Processing Demo")
    print("=" * 60)
    
    # Initialize system
    system = SentinelSystem()
    
    # Process data
    print("📊 Processing data...")
    system.process_batch_data('data/input')
    
    # Save events
    output_path = 'data/output/events.jsonl'
    system.save_events(output_path)
    
    print("\n✅ Batch processing completed!")
    print(f"📄 Events generated in: {output_path}")
    
    # Show results
    events = system.event_generator.get_events()
    print(f"\n🔍 Generated {len(events)} events:")
    for event in events:
        event_name = event['event_data']['event_name']
        station_id = event['event_data']['station_id']
        print(f"  • {event['timestamp']}: {event_name} at {station_id}")

def run_streaming_demo():
    """Run streaming demo with dashboard."""
    print("🚀 Starting Project Sentinel - Streaming Demo")
    print("=" * 60)
    
    # Initialize system
    system = SentinelSystem()
    
    # Start dashboard server
    dashboard = Dashboard(system)
    dashboard.start()
    
    print("🌐 Dashboard server started at http://localhost:8080")
    print("📡 Starting streaming data processor...")
    
    try:
        # Start streaming processor (optional - dashboard works without it)
        system.start_real_time_processing()
    except KeyboardInterrupt:
        print("\n⏹️  Stopping Sentinel system...")
    finally:
        if 'dashboard' in locals():
            dashboard.stop()

def run_full_backend():
    """Run complete backend system with streaming server, client, and API."""
    print("🚀 Starting Project Sentinel - Full Backend System")
    print("=" * 60)
    
    processes = []
    
    try:
        # Get base directory
        base_dir = Path(__file__).parent.parent
        
        # Start streaming server
        print("📡 Starting streaming server...")
        streaming_server_path = base_dir / "data" / "streaming-server" / "stream_server.py"
        server_process = subprocess.Popen([
            sys.executable, str(streaming_server_path), 
            "--loop", "--speed", "1.0"
        ], cwd=str(streaming_server_path.parent))
        processes.append(("Streaming Server", server_process))
        
        # Wait for server to start
        time.sleep(3)
        
        # Start streaming client (optional demo)
        print("👥 Starting streaming client demo...")
        client_path = base_dir / "data" / "streaming-clients" / "client_example.py"
        client_process = subprocess.Popen([
            sys.executable, str(client_path), 
            "--limit", "0"  # Unlimited events
        ], cwd=str(client_path.parent))
        processes.append(("Streaming Client", client_process))
        
        # Wait a bit more
        time.sleep(2)
        
        # Start Python backend API
        print("🐍 Starting Python backend API...")
        dashboard_path = Path(__file__).parent / "streaming_dashboard.py"
        api_process = subprocess.Popen([
            sys.executable, str(dashboard_path)
        ], cwd=str(dashboard_path.parent))
        processes.append(("Backend API", api_process))
        
        print("\n" + "=" * 60)
        print("✅ Full Backend System Started!")
        print("=" * 60)
        print("🌐 Services Running:")
        print("  • Streaming Server: localhost:8765")
        print("  • Backend API: http://localhost:8081")
        print("  • API Endpoints:")
        print("    - http://localhost:8081/api/data")
        print("    - http://localhost:8081/api/events")
        print("  • Streaming Client: Displaying live data")
        print("  • Auto-saving events to test/events.json every 10 seconds")
        print("\n📊 React Frontend can be started with:")
        print("  cd ../dashboard && npm run dev")
        print("\n⏹️  Press Ctrl+C to stop all services...")
        
        # Wait for interrupt
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n⏹️  Shutting down all services...")
        
    finally:
        # Clean up all processes
        for name, process in processes:
            try:
                print(f"🛑 Stopping {name}...")
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print(f"🔥 Force killing {name}...")
                process.kill()
            except Exception as e:
                print(f"⚠️  Error stopping {name}: {e}")
        
        print("✅ All services stopped!")

def main():
    """Main entry point."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print("No mode specified, defaulting to 'full' (complete backend)")
        print("Available modes:")
        print("  python run_demo.py batch     - Process data in batch mode")
        print("  python run_demo.py streaming - Start streaming mode with dashboard")
        print("  python run_demo.py full      - Start complete backend (streaming server + client + API)")
        print()
        mode = 'full'
    else:
        mode = sys.argv[1].lower()
    
    if mode == 'batch':
        run_batch_demo()
    elif mode == 'streaming':
        run_streaming_demo()
    elif mode == 'full':
        run_full_backend()
    else:
        print(f"Unknown mode: {mode}")
        print("Use 'batch', 'streaming', or 'full'")
        sys.exit(1)

if __name__ == "__main__":
    main()