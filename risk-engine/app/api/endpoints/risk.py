from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import random

router = APIRouter()

class IdentityRiskRequest(BaseModel):
    name: str
    age_days: int
    last_used_days: int
    permission_count: int
    has_mfa: bool
    is_service_account: bool
    access_frequency: int

class RiskResponse(BaseModel):
    identity_name: str
    risk_score: float
    risk_level: str
    factors: List[str]

@router.post("/predict", response_model=RiskResponse)
async def predict_risk(identity: IdentityRiskRequest):
    """
    Predict risk score for an identity.
    Uses a rule-based system for demo purposes.
    """
    risk_score = 0.0
    factors = []
    
    # Age factor - older accounts are riskier
    if identity.age_days > 365:
        risk_score += 0.3
        factors.append("Account is over 1 year old")
    elif identity.age_days > 180:
        risk_score += 0.15
        factors.append("Account is over 6 months old")
    
    # Last used factor - unused accounts are riskier
    if identity.last_used_days > 90:
        risk_score += 0.3
        factors.append("Account not used in over 90 days")
    elif identity.last_used_days > 30:
        risk_score += 0.15
        factors.append("Account not used in over 30 days")
    
    # Permission factor - more permissions = more risk
    if identity.permission_count > 20:
        risk_score += 0.3
        factors.append(f"Account has {identity.permission_count} permissions (excessive)")
    elif identity.permission_count > 10:
        risk_score += 0.15
        factors.append(f"Account has {identity.permission_count} permissions")
    
    # MFA factor - no MFA is risky
    if not identity.has_mfa:
        risk_score += 0.2
        factors.append("MFA is not enabled")
    
    # Service account factor
    if identity.is_service_account:
        risk_score += 0.1
        factors.append("Service account with potential excessive permissions")
    
    # Normalize to 0-1
    risk_score = min(1.0, risk_score)
    
    # Determine risk level
    if risk_score < 0.3:
        risk_level = "LOW"
    elif risk_score < 0.6:
        risk_level = "MEDIUM"
    elif risk_score < 0.8:
        risk_level = "HIGH"
    else:
        risk_level = "CRITICAL"
    
    return RiskResponse(
        identity_name=identity.name,
        risk_score=round(risk_score, 3),
        risk_level=risk_level,
        factors=factors
    )

@router.post("/batch-predict")
async def batch_predict(identities: List[IdentityRiskRequest]):
    """
    Predict risk scores for multiple identities.
    """
    results = []
    for identity in identities:
        result = await predict_risk(identity)
        results.append(result.dict())
    
    return {
        "total_processed": len(results),
        "results": results
    }

@router.get("/status")
async def risk_status():
    return {
        "status": "ok",
        "model_type": "rule-based",
        "version": "1.0.0"
    }
