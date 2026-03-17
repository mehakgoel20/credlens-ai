from app.services.rag_pipeline import RAGPipeline

rag = RAGPipeline()

KEYWORDS = {
    "HIGH_DTI": ["DTI", "> 0.50", "Reject", "threshold"],
    "LOW_CREDIT_HISTORY": ["Credit history", "< 12", "Manual Review", "months"],
    "MULTIPLE_EXISTING_LOANS": ["existing_loans", "existing loans", "Manual Review", "Reject", ">= 3", ">= 5"],
    "LOW_EMPLOYMENT_STABILITY": ["employment", "12 months", "current job", "stability"],
}

QUERIES = {
    "HIGH_DTI": "DTI > 0.50 reject rule",
    "LOW_CREDIT_HISTORY": "credit history less than 12 months manual review rule",
    "MULTIPLE_EXISTING_LOANS": "existing loans >=3 manual review >=5 reject rule",
    "LOW_EMPLOYMENT_STABILITY": "minimum employment stability 12 months current job rule",
}

def score_chunk(chunk_text: str, reason_code: str) -> int:
    text = chunk_text.lower()
    score = 0
    for kw in KEYWORDS.get(reason_code, []):
        if kw.lower() in text:
            score += 1
    return score

def verify_and_fix_evidence(decision_output: dict):
    reasons = decision_output.get("reasons", [])
    fixed_reasons = []

    for r in reasons:
        reason_code = r.get("reason_code", "UNKNOWN")
        reason_text = r.get("reason_text", "")

        query = QUERIES.get(reason_code, reason_text)
        candidates = rag.retrieve(query=query, top_k=5)

        # Pick chunk with best keyword match
        best = None
        best_score = -1
        for c in candidates:
            s = score_chunk(c.get("chunk_text", ""), reason_code)
            if s > best_score:
                best_score = s
                best = c

        if best and best.get("metadata"):
            meta = best["metadata"]
            fixed_reasons.append({
                "reason_code": reason_code,
                "reason_text": reason_text,
                "evidence": {
                    "chunk_index": meta.get("chunk_index", -1),
                    "source": meta.get("source", "unknown")
                }
            })
        else:
            fixed_reasons.append(r)

    decision_output["reasons"] = fixed_reasons
    return decision_output
