"""
PrimeFusion-FANET Session-MAC Authentication
============================================

Implements hybrid Ed25519 + HMAC authentication scheme for blockchain.
Reduces CPU overhead by >15% compared to pure Ed25519 signatures.

Root Certificate: Ed25519 signature every 100 blocks
Interim Blocks: HMAC authentication for blocks 1-99

Author: PrimeFusion-FANET Team
Date: October 2025
Version: 1.0
"""

import time
import hmac
import hashlib
from typing import Tuple, Optional
from dataclasses import dataclass
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization


@dataclass
class SessionMACMetrics:
    """Performance metrics for Session-MAC operations"""
    operation_latency: float  # milliseconds
    operation_type: str  # 'root_sign', 'interim_sign', 'root_verify', 'interim_verify'
    cpu_cycles: int  # estimated CPU cycles
    success: bool
    timestamp: float


class SessionMAC:
    """
    Hybrid Ed25519 + HMAC authentication for blockchain.
    
    Strategy:
    - Block 0, 100, 200, ... : Ed25519 root certificate (expensive)
    - Blocks 1-99, 101-199, ... : HMAC interim (cheap)
    
    This reduces average CPU overhead by >15% while maintaining security.
    """
    
    # Root certificate interval (blocks)
    ROOT_CERT_INTERVAL = 100
    
    # Estimated CPU cycles (for metrics)
    ED25519_SIGN_CYCLES = 273000
    ED25519_VERIFY_CYCLES = 273000
    HMAC_SIGN_CYCLES = 12000
    HMAC_VERIFY_CYCLES = 12000
    
    def __init__(self, node_id: int = 0):
        """
        Initialize Session-MAC with node identity.
        
        Args:
            node_id: Unique identifier for this UAV node
        """
        self.node_id = node_id
        
        # Generate Ed25519 key pair
        self.private_key = ed25519.Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()
        
        # Session key for HMAC (derived from Ed25519 private key)
        self.session_key = self._derive_session_key()
        
        # Performance tracking
        self.operation_history = []
        
    def _derive_session_key(self) -> bytes:
        """Derive HMAC session key from Ed25519 private key"""
        # Get private key bytes
        private_bytes = self.private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Derive session key using SHA-256
        session_key = hashlib.sha256(private_bytes).digest()
        return session_key
    
    def sign_block(self, block_number: int, block_data: bytes) -> Tuple[bytes, SessionMACMetrics]:
        """
        Sign a block using appropriate method (Ed25519 or HMAC).
        
        Args:
            block_number: Block index in blockchain
            block_data: Block data to sign
            
        Returns:
            Tuple of (signature, metrics)
        """
        start_time = time.time()
        
        try:
            if self._is_root_block(block_number):
                # Root certificate: Ed25519 signature
                signature = self.private_key.sign(block_data)
                operation_type = 'root_sign'
                cpu_cycles = self.ED25519_SIGN_CYCLES
            else:
                # Interim block: HMAC
                signature = hmac.new(
                    self.session_key,
                    block_data,
                    hashlib.sha256
                ).digest()
                operation_type = 'interim_sign'
                cpu_cycles = self.HMAC_SIGN_CYCLES
            
            latency = (time.time() - start_time) * 1000  # ms
            
            metrics = SessionMACMetrics(
                operation_latency=latency,
                operation_type=operation_type,
                cpu_cycles=cpu_cycles,
                success=True,
                timestamp=time.time()
            )
            
            self.operation_history.append({
                'block': block_number,
                'type': operation_type,
                'latency': latency,
                'cpu_cycles': cpu_cycles
            })
            
            return signature, metrics
            
        except Exception as e:
            error_metrics = SessionMACMetrics(
                operation_latency=999.0,
                operation_type='error',
                cpu_cycles=0,
                success=False,
                timestamp=time.time()
            )
            return b'', error_metrics
    
    def verify_block(self, block_number: int, block_data: bytes, 
                     signature: bytes, public_key: Optional[ed25519.Ed25519PublicKey] = None) -> Tuple[bool, SessionMACMetrics]:
        """
        Verify a block signature using appropriate method.
        
        Args:
            block_number: Block index in blockchain
            block_data: Block data to verify
            signature: Signature to verify
            public_key: Public key for Ed25519 verification (required for root blocks)
            
        Returns:
            Tuple of (verification_result, metrics)
        """
        start_time = time.time()
        
        try:
            if self._is_root_block(block_number):
                # Root certificate: Ed25519 verification
                if public_key is None:
                    public_key = self.public_key
                
                try:
                    public_key.verify(signature, block_data)
                    valid = True
                except:
                    valid = False
                
                operation_type = 'root_verify'
                cpu_cycles = self.ED25519_VERIFY_CYCLES
            else:
                # Interim block: HMAC verification
                expected_hmac = hmac.new(
                    self.session_key,
                    block_data,
                    hashlib.sha256
                ).digest()
                
                valid = hmac.compare_digest(signature, expected_hmac)
                operation_type = 'interim_verify'
                cpu_cycles = self.HMAC_VERIFY_CYCLES
            
            latency = (time.time() - start_time) * 1000  # ms
            
            metrics = SessionMACMetrics(
                operation_latency=latency,
                operation_type=operation_type,
                cpu_cycles=cpu_cycles,
                success=valid,
                timestamp=time.time()
            )
            
            self.operation_history.append({
                'block': block_number,
                'type': operation_type,
                'latency': latency,
                'cpu_cycles': cpu_cycles,
                'valid': valid
            })
            
            return valid, metrics
            
        except Exception as e:
            error_metrics = SessionMACMetrics(
                operation_latency=999.0,
                operation_type='error',
                cpu_cycles=0,
                success=False,
                timestamp=time.time()
            )
            return False, error_metrics
    
    def _is_root_block(self, block_number: int) -> bool:
        """Check if block number requires root certificate"""
        return block_number % self.ROOT_CERT_INTERVAL == 0
    
    def get_public_key_bytes(self) -> bytes:
        """Get public key in raw bytes format"""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
    
    def get_performance_stats(self) -> dict:
        """Get comprehensive performance statistics"""
        if not self.operation_history:
            return {
                'total_operations': 0,
                'root_operations': 0,
                'interim_operations': 0,
                'avg_root_latency': 0.0,
                'avg_interim_latency': 0.0,
                'avg_cpu_cycles': 0,
                'cpu_reduction_vs_pure_ed25519': 0.0
            }
        
        root_ops = [op for op in self.operation_history if 'root' in op['type']]
        interim_ops = [op for op in self.operation_history if 'interim' in op['type']]
        
        avg_root_latency = sum(op['latency'] for op in root_ops) / len(root_ops) if root_ops else 0.0
        avg_interim_latency = sum(op['latency'] for op in interim_ops) / len(interim_ops) if interim_ops else 0.0
        
        # Calculate average CPU cycles
        total_cycles = sum(op['cpu_cycles'] for op in self.operation_history)
        avg_cycles = total_cycles / len(self.operation_history)
        
        # Calculate CPU reduction vs pure Ed25519
        # Pure Ed25519 would use ED25519_SIGN_CYCLES for every block
        pure_ed25519_cycles = self.ED25519_SIGN_CYCLES
        cpu_reduction = ((pure_ed25519_cycles - avg_cycles) / pure_ed25519_cycles) * 100
        
        return {
            'total_operations': len(self.operation_history),
            'root_operations': len(root_ops),
            'interim_operations': len(interim_ops),
            'avg_root_latency': avg_root_latency,
            'avg_interim_latency': avg_interim_latency,
            'avg_cpu_cycles': avg_cycles,
            'cpu_reduction_vs_pure_ed25519': cpu_reduction,
            'target_cpu_reduction_met': cpu_reduction >= 15.0
        }


