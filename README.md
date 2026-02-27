# Sentinel-Sentry: Asynchronous Attack Surface Mapper

Sentinel-Sentry is a high-performance network auditing utility designed for rapid service discovery and fingerprinting. By utilizing Python’s `asyncio` framework, the tool performs non-blocking I/O operations, allowing for massive concurrency in port scanning and banner acquisition without the overhead typically associated with synchronous multi-threading or multi-processing.

---

## Core Technical Features

### Asynchronous Event Loop

The scanner operates on a single-threaded event loop that manages thousands of concurrent connection attempts. This architecture significantly reduces context-switching overhead and memory consumption compared to traditional thread-per-socket models.

### Concurrency Throttling via Semaphores

To prevent resource exhaustion and ensure compliance with system-level file descriptor limits (`ulimit`), Sentinel-Sentry implements an `asyncio.Semaphore`. This mechanism caps the number of active, open sockets at any given millisecond, ensuring stability on consumer-grade hardware.

### Automated Service Fingerprinting

Upon establishing a successful TCP handshake, the engine performs a banner-grabbing routine. It utilizes a `StreamReader` to capture the initial data payload sent by the server, allowing for precise identification of service versions and underlying operating systems.

### Heuristic Risk Classification

The engine includes a post-processing layer that parses retrieved banners for known security signatures. Services returning strings associated with vulnerable or legacy software are automatically prioritized in the final report.

---

## Installation and Deployment

### 1. Environment Configuration

Sentinel-Sentry requires Python 3.10 or higher. It is recommended to deploy within a virtual environment to maintain dependency integrity.

```bash
git clone https://github.com/RohanDS2024/Sentinel-Sentry.git
cd Sentinel-Sentry
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### 2. Global Path Integration
To enable system-wide execution, a shell-wrapper launcher is provided. This wrapper handles virtual environment activation and absolute path resolution automatically.
chmod +x sentinel-launcher.sh
sudo ln -s $(pwd)/sentinel-launcher.sh /usr/local/bin/Sentinel-Sentry

### 3. Execution
Once deployed to the system path, the tool can be initialized from any directory:
Sentinel-Sentry start
