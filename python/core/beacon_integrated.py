"""
PrimeFusion-FANET Integrated Beacon Manager
===========================================

Integrates blockchain hash and milestone pig-backing into beacons.
Implements zero-overhead consensus through beacon-embedded metadata.

Beacon Structure:
- Standard beacon data (UAV position, status, etc.)
- 12-byte trailer: blockchain hash (8) + milestone data (4)

Author: PrimeFusion-FANET Team
Date: October 2025
Version: 1.0
"""

import time
from typing import Dict, Tuple, Optional
from dataclasses import dataclass
from blockchain import LinearBlockchain, BlockchainMetrics
from milestone import MilestonePigBacking, MilestoneMetrics
from cbor_optimizer import CBORCompressor, CompressionMetrics


@dataclass
class BeaconMetrics:
    """Performance metrics for beacon operations"""
    total_latency: float  # milliseconds
    beacon_size: int  # bytes
    trailer_size: int  # bytes
    compression_ratio: float
    success: bool
    timestamp: float


class IntegratedBeaconManager:
    """
    Integrated beacon manager with blockchain and milestone embedding.
    
    Features:
    - Embeds blockchain hash in beacon trailer
    - Embeds milestone pig-backing data
    - CBOR compression for beacon payload
    - Zero-overhead consensus
    """
    
    def __init__(self, node_id: int = 0):
        """
        Initialize integrated beacon manager.
        
        Args:
            node_id: Unique identifier for this UAV node
        """
        self.node_id = node_id
        
        # Initialize components
        self.blockchain = LinearBlockchain(node_id)
        self.milestone_mgr = MilestonePigBacking(node_id)
        self.cbor_compressor = CBORCompressor()
        
        # Performance tracking
        self.beacon_history = []
        
        # Beacon interval (seconds)
        self.beacon_interval = 1.0
        self.last_beacon_time = 0.0
    
    def add_blockchain_transaction(self, transaction_data: bytes) -> BlockchainMetrics:
        """
        Add a transaction to the blockchain.
        
        Args:
            transaction_data: Transaction data bytes
            
        Returns:
            Blockchain metrics
        """
        block, metrics = self.blockchain.add_block(transaction_data)
        return metrics
    
    def add_consensus_round(self, round_id: int):
        """
        Add a consensus round to milestone tracking.
        
        Args:
            round_id: Consensus round identifier
        """
        self.milestone_mgr.add_consensus_round(round_id)
    
    def generate_beacon(self, uav_data: Dict) -> Tuple[bytes, BeaconMetrics]:
        """
        Generate a complete beacon with embedded blockchain and milestone data.
        
        Args:
            uav_data: UAV state data (position, velocity, status, etc.)
            
        Returns:
            Tuple of (beacon_bytes, metrics)
        """
        start_time = time.time()
        
        try:
            # Step 1: Get blockchain hash
            blockchain_hash, hash_metrics = self.blockchain.get_latest_hash()
            
            # Step 2: Select and encode milestones
            milestone_indices, select_metrics = self.milestone_mgr.select_milestones()
            
            # Step 3: Create beacon trailer
            trailer, trailer_metrics = self.milestone_mgr.create_beacon_trailer(
                blockchain_hash,
                milestone_indices
            )
            
            # Step 4: Compress UAV data with CBOR
            compressed_data, compress_metrics = self.cbor_compressor.compress(uav_data)
            
            # Step 5: Combine compressed data + trailer
            beacon_bytes = compressed_data + trailer
            
            # Calculate total metrics
            total_latency = (time.time() - start_time) * 1000  # ms
            
            metrics = BeaconMetrics(
                total_latency=total_latency,
                beacon_size=len(beacon_bytes),
                trailer_size=len(trailer),
                compression_ratio=compress_metrics.compression_ratio,
                success=True,
                timestamp=time.time()
            )
            
            # Update history
            self.beacon_history.append({
                'timestamp': time.time(),
                'beacon_size': len(beacon_bytes),
                'trailer_size': len(trailer),
                'compression_ratio': compress_metrics.compression_ratio,
                'total_latency': total_latency
            })
            
            self.last_beacon_time = time.time()
            
            return beacon_bytes, metrics
            
        except Exception as e:
            error_metrics = BeaconMetrics(
                total_latency=999.0,
                beacon_size=0,
                trailer_size=0,
                compression_ratio=1.0,
                success=False,
                timestamp=time.time()
            )
            return b'', error_metrics
    
    def parse_beacon(self, beacon_bytes: bytes) -> Tuple[Dict, BeaconMetrics]:
        """
        Parse a received beacon to extract UAV data and metadata.
        
        Args:
            beacon_bytes: Complete beacon bytes
            
        Returns:
            Tuple of (parsed_data, metrics)
        """
        start_time = time.time()
        
        try:
            # Extract trailer (last 12 bytes)
            trailer = beacon_bytes[-12:]
            compressed_data = beacon_bytes[:-12]
            
            # Parse trailer
            trailer_data, trailer_metrics = self.milestone_mgr.parse_beacon_trailer(trailer)
            
            # Decompress UAV data
            uav_data, decompress_metrics = self.cbor_compressor.decompress(compressed_data)
            
            # Combine all data
            parsed_data = {
                'uav_data': uav_data,
                'blockchain_hash': trailer_data['blockchain_hash'],
                'milestone_indices': trailer_data['milestone_indices']
            }
            
            total_latency = (time.time() - start_time) * 1000  # ms
            
            metrics = BeaconMetrics(
                total_latency=total_latency,
                beacon_size=len(beacon_bytes),
                trailer_size=len(trailer),
                compression_ratio=decompress_metrics.compression_ratio,
                success=True,
                timestamp=time.time()
            )
            
            return parsed_data, metrics
            
        except Exception as e:
            error_metrics = BeaconMetrics(
                total_latency=999.0,
                beacon_size=len(beacon_bytes) if beacon_bytes else 0,
                trailer_size=0,
                compression_ratio=1.0,
                success=False,
                timestamp=time.time()
            )
            return {}, error_metrics
    
    def get_performance_stats(self) -> Dict:
        """Get comprehensive integrated beacon performance statistics"""
        if not self.beacon_history:
            return {
                'total_beacons': 0,
                'avg_beacon_size': 0,
                'avg_trailer_size': 0,
                'avg_compression_ratio': 0.0,
                'avg_total_latency': 0.0,
                'blockchain_stats': self.blockchain.get_performance_stats(),
                'milestone_stats': self.milestone_mgr.get_performance_stats(),
                'cbor_stats': self.cbor_compressor.get_compression_stats()
            }
        
        total_beacons = len(self.beacon_history)
        avg_size = sum(b['beacon_size'] for b in self.beacon_history) / total_beacons
        avg_trailer = sum(b['trailer_size'] for b in self.beacon_history) / total_beacons
        avg_ratio = sum(b['compression_ratio'] for b in self.beacon_history) / total_beacons
        avg_latency = sum(b['total_latency'] for b in self.beacon_history) / total_beacons
        
        return {
            'total_beacons': total_beacons,
            'avg_beacon_size': avg_size,
            'avg_trailer_size': avg_trailer,
            'avg_compression_ratio': avg_ratio,
            'avg_total_latency': avg_latency,
            'target_latency_met': avg_latency < 5.0,  # Target: <5ms
            'target_trailer_met': avg_trailer <= 12,  # Target: ≤12 bytes
            'blockchain_stats': self.blockchain.get_performance_stats(),
            'milestone_stats': self.milestone_mgr.get_performance_stats(),
            'cbor_stats': self.cbor_compressor.get_compression_stats()
        }


