"""
PrimeFusion-FANET CBOR Compression
==================================

Implements UAV-optimized CBOR compression with custom dictionaries
for efficient data serialization in UAV swarm communications.

Author: PrimeFusion-FANET Team
Date: September 2025
Version: 2.0 (Complete Implementation)
"""

import time
import cbor2
import json
import gzip
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass


@dataclass
class CompressionMetrics:
    """Performance metrics for compression operations"""
    compression_latency: float  # milliseconds
    original_size: int  # bytes
    compressed_size: int  # bytes
    compression_ratio: float
    success: bool
    timestamp: float


class CBORCompressor:
    """
    UAV-optimized CBOR compression with custom dictionaries.
    
    Provides efficient serialization for UAV swarm data with
    specialized compression for common UAV message patterns.
    """
    
    def __init__(self):
        self.compression_history = []
        
        # UAV-specific compression dictionary
        self.uav_dictionary = {
            'position': 'p',
            'velocity': 'v', 
            'altitude': 'a',
            'heading': 'h',
            'timestamp': 't',
            'uav_id': 'id',
            'battery': 'b',
            'status': 's',
            'mission': 'm',
            'waypoint': 'w',
            'formation': 'f',
            'consensus': 'c',
            'transaction': 'tx',
            'beacon': 'bc',
            'coordinate': 'coord',
            'latitude': 'lat',
            'longitude': 'lon',
            'emergency': 'emg',
            'communication': 'comm'
        }
        
        # Performance targets
        self.TARGET_COMPRESSION_RATIO = 0.67  # 67% compression
        self.TARGET_LATENCY = 0.1  # ms
        
    def compress(self, data) -> Tuple[bytes, CompressionMetrics]:
        """
        Compress data using UAV-optimized CBOR.
        
        Args:
            data: Dictionary or bytes data to compress
            
        Returns:
            Tuple of (compressed_data, metrics)
        """
        start_time = time.time()
        
        try:
            # Handle different input types
            if isinstance(data, bytes):
                # Convert bytes to dict if possible
                try:
                    data = json.loads(data.decode())
                except:
                    # If not JSON, treat as raw data
                    original_size = len(data)
                    compressed_data = gzip.compress(data, compresslevel=6)
                    
                    compression_time = (time.time() - start_time) * 1000
                    metrics = CompressionMetrics(
                        compression_latency=compression_time,
                        original_size=original_size,
                        compressed_size=len(compressed_data),
                        compression_ratio=len(compressed_data) / original_size,
                        success=True,
                        timestamp=time.time()
                    )
                    return compressed_data, metrics
            
            # Apply dictionary compression
            compressed_dict = self._apply_dictionary_compression(data)
            
            # Serialize with CBOR
            original_json = json.dumps(data, separators=(',', ':')).encode()
            cbor_data = cbor2.dumps(compressed_dict)
            
            # Additional gzip compression for better ratios
            final_compressed = gzip.compress(cbor_data, compresslevel=6)
            
            # Calculate metrics
            compression_time = (time.time() - start_time) * 1000  # ms
            original_size = len(original_json)
            compressed_size = len(final_compressed)
            compression_ratio = compressed_size / original_size if original_size > 0 else 1.0
            
            metrics = CompressionMetrics(
                compression_latency=compression_time,
                original_size=original_size,
                compressed_size=compressed_size,
                compression_ratio=compression_ratio,
                success=True,
                timestamp=time.time()
            )
            
            # Update history
            self.compression_history.append({
                'timestamp': time.time(),
                'original_size': original_size,
                'compressed_size': compressed_size,
                'ratio': compression_ratio,
                'latency': compression_time
            })
            
            return final_compressed, metrics
            
        except Exception as e:
            error_metrics = CompressionMetrics(
                compression_latency=999.0,
                original_size=len(str(data).encode()) if data else 0,
                compressed_size=0,
                compression_ratio=1.0,
                success=False,
                timestamp=time.time()
            )
            return b'', error_metrics
    
    def decompress(self, compressed_data: bytes) -> Tuple[Dict[Any, Any], CompressionMetrics]:
        """
        Decompress CBOR data back to original format.
        
        Args:
            compressed_data: Compressed data bytes
            
        Returns:
            Tuple of (decompressed_data, metrics)
        """
        start_time = time.time()
        
        try:
            # Decompress gzip
            cbor_data = gzip.decompress(compressed_data)
            
            # Deserialize CBOR
            compressed_dict = cbor2.loads(cbor_data)
            
            # Reverse dictionary compression
            original_data = self._reverse_dictionary_compression(compressed_dict)
            
            # Calculate metrics
            decompression_time = (time.time() - start_time) * 1000  # ms
            
            metrics = CompressionMetrics(
                compression_latency=decompression_time,
                original_size=len(compressed_data),
                compressed_size=len(json.dumps(original_data, separators=(',', ':')).encode()),
                compression_ratio=1.0,  # Not applicable for decompression
                success=True,
                timestamp=time.time()
            )
            
            return original_data, metrics
            
        except Exception as e:
            error_metrics = CompressionMetrics(
                compression_latency=999.0,
                original_size=len(compressed_data) if compressed_data else 0,
                compressed_size=0,
                compression_ratio=1.0,
                success=False,
                timestamp=time.time()
            )
            return {}, error_metrics
    
    def _apply_dictionary_compression(self, data: Dict[Any, Any]) -> Dict[Any, Any]:
        """Apply UAV dictionary compression to reduce key sizes"""
        if not isinstance(data, dict):
            return data
        
        compressed = {}
        for key, value in data.items():
            # Compress key using dictionary
            compressed_key = self.uav_dictionary.get(str(key), key)
            
            # Recursively compress nested dictionaries
            if isinstance(value, dict):
                compressed_value = self._apply_dictionary_compression(value)
            elif isinstance(value, list):
                compressed_value = [
                    self._apply_dictionary_compression(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                compressed_value = value
            
            compressed[compressed_key] = compressed_value
        
        return compressed
    
    def _reverse_dictionary_compression(self, data: Dict[Any, Any]) -> Dict[Any, Any]:
        """Reverse dictionary compression to restore original keys"""
        if not isinstance(data, dict):
            return data
        
        # Create reverse dictionary
        reverse_dict = {v: k for k, v in self.uav_dictionary.items()}
        
        decompressed = {}
        for key, value in data.items():
            # Decompress key using reverse dictionary
            original_key = reverse_dict.get(str(key), key)
            
            # Recursively decompress nested dictionaries
            if isinstance(value, dict):
                decompressed_value = self._reverse_dictionary_compression(value)
            elif isinstance(value, list):
                decompressed_value = [
                    self._reverse_dictionary_compression(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                decompressed_value = value
            
            decompressed[original_key] = decompressed_value
        
        return decompressed
    
    def get_compression_stats(self) -> Dict:
        """Get comprehensive compression statistics"""
        if not self.compression_history:
            return {
                'total_compressions': 0,
                'avg_compression_ratio': 0.0,
                'avg_latency': 0.0,
                'total_bytes_saved': 0
            }
        
        total_compressions = len(self.compression_history)
        avg_ratio = sum(h['ratio'] for h in self.compression_history) / total_compressions
        avg_latency = sum(h['latency'] for h in self.compression_history) / total_compressions
        total_saved = sum(h['original_size'] - h['compressed_size'] for h in self.compression_history)
        
        return {
            'total_compressions': total_compressions,
            'avg_compression_ratio': avg_ratio,
            'avg_latency': avg_latency,
            'total_bytes_saved': total_saved,
            'target_ratio_met': avg_ratio <= self.TARGET_COMPRESSION_RATIO,
            'target_latency_met': avg_latency <= self.TARGET_LATENCY
        }


if __name__ == "__main__":
    # Test CBOR compression
    compressor = CBORCompressor()
    
    # Test data
    test_data = {
        'uav_id': 1,
        'position': {'latitude': 40.7128, 'longitude': -74.0060, 'altitude': 100.0},
        'velocity': {'x': 1.5, 'y': 0.8, 'z': 0.0},
        'status': 'active',
        'battery': 85.5,
        'mission': 'patrol',
        'timestamp': time.time()
    }
    
    # Test compression
    compressed_data, metrics = compressor.compress(test_data)
    print(f"Compression successful: {metrics.success}")
    print(f"Original size: {metrics.original_size} bytes")
    print(f"Compressed size: {metrics.compressed_size} bytes")
    print(f"Compression ratio: {metrics.compression_ratio:.3f}")
    print(f"Compression latency: {metrics.compression_latency:.3f} ms")
    
    # Test decompression
    decompressed_data, decomp_metrics = compressor.decompress(compressed_data)
    print(f"Decompression successful: {decomp_metrics.success}")
    print(f"Data matches: {decompressed_data == test_data}")

