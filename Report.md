# 📊 Engineering Engagement Report: Sentinel-Sentry

**Status:** Deployed / Operational  
**Classification:** Internal / Academic Research  

## 1. Executive Summary
The Sentinel-Sentry project focused on the development of a lightweight, asynchronous tool for internal security teams to map their attack surface. Unlike traditional scanners, this engine prioritizes the speed of non-blocking I/O tasks, allowing a single-threaded process to manage hundreds of concurrent connections with minimal CPU overhead.

## 2. Technical Architecture & Concurrency
The engine utilizes a custom semaphore-throttled task queue. By limiting active connections to a specific pool (Semaphore=100), the tool avoids the common "Max Open Files" (file descriptor) limit exhaustion on Unix-based systems while maintaining high throughput.

### 3-Tier Service Fingerprinting Logic
To handle both verbose and silent network services, the scanner implements a robust three-tier identification system:

1. **Passive Banner Grabbing:** The engine establishes a TCP handshake and waits up to 1.0 seconds for the service to transmit a welcome banner (e.g., SSH or FTP).
2. **Active Payload Probing:** If the socket times out (common with web servers), the engine transmits a generic `GET / HTTP/1.1\r\n\r\n` payload to force a response and parses the resulting Server headers.
3. **Heuristic Port Fallback:** If the packet is dropped or the service remains silent, the engine references a hardcoded dictionary of common high-value competition target ports (e.g., 445/SMB, 3389/RDP) to categorize the potential exposure.



## 3. Advanced Risk Heuristics
The post-processing engine parses retrieved banners and port associations against a known-threat matrix, outputting a structured, color-coded terminal report:
* **CRITICAL:** Explicitly vulnerable service strings or known backdoors.
* **HIGH:** Cleartext protocols (Telnet, FTP) and high-value remote management targets (SMB, RDP, WinRM).
* **MEDIUM:** Standard database deployments (MSSQL, MySQL) and Active Directory infrastructure (LDAP, Kerberos) that require configuration auditing.
* **LOW:** Standard, low-risk network services.

## 4. Engineering Challenges & Mitigations

| Challenge | Technical Impact | Resolution |
| :--- | :--- | :--- |
| **File Descriptor Caps** | Large-scale scans (65k+ ports) on macOS/Linux can hit the system `ulimit`, causing process termination. | **Concurrency Throttling:** Implemented `asyncio.Semaphore` to cap active sockets, ensuring system stability. |
| **Tarpit/Latency Latency** | Synchronous banner grabs on filtered or "tarpit" ports would block the entire event loop. | **Timeout Enforcement:** Wrapped all `StreamReader` operations in strict `asyncio.wait_for` blocks. |
| **Silent Port Timeouts** | Web servers (Port 80/443) would register as "Unknown" due to awaiting an initial client request. | **Active Probing Protocol:** Engineered a fallback `try/except` block to inject an HTTP GET request into silent sockets. |

## 5. Professional Incident Response Log (Development Phase)

| ID | Issue | Mitigation Strategy | Result |
| :--- | :--- | :--- | :--- |
| **IR-101** | **Socket Binding Conflict** (`EADDRINUSE`) | Implemented `socket.SO_REUSEADDR` in test listeners to allow immediate port recycling. | **Resolved** |
| **IR-102** | **Asynchronous Blocking** | Identified blocking calls in standard library `socket` calls; migrated to `asyncio.open_connection`. | **Resolved** |
| **IR-103** | **Environment Integrity** | Resolved dependency conflicts across macOS/Linux by implementing a local-path wrapper script. | **Resolved** |