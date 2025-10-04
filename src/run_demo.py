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

def main():
    """Main entry point."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python run_demo.py [batch|streaming]")
        print("  batch     - Process data in batch mode")
        print("  streaming - Start streaming mode with dashboard")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    if mode == 'batch':
        run_batch_demo()
    elif mode == 'streaming':
        run_streaming_demo()
    else:
        print(f"Unknown mode: {mode}")
        print("Use 'batch' or 'streaming'")
        sys.exit(1)

if __name__ == "__main__":
    main()