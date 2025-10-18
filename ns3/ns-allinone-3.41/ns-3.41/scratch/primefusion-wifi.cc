/*
 * PrimeFusion-FANET NS-3 WiFi Simulation
 * ======================================
 * 
 * Simplified version with proper broadcast reception.
 * Uses subnet broadcast and proper socket configuration.
 * 
 * Author: PrimeFusion-FANET Team
 * Date: October 2025
 * Version: 3.0 (Fixed broadcast reception)
 */

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/mobility-module.h"
#include "ns3/wifi-module.h"
#include "ns3/internet-module.h"
#include "primefusion-helper.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE("PrimeFusionWiFi");

// Global variables for metrics
uint32_t g_beaconsSent = 0;
uint32_t g_beaconsReceived = 0;
std::vector<double> g_latencies;
uint64_t g_totalBytes = 0;

// Per-node state
struct NodeState
{
    Ptr<Socket> sendSocket;
    Ptr<Socket> recvSocket;
    uint32_t nodeId;
    uint32_t blockNumber;
    uint32_t packetsSent;
    uint32_t maxPackets;
    uint32_t packetSize;
    PrimeFusionHelper primefusion;
};

std::vector<NodeState> g_nodeStates;

/**
 * Send beacon function
 */
void SendBeacon(NodeState* state)
{
    // Generate blockchain hash
    std::string blockHash = state->primefusion.GenerateBlockchainHash(state->blockNumber);
    
    // Encode milestones
    std::vector<uint8_t> milestones = {7, 8, 9};
    uint16_t encodedMilestones = state->primefusion.EncodeMilestones(milestones);
    
    // Create beacon trailer
    std::vector<uint8_t> trailer = state->primefusion.CreateBeaconTrailer(blockHash, encodedMilestones);
    
    // Create packet
    Ptr<Packet> packet = Create<Packet>(state->packetSize - trailer.size());
    packet->AddAtEnd(Create<Packet>(&trailer[0], trailer.size()));
    
    // Add timestamp
    TimestampTag timestamp(Simulator::Now());
    packet->AddByteTag(timestamp);
    
    // Send
    int sent = state->sendSocket->Send(packet);
    
    if (sent > 0)
    {
        // Update metrics
        g_beaconsSent++;
        g_totalBytes += packet->GetSize();
        state->blockNumber++;
        state->packetsSent++;
        
        NS_LOG_INFO("Node " << state->nodeId << " sent beacon " << state->packetsSent << " (" << packet->GetSize() << " bytes)");
    }
    else
    {
        NS_LOG_WARN("Node " << state->nodeId << " failed to send beacon");
    }
    
    // Schedule next beacon
    if (state->packetsSent < state->maxPackets)
    {
        Simulator::Schedule(Seconds(1.0), &SendBeacon, state);
    }
}

/**
 * Receive callback
 */
void ReceiveBeacon(Ptr<Socket> socket)
{
    Ptr<Packet> packet;
    Address from;
    
    while ((packet = socket->RecvFrom(from)))
    {
        // Extract timestamp
        TimestampTag timestamp;
        if (packet->FindFirstMatchingByteTag(timestamp))
        {
            Time tx = timestamp.GetTimestamp();
            Time rx = Simulator::Now();
            Time latency = rx - tx;
            g_latencies.push_back(latency.GetMilliSeconds());
        }
        
        g_beaconsReceived++;
        
        InetSocketAddress inetAddr = InetSocketAddress::ConvertFrom(from);
        NS_LOG_INFO("Received beacon from " << inetAddr.GetIpv4() << ": size=" << packet->GetSize() << " bytes");
    }
}

/**
 * Main simulation function
 */
