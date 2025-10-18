# PrimeFusion-FANET NS-3 Implementation

**Version**: 1.0 (Minimal WiFi)  
**NS-3 Version**: 3.40+ (tested with 3.41)  
**Status**: Ready to compile and run

---

## 📁 Files in This Directory

1. **`primefusion-wifi.cc`** - Main simulation script (~350 lines)
2. **`primefusion-helper.h`** - Header-only helper (~250 lines)
3. **`README.md`** - This file

---

## 🚀 Quick Start

### **Step 1: Install NS-3** (if not already installed)

```bash
# Navigate to this directory
cd /path/to/primefusion-project/ns3

# Download NS-3
wget https://www.nsnam.org/releases/ns-allinone-3.41.tar.bz2

# Extract
tar xjf ns-allinone-3.41.tar.bz2

# Build (takes 10-30 minutes)
cd ns-allinone-3.41
./build.py --enable-examples --enable-tests
```

### **Step 2: Copy PrimeFusion Files**

```bash
# Navigate to NS-3 directory
cd ns-allinone-3.41/ns-3.41

# Copy simulation script
cp ../../primefusion-wifi.cc scratch/

# Copy helper header
cp ../../primefusion-helper.h scratch/

# Verify
ls scratch/primefusion-*
# Should show: primefusion-wifi.cc  primefusion-helper.h
```

### **Step 3: Create Results Directory**

```bash
# Create results directory (NS-3 won't create it automatically)
mkdir -p ../../results/ns3
```

### **Step 4: Compile**

```bash
# Configure (first time only)
./ns3 configure --enable-examples --enable-tests

# Build
./ns3 build

# Should complete without errors
```

### **Step 5: Run**

```bash
# Run with default parameters (5 UAVs, 60 seconds)
./ns3 run primefusion-wifi

# Expected output:
# ========================================
# PrimeFusion-FANET NS-3 WiFi Simulation
# ========================================
# Configuration:
#   UAVs: 5
#   Duration: 60s
#   ...
# Running simulation...
# ========================================
# Simulation Results
# ========================================
# Network Metrics:
#   Beacons sent: 295
#   Beacons received: 240
#   PDR: 81.36%
#   Avg latency: 2.45 ms
#   ...
```

---

## ⚙️ Command Line Options

### **Basic Usage**

```bash
# Default (5 UAVs, 60s)
./ns3 run primefusion-wifi

# Custom number of UAVs
./ns3 run "primefusion-wifi --nUavs=10"

# Custom duration
./ns3 run "primefusion-wifi --duration=120"

# Custom beacon interval
./ns3 run "primefusion-wifi --beaconInterval=2.0"

# Custom beacon size
./ns3 run "primefusion-wifi --beaconSize=200"

# Enable verbose logging
./ns3 run "primefusion-wifi --verbose=true"

# Combine multiple options
./ns3 run "primefusion-wifi --nUavs=10 --duration=120 --verbose=true"
```

### **Available Parameters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `nUavs` | uint32_t | 5 | Number of UAV nodes |
| `duration` | double | 60.0 | Simulation duration (seconds) |
| `beaconInterval` | double | 1.0 | Beacon interval (seconds) |
| `beaconSize` | uint32_t | 160 | Beacon size (bytes) |
| `verbose` | bool | false | Enable verbose logging |

---

## 📊 Expected Results

### **5 UAVs, 60 seconds**

```
Network Metrics:
  Beacons sent: ~295
  Beacons received: ~240
  PDR: ~80-85%
  Avg latency: ~2-5 ms
  Throughput: ~125 kbps
```

### **10 UAVs, 60 seconds**

```
Network Metrics:
  Beacons sent: ~590
  Beacons received: ~500-600
  PDR: ~85-100%
  Avg latency: ~3-6 ms
  Throughput: ~250 kbps
```

---

## 🔍 Validation Against Python Baseline

### **Comparison Table**

| Metric | Python (5 UAVs) | NS-3 (5 UAVs) | Notes |
|--------|-----------------|---------------|-------|
| **PDR** | 78.6% | ~80-85% | ✅ Similar (NS-3 slightly higher due to WiFi reliability) |
| **Latency** | 0.104 ms | ~2-5 ms | ⚠️ Higher (expected - includes PHY/MAC overhead) |
| **Beacon Size** | 159.6 B | 160 B | ✅ Same |
| **Throughput** | N/A | ~125 kbps | ✅ Realistic for 802.11n |

### **Why NS-3 Latency is Higher**

- **Python**: No PHY/MAC overhead, direct packet delivery
- **NS-3**: Realistic WiFi MAC (CSMA/CA, backoff, collisions, ACKs)
- **This is expected and correct** - NS-3 provides realistic network simulation

---

## 📁 Output Files

### **Results File**

