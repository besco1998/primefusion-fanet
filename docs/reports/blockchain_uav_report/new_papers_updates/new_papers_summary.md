## Summary of New Papers for Report Update

### 1. iBANDA: A Blockchain-Assisted Defense System (drones-09-00590-v2.pdf)
- **Authors:** Ajakwe et al.
- **Contribution:** Proposes iBANDA, a framework for dual-layer authentication of drones and their payloads in logistics.
- **Key Technologies:**
  - **AI:** YOLOv5s for visual object detection.
  - **Blockchain:** Snowball-based Proof-of-Stake (PoS) consensus.
  - **Architecture:** Edge-deployable Decentralized Application (DApp).
- **Key Findings:**
  - Achieves high precision (99.5%) and recall (100%) in visual detection.
  - Outperforms public testnets (Goerli, Sepolia) in latency and throughput.
  - Demonstrates resilience to Sybil and GPS spoofing attacks.
- **Relevance:** Highly relevant for the **Security and Authentication** sections. Provides a concrete example of a hybrid AI-blockchain system and a different PoS consensus variant (Snowball).

### 2. Lightweight Authentication with aSVC (drones-09-00654-v2.pdf)
- **Authors:** Jiao et al.
- **Contribution:** A lightweight and dynamic identity authentication scheme for UAV swarms.
- **Key Technologies:**
  - **Blockchain:** For distributed trust.
  - **Aggregatable Subvector Commitments (aSVC):** To compress identity states and reduce on-chain storage.
- **Key Findings:**
  - Reduces on-chain storage overhead to a constant level.
  - Optimizes computational complexity for batch authentication from linear to constant.
- **Relevance:** Directly addresses the challenge of blockchain overhead in resource-constrained UAVs. Highly relevant for the **Authentication**, **Methodology**, and **Limitations** sections. The aSVC technique is a key innovation to contrast with PrimeFusion's approach.

### 3. Performance of Private Blockchains (sensors-24-07813.pdf)
- **Authors:** Hossain et al.
- **Contribution:** Evaluates the performance of private blockchain architectures in UAV networks.
- **Key Technologies:**
  - **Blockchain:** Private blockchain (likely PBFT-like).
- **Metrics:** Throughput, latency, resource utilization.
- **Key Findings:**
  - Provides empirical data on the performance of private blockchains in UAV contexts.
  - Highlights the performance degradation as the number of nodes increases.
- **Relevance:** This is the same paper already in the bibliography. It provides crucial empirical data that supports the arguments in the **Problem Statement** and **Comparative Analysis** sections regarding the limitations of generic blockchain solutions.

### 4. Secure LoRa D2D Communication (sensors-25-05087.pdf)
- **Authors:** Khor et al.
- **Contribution:** A secure LoRa-based drone-to-drone (D2D) communication protocol for public Unmanned Traffic Management (UTM).
- **Key Technologies:**
  - **Communication:** LoRa for long-range, low-power communication.
  - **Blockchain:** Public blockchain for collision avoidance and UTM.
- **Relevance:** Introduces a different communication technology (LoRa) and a specific application (UTM). Relevant for the **Background** (UAV Communication Networks) and **Literature Review** sections.

### 5. Performance of HotStuff Consensus (drones-09-00334.pdf)
- **Authors:** Huang et al.
- **Contribution:** Analyzes the performance of the chained-HotStuff consensus algorithm in UAV networks.
- **Key Technologies:**
  - **Consensus:** Chained-HotStuff.
  - **Network Conditions:** Considers UAV communication conditions and CSMA/CA.
- **Key Findings:**
  - Provides analysis of a specific, modern consensus algorithm (HotStuff) in a UAV context.
- **Relevance:** Very important for the **Consensus Mechanisms** part of the **Literature Review** and for the **Comparative Analysis**, providing another specific consensus algorithm to compare against PrimeFusion's PoC.
