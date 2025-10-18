"""
PrimeFusion-FANET Comprehensive Test Suite
==========================================

Tests all core modules and integration.

Author: PrimeFusion-FANET Team
Date: October 2025
Version: 1.0
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'core'))

import time
from session_mac import SessionMAC
from blockchain import LinearBlockchain
from milestone import MilestonePigBacking
from cbor_optimizer import CBORCompressor
from beacon_integrated import IntegratedBeaconManager


def test_session_mac():
    """Test Session-MAC authentication"""
    print("\n" + "=" * 60)
    print("TEST: Session-MAC Authentication")
    print("=" * 60)
    
    session_mac = SessionMAC(node_id=1)
    
    # Test signing 100 blocks
    signatures = []
    for i in range(100):
        block_data = f"Block {i}".encode()
        signature, metrics = session_mac.sign_block(i, block_data)
        signatures.append((i, block_data, signature))
        assert metrics.success, f"Signing failed for block {i}"
    
    # Verify all signatures
    for i, block_data, signature in signatures:
        valid, metrics = session_mac.verify_block(i, block_data, signature)
        assert valid, f"Verification failed for block {i}"
        assert metrics.success, f"Verification metrics failed for block {i}"
    
    # Check performance
    stats = session_mac.get_performance_stats()
    assert stats['cpu_reduction_vs_pure_ed25519'] >= 15.0, \
        f"CPU reduction {stats['cpu_reduction_vs_pure_ed25519']:.1f}% < 15%"
    
    print(f"✓ Signed and verified 100 blocks")
    print(f"✓ CPU reduction: {stats['cpu_reduction_vs_pure_ed25519']:.1f}% (target: >15%)")
    print(f"✓ Avg root latency: {stats['avg_root_latency']:.3f} ms")
    print(f"✓ Avg interim latency: {stats['avg_interim_latency']:.3f} ms")
    print("✓ Session-MAC: PASS")
    return True


def test_blockchain():
    """Test Linear Blockchain"""
    print("\n" + "=" * 60)
    print("TEST: Linear Blockchain")
    print("=" * 60)
    
    blockchain = LinearBlockchain(node_id=1)
    
    # Add 20 blocks
    for i in range(20):
        block_data = f"Transaction {i}".encode()
        block, metrics = blockchain.add_block(block_data)
        assert metrics.success, f"Adding block {i} failed"
        assert block is not None, f"Block {i} is None"
    
    # Verify chain
    assert blockchain.is_chain_valid(), "Blockchain validation failed"
    
    # Get latest hash
    hash_8bytes, metrics = blockchain.get_latest_hash()
    assert len(hash_8bytes) == 16, f"Hash length {len(hash_8bytes)} != 16"  # 8 bytes = 16 hex chars
    assert metrics.success, "Getting latest hash failed"
    
    # Check performance
    stats = blockchain.get_performance_stats()
    assert stats['chain_valid'], "Chain not valid"
    assert stats['avg_add_latency'] < 1.0, f"Add latency {stats['avg_add_latency']:.3f}ms > 1ms"
    
    print(f"✓ Added 20 blocks")
    print(f"✓ Chain valid: {stats['chain_valid']}")
    print(f"✓ Avg add latency: {stats['avg_add_latency']:.3f} ms (target: <1ms)")
    print(f"✓ Session-MAC CPU reduction: {stats['session_mac_cpu_reduction']:.1f}%")
    print("✓ Blockchain: PASS")
    return True


def test_milestone():
    """Test Milestone Pig-Backing"""
    print("\n" + "=" * 60)
    print("TEST: Milestone Pig-Backing")
    print("=" * 60)
    
    milestone_mgr = MilestonePigBacking(node_id=1)
    
    # Add consensus rounds
    for i in range(15):
        milestone_mgr.add_consensus_round(i + 1)
    
    # Select milestones
    indices, metrics = milestone_mgr.select_milestones()
    assert metrics.success, "Selecting milestones failed"
    assert len(indices) == 3, f"Milestone count {len(indices)} != 3"
    
    # Encode milestones
    encoded, metrics = milestone_mgr.encode_milestones(indices)
    assert metrics.success, "Encoding milestones failed"
    assert len(encoded) == 2, f"Encoded size {len(encoded)} != 2 bytes"
    
    # Decode milestones
    decoded, metrics = milestone_mgr.decode_milestones(encoded)
    assert metrics.success, "Decoding milestones failed"
    assert decoded == indices, f"Decoded {decoded} != original {indices}"
    
    # Create beacon trailer
    blockchain_hash = "7a24013b6a411875"
    trailer, metrics = milestone_mgr.create_beacon_trailer(blockchain_hash, indices)
    assert metrics.success, "Creating trailer failed"
    assert len(trailer) == 12, f"Trailer size {len(trailer)} != 12 bytes"
    
    # Parse beacon trailer
    parsed, metrics = milestone_mgr.parse_beacon_trailer(trailer)
    assert metrics.success, "Parsing trailer failed"
    assert parsed['blockchain_hash'] == blockchain_hash, "Hash mismatch"
    assert parsed['milestone_indices'] == indices, "Indices mismatch"
    
    # Check performance
    stats = milestone_mgr.get_performance_stats()
    assert stats['avg_trailer_latency'] < 1.0, \
        f"Trailer latency {stats['avg_trailer_latency']:.3f}ms > 1ms"
    
    print(f"✓ Encoded/decoded milestones correctly")
    print(f"✓ Trailer size: {stats['trailer_size_bytes']} bytes (target: 12)")
    print(f"✓ Avg trailer latency: {stats['avg_trailer_latency']:.3f} ms (target: <1ms)")
    print("✓ Milestone: PASS")
    return True


def test_cbor():
    """Test CBOR Compression"""
    print("\n" + "=" * 60)
    print("TEST: CBOR Compression")
    print("=" * 60)
    
    compressor = CBORCompressor()
    
    # Test data with blockchain keys
    test_data = {
        'uav_id': 1,
        'position': {'latitude': 40.7128, 'longitude': -74.0060, 'altitude': 100.0},
        'velocity': {'x': 1.5, 'y': 0.8, 'z': 0.0},
        'blockchain': {'block_hash': 'abc123', 'block_index': 42},
        'milestone': [1, 2, 3],
        'timestamp': time.time()
    }
    
    # Compress
    compressed, metrics = compressor.compress(test_data)
    assert metrics.success, "Compression failed"
    assert metrics.compression_ratio < 0.70, \
        f"Compression ratio {metrics.compression_ratio:.3f} >= 0.70"
    
    # Decompress
    decompressed, metrics = compressor.decompress(compressed)
    assert metrics.success, "Decompression failed"
    assert decompressed == test_data, "Decompressed data doesn't match"
    
    # Check performance
    stats = compressor.get_compression_stats()
    assert stats['avg_compression_ratio'] <= 0.70, \
        f"Avg compression ratio {stats['avg_compression_ratio']:.3f} > 0.70"
    
    print(f"✓ Compressed and decompressed correctly")
    print(f"✓ Compression ratio: {stats['avg_compression_ratio']:.3f} (target: <0.70)")
    print(f"✓ Avg latency: {stats['avg_latency']:.3f} ms")
    print(f"✓ Total bytes saved: {stats['total_bytes_saved']}")
    print("✓ CBOR: PASS")
    return True


def test_integrated_beacon():
    """Test Integrated Beacon Manager"""
    print("\n" + "=" * 60)
    print("TEST: Integrated Beacon Manager")
    print("=" * 60)
    
    beacon_mgr = IntegratedBeaconManager(node_id=1)
    
    # Add blockchain transactions
    for i in range(5):
        tx_data = f"Transaction {i}".encode()
        metrics = beacon_mgr.add_blockchain_transaction(tx_data)
        assert metrics.success, f"Transaction {i} failed"
    
    # Add consensus rounds
    for i in range(10):
        beacon_mgr.add_consensus_round(i + 1)
    
    # Generate beacons
    beacons = []
    for i in range(5):
        uav_data = {
            'uav_id': 1,
            'position': {'latitude': 40.7128, 'longitude': -74.0060, 'altitude': 100.0},
            'velocity': {'x': 1.5, 'y': 0.8, 'z': 0.0},
            'status': 'active',
            'battery': 85.5,
            'timestamp': time.time()
        }
        
        beacon_bytes, metrics = beacon_mgr.generate_beacon(uav_data)
        assert metrics.success, f"Beacon {i} generation failed"
        assert metrics.trailer_size == 12, f"Trailer size {metrics.trailer_size} != 12"
        beacons.append(beacon_bytes)
    
    # Parse a beacon
    parsed, metrics = beacon_mgr.parse_beacon(beacons[0])
    assert metrics.success, "Beacon parsing failed"
    assert 'uav_data' in parsed, "UAV data missing"
    assert 'blockchain_hash' in parsed, "Blockchain hash missing"
    assert 'milestone_indices' in parsed, "Milestone indices missing"
    
    # Check performance
    stats = beacon_mgr.get_performance_stats()
    assert stats['avg_total_latency'] < 5.0, \
        f"Avg latency {stats['avg_total_latency']:.3f}ms >= 5ms"
    assert stats['avg_trailer_size'] <= 12, \
        f"Avg trailer {stats['avg_trailer_size']:.1f}B > 12B"
    
    print(f"✓ Generated and parsed 5 beacons")
    print(f"✓ Avg beacon size: {stats['avg_beacon_size']:.1f} bytes")
    print(f"✓ Avg trailer size: {stats['avg_trailer_size']:.1f} bytes (target: ≤12)")
    print(f"✓ Avg total latency: {stats['avg_total_latency']:.3f} ms (target: <5ms)")
    print(f"✓ Compression ratio: {stats['avg_compression_ratio']:.3f}")
    print("✓ Integrated Beacon: PASS")
    return True


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("PRIMEFUSION-FANET COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Session-MAC", test_session_mac),
        ("Blockchain", test_blockchain),
        ("Milestone", test_milestone),
        ("CBOR", test_cbor),
        ("Integrated Beacon", test_integrated_beacon)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name}: FAIL")
            print(f"  Error: {str(e)}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {name}: {status}")
    
    print("=" * 60)
    print(f"TOTAL: {passed}/{total} tests passed")
    print("=" * 60)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

