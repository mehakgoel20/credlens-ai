from fastapi import APIRouter
from sqlmodel import select
from app.db.session import get_session
from app.db.models import DecisionCase
import json

router = APIRouter()

@router.get("/cases")
def list_cases(limit: int = 10):
    session = get_session()
    cases = session.exec(select(DecisionCase).order_by(DecisionCase.id.desc()).limit(limit)).all()

    return [
        {
            "case_id": c.id,
            "created_at": c.created_at,
            "applicant": json.loads(c.applicant_json),
            "risk_output": json.loads(c.risk_output_json),
            "decision_output": json.loads(c.decision_output_json)
        }
        for c in cases
    ]

@router.get("/cases/{case_id}")
def get_case(case_id: int):
    session = get_session()
    case = session.get(DecisionCase, case_id)

    if not case:
        return {"error": "case not found"}

    return {
        "case_id": case.id,
        "created_at": case.created_at,
        "applicant": json.loads(case.applicant_json),
        "risk_output": json.loads(case.risk_output_json),
        "decision_output": json.loads(case.decision_output_json)
    }
