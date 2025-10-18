"""
PrimeFusion-FANET Unified Framework
===================================

Integrates all PrimeFusion components into a unified framework for UAV swarms.
Provides high-level API for beacon-embedded distributed ledger operations.

Author: PrimeFusion-FANET Team
Date: September 2025
Version: 2.0 (Complete Implementation)
"""

import time
import json
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

from .beacon import BeaconManager, BeaconMetrics
from .consensus import DAGConsensus, ConsensusMetrics
from .cbor_compression import CBORCompressor, CompressionMetrics
from .crypto import PrimeFusionCrypto, CryptoMetrics
from .message_classifier import AdaptiveMessageClassifier, MessageClassification, ClassificationMetrics


@dataclass
class FrameworkMetrics:
    """Comprehensive framework performance metrics"""
    total_operations: int
    avg_latency: float  # milliseconds
    success_rate: float
    energy_efficiency: float
    compression_ratio: float
    security_overhead: float
    timestamp: float


class PrimeFusionFramework:
    """
    Unified PrimeFusion-FANET Framework
    
    Integrates beacon management, consensus, compression, cryptography,
    and message classification into a cohesive UAV swarm communication system.
    """
    
    def __init__(self, uav_id: int):
        self.uav_id = uav_id
        self.framework_history = []
        
        # Initialize all components
        self.beacon_manager = BeaconManager()
        self.beacon_manager.set_uav_id(uav_id)
        
        self.consensus_engine = DAGConsensus()
        self.consensus_engine.set_node_id(uav_id)
        
        self.compressor = CBORCompressor()
        self.crypto = PrimeFusionCrypto()
        self.classifier = AdaptiveMessageClassifier()
        
        # Performance targets
        self.TARGET_LATENCY = 0.5  # ms for complete cycle
        self.TARGET_COMPRESSION = 2.0  # minimum compression ratio
        
    def set_shared_key(self, key: str):
        """Set shared cryptographic key"""
        self.beacon_manager.set_shared_key(key)
        self.crypto.set_shared_key(self.uav_id, key)
    
    def process_complete_beacon_cycle(self, position: List[float], velocity: List[float], 
                                    transaction_data: Dict) -> Tuple[bytes, FrameworkMetrics]:
        """
        Process complete beacon cycle with all PrimeFusion components.
        
        Args:
            position: UAV position [x, y, z]
            velocity: UAV velocity [vx, vy, vz]
            transaction_data: Transaction payload dictionary
            
        Returns:
            Tuple of (complete_beacon_data, framework_metrics)
        """
        start_time = time.time()
        operation_results = {}
        
        try:
            # Step 1: Compress transaction data
            tx_json = json.dumps(transaction_data).encode()
            compressed_data, compression_metrics = self.compressor.compress(tx_json)
            operation_results['compression'] = compression_metrics
            
            if not compression_metrics.success:
                raise Exception("Compression failed")
            
            # Step 2: Generate beacon with embedded ledger
            beacon_data, beacon_metrics = self.beacon_manager.generate_beacon(
                position, velocity, compressed_data
            )
            operation_results['beacon'] = beacon_metrics
            
            if not beacon_metrics.success:
                raise Exception("Beacon generation failed")
            
            # Step 3: Add cryptographic security
            secure_trailer, crypto_metrics = self.crypto.compute_hmac(
                beacon_data, self.uav_id
            )
            operation_results['crypto'] = crypto_metrics
            
            if not crypto_metrics.success:
                raise Exception("Cryptographic security failed")
            
            # Step 4: Create final secure beacon
            final_beacon = beacon_data + secure_trailer
            
            # Step 5: Classify the beacon message
            classification, class_metrics = self.classifier.classify_message(
                transaction_data
            )
            operation_results['classification'] = class_metrics
            
            # Calculate comprehensive metrics
            total_time = (time.time() - start_time) * 1000
            
            framework_metrics = FrameworkMetrics(
                total_operations=4,  # compression, beacon, crypto, classification
                avg_latency=total_time,
                success_rate=1.0,
                energy_efficiency=self._calculate_energy_efficiency(operation_results),
                compression_ratio=compression_metrics.compression_ratio,
                security_overhead=len(secure_trailer) / len(beacon_data),
                timestamp=time.time()
            )
            
            # Update framework history
            self.framework_history.append({
                'timestamp': time.time(),
                'operation': 'complete_beacon_cycle',
                'latency': total_time,
                'success': True,
                'components': operation_results
            })
            
            return final_beacon, framework_metrics
            
        except Exception as e:
            # Return error metrics
            error_metrics = FrameworkMetrics(
                total_operations=0,
                avg_latency=999.0,
                success_rate=0.0,
                energy_efficiency=0.0,
                compression_ratio=0.0,
                security_overhead=0.0,
                timestamp=time.time()
            )
            
            return b'', error_metrics
    
    def _calculate_energy_efficiency(self, operation_results: Dict) -> float:
        """Calculate energy efficiency based on operation results"""
        total_energy = 0.0
        
        for component, metrics in operation_results.items():
            if hasattr(metrics, 'energy_consumption'):
                total_energy += metrics.energy_consumption
            else:
                # Estimate energy consumption
                if component == 'compression':
                    total_energy += 0.001
                elif component == 'beacon':
                    total_energy += 0.001
                elif component == 'crypto':
                    total_energy += 0.0005
                elif component == 'classification':
                    total_energy += 0.0002
        
        # Energy efficiency as inverse of consumption (higher is better)
        return 1.0 / (total_energy + 0.001)  # Avoid division by zero
    
    def get_comprehensive_stats(self) -> Dict:
        """Get comprehensive framework statistics"""
        if not self.framework_history:
            return {
                'framework_operations': 0,
                'avg_latency': 0.0,
                'success_rate': 0.0,
                'component_stats': {}
            }
        
        total_ops = len(self.framework_history)
        successful_ops = [op for op in self.framework_history if op['success']]
        
        avg_latency = sum(op['latency'] for op in successful_ops) / len(successful_ops) if successful_ops else 0.0
        success_rate = len(successful_ops) / total_ops
        
        # Get component statistics
        component_stats = {
            'beacon': self.beacon_manager.get_performance_stats(),
            'consensus': self.consensus_engine.get_consensus_stats(),
            'compression': self.compressor.get_compression_stats(),
            'crypto': {'operations': len(self.crypto.shared_keys)},
            'classification': self.classifier.get_classification_stats()
        }
        
        return {
            'framework_operations': total_ops,
            'successful_operations': len(successful_ops),
            'avg_latency': avg_latency,
            'success_rate': success_rate,
            'target_latency_met': avg_latency <= self.TARGET_LATENCY * 2,
            'target_success_met': success_rate >= 0.95,
            'component_stats': component_stats
        }


if __name__ == "__main__":
    # Test complete framework functionality
    framework = PrimeFusionFramework(uav_id=1)
    framework.set_shared_key("test-framework-key")
    
    # Test complete beacon cycle
    position = [500.0, 500.0, 100.0]
    velocity = [1.0, 0.5, 0.0]
    transaction_data = {
        "type": "coordination",
        "mission_id": "test_mission_1",
        "timestamp": time.time(),
        "data": "formation_update"
    }
    
    beacon_data, metrics = framework.process_complete_beacon_cycle(
        position, velocity, transaction_data
    )
    
    print(f"Complete beacon cycle:")
    print(f"  Success: {len(beacon_data) > 0}")
    print(f"  Total latency: {metrics.avg_latency:.3f} ms")
    print(f"  Beacon size: {len(beacon_data)} bytes")
    print(f"  Compression ratio: {metrics.compression_ratio:.2f}")