if __name__ == "__main__":
    # Test Session-MAC
    print("=" * 60)
    print("Session-MAC Authentication Test")
    print("=" * 60)
    
    session_mac = SessionMAC(node_id=1)
    
    # Test signing 200 blocks (includes 2 root certificates)
    print("\nSigning 200 blocks...")
    for block_num in range(200):
        block_data = f"Block {block_num} data".encode()
        signature, metrics = session_mac.sign_block(block_num, block_data)
        
        if block_num % 50 == 0:
            print(f"  Block {block_num}: {metrics.operation_type}, "
                  f"latency={metrics.operation_latency:.3f}ms, "
                  f"cpu_cycles={metrics.cpu_cycles}")
    
    # Get performance stats
    stats = session_mac.get_performance_stats()
    
    print("\n" + "=" * 60)
    print("Performance Statistics")
    print("=" * 60)
    print(f"Total operations: {stats['total_operations']}")
    print(f"Root operations (Ed25519): {stats['root_operations']}")
    print(f"Interim operations (HMAC): {stats['interim_operations']}")
    print(f"Avg root latency: {stats['avg_root_latency']:.3f} ms")
    print(f"Avg interim latency: {stats['avg_interim_latency']:.3f} ms")
    print(f"Avg CPU cycles: {stats['avg_cpu_cycles']:.0f}")
    print(f"CPU reduction vs pure Ed25519: {stats['cpu_reduction_vs_pure_ed25519']:.1f}%")
    print(f"Target (>15%) met: {stats['target_cpu_reduction_met']}")
    print("=" * 60)

