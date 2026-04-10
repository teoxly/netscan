# Network Scanner

Un tool de scanare a rețelei scris în Python, inspirat de nmap.
Oferă informații despre IP-uri și domenii: porturi deschise, locație geografică, date WHOIS și înregistrări DNS.

## Funcționalități

- **Port Scanner** — scanează porturile TCP comune în paralel (threading) și detectează serviciile care rulează
- **IP Info** — locație geografică, ISP și organizație via ip-api.com
- **WHOIS** — registrar, data înregistrării și expirării domeniului
- **DNS** — înregistrări A, MX, NS, TXT
- **Input flexibil** — acceptă IP, domeniu sau range CIDR (ex: 192.168.1.0/24)

## Instalare

```bash
git clone https://github.com/username/network-scanner.git
cd network-scanner
pip install -r requirements.txt
```

## Utilizare

```bash
# Scanează un IP
python main.py 8.8.8.8

# Scanează un domeniu (include WHOIS și DNS)
python main.py google.com

# Scanează un range de rețea
python main.py 192.168.1.0/24
```

## Exemplu output

```
[*] Target: google.com

==================================================

--- Informatii generale ---
  IP        : 142.250.74.46
  Hostname  : google.com
  Tip retea : Public (Internet)
  Versiune  : IPv4

--- Locatie si provider ---
  Tara      : United States
  Oras      : Mountain View
  ISP       : Google LLC

--- WHOIS si DNS ---
  Registrar   : MarkMonitor Inc.
  Inregistrat : 1997-09-15
  Expira      : 2028-09-14
  A (IP)      : 142.250.74.46
  MX          : 10 smtp.google.com.

--- Porturi ---
  PORT     SERVICIU        BANNER
  ------------------------------------------------------------
  80       HTTP            —
  443      HTTPS           —
```

## Structura proiectului

```
network-scanner/
├── scanner/
│   ├── input_parser.py   # validare și parsare input (IP, domeniu, CIDR)
│   ├── port_scanner.py   # scanare TCP cu threading
│   ├── ip_info.py        # locație geografică via ip-api.com
│   └── whois_dns.py      # date WHOIS și înregistrări DNS
├── main.py               # punctul de intrare, orchestrează modulele
└── requirements.txt
```

## Tehnologii folosite

- `socket` — conexiuni TCP pentru port scanning
- `concurrent.futures` — threading pentru scanare paralelă
- `ipaddress` — validare și parsare IP/CIDR
- `requests` — HTTP requests către ip-api.com
- `python-whois` — interogare WHOIS
- `dnspython` — interogare DNS

## Note legale

Folosește acest tool doar pe rețele și sisteme pentru care ai permisiune explicită. Scanarea neautorizată poate fi ilegală.