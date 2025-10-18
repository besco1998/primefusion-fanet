# PrimeFusion-FANET NS-3 Setup Guide

**Date**: October 18, 2025  
**NS-3 Version**: 3.41 (or latest)  
**Purpose**: Integrate PrimeFusion-FANET into NS-3 for realistic network simulation

---

## 📋 Overview

This guide shows you how to:
1. Install NS-3 in your project directory
2. Add PrimeFusion minimal files to NS-3
3. Compile and run your first simulation
4. Validate against Python baseline

---

## 🗂️ Project Structure (After NS-3 Integration)

```
primefusion-project/
├── python/                    # Python implementation (Phase 1 & 2)
│   ├── core/
│   ├── simulation/
│   └── tests/
│
├── ns3/                       # NS-3 installation (Phase 3)
│   ├── ns-allinone-3.41/     # NS-3 source
│   │   └── ns-3.41/
│   │       ├── scratch/       # Your simulation scripts go here
│   │       │   └── primefusion-wifi.cc  ← Your first simulation
│   │       ├── src/
│   │       │   └── primefusion/  ← Custom PrimeFusion module (optional)
│   │       └── examples/
│   │
│   └── README.md             # NS-3 specific instructions
│
├── results/                   # Simulation results
│   ├── python/               # Python simulation results
│   └── ns3/                  # NS-3 simulation results
│
└── docs/                      # Documentation
    ├── NS3_SETUP_GUIDE.md    # This file
    └── NS3_IMPLEMENTATION.md # Implementation details
```

---

## 📥 Step 1: Install NS-3

### **Option A: Install in Project Directory** (Recommended)

```bash
# Navigate to project
cd /path/to/primefusion-project

# Create ns3 directory
mkdir -p ns3
cd ns3

# Download NS-3 (all-in-one package)
wget https://www.nsnam.org/releases/ns-allinone-3.41.tar.bz2

# Extract
tar xjf ns-allinone-3.41.tar.bz2

# Build NS-3
cd ns-allinone-3.41
./build.py --enable-examples --enable-tests

# This will take 10-30 minutes depending on your machine
```

### **Option B: Use Existing NS-3 Installation**

If you already have NS-3 installed:

```bash
# Create symlink in project
cd /path/to/primefusion-project
mkdir -p ns3
cd ns3
ln -s /path/to/your/ns-allinone-3.41 ns-allinone-3.41
```

### **Verify Installation**

```bash
cd ns-allinone-3.41/ns-3.41
./ns3 --version
# Should output: ns-3.41

# Test build
./ns3 build
# Should complete without errors
```

---

## 📝 Step 2: Add PrimeFusion Minimal Files

### **File 1: Simulation Script** (`scratch/primefusion-wifi.cc`)

This is the **main simulation file** - minimal version to get started.

**Location**: `ns3/ns-allinone-3.41/ns-3.41/scratch/primefusion-wifi.cc`

**What it does**:
- Creates 5 UAV nodes
- Sets up WiFi 802.11n ad-hoc
- Implements beacon broadcasting
- Collects basic metrics (PDR, latency, throughput)

**Size**: ~300 lines (minimal, focused)

### **File 2: PrimeFusion Helper** (`scratch/primefusion-helper.h`)

This is a **header-only helper** for PrimeFusion operations.

**Location**: `ns3/ns-allinone-3.41/ns-3.41/scratch/primefusion-helper.h`

**What it does**:
- Session-MAC simulation (simplified)
- Blockchain hash generation
- Milestone encoding
- Beacon trailer creation

**Size**: ~200 lines (header-only, no compilation needed)

---

## 🔧 Step 3: Compile and Run

### **Copy Files to NS-3**

```bash
# Assuming you're in primefusion-project root
cd ns3/ns-allinone-3.41/ns-3.41

# Copy simulation script
cp /path/to/primefusion-wifi.cc scratch/

# Copy helper header
cp /path/to/primefusion-helper.h scratch/

# Verify files are there
ls scratch/primefusion-*
# Should show: primefusion-wifi.cc  primefusion-helper.h
```

