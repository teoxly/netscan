"""
whois_dns.py
------------
Responsabilitate: pentru un domeniu dat, aflăm:
  - informații WHOIS (cine l-a înregistrat, când expiră)
  - înregistrări DNS (A, MX, NS, TXT)

Notă: WHOIS funcționează doar pentru domenii (google.com),
nu pentru IP-uri brute (8.8.8.8).
"""

import dns.resolver
import whois
from dataclasses import dataclass, field


@dataclass
class WhoisInfo:
    """Informații din registrul WHOIS al unui domeniu."""
    registrar: str        # compania prin care e înregistrat (ex: GoDaddy)
    creation_date: str    # când a fost înregistrat prima dată
    expiration_date: str  # când expiră înregistrarea
    name_servers: list    # serverele DNS responsabile pentru domeniu


@dataclass
class DNSInfo:
    """Înregistrările DNS ale unui domeniu."""
    # field(default_factory=list) = valoare implicită listă goală
    # (în @dataclass nu poți pune [] direct, folosești asta în schimb)
    a_records: list = field(default_factory=list)     # IP-uri ale domeniului
    mx_records: list = field(default_factory=list)    # servere de email
    ns_records: list = field(default_factory=list)    # servere de DNS
    txt_records: list = field(default_factory=list)   # înregistrări text


def get_whois_info(domain: str) -> WhoisInfo | None:
    """
    Interogează WHOIS pentru un domeniu și returnează informațiile găsite.
    Returnează None dacă domeniul nu există sau WHOIS nu răspunde.
    """
    try:
        w = whois.whois(domain)

        # Datele de dată pot veni ca listă (mai multe date istorice)
        # sau ca un singur obiect — le normalizăm la string
        creation = w.creation_date
        if isinstance(creation, list):
            creation = creation[0]   # luăm prima dată din listă

        expiration = w.expiration_date
        if isinstance(expiration, list):
            expiration = expiration[0]

        # Serverele de nume pot fi None dacă WHOIS nu le returnează
        name_servers = w.name_servers or []

        return WhoisInfo(
            registrar=w.registrar or "?",
            creation_date=str(creation)[:10] if creation else "?",   # doar data, fără ora
            expiration_date=str(expiration)[:10] if expiration else "?",
            name_servers=list(name_servers),
        )

    except Exception:
        return None


def get_dns_records(domain: str) -> DNSInfo:
    """
    Interoghează serverele DNS pentru toate tipurile de înregistrări.
    Dacă un tip de înregistrare nu există, lasă lista goală — nu e eroare.
    """
    info = DNSInfo()

    # Pentru fiecare tip de înregistrare, încercăm să o obținem
    # Dacă nu există sau DNS-ul nu răspunde, continuăm cu celelalte
    record_types = {
        "A":   info.a_records,    # IP-uri
        "MX":  info.mx_records,   # mail servers
        "NS":  info.ns_records,   # name servers
        "TXT": info.txt_records,  # text records
    }

    for record_type, target_list in record_types.items():
        try:
            # dns.resolver.resolve() întreabă DNS-ul: "ce înregistrări
            # de tipul X există pentru acest domeniu?"
            answers = dns.resolver.resolve(domain, record_type)

            for record in answers:
                # Fiecare tip de înregistrare are un format diferit
                # MX are și o prioritate (ex: "10 smtp.google.com")
                # celelalte sunt text simplu
                target_list.append(str(record))

        except Exception:
            pass  # înregistrarea nu există sau DNS-ul a dat eroare — ignorăm

    return info


def get_full_info(domain: str) -> tuple[WhoisInfo | None, DNSInfo]:
    """
    Funcția principală — returnează atât WHOIS cât și DNS într-un singur apel.
    Returnează un tuple: (whois_info, dns_info)
    """
    whois_info = get_whois_info(domain)
    dns_info = get_dns_records(domain)
    return whois_info, dns_info