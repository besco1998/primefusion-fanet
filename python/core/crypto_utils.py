"""
PrimeFusion-FANET Cryptography
==============================

Implements lightweight cryptographic functions for UAV swarm security.
Provides HMAC authentication, CRC error detection, and key management.

Author: PrimeFusion-FANET Team
Date: September 2025
Version: 2.0 (Complete Implementation)
"""

import time
import hashlib
import hmac
import secrets
from typing import List, Tuple, Dict
from dataclasses import dataclass


@dataclass
class CryptoMetrics:
    """Performance metrics for cryptographic operations"""
    operation_time: float  # milliseconds
    data_size: int  # bytes
    success: bool
    timestamp: float


class PrimeFusionCrypto:
    """
    Lightweight cryptography for UAV swarm communications.
    
    Implements HMAC-SHA256 for authentication and CRC8 for error detection,
    optimized for real-time UAV operations with minimal overhead.
    """
    
    def __init__(self):
        self.crypto_history = []
        self.shared_keys = {}  # UAV_ID -> shared_key mapping
        
        # Performance targets
        self.TARGET_HMAC_TIME = 0.5  # ms
        self.TARGET_CRC_TIME = 0.1   # ms
        
        # CRC8 lookup table for fast computation
        self.crc8_table = self._generate_crc8_table()
    
    def generate_shared_key(self, uav_id: int) -> str:
        """Generate a shared key for UAV authentication"""
        key = secrets.token_hex(16)  # 128-bit key
        self.shared_keys[uav_id] = key
        return key
    
    def set_shared_key(self, uav_id: int, key: str):
        """Set shared key for specific UAV"""
        self.shared_keys[uav_id] = key
    
    def encrypt(self, data: bytes, uav_id: int = 1) -> Tuple[bytes, CryptoMetrics]:
        """Simple encryption using HMAC (for demonstration)"""
        return self.compute_hmac(data, uav_id)
    
    def decrypt(self, encrypted_data: bytes, uav_id: int = 1) -> Tuple[bytes, CryptoMetrics]:
        """Simple decryption (returns original data for demonstration)"""
        start_time = time.time()
        
        metrics = CryptoMetrics(
            operation_time=(time.time() - start_time) * 1000,
            data_size=len(encrypted_data),
            success=True,
            timestamp=time.time()
        )
        
        return encrypted_data, metrics
    
    def compute_hmac(self, data: bytes, uav_id: int) -> Tuple[bytes, CryptoMetrics]:
        """Compute HMAC-SHA256 authentication tag."""
        start_time = time.time()
        
        try:
            if uav_id not in self.shared_keys:
                key = self.generate_shared_key(uav_id)
            else:
                key = self.shared_keys[uav_id]
            
            hmac_tag = hmac.new(key.encode(), data, hashlib.sha256).digest()[:8]  # 8-byte tag
            
            operation_time = (time.time() - start_time) * 1000
            
            metrics = CryptoMetrics(
                operation_time=operation_time,
                data_size=len(data),
                success=True,
                timestamp=time.time()
            )
            
            return hmac_tag, metrics
            
        except Exception as e:
            error_metrics = CryptoMetrics(
                operation_time=999.0,
                data_size=len(data) if data else 0,
                success=False,
                timestamp=time.time()
            )
            return b'', error_metrics
    
    def compute_crc8(self, data: bytes) -> Tuple[int, CryptoMetrics]:
        """Compute CRC8 error detection code."""
        start_time = time.time()
        
        try:
            crc = 0
            for byte in data:
                crc = self.crc8_table[crc ^ byte]
            
            operation_time = (time.time() - start_time) * 1000
            
            metrics = CryptoMetrics(
                operation_time=operation_time,
                data_size=len(data),
                success=True,
                timestamp=time.time()
            )
            
            return crc, metrics
            
        except Exception as e:
            error_metrics = CryptoMetrics(
                operation_time=999.0,
                data_size=len(data) if data else 0,
                success=False,
                timestamp=time.time()
            )
            return 0, error_metrics
    
    def _generate_crc8_table(self) -> List[int]:
        """Generate CRC8 lookup table for fast computation"""
        table = []
        for i in range(256):
            crc = i
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ 0x07  # CRC-8-CCITT polynomial
                else:
                    crc = crc << 1
                crc &= 0xFF
            table.append(crc)
        return table
    
    def secure_beacon_trailer(self, beacon_data: bytes, uav_id: int) -> Tuple[bytes, CryptoMetrics]:
        """Create secure beacon trailer with HMAC and CRC8."""
        start_time = time.time()
        
        try:
            # Compute HMAC (8 bytes)
            hmac_tag, hmac_metrics = self.compute_hmac(beacon_data, uav_id)
            if not hmac_metrics.success:
                raise Exception("HMAC computation failed")
            
            # Compute CRC8 (1 byte)
            crc8_value, crc_metrics = self.compute_crc8(beacon_data + hmac_tag)
            if not crc_metrics.success:
                raise Exception("CRC8 computation failed")
            
            # Create secure trailer: HMAC(8) + CRC8(1) + UAV_ID(1) = 10 bytes
            trailer = hmac_tag + crc8_value.to_bytes(1, 'big') + uav_id.to_bytes(1, 'big')
            
            total_time = (time.time() - start_time) * 1000
            
            metrics = CryptoMetrics(
                operation_time=total_time,
                data_size=len(beacon_data),
                success=True,
                timestamp=time.time()
            )
            
            return trailer, metrics
            
        except Exception as e:
            error_metrics = CryptoMetrics(
                operation_time=999.0,
                data_size=len(beacon_data) if beacon_data else 0,
                success=False,
                timestamp=time.time()
            )
            return b'', error_metrics


if __name__ == "__main__":
    # Test cryptographic functionality
    crypto = PrimeFusionCrypto()
    
    # Generate keys for test UAVs
    uav_id = 1
    key = crypto.generate_shared_key(uav_id)
    print(f"Generated key for UAV {uav_id}: {key[:16]}...")
    
    # Test beacon security
    test_beacon = b"test_beacon_data_payload"
    trailer, metrics = crypto.secure_beacon_trailer(test_beacon, uav_id)
    
    print(f"Secure trailer created: {metrics.success}")
    print(f"Operation time: {metrics.operation_time:.3f} ms")
    print(f"Trailer length: {len(trailer)} bytes")

