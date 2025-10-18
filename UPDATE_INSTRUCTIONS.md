# PrimeFusion-FANET Update & Testing Instructions

**Last Updated**: October 18, 2025  
**Version**: 1.0 (Core Implementation Complete)

---

## 📥 Step 1: Update Project Locally

### **Option A: Extract from Archive** (Recommended if starting fresh)

```bash
# Download the archive (primefusion-implementation.tar.gz)
# Extract to your local machine
cd ~/Downloads  # or wherever you downloaded it
tar -xzf primefusion-implementation.tar.gz

# This will create/update:
# primefusion-project/python/core/session_mac.py
# primefusion-project/python/core/blockchain.py
# primefusion-project/python/core/milestone.py
# primefusion-project/python/core/cbor_optimizer.py
# primefusion-project/python/core/beacon_integrated.py
# primefusion-project/python/tests/test_all_modules.py
# primefusion-project/CODE_REVIEW.md
# primefusion-project/IMPLEMENTATION_SUMMARY.md
```

### **Option B: Download Full Project** (If you want everything)

```bash
# Clone from GitHub
git clone https://github.com/besco1998/primefusion-fanet.git
cd primefusion-fanet

# The repository should already have all files
# If not, extract the archive on top of it
```

### **Option C: Manual File Copy** (If you already have the project)

```bash
# Navigate to your existing project
cd /path/to/primefusion-project

# Copy new files from archive
# (Extract archive first, then copy files)
cp /path/to/extracted/primefusion-project/python/core/session_mac.py python/core/
cp /path/to/extracted/primefusion-project/python/core/blockchain.py python/core/
cp /path/to/extracted/primefusion-project/python/core/milestone.py python/core/
cp /path/to/extracted/primefusion-project/python/core/beacon_integrated.py python/core/
cp /path/to/extracted/primefusion-project/python/core/cbor_optimizer.py python/core/
cp /path/to/extracted/primefusion-project/python/tests/test_all_modules.py python/tests/
cp /path/to/extracted/primefusion-project/CODE_REVIEW.md .
cp /path/to/extracted/primefusion-project/IMPLEMENTATION_SUMMARY.md .
```

---

## 🔧 Step 2: Install Dependencies

### **Check Python Version**

```bash
python3 --version
# Should be Python 3.11 or higher
```

### **Install Required Packages**

```bash
# Navigate to project directory
cd primefusion-project

# Install dependencies
pip3 install -r requirements.txt

# Or install individually
pip3 install cbor2>=5.7.0
pip3 install cryptography>=46.0.0
pip3 install pytest>=8.0.0
```

### **Verify Installation**

```bash
python3 -c "import cbor2; import cryptography; print('✓ Dependencies installed')"
```

---

## 🧪 Step 3: Run Tests

### **Option 1: Run Comprehensive Test Suite** (Recommended)

```bash
# Navigate to project root
cd primefusion-project

# Run all tests
python3 python/tests/test_all_modules.py
```

**Expected Output**:
```
============================================================
PRIMEFUSION-FANET COMPREHENSIVE TEST SUITE
============================================================
============================================================
TEST: Session-MAC Authentication
============================================================
✓ Signed and verified 100 blocks
✓ CPU reduction: 94.6% (target: >15%)
✓ Session-MAC: PASS

[... more tests ...]

============================================================
TEST SUMMARY
============================================================
✓ Session-MAC: PASS
✓ Blockchain: PASS
✓ Milestone: PASS
✓ CBOR: PASS
✓ Integrated Beacon: PASS
============================================================
TOTAL: 5/5 tests passed
============================================================
```

### **Option 2: Test Individual Modules**

```bash
# Test Session-MAC
python3 python/core/session_mac.py

# Test Blockchain
python3 python/core/blockchain.py

# Test Milestone Pig-Backing
python3 python/core/milestone.py

# Test CBOR Compression
python3 python/core/cbor_optimizer.py

# Test Integrated Beacon Manager
python3 python/core/beacon_integrated.py
```

### **Option 3: Use pytest** (If installed)

```bash
# Run with pytest for detailed output
pytest python/tests/test_all_modules.py -v
```

---

## 📤 Step 4: Update GitHub Repository

### **Method 1: Command Line** (Recommended)

```bash
# Navigate to project directory
cd primefusion-project

# Check current status
git status

# Add all new files
git add python/core/session_mac.py
git add python/core/blockchain.py
git add python/core/milestone.py
git add python/core/beacon_integrated.py
git add python/core/cbor_optimizer.py
git add python/tests/test_all_modules.py
git add CODE_REVIEW.md
git add IMPLEMENTATION_SUMMARY.md
git add UPDATE_INSTRUCTIONS.md

# Or add all at once
git add .

# Commit changes
git commit -m "Core implementation complete: Session-MAC, Blockchain, Milestone, Integrated Beacon

- Implemented Session-MAC authentication (94.6% CPU reduction)
- Implemented linear blockchain with Session-MAC integration
- Implemented milestone pig-backing (12-byte trailer)
- Enhanced CBOR compression with blockchain keys
- Integrated beacon manager with all components
- Comprehensive test suite (5/5 tests passed)
- All performance targets met or exceeded

Test Results:
- Session-MAC: 94.6% CPU reduction (target: >15%)
- Blockchain: 0.011ms latency (target: <1ms)
- Milestone: 12 bytes, 0.005ms (target: ≤12B, <1ms)
- CBOR: 0.559 ratio (target: <0.70)
- Integrated: 0.114ms total (target: <5ms)"

# Push to GitHub
git push origin main
```

### **Method 2: GitHub Desktop** (If you use it)

1. Open GitHub Desktop
2. Select `primefusion-fanet` repository
3. Review changes in the left panel
4. Add commit message (use the message from Method 1)
5. Click "Commit to main"
6. Click "Push origin"

