import json
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import select

from app.core.security import require_api_key
from app.db.session import get_session
from app.db.models import DecisionCase

from app.services.rag_pipeline import RAGPipeline
from app.services.risk_model import ml_risk_score
from app.services.decision_agent import generate_decision
from app.services.evidence_verifier import verify_and_fix_evidence

from app.utils.audit_hash import compute_case_hash
from app.services.citation_verifier import compute_grounding_score

router = APIRouter()
rag = RAGPipeline()


# -----------------------------
# Request Schema
# -----------------------------
class ApplicantData(BaseModel):
    monthly_income: float
    monthly_emi: float
    credit_history_years: float
    existing_loans: int
    employment_years: float


# -----------------------------
# Deterministic decision gates
# -----------------------------
def policy_gate_decision(applicant: dict, risk_output: dict):
    """
    Tier-1 rule gating:
    - DTI > 0.50 => REJECT
    - DTI <= 0.35 and credit history >= 1y and existing loans < 3 => APPROVE
    - else => MANUAL_REVIEW
    """

    dti = risk_output["dti"]

    # Hard Reject
    if dti > 0.50:
        return "REJECT", "DTI > 0.50 (policy hard reject)"

    # Hard Approve (clearly eligible)
    if (
        dti <= 0.35
        and applicant["credit_history_years"] >= 1
        and applicant["existing_loans"] < 3
    ):
        return "APPROVE", "DTI <= 0.35 and credit history >= 12 months with low existing loans"

    # Everything else: manual review
    return "MANUAL_REVIEW", "Borderline policy conditions require manual underwriting review"


def calibrate_confidence(decision: str, dti: float):
    """
    Confidence calibration (simple but meaningful):
    farther from boundaries => higher confidence.
    """

    if decision == "REJECT":
        # if dti is barely above 0.50, slightly lower confidence
        if dti < 0.55:
            return 0.80
        return 0.90

    if decision == "APPROVE":
        # if dti is close to 0.35 boundary, slightly lower confidence
        if dti > 0.30:
            return 0.80
        return 0.85

    # manual review is always moderate confidence
    return 0.60


# -----------------------------
# Main API
# -----------------------------
@router.post("/", dependencies=[Depends(require_api_key)])
def make_decision(data: ApplicantData):
    applicant = data.model_dump()

    # 1) Risk scoring (ML with fallback to rules)
    risk_output = ml_risk_score(applicant)
    dti = risk_output["dti"]

    # 2) Retrieve policy chunks (RAG)
    policy_query = (
        "Loan approval policy rules: DTI thresholds, credit history requirements, "
        "employment stability criteria, existing loans criteria, approve reject manual review rules"
    )
    policy_chunks = rag.retrieve(query=policy_query, top_k=5)

    # 3) Deterministic policy gate decides final decision
    forced_decision, forced_reason = policy_gate_decision(applicant, risk_output)

    # 4) LLM is ONLY used to generate explanation JSON (not final authority)
    #    We pass forced_decision so it follows deterministic output.
    # 4) LLM explanation generation (safe fallback)

    llm_status = "success"

    try:

        decision_output = generate_decision(
            applicant_data=applicant,
            policy_context=policy_chunks,
            risk_output={
                **risk_output,
                "forced_decision": forced_decision,
                "forced_reason": forced_reason
            }
        )

    except Exception as e:

        print("LLM FAILURE:", e)

        llm_status = "unavailable"

        decision_output = {
            "decision": forced_decision,
            "confidence": None,
            "reasons": [{
                "reason_code": "LLM_UNAVAILABLE",
                "reason_text": forced_reason,
                "evidence": {
                    "chunk_index": policy_chunks[0]["metadata"].get("chunk_index", -1) if policy_chunks else -1,
                    "source": policy_chunks[0]["metadata"].get("source", "unknown") if policy_chunks else "unknown"
                }
            }]
        }

    # 5) Evidence verifier (fix wrong chunk citations)
    decision_output = verify_and_fix_evidence(decision_output)
    grounding_score = compute_grounding_score(decision_output, policy_chunks)

    # 6) Override decision to ensure strict determinism
    decision_output["decision"] = forced_decision

    # 7) Ensure at least one reason exists
    if not decision_output.get("reasons"):
        decision_output["reasons"] = [{
            "reason_code": "FORCED_DECISION",
            "reason_text": forced_reason,
            "evidence": {
                "chunk_index": policy_chunks[0]["metadata"].get("chunk_index", -1) if policy_chunks else -1,
                "source": policy_chunks[0]["metadata"].get("source", "unknown") if policy_chunks else "unknown"
            }
        }]

    # 8) Calibrate confidence
    decision_output["confidence"] = calibrate_confidence(forced_decision, dti)

    # 9) Audit logging with tamper-evident hash chaining
    session = next(get_session())

    last_case = session.exec(
        select(DecisionCase).order_by(DecisionCase.id.desc())
    ).first()

    prev_hash = last_case.case_hash if last_case else "GENESIS"
    

    case = DecisionCase(
        applicant_json=json.dumps(applicant),
        risk_output_json=json.dumps(risk_output),
        decision_output_json=json.dumps(decision_output),
        policy_version="loan_policy_v1",
        rules_version="rules_2026_01",
        prev_hash=prev_hash,
        status="PENDING_REVIEW",
        grounding_score=grounding_score,
        reviewer=""
    )

    # persist case: compute hash, commit, and always close session
    try:
        case.case_hash = compute_case_hash(
            prev_hash=case.prev_hash,
            applicant_json=case.applicant_json,
            risk_json=case.risk_output_json,
            decision_json=case.decision_output_json
        )

        session.add(case)
        session.commit()
        session.refresh(case)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

    return {
        "case_id": case.id,
        "case_hash": case.case_hash,
        "prev_hash": case.prev_hash,
        "applicant": applicant,
        "risk_output": risk_output,
        "decision_output": decision_output,
        "grounding_score": grounding_score,
        "llm_status": llm_status
    }