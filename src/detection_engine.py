# #!/usr/bin/env python3
# """
# Detection algorithms for Project Sentinel retail analytics.
# Implements all required anomaly detection algorithms with proper tagging.
# """

# import json
# from datetime import datetime, timedelta
# from typing import Dict, List, Any, Optional, Tuple
# import logging

# class DetectionEngine:
#     """Implements detection algorithms for retail anomalies and insights."""
    
#     def __init__(self, data_correlator, data_parser):
#         self.correlator = data_correlator
#         self.parser = data_parser
#         self.logger = logging.getLogger(__name__)
        
#         # Thresholds for detection
#         self.WEIGHT_TOLERANCE = 50  # grams
#         self.LONG_QUEUE_THRESHOLD = 4  # customers
#         self.LONG_WAIT_THRESHOLD = 300  # seconds (5 minutes)
#         self.PRICE_DIFFERENCE_THRESHOLD = 0.5  # 50% price difference
#         self.INVENTORY_VARIANCE_THRESHOLD = 10  # 10% variance
    
#     # @algorithm Scanner Avoidance | Detects items in scan area without corresponding POS transactions
#     def detect_scanner_avoidance(self, station_id: str, timestamp: datetime) -> Optional[Dict]:
#         """Detect scanner avoidance incidents."""
#         try:
#             correlations = self.correlator.find_correlations(station_id, timestamp)
#             rfid_readings = correlations['rfid_readings']
#             pos_transactions = correlations['pos_transactions']
            
#             # Look for RFID readings without corresponding POS transactions
#             for rfid in rfid_readings:
#                 if rfid['location'] == 'IN_SCAN_AREA' and rfid['sku']:
#                     # Check if there's a corresponding POS transaction for this SKU
#                     found_transaction = False
#                     for pos in pos_transactions:
#                         if pos['sku'] == rfid['sku']:
#                             found_transaction = True
#                             break
                    
#                     if not found_transaction:
#                         return {
#                             'event_name': 'Scanner Avoidance',
#                             'station_id': station_id,
#                             'product_sku': rfid['sku'],
#                             'timestamp': timestamp.isoformat(),
#                             'confidence': 0.8
#                         }
            
#             return None
            
#         except Exception as e:
#             self.logger.error(f"Scanner avoidance detection error: {e}")
#             return None
    
#     # @algorithm Barcode Switching | Detects price discrepancies indicating barcode switching fraud
#     def detect_barcode_switching(self, station_id: str, timestamp: datetime) -> Optional[Dict]:
#         """Detect barcode switching incidents."""
#         try:
#             correlations = self.correlator.find_correlations(station_id, timestamp)
#             pos_transactions = correlations['pos_transactions']
#             rfid_readings = correlations['rfid_readings']
            
#             # Compare POS transaction prices with RFID detected items
#             for pos in pos_transactions:
#                 pos_sku = pos['sku']
#                 pos_price = pos['price']
                
#                 # Find corresponding RFID reading
#                 for rfid in rfid_readings:
#                     if rfid['location'] == 'IN_SCAN_AREA':
#                         rfid_sku = rfid['sku']
                        
#                         # If different SKUs detected at same time
#                         if rfid_sku != pos_sku:
#                             expected_price = self.parser.get_expected_price(rfid_sku)
#                             if expected_price and pos_price < expected_price * self.PRICE_DIFFERENCE_THRESHOLD:
#                                 return {
#                                     'event_name': 'Barcode Switching',
#                                     'station_id': station_id,
#                                     'actual_sku': rfid_sku,
#                                     'scanned_sku': pos_sku,
#                                     'timestamp': timestamp.isoformat(),
#                                     'price_difference': expected_price - pos_price,
#                                     'confidence': 0.9
#                                 }
            
#             return None
            
#         except Exception as e:
#             self.logger.error(f"Barcode switching detection error: {e}")
#             return None
    
#     # @algorithm Weight Discrepancy | Detects weight mismatches indicating potential theft
#     def detect_weight_discrepancies(self, station_id: str, timestamp: datetime) -> Optional[Dict]:
#         """Detect weight discrepancies."""
#         try:
#             correlations = self.correlator.find_correlations(station_id, timestamp)
#             pos_transactions = correlations['pos_transactions']
            
#             for pos in pos_transactions:
#                 sku = pos['sku']
#                 actual_weight = pos.get('weight_g')
                
