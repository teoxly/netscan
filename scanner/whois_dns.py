"""
whois_dns.py
------------
Responsabilitate: pentru un domeniu dat, aflăm:
  - informații WHOIS
  - înregistrări DNS
"""

import dns.resolver
import whois
from dataclasses import dataclass, field


@dataclass
class WhoisInfo:
    """Informații din registrul WHOIS al unui domeniu."""
    registrar: str
    creation_date: str
    expiration_date: str
    name_servers: list


@dataclass
class DNSInfo:
    """Înregistrările DNS ale unui domeniu."""
    a_records: list = field(default_factory=list)
    mx_records: list = field(default_factory=list)
    ns_records: list = field(default_factory=list)
    txt_records: list = field(default_factory=list)


def get_whois_info(domain: str) -> WhoisInfo | None:
    """
    Interoghează WHOIS pentru un domeniu și returnează informațiile găsite.
    """
    try:
        w = whois.whois(domain)

        creation = w.creation_date
        if isinstance(creation, list):
            creation = creation[0]

        expiration = w.expiration_date
        if isinstance(expiration, list):
            expiration = expiration[0]

        name_servers = w.name_servers or []

        return WhoisInfo(
            registrar=w.registrar or "?",
            creation_date=str(creation)[:10] if creation else "?",
            expiration_date=str(expiration)[:10] if expiration else "?",
            name_servers=list(name_servers),
        )
    except Exception:
        return None


def get_dns_records(domain: str) -> DNSInfo:
    """
    Interoghează serverele DNS pentru A, MX, NS și TXT.
    """
    info = DNSInfo()

    record_types = {
        "A": info.a_records,
        "MX": info.mx_records,
        "NS": info.ns_records,
        "TXT": info.txt_records,
    }

    for record_type, target_list in record_types.items():
        try:
            answers = dns.resolver.resolve(domain, record_type)
            for record in answers:
                target_list.append(str(record))
        except Exception:
            pass

    return info


def get_full_info(domain: str) -> tuple[WhoisInfo | None, DNSInfo]:
    """
    Returnează atât WHOIS cât și DNS într-un singur apel.
    """
    whois_info = get_whois_info(domain)
    dns_info = get_dns_records(domain)
    return whois_info, dns_info