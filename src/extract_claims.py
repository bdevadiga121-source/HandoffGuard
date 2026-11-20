"""Split a handover note into checkable claims (simple rule-based version).
An LLM can replace this later; the output format stays the same."""
import re

DOSE = re.compile(r"(?P<drug>[A-Za-z]+)\s+(?P<amt>\d+(?:\.\d+)?)\s*(?P<unit>mg|g)\s+(?P<freq>q\d+h)", re.I)


def extract_claims(note):
    claims = []
    for sentence in [s.strip() for s in note.split(".") if s.strip()]:
        low = sentence.lower()
        m = DOSE.search(sentence)
        if "allergy" in low:
            claims.append({"type": "allergy", "text": sentence,
                           "substance": sentence.split()[0]})
        elif "pending" in low:
            claims.append({"type": "lab_pending", "text": sentence,
                           "test": sentence.split()[0]})
        elif m:
            mg = float(m["amt"]) * (1000 if m["unit"].lower() == "g" else 1)
            claims.append({"type": "medication", "text": sentence,
                           "drug": m["drug"], "dose_mg": mg, "frequency": m["freq"]})
        elif low.startswith("repeat"):
            claims.append({"type": "task", "text": sentence})
    return claims
