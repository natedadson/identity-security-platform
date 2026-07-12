from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid
import asyncio
import random

router = APIRouter()

class ScanRequest(BaseModel):
    provider: str
    regions: Optional[List[str]] = None

class ScanResponse(BaseModel):
    task_id: str
    status: str
    message: str

class ScanStatus(BaseModel):
    scan_id: str
    status: str
    progress: int
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    results: Optional[dict]

# In-memory storage for demo
scan_store = {}

@router.post("/start", response_model=ScanResponse)
async def start_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    """
    Start a new identity scan.
    """
    scan_id = str(uuid.uuid4())
    
    # Store scan record
    scan_store[scan_id] = {
        "id": scan_id,
        "provider": request.provider,
        "status": "pending",
        "progress": 0,
        "started_at": datetime.utcnow(),
        "completed_at": None,
        "results": None
    }
    
    # Add background task
    background_tasks.add_task(simulate_scan, scan_id)
    
    return ScanResponse(
        task_id=scan_id,
        status="accepted",
        message="Scan started successfully"
    )

@router.get("/{scan_id}/status", response_model=ScanStatus)
async def get_scan_status(scan_id: str):
    """
    Get status of a scan.
    """
    scan = scan_store.get(scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    return ScanStatus(
        scan_id=scan_id,
        status=scan["status"],
        progress=scan["progress"],
        started_at=scan["started_at"],
        completed_at=scan["completed_at"],
        results=scan["results"]
    )

@router.get("/", response_model=List[ScanStatus])
async def list_scans():
    """
    List all scans.
    """
    return [
        ScanStatus(
            scan_id=scan_id,
            status=scan["status"],
            progress=scan["progress"],
            started_at=scan["started_at"],
            completed_at=scan["completed_at"],
            results=scan["results"]
        )
        for scan_id, scan in scan_store.items()
    ]

async def simulate_scan(scan_id: str):
    """
    Simulate a scan for demonstration.
    """
    # Update status to running
    scan_store[scan_id]["status"] = "running"
    
    # Simulate progress
    for progress in range(10, 100, 10):
        await asyncio.sleep(0.5)
        scan_store[scan_id]["progress"] = progress
    
    # Complete
    scan_store[scan_id]["status"] = "completed"
    scan_store[scan_id]["progress"] = 100
    scan_store[scan_id]["completed_at"] = datetime.utcnow()
    scan_store[scan_id]["results"] = {
        "identities_found": random.randint(20, 50),
        "high_risk": random.randint(1, 5),
        "medium_risk": random.randint(3, 10),
        "low_risk": random.randint(10, 30)
    }
