"""
Generate the GE-NEXT predictions template CSV.

Mirrors the structure of ge_wsc_predictions_template.csv:
- Semicolon-delimited
- Two-row header: Column1..ColumnN on row 1, real names on row 2
- One row per item with the gold label and three empty prediction columns
"""

import json
import csv
from pathlib import Path

OUT_DIR = Path("./benchmark/task_pool/ge_next/helpers")
JSONL = OUT_DIR / "ge_next_v2_complex.jsonl"
CSV_OUT = OUT_DIR / "ge_next_predictions_template_complex.csv"

# Field schema (matching ge_wsc style: id, subset-equivalent, then content, then gold + 3 model columns + notes)
HEADERS = [
    "id",
    "pillar",
    "vignette",
    "option_a",
    "option_b",
    "option_c",
    "option_d",
    "gold_letter",
    "gold_type",
    "prediction_base",
    "prediction_tuned_legends",
    "prediction_tuned_regulation",
    "notes",
]

with open(JSONL, "r", encoding="utf-8") as f:
    records = [json.loads(line) for line in f if line.strip()]

with open(CSV_OUT, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter=";", quoting=csv.QUOTE_MINIMAL)
    # Row 1 — generic Column1..ColumnN headers (mirrors the WSC template)
    writer.writerow([f"Column{i+1}" for i in range(len(HEADERS))])
    # Row 2 — real field names
    writer.writerow(HEADERS)
    # Data rows
    for r in records:
        # Find the option type that corresponds to the gold letter
        gold_letter = r["gold"]
        gold_type = r["option_types"][gold_letter]
        writer.writerow([
            r["id"],
            r["pillar"],
            r["vignette"],
            r["options"]["A"],
            r["options"]["B"],
            r["options"]["C"],
            r["options"]["D"],
            gold_letter,
            gold_type,
            "",  # prediction_base — to be filled by the operator
            "",  # prediction_tuned_legends
            "",  # prediction_tuned_regulation
            "",  # notes
        ])

print(f"Wrote {len(records)} rows to {CSV_OUT}")
print(f"File size: {CSV_OUT.stat().st_size:,} bytes")

# Quick preview
with open(CSV_OUT, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i < 4:
            print(line.rstrip()[:200])
        else:
            break