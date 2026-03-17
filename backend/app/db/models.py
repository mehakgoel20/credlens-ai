from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import json
class PolicyDoc(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    doc_hash: str
    doc_name: str
    policy_version: str = "policy_v1"
    rules_version: str = "rules_v1"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    grounding_score: Optional[float] = None

    
class DecisionCase(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    applicant_json: str
    risk_output_json: str
    decision_output_json: str

    prev_hash: str = ""
    case_hash: str = ""
    status: str = "PENDING_REVIEW"
    reviewer: str = ""

    def set_applicant(self, d: dict):
        self.applicant_json = json.dumps(d)

    def set_risk_output(self, d: dict):
        self.risk_output_json = json.dumps(d)

    def set_decision_output(self, d: dict):
        self.decision_output_json = json.dumps(d)
