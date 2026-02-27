# Sentinel-Sentry
## Enterprise-Grade Asynchronous Attack Surface Mapper

Sentinel-Sentry is a high-performance network reconnaissance and service fingerprinting engine engineered for modern security auditing environments. Built on Python’s asynchronous I/O framework (`asyncio`), the platform enables large-scale concurrent port scanning and banner intelligence collection with minimal system overhead.

Designed for security researchers, blue teams, and penetration testers, Sentinel-Sentry demonstrates practical implementation of scalable network reconnaissance architecture without relying on thread-per-socket or multi-processing models.

---

## Executive Summary

Traditional scanners rely heavily on multi-threading, resulting in high memory usage and context-switching overhead. Sentinel-Sentry adopts a single-threaded, event-driven model capable of managing thousands of concurrent socket connections efficiently.

This architecture enables:
- High-speed TCP service discovery
- Low memory footprint under load
- Stable operation under file descriptor constraints
- Automated service fingerprint extraction
- Heuristic risk flagging of legacy/vulnerable services

---

## Core Security Capabilities

### Asynchronous Reconnaissance Engine
- Event-driven architecture using `asyncio`
- Non-blocking TCP connection handling
- Massive concurrency without thread overhead
- Optimized for high-latency network environments

### Controlled Concurrency Model
- Semaphore-based throttling mechanism
- Prevents descriptor exhaustion (`ulimit` compliance)
- Maintains stability during wide port-range scans

### Service Intelligence & Banner Acquisition
- Automated TCP handshake validation
- StreamReader-based banner capture
- Service version and OS signature extraction

### Heuristic Risk Classification Layer
- Pattern matching against legacy service indicators
- Prioritization of potentially vulnerable endpoints
- Structured risk-tiered reporting output

---

## Technical Architecture

    User Input
        ↓
    Target Parser
        ↓
    Async Task Scheduler (Event Loop)
        ↓
    Semaphore-Constrained Connection Pool
        ↓
    TCP Handshake + Banner Retrieval
        ↓
    Heuristic Analysis Engine
        ↓
    Structured Security Report

---

## Performance Characteristics

| Metric | Traditional Threaded Scanner | Sentinel-Sentry |
|--------|------------------------------|------------------|
| Concurrency Model | Thread-per-connection | Async event loop |
| Memory Usage | High under scale | Low and stable |
| Context Switching | Heavy | Minimal |
| Descriptor Safety | Manual control | Built-in throttling |
| Scalability | Moderate | High |

---

## Installation

### Requirements
- Python 3.10+
- Unix-based OS recommended (Linux/macOS)

### Setup

    git clone https://github.com/RohanDS2024/Sentinel-Sentry.git
    cd Sentinel-Sentry
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

---

## Optional: System-Wide Deployment

    chmod +x sentinel-launcher.sh
    sudo ln -s "$(pwd)/sentinel-launcher.sh" /usr/local/bin/Sentinel-Sentry

---

## Usage

### Basic Scan

    Sentinel-Sentry start --target 192.168.1.1

### Full Port Sweep

    Sentinel-Sentry start --target 192.168.1.1 --ports 1-65535

### Tuned Concurrency

    Sentinel-Sentry start --target 192.168.1.1 --ports 1-10000 --max-connections 500

---

## Security Use Cases

- Internal network exposure assessment
- Rapid service discovery during incident response
- Lab-based vulnerability research
- Blue-team attack surface mapping
- Security engineering demonstrations

---

## Defensive & Ethical Use Statement

Sentinel-Sentry is strictly intended for authorized security testing, academic research, and defensive cybersecurity operations.
Unauthorized scanning of networks or systems is illegal and unethical.

---

## Portfolio Value & Demonstrated Skills

This project demonstrates applied knowledge in:
- Asynchronous systems design (Python/Java)
- Event-driven architecture and Network socket programming
- Concurrency control mechanisms
- Resource-aware engineering for cloud and local deployments
- Service fingerprinting methodology
- Practical cybersecurity tooling development

---

## Author

**Rohan Devikoppa Shreedhara** M.S. Computer Science | Florida Atlantic University (FAU)  
Website Manager, FAU Cybersecurity Club  
Email: rohandstech@gmail.com  

Focused on scalable systems, cybersecurity engineering, cloud infrastructure, and performance-oriented software design.

---

## Future Enhancements Roadmap

- UDP scanning module
- CVE database integration
- JSON report export
- Distributed scanning capability
- Dockerized deployment
- SIEM integration support
- Real-time dashboard interface
