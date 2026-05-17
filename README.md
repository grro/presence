# Presence

A device presence detection system that monitors network-connected devices using IP-based ping detection. 
The system provides multiple interfaces for querying presence status, making it ideal for home automation,
occupancy detection, and AI integration.

## Features
- **IP-Based Presence Detection**: Monitors devices by pinging their IP addresses at configurable intervals
- **Multiple Server Interfaces**:
  - **WebThing Server**: Mozilla IoT Protocol integration for smart home automation
  - **REST API**: Simple HTTP endpoints for presence queries
  - **MCP Server**: Model Context Protocol support for AI/LLM integration with real-time push notifications
- **Presence Aggregation**: Combine multiple devices into aggregate presence sensors (e.g., "anyone home")
- **mDNS Service Discovery**: Automatic service registration for network discovery


## Docker
A Dockerfile is included for containerization:

```bash
docker build -f presence .
docker run --name presence --network host -e devices='Alice=192.168.1.100&Bob=192.168.1.101' grro/presence
```

