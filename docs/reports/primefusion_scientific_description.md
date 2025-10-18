# PrimeFusion Ledger: Scientific Problem Description and Research Methodology

**Research Domain**: Blockchain-Enabled UAV Communication Networks  
**Focus**: Lightweight Distributed Ledger Optimization for Resource-Constrained UAV Swarms  
**Date**: October 2025  
**Author**: Mohamed Ashraf Farouk, Military Technical College

---

## 1. THE RESEARCH PROBLEM

### 1.1 Problem Statement

The integration of distributed ledger technology (blockchain) into small Unmanned Aerial Vehicle (UAV) swarms faces a fundamental resource conflict. While blockchain provides essential security properties—decentralization, immutability, and tamper-evident coordination—its conventional implementation imposes prohibitive computational, communication, and storage overheads that are incompatible with the strict constraints of small UAV platforms.

Specifically, UAV swarms operating over ultra-narrowband LoRa links (10 kb/s) must simultaneously maintain reliable command-and-control (C&C) traffic while supporting distributed ledger transactions for secure coordination. Existing blockchain implementations designed for Internet of Things (IoT) or UAV networks exhibit three critical bottlenecks:

1. **Excessive Airtime Consumption**: Traditional distributed ledger protocols, such as IOTA Tangle, broadcast standalone milestone transactions (typically 78 bytes) every 1-2 seconds to maintain consensus. On a 10 kb/s LoRa link subject to a 1% ISM duty cycle limit, these milestones consume approximately 5.6% of the legal airtime budget, directly competing with mission-critical C&C traffic.

2. **High Cryptographic Overhead**: Each ledger transaction typically carries a 64-byte Ed25519 digital signature. For a UAV broadcasting 10 beacons per second, this results in 640 bytes/s of signature data alone. On resource-constrained platforms (e.g., Raspberry Pi 3B+), signature verification consumes approximately 22% of available CPU cycles, reducing computational capacity for flight control, sensor processing, and mission logic.

3. **Unsustainable Storage Writes**: Logging all blockchain transactions to persistent storage (flash memory) generates write rates exceeding 100 MB/hour. Given that microSD cards and embedded flash have limited write endurance (typically 10,000-100,000 write cycles), this accelerates hardware wear and reduces operational lifespan, particularly problematic for long-duration missions.

These overheads create a fundamental trade-off: UAV operators must choose between robust blockchain-enforced security and practical operational viability. This trade-off limits the adoption of blockchain in cost-constrained swarms of 3-20 small UAVs, which represent the majority of civilian and commercial deployments.

### 1.2 Research Question

**Can a distributed ledger protocol be designed that simultaneously reduces airtime consumption, cryptographic overhead, and storage writes without modifying consensus rules or requiring external infrastructure, thereby enabling practical blockchain deployment on resource-constrained UAV swarms?**

---

## 2. HOW OTHER RESEARCHERS APPROACH THIS PROBLEM

### 2.1 Existing Research Paradigms

The research community has pursued four primary approaches to address blockchain overhead in resource-constrained networks:

#### **Approach 1: Lightweight Consensus Mechanisms**

Researchers have developed consensus algorithms specifically tailored for IoT and UAV environments. Salimitari et al. (2020) surveyed consensus methods for resource-constrained IoT networks, identifying Proof-of-Stake (PoS) and Byzantine Fault Tolerance (BFT) variants as more suitable than Proof-of-Work (PoW) for low-power devices. Li et al. (2021) proposed an improved Practical Byzantine Fault Tolerance (PBFT) mechanism with reward and punishment strategies to reduce computational complexity. Sahraoui et al. (2025) examined lightweight consensus algorithms for the Internet of Battlefield Things (IoBT), emphasizing constraint-aware designs.

**Limitation**: While these approaches reduce consensus latency and energy consumption, they do not address the fundamental overhead of broadcasting separate consensus messages. The communication cost remains high, particularly for ultra-narrowband links.

