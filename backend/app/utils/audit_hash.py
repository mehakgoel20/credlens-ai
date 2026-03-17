import hashlib

def sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def compute_case_hash(prev_hash: str, applicant_json: str, risk_json: str, decision_json: str) -> str:
    payload = prev_hash + applicant_json + risk_json + decision_json
    return sha256(payload)
