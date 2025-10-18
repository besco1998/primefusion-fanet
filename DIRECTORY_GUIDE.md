# PrimeFusion-FANET Directory Guide

**Quick reference for navigating the project structure.**

---

## 📁 Top-Level Directories

### `/python/` - Python Implementation
**Purpose**: Proof-of-concept implementation and rapid prototyping  
**Status**: ⏳ In development  
**Contents**:
- `core/` - Core PrimeFusion modules
- `simulation/` - Multi-UAV network simulator
- `tests/` - Unit and integration tests
- `utils/` - Utility functions and helpers

### `/ns3/` - NS-3 Simulation
**Purpose**: Network simulation for validation and performance evaluation  
**Status**: ⏳ Planned  
**Contents**:
- `scratch/` - NS-3 simulation scripts
- `modules/` - Custom NS-3 modules
- `scenarios/` - Simulation scenarios

### `/docs/` - Documentation
**Purpose**: All project documentation, reports, and papers  
**Status**: ✅ Organized  
**Contents**:
- `reports/` - Research reports and plans
- `papers/` - Academic papers and bibliography
- `analysis/` - Analysis documents
- `presentations/` - Slides and posters
- `INDEX.md` - Documentation index (START HERE)

### `/results/` - Simulation Results
**Purpose**: Store all simulation outputs, figures, and tables  
**Status**: 📊 Ready for data  
**Contents**:
- `python/` - Python simulation results
- `ns3/` - NS-3 simulation results
- `figures/` - Publication-quality figures
- `tables/` - LaTeX-formatted tables

### `/scripts/` - Automation Scripts
**Purpose**: Automate testing, simulation, and analysis  
**Status**: ⏳ In development  
**Contents**:
- Testing scripts
- Simulation runners
- Figure/table generators
- GitHub setup script

### `/config/` - Configuration Files
**Purpose**: Centralized configuration for simulations  
**Status**: 📝 Ready for configs  
**Contents**:
- Simulation parameters (YAML)
- Network topology configs
- Performance targets

---

## 🔍 Detailed Directory Structure

### `/python/core/` - Core Modules

| File | Description | Status |
|------|-------------|--------|
| `blockchain.py` | Linear blockchain with Session-MAC | ⏳ To implement |
| `milestone.py` | Milestone pig-backing manager | ⏳ To implement |
| `cbor_optimizer.py` | CBOR compression (existing) | ✅ Exists, needs enhancement |
| `beacon_manager.py` | Integrated beacon manager | ✅ Exists, needs integration |
| `crypto_utils.py` | Cryptographic utilities | ✅ Exists |
| `consensus.py` | DAG consensus (existing) | ✅ Exists |
| `framework.py` | Main framework (existing) | ✅ Exists, needs fixing |

### `/python/simulation/` - Simulation

| File | Description | Status |
|------|-------------|--------|
| `network_simulator.py` | Multi-UAV network simulator | ⏳ To implement |
| `uav_node.py` | UAV node implementation | ⏳ To implement |
| `metrics_collector.py` | Performance metrics collection | ⏳ To implement |

### `/python/tests/` - Testing

| File | Description | Status |
|------|-------------|--------|
| `test_blockchain.py` | Blockchain module tests | ⏳ To implement |
| `test_milestone.py` | Milestone pig-backing tests | ⏳ To implement |
| `test_cbor.py` | CBOR compression tests | ⏳ To implement |
| `test_beacon.py` | Beacon manager tests | ⏳ To implement |
| `test_integration.py` | End-to-end integration tests | ⏳ To implement |

### `/python/utils/` - Utilities

| File | Description | Status |
|------|-------------|--------|
| `logger.py` | Logging utilities | ⏳ To implement |
| `visualizer.py` | Results visualization | ⏳ To implement |
| `comparator.py` | Literature comparison tools | ⏳ To implement |
| `message_classifier.py` | Message classification (existing) | ✅ Exists |

### `/ns3/scratch/` - NS-3 Scripts

| File | Description | Status |
|------|-------------|--------|
| `primefusion-wifi.cc` | WiFi-based simulation | ⏳ To implement |
| `primefusion-lora.cc` | LoRa-based simulation | ⏳ To implement |
| `primefusion-scalability.cc` | Scalability testing | ⏳ To implement |