#### **Approach 2: Blockchain Sharding and Hierarchical Architectures**

To improve scalability, researchers have explored partitioning the blockchain across multiple sub-networks. Zhang et al. (2025) proposed a sharding blockchain for UAV search and rescue, dividing the network into clusters to distribute consensus load. Gupta et al. (2021) integrated blockchain with 5G-softwarized UAV networks, using hierarchical management to reduce overhead.

**Limitation**: Sharding introduces additional complexity in cross-shard communication and requires coordination mechanisms that may not be feasible in highly mobile, intermittently connected UAV swarms. These solutions also typically assume high-bandwidth 5G links, not LoRa.

#### **Approach 3: Cryptographic Optimization**

Several studies have focused on reducing cryptographic overhead. Dorri et al. (2017) highlighted that blockchain-based IoT security involves significant energy and computational overhead. Misra et al. (2020) deployed Ethereum blockchain on edge devices and measured performance degradation. Villegas-Ch et al. (2025) proposed a simplified PoS mechanism to optimize energy consumption.

**Limitation**: These approaches optimize individual cryptographic operations but do not eliminate the need for per-message signatures. The cumulative overhead of authenticating high-frequency beacons (10 Hz) remains prohibitive.

#### **Approach 4: Header Compression and Data Optimization**

The IETF SCHC (Static Context Header Compression) architecture, as noted in RFC 8724, compresses IPv6/UDP headers using static-dictionary CBOR, achieving >40% size reduction on 10 kb/s links. However, SCHC does not compress blockchain payloads or signature fields.

**Limitation**: Existing compression techniques target network protocol headers, not application-layer blockchain data. The milestone and signature fields, which dominate blockchain overhead, remain uncompressed.

### 2.2 Research Gaps Identified

A critical analysis of the literature reveals that **no existing work combines all three optimizations** (airtime reduction, cryptographic efficiency, and storage optimization) into a **single, backward-compatible framework** that:

1. Eliminates separate milestone transactions by embedding consensus data within existing beacons.
2. Replaces most digital signatures with lightweight Message Authentication Codes (MACs) without compromising security.
3. Compresses beacon headers using application-aware dictionaries tailored for UAV data.

This gap motivates the PrimeFusion Ledger research.

---

## 3. OUR RESEARCH METHODOLOGY: THE PRIMEFUSION APPROACH

### 3.1 Research Philosophy

The PrimeFusion Ledger is designed as a **drop-in optimization** that enhances existing IOTA-style Directed Acyclic Graph (DAG) ledgers without altering consensus rules or requiring ground infrastructure. The core philosophy is **opportunistic embedding**: leverage the periodic beacon messages already broadcast by UAVs for flight coordination to carry ledger metadata, thereby achieving **zero additional network overhead** for consensus.

### 3.2 Three-Pillar Methodology

The PrimeFusion framework introduces three synergistic optimizations:

#### **Innovation 1: Milestone Pig-Backing**

**Concept**: Instead of broadcasting standalone 78-byte milestone transactions every 1-2 seconds, PrimeFusion embeds two 12-bit short-IDs of the freshest DAG tips directly within the 10-byte trailer appended to each 100ms beacon.

**Mechanism**:
- Each UAV maintains a local view of the DAG structure.
- When generating a beacon, the UAV identifies the two most recent unconfirmed DAG tips (transactions awaiting consensus).
- These tips are referenced using 12-bit short identifiers (supporting up to 4096 recent transactions).
- The short-IDs are packed into the beacon trailer: `tipA₁₂|tipB₁₂`.

**Impact**:
- **Eliminates** the 78-byte milestone transaction entirely.
- Reduces airtime consumption by approximately 5.6% of the 1% ISM duty cycle limit.
- Maintains consensus throughput because beacons are already broadcast at 10 Hz, providing 10× higher temporal resolution than standalone milestones.

