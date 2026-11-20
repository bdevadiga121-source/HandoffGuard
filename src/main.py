import json
from pathlib import Path
from extract_claims import extract_claims
from verify import check_claim

ORDER = {"HIGH": 0, "MEDIUM": 1, "INFO": 2, "OK": 3}


def main():
    data = json.loads((Path(__file__).parent.parent / "data" / "sample_patient.json").read_text())
    h = data["handover"]
    print(f'HandoffGuard | {data["patient"]["name"]} | {h["from"]} -> {h["to"]}\n')
    flags = [f for c in extract_claims(h["note"])
             if (f := check_claim(c, data["records"], h["written_at"]))]
    for f in sorted(flags, key=lambda x: ORDER[x["severity"]]):
        print(f'[{f["severity"]}] Handover says: "{f["claim"]}"')
        print(f'   Evidence: {f["evidence"]}')
        print(f'   Status:   {f["status"]}\n')


if __name__ == "__main__":
    main()