int main(int argc, char* argv[])
{
    // Default parameters
    uint32_t nUavs = 5;
    double duration = 60.0;
    double beaconInterval = 1.0;
    uint32_t beaconSize = 160;
    bool verbose = false;
    
    // Command line arguments
    CommandLine cmd;
    cmd.AddValue("nUavs", "Number of UAV nodes", nUavs);
    cmd.AddValue("duration", "Simulation duration (seconds)", duration);
    cmd.AddValue("beaconInterval", "Beacon interval (seconds)", beaconInterval);
    cmd.AddValue("beaconSize", "Beacon size (bytes)", beaconSize);
    cmd.AddValue("verbose", "Enable verbose logging", verbose);
    cmd.Parse(argc, argv);
    
    // Enable logging
    if (verbose)
    {
        LogComponentEnable("PrimeFusionWiFi", LOG_LEVEL_INFO);
    }
    
    // Print configuration
    std::cout << "\n========================================" << std::endl;
    std::cout << "PrimeFusion-FANET NS-3 WiFi Simulation" << std::endl;
    std::cout << "========================================" << std::endl;
    std::cout << "Configuration:" << std::endl;
    std::cout << "  UAVs: " << nUavs << std::endl;
    std::cout << "  Duration: " << duration << "s" << std::endl;
    std::cout << "  Beacon interval: " << beaconInterval << "s" << std::endl;
    std::cout << "  Beacon size: " << beaconSize << " bytes" << std::endl;
    std::cout << "  PHY: WiFi 802.11n" << std::endl;
    std::cout << "========================================\n" << std::endl;
    
    // Create UAV nodes
    NodeContainer uavNodes;
    uavNodes.Create(nUavs);
    
    // Setup WiFi
    WifiHelper wifi;
    wifi.SetStandard(WIFI_STANDARD_80211n);
    wifi.SetRemoteStationManager("ns3::ConstantRateWifiManager",
                                  "DataMode", StringValue("HtMcs7"),
                                  "ControlMode", StringValue("HtMcs0"));
    
    YansWifiPhyHelper wifiPhy;
    YansWifiChannelHelper wifiChannel = YansWifiChannelHelper::Default();
    wifiPhy.SetChannel(wifiChannel.Create());
    
    WifiMacHelper wifiMac;
    wifiMac.SetType("ns3::AdhocWifiMac");
    
    NetDeviceContainer devices = wifi.Install(wifiPhy, wifiMac, uavNodes);
    
    // Setup mobility - Close grid for good connectivity
    MobilityHelper mobility;
    mobility.SetPositionAllocator("ns3::GridPositionAllocator",
                                  "MinX", DoubleValue(0.0),
                                  "MinY", DoubleValue(0.0),
                                  "DeltaX", DoubleValue(10.0),  // 10m spacing - very close
                                  "DeltaY", DoubleValue(10.0),
                                  "GridWidth", UintegerValue(5),
                                  "LayoutType", StringValue("RowFirst"));
    mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");
    mobility.Install(uavNodes);
    
    // Set altitude
    for (uint32_t i = 0; i < nUavs; ++i)
    {
        Ptr<MobilityModel> mob = uavNodes.Get(i)->GetObject<MobilityModel>();
        Vector pos = mob->GetPosition();
        pos.z = 100.0;
        mob->SetPosition(pos);
    }
    
    // Install Internet stack
    InternetStackHelper internet;
    internet.Install(uavNodes);
    
    Ipv4AddressHelper ipv4;
    ipv4.SetBase("10.1.1.0", "255.255.255.0");
    Ipv4InterfaceContainer interfaces = ipv4.Assign(devices);
    
    // Print IP addresses for debugging
    if (verbose)
    {
        for (uint32_t i = 0; i < nUavs; ++i)
        {
            Ptr<Ipv4> ipv4Node = uavNodes.Get(i)->GetObject<Ipv4>();
            Ipv4Address addr = ipv4Node->GetAddress(1, 0).GetLocal();
            std::cout << "Node " << (i+1) << " IP: " << addr << std::endl;
        }
    }
    
    // Setup sockets and node states
    TypeId tid = TypeId::LookupByName("ns3::UdpSocketFactory");
    uint32_t maxPackets = static_cast<uint32_t>(duration / beaconInterval);
    
    g_nodeStates.resize(nUavs);
    
    for (uint32_t i = 0; i < nUavs; ++i)
    {
        // Create receiver socket FIRST
        Ptr<Socket> recvSocket = Socket::CreateSocket(uavNodes.Get(i), tid);
        InetSocketAddress local = InetSocketAddress(Ipv4Address::GetAny(), 9);
        if (recvSocket->Bind(local) == -1)
        {
            NS_LOG_ERROR("Failed to bind receiver socket on node " << i);
        }
        recvSocket->SetAllowBroadcast(true);
        recvSocket->SetRecvCallback(MakeCallback(&ReceiveBeacon));
        
        // Create sender socket
        Ptr<Socket> sendSocket = Socket::CreateSocket(uavNodes.Get(i), tid);
        InetSocketAddress remote = InetSocketAddress(Ipv4Address("10.1.1.255"), 9);  // Subnet broadcast
        sendSocket->SetAllowBroadcast(true);
        if (sendSocket->Connect(remote) == -1)
        {
            NS_LOG_ERROR("Failed to connect sender socket on node " << i);
        }
        
        // Initialize node state
        g_nodeStates[i].sendSocket = sendSocket;
        g_nodeStates[i].recvSocket = recvSocket;
        g_nodeStates[i].nodeId = i + 1;
        g_nodeStates[i].blockNumber = 0;
        g_nodeStates[i].packetsSent = 0;
        g_nodeStates[i].maxPackets = maxPackets;
        g_nodeStates[i].packetSize = beaconSize;
        
        // Schedule first beacon (stagger start times slightly)
        Simulator::Schedule(Seconds(1.0 + i * 0.01), &SendBeacon, &g_nodeStates[i]);
    }
    
    // Run simulation
    std::cout << "Running simulation..." << std::endl;
    
    Simulator::Stop(Seconds(duration + 2.0));
    Simulator::Run();
    
    // Calculate metrics
    double pdr = (g_beaconsSent > 0) ? (100.0 * g_beaconsReceived / g_beaconsSent) : 0.0;
    double avgLatency = 0.0;
    if (!g_latencies.empty())
    {
        for (double lat : g_latencies)
        {
            avgLatency += lat;
        }
        avgLatency /= g_latencies.size();
    }
    double throughput = (g_totalBytes * 8.0) / (duration * 1000.0);
    
    // Print results
    std::cout << "\n========================================" << std::endl;
    std::cout << "Simulation Results" << std::endl;
    std::cout << "========================================" << std::endl;
    std::cout << "Network Metrics:" << std::endl;
    std::cout << "  Beacons sent: " << g_beaconsSent << std::endl;
    std::cout << "  Beacons received: " << g_beaconsReceived << std::endl;
    std::cout << "  PDR: " << std::fixed << std::setprecision(2) << pdr << "%" << std::endl;
    std::cout << "  Avg latency: " << std::fixed << std::setprecision(3) << avgLatency << " ms" << std::endl;
    std::cout << "  Throughput: " << std::fixed << std::setprecision(2) << throughput << " kbps" << std::endl;
    std::cout << "========================================\n" << std::endl;
    
    Simulator::Destroy();
    
    return 0;
}

