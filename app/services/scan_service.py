from scanner.input_parser import parse_target
from scanner.port_scanner import scan_ports, get_default_ports
from scanner.ip_info import get_ip_info
from scanner.whois_dns import get_full_info
from scanner.logger import get_logger

logger = get_logger(__name__)

SCAN_STORAGE = {}


def run_scan_job(scan_id: str, target: str, ports=None, timeout: float = 1.0, concurrency: int = 100):
    logger.info("Starting scan %s for %s", scan_id, target)

    try:
        parsed_targets = parse_target(target)
        results = []

        for parsed in parsed_targets:
            ports_to_scan = ports or get_default_ports()

            ip_info = get_ip_info(parsed.ip)
            whois_info, dns_info = (None, None)

            if parsed.hostname:
                whois_info, dns_info = get_full_info(parsed.hostname)

            open_ports = scan_ports(parsed.ip, ports_to_scan, max_threads=concurrency)

            result = {
                "target": parsed.raw_input,
                "host_info": {
                    "target": parsed.raw_input,
                    "resolved_ip": parsed.ip,
                    "hostname": parsed.hostname,
                    "os_guess": None,
                    "whois": None if not whois_info else {
                        "registrar": whois_info.registrar,
                        "creation_date": whois_info.creation_date,
                        "expiration_date": whois_info.expiration_date,
                        "name_servers": whois_info.name_servers,
                    },
                    "dns_records": {} if not dns_info else {
                        "a_records": dns_info.a_records,
                        "mx_records": dns_info.mx_records,
                        "ns_records": dns_info.ns_records,
                        "txt_records": dns_info.txt_records,
                    },
                },
                "ports": open_ports,
                "metadata": {
                    "timeout": timeout,
                    "concurrency": concurrency,
                    "ip_info": None if ip_info is None else {
                        "ip": ip_info.ip,
                        "country": ip_info.country,
                        "city": ip_info.city,
                        "region": ip_info.region,
                        "isp": ip_info.isp,
                        "org": ip_info.org,
                        "lat": ip_info.lat,
                        "lon": ip_info.lon,
                        "timezone": ip_info.timezone,
                    },
                },
            }
            results.append(result)

        SCAN_STORAGE[scan_id] = {
            "status": "done",
            "results": results,
        }

        logger.info("Scan %s finished successfully", scan_id)

    except ValueError as e:
        logger.error("Scan %s failed — invalid target: %s", scan_id, e)
        SCAN_STORAGE[scan_id] = {
            "status": "error",
            "error": f"Target invalid: {e}",
            "results": None,
        }

    except Exception as e:
        logger.exception("Scan %s failed with unexpected error: %s", scan_id, e)
        SCAN_STORAGE[scan_id] = {
            "status": "error",
            "error": f"Eroare internă: {type(e).__name__}: {e}",
            "results": None,
        }


def create_scan(scan_id: str, target: str, ports=None, timeout: float = 1.0, concurrency: int = 100):
    SCAN_STORAGE[scan_id] = {"status": "running", "results": None}
    return scan_id


def get_scan(scan_id: str):
    return SCAN_STORAGE.get(scan_id)


def get_all_scans():
    return [
        {"scan_id": scan_id, **scan_data}
        for scan_id, scan_data in SCAN_STORAGE.items()
    ]