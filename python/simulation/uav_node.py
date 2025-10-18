"""
PrimeFusion-FANET UAV Node Simulation
=====================================

Simulates a single UAV node with PrimeFusion capabilities.

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
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from beacon_integrated import IntegratedBeaconManager, BeaconMetrics


@dataclass
class UAVPosition:
    """3D position of UAV"""
    latitude: float
    longitude: float
    altitude: float
    
    def distance_to(self, other: 'UAVPosition') -> float:
        """Calculate Euclidean distance to another position (simplified)"""
        lat_diff = (self.latitude - other.latitude) * 111000  # ~111km per degree
        lon_diff = (self.longitude - other.longitude) * 111000
        alt_diff = self.altitude - other.altitude
        return math.sqrt(lat_diff**2 + lon_diff**2 + alt_diff**2)


@dataclass
class UAVVelocity:
    """3D velocity of UAV"""
    x: float  # m/s
    y: float  # m/s
    z: float  # m/s
    
    def speed(self) -> float:
        """Calculate speed magnitude"""
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)


class UAVNode:
    """
    Simulated UAV node with PrimeFusion-FANET capabilities.
    
    Features:
    - Beacon-embedded blockchain
    - Milestone pig-backing
    - CBOR compression
    - Session-MAC authentication
    - Mobility model
    - Network communication
    """
    
    def __init__(self, node_id: int, initial_position: UAVPosition, 
                 beacon_interval: float = 1.0):
        """
        Initialize UAV node.
        
        Args:
            node_id: Unique node identifier
            initial_position: Initial 3D position
            beacon_interval: Beacon transmission interval (seconds)
        """
        self.node_id = node_id
        self.position = initial_position
        self.velocity = UAVVelocity(x=0.0, y=0.0, z=0.0)
        self.beacon_interval = beacon_interval
        
        # PrimeFusion components
        self.beacon_mgr = IntegratedBeaconManager(node_id)
        
        # Node state
        self.battery = 100.0  # percentage
        self.status = 'active'
        self.mission = 'patrol'
        
        # Network state
        self.neighbors: List[int] = []  # List of neighbor node IDs
        self.received_beacons: List[Tuple[int, bytes, float]] = []  # (sender_id, beacon, timestamp)
        
        # Performance tracking
        self.beacons_sent = 0
        self.beacons_received = 0
        self.transactions_created = 0
        self.consensus_rounds = 0
        
        # Timing
        self.last_beacon_time = 0.0
        self.last_transaction_time = 0.0
        self.start_time = time.time()
    
    def update_position(self, dt: float):
        """
        Update position based on velocity and time step.
        
        Args:
            dt: Time step (seconds)
        """
        # Update position
        self.position.latitude += (self.velocity.x / 111000) * dt  # Convert m to degrees
        self.position.longitude += (self.velocity.y / 111000) * dt
        self.position.altitude += self.velocity.z * dt
        
        # Update battery (simplified model)
        # Assume 1% battery per 60 seconds of flight
        self.battery -= (dt / 60.0)
        self.battery = max(0.0, self.battery)
        
        # Update status based on battery
        if self.battery < 20.0:
            self.status = 'low_battery'
        elif self.battery < 10.0:
            self.status = 'critical'
        elif self.battery == 0.0:
            self.status = 'dead'
        else:
            self.status = 'active'
    
    def set_velocity(self, vx: float, vy: float, vz: float):
        """Set UAV velocity"""
        self.velocity.x = vx
        self.velocity.y = vy
        self.velocity.z = vz
    
    def create_transaction(self, data: str) -> bool:
        """
        Create a blockchain transaction.
        
        Args:
            data: Transaction data
            
        Returns:
            Success status
        """
        try:
            tx_data = f"Node {self.node_id}: {data}".encode()
            metrics = self.beacon_mgr.add_blockchain_transaction(tx_data)
            
            if metrics.success:
                self.transactions_created += 1
                self.last_transaction_time = time.time()
                return True
            return False
        except:
            return False
    
    def participate_in_consensus(self, round_id: int):
        """
        Participate in a consensus round.
        
        Args:
            round_id: Consensus round identifier
        """
        self.beacon_mgr.add_consensus_round(round_id)
        self.consensus_rounds += 1
    
    def should_send_beacon(self, current_time: float) -> bool:
        """Check if it's time to send a beacon"""
        return (current_time - self.last_beacon_time) >= self.beacon_interval
    
    def generate_beacon(self, current_time: float) -> Tuple[bytes, BeaconMetrics]:
        """
        Generate a beacon with current UAV state.
        
        Args:
            current_time: Current simulation time
            
        Returns:
            Tuple of (beacon_bytes, metrics)
        """
        uav_data = {
            'uav_id': self.node_id,
            'position': {
                'latitude': self.position.latitude,
                'longitude': self.position.longitude,
                'altitude': self.position.altitude
            },
            'velocity': {
                'x': self.velocity.x,
                'y': self.velocity.y,
                'z': self.velocity.z
            },
            'status': self.status,
            'battery': self.battery,
            'mission': self.mission,
            'timestamp': current_time,
            'neighbors': len(self.neighbors)
        }
        
        beacon_bytes, metrics = self.beacon_mgr.generate_beacon(uav_data)
        
        if metrics.success:
            self.beacons_sent += 1
            self.last_beacon_time = current_time
        
        return beacon_bytes, metrics
    
    def receive_beacon(self, sender_id: int, beacon_bytes: bytes, current_time: float) -> bool:
        """
        Receive and process a beacon from another UAV.
        
        Args:
            sender_id: Sender node ID
            beacon_bytes: Beacon data
            current_time: Current simulation time
            
        Returns:
            Success status
        """
        try:
            # Parse beacon
            parsed, metrics = self.beacon_mgr.parse_beacon(beacon_bytes)
            
            if metrics.success:
                self.received_beacons.append((sender_id, beacon_bytes, current_time))
                self.beacons_received += 1
                
                # Update neighbors list
                if sender_id not in self.neighbors:
                    self.neighbors.append(sender_id)
                
                return True
            return False
        except:
            return False
    
    def update_neighbors(self, all_nodes: List['UAVNode'], communication_range: float):
        """
        Update neighbor list based on communication range.
        
        Args:
            all_nodes: List of all UAV nodes
            communication_range: Maximum communication range (meters)
        """
        self.neighbors = []
        
        for node in all_nodes:
            if node.node_id == self.node_id:
                continue
            
            distance = self.position.distance_to(node.position)
            if distance <= communication_range:
                self.neighbors.append(node.node_id)
    
    def get_statistics(self) -> Dict:
        """Get comprehensive node statistics"""
        uptime = time.time() - self.start_time
        
        beacon_stats = self.beacon_mgr.get_performance_stats()
        
        return {
            'node_id': self.node_id,
            'uptime': uptime,
            'position': {
                'latitude': self.position.latitude,
                'longitude': self.position.longitude,
                'altitude': self.position.altitude
            },
            'velocity': {
                'x': self.velocity.x,
                'y': self.velocity.y,
                'z': self.velocity.z,
                'speed': self.velocity.speed()
            },
            'battery': self.battery,
            'status': self.status,
            'beacons_sent': self.beacons_sent,
            'beacons_received': self.beacons_received,
            'transactions_created': self.transactions_created,
            'consensus_rounds': self.consensus_rounds,
            'neighbors': len(self.neighbors),
            'neighbor_ids': self.neighbors,
            'beacon_performance': beacon_stats
        }