#                 if actual_weight:
#                     expected_weight = self.parser.get_expected_weight(sku)
#                     if expected_weight:
#                         weight_diff = abs(actual_weight - expected_weight)
#                         if weight_diff > self.WEIGHT_TOLERANCE:
#                             return {
#                                 'event_name': 'Weight Discrepancies',
#                                 'station_id': station_id,
#                                 'product_sku': sku,
#                                 'expected_weight': expected_weight,
#                                 'actual_weight': actual_weight,
#                                 'timestamp': timestamp.isoformat(),
#                                 'confidence': 0.85
#                             }
            
#             return None
            
#         except Exception as e:
#             self.logger.error(f"Weight discrepancy detection error: {e}")
#             return None
    
#     # @algorithm System Crash Detection | Identifies system failures and crashes
#     def detect_system_crashes(self, station_id: str, timestamp: datetime) -> Optional[Dict]:
#         """Detect system crashes and failures."""
#         try:
#             status, last_activity = self.correlator.get_station_status(station_id)
            
#             if status in ['System Crash', 'Read Error']:
#                 return {
#                     'event_name': 'Unexpected Systems Crash',
#                     'station_id': station_id,
#                     'timestamp': timestamp.isoformat(),
#                     'error_type': status,
#                     'confidence': 1.0
#                 }
            
#             return None
            
#         except Exception as e:
#             self.logger.error(f"System crash detection error: {e}")
#             return None
    
#     # @algorithm Queue Length Analysis | Monitors queue lengths and suggests optimizations
#     def detect_long_queue_length(self, station_id: str, timestamp: datetime) -> Optional[Dict]:
#         """Detect long queue lengths."""
#         try:
#             recent_queue_data = self.correlator.get_recent_data(station_id, 'queue_data', 1)
            
#             if recent_queue_data:
#                 latest_queue = recent_queue_data[-1]
#                 customer_count = latest_queue.get('customer_count', 0)
                
#                 if customer_count >= self.LONG_QUEUE_THRESHOLD:
#                     return {
#                         'event_name': 'Long Queue Length',
#                         'station_id': station_id,
#                         'num_of_customers': customer_count,
#                         'timestamp': timestamp.isoformat(),
#                         'confidence': 0.9
#                     }
            
#             return None
            
#         except Exception as e:
#             self.logger.error(f"Queue length detection error: {e}")
#             return None
    
#     # @algorithm Wait Time Analysis | Identifies extended customer wait times
#     def detect_long_wait_times(self, station_id: str, timestamp: datetime) -> Optional[Dict]:
#         """Detect long wait times."""
#         try:
#             recent_queue_data = self.correlator.get_recent_data(station_id, 'queue_data', 1)
            
#             if recent_queue_data:
#                 latest_queue = recent_queue_data[-1]
#                 dwell_time = latest_queue.get('average_dwell_time', 0)
                
#                 if dwell_time >= self.LONG_WAIT_THRESHOLD:
#                     return {
#                         'event_name': 'Long Wait Time',
#                         'station_id': station_id,
#                         'wait_time_seconds': dwell_time,
#                         'timestamp': timestamp.isoformat(),
#                         'confidence': 0.85
#                     }
            
#             return None
            
#         except Exception as e:
#             self.logger.error(f"Wait time detection error: {e}")
#             return None
    
#     # @algorithm Inventory Discrepancy | Detects inventory level mismatches
#     def detect_inventory_discrepancies(self, timestamp: datetime) -> List[Dict]:
#         """Detect inventory discrepancies."""
#         try:
#             events = []
#             latest_inventory = self.correlator.get_latest_inventory()
            
#             if latest_inventory:
#                 inventory_data = latest_inventory.get('inventory_data', {})
                
#                 for sku, actual_quantity in inventory_data.items():
#                     expected_info = self.parser.get_product_info(sku)
#                     if expected_info:
#                         expected_quantity = expected_info['quantity']
#                         variance = abs(actual_quantity - expected_quantity) / expected_quantity * 100
                        
#                         if variance > self.INVENTORY_VARIANCE_THRESHOLD:
#                             events.append({
#                                 'event_name': 'Inventory Discrepancy',
#                                 'SKU': sku,
#                                 'Expected_Inventory': expected_quantity,
#                                 'Actual_Inventory': actual_quantity,
#                                 'timestamp': timestamp.isoformat(),
#                                 'variance_percent': variance,
#                                 'confidence': 0.8
#                             })
            
