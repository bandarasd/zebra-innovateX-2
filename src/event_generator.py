#!/usr/bin/env python3
"""
Event generator for Project Sentinel.
Generates events.jsonl output in the required format.
"""

import json
from datetime import datetime
from typing import Dict, List, Any
import logging

class EventGenerator:
    """Generates events in the required JSON format for submission."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.event_counter = 0
        self.events: List[Dict] = []
    
    def add_event(self, event_data: Dict[str, Any], timestamp: datetime = None):
        """Add an event to the events list."""
        if timestamp is None:
            timestamp = datetime.now()
        
        # Generate event ID
        event_id = f"E{self.event_counter:03d}"
        self.event_counter += 1
        
        # Create event in required format
        event = {
            "timestamp": timestamp.isoformat() if isinstance(timestamp, datetime) else timestamp,
            "event_id": event_id,
            "event_data": event_data
        }
        
        self.events.append(event)
        self.logger.debug(f"Added event {event_id}: {event_data.get('event_name', 'Unknown')}")
    
    def add_success_operation(self, station_id: str, customer_id: str, product_sku: str, timestamp: datetime):
        """Add a successful operation event."""
        event_data = {
            "event_name": "Success Operation",
            "station_id": station_id,
            "customer_id": customer_id,
            "product_sku": product_sku
        }
        self.add_event(event_data, timestamp)
    
    def add_scanner_avoidance(self, station_id: str, customer_id: str, product_sku: str, timestamp: datetime):
        """Add a scanner avoidance event."""
        event_data = {
            "event_name": "Scanner Avoidance",
            "station_id": station_id,
            "customer_id": customer_id,
            "product_sku": product_sku
        }
        self.add_event(event_data, timestamp)
    
    def add_barcode_switching(self, station_id: str, customer_id: str, actual_sku: str, scanned_sku: str, timestamp: datetime):
        """Add a barcode switching event."""
        event_data = {
            "event_name": "Barcode Switching",
            "station_id": station_id,
            "customer_id": customer_id,
            "actual_sku": actual_sku,
            "scanned_sku": scanned_sku
        }
        self.add_event(event_data, timestamp)
    
    def add_weight_discrepancy(self, station_id: str, customer_id: str, product_sku: str, 
                              expected_weight: float, actual_weight: float, timestamp: datetime):
        """Add a weight discrepancy event."""
        event_data = {
            "event_name": "Weight Discrepancies",
            "station_id": station_id,
            "customer_id": customer_id,
            "product_sku": product_sku,
            "expected_weight": expected_weight,
            "actual_weight": actual_weight
        }
        self.add_event(event_data, timestamp)
    
    def add_system_crash(self, station_id: str, duration_seconds: int, timestamp: datetime):
        """Add a system crash event."""
        event_data = {
            "event_name": "Unexpected Systems Crash",
            "station_id": station_id,
            "duration_seconds": duration_seconds
        }
        self.add_event(event_data, timestamp)
    
    def add_long_wait_time(self, station_id: str, customer_id: str, wait_time_seconds: int, timestamp: datetime):
        """Add a long wait time event."""
        event_data = {
            "event_name": "Long Wait Time",
            "station_id": station_id,
            "customer_id": customer_id,
            "wait_time_seconds": wait_time_seconds
        }
        self.add_event(event_data, timestamp)
    
    def add_long_queue_length(self, station_id: str, num_customers: int, timestamp: datetime):
        """Add a long queue length event."""
        event_data = {
            "event_name": "Long Queue Length",
            "station_id": station_id,
            "num_of_customers": num_customers
        }
        self.add_event(event_data, timestamp)
    
    def add_staffing_needs(self, station_id: str, staff_type: str, timestamp: datetime):
        """Add a staffing needs event."""
        event_data = {
            "event_name": "Staffing Needs",
            "station_id": station_id,
            "Staff_type": staff_type
        }
        self.add_event(event_data, timestamp)
    
    def add_checkout_station_action(self, station_id: str, action: str, timestamp: datetime):
        """Add a checkout station action event."""
        event_data = {
            "event_name": "Checkout Station Action",
            "station_id": station_id,
            "Action": action
        }
        self.add_event(event_data, timestamp)
    
    def add_inventory_discrepancy(self, sku: str, expected_inventory: int, actual_inventory: int, timestamp: datetime):
        """Add an inventory discrepancy event."""
        event_data = {
            "event_name": "Inventory Discrepancy",
            "SKU": sku,
            "Expected_Inventory": expected_inventory,
            "Actual_Inventory": actual_inventory
        }
        self.add_event(event_data, timestamp)
    
    def add_detection_result(self, detection_result: Dict[str, Any], timestamp: datetime = None):
        """Add a detection result as an event."""
        if not detection_result:
            return
        
        # Map detection results to the proper event format
        event_name = detection_result.get('event_name')
        
        if event_name == 'Scanner Avoidance':
            self.add_scanner_avoidance(
                detection_result.get('station_id'),
                detection_result.get('customer_id', 'Unknown'),
                detection_result.get('product_sku'),
                timestamp or datetime.now()
            )
        elif event_name == 'Barcode Switching':
            self.add_barcode_switching(
                detection_result.get('station_id'),
                detection_result.get('customer_id', 'Unknown'),
                detection_result.get('actual_sku'),
                detection_result.get('scanned_sku'),
                timestamp or datetime.now()
            )
        elif event_name == 'Weight Discrepancies':
            self.add_weight_discrepancy(
                detection_result.get('station_id'),
                detection_result.get('customer_id', 'Unknown'),
                detection_result.get('product_sku'),
                detection_result.get('expected_weight'),
                detection_result.get('actual_weight'),
                timestamp or datetime.now()
            )
        elif event_name == 'Unexpected Systems Crash':
            self.add_system_crash(
                detection_result.get('station_id'),
                detection_result.get('duration_seconds', 0),
                timestamp or datetime.now()
            )
        elif event_name == 'Long Wait Time':
            self.add_long_wait_time(
                detection_result.get('station_id'),
                detection_result.get('customer_id', 'Unknown'),
                detection_result.get('wait_time_seconds'),
                timestamp or datetime.now()
            )
        elif event_name == 'Long Queue Length':
            self.add_long_queue_length(
                detection_result.get('station_id'),
                detection_result.get('num_of_customers'),
                timestamp or datetime.now()
            )
        elif event_name == 'Staffing Needs':
            self.add_staffing_needs(
                detection_result.get('station_id', 'Unknown'),
                detection_result.get('staff_type', 'Cashier'),
                timestamp or datetime.now()
            )
        elif event_name == 'Checkout Station Action':
            self.add_checkout_station_action(
                detection_result.get('station_id', 'Unknown'),
                detection_result.get('action', 'Open'),
                timestamp or datetime.now()
            )
        elif event_name == 'Inventory Discrepancy':
            self.add_inventory_discrepancy(
                detection_result.get('SKU'),
                detection_result.get('Expected_Inventory'),
                detection_result.get('Actual_Inventory'),
                timestamp or datetime.now()
            )
        else:
            # Generic event
            self.add_event(detection_result, timestamp)
    
    def get_events(self) -> List[Dict]:
        """Get all generated events."""
        return self.events.copy()
    
    def save_events(self, filepath: str):
        """Save events to a JSONL file."""
        try:
            with open(filepath, 'w') as f:
                for event in self.events:
                    f.write(json.dumps(event) + '\n')
            
            self.logger.info(f"Saved {len(self.events)} events to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Failed to save events to {filepath}: {e}")
    
    def save_events_json(self, filepath: str):
        """Save events to a JSON file with events array format."""
        try:
            import os
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            events_data = {
                "events": self.events
            }
            
            with open(filepath, 'w') as f:
                json.dump(events_data, f, indent=2)
            
            self.logger.info(f"Saved {len(self.events)} events to {filepath} in JSON format")
            
        except Exception as e:
            self.logger.error(f"Failed to save events to {filepath}: {e}")
    
    def clear_events(self):
        """Clear all events."""
        self.events.clear()
        self.event_counter = 0
        self.logger.info("Cleared all events")
    
    def get_event_summary(self) -> Dict[str, int]:
        """Get a summary of event counts by type."""
        summary = {}
        for event in self.events:
            event_name = event.get('event_data', {}).get('event_name', 'Unknown')
            summary[event_name] = summary.get(event_name, 0) + 1
        return summary