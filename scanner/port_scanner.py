"""
port_scanner.py
---------------
Responsabilitate: încearcă să se conecteze la fiecare port al unui IP
și raportează care sunt deschise și ce serviciu rulează pe ele.
"""

import socket
import concurrent.futures

COMMON_SERVICES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-alt",
    8443: "HTTPS-alt",
    27017: "MongoDB",
}


def grab_banner(sock) -> str | None:
    """
    După ce ne-am conectat la un port, încercăm să citim banner-ul.
    """
    try:
        sock.settimeout(2)
        banner = sock.recv(1024)
        return banner.decode(errors="ignore").strip()
    except Exception:
        return None


def scan_port(ip: str, port: int, timeout: float = 1.0) -> dict | None:
    """
    Încearcă să se conecteze la un singur port.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        result = sock.connect_ex((ip, port))
        if result == 0:
            banner = grab_banner(sock)
            return {
                "port": port,
                "service": COMMON_SERVICES.get(port, "unknown"),
                "banner": banner,
            }
        return None
    except Exception:
        return None
    finally:
        sock.close()


def scan_ports(ip: str, ports: list[int], max_threads: int = 100) -> list[dict]:
    """
    Scanează o listă de porturi în paralel folosind threading.
    """
    open_ports = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {
            executor.submit(scan_port, ip, port): port
            for port in ports
        }

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result is not None:
                open_ports.append(result)

    return sorted(open_ports, key=lambda x: x["port"])


def get_default_ports() -> list[int]:
    """
    Returnează lista porturilor pe care le scanăm implicit.
    """
    return list(COMMON_SERVICES.keys())