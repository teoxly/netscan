from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ScanRequest(BaseModel):
    target: str = Field(..., examples=["google.com", "8.8.8.8", "192.168.1.0/24"])
    ports: Optional[List[int]] = None
    timeout: float = 1.0
    concurrency: int = 100


class PortResult(BaseModel):
    port: int
    service: str
    banner: Optional[str] = None


class HostInfo(BaseModel):
    target: str
    resolved_ip: Optional[str] = None
    hostname: Optional[str] = None
    os_guess: Optional[str] = None
    whois: Optional[str] = None
    dns_records: Dict[str, Any] = {}


class ScanResult(BaseModel):
    target: str
    host_info: HostInfo
    ports: List[PortResult]
    metadata: Dict[str, Any]