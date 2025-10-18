"""
PrimeFusion-FANET Milestone Pig-Backing
=======================================

Implements milestone pig-backing for embedding DAG consensus in beacons.
Reduces airtime overhead by >90% by eliminating separate consensus messages.

12-bit encoding: 3 DAG tips × 4 bits each
Beacon trailer: 12 bytes total (8-byte blockchain hash + 4-byte milestone data)

Author: PrimeFusion-FANET Team
Date: October 2025
Version: 1.0
"""

import time
import struct
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass


@dataclass
class MilestoneMetrics:
    """Performance metrics for milestone operations"""
    operation_latency: float  # milliseconds
    operation_type: str  # 'encode', 'decode', 'select'
    milestone_count: int
    success: bool
    timestamp: float


class MilestonePigBacking:
    """
    Milestone pig-backing for beacon-embedded consensus.
    
    Strategy:
    - Select last 3 consensus rounds as DAG tips
    - Encode each tip as 4-bit index (0-15)
    - Pack into 12 bits (1.5 bytes)
    - Combine with blockchain hash for 12-byte beacon trailer
    
    This achieves >90% airtime reduction vs. separate consensus messages.
    """
    
    # Maximum DAG tips to track
    MAX_DAG_TIPS = 16  # 4-bit encoding allows 0-15
    
    # Milestone encoding size
    MILESTONE_BITS = 12  # 3 tips × 4 bits
    MILESTONE_BYTES = 2  # 12 bits = 1.5 bytes, rounded to 2
    
    # Beacon trailer size
    BLOCKCHAIN_HASH_BYTES = 8
    TOTAL_TRAILER_BYTES = BLOCKCHAIN_HASH_BYTES + 4  # 8 + 4 = 12 bytes
    
    def __init__(self, node_id: int = 0):
        """
        Initialize milestone pig-backing.
        
        Args:
            node_id: Unique identifier for this UAV node
        """
        self.node_id = node_id
        self.dag_tips: List[int] = []  # Recent consensus round IDs
        self.operation_history = []
        
    def add_consensus_round(self, round_id: int):
        """
        Add a new consensus round to DAG tips.
        
        Args:
            round_id: Consensus round identifier
        """
        self.dag_tips.append(round_id)
        
        # Keep only last MAX_DAG_TIPS
        if len(self.dag_tips) > self.MAX_DAG_TIPS:
            self.dag_tips = self.dag_tips[-self.MAX_DAG_TIPS:]
    
    def select_milestones(self) -> Tuple[List[int], MilestoneMetrics]:
        """
        Select the last 3 consensus rounds as milestones.
        
        Returns:
            Tuple of (milestone_indices, metrics)
        """
        start_time = time.time()
        
        try:
            # Select last 3 DAG tips (or fewer if not enough)
            if len(self.dag_tips) >= 3:
                milestones = self.dag_tips[-3:]
            elif len(self.dag_tips) > 0:
                # Pad with zeros if fewer than 3
                milestones = self.dag_tips + [0] * (3 - len(self.dag_tips))
            else:
                # No tips yet, use zeros
                milestones = [0, 0, 0]
            
            # Convert to indices (0-15)
            milestone_indices = []
            for tip in milestones:
                # Map tip ID to index in current DAG tips list
                if tip in self.dag_tips:
                    index = self.dag_tips.index(tip)
                else:
                    index = 0
                
                # Ensure index fits in 4 bits
                milestone_indices.append(min(index, 15))
            
            latency = (time.time() - start_time) * 1000  # ms
            
            metrics = MilestoneMetrics(
                operation_latency=latency,
                operation_type='select',
                milestone_count=len(milestone_indices),
                success=True,
                timestamp=time.time()
            )
            
            self.operation_history.append({
                'operation': 'select',
                'milestones': milestone_indices,
                'latency': latency,
                'timestamp': time.time()
            })
            
            return milestone_indices, metrics
            
        except Exception as e:
            error_metrics = MilestoneMetrics(
                operation_latency=999.0,
                operation_type='select',
                milestone_count=0,
                success=False,
                timestamp=time.time()
            )
            return [0, 0, 0], error_metrics
    
    def encode_milestones(self, milestone_indices: List[int]) -> Tuple[bytes, MilestoneMetrics]:
        """
        Encode 3 milestone indices into 12 bits (2 bytes).
        
        Args:
            milestone_indices: List of 3 indices (0-15 each)
            
        Returns:
            Tuple of (encoded_bytes, metrics)
        """
        start_time = time.time()
        
        try:
            # Ensure we have exactly 3 indices
            if len(milestone_indices) != 3:
                milestone_indices = (milestone_indices + [0, 0, 0])[:3]
            
            # Pack 3 × 4-bit values into 12 bits
            # Format: [tip1:4][tip2:4][tip3:4][padding:4]
            packed_value = (
                (milestone_indices[0] & 0x0F) << 12 |  # First 4 bits
                (milestone_indices[1] & 0x0F) << 8  |  # Next 4 bits
                (milestone_indices[2] & 0x0F) << 4     # Next 4 bits
                # Last 4 bits are padding (0)
            )
            
            # Convert to 2 bytes
            encoded_bytes = struct.pack('>H', packed_value)
            
            latency = (time.time() - start_time) * 1000  # ms
            
            metrics = MilestoneMetrics(
                operation_latency=latency,
                operation_type='encode',
                milestone_count=3,
                success=True,
                timestamp=time.time()
            )
            
            self.operation_history.append({
                'operation': 'encode',
                'indices': milestone_indices,
                'encoded': encoded_bytes.hex(),
                'latency': latency,
                'timestamp': time.time()
            })
            
            return encoded_bytes, metrics
            
        except Exception as e:
            error_metrics = MilestoneMetrics(
                operation_latency=999.0,
                operation_type='encode',
                milestone_count=0,
                success=False,
                timestamp=time.time()
            )
            return b'\x00\x00', error_metrics
    
    def decode_milestones(self, encoded_bytes: bytes) -> Tuple[List[int], MilestoneMetrics]:
        """
        Decode 2 bytes back into 3 milestone indices.
        
        Args:
            encoded_bytes: 2-byte encoded milestone data
            
        Returns:
            Tuple of (milestone_indices, metrics)
        """
        start_time = time.time()
        
        try:
            # Unpack 2 bytes
            packed_value = struct.unpack('>H', encoded_bytes)[0]
            
            # Extract 3 × 4-bit values
            tip1 = (packed_value >> 12) & 0x0F
            tip2 = (packed_value >> 8) & 0x0F
            tip3 = (packed_value >> 4) & 0x0F
            
            milestone_indices = [tip1, tip2, tip3]
            
            latency = (time.time() - start_time) * 1000  # ms
            
            metrics = MilestoneMetrics(
                operation_latency=latency,
                operation_type='decode',
                milestone_count=3,
                success=True,
                timestamp=time.time()
            )
            
            self.operation_history.append({
                'operation': 'decode',
                'encoded': encoded_bytes.hex(),
                'indices': milestone_indices,
                'latency': latency,
                'timestamp': time.time()
            })
            
            return milestone_indices, metrics
            
        except Exception as e:
            error_metrics = MilestoneMetrics(
                operation_latency=999.0,
                operation_type='decode',
                milestone_count=0,
                success=False,
                timestamp=time.time()
            )
            return [0, 0, 0], error_metrics
    
    def create_beacon_trailer(self, blockchain_hash: str, milestone_indices: List[int]) -> Tuple[bytes, MilestoneMetrics]:
        """
        Create complete 12-byte beacon trailer.
        
        Format:
        - Bytes 0-7: Blockchain hash (8 bytes)
        - Bytes 8-9: Milestone data (2 bytes, 12 bits used)
        - Bytes 10-11: Reserved/padding (2 bytes)
        
        Args:
            blockchain_hash: 8-byte blockchain hash (16 hex chars)
            milestone_indices: List of 3 milestone indices
            
        Returns:
            Tuple of (trailer_bytes, metrics)
        """
        start_time = time.time()
        
        try:
            # Convert blockchain hash to bytes (first 8 bytes)
            hash_bytes = bytes.fromhex(blockchain_hash[:16])
            
            # Encode milestones
            milestone_bytes, _ = self.encode_milestones(milestone_indices)
            
            # Create trailer: hash (8) + milestone (2) + padding (2)
            trailer = hash_bytes + milestone_bytes + b'\x00\x00'
            
            latency = (time.time() - start_time) * 1000  # ms
            
            metrics = MilestoneMetrics(
                operation_latency=latency,
                operation_type='create_trailer',
                milestone_count=3,
                success=True,
                timestamp=time.time()
            )
            
            self.operation_history.append({
                'operation': 'create_trailer',
                'hash': blockchain_hash[:16],
                'milestones': milestone_indices,
                'trailer_size': len(trailer),
                'latency': latency,
                'timestamp': time.time()
            })
            
            return trailer, metrics
            
        except Exception as e:
            error_metrics = MilestoneMetrics(
                operation_latency=999.0,
                operation_type='create_trailer',
                milestone_count=0,
                success=False,
                timestamp=time.time()
            )
            return b'\x00' * 12, error_metrics
    
    def parse_beacon_trailer(self, trailer: bytes) -> Tuple[Dict, MilestoneMetrics]:
        """
        Parse 12-byte beacon trailer.
        
        Args:
            trailer: 12-byte beacon trailer
            
        Returns:
            Tuple of (parsed_data, metrics)
        """
        start_time = time.time()
        
        try:
            # Extract blockchain hash (bytes 0-7)
            hash_bytes = trailer[:8]
            blockchain_hash = hash_bytes.hex()
            
            # Extract milestone data (bytes 8-9)
            milestone_bytes = trailer[8:10]
            milestone_indices, _ = self.decode_milestones(milestone_bytes)
            
            parsed_data = {
                'blockchain_hash': blockchain_hash,
                'milestone_indices': milestone_indices,
                'trailer_size': len(trailer)
            }
            
            latency = (time.time() - start_time) * 1000  # ms
            
            metrics = MilestoneMetrics(
                operation_latency=latency,
                operation_type='parse_trailer',
                milestone_count=3,
                success=True,
                timestamp=time.time()
            )
            
            return parsed_data, metrics
            
        except Exception as e:
            error_metrics = MilestoneMetrics(
                operation_latency=999.0,
                operation_type='parse_trailer',
                milestone_count=0,
                success=False,
                timestamp=time.time()
            )
            return {}, error_metrics
    
    def get_performance_stats(self) -> Dict:
        """Get comprehensive milestone pig-backing statistics"""
        if not self.operation_history:
            return {
                'total_operations': 0,
                'avg_encode_latency': 0.0,
                'avg_decode_latency': 0.0,
                'avg_trailer_latency': 0.0,
                'dag_tips_tracked': len(self.dag_tips)
            }
        
        encode_ops = [op for op in self.operation_history if op['operation'] == 'encode']
        decode_ops = [op for op in self.operation_history if op['operation'] == 'decode']
        trailer_ops = [op for op in self.operation_history if op['operation'] == 'create_trailer']
        
        avg_encode = sum(op['latency'] for op in encode_ops) / len(encode_ops) if encode_ops else 0.0
        avg_decode = sum(op['latency'] for op in decode_ops) / len(decode_ops) if decode_ops else 0.0
        avg_trailer = sum(op['latency'] for op in trailer_ops) / len(trailer_ops) if trailer_ops else 0.0
        
        return {
            'total_operations': len(self.operation_history),
            'avg_encode_latency': avg_encode,
            'avg_decode_latency': avg_decode,
            'avg_trailer_latency': avg_trailer,
            'dag_tips_tracked': len(self.dag_tips),
            'trailer_size_bytes': self.TOTAL_TRAILER_BYTES,
            'target_latency_met': avg_trailer < 1.0  # Target: <1ms
        }


