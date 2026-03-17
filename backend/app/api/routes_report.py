from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlmodel import Session
from app.db.session import get_session
from app.db.models import DecisionCase
from app.services.report_generator import generate_case_report
import json
import os

router = APIRouter()

@router.get("/{case_id}")
def download_report(
    case_id: int,
    session: Session = Depends(get_session)
):
    case = session.get(DecisionCase, case_id)

    if not case:
        return {"error": "case not found"}

    case_data = {
        "applicant": json.loads(case.applicant_json),
        "risk_output": json.loads(case.risk_output_json),
        "decision_output": json.loads(case.decision_output_json),
    }

    os.makedirs("reports", exist_ok=True)
    out_path = f"reports/case_{case_id}_report.pdf"

    generate_case_report(case_id=case_id, case_data=case_data, out_path=out_path)

    return FileResponse(
        out_path,
        media_type="application/pdf",
        filename=f"CredLens_Case_{case_id}_Report.pdf"
    )
