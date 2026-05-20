from fastapi import APIRouter, BackgroundTasks, HTTPException
from uuid import uuid4

from app.schemas.scan import ScanRequest
from app.services.scan_service import create_scan, run_scan_job, get_scan, get_all_scans

router = APIRouter()


@router.post("")
def start_scan(payload: ScanRequest, background_tasks: BackgroundTasks):
    scan_id = str(uuid4())
    create_scan(scan_id, payload.target, payload.ports, payload.timeout, payload.concurrency)
    background_tasks.add_task(
        run_scan_job,
        scan_id,
        payload.target,
        payload.ports,
        payload.timeout,
        payload.concurrency,
    )
    return {"scan_id": scan_id, "status": "running"}


@router.get("")
def list_scans():
    return get_all_scans()


@router.get("/{scan_id}")
def scan_status(scan_id: str):
    scan = get_scan(scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan