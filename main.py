import sys
import asyncio
from rich.console import Console
from rich.table import Table

console = Console()
semaphore = asyncio.Semaphore(100)

# The Ultimate Competition / CTF Port Dictionary
COMPETITION_PORTS = {
    21: "FTP (Cleartext)",
    22: "SSH",
    23: "Telnet (Cleartext)",
    25: "SMTP",
    53: "DNS",
    80: "HTTP (Web)",
    88: "Kerberos (Active Directory)",
    110: "POP3",
    111: "RPCbind",
    135: "MSRPC",
    139: "NetBIOS",
    389: "LDAP (Active Directory)",
    443: "HTTPS",
    445: "SMB (Windows Share)",
    636: "LDAPS",
    1433: "MSSQL (Database)",
    1521: "Oracle DB",
    2049: "NFS (Linux Share)",
    3306: "MySQL (Database)",
    3389: "RDP (Remote Desktop)",
    5432: "PostgreSQL",
    5900: "VNC (Remote Admin)",
    5985: "WinRM (Windows Remote)",
    8080: "HTTP Alternate"
}

async def scan_port(ip, port, results):
    async with semaphore:
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, port), timeout=0.8
            )
            
            # 1. Passive Listening
            try:
                banner_bytes = await asyncio.wait_for(reader.read(1024), timeout=1.0)
                banner = banner_bytes.decode().strip()
                if not banner:
                    raise ValueError("Empty")
            except:
                # 2. Active Probing (Poke silent web servers)
                try:
                    writer.write(b"GET / HTTP/1.1\r\n\r\n")
                    await writer.drain()
                    banner_bytes = await asyncio.wait_for(reader.read(1024), timeout=1.0)
                    banner = banner_bytes.decode().strip()
                    if "HTTP" in banner:
                        banner = banner.split("\n")[0] 
                    if not banner:
                        raise ValueError("Still Empty")
                except:
                    # 3. Competition Fallback Dictionary
                    banner = COMPETITION_PORTS.get(port, "Unknown / Silent")

            # Store the result
            results.append({"port": str(port), "status": "[green]OPEN[/]", "banner": banner})
            
            writer.close()
            await writer.wait_closed()
        except:
            pass

async def main():
    if len(sys.argv) < 2 or sys.argv[1].lower() != "start":
        console.print("[bold yellow]Usage: Sentinel-Sentry start[/]")
        return

    target_ip = "127.0.0.1" 
    results = [] 
    
    port_range = range(1, 10000)
    tasks = [scan_port(target_ip, p, results) for p in port_range]
    
    console.print(f"[bold blue][*] Initializing Sentinel Scan on {target_ip}...[/]")
    
    with console.status("[bold green]Scanning ports...") as status:
        await asyncio.gather(*tasks)

    table = Table(title=f"Sentinel-Sentry Scan Results: {target_ip}")
    table.add_column("Port", style="cyan")
    table.add_column("Status", style="bold green")
    table.add_column("Banner/Service", style="magenta")
    table.add_column("Risk Level", style="bold")

    for res in results:
        banner_upper = res["banner"].upper()
        
        # LOGIC: Advanced Competition Heuristics
        if "VULNERABLE" in banner_upper or "BACKDOOR" in banner_upper:
            risk = "[bold red]CRITICAL[/]"
            banner_style = "[bold red]" + res["banner"] + "[/]"
            
        # In competitions, exposing these usually means instant Red Team access
        elif any(x in banner_upper for x in ["TELNET", "FTP", "SMB", "RDP", "VNC", "WINRM"]):
            risk = "[bold orange3]HIGH[/]"
            banner_style = "[bold orange3]" + res["banner"] + "[/]"
            
        # AD and Database ports are high-value targets
        elif any(x in banner_upper for x in ["MYSQL", "MSSQL", "LDAP", "KERBEROS", "POSTGRES", "HTTP", "RPC"]):
            risk = "[bold yellow]MEDIUM[/]"
            banner_style = "[bold yellow]" + res["banner"] + "[/]"
            
        else:
            risk = "[bold green]LOW[/]"
            banner_style = res["banner"]

        table.add_row(res["port"], res["status"], banner_style, risk)

    console.print(table)

if __name__ == "__main__":
    asyncio.run(main())