# PrimeFusion-FANET: Blockchain-Optimized UAV Swarm Communication

**A lightweight blockchain framework for Flying Ad-hoc Networks (FANETs) with beacon-embedded consensus, Session-MAC authentication, and milestone pig-backing.**

---

## Project Overview

PrimeFusion-FANET addresses the critical challenge of integrating blockchain security into resource-constrained UAV swarms operating over LoRa networks. The framework introduces three key innovations:

1. **Session-MAC Authentication**: Hybrid Ed25519 + HMAC scheme reducing CPU overhead by >15%
2. **Milestone Pig-Backing**: Embedding DAG consensus in beacons, reducing airtime by >90%
3. **CBOR Compression**: UAV-optimized compression achieving >30% size reduction

---

## Project Structure

```
primefusion-project/
│
├── python/                          # Python implementation (proof-of-concept)
│   ├── core/                        # Core PrimeFusion modules
│   │   ├── blockchain.py            # Linear blockchain with Session-MAC
│   │   ├── milestone.py             # Milestone pig-backing manager
│   │   ├── cbor_optimizer.py        # CBOR compression with UAV dictionary
│   │   ├── beacon_manager.py        # Integrated beacon manager
│   │   └── crypto_utils.py          # Cryptographic utilities
│   │
│   ├── simulation/                  # Python-based simulation
│   │   ├── network_simulator.py     # Multi-UAV network simulator
│   │   ├── uav_node.py              # UAV node implementation
│   │   └── metrics_collector.py     # Performance metrics collection
│   │
│   ├── tests/                       # Unit and integration tests
│   │   ├── test_blockchain.py       # Blockchain module tests
│   │   ├── test_milestone.py        # Milestone pig-backing tests
│   │   ├── test_cbor.py             # CBOR compression tests
│   │   ├── test_beacon.py           # Beacon manager tests
│   │   └── test_integration.py      # End-to-end integration tests
│   │
│   └── utils/                       # Utility modules
│       ├── logger.py                # Logging utilities
│       ├── visualizer.py            # Results visualization
│       └── comparator.py            # Literature comparison tools
│
├── ns3/                             # NS-3 simulation (validation)
│   ├── scratch/                     # NS-3 simulation scripts
│   │   ├── primefusion-wifi.cc      # WiFi-based simulation
│   │   ├── primefusion-lora.cc      # LoRa-based simulation
│   │   └── primefusion-scalability.cc # Scalability testing
│   │
│   ├── modules/                     # Custom NS-3 modules
│   │   └── primefusion/             # PrimeFusion NS-3 module
│   │       ├── model/               # C++ implementation
│   │       ├── helper/              # NS-3 helper classes
│   │       └── examples/            # Example scenarios
│   │
│   └── scenarios/                   # Simulation scenarios
│       ├── urban-delivery.json      # Urban UAV delivery scenario
│       ├── disaster-response.json   # Disaster response scenario
│       └── surveillance.json        # Surveillance mission scenario
│
├── docs/                            # Documentation
│   ├── reports/                     # Research reports
│   │   ├── blockchain_uav_report/   # Comprehensive LaTeX report
│   │   ├── gap_analysis.md          # What's achieved vs. required
│   │   ├── scientific_description.md # Problem, methodology, impact
│   │   ├── simplified_plan.md       # Original simplified plan
│   │   └── enhanced_plan.md         # Enhanced development plan
│   │
│   ├── papers/                      # Academic papers
│   │   ├── bibliography_analysis.md # Bibliography analysis
│   │   ├── primefusion_summary.md   # PrimeFusion framework summary
│   │   └── references.bib           # BibTeX references
│   │
│   ├── presentations/               # Presentation materials
│   │   └── (slides, posters, etc.)
│   │
│   └── analysis/                    # Analysis documents
│       ├── comparative_analysis.md  # Comparison with literature
│       └── performance_metrics.md   # Performance metrics definition
│
├── results/                         # Simulation results
│   ├── python/                      # Python simulation results
│   │   ├── raw_data/                # Raw CSV/JSON data
│   │   └── processed/               # Processed results
│   │
│   ├── ns3/                         # NS-3 simulation results
│   │   ├── wifi/                    # WiFi simulation results
│   │   ├── lora/                    # LoRa simulation results
│   │   └── scalability/             # Scalability test results
│   │
│   ├── figures/                     # Generated figures (PDF/PNG)
│   │   ├── consensus_latency.pdf
│   │   ├── scalability_pdr.pdf
│   │   └── compression_ratio.pdf
│   │
│   └── tables/                      # Generated tables (LaTeX/CSV)
│       ├── performance_comparison.tex
│       └── literature_comparison.tex
│
├── scripts/                         # Automation scripts
│   ├── run_python_tests.sh          # Run Python tests
│   ├── run_python_simulation.sh     # Run Python simulation
│   ├── run_ns3_experiments.sh       # Run NS-3 experiments
│   ├── generate_figures.py          # Generate publication figures
│   ├── generate_tables.py           # Generate LaTeX tables
│   └── comparative_analysis.py      # Compare with literature
│
├── config/                          # Configuration files
│   ├── simulation_params.yaml       # Simulation parameters
│   ├── network_topology.yaml        # Network topology configs
│   └── performance_targets.yaml     # Performance targets
│
├── .gitignore                       # Git ignore file
├── requirements.txt                 # Python dependencies
├── LICENSE                          # Project license
└── README.md                        # This file
```

