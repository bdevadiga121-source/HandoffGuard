# HandoffGuard
Evidence-based patient handover verification
# HandoffGuard

**Evidence-based patient handover verification system**

HandoffGuard checks patient handover notes against the original hospital records before the receiving team accepts them. It links each important statement to its source, flags outdated or conflicting information, and tracks whether pending tasks have been acknowledged.

> Team **Quantum bytes** | Bhoomika, Sharanyaraj

---

## Problem

When patients move between departments (ICU, ER, general ward), handover notes can contain outdated, incomplete or contradictory information. For example, a note may say a lab test is "pending" when the result is already in the lab system. Most tools only transfer information faster; none verify that it is correct.

**Target users:** doctors and nurses receiving patients, patient-safety teams and hospital administrators.

## Solution

1. **Claim extraction:** the handover note is split into checkable claims (medication, allergy, lab, pending task, etc.).
2. **Source linking:** every claim is tied to a source record with ID, author and timestamp. Claims with no source are flagged as unsupported.
3. **Currency check:** compares the claim with the latest record (e.g. "pending" lab that now has a result).
4. **Contradiction detection:** compares across records (e.g. two different doses of the same drug) and shows both pieces of evidence side by side.
5. **Task acknowledgment:** each pending task has an owner and a status (unseen, seen, accepted, completed).

### Example output

```
WARNING  Handover says: "CBC pending"
Evidence: CBC resulted 14:32 (Lab system), Hb 9.1 g/dL. Note written 11:05.
Status:   Outdated
Action:   Update the note and review the result.
```

### Design principles

- Safety checks are **rule-based and deterministic**; an LLM is used only to extract claims from free text.
- If a source cannot be reached, the system shows **"could not verify"**, never "no issues found".
- Alerts are **ranked by severity** to avoid alert fatigue.
- The clinician **makes the final decision**; the system never edits records.

## Architecture

```
Handover note -> Claim extraction -> Source linking (FHIR/HL7)
              -> Rule-based checks -> Severity ranking
              -> Clinician review + task acknowledgment
```

Storage: PostgreSQL (claims, evidence links, acknowledgments, audit log).

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | React, Tailwind CSS |
| Backend | Python, FastAPI |
| Database | PostgreSQL, Redis |
| Interoperability | FHIR R4, HL7 v2 |
| AI | LLM API (claim extraction only) |
| Test data | Synthetic data (Synthea) |
| Security | Role-based access, JWT, audit logging |

## Project structure

```
HandoffGuard/
├── README.md
├── requirements.txt
├── data/
│   └── sample_patient.json
├── src/
│   ├── extract_claims.py
│   ├── verify.py
│   └── main.py
└── docs/
    └── wireframe.png
```

## Getting started

```bash
git clone https://github.com/<your-username>/HandoffGuard.git
cd HandoffGuard
pip install -r requirements.txt
python src/main.py
```

The proof of concept reads `data/sample_patient.json` (fake data only) and prints any flagged discrepancies with their evidence.

## Roadmap

- [x] Problem definition and system design
- [ ] Proof of concept: currency check on sample data
- [ ] Contradiction detection (medication doses, allergies)
- [ ] Task acknowledgment tracking
- [ ] Web dashboard
- [ ] FHIR integration with a sandbox server
- [ ] Testing on synthetic handovers

## Privacy note

This project uses **synthetic data only**. Never commit real patient information.

## License

MIT
