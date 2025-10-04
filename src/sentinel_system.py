#!/usr/bin/env python3
"""
Main Project Sentinel retail analytics system.
Integrates all components to process streaming data and generate insights.
"""

import os
import sys
import logging
import time
import argparse
import json
from datetime import datetime
from pathlib import Path

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from streaming_client import StreamingClient
from data_parser import DataParser
from data_correlator import DataCorrelator
from detection_engine import DetectionEngine
from event_generator import EventGenerator

class SentinelSystem:
    """Main Project Sentinel system coordinator."""
    
    def __init__(self, data_root: str = None):
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.streaming_client = StreamingClient()
        self.data_parser = DataParser()
        self.data_correlator = DataCorrelator()
        self.detection_engine = DetectionEngine(self.data_correlator, self.data_parser)
        self.event_generator = EventGenerator()
        
        # Set data root
        if data_root is None:
            data_root = os.path.join(os.path.dirname(__file__), '..', 'data', 'input')
        self.data_root = data_root
        
        # Load reference data
        self._load_reference_data()
        
        # Register streaming callbacks
        self._setup_streaming_callbacks()
        
        # Global detection timer
        self.last_global_detection = datetime.now()
        self.global_detection_interval = 60  # seconds
    
    def _load_reference_data(self):
        """Load product and customer reference data."""
        try:
            products_path = os.path.join(self.data_root, 'products_list.csv')
            customers_path = os.path.join(self.data_root, 'customer_data.csv')
            
            if os.path.exists(products_path) and os.path.exists(customers_path):
                self.data_parser.load_reference_data(products_path, customers_path)
                self.logger.info("Reference data loaded successfully")
            else:
                self.logger.warning(f"Reference data files not found in {self.data_root}")
                
        except Exception as e:
            self.logger.error(f"Failed to load reference data: {e}")
    
    def _setup_streaming_callbacks(self):
        """Setup callbacks for different data streams."""
        # Use the exact dataset names from the streaming server
        self.streaming_client.register_callback('POS_Transactions', self._process_pos_transaction)
        self.streaming_client.register_callback('RFID_data', self._process_rfid_reading)
        self.streaming_client.register_callback('Queue_monitor', self._process_queue_monitoring)
        self.streaming_client.register_callback('Product_recognism', self._process_product_recognition)
        self.streaming_client.register_callback('Current_inventory_data', self._process_inventory_snapshot)
    
    def _process_pos_transaction(self, event):
        """Process POS transaction data."""
        try:
            parsed_data = self.data_parser.parse_streaming_event(event)
            if parsed_data:
                self.data_correlator.add_data(parsed_data)
                
                # Run detections for this station
                station_id = parsed_data.get('station_id')
                timestamp_str = parsed_data.get('timestamp')
                if station_id and timestamp_str:
                    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    self._run_station_detections(station_id, timestamp)
                    
                    # Add success operation if transaction is normal
                    if parsed_data.get('status') == 'Active':
                        self.event_generator.add_success_operation(
                            station_id,
                            parsed_data.get('customer_id', 'Unknown'),
                            parsed_data.get('sku', 'Unknown'),
                            timestamp
                        )
                
        except Exception as e:
            self.logger.error(f"Error processing POS transaction: {e}")
    
    def _process_rfid_reading(self, event):
        """Process RFID reading data."""
        try:
            parsed_data = self.data_parser.parse_streaming_event(event)
            if parsed_data:
                self.data_correlator.add_data(parsed_data)
                
                # Run detections for this station
                station_id = parsed_data.get('station_id')
                timestamp_str = parsed_data.get('timestamp')
                if station_id and timestamp_str:
                    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    self._run_station_detections(station_id, timestamp)
                
        except Exception as e:
            self.logger.error(f"Error processing RFID reading: {e}")
    
    def _process_queue_monitoring(self, event):
        """Process queue monitoring data."""
        try:
            parsed_data = self.data_parser.parse_streaming_event(event)
            if parsed_data:
                self.data_correlator.add_data(parsed_data)
                
                # Run detections for this station
                station_id = parsed_data.get('station_id')
                timestamp_str = parsed_data.get('timestamp')
                if station_id and timestamp_str:
                    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    self._run_station_detections(station_id, timestamp)
                
        except Exception as e:
            self.logger.error(f"Error processing queue monitoring: {e}")
    
    def _process_product_recognition(self, event):
        """Process product recognition data."""
        try:
            parsed_data = self.data_parser.parse_streaming_event(event)
            if parsed_data:
                self.data_correlator.add_data(parsed_data)
                
        except Exception as e:
            self.logger.error(f"Error processing product recognition: {e}")
    
    def _process_inventory_snapshot(self, event):
        """Process inventory snapshot data."""
        try:
            parsed_data = self.data_parser.parse_streaming_event(event)
            if parsed_data:
                self.data_correlator.add_data(parsed_data)
                
                # Run global detections
                timestamp_str = parsed_data.get('timestamp')
                if timestamp_str:
                    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    self._run_global_detections(timestamp)
                
        except Exception as e:
            self.logger.error(f"Error processing inventory snapshot: {e}")
    
    def _run_station_detections(self, station_id: str, timestamp: datetime):
        """Run detection algorithms for a specific station."""
        try:
            events = self.detection_engine.run_all_detections(station_id, timestamp)
            for event in events:
                self.event_generator.add_detection_result(event, timestamp)
                
        except Exception as e:
            self.logger.error(f"Error running station detections: {e}")
    
    def _run_global_detections(self, timestamp: datetime):
        """Run global detection algorithms periodically."""
        try:
            time_since_last = (timestamp - self.last_global_detection).total_seconds()
            if time_since_last >= self.global_detection_interval:
                events = self.detection_engine.run_global_detections(timestamp)
                for event in events:
                    self.event_generator.add_detection_result(event, timestamp)
                
                self.last_global_detection = timestamp
                
        except Exception as e:
            self.logger.error(f"Error running global detections: {e}")
    
    def start_real_time_processing(self, duration_seconds: int = None):
        """Start real-time processing of streaming data."""
        self.logger.info("Starting real-time processing...")
        
        if not self.streaming_client.start_streaming():
            self.logger.error("Failed to start streaming client")
            return False
        
        try:
            start_time = time.time()
            while True:
                if duration_seconds and (time.time() - start_time) > duration_seconds:
                    break
                
                time.sleep(1)  # Process for specified duration or until interrupted
                
                # Periodically run global detections
                current_time = datetime.now()
                self._run_global_detections(current_time)
                
        except KeyboardInterrupt:
            self.logger.info("Processing interrupted by user")
        finally:
            self.streaming_client.stop_streaming()
            self.logger.info("Stopped streaming client")
        
        return True
    
    def process_batch_data(self, input_dir: str):
        """Process batch data files for testing."""
        self.logger.info(f"Processing batch data from {input_dir}")
        
        # Process each JSONL file
        data_files = {
            'pos_transactions': 'pos_transactions.jsonl',
            'rfid_readings': 'rfid_readings.jsonl',
            'queue_monitoring': 'queue_monitoring.jsonl',
            'product_recognition': 'product_recognition.jsonl',
            'inventory_snapshots': 'inventory_snapshots.jsonl'
        }
        
        all_events = []
        
        for dataset_name, filename in data_files.items():
            filepath = os.path.join(input_dir, filename)
            if os.path.exists(filepath):
                self.logger.info(f"Processing {filename}")
                with open(filepath, 'r') as f:
                    for line in f:
                        if line.strip():
                            try:
                                data = json.loads(line)
                                # Create event format expected by parser
                                event = {
                                    'dataset': dataset_name,
                                    'payload': data
                                }
                                all_events.append(event)
                            except json.JSONDecodeError as e:
                                self.logger.warning(f"Failed to parse line in {filename}: {e}")
        
        # Sort events by timestamp
        def get_timestamp(event):
            try:
                payload = event.get('payload', {})
                timestamp_str = payload.get('timestamp', '')
                return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            except:
                return datetime.min
        
        all_events.sort(key=get_timestamp)
        
        # Process events in chronological order
        for event in all_events:
            dataset = event.get('dataset')
            if dataset == 'pos_transactions':
                self._process_pos_transaction(event)
            elif dataset == 'rfid_readings':
                self._process_rfid_reading(event)
            elif dataset == 'queue_monitoring':
                self._process_queue_monitoring(event)
            elif dataset == 'product_recognition':
                self._process_product_recognition(event)
            elif dataset == 'inventory_snapshots':
                self._process_inventory_snapshot(event)
        
        self.logger.info(f"Processed {len(all_events)} events")
    
    def save_events(self, output_path: str):
        """Save generated events to file."""
        self.event_generator.save_events(output_path)
        
        # Print summary
        summary = self.event_generator.get_event_summary()
        self.logger.info("Event Summary:")
        for event_type, count in summary.items():
            self.logger.info(f"  {event_type}: {count}")
    
    def get_dashboard_data(self):
        """Get current data for dashboard display."""
        try:
            stations = self.data_correlator.get_all_stations()
            dashboard_data = {
                'timestamp': datetime.now().isoformat(),
                'stations': {},
                'summary': {
                    'total_stations': len(stations),
                    'active_stations': 0,
                    'total_customers': 0,
                    'total_events': len(self.event_generator.get_events())
                }
            }
            
            for station_id in stations:
                status, last_activity = self.data_correlator.get_station_status(station_id)
                recent_queue = self.data_correlator.get_recent_data(station_id, 'queue_data', 1)
                
                customer_count = 0
                dwell_time = 0
                if recent_queue:
                    customer_count = recent_queue[-1].get('customer_count', 0)
                    dwell_time = recent_queue[-1].get('average_dwell_time', 0)
                
                dashboard_data['stations'][station_id] = {
                    'status': status,
                    'last_activity': last_activity.isoformat() if last_activity else None,
                    'customer_count': customer_count,
                    'average_dwell_time': dwell_time
                }
                
                if status == 'Active':
                    dashboard_data['summary']['active_stations'] += 1
                dashboard_data['summary']['total_customers'] += customer_count
            
            dashboard_data['recent_events'] = self.event_generator.get_events()[-10:]  # Last 10 events
            dashboard_data['event_summary'] = self.event_generator.get_event_summary()
            
            return dashboard_data
            
        except Exception as e:
            self.logger.error(f"Error getting dashboard data: {e}")
            return None


def main():
    """Main function for running the Sentinel system."""
    parser = argparse.ArgumentParser(description='Project Sentinel Retail Analytics System')
    parser.add_argument('--mode', choices=['real-time', 'batch'], default='batch',
                       help='Processing mode: real-time streaming or batch processing')
    parser.add_argument('--input-dir', default='../data/input',
                       help='Input directory for batch processing')
    parser.add_argument('--output-dir', default='../evidence/output/test',
                       help='Output directory for events.jsonl')
    parser.add_argument('--duration', type=int, default=60,
                       help='Duration for real-time processing (seconds)')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                       default='INFO', help='Logging level')
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize system
    system = SentinelSystem(args.input_dir)
    
    try:
        if args.mode == 'real-time':
            # Real-time processing
            system.start_real_time_processing(args.duration)
        else:
            # Batch processing
            system.process_batch_data(args.input_dir)
        
        # Save events
        os.makedirs(args.output_dir, exist_ok=True)
        output_path = os.path.join(args.output_dir, 'events.jsonl')
        system.save_events(output_path)
        
        print(f"\\nProcessing complete! Events saved to: {output_path}")
        
    except Exception as e:
        logging.error(f"System error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())