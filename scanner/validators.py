import ipaddress
import re
from .config import MAX_PORT, MIN_PORT
from .exceptions import InvalidTargetError

HOSTNAME_REGEX = re.compile(
    r"^(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z]{2,63}$"
)

def validate_ip_or_network(value: str):
    try:
        if "/" in value:
            return ipaddress.ip_network(value, strict=False)
        return ipaddress.ip_address(value)
    except ValueError as exc:
        raise InvalidTargetError(f"Invalid IP/network: {value}") from exc

def validate_hostname(value: str) -> str:
    if not HOSTNAME_REGEX.match(value):
        raise InvalidTargetError(f"Invalid hostname: {value}")
    return value

def validate_target(value: str) -> str:
    value = value.strip()
    try:
        validate_ip_or_network(value)
        return value
    except InvalidTargetError:
        return validate_hostname(value)

def validate_port(port: int) -> int:
    if not isinstance(port, int):
        raise InvalidTargetError("Port must be an integer")
    if port < MIN_PORT or port > MAX_PORT:
        raise InvalidTargetError(f"Port must be between {MIN_PORT} and {MAX_PORT}")
    return port

def validate_port_range(start: int, end: int):
    validate_port(start)
    validate_port(end)
    if start > end:
        raise InvalidTargetError("Start port must be <= end port")
    return start, end