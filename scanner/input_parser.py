"""
input_parser.py
---------------
Responsabilitate: primește ce tastează utilizatorul și returnează
o listă curată de IP-uri gata de scanat.

Suportă trei formate:
  1. IP direct        →  192.168.1.1
  2. Domeniu          →  google.com
  3. Range CIDR       →  192.168.1.0/24
"""

import ipaddress
import socket
from dataclasses import dataclass


@dataclass
class ParsedTarget:
    """Rezultatul parsării: tot ce știm despre țintă înainte de scanare."""
    raw_input: str          # ce a tastat utilizatorul
    ip: str                 # IP-ul rezolvat
    hostname: str | None    # domeniu (dacă a dat domeniu) sau None
    is_private: bool        # IP privat (192.168.x.x, 10.x.x.x etc.)
    ip_version: int         # 4 sau 6


def resolve_hostname(hostname: str) -> str:
    """
    Transformă un domeniu (ex: google.com) în IP.
    Aruncă ValueError dacă domeniul nu există.
    """
    try:
        ip = socket.gethostbyname(hostname)
        return ip
    except socket.gaierror:
        raise ValueError(f"Nu pot rezolva domeniul: '{hostname}'")


def parse_single_target(raw: str) -> ParsedTarget:
    """
    Parsează un singur target: IP sau domeniu.
    Returnează un ParsedTarget cu toate informațiile.
    """
    raw = raw.strip()

    # Încearcă să parseze direct ca IP
    try:
        addr = ipaddress.ip_address(raw)
        return ParsedTarget(
            raw_input=raw,
            ip=str(addr),
            hostname=None,
            is_private=addr.is_private,
            ip_version=addr.version,
        )
    except ValueError:
        pass  # nu e IP, probabil e domeniu

    # Tratează ca domeniu și rezolvă DNS
    ip_str = resolve_hostname(raw)
    addr = ipaddress.ip_address(ip_str)

    return ParsedTarget(
        raw_input=raw,
        ip=ip_str,
        hostname=raw,
        is_private=addr.is_private,
        ip_version=addr.version,
    )


def parse_cidr(cidr: str) -> list[ParsedTarget]:
    """
    Expandează un range CIDR (ex: 192.168.1.0/24) într-o listă de IP-uri.
    Pentru /24 → 254 hosturi, pentru /16 → limităm la 1024 ca să nu dureze ore.
    """
    try:
        network = ipaddress.ip_network(cidr, strict=False)
    except ValueError:
        raise ValueError(f"Format CIDR invalid: '{cidr}'")

    hosts = list(network.hosts())

    MAX_HOSTS = 1024
    if len(hosts) > MAX_HOSTS:
        print(f"  [!] Range-ul are {len(hosts)} hosturi. Scanez doar primele {MAX_HOSTS}.")
        hosts = hosts[:MAX_HOSTS]

    return [
        ParsedTarget(
            raw_input=cidr,
            ip=str(host),
            hostname=None,
            is_private=host.is_private,
            ip_version=host.version,
        )
        for host in hosts
    ]


def parse_target(raw: str) -> list[ParsedTarget]:
    """
    Punct de intrare principal.
    Detectează automat tipul inputului și returnează lista de targete.

    Exemple:
        parse_target("8.8.8.8")           → [ParsedTarget(ip="8.8.8.8", ...)]
        parse_target("google.com")         → [ParsedTarget(ip="142.250.x.x", hostname="google.com", ...)]
        parse_target("192.168.1.0/24")    → [ParsedTarget(...), ParsedTarget(...), ...]
    """
    raw = raw.strip()

    if not raw:
        raise ValueError("Input gol — specifică un IP, domeniu sau range CIDR.")

    # Detectează CIDR după slash
    if "/" in raw:
        return parse_cidr(raw)

    # Altfel: IP sau domeniu
    return [parse_single_target(raw)]