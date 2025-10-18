"""
PrimeFusion-FANET Linear Blockchain
===================================

Implements simple hash-chain blockchain with Session-MAC authentication.
Optimized for UAV swarm communication with minimal overhead.

Author: PrimeFusion-FANET Team
Date: October 2025
Version: 1.0
"""

import time
import hashlib
from typing import List, Optional, Tuple, Dict
from dataclasses import dataclass
from session_mac import SessionMAC, SessionMACMetrics


@dataclass
class Block:
    """Blockchain block structure"""
    index: int
    timestamp: float
    data: bytes
    previous_hash: str
    hash: str
    signature: bytes
    nonce: int = 0


@dataclass
class BlockchainMetrics:
    """Performance metrics for blockchain operations"""
    operation_latency: float  # milliseconds
    operation_type: str  # 'add_block', 'verify_block', 'get_hash'
    block_index: int
    success: bool
    timestamp: float


class LinearBlockchain:
    """
    Simple hash-chain blockchain with Session-MAC authentication.
    
    Features:
    - Linear chain structure (no forks)
    - Session-MAC hybrid authentication
    - Lightweight consensus integration
    - 8-byte hash trailer for beacon embedding
    """
    
    def __init__(self, node_id: int = 0):
        """
        Initialize blockchain with genesis block.
        
        Args:
            node_id: Unique identifier for this UAV node
        """
        self.node_id = node_id
        self.chain: List[Block] = []
        self.session_mac = SessionMAC(node_id)
        self.operation_history = []
        
        # Create genesis block
        self._create_genesis_block()
    
    def _create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_data = f"Genesis Block - Node {self.node_id}".encode()
        genesis_block = Block(
            index=0,
            timestamp=time.time(),
            data=genesis_data,
            previous_hash="0" * 64,
            hash="",
            signature=b'',
            nonce=0
        )
        
        # Calculate hash
        genesis_block.hash = self._calculate_hash(genesis_block)
        
        # Sign with Session-MAC
        block_bytes = self._block_to_bytes(genesis_block)
        signature, _ = self.session_mac.sign_block(0, block_bytes)
        genesis_block.signature = signature
        
        self.chain.append(genesis_block)
    
    def add_block(self, data: bytes) -> Tuple[Block, BlockchainMetrics]:
        """
        Add a new block to the blockchain.
        
        Args:
            data: Block data (transaction, consensus, etc.)
            
        Returns:
            Tuple of (new_block, metrics)
        """
        start_time = time.time()
        
        try:
            # Get previous block
            previous_block = self.chain[-1]
            
            # Create new block
            new_block = Block(
                index=len(self.chain),
                timestamp=time.time(),
                data=data,
                previous_hash=previous_block.hash,
                hash="",
                signature=b'',
                nonce=0
            )
            
            # Calculate hash
            new_block.hash = self._calculate_hash(new_block)
            
            # Sign with Session-MAC
            block_bytes = self._block_to_bytes(new_block)
            signature, mac_metrics = self.session_mac.sign_block(new_block.index, block_bytes)
            new_block.signature = signature
            
            # Add to chain
            self.chain.append(new_block)
            
            # Calculate metrics
            latency = (time.time() - start_time) * 1000  # ms
            
            metrics = BlockchainMetrics(
                operation_latency=latency,
                operation_type='add_block',
                block_index=new_block.index,
                success=True,
                timestamp=time.time()
            )
            
            self.operation_history.append({
                'operation': 'add_block',
                'block_index': new_block.index,
                'latency': latency,
                'timestamp': time.time()
            })
            
            return new_block, metrics
            
        except Exception as e:
            error_metrics = BlockchainMetrics(
                operation_latency=999.0,
                operation_type='add_block',
                block_index=-1,
                success=False,
                timestamp=time.time()
            )
            return None, error_metrics
    
    def verify_block(self, block: Block) -> Tuple[bool, BlockchainMetrics]:
        """
        Verify a block's integrity and signature.
        
        Args:
            block: Block to verify
            
        Returns:
            Tuple of (verification_result, metrics)
        """
        start_time = time.time()
        
        try:
            # Verify hash
            calculated_hash = self._calculate_hash(block)
            if calculated_hash != block.hash:
                latency = (time.time() - start_time) * 1000
                metrics = BlockchainMetrics(
                    operation_latency=latency,
                    operation_type='verify_block',
                    block_index=block.index,
                    success=False,
                    timestamp=time.time()
                )
                return False, metrics
            
            # Verify signature with Session-MAC
            block_bytes = self._block_to_bytes(block)
            valid, mac_metrics = self.session_mac.verify_block(
                block.index,
                block_bytes,
                block.signature
            )
            
            latency = (time.time() - start_time) * 1000  # ms
            
            metrics = BlockchainMetrics(
                operation_latency=latency,
                operation_type='verify_block',
                block_index=block.index,
                success=valid,
                timestamp=time.time()
            )
            
            self.operation_history.append({
                'operation': 'verify_block',
                'block_index': block.index,
                'latency': latency,
                'valid': valid,
                'timestamp': time.time()
            })
            
            return valid, metrics
            
        except Exception as e:
            error_metrics = BlockchainMetrics(
                operation_latency=999.0,
                operation_type='verify_block',
                block_index=block.index if block else -1,
                success=False,
                timestamp=time.time()
            )
            return False, error_metrics
    
    def get_latest_hash(self) -> Tuple[str, BlockchainMetrics]:
        """
        Get the hash of the latest block (for beacon embedding).
        
        Returns:
            Tuple of (hash_8bytes, metrics)
        """
        start_time = time.time()
        
        try:
            latest_block = self.chain[-1]
            # Return first 8 bytes (16 hex chars) of hash
            hash_8bytes = latest_block.hash[:16]
            
            latency = (time.time() - start_time) * 1000  # ms
            
            metrics = BlockchainMetrics(
                operation_latency=latency,
                operation_type='get_hash',
                block_index=latest_block.index,
                success=True,
                timestamp=time.time()
            )
            
            return hash_8bytes, metrics
            
        except Exception as e:
            error_metrics = BlockchainMetrics(
                operation_latency=999.0,
                operation_type='get_hash',
                block_index=-1,
                success=False,
                timestamp=time.time()
            )
            return "", error_metrics
    
    def get_chain_length(self) -> int:
        """Get the current length of the blockchain"""
        return len(self.chain)
    
    def get_block(self, index: int) -> Optional[Block]:
        """Get a block by index"""
        if 0 <= index < len(self.chain):
            return self.chain[index]
        return None
    
    def _calculate_hash(self, block: Block) -> str:
        """Calculate SHA-256 hash of a block"""
        block_string = f"{block.index}{block.timestamp}{block.data}{block.previous_hash}{block.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def _block_to_bytes(self, block: Block) -> bytes:
        """Convert block to bytes for signing"""
        block_string = f"{block.index}{block.timestamp}{block.data}{block.previous_hash}{block.hash}{block.nonce}"
        return block_string.encode()
    
    def is_chain_valid(self) -> bool:
        """Verify the entire blockchain integrity"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Verify hash
            if current_block.hash != self._calculate_hash(current_block):
                return False
            
            # Verify previous hash link
            if current_block.previous_hash != previous_block.hash:
                return False
            
            # Verify signature
            valid, _ = self.verify_block(current_block)
            if not valid:
                return False
        
        return True
    
    def get_performance_stats(self) -> Dict:
        """Get comprehensive blockchain performance statistics"""
        if not self.operation_history:
            return {
                'total_operations': 0,
                'total_blocks': len(self.chain),
                'avg_add_latency': 0.0,
                'avg_verify_latency': 0.0,
                'chain_valid': self.is_chain_valid()
            }
        
        add_ops = [op for op in self.operation_history if op['operation'] == 'add_block']
        verify_ops = [op for op in self.operation_history if op['operation'] == 'verify_block']
        
        avg_add_latency = sum(op['latency'] for op in add_ops) / len(add_ops) if add_ops else 0.0
        avg_verify_latency = sum(op['latency'] for op in verify_ops) / len(verify_ops) if verify_ops else 0.0
        
        # Get Session-MAC stats
        mac_stats = self.session_mac.get_performance_stats()
        
        return {
            'total_operations': len(self.operation_history),
            'total_blocks': len(self.chain),
            'avg_add_latency': avg_add_latency,
            'avg_verify_latency': avg_verify_latency,
            'chain_valid': self.is_chain_valid(),
            'session_mac_cpu_reduction': mac_stats['cpu_reduction_vs_pure_ed25519'],
            'session_mac_target_met': mac_stats['target_cpu_reduction_met']
        }


if __name__ == "__main__":
    # Test Linear Blockchain
    print("=" * 60)
    print("Linear Blockchain Test")
    print("=" * 60)
    
    blockchain = LinearBlockchain(node_id=1)
    
    # Add 10 blocks
    print("\nAdding 10 blocks...")
    for i in range(1, 11):
        block_data = f"Transaction {i}: UAV data".encode()
        block, metrics = blockchain.add_block(block_data)
        print(f"  Block {block.index}: hash={block.hash[:16]}..., "
              f"latency={metrics.operation_latency:.3f}ms")
    
    # Verify chain
    print("\nVerifying blockchain...")
    is_valid = blockchain.is_chain_valid()
    print(f"  Chain valid: {is_valid}")
    
    # Get latest hash for beacon
    print("\nGetting latest hash for beacon embedding...")
    hash_8bytes, metrics = blockchain.get_latest_hash()
    print(f"  Latest hash (8 bytes): {hash_8bytes}")
    print(f"  Retrieval latency: {metrics.operation_latency:.3f}ms")
    
    # Get performance stats
    stats = blockchain.get_performance_stats()
    
    print("\n" + "=" * 60)
    print("Performance Statistics")
    print("=" * 60)
    print(f"Total blocks: {stats['total_blocks']}")
    print(f"Total operations: {stats['total_operations']}")
    print(f"Avg add block latency: {stats['avg_add_latency']:.3f} ms")
    print(f"Avg verify latency: {stats['avg_verify_latency']:.3f} ms")
    print(f"Chain valid: {stats['chain_valid']}")
    print(f"Session-MAC CPU reduction: {stats['session_mac_cpu_reduction']:.1f}%")
    print(f"Session-MAC target met: {stats['session_mac_target_met']}")
    print("=" * 60)

