import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a fintech credit risk decision assistant.

You MUST follow these rules:
1) Use only the provided policy_context and applicant_data and risk_output.
2) If risk_output contains forced_decision, you MUST set decision = forced_decision.
3) Every reason must cite evidence from policy_context using chunk_index and source from metadata.
4) If policy evidence is missing, still follow forced_decision but add missing_info.
5) Return STRICT JSON ONLY in the given schema. No extra text.

Schema:
{
  "decision": "APPROVE|REJECT|MANUAL_REVIEW",
  "confidence": 0.0,
  "reasons": [
    {
      "reason_code": "STRING",
      "reason_text": "STRING",
      "evidence": { "chunk_index": INT, "source": "STRING" }
    }
  ],
  "missing_info": ["STRING"],
  "next_steps": ["STRING"]
}
"""

def generate_decision(applicant_data: dict, policy_context: list, risk_output: dict):
    user_payload = {
        "applicant_data": applicant_data,
        "risk_output": risk_output,
        "policy_context": policy_context
    }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(user_payload)}
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except Exception:
        return {
            "decision": risk_output.get("forced_decision") or "MANUAL_REVIEW",
            "confidence": 0.2,
            "reasons": [
                {
                    "reason_code": "FORMAT_ERROR",
                    "reason_text": "LLM did not return valid JSON. Manual review required.",
                    "evidence": {"chunk_index": -1, "source": "N/A"}
                }
            ],
            "missing_info": ["Valid structured JSON response"],
            "next_steps": ["Retry request", "Check logs"]
        }
