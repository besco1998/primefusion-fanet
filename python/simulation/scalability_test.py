"""
PrimeFusion-FANET Scalability Testing
=====================================

Tests PrimeFusion performance with varying numbers of UAVs.

Author: PrimeFusion-FANET Team
Date: October 2025
Version: 1.0
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'core'))

import json
import time
from typing import List, Dict
from network_simulator import NetworkSimulator, SimulationConfig


def run_scalability_test(uav_counts: List[int], duration: float = 60.0) -> List[Dict]:
    """
    Run scalability tests with different UAV counts.
    
    Args:
        uav_counts: List of UAV counts to test
        duration: Simulation duration for each test (seconds)
        
    Returns:
        List of results for each configuration
    """
    print("=" * 60)
    print("PRIMEFUSION-FANET SCALABILITY TEST")
    print("=" * 60)
    print(f"\nTesting UAV counts: {uav_counts}")
    print(f"Duration per test: {duration}s")
    print("=" * 60)
    
    all_results = []
    
    for num_uavs in uav_counts:
        print(f"\n{'='*60}")
        print(f"Test: {num_uavs} UAVs")
        print(f"{'='*60}")
        
        # Create configuration
        config = SimulationConfig(
            num_uavs=num_uavs,
            simulation_duration=duration,
            time_step=0.1,
            beacon_interval=1.0,
            communication_range=500.0,
            transaction_probability=0.05,
            consensus_interval=5.0
        )
        
        # Run simulation
        simulator = NetworkSimulator(config)
        results = simulator.run()
        
        # Add to results
        all_results.append(results)
        
        # Print summary
        print(f"\nSummary for {num_uavs} UAVs:")
        print(f"  PDR: {results['network']['packet_delivery_ratio']:.2%}")
        print(f"  Avg beacon latency: {results['performance']['avg_beacon_latency']:.3f} ms")
        print(f"  Avg neighbors: {results['network']['avg_neighbors']:.1f}")
        print(f"  CPU reduction: {results['performance']['avg_cpu_reduction']:.1f}%")
    
    return all_results


def print_comparative_analysis(all_results: List[Dict]):
    """Print comparative analysis across all tests"""
    print("\n" + "=" * 60)
    print("COMPARATIVE ANALYSIS")
    print("=" * 60)
    
    print("\n{:<10} {:<10} {:<10} {:<15} {:<15} {:<15}".format(
        "UAVs", "PDR (%)", "Neighbors", "Latency (ms)", "Size (B)", "CPU Red (%)"
    ))
    print("-" * 80)
    
    for results in all_results:
        num_uavs = results['config']['num_uavs']
        pdr = results['network']['packet_delivery_ratio'] * 100
        neighbors = results['network']['avg_neighbors']
        latency = results['performance']['avg_beacon_latency']
        size = results['performance']['avg_beacon_size']
        cpu_red = results['performance']['avg_cpu_reduction']
        
        print("{:<10} {:<10.1f} {:<10.1f} {:<15.3f} {:<15.1f} {:<15.1f}".format(
            num_uavs, pdr, neighbors, latency, size, cpu_red
        ))
    
    print("-" * 80)


def save_results(all_results: List[Dict], filename: str = "scalability_results.json"):
    """Save results to JSON file"""
    output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'results', filename)
    
    # Create results directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\nResults saved to: {output_path}")
    return output_path


def generate_latex_table(all_results: List[Dict]) -> str:
    """Generate LaTeX table from results"""
    latex = []
    latex.append("\\begin{table}[htbp]")
    latex.append("\\centering")
    latex.append("\\caption{PrimeFusion-FANET Scalability Test Results}")
    latex.append("\\label{tab:scalability}")
    latex.append("\\begin{tabular}{|c|c|c|c|c|c|}")
    latex.append("\\hline")
    latex.append("\\textbf{UAVs} & \\textbf{PDR (\\%)} & \\textbf{Neighbors} & \\textbf{Latency (ms)} & \\textbf{Size (B)} & \\textbf{CPU Red (\\%)} \\\\")
    latex.append("\\hline")
    
    for results in all_results:
        num_uavs = results['config']['num_uavs']
        pdr = results['network']['packet_delivery_ratio'] * 100
        neighbors = results['network']['avg_neighbors']
        latency = results['performance']['avg_beacon_latency']
        size = results['performance']['avg_beacon_size']
        cpu_red = results['performance']['avg_cpu_reduction']
        
        latex.append(f"{num_uavs} & {pdr:.1f} & {neighbors:.1f} & {latency:.3f} & {size:.1f} & {cpu_red:.1f} \\\\")
    
    latex.append("\\hline")
    latex.append("\\end{tabular}")
    latex.append("\\end{table}")
    
    return "\n".join(latex)


if __name__ == "__main__":
    # Scalability test configurations
    uav_counts = [3, 5, 10, 15, 20]
    duration = 60.0  # 60 seconds per test
    
    # Run tests
    start_time = time.time()
    all_results = run_scalability_test(uav_counts, duration)
    total_time = time.time() - start_time
    
    # Print comparative analysis
    print_comparative_analysis(all_results)
    
    # Save results
    json_path = save_results(all_results)
    
    # Generate LaTeX table
    latex_table = generate_latex_table(all_results)
    latex_path = os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'scalability_table.tex')
    with open(latex_path, 'w') as f:
        f.write(latex_table)
    print(f"LaTeX table saved to: {latex_path}")
    
    print("\n" + "=" * 60)
    print("SCALABILITY TEST COMPLETE")
    print("=" * 60)
    print(f"Total execution time: {total_time:.2f}s")
    print(f"Tests completed: {len(all_results)}")
    print(f"Results saved to: {json_path}")
    print("=" * 60)

