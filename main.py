"""
main.py
-------
Punctul de intrare al scannerului.
"""

import sys
from scanner.input_parser import parse_target
from scanner.port_scanner import scan_ports, get_default_ports
from scanner.ip_info import get_ip_info
from scanner.whois_dns import get_full_info


def print_target_info(target):
    print(f"\n  IP           : {target.ip}")
    print(f"  Hostname     : {target.hostname or '—'}")
    print(f"  Network type : {'Private (LAN)' if target.is_private else 'Public (Internet)'}")
    print(f"  Version      : IPv{target.ip_version}")


def print_ip_info(info):
    if info is None:
        print("\n  [!] Geographic information unavailable (private IP or no Internet)")
        return

    print(f"\n  Country      : {info.country}")
    print(f"  Region       : {info.region}")
    print(f"  City         : {info.city}")
    print(f"  ISP          : {info.isp}")
    print(f"  Org          : {info.org}")
    print(f"  Timezone     : {info.timezone}")
    print(f"  Coordinates  : {info.lat}, {info.lon}")


def print_whois_dns_info(domain):
    whois_info, dns_info = get_full_info(domain)

    if whois_info:
        print("\n  --- WHOIS ---")
        print(f"  Registrar     : {whois_info.registrar}")
        print(f"  Creation date : {whois_info.creation_date}")
        print(f"  Expiration    : {whois_info.expiration_date}")
        print(f"  Name servers  : {', '.join(whois_info.name_servers) if whois_info.name_servers else '—'}")
    else:
        print("\n  [!] WHOIS information unavailable")

    print("\n  --- DNS ---")
    print(f"  A records   : {', '.join(dns_info.a_records) if dns_info.a_records else '—'}")
    print(f"  MX records  : {', '.join(dns_info.mx_records) if dns_info.mx_records else '—'}")
    print(f"  NS records  : {', '.join(dns_info.ns_records) if dns_info.ns_records else '—'}")
    print(f"  TXT records : {', '.join(dns_info.txt_records) if dns_info.txt_records else '—'}")


def print_port_results(open_ports):
    if not open_ports:
        print("\n  No open ports found.")
        return

    print(f"\n  {'PORT':<8} {'SERVICE':<15} {'BANNER'}")
    print("  " + "-" * 60)

    for p in open_ports:
        banner = p["banner"] or "—"
        if len(banner) > 40:
            banner = banner[:40] + "..."
        print(f"  {p['port']:<8} {p['service']:<15} {banner}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <ip|domeniu|CIDR>")
        sys.exit(1)

    raw_input = sys.argv[1]

    print(f"\n[*] Target: {raw_input}")
    try:
        targets = parse_target(raw_input)
    except ValueError as e:
        print(f"[!] Error: {e}")
        sys.exit(1)

    ports_to_scan = get_default_ports()

    for target in targets:
        print(f"\n{'=' * 50}")

        print("\n--- General information ---")
        print_target_info(target)

        if target.hostname:
            print("\n--- WHOIS / DNS ---")
            print_whois_dns_info(target.hostname)

        print("\n--- Location and provider ---")
        ip_info = get_ip_info(target.ip)
        print_ip_info(ip_info)

        print("\n--- Ports ---")
        print(f"[*] Scanning {len(ports_to_scan)} ports...")
        open_ports = scan_ports(target.ip, ports_to_scan)
        print_port_results(open_ports)


if __name__ == "__main__":
    main()