#             return events
            
#         except Exception as e:
#             self.logger.error(f"Inventory discrepancy detection error: {e}")
#             return []
    
#     # @algorithm Staffing Optimization | Recommends staffing adjustments based on traffic
#     def recommend_staffing_needs(self, timestamp: datetime) -> List[Dict]:
#         """Recommend staffing adjustments."""
#         try:
#             events = []
#             stations = self.correlator.get_all_stations()
            
#             total_customers = 0
#             busy_stations = 0
            
#             for station_id in stations:
#                 recent_queue_data = self.correlator.get_recent_data(station_id, 'queue_data', 1)
#                 if recent_queue_data:
#                     customer_count = recent_queue_data[-1].get('customer_count', 0)
#                     total_customers += customer_count
#                     if customer_count > 2:
#                         busy_stations += 1
            
#             # Recommend additional staff if many stations are busy
#             if busy_stations > len(stations) * 0.7:  # 70% of stations busy
#                 events.append({
#                     'event_name': 'Staffing Needs',
#                     'staff_type': 'Cashier',
#                     'reason': 'High customer traffic',
#                     'busy_stations': busy_stations,
#                     'total_stations': len(stations),
#                     'timestamp': timestamp.isoformat(),
#                     'confidence': 0.75
#                 })
            
#             return events
            
#         except Exception as e:
#             self.logger.error(f"Staffing recommendation error: {e}")
#             return []
    
#     # @algorithm Station Management | Recommends opening/closing checkout stations
#     def recommend_station_actions(self, timestamp: datetime) -> List[Dict]:
#         """Recommend station opening/closing actions."""
#         try:
#             events = []
#             stations = self.correlator.get_all_stations()
            
#             active_stations = 0
#             total_customers = 0
            
#             for station_id in stations:
#                 status, last_activity = self.correlator.get_station_status(station_id)
#                 if status == 'Active':
#                     active_stations += 1
                
#                 recent_queue_data = self.correlator.get_recent_data(station_id, 'queue_data', 1)
#                 if recent_queue_data:
#                     total_customers += recent_queue_data[-1].get('customer_count', 0)
            
#             # Target ratio: 6 customers per station
#             optimal_stations = max(1, (total_customers + 5) // 6)
            
#             if optimal_stations > active_stations:
#                 events.append({
#                     'event_name': 'Checkout Station Action',
#                     'action': 'Open',
#                     'recommended_stations': optimal_stations - active_stations,
#                     'current_customers': total_customers,
#                     'timestamp': timestamp.isoformat(),
#                     'confidence': 0.8
#                 })
#             elif optimal_stations < active_stations and total_customers < active_stations * 2:
#                 events.append({
#                     'event_name': 'Checkout Station Action',
#                     'action': 'Close',
#                     'recommended_stations': active_stations - optimal_stations,
#                     'current_customers': total_customers,
#                     'timestamp': timestamp.isoformat(),
#                     'confidence': 0.7
#                 })
            
#             return events
            
#         except Exception as e:
#             self.logger.error(f"Station action recommendation error: {e}")
#             return []
    
#     def run_all_detections(self, station_id: str, timestamp: datetime) -> List[Dict]:
#         """Run all detection algorithms for a station at a given time."""
#         events = []
        
#         # Run station-specific detections
#         detections = [
#             self.detect_scanner_avoidance(station_id, timestamp),
#             self.detect_barcode_switching(station_id, timestamp),
#             self.detect_weight_discrepancies(station_id, timestamp),
#             self.detect_system_crashes(station_id, timestamp),
#             self.detect_long_queue_length(station_id, timestamp),
#             self.detect_long_wait_times(station_id, timestamp)
#         ]
        
#         for detection in detections:
#             if detection:
#                 events.append(detection)
        
#         return events
    
#     def run_global_detections(self, timestamp: datetime) -> List[Dict]:
#         """Run global detection algorithms."""
#         events = []
        
#         # Run global detections
#         events.extend(self.detect_inventory_discrepancies(timestamp))
#         events.extend(self.recommend_staffing_needs(timestamp))
#         events.extend(self.recommend_station_actions(timestamp))
        
#         return events