if __name__ == "__main__":
    # Test UAV Node
    print("=" * 60)
    print("UAV Node Test")
    print("=" * 60)
    
    # Create UAV node
    initial_pos = UAVPosition(latitude=40.7128, longitude=-74.0060, altitude=100.0)
    uav = UAVNode(node_id=1, initial_position=initial_pos, beacon_interval=1.0)
    
    print(f"\nInitialized UAV Node {uav.node_id}")
    print(f"  Position: ({uav.position.latitude:.4f}, {uav.position.longitude:.4f}, {uav.position.altitude:.1f}m)")
    print(f"  Battery: {uav.battery:.1f}%")
    print(f"  Status: {uav.status}")
    
    # Set velocity
    uav.set_velocity(vx=5.0, vy=3.0, vz=0.5)
    print(f"\nSet velocity: ({uav.velocity.x}, {uav.velocity.y}, {uav.velocity.z}) m/s")
    print(f"  Speed: {uav.velocity.speed():.2f} m/s")
    
    # Create transactions
    print("\nCreating transactions...")
    for i in range(3):
        success = uav.create_transaction(f"Transaction {i+1}")
        print(f"  Transaction {i+1}: {'✓' if success else '✗'}")
    
    # Participate in consensus
    print("\nParticipating in consensus rounds...")
    for i in range(5):
        uav.participate_in_consensus(i + 1)
    print(f"  Consensus rounds: {uav.consensus_rounds}")
    
    # Simulate beacon transmission
    print("\nSimulating beacon transmission...")
    current_time = time.time()
    
    for i in range(3):
        if uav.should_send_beacon(current_time):
            beacon_bytes, metrics = uav.generate_beacon(current_time)
            print(f"  Beacon {i+1}: size={metrics.beacon_size}B, latency={metrics.total_latency:.3f}ms")
            current_time += 1.0  # Advance time
    
    # Update position
    print("\nUpdating position (10 seconds)...")
    uav.update_position(dt=10.0)
    print(f"  New position: ({uav.position.latitude:.4f}, {uav.position.longitude:.4f}, {uav.position.altitude:.1f}m)")
    print(f"  Battery: {uav.battery:.1f}%")
    
    # Get statistics
    stats = uav.get_statistics()
    
    print("\n" + "=" * 60)
    print("Node Statistics")
    print("=" * 60)
    print(f"Node ID: {stats['node_id']}")
    print(f"Uptime: {stats['uptime']:.2f}s")
    print(f"Battery: {stats['battery']:.1f}%")
    print(f"Status: {stats['status']}")
    print(f"Beacons sent: {stats['beacons_sent']}")
    print(f"Beacons received: {stats['beacons_received']}")
    print(f"Transactions created: {stats['transactions_created']}")
    print(f"Consensus rounds: {stats['consensus_rounds']}")
    print(f"Neighbors: {stats['neighbors']}")
    print("=" * 60)