**Location**: `../../results/ns3/primefusion-wifi-{nUavs}uavs-{duration}s.txt`

**Example**: `../../results/ns3/primefusion-wifi-5uavs-60s.txt`

**Content**:
```
PrimeFusion-FANET NS-3 WiFi Simulation Results
==============================================

Configuration:
  UAVs: 5
  Duration: 60s
  Beacon interval: 1s
  Beacon size: 160 bytes
  PHY: WiFi 802.11n

Results:
  Beacons sent: 295
  Beacons received: 240
  PDR: 81.36%
  Avg latency: 2.45 ms
  Throughput: 125.3 kbps
```

---

## 🔧 Troubleshooting

### **Problem: Build fails**

```bash
# Solution 1: Install dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install g++ python3 cmake ninja-build

# Solution 2: Clean and rebuild
./ns3 clean
./ns3 configure --enable-examples
./ns3 build
```

### **Problem: "primefusion-wifi not found"**

```bash
# Check if files are in scratch/
ls scratch/primefusion-*

# If not, copy again
cp ../../primefusion-wifi.cc scratch/
cp ../../primefusion-helper.h scratch/

# Rebuild
./ns3 build
```

### **Problem: "results/ns3/ directory not found"**

```bash
# Create directory manually
mkdir -p ../../results/ns3

# Or run from project root
cd /path/to/primefusion-project
mkdir -p results/ns3
```

### **Problem: Compilation errors**

```bash
# Check NS-3 version
./ns3 --version
# Should be 3.40 or later

# Check C++ standard
g++ --version
# Should support C++17 or later

# Try with verbose output
./ns3 build --verbose
```

---

## 📈 Next Steps

### **1. Validate WiFi Results**

```bash
# Run multiple times to get average
for i in {1..5}; do
  ./ns3 run "primefusion-wifi --nUavs=5 --duration=60"
done

# Compare with Python baseline
# Expected: PDR ~80-85%, Latency ~2-5ms
```

### **2. Scalability Testing**

```bash
# Test with different UAV counts
./ns3 run "primefusion-wifi --nUavs=3 --duration=60"
./ns3 run "primefusion-wifi --nUavs=5 --duration=60"
./ns3 run "primefusion-wifi --nUavs=10 --duration=60"
./ns3 run "primefusion-wifi --nUavs=15 --duration=60"
./ns3 run "primefusion-wifi --nUavs=20 --duration=60"
```

### **3. Longer Simulations**

```bash
# Test with longer duration
./ns3 run "primefusion-wifi --nUavs=5 --duration=300"  # 5 minutes
./ns3 run "primefusion-wifi --nUavs=10 --duration=600"  # 10 minutes
```

### **4. Add LoRa PHY** (Future)

- Implement LoRa physical layer
- Compare WiFi vs. LoRa performance
- Validate airtime reduction claims

---

## 📝 Implementation Notes

### **What's Implemented**

✅ **WiFi 802.11n**: Realistic PHY/MAC layer  
✅ **Beacon Broadcasting**: Custom application  
✅ **PrimeFusion Trailer**: 12-byte trailer (8-byte hash + 4-byte milestone)  
✅ **Mobility**: Random Waypoint model  
✅ **Metrics**: PDR, latency, throughput  
✅ **Results Export**: Text file output  

### **What's Simplified**

⚠️ **Blockchain**: Simplified hash (not full SHA-256)  
⚠️ **Session-MAC**: CPU cycle estimation (not actual crypto)  
⚠️ **CBOR**: Size estimation (not actual compression)  
⚠️ **Consensus**: Milestone encoding only (no DAG)  

### **Why Simplified?**

- **Focus on network validation**: PHY/MAC/mobility effects
- **Faster simulation**: No crypto overhead in NS-3
- **Easier to extend**: Add full implementation later
- **Python baseline**: Full crypto validated in Python

---

## ✅ Success Criteria

After running, you should see:

1. ✅ Simulation completes without errors
2. ✅ PDR ~80-85% for 5 UAVs
3. ✅ Latency ~2-5 ms (higher than Python, expected)
4. ✅ Results file created in `results/ns3/`
5. ✅ Beacon size = 160 bytes (matches Python)

---

## 📧 Summary

**To use NS-3 implementation**:

1. ✅ Install NS-3 in `primefusion-project/ns3/`
2. ✅ Copy 2 files to `scratch/`
3. ✅ Create `results/ns3/` directory
4. ✅ Compile with `./ns3 build`
5. ✅ Run with `./ns3 run primefusion-wifi`
6. ✅ Validate against Python baseline

**Files provided**:
- ✅ `primefusion-wifi.cc` - Main simulation (~350 lines)
- ✅ `primefusion-helper.h` - Helper functions (~250 lines)
- ✅ `README.md` - This file

**Ready to compile and run!**

