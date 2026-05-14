"""
generate_probe_csv.py
Generates ge_explainability_probes_template.csv — a semicolon-delimited
predictions template with all 50 probes pre-populated and three empty
response columns ready for manual entry after GUI testing.

Usage:
    python3 generate_probe_csv.py
Output:
    ge_explainability_probes_template.csv  (same directory)
"""

import csv
import json
from pathlib import Path

JSONL_PATH = Path("ge_explainability_probes.jsonl")
CSV_PATH   = Path("ge_explainability_probes_template.csv")

HEADERS = [
    "probe_id",
    "archetype",
    "prompt_text",
    "base_response_text",
    "regulation_tuned_response_text",
    "legends_tuned_response_text",
]

def load_probes(jsonl_path: Path) -> list[dict]:
    probes = []
    with open(jsonl_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                probes.append(json.loads(line))
    return probes


def write_csv(probes: list[dict], csv_path: Path) -> None:
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";", quoting=csv.QUOTE_ALL)
        writer.writerow(HEADERS)
        for p in probes:
            writer.writerow([
                p["probe_id"],
                p["archetype"],
                p["prompt_text"],
                "",   # base_response_text — fill in during testing
                "",   # regulation_tuned_response_text
                "",   # legends_tuned_response_text
            ])
    print(f"Written {len(probes)} rows to {csv_path}")


if __name__ == "__main__":
    if not JSONL_PATH.exists():
        raise FileNotFoundError(
            f"JSONL source not found: {JSONL_PATH}\n"
            "Ensure ge_explainability_probes.jsonl is in the same directory."
        )
    probes = load_probes(JSONL_PATH)
    assert len(probes) == 50, f"Expected 50 probes, got {len(probes)}"
    write_csv(probes, CSV_PATH)
