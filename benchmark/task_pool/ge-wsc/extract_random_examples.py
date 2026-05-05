"""Stratified sample of 100 records from ge_wsc.jsonl.

Strategy:
- Re-derive source metadata (stereotype, type, split) by re-reading the
  eight source files in the same order they were concatenated.
- Stratify by (stereotype x type) -> 4 cells, 25 per cell.
- Within each cell, balance male vs female pronouns as evenly as possible.
- Fixed random seed for reproducibility.
"""

import json
import os
import random
import re
from collections import defaultdict, Counter

INPUT_DIR = "/mnt/user-data/uploads"
OUTPUT_DIR = "/mnt/user-data/outputs"
SOURCE_JSONL = os.path.join(OUTPUT_DIR, "ge_wsc.jsonl")
OUT_JSONL = os.path.join(OUTPUT_DIR, "ge_wsc_sample100.jsonl")
SEED = 42
N_PER_CELL = 25

# Same order used when building ge_wsc.jsonl
FILES = [
    "pro_stereotyped_type1_txt.dev",
    "pro_stereotyped_type1_txt.test",
    "pro_stereotyped_type2_txt.dev",
    "pro_stereotyped_type2_txt.test",
    "anti_stereotyped_type1_txt.dev",
    "anti_stereotyped_type1_txt.test",
    "anti_stereotyped_type2_txt.dev",
    "anti_stereotyped_type2_txt.test",
]

MALE_PRON = {"he", "him", "his", "himself"}
FEMALE_PRON = {"she", "her", "hers", "herself"}


def parse_filename(fname):
    m = re.match(r"(pro|anti)_stereotyped_type(\d)_txt\.(dev|test)", fname)
    return {
        "stereotype": m.group(1),
        "type": f"type{m.group(2)}",
        "split": m.group(3),
    }


# 1. Build source-file index mirroring how ge_wsc.jsonl was written
source_meta = []
for fname in FILES:
    meta = parse_filename(fname)
    path = os.path.join(INPUT_DIR, fname)
    with open(path) as f:
        for ln, line in enumerate(f, 1):
            if line.strip():
                source_meta.append({**meta, "src_file": fname, "src_line": ln})

# 2. Read records and zip with metadata
records = []
with open(SOURCE_JSONL) as f:
    for i, line in enumerate(f):
        rec = json.loads(line)
        rec["_meta"] = source_meta[i]
        # Extract pronoun from question
        pron = rec["question"].replace("To whom does ", "").replace(" refer?", "")
        gender = "M" if pron.lower() in MALE_PRON else "F"
        rec["_gender"] = gender
        records.append(rec)

assert len(records) == len(source_meta), "Length mismatch"
print(f"Loaded {len(records)} records")

# 3. Bucket by (stereotype, type) and then by gender
buckets = defaultdict(lambda: defaultdict(list))
for r in records:
    key = (r["_meta"]["stereotype"], r["_meta"]["type"])
    buckets[key][r["_gender"]].append(r)

# Diagnostics
print("\nCell sizes:")
for key, gdict in sorted(buckets.items()):
    print(f"  {key}: M={len(gdict['M'])}, F={len(gdict['F'])}, "
          f"total={len(gdict['M']) + len(gdict['F'])}")

# 4. Sample
rng = random.Random(SEED)
sample = []
for key in sorted(buckets.keys()):
    m_pool = buckets[key]["M"]
    f_pool = buckets[key]["F"]
    n_m = N_PER_CELL // 2          # 12
    n_f = N_PER_CELL - n_m         # 13 (one extra to female to fill 25)
    # alternate which gender gets the extra slot per cell to keep balance overall
    # parity: pro/type1 -> F gets extra, pro/type2 -> M gets extra, etc.
    cell_idx = sorted(buckets.keys()).index(key)
    if cell_idx % 2 == 1:
        n_m, n_f = n_f, n_m
    picks_m = rng.sample(m_pool, min(n_m, len(m_pool)))
    picks_f = rng.sample(f_pool, min(n_f, len(f_pool)))
    sample.extend(picks_m + picks_f)

print(f"\nSampled {len(sample)} records")

# 5. Shuffle so cells aren't grouped, write out without internal _meta keys
rng.shuffle(sample)

with open(OUT_JSONL, "w", encoding="utf-8") as out:
    for r in sample:
        clean = {k: v for k, v in r.items() if not k.startswith("_")}
        out.write(json.dumps(clean, ensure_ascii=False) + "\n")

# 6. Final distribution report
print("\nFinal sample distribution:")
print("  By stereotype:", Counter(r["_meta"]["stereotype"] for r in sample))
print("  By type:      ", Counter(r["_meta"]["type"] for r in sample))
print("  By split:     ", Counter(r["_meta"]["split"] for r in sample))
print("  By gender:    ", Counter(r["_gender"] for r in sample))
print("  By cell:      ",
      Counter((r["_meta"]["stereotype"], r["_meta"]["type"]) for r in sample))
print("  By label pos: ",
      Counter("A" if r["label"] == r["option_a"] else "B" for r in sample))

print(f"\nWrote: {OUT_JSONL}")