"""
PrimeFusion-FANET Network Simulator
===================================

Simulates a multi-UAV network with PrimeFusion-FANET protocol.

Author: PrimeFusion-FANET Team
Date: October 2025
Version: 1.0
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'core'))

import time
import random
import math
from typing import List, Dict, Tuple
from dataclasses import dataclass
from uav_node import UAVNode, UAVPosition, UAVVelocity


@dataclass
class SimulationConfig:
    """Simulation configuration parameters"""
    num_uavs: int = 5
    simulation_duration: float = 60.0  # seconds
    time_step: float = 0.1  # seconds
    beacon_interval: float = 1.0  # seconds
    communication_range: float = 500.0  # meters
    area_size: float = 1000.0  # meters (square area)
    initial_altitude: float = 100.0  # meters
    max_velocity: float = 10.0  # m/s
    transaction_probability: float = 0.1  # probability per time step
    consensus_interval: float = 5.0  # seconds


class NetworkSimulator:
    """
    Multi-UAV network simulator with PrimeFusion-FANET protocol.
    
    Features:
    - Multiple UAV nodes
    - Mobility models
    - Beacon broadcasting
    - Blockchain transactions
    - Consensus rounds
    - Performance metrics collection
    """
    
    def __init__(self, config: SimulationConfig):
        """
        Initialize network simulator.
        
        Args:
            config: Simulation configuration
        """
        self.config = config
        self.nodes: List[UAVNode] = []
        self.current_time = 0.0
        self.consensus_round = 0
        self.last_consensus_time = 0.0
        
        # Performance metrics
        self.total_beacons_sent = 0
        self.total_beacons_received = 0
        self.total_transactions = 0
        self.total_consensus_rounds = 0
        
        # Initialize UAV nodes
        self._initialize_nodes()
    
    def _initialize_nodes(self):
        """Initialize UAV nodes with random positions"""
        print(f"\nInitializing {self.config.num_uavs} UAV nodes...")
        
        for i in range(self.config.num_uavs):
            # Random position within area
            lat = 40.7128 + random.uniform(-0.01, 0.01)  # ~±1km
            lon = -74.0060 + random.uniform(-0.01, 0.01)
            alt = self.config.initial_altitude + random.uniform(-20, 20)
            
            position = UAVPosition(latitude=lat, longitude=lon, altitude=alt)
            
            # Create node
            node = UAVNode(
                node_id=i + 1,
                initial_position=position,
                beacon_interval=self.config.beacon_interval
            )
            
            # Set random velocity
            vx = random.uniform(-self.config.max_velocity, self.config.max_velocity)
            vy = random.uniform(-self.config.max_velocity, self.config.max_velocity)
            vz = random.uniform(-2.0, 2.0)  # Slower vertical movement
            node.set_velocity(vx, vy, vz)
            
            self.nodes.append(node)
            
            print(f"  Node {node.node_id}: pos=({lat:.4f}, {lon:.4f}, {alt:.1f}m), "
                  f"vel=({vx:.1f}, {vy:.1f}, {vz:.1f})m/s")
    
    def _update_network_topology(self):
        """Update neighbor relationships based on communication range"""
        for node in self.nodes:
            node.update_neighbors(self.nodes, self.config.communication_range)
    
    def _broadcast_beacons(self):
        """Handle beacon broadcasting and reception"""
        beacons_this_step = []
        
        # Generate beacons from nodes that should send
        for node in self.nodes:
            if node.should_send_beacon(self.current_time):
                beacon_bytes, metrics = node.generate_beacon(self.current_time)
                if metrics.success:
                    beacons_this_step.append((node.node_id, beacon_bytes))
                    self.total_beacons_sent += 1
        
        # Deliver beacons to neighbors
        for sender_id, beacon_bytes in beacons_this_step:
            sender_node = self.nodes[sender_id - 1]
            
            for neighbor_id in sender_node.neighbors:
                neighbor_node = self.nodes[neighbor_id - 1]
                success = neighbor_node.receive_beacon(sender_id, beacon_bytes, self.current_time)
                if success:
                    self.total_beacons_received += 1
    
    def _handle_transactions(self):
        """Randomly generate blockchain transactions"""
        for node in self.nodes:
            if random.random() < self.config.transaction_probability:
                tx_data = f"Data at t={self.current_time:.1f}s"
                success = node.create_transaction(tx_data)
                if success:
                    self.total_transactions += 1
    
    def _handle_consensus(self):
        """Handle consensus rounds"""
        if (self.current_time - self.last_consensus_time) >= self.config.consensus_interval:
            self.consensus_round += 1
            
            for node in self.nodes:
                node.participate_in_consensus(self.consensus_round)
            
            self.total_consensus_rounds += 1
            self.last_consensus_time = self.current_time
    
    def _update_mobility(self):
        """Update UAV positions based on mobility model"""
        for node in self.nodes:
            node.update_position(self.config.time_step)
            
            # Simple boundary check (bounce back)
            if abs(node.position.latitude - 40.7128) > 0.01:
                node.velocity.x = -node.velocity.x
            if abs(node.position.longitude - (-74.0060)) > 0.01:
                node.velocity.y = -node.velocity.y
            if node.position.altitude < 50 or node.position.altitude > 150:
                node.velocity.z = -node.velocity.z
    
    def run(self) -> Dict:
        """
        Run the simulation.
        
        Returns:
            Simulation results and metrics
        """
        print("\n" + "=" * 60)
        print(f"Starting simulation: {self.config.num_uavs} UAVs, {self.config.simulation_duration}s")
        print("=" * 60)
        
        start_time = time.time()
        num_steps = int(self.config.simulation_duration / self.config.time_step)
        
        # Progress tracking
        progress_interval = num_steps // 10  # 10% intervals
        
        for step in range(num_steps):
            self.current_time = step * self.config.time_step
            
            # Update network topology
            self._update_network_topology()
            
            # Handle beacons
            self._broadcast_beacons()
            
            # Handle transactions
            self._handle_transactions()
            
            # Handle consensus
            self._handle_consensus()
            
            # Update mobility
            self._update_mobility()
            
            # Progress update
            if step % progress_interval == 0 and step > 0:
                progress = (step / num_steps) * 100
                print(f"  Progress: {progress:.0f}% (t={self.current_time:.1f}s, "
                      f"beacons={self.total_beacons_sent}, tx={self.total_transactions})")
        
        execution_time = time.time() - start_time
        
        print(f"\nSimulation completed in {execution_time:.2f}s (real time)")
        
        # Collect results
        results = self._collect_results(execution_time)
        
        return results
    
    def _collect_results(self, execution_time: float) -> Dict:
        """Collect comprehensive simulation results"""
        
        # Collect node statistics
        node_stats = [node.get_statistics() for node in self.nodes]
        
        # Calculate aggregate metrics
        total_beacons_sent = sum(stats['beacons_sent'] for stats in node_stats)
        total_beacons_received = sum(stats['beacons_received'] for stats in node_stats)
        total_transactions = sum(stats['transactions_created'] for stats in node_stats)
        total_neighbors = sum(stats['neighbors'] for stats in node_stats)
        avg_neighbors = total_neighbors / len(node_stats) if node_stats else 0
        
        # Calculate beacon delivery ratio
        pdr = (total_beacons_received / total_beacons_sent) if total_beacons_sent > 0 else 0.0
        
        # Collect beacon performance metrics
        beacon_latencies = []
        beacon_sizes = []
        compression_ratios = []
        
        for stats in node_stats:
            bp = stats['beacon_performance']
            if bp['total_beacons'] > 0:
                beacon_latencies.append(bp['avg_total_latency'])
                beacon_sizes.append(bp['avg_beacon_size'])
                compression_ratios.append(bp['avg_compression_ratio'])
        
        avg_beacon_latency = sum(beacon_latencies) / len(beacon_latencies) if beacon_latencies else 0.0
        avg_beacon_size = sum(beacon_sizes) / len(beacon_sizes) if beacon_sizes else 0.0
        avg_compression = sum(compression_ratios) / len(compression_ratios) if compression_ratios else 0.0
        
        # Collect blockchain performance
        blockchain_stats = []
        for stats in node_stats:
            bp = stats['beacon_performance']['blockchain_stats']
            blockchain_stats.append(bp)
        
        avg_chain_length = sum(bs['total_blocks'] for bs in blockchain_stats) / len(blockchain_stats)
        avg_cpu_reduction = sum(bs['session_mac_cpu_reduction'] for bs in blockchain_stats) / len(blockchain_stats)
        
        results = {
            'config': {
                'num_uavs': self.config.num_uavs,
                'simulation_duration': self.config.simulation_duration,
                'communication_range': self.config.communication_range,
                'beacon_interval': self.config.beacon_interval
            },
            'execution': {
                'execution_time': execution_time,
                'simulation_duration': self.config.simulation_duration,
                'time_steps': int(self.config.simulation_duration / self.config.time_step)
            },
            'network': {
                'total_beacons_sent': total_beacons_sent,
                'total_beacons_received': total_beacons_received,
                'packet_delivery_ratio': pdr,
                'avg_neighbors': avg_neighbors,
                'total_transactions': total_transactions,
                'consensus_rounds': self.consensus_round
            },
            'performance': {
                'avg_beacon_latency': avg_beacon_latency,
                'avg_beacon_size': avg_beacon_size,
                'avg_compression_ratio': avg_compression,
                'avg_chain_length': avg_chain_length,
                'avg_cpu_reduction': avg_cpu_reduction
            },
            'nodes': node_stats
        }
        
        return results
    
    def print_results(self, results: Dict):
        """Print formatted simulation results"""
        print("\n" + "=" * 60)
        print("SIMULATION RESULTS")
        print("=" * 60)
        
        print("\nConfiguration:")
        print(f"  UAVs: {results['config']['num_uavs']}")
        print(f"  Duration: {results['config']['simulation_duration']}s")
        print(f"  Communication range: {results['config']['communication_range']}m")
        print(f"  Beacon interval: {results['config']['beacon_interval']}s")
        
        print("\nExecution:")
        print(f"  Real execution time: {results['execution']['execution_time']:.2f}s")
        print(f"  Time steps: {results['execution']['time_steps']}")
        
        print("\nNetwork Metrics:")
        print(f"  Total beacons sent: {results['network']['total_beacons_sent']}")
        print(f"  Total beacons received: {results['network']['total_beacons_received']}")
        print(f"  Packet Delivery Ratio (PDR): {results['network']['packet_delivery_ratio']:.2%}")
        print(f"  Avg neighbors per UAV: {results['network']['avg_neighbors']:.1f}")
        print(f"  Total transactions: {results['network']['total_transactions']}")
        print(f"  Consensus rounds: {results['network']['consensus_rounds']}")
        
        print("\nPerformance Metrics:")
        print(f"  Avg beacon latency: {results['performance']['avg_beacon_latency']:.3f} ms")
        print(f"  Avg beacon size: {results['performance']['avg_beacon_size']:.1f} bytes")
        print(f"  Avg compression ratio: {results['performance']['avg_compression_ratio']:.3f}")
        print(f"  Avg blockchain length: {results['performance']['avg_chain_length']:.1f} blocks")
        print(f"  Avg CPU reduction: {results['performance']['avg_cpu_reduction']:.1f}%")
        
        print("\nPer-Node Statistics:")
        for node_stat in results['nodes']:
            print(f"  Node {node_stat['node_id']}: "
                  f"beacons={node_stat['beacons_sent']}/{node_stat['beacons_received']}, "
                  f"tx={node_stat['transactions_created']}, "
                  f"neighbors={node_stat['neighbors']}, "
                  f"battery={node_stat['battery']:.1f}%")
        
        print("=" * 60)


if __name__ == "__main__":
    # Test Network Simulator
    print("=" * 60)
    print("PrimeFusion-FANET Network Simulator Test")
    print("=" * 60)
    
    # Configuration
    config = SimulationConfig(
        num_uavs=5,
        simulation_duration=30.0,  # 30 seconds for quick test
        time_step=0.1,
        beacon_interval=1.0,
        communication_range=500.0,
        transaction_probability=0.05
    )
    
    # Create and run simulator
    simulator = NetworkSimulator(config)
    results = simulator.run()
    
    # Print results
    simulator.print_results(results)