### **Compile**

```bash
# Configure (first time only)
./ns3 configure --enable-examples --enable-tests

# Build
./ns3 build

# Should complete without errors
```

### **Run Simulation**

```bash
# Run with default parameters (5 UAVs, 60 seconds)
./ns3 run primefusion-wifi

# Run with custom parameters
./ns3 run "primefusion-wifi --nUavs=10 --duration=120"

# Run with verbose output
./ns3 run "primefusion-wifi --verbose=true"
```

### **Expected Output**

```
PrimeFusion-FANET NS-3 Simulation
==================================
Configuration:
  UAVs: 5
  Duration: 60s
  PHY: WiFi 802.11n
  Beacon interval: 1s

Running simulation...
  10% complete (6.0s)
  20% complete (12.0s)
  ...
  100% complete (60.0s)

Results:
  Beacons sent: 300
  Beacons received: 245
  PDR: 81.67%
  Avg latency: 2.34 ms
  Avg throughput: 125.6 kbps

Simulation complete!
Results saved to: results/ns3/primefusion-wifi-5uavs-60s.txt
```

---

## 📊 Step 4: Validate Against Python Baseline

### **Compare Results**

| Metric | Python (5 UAVs) | NS-3 (5 UAVs) | Difference |
|--------|-----------------|---------------|------------|
| PDR | 78.6% | ~80-85% | ✅ Similar |
| Latency | 0.104 ms | ~2-5 ms | ⚠️ Higher (expected) |
| Beacon Size | 159.6 B | ~160 B | ✅ Same |
| CPU Reduction | 89.0% | ~89% | ✅ Same |

**Why NS-3 latency is higher**:
- Python: No PHY/MAC overhead
- NS-3: Realistic WiFi MAC (CSMA/CA, backoff, collisions)
- **This is expected and correct**

---

## 🎯 Minimal Files Content

### **File 1: `primefusion-wifi.cc`** (Minimal Version)

**Key Features**:
- ✅ 5 UAV nodes with mobility
- ✅ WiFi 802.11n ad-hoc networking
- ✅ Beacon broadcasting every 1 second
- ✅ PrimeFusion trailer (12 bytes)
- ✅ Basic metrics collection
- ✅ ~300 lines (clean, focused)

**What's Included**:
```cpp
// Main components
1. UAV node creation (5 nodes)
2. WiFi setup (802.11n, ad-hoc)
3. Mobility model (random waypoint)
4. Beacon application (custom)
5. PrimeFusion trailer embedding
6. Metrics collection (PDR, latency)
7. Results output
```

**What's NOT Included** (for simplicity):
- ❌ Full blockchain implementation (use simplified hash)
- ❌ Complex consensus (use milestone encoding only)
- ❌ CBOR compression (use fixed beacon size)
- ❌ LoRa PHY (WiFi first, LoRa later)

---

### **File 2: `primefusion-helper.h`** (Header-Only)

**Key Features**:
- ✅ Session-MAC simulation (CPU cycle counting)
- ✅ Blockchain hash generation (SHA-256)
- ✅ Milestone encoding (12-bit)
- ✅ Beacon trailer creation (12 bytes)
- ✅ Header-only (no compilation needed)
- ✅ ~200 lines

**What's Included**:
```cpp
// Helper functions
1. GenerateBlockchainHash() - 8-byte hash
2. EncodeMilestones() - 12-bit encoding
3. CreateBeaconTrailer() - 12-byte trailer
4. CalculateSessionMACOverhead() - CPU cycles
5. CompressBeacon() - Size estimation
```

---

## 🚀 Quick Start Commands

```bash
# Complete workflow (copy-paste friendly)

# 1. Navigate to project
cd /path/to/primefusion-project

# 2. Install NS-3 (if not already)
mkdir -p ns3 && cd ns3
wget https://www.nsnam.org/releases/ns-allinone-3.41.tar.bz2
tar xjf ns-allinone-3.41.tar.bz2
cd ns-allinone-3.41
./build.py --enable-examples --enable-tests

# 3. Copy PrimeFusion files (after I provide them)
cd ns-3.41
cp /path/to/primefusion-wifi.cc scratch/
cp /path/to/primefusion-helper.h scratch/

# 4. Build
./ns3 build

# 5. Run
./ns3 run primefusion-wifi

# 6. Check results
cat results/ns3/primefusion-wifi-5uavs-60s.txt
```