if __name__ == "__main__":
    # Test Milestone Pig-Backing
    print("=" * 60)
    print("Milestone Pig-Backing Test")
    print("=" * 60)
    
    milestone_mgr = MilestonePigBacking(node_id=1)
    
    # Simulate adding consensus rounds
    print("\nAdding 10 consensus rounds...")
    for i in range(10):
        milestone_mgr.add_consensus_round(i + 1)
    print(f"  DAG tips tracked: {len(milestone_mgr.dag_tips)}")
    
    # Select milestones
    print("\nSelecting milestones...")
    indices, metrics = milestone_mgr.select_milestones()
    print(f"  Selected indices: {indices}")
    print(f"  Selection latency: {metrics.operation_latency:.3f}ms")
    
    # Encode milestones
    print("\nEncoding milestones...")
    encoded, metrics = milestone_mgr.encode_milestones(indices)
    print(f"  Encoded bytes: {encoded.hex()}")
    print(f"  Encoding latency: {metrics.operation_latency:.3f}ms")
    
    # Decode milestones
    print("\nDecoding milestones...")
    decoded, metrics = milestone_mgr.decode_milestones(encoded)
    print(f"  Decoded indices: {decoded}")
    print(f"  Decoding latency: {metrics.operation_latency:.3f}ms")
    print(f"  Match original: {decoded == indices}")
    
    # Create beacon trailer
    print("\nCreating beacon trailer...")
    blockchain_hash = "7a24013b6a411875"  # Example from blockchain test
    trailer, metrics = milestone_mgr.create_beacon_trailer(blockchain_hash, indices)
    print(f"  Trailer (hex): {trailer.hex()}")
    print(f"  Trailer size: {len(trailer)} bytes")
    print(f"  Creation latency: {metrics.operation_latency:.3f}ms")
    
    # Parse beacon trailer
    print("\nParsing beacon trailer...")
    parsed, metrics = milestone_mgr.parse_beacon_trailer(trailer)
    print(f"  Blockchain hash: {parsed['blockchain_hash']}")
    print(f"  Milestone indices: {parsed['milestone_indices']}")
    print(f"  Parsing latency: {metrics.operation_latency:.3f}ms")
    
    # Get performance stats
    stats = milestone_mgr.get_performance_stats()
    
    print("\n" + "=" * 60)
    print("Performance Statistics")
    print("=" * 60)
    print(f"Total operations: {stats['total_operations']}")
    print(f"Avg encode latency: {stats['avg_encode_latency']:.3f} ms")
    print(f"Avg decode latency: {stats['avg_decode_latency']:.3f} ms")
    print(f"Avg trailer creation latency: {stats['avg_trailer_latency']:.3f} ms")
    print(f"DAG tips tracked: {stats['dag_tips_tracked']}")
    print(f"Trailer size: {stats['trailer_size_bytes']} bytes")
    print(f"Target (<1ms) met: {stats['target_latency_met']}")
    print("=" * 60)

