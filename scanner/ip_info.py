"""
ip_info.py
----------
Responsabilitate: trimite un IP către ip-api.com și returnează
informații despre locație, provider, etc.
"""

import requests
from dataclasses import dataclass


@dataclass
class IPInfo:
    """Cutia cu informații despre un IP — același concept ca ParsedTarget."""
    ip: str
    country: str
    city: str
    region: str
    isp: str        # Internet Service Provider — compania care deține IP-ul
    org: str        # organizația (uneori diferită de ISP)
    lat: float      # latitudine
    lon: float      # longitudine
    timezone: str


def get_ip_info(ip: str) -> IPInfo | None:
    """
    Întreabă ip-api.com despre un IP și returnează un obiect IPInfo.
    Returnează None dacă ceva merge prost (IP privat, fără internet, etc.)
    """

    # IP-urile private (192.168.x.x, 10.x.x.x) nu au informații publice
    # ip-api.com nu le poate localiza, deci nu are sens să întrebăm
    if ip.startswith("192.168.") or ip.startswith("10.") or ip.startswith("127."):
        return None

    try:
        # Construim URL-ul — practic adresa la care "batem"
        url = f"http://ip-api.com/json/{ip}"

        # requests.get() face un HTTP request și așteaptă răspunsul
        # timeout=5 înseamnă: dacă nu răspunde în 5 secunde, renunțăm
        response = requests.get(url, timeout=5)

        # Transformăm răspunsul din text JSON într-un dicționar Python
        # Adică din '{"country": "Romania"}' → {"country": "Romania"}
        data = response.json()

        # ip-api.com ne spune dacă cererea a reușit prin câmpul "status"
        if data.get("status") != "success":
            return None

        # Construim și returnăm obiectul IPInfo cu datele primite
        # data.get("country", "?") înseamnă: ia valoarea "country" din dicționar,
        # iar dacă nu există, pune "?" în loc să dea eroare
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