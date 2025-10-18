/*
 * PrimeFusion-FANET Helper
 * ========================
 * 
 * Header-only helper for PrimeFusion operations in NS-3.
 * 
 * Features:
 * - Blockchain hash generation
 * - Milestone encoding (12-bit)
 * - Beacon trailer creation (12 bytes)
 * - Session-MAC overhead calculation
 * 
 * Author: PrimeFusion-FANET Team
 * Date: October 2025
 * Version: 1.2 (Use NS-3 built-in TimestampTag)
 */

#ifndef PRIMEFUSION_HELPER_H
#define PRIMEFUSION_HELPER_H

#include "ns3/core-module.h"
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>
#include <cstring>

using namespace ns3;

/**
 * PrimeFusion Helper Class
 */
class PrimeFusionHelper
{
public:
    PrimeFusionHelper();
    ~PrimeFusionHelper();
    
    /**
     * Generate blockchain hash (8 bytes, 16 hex chars)
     * Simplified version - uses block number as seed
     */
    std::string GenerateBlockchainHash(uint32_t blockNumber);
    
    /**
     * Encode 3 milestone indices into 12 bits
     * Format: [tip1:4][tip2:4][tip3:4][padding:4]
     * Returns: 16-bit value (12 bits used + 4 bits padding)
     */
    uint16_t EncodeMilestones(const std::vector<uint8_t>& milestones);
    
    /**
     * Decode 12-bit milestone data back to 3 indices
     */
    std::vector<uint8_t> DecodeMilestones(uint16_t encoded);
    
    /**
     * Create 12-byte beacon trailer
     * Format: [blockchain_hash:8][milestone_data:2][padding:2]
     */
    std::vector<uint8_t> CreateBeaconTrailer(const std::string& blockHash, uint16_t milestones);
    
    /**
     * Parse 12-byte beacon trailer
     */
    void ParseBeaconTrailer(const std::vector<uint8_t>& trailer, 
                           std::string& blockHash, 
                           std::vector<uint8_t>& milestones);
    
    /**
     * Calculate Session-MAC CPU overhead reduction
     * Returns: CPU cycles saved (%)
     */
    double CalculateSessionMACOverhead(uint32_t blockNumber);
    
    /**
     * Estimate CBOR compression ratio
     * Returns: Compression ratio (0.0-1.0)
     */
    double EstimateCompressionRatio();

private:
    // Simple hash function (for simulation only)
    std::string SimpleHash(const std::string& input);
    
    // Session-MAC constants
    static const uint32_t ROOT_CERT_INTERVAL = 100;
    static const uint32_t ED25519_CYCLES = 273000;
    static const uint32_t HMAC_CYCLES = 12000;
};

PrimeFusionHelper::PrimeFusionHelper()
{
}

PrimeFusionHelper::~PrimeFusionHelper()
{
}

std::string
PrimeFusionHelper::SimpleHash(const std::string& input)
{
    // Simple hash for simulation (not cryptographically secure)
    // In real implementation, use SHA-256
    uint32_t hash = 0;
    for (char c : input)
    {
        hash = hash * 31 + static_cast<uint32_t>(c);
    }
    
    std::stringstream ss;
    ss << std::hex << std::setfill('0') << std::setw(16) << hash;
    return ss.str();
}

std::string
PrimeFusionHelper::GenerateBlockchainHash(uint32_t blockNumber)
{
    // Generate deterministic hash based on block number
    std::stringstream ss;
    ss << "block_" << blockNumber << "_data";
    return SimpleHash(ss.str());
}

uint16_t
PrimeFusionHelper::EncodeMilestones(const std::vector<uint8_t>& milestones)
{
    // Ensure we have exactly 3 milestones
    uint8_t tip1 = (milestones.size() > 0) ? (milestones[0] & 0x0F) : 0;
    uint8_t tip2 = (milestones.size() > 1) ? (milestones[1] & 0x0F) : 0;
    uint8_t tip3 = (milestones.size() > 2) ? (milestones[2] & 0x0F) : 0;
    
    // Pack into 16 bits: [tip1:4][tip2:4][tip3:4][padding:4]
    uint16_t encoded = (static_cast<uint16_t>(tip1) << 12) |
                       (static_cast<uint16_t>(tip2) << 8) |
                       (static_cast<uint16_t>(tip3) << 4);
    
    return encoded;
}

std::vector<uint8_t>
PrimeFusionHelper::DecodeMilestones(uint16_t encoded)
{
    std::vector<uint8_t> milestones;
    
    // Extract 3 × 4-bit values
    milestones.push_back((encoded >> 12) & 0x0F);
    milestones.push_back((encoded >> 8) & 0x0F);
    milestones.push_back((encoded >> 4) & 0x0F);
    
    return milestones;
}

std::vector<uint8_t>
PrimeFusionHelper::CreateBeaconTrailer(const std::string& blockHash, uint16_t milestones)
{
    std::vector<uint8_t> trailer;
    
    // Add blockchain hash (8 bytes from 16 hex chars)
    for (size_t i = 0; i < 16 && i < blockHash.length(); i += 2)
    {
        std::string byteString = blockHash.substr(i, 2);
        uint8_t byte = static_cast<uint8_t>(std::stoul(byteString, nullptr, 16));
        trailer.push_back(byte);
    }
    
    // Pad to 8 bytes if needed
    while (trailer.size() < 8)
    {
        trailer.push_back(0);
    }
    
    // Add milestone data (2 bytes)
    trailer.push_back((milestones >> 8) & 0xFF);
    trailer.push_back(milestones & 0xFF);
    
    // Add padding (2 bytes)
    trailer.push_back(0);
    trailer.push_back(0);
    
    return trailer;
}

void
PrimeFusionHelper::ParseBeaconTrailer(const std::vector<uint8_t>& trailer,
                                      std::string& blockHash,
                                      std::vector<uint8_t>& milestones)
{
    if (trailer.size() < 12)
    {
        return;
    }
    
    // Extract blockchain hash (8 bytes)
    std::stringstream ss;
    for (size_t i = 0; i < 8; ++i)
    {
        ss << std::hex << std::setfill('0') << std::setw(2) 
           << static_cast<int>(trailer[i]);
    }
    blockHash = ss.str();
    
    // Extract milestone data (2 bytes)
    uint16_t encoded = (static_cast<uint16_t>(trailer[8]) << 8) | trailer[9];
    milestones = DecodeMilestones(encoded);
}

double
PrimeFusionHelper::CalculateSessionMACOverhead(uint32_t blockNumber)
{
    // Calculate CPU cycles for this block
    uint32_t cycles;
    if (blockNumber % ROOT_CERT_INTERVAL == 0)
    {
        // Root certificate: Ed25519
        cycles = ED25519_CYCLES;
    }
    else
    {
        // Interim block: HMAC
        cycles = HMAC_CYCLES;
    }
    
    // Calculate reduction vs. pure Ed25519
    double reduction = ((ED25519_CYCLES - cycles) / static_cast<double>(ED25519_CYCLES)) * 100.0;
    
    return reduction;
}

double
PrimeFusionHelper::EstimateCompressionRatio()
{
    // Based on Python implementation results
    // CBOR compression achieves ~0.55-0.60 ratio
    return 0.559;
}

#endif // PRIMEFUSION_HELPER_H

