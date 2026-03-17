import re


def compute_grounding_score(decision_output, policy_chunks):
    """
    Verifies that cited evidence appears in retrieved policy chunks.
    Returns score between 0 and 1.
    """

    reasons = decision_output.get("reasons", [])

    if not reasons:
        return 0.0

    matches = 0
    total = len(reasons)

    for r in reasons:

        evidence = r.get("evidence", {})
        idx = evidence.get("chunk_index")

        if idx is None:
            continue

        if idx < len(policy_chunks):

            chunk_text = policy_chunks[idx]["chunk_text"]
            reason_text = r.get("reason_text", "")

            keywords = re.findall(r"\w+", reason_text.lower())

            overlap = any(word in chunk_text.lower() for word in keywords)

            if overlap:
                matches += 1

    return matches / total