#!/usr/bin/env python3
"""
Detection algorithms for Project Sentinel retail analytics.
Implements all required anomaly detection algorithms with proper tagging and fixes.
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
        self.LONG_QUEUE_THRESHOLD = 3  # customers (lowered from 4)
        self.LONG_WAIT_THRESHOLD = 120  # seconds (lowered from 300)
        self.PRICE_DIFFERENCE_THRESHOLD = 0.5  # 50% price difference
        self.INVENTORY_VARIANCE_THRESHOLD = 5.0  # 5% variance (lowered from 10%)
        self.MIN_INVENTORY_FOR_VARIANCE = 10  # Minimum inventory to calculate variance
    
    # @algorithm Scanner Avoidance | Detects items in scan area without corresponding POS transactions
    def detect_scanner_avoidance(self, station_id: str, timestamp: datetime) -> Optional[Dict]:
        """Detect scanner avoidance incidents."""
        try:
            correlations = self.correlator.find_correlations(station_id, timestamp)
            rfid_readings = correlations.get('rfid_readings', [])
            pos_transactions = correlations.get('pos_transactions', [])
            
            # Look for RFID readings without corresponding POS transactions
            for rfid in rfid_readings:
                # Add null checks for RFID data
                location = rfid.get('location')
                sku = rfid.get('sku')
                
                if location == 'IN_SCAN_AREA' and sku and sku != 'null':
                    # Check if there's a corresponding POS transaction for this SKU
                    found_transaction = False
                    for pos in pos_transactions:
                        if pos.get('sku') == sku:
                            found_transaction = True
                            break
                    
                    if not found_transaction:
                        return {
                            'event_name': 'Scanner Avoidance',
                            'station_id': station_id,
                            'product_sku': sku,
                            'timestamp': timestamp.isoformat(),
                            'confidence': 0.8,
                            'severity': 'HIGH'
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
            pos_transactions = correlations.get('pos_transactions', [])
            rfid_readings = correlations.get('rfid_readings', [])
            
            # Compare POS transaction prices with RFID detected items
            for pos in pos_transactions:
                pos_sku = pos.get('sku')
                pos_price = pos.get('price')
                
                if not pos_sku or pos_price is None:
                    continue
                
                # Find corresponding RFID reading
                for rfid in rfid_readings:
                    location = rfid.get('location')
                    rfid_sku = rfid.get('sku')
                    
                    if location == 'IN_SCAN_AREA' and rfid_sku and rfid_sku != 'null':
                        # If different SKUs detected at same time
                        if rfid_sku != pos_sku:
                            expected_price = self.parser.get_expected_price(rfid_sku)
                            if expected_price and expected_price > 0:
                                price_ratio = pos_price / expected_price
                                if price_ratio < self.PRICE_DIFFERENCE_THRESHOLD:
                                    return {
                                        'event_name': 'Barcode Switching',
                                        'station_id': station_id,
                                        'actual_sku': rfid_sku,
                                        'scanned_sku': pos_sku,
                                        'timestamp': timestamp.isoformat(),
                                        'expected_price': expected_price,
                                        'actual_price': pos_price,
                                        'price_difference': expected_price - pos_price,
                                        'confidence': 0.9,
                                        'severity': 'CRITICAL'
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
            pos_transactions = correlations.get('pos_transactions', [])
            
            for pos in pos_transactions:
                sku = pos.get('sku')
                actual_weight = pos.get('weight_g')
                
                if not sku or actual_weight is None:
                    continue
                
                expected_weight = self.parser.get_expected_weight(sku)
                if expected_weight and expected_weight > 0:
                    weight_diff = abs(actual_weight - expected_weight)
                    variance_percent = (weight_diff / expected_weight) * 100
                    
                    if weight_diff > self.WEIGHT_TOLERANCE:
                        return {
                            'event_name': 'Weight Discrepancies',
                            'station_id': station_id,
                            'product_sku': sku,
                            'expected_weight': expected_weight,
                            'actual_weight': actual_weight,
                            'weight_difference': weight_diff,
                            'variance_percent': round(variance_percent, 2),
                            'timestamp': timestamp.isoformat(),
                            'confidence': 0.85,
                            'severity': 'HIGH' if variance_percent > 20 else 'MEDIUM'
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
            
            if status in ['System Crash', 'Read Error', 'Error', 'Failed']:
                return {
                    'event_name': 'Unexpected Systems Crash',
                    'station_id': station_id,
                    'timestamp': timestamp.isoformat(),
                    'error_type': status,
                    'last_activity': last_activity.isoformat() if last_activity else None,
                    'confidence': 1.0,
                    'severity': 'CRITICAL'
                }
            
            # Detect unresponsive stations (no activity for extended period)
            if last_activity and status == 'Active':
                time_diff = (timestamp - last_activity).total_seconds()
                if time_diff > 600:  # 10 minutes of inactivity
                    return {
                        'event_name': 'Station Unresponsive',
                        'station_id': station_id,
                        'timestamp': timestamp.isoformat(),
                        'inactive_duration': time_diff,
                        'last_activity': last_activity.isoformat(),
                        'confidence': 0.75,
                        'severity': 'HIGH'
                    }
            
            return None
            
        except Exception as e:
            self.logger.error(f"System crash detection error: {e}")
            return None
    
    # @algorithm Queue Length Analysis | Monitors queue lengths and suggests optimizations
    def detect_long_queue_length(self, station_id: str, timestamp: datetime) -> Optional[Dict]:
        """Detect long queue lengths with trend analysis."""
        try:
            # Get last 6 readings (30 seconds of data at 5-second intervals)
            recent_queue_data = self.correlator.get_recent_data(station_id, 'queue_data', 6)
            
            if not recent_queue_data:
                return None
            
            latest_queue = recent_queue_data[-1]
            customer_count = latest_queue.get('customer_count', 0)
            avg_dwell = latest_queue.get('average_dwell_time', 0)
            
            # Calculate trend if we have enough data
            trend = 'stable'
            duration_seconds = 0
            
            if len(recent_queue_data) >= 3:
                counts = [q.get('customer_count', 0) for q in recent_queue_data]
                
                # Check if queue is growing
                if counts[-1] > counts[0] and counts[-1] > counts[-2]:
                    trend = 'growing'
                elif counts[-1] < counts[0] and counts[-1] < counts[-2]:
                    trend = 'shrinking'
                
                # Calculate how long queue has been problematic
                problematic_readings = sum(1 for c in counts if c >= self.LONG_QUEUE_THRESHOLD)
                duration_seconds = problematic_readings * 5  # Assuming 5-second intervals
            
            # Trigger alert based on current count or sustained queue
            if customer_count >= self.LONG_QUEUE_THRESHOLD or duration_seconds >= 15:
                # Determine severity based on multiple factors
                if customer_count >= 7 or (customer_count >= 5 and trend == 'growing'):
                    severity = 'CRITICAL'
                elif customer_count >= 5 or duration_seconds >= 25:
                    severity = 'HIGH'
                else:
                    severity = 'MEDIUM'
                
                return {
                    'event_name': 'Long Queue Length',
                    'station_id': station_id,
                    'num_of_customers': customer_count,
                    'average_dwell_time': avg_dwell,
                    'queue_trend': trend,
                    'duration_seconds': duration_seconds,
                    'timestamp': timestamp.isoformat(),
                    'confidence': 0.9 if trend == 'growing' else 0.85,
                    'severity': severity
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Queue length detection error: {e}")
            return None
    
    # @algorithm Wait Time Analysis | Identifies extended customer wait times
    def detect_long_wait_times(self, station_id: str, timestamp: datetime) -> Optional[Dict]:
        """Detect long wait times with trend analysis."""
        try:
            # Get last 6 readings (30 seconds of data)
            recent_queue_data = self.correlator.get_recent_data(station_id, 'queue_data', 6)
            
            if not recent_queue_data:
                return None
            
            latest_queue = recent_queue_data[-1]
            dwell_time = latest_queue.get('average_dwell_time', 0)
            customer_count = latest_queue.get('customer_count', 0)
            
            # Calculate trend
            trend = 'stable'
            duration_seconds = 0
            avg_wait_time = dwell_time
            
            if len(recent_queue_data) >= 3:
                wait_times = [q.get('average_dwell_time', 0) for q in recent_queue_data]
                
                # Calculate average wait time over period
                avg_wait_time = sum(wait_times) / len(wait_times)
                
                # Check trend
                if wait_times[-1] > wait_times[0] and wait_times[-1] > wait_times[-2]:
                    trend = 'increasing'
                elif wait_times[-1] < wait_times[0] and wait_times[-1] < wait_times[-2]:
                    trend = 'decreasing'
                
                # Calculate sustained high wait time duration
                problematic_readings = sum(1 for w in wait_times if w >= self.LONG_WAIT_THRESHOLD)
                duration_seconds = problematic_readings * 5
            
            # Trigger alert
            if dwell_time >= self.LONG_WAIT_THRESHOLD or avg_wait_time >= self.LONG_WAIT_THRESHOLD:
                # Enhanced severity calculation
                if dwell_time >= 300 or (dwell_time >= 240 and trend == 'increasing'):
                    severity = 'CRITICAL'
                elif dwell_time >= 180 or avg_wait_time >= 200 or duration_seconds >= 20:
                    severity = 'HIGH'
                else:
                    severity = 'MEDIUM'
                
                return {
                    'event_name': 'Long Wait Time',
                    'station_id': station_id,
                    'wait_time_seconds': dwell_time,
                    'average_wait_time': round(avg_wait_time, 1),
                    'customer_count': customer_count,
                    'wait_trend': trend,
                    'sustained_duration_seconds': duration_seconds,
                    'timestamp': timestamp.isoformat(),
                    'confidence': 0.9 if trend == 'increasing' else 0.85,
                    'severity': severity
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Wait time detection error: {e}")
            return None
    
    # @algorithm Inventory Discrepancy | Detects inventory level mismatches
    def detect_inventory_discrepancies(self, timestamp: datetime) -> List[Dict]:
        """Detect inventory discrepancies with improved variance calculation."""
        try:
            events = []
            latest_inventory = self.correlator.get_latest_inventory()
            
            if not latest_inventory:
                return events
            
            inventory_data = latest_inventory.get('inventory_data', {})
            
            for sku, actual_quantity in inventory_data.items():
                if actual_quantity is None:
                    continue
                
                expected_info = self.parser.get_product_info(sku)
                if not expected_info:
                    continue
                
                expected_quantity = expected_info.get('quantity')
                if expected_quantity is None or expected_quantity <= 0:
                    continue
                
                # Calculate variance
                quantity_diff = abs(actual_quantity - expected_quantity)
                
                # Only calculate percentage variance for items with sufficient inventory
                if expected_quantity >= self.MIN_INVENTORY_FOR_VARIANCE:
                    variance = (quantity_diff / expected_quantity) * 100
                else:
                    # For low inventory items, use absolute difference
                    variance = quantity_diff * 10  # Scale to make comparable
                
                if variance > self.INVENTORY_VARIANCE_THRESHOLD:
                    severity = 'CRITICAL' if variance > 20 else 'HIGH' if variance > 10 else 'MEDIUM'
                    events.append({
                        'event_name': 'Inventory Discrepancy',
                        'SKU': sku,
                        'product_name': expected_info.get('name', 'Unknown'),
                        'expected_inventory': expected_quantity,
                        'actual_inventory': actual_quantity,
                        'difference': int(actual_quantity - expected_quantity),
                        'timestamp': timestamp.isoformat(),
                        'variance_percent': round(variance, 2),
                        'confidence': 0.8,
                        'severity': severity
                    })
            
            return events
            
        except Exception as e:
            self.logger.error(f"Inventory discrepancy detection error: {e}")
            return []
    
    # @algorithm Staffing Optimization | Recommends staffing adjustments based on traffic
    def recommend_staffing_needs(self, timestamp: datetime) -> List[Dict]:
        """Recommend staffing adjustments with temporal analysis."""
        try:
            events = []
            stations = self.correlator.get_all_stations()
            
            if not stations:
                return events
            
            total_customers = 0
            busy_stations = 0
            high_wait_stations = 0
            sustained_busy_stations = 0
            
            for station_id in stations:
                # Get recent data for trend analysis
                recent_queue_data = self.correlator.get_recent_data(station_id, 'queue_data', 6)
                
                if recent_queue_data:
                    latest = recent_queue_data[-1]
                    customer_count = latest.get('customer_count', 0)
                    dwell_time = latest.get('average_dwell_time', 0)
                    
                    total_customers += customer_count
                    
                    if customer_count >= 2:
                        busy_stations += 1
                    
                    if dwell_time >= self.LONG_WAIT_THRESHOLD:
                        high_wait_stations += 1
                    
                    # Check if station has been consistently busy
                    if len(recent_queue_data) >= 4:
                        busy_readings = sum(1 for q in recent_queue_data if q.get('customer_count', 0) >= 3)
                        if busy_readings >= 3:  # Busy for at least 15 seconds
                            sustained_busy_stations += 1
            
            busy_ratio = busy_stations / len(stations) if len(stations) > 0 else 0
            sustained_ratio = sustained_busy_stations / len(stations) if len(stations) > 0 else 0
            
            # Recommend additional cashiers if many stations are busy
            if busy_ratio >= 0.6 or sustained_ratio >= 0.5:
                severity = 'HIGH' if busy_ratio >= 0.8 or sustained_ratio >= 0.7 else 'MEDIUM'
                events.append({
                    'event_name': 'Staffing Needs',
                    'staff_type': 'Cashier',
                    'action': 'ADD',
                    'reason': 'Sustained high customer traffic detected',
                    'busy_stations': busy_stations,
                    'sustained_busy_stations': sustained_busy_stations,
                    'total_stations': len(stations),
                    'total_customers': total_customers,
                    'busy_ratio': round(busy_ratio, 2),
                    'sustained_ratio': round(sustained_ratio, 2),
                    'timestamp': timestamp.isoformat(),
                    'confidence': 0.8 if sustained_ratio >= 0.5 else 0.75,
                    'severity': severity
                })
            
            # Recommend support staff if wait times are high
            if high_wait_stations >= 2:
                events.append({
                    'event_name': 'Staffing Needs',
                    'staff_type': 'Support Staff',
                    'action': 'ADD',
                    'reason': 'Extended wait times at multiple stations',
                    'affected_stations': high_wait_stations,
                    'timestamp': timestamp.isoformat(),
                    'confidence': 0.8,
                    'severity': 'HIGH'
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
            
            if not stations:
                return events
            
            active_stations = 0
            idle_stations = []
            total_customers = 0
            
            for station_id in stations:
                status, last_activity = self.correlator.get_station_status(station_id)
                
                recent_queue_data = self.correlator.get_recent_data(station_id, 'queue_data', 1)
                customer_count = 0
                if recent_queue_data:
                    customer_count = recent_queue_data[-1].get('customer_count', 0)
                    total_customers += customer_count
                
                if status == 'Active':
                    active_stations += 1
                    if customer_count == 0:
                        idle_stations.append(station_id)
            
            # Target ratio: 4-5 customers per station (adjusted)
            if active_stations > 0:
                avg_customers_per_station = total_customers / active_stations
                optimal_stations = max(1, (total_customers + 4) // 5)
                
                # Recommend opening new stations
                if avg_customers_per_station > 5 and optimal_stations > active_stations:
                    stations_to_open = min(optimal_stations - active_stations, 3)  # Max 3 at once
                    events.append({
                        'event_name': 'Checkout Station Action',
                        'action': 'OPEN',
                        'recommended_stations': stations_to_open,
                        'current_active_stations': active_stations,
                        'current_customers': total_customers,
                        'avg_customers_per_station': round(avg_customers_per_station, 1),
                        'reason': 'High customer load per station',
                        'timestamp': timestamp.isoformat(),
                        'confidence': 0.8,
                        'severity': 'HIGH'
                    })
                
                # Recommend closing stations (only if multiple idle)
                elif len(idle_stations) >= 2 and active_stations > 2:
                    stations_to_close = min(len(idle_stations) - 1, active_stations - 2)  # Keep at least 2 open
                    if stations_to_close > 0:
                        events.append({
                            'event_name': 'Checkout Station Action',
                            'action': 'CLOSE',
                            'recommended_stations': stations_to_close,
                            'idle_stations': idle_stations[:stations_to_close],
                            'current_active_stations': active_stations,
                            'current_customers': total_customers,
                            'reason': 'Low customer traffic',
                            'timestamp': timestamp.isoformat(),
                            'confidence': 0.7,
                            'severity': 'LOW'
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
    
    def generate_summary_report(self, events: List[Dict]) -> Dict[str, Any]:
        """Generate a summary report of all detected events."""
        summary = {
            'total_events': len(events),
            'by_severity': {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0},
            'by_type': {},
            'critical_events': []
        }
        
        for event in events:
            event_name = event.get('event_name', 'Unknown')
            severity = event.get('severity', 'MEDIUM')
            
            summary['by_severity'][severity] = summary['by_severity'].get(severity, 0) + 1
            summary['by_type'][event_name] = summary['by_type'].get(event_name, 0) + 1
            
            if severity == 'CRITICAL':
                summary['critical_events'].append(event)
        
        return summary