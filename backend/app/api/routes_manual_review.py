from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.db.session import get_session
from app.db.models import DecisionCase
from app.core.security import require_api_key
import json

router = APIRouter()

class AssignReviewer(BaseModel):
    reviewer: str

class ResolveReview(BaseModel):
    final_decision: str  # APPROVE/REJECT
    notes: str = ""

@router.post("/assign/{case_id}", dependencies=[Depends(require_api_key)])
def assign(case_id: int, data: AssignReviewer):
    session = get_session()
    case = session.get(DecisionCase, case_id)
    if not case:
        return {"error": "case not found"}

    case.reviewer = data.reviewer
    case.status = "PENDING_REVIEW"
    session.add(case)
    session.commit()
    return {"case_id": case.id, "status": case.status, "reviewer": case.reviewer}

@router.post("/resolve/{case_id}", dependencies=[Depends(require_api_key)])
def resolve(case_id: int, data: ResolveReview):
    session = get_session()
    case = session.get(DecisionCase, case_id)
    if not case:
        return {"error": "case not found"}

    decision = json.loads(case.decision_output_json)
    decision["decision"] = data.final_decision
    decision["review_notes"] = data.notes
    decision["confidence"] = 0.95

    case.decision_output_json = json.dumps(decision)
    case.status = "APPROVED" if data.final_decision == "APPROVE" else "REJECTED"

    session.add(case)
    session.commit()
    return {"case_id": case.id, "status": case.status, "final_decision": data.final_decision}