if __name__ == "__main__":
    # Test Integrated Beacon Manager
    print("=" * 60)
    print("Integrated Beacon Manager Test")
    print("=" * 60)
    
    beacon_mgr = IntegratedBeaconManager(node_id=1)
    
    # Add some blockchain transactions
    print("\nAdding blockchain transactions...")
    for i in range(5):
        tx_data = f"Transaction {i+1}: UAV consensus data".encode()
        metrics = beacon_mgr.add_blockchain_transaction(tx_data)
        print(f"  Transaction {i+1}: latency={metrics.operation_latency:.3f}ms")
    
    # Add consensus rounds
    print("\nAdding consensus rounds...")
    for i in range(10):
        beacon_mgr.add_consensus_round(i + 1)
    print(f"  Added 10 consensus rounds")
    
    # Generate beacons
    print("\nGenerating beacons...")
    for i in range(5):
        uav_data = {
            'uav_id': beacon_mgr.node_id,
            'position': {'latitude': 40.7128 + i*0.001, 'longitude': -74.0060, 'altitude': 100.0},
            'velocity': {'x': 1.5, 'y': 0.8, 'z': 0.0},
            'status': 'active',
            'battery': 85.5 - i*2,
            'timestamp': time.time()
        }
        
        beacon_bytes, metrics = beacon_mgr.generate_beacon(uav_data)
        print(f"  Beacon {i+1}: size={metrics.beacon_size}B, "
              f"trailer={metrics.trailer_size}B, "
              f"latency={metrics.total_latency:.3f}ms")
        
        # Test parsing the beacon
        if i == 0:  # Parse first beacon as test
            print("\n  Parsing beacon 1...")
            parsed, parse_metrics = beacon_mgr.parse_beacon(beacon_bytes)
            print(f"    UAV ID: {parsed['uav_data'].get('uav_id', 'N/A')}")
            print(f"    Blockchain hash: {parsed['blockchain_hash']}")
            print(f"    Milestone indices: {parsed['milestone_indices']}")
            print(f"    Parse latency: {parse_metrics.total_latency:.3f}ms")
    
    # Get comprehensive stats
    stats = beacon_mgr.get_performance_stats()
    
    print("\n" + "=" * 60)
    print("Integrated Performance Statistics")
    print("=" * 60)
    print(f"Total beacons: {stats['total_beacons']}")
    print(f"Avg beacon size: {stats['avg_beacon_size']:.1f} bytes")
    print(f"Avg trailer size: {stats['avg_trailer_size']:.1f} bytes")
    print(f"Avg compression ratio: {stats['avg_compression_ratio']:.3f}")
    print(f"Avg total latency: {stats['avg_total_latency']:.3f} ms")
    print(f"Target latency (<5ms) met: {stats['target_latency_met']}")
    print(f"Target trailer (≤12B) met: {stats['target_trailer_met']}")
    
    print("\nBlockchain Stats:")
    bc_stats = stats['blockchain_stats']
    print(f"  Total blocks: {bc_stats['total_blocks']}")
    print(f"  Chain valid: {bc_stats['chain_valid']}")
    print(f"  Session-MAC CPU reduction: {bc_stats['session_mac_cpu_reduction']:.1f}%")
    
    print("\nMilestone Stats:")
    ms_stats = stats['milestone_stats']
    print(f"  DAG tips tracked: {ms_stats['dag_tips_tracked']}")
    print(f"  Avg trailer latency: {ms_stats['avg_trailer_latency']:.3f} ms")
    
    print("\nCBOR Stats:")
    cbor_stats = stats['cbor_stats']
    print(f"  Total compressions: {cbor_stats['total_compressions']}")
    print(f"  Avg compression ratio: {cbor_stats['avg_compression_ratio']:.3f}")
    print(f"  Total bytes saved: {cbor_stats['total_bytes_saved']}")
    
    print("=" * 60)

