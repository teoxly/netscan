from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PortResult:
    port: int
    is_open: bool
    service: Optional[str] = None
    banner: Optional[str] = None


@dataclass
class HostInfo:
    target: str
    resolved_ip: Optional[str] = None
    hostname: Optional[str] = None
    os_guess: Optional[str] = None
    whois: Optional[str] = None
    dns_records: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ScanResult:
    target: str
    host_info: HostInfo
    ports: List[PortResult] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)