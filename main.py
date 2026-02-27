import sys
import asyncio
from rich.console import Console
from rich.table import Table
from rich.live import Live

console = Console()
semaphore = asyncio.Semaphore(100)

async def scan_port(ip, port, results):
    async with semaphore:
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, port), timeout=0.8
            )
            try:
                banner_bytes = await asyncio.wait_for(reader.read(1024), timeout=1.0)
                banner = banner_bytes.decode().strip()
            except:
                banner = "Unknown"

            # Store the result for the table
            results.append({"port": str(port), "status": "[green]OPEN[/]", "banner": banner})
            
            writer.close()
            await writer.wait_closed()
        except:
            pass

async def main():
    # Check if the 'start' argument was provided
    if len(sys.argv) < 2 or sys.argv[1].lower() != "start":
        console.print("[bold yellow]Usage: Sentinel-Sentry start[/]")
        return

    target_ip = "127.0.0.1" # Internal scan
    results = [] # To store found services
    
    # We will scan a wider range to show the power of the tool
    port_range = range(9990, 10005)
    tasks = [scan_port(target_ip, p, results) for p in port_range]
    
    console.print(f"[bold blue][*] Initializing Sentinel Scan on {target_ip}...[/]")
    
    with console.status("[bold green]Scanning ports...") as status:
        await asyncio.gather(*tasks)

    # Professional Table Output
    table = Table(title=f"Sentinel-Sentry Scan Results: {target_ip}")
    table.add_column("Port", style="cyan")
    table.add_column("Status", style="bold green")
    table.add_column("Banner/Service", style="magenta")
    table.add_column("Risk Level", style="bold")

    for res in results:
        # LOGIC: Check for vulnerabilities in the banner
        if "Vulnerable" in res["banner"]:
            risk = "[bold red]CRITICAL[/]"
            banner_style = "[bold red]" + res["banner"] + "[/]"
        else:
            risk = "[blue]LOW[/]"
            banner_style = res["banner"]

        table.add_row(res["port"], res["status"], banner_style, risk)

    console.print(table)

if __name__ == "__main__":
    asyncio.run(main())