### **Method 3: GitHub Web Interface** (Upload files)

1. Go to https://github.com/besco1998/primefusion-fanet
2. Navigate to the appropriate directory
3. Click "Add file" → "Upload files"
4. Drag and drop the new files
5. Add commit message
6. Click "Commit changes"

---

## ✅ Step 5: Verify Everything Works

### **1. Verify Local Tests**

```bash
# Run comprehensive tests
python3 python/tests/test_all_modules.py

# Should see: TOTAL: 5/5 tests passed
```

### **2. Verify GitHub Upload**

```bash
# Check GitHub repository
# Visit: https://github.com/besco1998/primefusion-fanet

# Verify these files exist:
# - python/core/session_mac.py
# - python/core/blockchain.py
# - python/core/milestone.py
# - python/core/beacon_integrated.py
# - python/tests/test_all_modules.py
# - CODE_REVIEW.md
# - IMPLEMENTATION_SUMMARY.md
```

### **3. Test from Fresh Clone** (Optional but recommended)

```bash
# Clone to a new directory
cd ~/temp
git clone https://github.com/besco1998/primefusion-fanet.git
cd primefusion-fanet

# Install dependencies
pip3 install -r requirements.txt

# Run tests
python3 python/tests/test_all_modules.py

# Should pass all tests
```

---

## 🔍 Troubleshooting

### **Problem: Import Errors**

```bash
# Error: ModuleNotFoundError: No module named 'cbor2'
# Solution: Install dependencies
pip3 install cbor2 cryptography

# Error: ModuleNotFoundError: No module named 'session_mac'
# Solution: Run from project root
cd primefusion-project
python3 python/tests/test_all_modules.py
```

### **Problem: Git Push Fails**

```bash
# Error: Authentication failed
# Solution 1: Use GitHub CLI
gh auth login

# Solution 2: Use personal access token
# 1. Go to GitHub Settings → Developer settings → Personal access tokens
# 2. Generate new token with 'repo' scope
# 3. Use token as password when pushing
```

### **Problem: Tests Fail**

```bash
# Check Python version
python3 --version  # Should be 3.11+

# Check dependencies
pip3 list | grep cbor2
pip3 list | grep cryptography

# Reinstall dependencies
pip3 install --upgrade cbor2 cryptography

# Run individual module tests to isolate issue
python3 python/core/session_mac.py
```

---

## 📊 Expected Test Results

### **All Tests Should Pass**

```
✓ Session-MAC: PASS
  - CPU reduction: 94.6% (target: >15%)
  - 100 blocks signed and verified

✓ Blockchain: PASS
  - Add latency: 0.011ms (target: <1ms)
  - Chain validation: 100%

✓ Milestone: PASS
  - Trailer size: 12 bytes (target: ≤12)
  - Latency: 0.005ms (target: <1ms)

✓ CBOR: PASS
  - Compression ratio: 0.559 (target: <0.70)
  - Lossless compression/decompression

✓ Integrated Beacon: PASS
  - Total latency: 0.114ms (target: <5ms)
  - Trailer size: 12 bytes (target: ≤12)
```

### **If Any Test Fails**

1. Check the error message
2. Verify dependencies are installed
3. Check Python version (3.11+)
4. Run individual module test to isolate
5. Check file paths are correct
6. Verify you're running from project root

---

## 📁 File Checklist

After updating, verify these files exist:

### **New Core Modules** (Must have)
- [ ] `python/core/session_mac.py`
- [ ] `python/core/blockchain.py`
- [ ] `python/core/milestone.py`
- [ ] `python/core/beacon_integrated.py`

### **Enhanced Modules** (Must have)
- [ ] `python/core/cbor_optimizer.py` (with blockchain keys)

### **Tests** (Must have)
- [ ] `python/tests/test_all_modules.py`

### **Documentation** (Should have)
- [ ] `CODE_REVIEW.md`
- [ ] `IMPLEMENTATION_SUMMARY.md`
- [ ] `UPDATE_INSTRUCTIONS.md` (this file)

### **Existing Files** (Should have)
- [ ] `README.md`
- [ ] `requirements.txt`
- [ ] `.gitignore`
- [ ] `python/core/crypto_utils.py`
- [ ] `python/core/consensus.py`
- [ ] `python/core/beacon.py`

---

## 🚀 Quick Start Commands

```bash
# Complete workflow (copy-paste friendly)

# 1. Navigate to project
cd primefusion-project

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Run tests
python3 python/tests/test_all_modules.py

# 4. If all tests pass, update GitHub
git add .
git commit -m "Core implementation complete (5/5 tests passed)"
git push origin main

# 5. Verify on GitHub
# Visit: https://github.com/besco1998/primefusion-fanet
```

---

## 📞 Need Help?

### **Check These First**
1. Python version: `python3 --version` (should be 3.11+)
2. Dependencies: `pip3 list | grep -E "(cbor|crypto)"`
3. File paths: `ls python/core/session_mac.py` (should exist)
4. Git status: `git status` (check for uncommitted changes)

### **Common Issues**
- **Import errors**: Install dependencies with `pip3 install -r requirements.txt`
- **Test failures**: Check Python version and dependencies
- **Git push fails**: Authenticate with `gh auth login` or use personal access token
- **File not found**: Verify you're in the correct directory

---

## ✅ Success Criteria

You've successfully updated when:

1. ✅ All dependencies installed
2. ✅ All 5 tests pass (5/5)
3. ✅ Files committed to Git
4. ✅ Changes pushed to GitHub
5. ✅ GitHub repository shows new files

---

**Ready to proceed to Phase 2 (Python Simulation) after successful update!**

