#!/usr/bin/env python3
"""
Detection algorithms for Project Sentinel retail analytics.
Implements all required anomaly detection algorithms with proper tagging.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import logging

class DetectionEngine:
    """Implements detection algorithms for retail anomalies and insights."""
    
    def __init__(self, data_correlator, data_parser):
        self.correlator = data_correlator
        self.parser = data_parser
        self.logger = logging.getLogger(__name__)
        
        # Thresholds for detection
        self.WEIGHT_TOLERANCE = 50  # grams
        self.LONG_QUEUE_THRESHOLD = 4  # customers
        self.LONG_WAIT_THRESHOLD = 300  # seconds (5 minutes)
        self.PRICE_DIFFERENCE_THRESHOLD = 0.5  # 50% price difference
        self.INVENTORY_VARIANCE_THRESHOLD = 10  # 10% variance
    
    # @algorithm Scanner Avoidance | Detects items in scan area without corresponding POS transactions
    def detect_scanner_avoidance(self, station_id: str, timestamp: datetime) -> Optional[Dict]:
        """Detect scanner avoidance incidents."""
        try:
            correlations = self.correlator.find_correlations(station_id, timestamp)
            rfid_readings = correlations['rfid_readings']
            pos_transactions = correlations['pos_transactions']
            
            # Look for RFID readings without corresponding POS transactions
            for rfid in rfid_readings:
                if rfid['location'] == 'IN_SCAN_AREA' and rfid['sku']:
                    # Check if there's a corresponding POS transaction for this SKU
                    found_transaction = False
                    for pos in pos_transactions:
                        if pos['sku'] == rfid['sku']:
                            found_transaction = True
                            break
                    
                    if not found_transaction:
                        return {
                            'event_name': 'Scanner Avoidance',
                            'station_id': station_id,
                            'product_sku': rfid['sku'],
                            'timestamp': timestamp.isoformat(),
                            'confidence': 0.8
                        }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Scanner avoidance detection error: {e}")
            return None
    
    # @algorithm Barcode Switching | Detects price discrepancies indicating barcode switching fraud
    def detect_barcode_switching(self, station_id: str, timestamp: datetime) -> Optional[Dict]:
        """Detect barcode switching incidents."""
        try:
            correlations = self.correlator.find_correlations(station_id, timestamp)
            pos_transactions = correlations['pos_transactions']
            rfid_readings = correlations['rfid_readings']
            
            # Compare POS transaction prices with RFID detected items
            for pos in pos_transactions:
                pos_sku = pos['sku']
                pos_price = pos['price']
                
                # Find corresponding RFID reading
                for rfid in rfid_readings:
                    if rfid['location'] == 'IN_SCAN_AREA':
                        rfid_sku = rfid['sku']
                        
                        # If different SKUs detected at same time
                        if rfid_sku != pos_sku:
                            expected_price = self.parser.get_expected_price(rfid_sku)
                            if expected_price and pos_price < expected_price * self.PRICE_DIFFERENCE_THRESHOLD:
                                return {
                                    'event_name': 'Barcode Switching',
                                    'station_id': station_id,
                                    'actual_sku': rfid_sku,
                                    'scanned_sku': pos_sku,
                                    'timestamp': timestamp.isoformat(),
                                    'price_difference': expected_price - pos_price,
                                    'confidence': 0.9
                                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Barcode switching detection error: {e}")
            return None
    
    # @algorithm Weight Discrepancy | Detects weight mismatches indicating potential theft
    def detect_weight_discrepancies(self, station_id: str, timestamp: datetime) -> Optional[Dict]:
        """Detect weight discrepancies."""
        try:
            correlations = self.correlator.find_correlations(station_id, timestamp)
            pos_transactions = correlations['pos_transactions']
            
            for pos in pos_transactions:
                sku = pos['sku']
                actual_weight = pos.get('weight_g')
                
                if actual_weight:
                    expected_weight = self.parser.get_expected_weight(sku)
                    if expected_weight:
                        weight_diff = abs(actual_weight - expected_weight)
                        if weight_diff > self.WEIGHT_TOLERANCE:
                            return {
                                'event_name': 'Weight Discrepancies',
                                'station_id': station_id,
                                'product_sku': sku,
                                'expected_weight': expected_weight,
                                'actual_weight': actual_weight,
                                'timestamp': timestamp.isoformat(),
                                'confidence': 0.85
                            }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Weight discrepancy detection error: {e}")
            return None
    
    # @algorithm System Crash Detection | Identifies system failures and crashes
    def detect_system_crashes(self, station_id: str, timestamp: datetime) -> Optional[Dict]:
        """Detect system crashes and failures."""
        try:
            status, last_activity = self.correlator.get_station_status(station_id)
            
            if status in ['System Crash', 'Read Error']:
                return {
                    'event_name': 'Unexpected Systems Crash',
                    'station_id': station_id,
                    'timestamp': timestamp.isoformat(),
                    'error_type': status,
                    'confidence': 1.0
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"System crash detection error: {e}")
            return None
    
    # @algorithm Queue Length Analysis | Monitors queue lengths and suggests optimizations
    def detect_long_queue_length(self, station_id: str, timestamp: datetime) -> Optional[Dict]:
        """Detect long queue lengths."""
        try:
            recent_queue_data = self.correlator.get_recent_data(station_id, 'queue_data', 1)
            
            if recent_queue_data:
                latest_queue = recent_queue_data[-1]
                customer_count = latest_queue.get('customer_count', 0)
                
                if customer_count >= self.LONG_QUEUE_THRESHOLD:
                    return {
                        'event_name': 'Long Queue Length',
                        'station_id': station_id,
                        'num_of_customers': customer_count,
                        'timestamp': timestamp.isoformat(),
                        'confidence': 0.9
                    }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Queue length detection error: {e}")
            return None
    
    # @algorithm Wait Time Analysis | Identifies extended customer wait times
    def detect_long_wait_times(self, station_id: str, timestamp: datetime) -> Optional[Dict]:
        """Detect long wait times."""
        try:
            recent_queue_data = self.correlator.get_recent_data(station_id, 'queue_data', 1)
            
            if recent_queue_data:
                latest_queue = recent_queue_data[-1]
                dwell_time = latest_queue.get('average_dwell_time', 0)
                
                if dwell_time >= self.LONG_WAIT_THRESHOLD:
                    return {
                        'event_name': 'Long Wait Time',
                        'station_id': station_id,
                        'wait_time_seconds': dwell_time,
                        'timestamp': timestamp.isoformat(),
                        'confidence': 0.85
                    }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Wait time detection error: {e}")
            return None
    
    # @algorithm Inventory Discrepancy | Detects inventory level mismatches
    def detect_inventory_discrepancies(self, timestamp: datetime) -> List[Dict]:
        """Detect inventory discrepancies."""
        try:
            events = []
            latest_inventory = self.correlator.get_latest_inventory()
            
            if latest_inventory:
                inventory_data = latest_inventory.get('inventory_data', {})
                
                for sku, actual_quantity in inventory_data.items():
                    expected_info = self.parser.get_product_info(sku)
                    if expected_info:
                        expected_quantity = expected_info['quantity']
                        variance = abs(actual_quantity - expected_quantity) / expected_quantity * 100
                        
                        if variance > self.INVENTORY_VARIANCE_THRESHOLD:
                            events.append({
                                'event_name': 'Inventory Discrepancy',
                                'SKU': sku,
                                'Expected_Inventory': expected_quantity,
                                'Actual_Inventory': actual_quantity,
                                'timestamp': timestamp.isoformat(),
                                'variance_percent': variance,
                                'confidence': 0.8
                            })
            
            return events
            
        except Exception as e:
            self.logger.error(f"Inventory discrepancy detection error: {e}")
            return []
    
    # @algorithm Staffing Optimization | Recommends staffing adjustments based on traffic
    def recommend_staffing_needs(self, timestamp: datetime) -> List[Dict]:
        """Recommend staffing adjustments."""
        try:
            events = []
            stations = self.correlator.get_all_stations()
            
            total_customers = 0
            busy_stations = 0
            
            for station_id in stations:
                recent_queue_data = self.correlator.get_recent_data(station_id, 'queue_data', 1)
                if recent_queue_data:
                    customer_count = recent_queue_data[-1].get('customer_count', 0)
                    total_customers += customer_count
                    if customer_count > 2:
                        busy_stations += 1
            
            # Recommend additional staff if many stations are busy
            if busy_stations > len(stations) * 0.7:  # 70% of stations busy
                events.append({
                    'event_name': 'Staffing Needs',
                    'staff_type': 'Cashier',
                    'reason': 'High customer traffic',
                    'busy_stations': busy_stations,
                    'total_stations': len(stations),
                    'timestamp': timestamp.isoformat(),
                    'confidence': 0.75
                })
            
            return events
            
        except Exception as e:
            self.logger.error(f"Staffing recommendation error: {e}")
            return []
    
    # @algorithm Station Management | Recommends opening/closing checkout stations
    def recommend_station_actions(self, timestamp: datetime) -> List[Dict]:
        """Recommend station opening/closing actions."""
        try:
            events = []
            stations = self.correlator.get_all_stations()
            
            active_stations = 0
            total_customers = 0
            
            for station_id in stations:
                status, last_activity = self.correlator.get_station_status(station_id)
                if status == 'Active':
                    active_stations += 1
                
                recent_queue_data = self.correlator.get_recent_data(station_id, 'queue_data', 1)
                if recent_queue_data:
                    total_customers += recent_queue_data[-1].get('customer_count', 0)
            
            # Target ratio: 6 customers per station
            optimal_stations = max(1, (total_customers + 5) // 6)
            
            if optimal_stations > active_stations:
                events.append({
                    'event_name': 'Checkout Station Action',
                    'action': 'Open',
                    'recommended_stations': optimal_stations - active_stations,
                    'current_customers': total_customers,
                    'timestamp': timestamp.isoformat(),
                    'confidence': 0.8
                })
            elif optimal_stations < active_stations and total_customers < active_stations * 2:
                events.append({
                    'event_name': 'Checkout Station Action',
                    'action': 'Close',
                    'recommended_stations': active_stations - optimal_stations,
                    'current_customers': total_customers,
                    'timestamp': timestamp.isoformat(),
                    'confidence': 0.7
                })
            
            return events
            
        except Exception as e:
            self.logger.error(f"Station action recommendation error: {e}")
            return []
    
    def run_all_detections(self, station_id: str, timestamp: datetime) -> List[Dict]:
        """Run all detection algorithms for a station at a given time."""
        events = []
        
        # Run station-specific detections
        detections = [
            self.detect_scanner_avoidance(station_id, timestamp),
            self.detect_barcode_switching(station_id, timestamp),
            self.detect_weight_discrepancies(station_id, timestamp),
            self.detect_system_crashes(station_id, timestamp),
            self.detect_long_queue_length(station_id, timestamp),
            self.detect_long_wait_times(station_id, timestamp)
        ]
        
        for detection in detections:
            if detection:
                events.append(detection)
        
        return events
    
    def run_global_detections(self, timestamp: datetime) -> List[Dict]:
        """Run global detection algorithms."""
        events = []
        
        # Run global detections
        events.extend(self.detect_inventory_discrepancies(timestamp))
        events.extend(self.recommend_staffing_needs(timestamp))
        events.extend(self.recommend_station_actions(timestamp))
        
        return events