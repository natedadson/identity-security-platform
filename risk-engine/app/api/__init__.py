from fastapi import APIRouter
from app.api.endpoints import risk, scans, reports

api_router = APIRouter()

api_router.include_router(risk.router, prefix="/risk", tags=["risk"])
api_router.include_router(scans.router, prefix="/scans", tags=["scans"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