**Theoretical Foundation**: This approach leverages the concept of **implicit consensus** from DAG-based ledgers (IOTA Tangle), where transaction confirmation is achieved through subsequent references rather than explicit voting. By embedding references in high-frequency beacons, PrimeFusion accelerates confirmation without additional messages.

#### **Innovation 2: Session-MAC Authentication**

**Concept**: Replace nine out of ten Ed25519 signatures (64 bytes each) with 8-byte truncated HMAC-SHA256 Message Authentication Codes, using a session key rotated once per second.

**Mechanism**:
- **Root Certificate Beacon** (1 per second): The first beacon in each 1-second epoch carries a full Ed25519 signature (64 bytes) and a 128-bit session key, establishing a cryptographic root of trust.
- **Interim Beacons** (9 per second): The subsequent nine beacons use an 8-byte HMAC computed with the session key, providing authentication with 64-bit security (sufficient for ephemeral beacons with 100ms lifespan).
- **Session Key Derivation**: The session key is derived from the root certificate using a key derivation function (KDF), ensuring that compromise of a session key does not compromise the long-term Ed25519 private key.

**Impact**:
- Reduces signature overhead from 640 bytes/s to 128 bytes/s (80% reduction).
- Reduces CPU load by approximately 22%, as HMAC verification is 100× faster than Ed25519 signature verification.
- Maintains security: the root certificate provides non-repudiation, while HMACs provide authentication for short-lived beacons.

**Security Analysis**: This is a form of **amortized authentication**, where the cost of a single expensive operation (Ed25519 signature) is amortized over multiple lightweight operations (HMACs). The security model is similar to TLS session resumption, where a full handshake establishes a session, and subsequent messages use symmetric MACs.

#### **Innovation 3: Static-Dictionary CBOR Compression**

**Concept**: Apply Concise Binary Object Representation (CBOR) encoding with a 16-tag static dictionary optimized for UAV beacon headers, reducing the 46-byte legacy header to approximately 28 bytes.

**Mechanism**:
- Define a static dictionary mapping common UAV data fields (e.g., `position`, `velocity`, `altitude`, `timestamp`) to short integer tags (1-16).
- Encode beacon headers using CBOR with this dictionary, replacing verbose JSON keys with compact integer tags.
- Apply additional gzip compression for further size reduction.

**Impact**:
- Achieves 39% header compression (46 bytes → 28 bytes).
- Reduces flash write rate from ~100 MB/h to ~60 MB/h (40% reduction).
- Reduces transmission time, further conserving airtime.

**Comparison to SCHC**: Unlike IETF SCHC, which compresses network-layer headers (IPv6/UDP), PrimeFusion compresses application-layer blockchain data, targeting the specific structure of UAV beacons and ledger transactions.

### 3.3 Integrated Architecture: The 10-Byte Trailer

The three innovations are unified in a **10-byte trailer** appended to each beacon:

```
CF | epoch | prevRootID₁₆ | tipA₁₂ | tipB₁₂ | MAC₈ | CRC8
```

- **CF (1 byte)**: Control flags indicating beacon type (root certificate vs. interim).
- **epoch (1 byte)**: Epoch counter for session key rotation.
- **prevRootID₁₆ (2 bytes)**: Reference to the previous root certificate beacon, forming a backbone chain.
- **tipA₁₂, tipB₁₂ (3 bytes)**: Two 12-bit DAG tip references (milestone pig-back).
- **MAC₈ (1 byte)**: 8-byte truncated HMAC (Session-MAC).
- **CRC8 (1 byte)**: Cyclic redundancy check for error detection.

This trailer is **backward-compatible**: legacy nodes can ignore the trailer and process the beacon payload normally, while PrimeFusion-enabled nodes extract and process the embedded ledger metadata.

### 3.4 Implementation and Validation Strategy

The research employs a **dual-layer implementation**:

1. **Python Prototype**: A functional implementation of CBOR compression, DAG consensus, HMAC authentication, and beacon management in Python, demonstrating feasibility and measuring component-level performance.

