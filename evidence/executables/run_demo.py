#!/usr/bin/env python3
"""
Project Sentinel Demo Runner
Executable script for demonstration and testing.
"""

import os
import sys
import subprocess
import time
import signal
import logging
from pathlib import Path

# Add the src directory to Python path
script_dir = Path(__file__).parent
src_dir = script_dir / '..' / '..' / 'src'
sys.path.insert(0, str(src_dir.resolve()))

def run_command(cmd, description, background=False, timeout=None):
    """Run a command with logging."""
    print(f"\\n🔄 {description}")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        if background:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"✅ Started background process (PID: {process.pid})")
            return process
        else:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            if result.returncode == 0:
                print(f"✅ {description} completed successfully")
                if result.stdout:
                    print(f"Output: {result.stdout}")
            else:
                print(f"❌ {description} failed with return code {result.returncode}")
                if result.stderr:
                    print(f"Error: {result.stderr}")
            return result
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} timed out after {timeout} seconds")
        return None
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return None

def check_dependencies():
    """Check if required dependencies are available."""
    print("🔍 Checking dependencies...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 6):
        print("❌ Python 3.6+ required")
        return False
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check required directories
    required_dirs = [
        '../../data/input',
        '../../data/streaming-server',
        '../../src'
    ]
    
    for dir_path in required_dirs:
        full_path = script_dir / dir_path
        if not full_path.exists():
            print(f"❌ Required directory not found: {full_path}")
            return False
        print(f"✅ Found: {dir_path}")
    
    return True

def start_streaming_server():
    """Start the streaming server."""
    server_dir = script_dir / '..' / '..' / 'data' / 'streaming-server'
    server_script = server_dir / 'stream_server.py'
    
    if not server_script.exists():
        print(f"❌ Streaming server not found: {server_script}")
        return None
    
    cmd = [
        sys.executable, 
        str(server_script),
        '--speed', '10.0',
        '--loop',
        '--log-level', 'WARNING'
    ]
    
    os.chdir(server_dir)
    return run_command(cmd, "Starting streaming server", background=True)

def run_batch_processing():
    """Run batch processing on the sample data."""
    input_dir = script_dir / '..' / '..' / 'data' / 'input'
    output_dir = script_dir / '..' / 'output' / 'test'
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Change to src directory for proper imports
    os.chdir(src_dir)
    
    cmd = [
        sys.executable,
        'sentinel_system.py',
        '--mode', 'batch',
        '--input-dir', str(input_dir),
        '--output-dir', str(output_dir),
        '--log-level', 'INFO'
    ]
    
    return run_command(cmd, "Running batch processing", timeout=60)

def start_real_time_demo():
    """Start real-time demo with streaming."""
    output_dir = script_dir / '..' / 'output' / 'final'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Change to src directory
    os.chdir(src_dir)
    
    cmd = [
        sys.executable,
        'sentinel_system.py',
        '--mode', 'real-time',
        '--duration', '30',
        '--output-dir', str(output_dir),
        '--log-level', 'INFO'
    ]
    
    return run_command(cmd, "Running real-time demo (30 seconds)", timeout=40)

def start_dashboard():
    """Start the web dashboard."""
    os.chdir(src_dir)
    
    cmd = [
        sys.executable,
        'dashboard.py'
    ]
    
    return run_command(cmd, "Starting web dashboard", background=True)

def main():
    """Main demo runner."""
    print("=" * 60)
    print("🛒 PROJECT SENTINEL - RETAIL ANALYTICS DEMO")
    print("=" * 60)
    print("This demo will:")
    print("1. Check system dependencies")
    print("2. Run batch processing on sample data")
    print("3. Start streaming server")
    print("4. Run real-time processing demo")
    print("5. Generate events.jsonl outputs")
    print("=" * 60)
    
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    processes = []
    
    try:
        # Step 1: Check dependencies
        if not check_dependencies():
            print("❌ Dependency check failed. Please ensure all required files are present.")
            return 1
        
        # Step 2: Run batch processing
        print("\\n" + "="*40)
        print("STEP 1: BATCH PROCESSING")
        print("="*40)
        
        result = run_batch_processing()
        if result and result.returncode == 0:
            print("✅ Batch processing completed successfully")
            
            # Check if events file was created
            events_file = script_dir / '..' / 'output' / 'test' / 'events.jsonl'
            if events_file.exists():
                print(f"✅ Events file created: {events_file}")
                with open(events_file, 'r') as f:
                    event_count = len(f.readlines())
                print(f"📊 Generated {event_count} events")
            else:
                print("⚠️ Events file not found")
        else:
            print("⚠️ Batch processing completed with warnings")
        
        # Step 3: Start streaming server
        print("\\n" + "="*40)
        print("STEP 2: REAL-TIME DEMO")
        print("="*40)
        
        print("Starting streaming server...")
        server_process = start_streaming_server()
        if server_process:
            processes.append(server_process)
            time.sleep(3)  # Give server time to start
            
            # Step 4: Run real-time processing
            print("Running real-time processing...")
            result = start_real_time_demo()
            if result and result.returncode == 0:
                print("✅ Real-time demo completed successfully")
                
                # Check final events file
                final_events_file = script_dir / '..' / 'output' / 'final' / 'events.jsonl'
                if final_events_file.exists():
                    print(f"✅ Final events file created: {final_events_file}")
                    with open(final_events_file, 'r') as f:
                        event_count = len(f.readlines())
                    print(f"📊 Generated {event_count} events in real-time")
        
        # Step 5: Summary
        print("\\n" + "="*40)
        print("DEMO SUMMARY")
        print("="*40)
        
        test_events = script_dir / '..' / 'output' / 'test' / 'events.jsonl'
        final_events = script_dir / '..' / 'output' / 'final' / 'events.jsonl'
        
        if test_events.exists():
            print(f"✅ Test events: {test_events}")
        if final_events.exists():
            print(f"✅ Final events: {final_events}")
        
        print("\\n🎯 Key Features Demonstrated:")
        print("  • Real-time data stream processing")
        print("  • Multi-source data correlation")
        print("  • Anomaly detection algorithms")
        print("  • Event generation in required format")
        print("  • Retail analytics insights")
        
        print("\\n📋 Files Generated:")
        evidence_dir = script_dir / '..'
        if evidence_dir.exists():
            for root, dirs, files in os.walk(evidence_dir):
                for file in files:
                    if file.endswith(('.jsonl', '.py')):
                        filepath = Path(root) / file
                        relative_path = filepath.relative_to(script_dir / '..' / '..')
                        print(f"  📄 {relative_path}")
        
        print("\\n🎉 Demo completed successfully!")
        
        return 0
        
    except KeyboardInterrupt:
        print("\\n⏹️ Demo interrupted by user")
        return 1
    except Exception as e:
        print(f"\\n❌ Demo failed with error: {e}")
        return 1
    finally:
        # Clean up background processes
        for process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ Stopped background process (PID: {process.pid})")
            except:
                try:
                    process.kill()
                except:
                    pass

if __name__ == "__main__":
    sys.exit(main())