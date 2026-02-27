import socket

# This script creates a 'fake' open port for your scanner to find later
def start_mock_service():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Allow the port to be reused immediately if we restart
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server.bind(('127.0.0.1', 9999))
    server.listen(5)
    print("[+] Mock Target listening on 127.0.0.1:9999...")
    
    while True:
        client, addr = server.accept()
        # This is the 'Banner' your scanner will eventually 'Grab'
        client.send(b"SSH-2.0-Sentinel-Sentry-Mock-Vulnerable\n")
        client.close()

if __name__ == "__main__":
    start_mock_service()