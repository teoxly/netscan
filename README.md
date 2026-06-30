# netscan

A Python network reconnaissance tool I built inspired by nmap. Give it an IP, domain, or CIDR range and it returns open ports, geolocation, WHOIS data, and DNS records.

## Features

- Port scanning — checks common TCP ports in parallel using threading and identifies running services
- Geolocation — country, city, ISP via ip-api.com
- WHOIS lookups — registrar, registration/expiration dates
- DNS resolution — A, MX, NS, TXT records
- Works with single IPs, domains, or CIDR ranges

## Setup

```
git clone https://github.com/username/netscan.git
cd netscan
pip install -r requirements.txt
```

## How to use

```
python main.py 8.8.8.8           # single IP
python main.py google.com        # domain (includes WHOIS + DNS)
python main.py 192.168.1.0/24    # network range
```

## Example output

```
[*] Target: google.com
==================================================

--- General ---
  IP        : 142.250.74.46
  Hostname  : google.com
  Network   : Public (Internet)
  Version   : IPv4

--- Location & provider ---
  Country   : United States
  City      : Mountain View
  ISP       : Google LLC

--- WHOIS & DNS ---
  Registrar   : MarkMonitor Inc.
  Registered  : 1997-09-15
  Expires     : 2028-09-14
  A (IP)      : 142.250.74.46
  MX          : 10 smtp.google.com.

--- Open ports ---
  PORT     SERVICE         BANNER
  ------------------------------------------------------------
  80       HTTP            —
  443      HTTPS           —
```

## Project structure

The project is split into modules under `scanner/` — each one handles a different type of lookup (ports, geolocation, WHOIS, DNS). `main.py` ties them together and runs everything based on the input type.

## Dependencies

socket, concurrent.futures, ipaddress (standard library), plus requests, python-whois, and dnspython (in requirements.txt).

## Legal

Only use this on networks and systems you have permission to scan.
