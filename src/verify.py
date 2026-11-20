"""Deterministic checks: each returns a flag dict (or None)."""

def flag(severity, claim, status, evidence):
    return {"severity": severity, "claim": claim["text"], "status": status, "evidence": evidence}


def check_claim(claim, records, note_time):
    t = claim["type"]
    if t == "lab_pending":
        for lab in records["labs"]:
            if lab["test"].lower() == claim["test"].lower() and lab["status"] == "final":
                return flag("HIGH", claim, "Outdated",
                            f'{lab["test"]} resulted {lab["resulted_at"][-5:]} (Lab, {lab["id"]}), '
                            f'{lab["value"]}. Note written {note_time[-5:]}.')
        return flag("INFO", claim, "Still pending", "No final result found in lab records.")
    if t == "medication":
        for med in records["medications"]:
            if med["drug"].lower() == claim["drug"].lower():
                if med["dose_mg"] != claim["dose_mg"] or med["frequency"] != claim["frequency"]:
                    return flag("MEDIUM", claim, "Contradiction",
                                f'{med["source"]} ({med["id"]}) says {med["dose_mg"]:g} mg {med["frequency"]}, '
                                f'note says {claim["dose_mg"]:g} mg {claim["frequency"]}.')
                return flag("OK", claim, "Verified", f'Matches {med["source"]} ({med["id"]}).')
        return flag("MEDIUM", claim, "Unsupported", "No matching medication record found.")
    if t == "allergy":
        for a in records["allergies"]:
            if a["substance"].lower() == claim["substance"].lower():
                return flag("OK", claim, "Verified", f'{a["source"]} record {a["id"]}, {a["recorded_at"][-5:]}.')
        return flag("HIGH", claim, "Unsupported", "No allergy record found.")
    if t == "task":
        for task in records["tasks"]:
            if task["task"].lower() in claim["text"].lower():
                if task["ack"] == "unseen":
                    return flag("MEDIUM", claim, "Not acknowledged",
                                f'Owner: {task["owner"]}, due {task["due"]}, receiving team: unseen.')
                return flag("OK", claim, "Acknowledged", f'Status: {task["ack"]}.')
        return flag("MEDIUM", claim, "Unsupported", "No matching task record found.")
    return None
