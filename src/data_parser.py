#!/usr/bin/env python3
"""
Data parser module for Project Sentinel.
Handles parsing and normalization of all data sources.
"""

import json
import csv
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

class DataParser:
    """Parser for all Project Sentinel data sources."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.products_data: Dict[str, Dict] = {}
        self.customers_data: Dict[str, Dict] = {}
        
    def load_reference_data(self, products_csv_path: str, customers_csv_path: str):
        """Load reference data from CSV files."""
        try:
            # Load products data
            with open(products_csv_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.products_data[row['SKU']] = {
                        'product_name': row['product_name'],
                        'quantity': int(row['quantity']),
                        'epc_range': row['EPC_range'],
                        'barcode': row['barcode'],
                        'weight': float(row['weight']),
                        'price': float(row['price'])
                    }
            
            # Load customers data
            with open(customers_csv_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.customers_data[row['Customer_ID']] = {
                        'name': row['Name'],
                        'age': int(row['Age']),
                        'address': row['Address'],
                        'phone': row['TP']
                    }
                    
            self.logger.info(f"Loaded {len(self.products_data)} products and {len(self.customers_data)} customers")
            
        except Exception as e:
            self.logger.error(f"Failed to load reference data: {e}")
    
    def parse_streaming_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse a streaming event into normalized format."""
        try:
            dataset = event.get('dataset', '')
            payload = event.get('event', {})  # Note: using 'event' not 'payload'
            
            if dataset == 'POS_Transactions':
                return self._parse_pos_transaction(payload)
            elif dataset == 'RFID_data':
                return self._parse_rfid_reading(payload)
            elif dataset == 'Queue_monitor':
                return self._parse_queue_monitoring(payload)
            elif dataset == 'Product_recognism':
                return self._parse_product_recognition(payload)
            elif dataset == 'Current_inventory_data':
                return self._parse_inventory_snapshot(payload)
            else:
                self.logger.warning(f"Unknown dataset: {dataset}")
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to parse event: {e}")
            return None
    
    def _parse_pos_transaction(self, payload: Dict) -> Dict[str, Any]:
        """Parse POS transaction data."""
        return {
            'type': 'pos_transaction',
            'timestamp': payload.get('timestamp'),
            'station_id': payload.get('station_id'),
            'status': payload.get('status'),
            'customer_id': payload.get('data', {}).get('customer_id'),
            'sku': payload.get('data', {}).get('sku'),
            'product_name': payload.get('data', {}).get('product_name'),
            'barcode': payload.get('data', {}).get('barcode'),
            'price': payload.get('data', {}).get('price'),
            'weight_g': payload.get('data', {}).get('weight_g')
        }
    
    def _parse_rfid_reading(self, payload: Dict) -> Dict[str, Any]:
        """Parse RFID reading data."""
        return {
            'type': 'rfid_reading',
            'timestamp': payload.get('timestamp'),
            'station_id': payload.get('station_id'),
            'status': payload.get('status'),
            'epc': payload.get('data', {}).get('epc'),
            'sku': payload.get('data', {}).get('sku'),
            'location': payload.get('data', {}).get('location')
        }
    
    def _parse_queue_monitoring(self, payload: Dict) -> Dict[str, Any]:
        """Parse queue monitoring data."""
        return {
            'type': 'queue_monitoring',
            'timestamp': payload.get('timestamp'),
            'station_id': payload.get('station_id'),
            'status': payload.get('status'),
            'customer_count': payload.get('data', {}).get('customer_count'),
            'average_dwell_time': payload.get('data', {}).get('average_dwell_time')
        }
    
    def _parse_product_recognition(self, payload: Dict) -> Dict[str, Any]:
        """Parse product recognition data."""
        return {
            'type': 'product_recognition',
            'timestamp': payload.get('timestamp'),
            'station_id': payload.get('station_id'),
            'status': payload.get('status'),
            'predicted_product': payload.get('data', {}).get('predicted_product'),
            'accuracy': payload.get('data', {}).get('accuracy')
        }
    
    def _parse_inventory_snapshot(self, payload: Dict) -> Dict[str, Any]:
        """Parse inventory snapshot data."""
        return {
            'type': 'inventory_snapshot',
            'timestamp': payload.get('timestamp'),
            'inventory_data': payload.get('data', {})
        }
    
    def get_product_info(self, sku: str) -> Optional[Dict]:
        """Get product information by SKU."""
        return self.products_data.get(sku)
    
    def get_customer_info(self, customer_id: str) -> Optional[Dict]:
        """Get customer information by ID."""
        return self.customers_data.get(customer_id)
    
    def get_expected_weight(self, sku: str) -> Optional[float]:
        """Get expected weight for a product SKU."""
        product = self.get_product_info(sku)
        return product['weight'] if product else None
    
    def get_expected_price(self, sku: str) -> Optional[float]:
        """Get expected price for a product SKU."""
        product = self.get_product_info(sku)
        return product['price'] if product else None