#!/usr/bin/env python3
"""
Data correlation engine for Project Sentinel.
Correlates data streams by timestamp and station to detect patterns.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, deque
import logging

class DataCorrelator:
    """Correlates data streams from multiple sources to detect retail events."""
    
    def __init__(self, time_window_seconds: int = 30):
        self.time_window = timedelta(seconds=time_window_seconds)
        self.logger = logging.getLogger(__name__)
        
        # Store recent data for correlation
        self.pos_transactions: Dict[str, deque] = defaultdict(deque)  # station_id -> transactions
        self.rfid_readings: Dict[str, deque] = defaultdict(deque)     # station_id -> readings
        self.queue_data: Dict[str, deque] = defaultdict(deque)        # station_id -> queue info
        self.product_recognition: Dict[str, deque] = defaultdict(deque)  # station_id -> predictions
        self.inventory_snapshots: List[Dict] = []
        
        # System status tracking
        self.station_status: Dict[str, str] = {}  # station_id -> last status
        self.last_activity: Dict[str, datetime] = {}  # station_id -> last activity time
        
    def add_data(self, parsed_data: Dict[str, Any]):
        """Add parsed data to the correlation engine."""
        if not parsed_data:
            return
            
        data_type = parsed_data.get('type')
        timestamp_str = parsed_data.get('timestamp')
        
        if not timestamp_str:
            return
            
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except Exception as e:
            self.logger.warning(f"Invalid timestamp: {timestamp_str}")
            return
        
        # Add to appropriate data store
        if data_type == 'pos_transaction':
            self._add_pos_transaction(parsed_data, timestamp)
        elif data_type == 'rfid_reading':
            self._add_rfid_reading(parsed_data, timestamp)
        elif data_type == 'queue_monitoring':
            self._add_queue_data(parsed_data, timestamp)
        elif data_type == 'product_recognition':
            self._add_product_recognition(parsed_data, timestamp)
        elif data_type == 'inventory_snapshot':
            self._add_inventory_snapshot(parsed_data, timestamp)
        
        # Update station status
        station_id = parsed_data.get('station_id')
        if station_id:
            self.station_status[station_id] = parsed_data.get('status', 'Unknown')
            self.last_activity[station_id] = timestamp
        
        # Clean old data
        self._cleanup_old_data(timestamp)
    
    def _add_pos_transaction(self, data: Dict, timestamp: datetime):
        """Add POS transaction data."""
        station_id = data.get('station_id')
        if station_id:
            data['parsed_timestamp'] = timestamp
            self.pos_transactions[station_id].append(data)
    
    def _add_rfid_reading(self, data: Dict, timestamp: datetime):
        """Add RFID reading data."""
        station_id = data.get('station_id')
        if station_id:
            data['parsed_timestamp'] = timestamp
            self.rfid_readings[station_id].append(data)
    
    def _add_queue_data(self, data: Dict, timestamp: datetime):
        """Add queue monitoring data."""
        station_id = data.get('station_id')
        if station_id:
            data['parsed_timestamp'] = timestamp
            self.queue_data[station_id].append(data)
    
    def _add_product_recognition(self, data: Dict, timestamp: datetime):
        """Add product recognition data."""
        station_id = data.get('station_id')
        if station_id:
            data['parsed_timestamp'] = timestamp
            self.product_recognition[station_id].append(data)
    
    def _add_inventory_snapshot(self, data: Dict, timestamp: datetime):
        """Add inventory snapshot data."""
        data['parsed_timestamp'] = timestamp
        self.inventory_snapshots.append(data)
        # Keep only recent snapshots
        cutoff = timestamp - timedelta(hours=1)
        self.inventory_snapshots = [s for s in self.inventory_snapshots if s['parsed_timestamp'] > cutoff]
    
    def _cleanup_old_data(self, current_timestamp: datetime):
        """Remove data older than the time window."""
        cutoff = current_timestamp - self.time_window
        
        for station_data in [self.pos_transactions, self.rfid_readings, 
                           self.queue_data, self.product_recognition]:
            for station_id in station_data:
                while (station_data[station_id] and 
                       station_data[station_id][0]['parsed_timestamp'] < cutoff):
                    station_data[station_id].popleft()
    
    def find_correlations(self, station_id: str, timestamp: datetime) -> Dict[str, List]:
        """Find correlated data around a specific timestamp and station."""
        time_range = timedelta(seconds=10)  # Look within 10 seconds
        start_time = timestamp - time_range
        end_time = timestamp + time_range
        
        correlations = {
            'pos_transactions': [],
            'rfid_readings': [],
            'queue_data': [],
            'product_recognition': []
        }
        
        # Find correlated POS transactions
        for tx in self.pos_transactions.get(station_id, []):
            if start_time <= tx['parsed_timestamp'] <= end_time:
                correlations['pos_transactions'].append(tx)
        
        # Find correlated RFID readings
        for reading in self.rfid_readings.get(station_id, []):
            if start_time <= reading['parsed_timestamp'] <= end_time:
                correlations['rfid_readings'].append(reading)
        
        # Find correlated queue data
        for queue_info in self.queue_data.get(station_id, []):
            if start_time <= queue_info['parsed_timestamp'] <= end_time:
                correlations['queue_data'].append(queue_info)
        
        # Find correlated product recognition
        for recognition in self.product_recognition.get(station_id, []):
            if start_time <= recognition['parsed_timestamp'] <= end_time:
                correlations['product_recognition'].append(recognition)
        
        return correlations
    
    def get_recent_data(self, station_id: str, data_type: str, limit: int = 10) -> List[Dict]:
        """Get recent data of a specific type for a station."""
        data_stores = {
            'pos_transactions': self.pos_transactions,
            'rfid_readings': self.rfid_readings,
            'queue_data': self.queue_data,
            'product_recognition': self.product_recognition
        }
        
        if data_type not in data_stores:
            return []
        
        station_data = data_stores[data_type].get(station_id, deque())
        return list(station_data)[-limit:]
    
    def get_station_status(self, station_id: str) -> Tuple[str, Optional[datetime]]:
        """Get the current status and last activity time for a station."""
        status = self.station_status.get(station_id, 'Unknown')
        last_activity = self.last_activity.get(station_id)
        return status, last_activity
    
    def get_all_stations(self) -> List[str]:
        """Get list of all known stations."""
        stations = set()
        stations.update(self.pos_transactions.keys())
        stations.update(self.rfid_readings.keys())
        stations.update(self.queue_data.keys())
        stations.update(self.product_recognition.keys())
        return list(stations)
    
    def get_latest_inventory(self) -> Optional[Dict]:
        """Get the most recent inventory snapshot."""
        if self.inventory_snapshots:
            return self.inventory_snapshots[-1]
        return None