---

## Quick Start

### Python Implementation

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run unit tests
cd python/tests
python3.11 -m pytest

# Run Python simulation
cd python/simulation
python3.11 network_simulator.py --num-uavs 5 --duration 60

# Generate results
cd scripts
./run_python_simulation.sh
python3.11 generate_figures.py
```

### NS-3 Simulation

```bash
# Compile NS-3 with PrimeFusion module
cd ns3
./ns3 configure --enable-examples
./ns3 build

# Run WiFi simulation
./ns3 run "primefusion-wifi --numUavs=5 --simulationTime=60"

# Run LoRa simulation
./ns3 run "primefusion-lora --numUavs=5 --simulationTime=60"

# Run scalability tests
cd scripts
./run_ns3_experiments.sh
```

---

## Development Workflow

### Phase 1: Python Proof-of-Concept (Current)
- ✅ Core modules implementation
- ✅ Unit testing
- ⏳ Multi-UAV simulation
- ⏳ Performance benchmarking

### Phase 2: NS-3 Validation (Next)
- ⏳ WiFi-based validation
- ⏳ LoRa PHY integration
- ⏳ Scalability testing
- ⏳ Comparative analysis

### Phase 3: Documentation & Publication (Final)
- ⏳ Results analysis
- ⏳ Thesis integration
- ⏳ Paper preparation
- ⏳ Presentation materials

---

## Key Performance Targets

| Metric | Target | Status |
|--------|--------|--------|
| Consensus Latency | <500ms | ⏳ Testing |
| Beacon Overhead | <12 bytes | ⏳ Testing |
| Compression Ratio | <0.70 | ⏳ Testing |
| CPU Reduction (Session-MAC) | >15% | ⏳ Testing |
| Airtime Reduction (Milestone) | >90% | ⏳ Testing |
| Packet Delivery Ratio | >80% | ⏳ Testing |

---

## Research Contributions

1. **Novel Session-MAC Scheme**: First hybrid Ed25519 + HMAC authentication for blockchain-UAV systems
2. **Milestone Pig-Backing**: Zero-overhead consensus through beacon embedding
3. **Integrated Optimization**: Simultaneous airtime, CPU, and storage optimization
4. **Backward Compatibility**: Drop-in optimization for existing UAV protocols

---

## Comparative Analysis

PrimeFusion is compared against:
- Khan & Mohjazi (2023) - IOTA Tangle for UAVs
- Hossain et al. (2024) - Private blockchain with PBFT
- Hafeez et al. (2023) - Blockchain for UAV swarms survey
- IETF RFC 8724 - SCHC compression for LPWAN

See `docs/analysis/comparative_analysis.md` for detailed comparison.

---

## Documentation

- **[Enhanced Development Plan](docs/reports/enhanced_plan.md)** - Complete development roadmap
- **[Scientific Description](docs/reports/scientific_description.md)** - Problem, methodology, impact
- **[Gap Analysis](docs/reports/gap_analysis.md)** - What's achieved vs. required
- **[Bibliography Analysis](docs/papers/bibliography_analysis.md)** - Literature review

---

## Testing

### Unit Tests
```bash
cd python/tests
python3.11 -m pytest test_blockchain.py -v
python3.11 -m pytest test_milestone.py -v
python3.11 -m pytest test_cbor.py -v
```

### Integration Tests
```bash
python3.11 -m pytest test_integration.py -v
```

### Performance Benchmarks
```bash
cd python/simulation
python3.11 network_simulator.py --benchmark
```

---

## Results & Visualization

All results are stored in `results/` directory:
- **Raw data**: CSV/JSON format in `python/raw_data/` and `ns3/`
- **Figures**: Publication-quality PDF/PNG in `figures/`
- **Tables**: LaTeX-formatted tables in `tables/`

Generate figures and tables:
```bash
cd scripts
python3.11 generate_figures.py
python3.11 generate_tables.py
```

---

## Contributing

This is a research project. For questions or collaboration:
- Review the [Enhanced Development Plan](docs/reports/enhanced_plan.md)
- Check the [Gap Analysis](docs/reports/gap_analysis.md)
- See current status in project structure above

---

## License

[Specify license - e.g., MIT, Apache 2.0, or Academic Use Only]

---

## Citation

If you use PrimeFusion in your research, please cite:

```bibtex
@article{primefusion2025,
  title={PrimeFusion-FANET: Lightweight Blockchain for UAV Swarms with Beacon-Embedded Consensus},
  author={[Your Name]},
  journal={[Target Journal]},
  year={2025}
}
```

---

## Acknowledgments

This research builds upon the work of:
- Khan & Mohjazi (2023) - Blockchain-enabled UAV networks
- Hossain et al. (2024) - Blockchain integration in UAV networks
- Hafeez et al. (2023) - Blockchain for UAV swarms survey
- IOTA Foundation - DAG-based distributed ledger technology

See `docs/papers/references.bib` for complete bibliography.

---

## Contact

[Your contact information]

---

**Last Updated**: October 2025  
**Version**: 2.0 (Enhanced Implementation)

