import asyncio

# Dictionary mapping ports to their fake service banners
MOCK_SERVICES = {
    9999: b"SSH-2.0-Sentinel-Sentry-Mock-Vulnerable\n",   # Triggers CRITICAL (contains "Vulnerable")
    2121: b"220 ProFTPD 1.3.3c Server (Backdoor-Active)\r\n", # Triggers HIGH 
    2323: b"Welcome to Telnet Service. Password:\n",        # Triggers MEDIUM (Cleartext protocol)
    8080: b"HTTP/1.1 200 OK\r\nServer: nginx/1.24.0\r\n",   # Triggers LOW/INFO (Standard web server)
    3306: b"mysql_native_password\n"                        # Triggers INFO (Standard DB)
}

async def handle_client(reader, writer, port):
    # Send the fake banner when the scanner connects
    banner = MOCK_SERVICES.get(port, b"Unknown Service\n")
    writer.write(banner)
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def start_mock_server(port):
    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, port),
        '127.0.0.1', port
    )
    print(f"[*] Mock Service listening on Port {port}...")
    async with server:
        await server.serve_forever()

async def main():
    print("[!] Starting Sentinel-Sentry Multi-Target Lab...")
    # Start a listener for every port in our dictionary simultaneously
    tasks = [start_mock_server(port) for port in MOCK_SERVICES.keys()]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Shutting down mock servers.")