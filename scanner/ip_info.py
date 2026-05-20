"""
ip_info.py
----------
Responsabilitate: trimite un IP către ip-api.com și returnează
informații despre locație, provider etc.
"""

import ipaddress
import requests
from dataclasses import dataclass


@dataclass
class IPInfo:
    """Cutia cu informații despre un IP."""
    ip: str
    country: str
    city: str
    region: str
    isp: str
    org: str
    lat: float
    lon: float
    timezone: str


def get_ip_info(ip: str) -> IPInfo | None:
    """
    Întreabă ip-api.com despre un IP și returnează un obiect IPInfo.
    Returnează None dacă ceva merge prost sau IP-ul e privat.
    """
    try:
        addr = ipaddress.ip_address(ip)
        if addr.is_private or addr.is_loopback:
            return None
    except ValueError:
        return None

    try:
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("status") != "success":
            return None

        return IPInfo(
            ip=ip,
            country=data.get("country", "?"),
            city=data.get("city", "?"),
            region=data.get("regionName", "?"),
            isp=data.get("isp", "?"),
            org=data.get("org", "?"),
            lat=data.get("lat", 0.0),
            lon=data.get("lon", 0.0),
            timezone=data.get("timezone", "?"),
        )

    except requests.exceptions.ConnectionError:
        print("  [!] Nu mă pot conecta la ip-api.com")
        return None
    except requests.exceptions.Timeout:
        print("  [!] ip-api.com nu a răspuns la timp")
        return None
    except Exception as e:
        print(f"  [!] Eroare neașteptată: {e}")
        return None