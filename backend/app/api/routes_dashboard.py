from fastapi import APIRouter, Depends
from sqlmodel import Session
from sqlmodel import select
from app.db.session import get_session
from app.db.models import DecisionCase
from sqlmodel import Session
from app.db.session import engine

router = APIRouter()


@router.get("/stats")
def get_dashboard_stats():

    with Session(engine) as session:
        cases = session.exec(select(DecisionCase)).all()

    total = len(cases)

    approve = 0
    reject = 0
    manual = 0

    for c in cases:

        decision = eval(c.decision_output_json)["decision"]

        if decision == "APPROVE":
            approve += 1
        elif decision == "REJECT":
            reject += 1
        else:
            manual += 1

    return {
        "total_cases": total,
        "approve": approve,
        "reject": reject,
        "manual_review": manual
    }