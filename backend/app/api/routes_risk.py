from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.services.risk_model import ml_risk_score, simple_risk_score
router = APIRouter()

class RiskInput(BaseModel):
    monthly_income: float = Field(..., gt=0)
    monthly_emi: float = Field(..., ge=0)
    credit_history_years: float = Field(..., ge=0)
    existing_loans: int = Field(..., ge=0)
    employment_years: float = Field(..., ge=0)

@router.post("/score")
def score_risk(data: RiskInput):
    result = ml_risk_score(data.model_dump())
    return result