### `/docs/reports/` - Research Reports

| File | Description | Priority |
|------|-------------|----------|
| `primefusion_enhanced_plan.md` | Main development plan ⭐ | **HIGH** |
| `primefusion_gap_analysis.md` | Current status ⚠️ | **HIGH** |
| `primefusion_scientific_description.md` | Thesis material 📖 | **HIGH** |
| `primefusion_simplified_plan.md` | Original plan | Medium |
| `blockchain_uav_report/` | Complete LaTeX report | Medium |

### `/docs/papers/` - Academic Papers

| File | Description | Status |
|------|-------------|--------|
| `bibliography_analysis.md` | 50 papers analyzed | ✅ Complete |
| `primefusion_summary.md` | Framework summary | ✅ Complete |
| `references.bib` | BibTeX references | ✅ Complete |

### `/scripts/` - Automation

| File | Description | Status |
|------|-------------|--------|
| `setup_github.sh` | GitHub repo setup | ✅ Ready |
| `run_python_tests.sh` | Run Python tests | ⏳ To create |
| `run_python_simulation.sh` | Run Python simulation | ⏳ To create |
| `run_ns3_experiments.sh` | Run NS-3 experiments | ⏳ To create |
| `generate_figures.py` | Generate figures | ⏳ To create |
| `generate_tables.py` | Generate tables | ⏳ To create |
| `comparative_analysis.py` | Compare with literature | ⏳ To create |

---

## 🚀 Quick Start Paths

### For Development
```
1. Read: /docs/INDEX.md
2. Follow: /docs/reports/primefusion_enhanced_plan.md
3. Check: /docs/reports/primefusion_gap_analysis.md
4. Implement: /python/core/
5. Test: /python/tests/
6. Simulate: /python/simulation/
```

### For Thesis Writing
```
1. Read: /docs/INDEX.md
2. Use: /docs/reports/primefusion_scientific_description.md
3. Reference: /docs/reports/blockchain_uav_report/
4. Cite: /docs/papers/references.bib
5. Results: /results/ (after simulations)
```

### For NS-3 Development
```
1. Read: /docs/reports/primefusion_enhanced_plan.md (Week 3-5)
2. Implement: /ns3/scratch/primefusion-wifi.cc
3. Test: /ns3/scenarios/
4. Results: /results/ns3/
```

---

## 📊 File Status Legend

- ✅ **Complete** - File exists and is ready to use
- ⏳ **In Progress** - File exists but needs work
- 📝 **Planned** - File structure ready, content to be added
- ⚠️ **Important** - Critical file, review immediately
- ⭐ **Start Here** - Entry point for new users
- 📖 **Thesis Material** - Ready for thesis integration
- 📊 **Results** - Contains simulation results

---

## 🔄 Workflow

### Week 1: Core Implementation
```
Work in: /python/core/
Test in: /python/tests/
Document: /docs/reports/
```

### Week 2: Python Simulation
```
Work in: /python/simulation/
Test in: /python/tests/
Results: /results/python/
```

### Week 3-5: NS-3 Simulation
```
Work in: /ns3/scratch/
Test in: /ns3/scenarios/
Results: /results/ns3/
```

### Week 6-7: Analysis & Documentation
```
Analyze: /results/
Generate: /results/figures/, /results/tables/
Document: /docs/reports/
Write: Thesis chapters
```

---

## 📋 Checklist for Each Phase

### Python Implementation ✓
- [ ] Core modules implemented
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Python simulation running
- [ ] Results collected

### NS-3 Validation ✓
- [ ] WiFi simulation working
- [ ] LoRa simulation working
- [ ] Scalability tests complete
- [ ] Results validated

### Documentation ✓
- [ ] Figures generated
- [ ] Tables generated
- [ ] Comparative analysis complete
- [ ] Thesis sections written

---

## 💡 Tips

1. **Always start with** `/docs/INDEX.md`
2. **Check status in** `/docs/reports/primefusion_gap_analysis.md`
3. **Follow plan in** `/docs/reports/primefusion_enhanced_plan.md`
4. **Test frequently** using `/python/tests/`
5. **Document as you go** in `/docs/`

---

**Last Updated**: October 18, 2025
