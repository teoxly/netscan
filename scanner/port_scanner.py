"""
port_scanner.py
---------------
Responsabilitate: încearcă să se conecteze la fiecare port al unui IP
și raportează care sunt deschise și ce serviciu rulează pe ele.
"""

import socket
import concurrent.futures

# -----------------------------------------------------------------------
# Un dicționar simplu: număr port → nume serviciu
# Când găsim portul 80 deschis, știm să afișăm "HTTP" în loc de "80"
# -----------------------------------------------------------------------
COMMON_SERVICES = {
    21:   "FTP",
    22:   "SSH",
    23:   "Telnet",
    25:   "SMTP",
    53:   "DNS",
    80:   "HTTP",
    110:  "POP3",
    143:  "IMAP",
    443:  "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-alt",
    8443: "HTTPS-alt",
    27017:"MongoDB",
}


def grab_banner(sock) -> str | None:
    """
    După ce ne-am conectat la un port, încercăm să citim primul mesaj
    pe care ni-l trimite serverul. Acesta se numește "banner".

    De exemplu, SSH-ul răspunde cu ceva de genul:
        "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3"

    Din banner putem afla versiunea software-ului care rulează.
    Dacă serverul nu trimite nimic în 2 secunde, returnăm None.
    """
    try:
        sock.settimeout(2)
        banner = sock.recv(1024)         # citim maxim 1024 bytes
        return banner.decode().strip()   # transformăm bytes în text
    except Exception:
        return None                      # serverul n-a trimis nimic, e ok


def scan_port(ip: str, port: int, timeout: float = 1.0) -> dict | None:
    """
    Încearcă să se conecteze la un singur port.

    Returnează un dicționar cu informații dacă portul e deschis:
        { "port": 22, "service": "SSH", "banner": "SSH-2.0-OpenSSH..." }

    Returnează None dacă portul e închis sau nu răspunde.
    """

    # Creăm un "socket" — practic un telefon cu care sunăm la server
    # AF_INET    = folosim IPv4
    # SOCK_STREAM = folosim TCP (conexiune stabilă, nu UDP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)  # dacă nu răspunde în 1 secundă, renunțăm

    try:
        # connect_ex() încearcă conexiunea și returnează:
        #   0       → conexiune reușită (portul e deschis)
        #   altceva → portul e închis sau filtrat
        result = sock.connect_ex((ip, port))

        if result == 0:
            # Portul e deschis! Citim banner-ul și returnăm informațiile.
            banner = grab_banner(sock)
            return {
                "port":    port,
                "service": COMMON_SERVICES.get(port, "unknown"),
                "banner":  banner,
            }
        return None  # portul e închis

    except Exception:
        return None  # ceva a mers prost, tratăm ca închis

    finally:
        # "finally" rulează ÎNTOTDEAUNA, indiferent dacă a apărut o eroare
        # Închidem socket-ul ca să nu lăsăm conexiuni deschise
        sock.close()


def scan_ports(ip: str, ports: list[int], max_threads: int = 100) -> list[dict]:
    """
    Scanează o listă de porturi în paralel folosind threading.

    max_threads = câți "chelneri" lucrează simultan.
    100 e un număr bun — destul de rapid fără să supraîncarce rețeaua.
    """

    open_ports = []  # lista în care colectăm porturile deschise

    # ThreadPoolExecutor creează automat pool-ul de thread-uri
    # "with" se asigură că toate thread-urile se termină înainte să continuăm
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:

        # "submit" trimite fiecare port la un thread disponibil
        # future = o "promisiune" că rezultatul va veni când thread-ul termină
        futures = {
            executor.submit(scan_port, ip, port): port
            for port in ports
        }

        # as_completed() ne dă rezultatele PE MĂSURĂ ce thread-urile termină
        # (nu în ordinea în care le-am trimis, ci în ordinea în care termină)
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result is not None:           # None = portul era închis
                open_ports.append(result)

    # Sortăm după numărul portului ca să fie mai ușor de citit
    return sorted(open_ports, key=lambda x: x["port"])


def get_default_ports() -> list[int]:
    """
    Returnează lista porturilor pe care le scanăm implicit.
    Sunt cele mai comune — un scan rapid și relevant.
    """
    return list(COMMON_SERVICES.keys())