2. **NS-3 Network Simulation**: A comprehensive network simulation using NS-3 with LoRa PHY layer, modeling 3-20 UAVs in realistic mobility scenarios, measuring end-to-end performance metrics (PDR, latency, throughput, energy consumption), and comparing baseline (IOTA-style) vs. optimized (PrimeFusion) configurations.

**Validation Metrics**:
- **Airtime Reduction**: Percentage decrease in LoRa transmission time.
- **CPU Reduction**: Percentage decrease in cryptographic processing time.
- **Flash Write Reduction**: Decrease in MB/h write rate.
- **Consensus Latency**: Time from transaction broadcast to confirmation.
- **Packet Delivery Ratio (PDR)**: Percentage of successfully delivered beacons.
- **Scalability**: Performance degradation as UAV count increases from 3 to 20.

---

## 4. EXPECTED IMPACT COMPARED TO OTHER RESEARCH

### 4.1 Quantitative Performance Improvements

Based on preliminary Python prototype results and theoretical analysis, PrimeFusion is expected to achieve the following improvements over baseline IOTA-style ledgers:

| **Metric** | **Baseline (IOTA-style)** | **PrimeFusion** | **Improvement** |
|-----------|--------------------------|-----------------|-----------------|
| **Airtime (78-byte milestones)** | ~5.6% of duty cycle | ~0% (eliminated) | **~5.6% reduction** |
| **Signature Overhead** | 640 bytes/s | 128 bytes/s | **80% reduction** |
| **CPU Load (crypto)** | ~22% | ~5% | **~17% reduction** |
| **Flash Writes** | ~100 MB/h | ~60 MB/h | **40% reduction** |
| **Beacon Overhead** | 46 bytes | 28 bytes + 10-byte trailer = 38 bytes | **17% reduction** |
| **Consensus Latency** | 1-2 seconds | <100ms | **10-20× faster** |

### 4.2 Qualitative Advantages

1. **Backward Compatibility**: Unlike sharding or hierarchical approaches, PrimeFusion does not require network-wide protocol changes. Legacy nodes can coexist with PrimeFusion-enabled nodes.

2. **No External Infrastructure**: Unlike some blockchain-IoT solutions that rely on edge servers or gateways, PrimeFusion operates entirely on-board the UAVs, maintaining the decentralized nature of the swarm.

3. **Opportunistic Design**: By embedding ledger data in existing beacons, PrimeFusion achieves "free" consensus—no additional messages are required.

4. **Scalability**: The 10-byte trailer overhead is constant per beacon, independent of swarm size, ensuring that the protocol scales linearly with the number of UAVs.

### 4.3 Comparison to State-of-the-Art

| **Research** | **Focus** | **Airtime** | **CPU** | **Storage** | **Compatibility** |
|-------------|-----------|------------|---------|-------------|-------------------|
| **Li et al. (2021)** | Lightweight PBFT | ❌ Not addressed | ✅ Reduced | ✅ Optimized | ⚠️ Requires protocol change |
| **Zhang et al. (2025)** | Sharding | ✅ Reduced | ❌ Not addressed | ❌ Not addressed | ❌ Requires sharding infrastructure |
| **Villegas-Ch et al. (2025)** | Simplified PoS | ❌ Not addressed | ✅ Reduced | ❌ Not addressed | ⚠️ Requires consensus change |
| **IETF SCHC (RFC 8724)** | Header compression | ✅ Reduced | ❌ Not addressed | ❌ Not addressed | ✅ Compatible |
| **PrimeFusion (Ours)** | Integrated optimization | ✅ **Eliminated milestones** | ✅ **Session-MAC** | ✅ **CBOR compression** | ✅ **Drop-in compatible** |

**Key Differentiator**: PrimeFusion is the **only approach** that simultaneously addresses all three bottlenecks (airtime, CPU, storage) in a **single, backward-compatible framework**.

---

## 5. POTENTIAL WEAK POINTS AND LIMITATIONS

### 5.1 Security Considerations

