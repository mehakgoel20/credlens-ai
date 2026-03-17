from fpdf import FPDF
from datetime import datetime

def generate_case_report(case_id: int, case_data: dict, out_path: str):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_left_margin(15)
    pdf.set_right_margin(15)
    pdf.set_top_margin(15)

    usable_width = pdf.w - pdf.l_margin - pdf.r_margin

    pdf.set_font("Helvetica", size=14)
    pdf.cell(0, 10, "CredLens AI - Credit Decision Report", ln=True)

    pdf.set_font("Helvetica", size=11)
    pdf.cell(0, 8, f"Case ID: {case_id}", ln=True)
    pdf.cell(0, 8, f"Generated At: {datetime.utcnow().isoformat()} UTC", ln=True)
    pdf.ln(5)

    applicant = case_data["applicant"]
    risk = case_data["risk_output"]
    decision = case_data["decision_output"]

    def safe_line(text: str):
        # ✅ sanitize unsupported unicode
        text = (
            text.replace("–", "-")
                .replace("₹", "Rs.")
                .replace("→", "->")
                .replace("≤", "<=")
                .replace("≥", ">=")
        )
        text = text.encode("latin-1", "ignore").decode("latin-1")

        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(usable_width, 6, text)

    # Applicant Summary
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Applicant Summary", ln=True)

    pdf.set_font("Helvetica", size=11)
    safe_line(f"- Monthly Income: {applicant.get('monthly_income')}")
    safe_line(f"- Monthly EMI: {applicant.get('monthly_emi')}")
    safe_line(f"- Credit History (years): {applicant.get('credit_history_years')}")
    safe_line(f"- Existing Loans: {applicant.get('existing_loans')}")
    safe_line(f"- Employment (years): {applicant.get('employment_years')}")
    pdf.ln(4)

    # Risk Output
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Risk Output", ln=True)

    pdf.set_font("Helvetica", size=11)
    safe_line(f"- Risk Score: {risk.get('risk_score')}")
    safe_line(f"- Risk Bucket: {risk.get('risk_bucket')}")
    safe_line(f"- DTI: {risk.get('dti')}")
    safe_line(f"- Reason Codes: {', '.join(risk.get('reason_codes', []))}")
    pdf.ln(4)

    # Final Decision
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Final Decision", ln=True)

    pdf.set_font("Helvetica", size=11)
    safe_line(f"- Decision: {decision.get('decision')}")
    safe_line(f"- Confidence: {decision.get('confidence', 0)}")
    pdf.ln(4)

    # Reasons
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Decision Reasons (with Evidence)", ln=True)

    pdf.set_font("Helvetica", size=11)
    reasons = decision.get("reasons", [])

    if not reasons:
        safe_line("- No reasons provided")
    else:
        for r in reasons:
            ev = r.get("evidence", {})
            reason_code = r.get("reason_code", "N/A")
            reason_text = r.get("reason_text", "N/A")
            chunk_index = ev.get("chunk_index", "N/A")
            source = ev.get("source", "N/A")

            safe_line(f"- {reason_code}: {reason_text}")
            safe_line(f"  Evidence: chunk_index={chunk_index}, source={source}")
            pdf.ln(1)

    pdf.ln(2)

    # Next Steps
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Next Steps", ln=True)

    pdf.set_font("Helvetica", size=11)
    next_steps = decision.get("next_steps", [])

    if not next_steps:
        safe_line("- No next steps")
    else:
        for step in next_steps:
            safe_line(f"- {step}")

    pdf.output(out_path)
    return out_path
