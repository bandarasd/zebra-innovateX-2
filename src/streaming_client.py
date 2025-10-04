#!/usr/bin/env python3
"""
Streaming client for Project Sentinel data ingestion.
Connects to the streaming server and processes live JSONL data streams.
"""

import socket
import json
import threading
import time
from typing import Dict, List, Callable, Any
import logging

class StreamingClient:
    """Client to connect to the Project Sentinel streaming server."""
    
    def __init__(self, host: str = 'localhost', port: int = 8765):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        self.callbacks: Dict[str, List[Callable]] = {}
        self.logger = logging.getLogger(__name__)
        
    def register_callback(self, dataset_name: str, callback: Callable[[Dict], None]):
        """Register a callback function for a specific dataset."""
        if dataset_name not in self.callbacks:
            self.callbacks[dataset_name] = []
        self.callbacks[dataset_name].append(callback)
    
    def connect(self) -> bool:
        """Establish connection to the streaming server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.logger.info(f"Connected to streaming server at {self.host}:{self.port}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to streaming server: {e}")
            return False
    
    def start_streaming(self):
        """Start the streaming process in a separate thread."""
        if not self.connect():
            return False
            
        self.running = True
        self.stream_thread = threading.Thread(target=self._stream_loop, daemon=True)
        self.stream_thread.start()
        return True
    
    def stop_streaming(self):
        """Stop the streaming process."""
        self.running = False
        if self.socket:
            self.socket.close()
    
    def _stream_loop(self):
        """Main streaming loop to receive and process data."""
        buffer = ""
        
        try:
            while self.running:
                data = self.socket.recv(4096).decode('utf-8')
                if not data:
                    break
                    
                buffer += data
                lines = buffer.split('\n')
                buffer = lines[-1]  # Keep incomplete line in buffer
                
                for line in lines[:-1]:
                    if line.strip():
                        try:
                            event = json.loads(line)
                            self._process_event(event)
                        except json.JSONDecodeError as e:
                            self.logger.warning(f"Failed to parse JSON: {e}")
                            
        except Exception as e:
            self.logger.error(f"Streaming error: {e}")
        finally:
            self.socket.close()
    
    def _process_event(self, event: Dict[str, Any]):
        """Process a received event and call appropriate callbacks."""
        dataset_name = event.get('dataset', 'unknown')
        
        # Call registered callbacks for this dataset
        if dataset_name in self.callbacks:
            for callback in self.callbacks[dataset_name]:
                try:
                    callback(event)
                except Exception as e:
                    self.logger.error(f"Callback error for {dataset_name}: {e}")


def test_streaming_client():
    """Test function to verify streaming client works."""
    client = StreamingClient()
    
    def pos_callback(event):
        print(f"POS: {event}")
    
    def rfid_callback(event):
        print(f"RFID: {event}")
    
    client.register_callback('pos_transactions', pos_callback)
    client.register_callback('rfid_readings', rfid_callback)
    
    if client.start_streaming():
        try:
            time.sleep(10)  # Stream for 10 seconds
        except KeyboardInterrupt:
            pass
        finally:
            client.stop_streaming()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_streaming_client()