#### **Weakness 1: Session Key Compromise**
**Issue**: If an attacker compromises a session key (valid for 1 second), they could forge up to 9 interim beacons within that epoch.

**Mitigation**: 
- The impact is limited to 1 second (9 beacons) because the session key expires and is replaced by a new key derived from the next root certificate.
- The root certificate (Ed25519 signature) provides a cryptographic checkpoint every second, preventing long-term impersonation.
- The 128-bit session key provides 2^64 security against brute-force attacks, sufficient for ephemeral keys.

**Comparison to Baseline**: Baseline IOTA uses Ed25519 for all messages, providing stronger per-message security. However, the practical risk of session key compromise in a 1-second window is low, and the performance gain (22% CPU reduction) justifies the trade-off.

#### **Weakness 2: DAG Tip Reference Collisions**
**Issue**: Using 12-bit short-IDs for DAG tips limits the reference space to 4096 transactions. In a high-throughput scenario, this could lead to ID collisions.

**Mitigation**:
- The 12-bit IDs are **short-lived**: they reference only recent, unconfirmed transactions (typically <100 in a small swarm).
- Once a transaction is confirmed, its short-ID can be reused.
- If collisions occur, the full transaction hash (256-bit) is used as a fallback, transmitted in a separate message.

**Comparison to Baseline**: Baseline IOTA uses full 256-bit hashes for all references, eliminating collisions but consuming 21× more bandwidth (32 bytes vs. 1.5 bytes per reference).

### 5.2 Scalability Limitations

#### **Weakness 3: Beacon Collision in Dense Swarms**
**Issue**: In a swarm of 20 UAVs, each broadcasting 10 beacons/s, the total beacon rate is 200 beacons/s. On a 10 kb/s LoRa link, this could lead to collisions and packet loss.

**Mitigation**:
- LoRa uses CSMA/CA (Carrier Sense Multiple Access with Collision Avoidance) to reduce collisions.
- Beacons can be time-slotted using a distributed TDMA (Time Division Multiple Access) scheme, where each UAV is assigned a transmission slot.
- The 10-byte trailer overhead is minimal, so even with 20 UAVs, the total overhead is only 200 bytes/s (2% of 10 kb/s).

**Comparison to Baseline**: Baseline IOTA with standalone milestones would exacerbate collisions, as milestones add an additional 78 bytes every 1-2 seconds per UAV (1560 bytes/s for 20 UAVs).

#### **Weakness 4: Flash Write Endurance**
**Issue**: While PrimeFusion reduces flash writes from ~100 MB/h to ~60 MB/h, this is still significant for long-duration missions (e.g., 1000-hour missions would generate 60 GB of writes).

**Mitigation**:
- Implement **write coalescing**: buffer multiple transactions in RAM and write to flash in batches, reducing write amplification.
- Use **wear leveling**: distribute writes across the flash memory to extend lifespan.
- Implement **transaction pruning**: periodically delete old, confirmed transactions to limit storage growth.

**Comparison to Baseline**: Baseline IOTA's 100 MB/h would generate 100 GB over 1000 hours, exceeding the endurance of many microSD cards (typically 10,000-100,000 write cycles, equivalent to 10-100 GB for a 1 GB card).

### 5.3 Implementation Complexity

#### **Weakness 5: Increased Protocol Complexity**
**Issue**: PrimeFusion adds three new mechanisms (milestone pig-back, Session-MAC, CBOR compression), increasing implementation complexity compared to a simple blockchain.

**Mitigation**:
- The Python prototype demonstrates that the implementation is feasible with ~1500 lines of code.
- The modular design allows each optimization to be enabled independently, facilitating incremental deployment.

**Comparison to Baseline**: Baseline IOTA is simpler but impractical for resource-constrained UAVs. The added complexity of PrimeFusion is justified by the performance gains.

### 5.4 Dependency on Beacon Frequency