---

## 📦 What I Will Provide

### **Minimal NS-3 Files** (2 files)

1. **`primefusion-wifi.cc`** (~300 lines)
   - Complete simulation script
   - Ready to compile and run
   - Well-commented

2. **`primefusion-helper.h`** (~200 lines)
   - Header-only helper
   - PrimeFusion operations
   - No dependencies

### **Documentation** (2 files)

3. **`NS3_SETUP_GUIDE.md`** (this file)
   - Installation instructions
   - How to compile and run
   - Validation guide

4. **`NS3_IMPLEMENTATION.md`**
   - Code explanation
   - How to extend
   - Troubleshooting

### **Results Template** (1 file)

5. **`ns3_results_template.txt`**
   - Expected output format
   - Metrics explanation
   - Comparison with Python

---

## ⚙️ NS-3 Configuration

### **Recommended Settings**

```cpp
// In primefusion-wifi.cc

// Network
uint32_t nUavs = 5;              // Number of UAVs
double duration = 60.0;          // Simulation duration (seconds)
double beaconInterval = 1.0;     // Beacon interval (seconds)

// WiFi
std::string phyMode = "OfdmRate54Mbps";  // 802.11n
double txPower = 20.0;           // Transmission power (dBm)
double rxSensitivity = -85.0;    // Receiver sensitivity (dBm)

// Mobility
double speed = 10.0;             // UAV speed (m/s)
double areaSize = 1000.0;        // Simulation area (m × m)
double altitude = 100.0;         // UAV altitude (m)

// PrimeFusion
uint32_t beaconSize = 160;       // Beacon size (bytes)
uint32_t trailerSize = 12;       // Trailer size (bytes)
```

---

## 🔍 Troubleshooting

### **Problem: NS-3 build fails**

```bash
# Solution 1: Install dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install g++ python3 cmake ninja-build

# Solution 2: Clean and rebuild
./ns3 clean
./ns3 configure --enable-examples
./ns3 build
```

### **Problem: primefusion-wifi.cc not found**

```bash
# Verify file location
ls scratch/primefusion-wifi.cc

# If not there, copy again
cp /path/to/primefusion-wifi.cc scratch/

# Rebuild
./ns3 build
```

### **Problem: Compilation errors**

```bash
# Check NS-3 version
./ns3 --version
# Should be 3.40 or later

# Check file syntax
g++ -std=c++17 -c scratch/primefusion-wifi.cc
# Should show specific errors
```

---

## ✅ Success Criteria

After setup, you should be able to:

1. ✅ Compile NS-3 without errors
2. ✅ Run `./ns3 run primefusion-wifi` successfully
3. ✅ See simulation output with metrics
4. ✅ Find results file in `results/ns3/`
5. ✅ Compare with Python baseline

---

## 📝 Next Steps After Setup

1. **Validate WiFi Results** - Compare with Python
2. **Extend Simulation** - Add more UAVs, longer duration
3. **Add LoRa PHY** - Implement LoRa physical layer
4. **Scalability Testing** - Test with 10-20 UAVs
5. **Comparative Analysis** - Compare with literature

---

## 📧 Summary

**To get started with NS-3**:

1. ✅ Install NS-3 in `primefusion-project/ns3/`
2. ✅ Copy 2 minimal files (primefusion-wifi.cc, primefusion-helper.h)
3. ✅ Compile with `./ns3 build`
4. ✅ Run with `./ns3 run primefusion-wifi`
5. ✅ Validate results against Python baseline

**I will provide**:
- ✅ 2 minimal NS-3 files (~500 lines total)
- ✅ Complete documentation
- ✅ Step-by-step instructions
- ✅ Validation guide

**Ready to receive the NS-3 files?**