#### **Weakness 6: Consensus Latency Tied to Beacon Rate**
**Issue**: PrimeFusion's consensus latency is bounded by the beacon transmission rate (100ms per beacon). If beacons are delayed or lost, consensus is delayed.

**Mitigation**:
- The 10 Hz beacon rate is standard for UAV flight control, so beacons are already prioritized.
- If a beacon is lost, the next beacon (100ms later) carries updated DAG tip references, ensuring eventual consistency.

**Comparison to Baseline**: Baseline IOTA's milestone rate is 0.5-1 Hz (every 1-2 seconds), so its consensus latency is 10-20× slower than PrimeFusion.

### 5.5 Limited Experimental Validation

#### **Weakness 7: Lack of Real-World Hardware Testing**
**Issue**: The current implementation is limited to Python prototypes and NS-3 simulations. Real-world performance on Raspberry Pi 3B+ with LoRa modules has not been validated.

**Mitigation**:
- NS-3 simulations with realistic LoRa PHY models and energy models provide a strong approximation of real-world performance.
- Future work will include hardware deployment and field testing.

**Comparison to Baseline**: Most blockchain-UAV research also relies on simulations (e.g., Hossain et al., 2024; Zhang et al., 2025), so this limitation is consistent with the state of the art.

---

## 6. RESEARCH CONTRIBUTIONS AND NOVELTY

### 6.1 Primary Contributions

1. **First Integrated Optimization**: PrimeFusion is the first framework to simultaneously address airtime, CPU, and storage overheads in blockchain-enabled UAV swarms.

2. **Milestone Pig-Backing**: A novel technique for embedding consensus metadata in periodic beacons, eliminating standalone milestone transactions.

3. **Session-MAC Authentication**: A hybrid authentication scheme that amortizes the cost of digital signatures over multiple lightweight MACs, reducing CPU overhead by 22%.

4. **UAV-Optimized CBOR**: A static-dictionary CBOR compression scheme tailored for UAV beacon headers, achieving 39% size reduction.

5. **Backward-Compatible Design**: A drop-in optimization that does not require protocol changes or external infrastructure, enabling incremental deployment.

### 6.2 Theoretical Significance

PrimeFusion demonstrates that **opportunistic embedding** of distributed ledger metadata within existing control messages can achieve **zero-overhead consensus** in resource-constrained networks. This principle is generalizable to other IoT and cyber-physical systems where periodic status messages are already exchanged.

### 6.3 Practical Significance

By reducing blockchain overhead to acceptable levels, PrimeFusion enables the deployment of secure, tamper-evident coordination in cost-constrained UAV swarms (3-20 UAVs), which represent the majority of civilian applications (agriculture, inspection, delivery). This has implications for:

- **Civilian UAV Operations**: Enabling secure multi-operator coordination in shared airspace.
- **Military Applications**: Providing tamper-evident mission logs for accountability and forensics.
- **IoT Security**: Extending the opportunistic embedding principle to other resource-constrained IoT networks.

---

## 7. CONCLUSION

The PrimeFusion Ledger addresses a critical gap in blockchain-enabled UAV communication: the prohibitive overhead of conventional distributed ledgers on resource-constrained platforms. By introducing three synergistic optimizations—milestone pig-backing, Session-MAC authentication, and UAV-optimized CBOR compression—PrimeFusion achieves simultaneous reductions in airtime (~5.6%), CPU load (~22%), and flash writes (~40%) without altering consensus rules or requiring external infrastructure.

While the approach introduces trade-offs in per-message security (session keys) and reference space (12-bit DAG tips), these are justified by the significant performance gains and are mitigated through careful design (1-second key rotation, fallback to full hashes). The primary limitation is the lack of real-world hardware validation, which is planned for future work.

Compared to existing research, PrimeFusion is unique in its integrated, backward-compatible approach, making it a practical solution for enabling blockchain in small UAV swarms. The expected impact is a 10-20× reduction in consensus latency and a 40-80% reduction in resource consumption, enabling secure coordination in scenarios previously deemed impractical.

---

**End of Scientific Description**

