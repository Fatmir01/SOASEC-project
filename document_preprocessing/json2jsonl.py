"""
build_finetune_jsonl.py
------------------------
Converts a classified-and-QA JSON file (regulation or legends) into a
JSONL file compatible with FineTuneDB's chat fine-tuning format.

Input JSON shape (per chunk, simplified):
    {
        "chunk_number": int,
        "title": str | null,
        "subtitle": str | null,
        "classification": str,      # one of 5 pillars or "unknown"
        "content": str,
        "qa_pairs": [
            { "question": str, "answer": str,
              "type": "Factoid" | "Descriptive, non-factoid",
              "tag": str },
            ...
        ]
    }

The script supports both shapes used in this project:
    A) Regulation: top-level dict with `"chunks": [...]`
    B) Legends:    top-level dict with `"files": [{"chunks": [...]}, ...]`

Each Q&A pair becomes one JSONL line in chat format:
    {
      "messages": [
        {"role": "system",    "content": <SYSTEM_PROMPT>},
        {"role": "user",      "content": <question>},
        {"role": "assistant", "content": <answer>}
      ]
    }

Chunks classified as "unknown" and chunks with no Q&A pairs are skipped.

Usage:
    python build_finetune_jsonl.py INPUT.json OUTPUT.jsonl
    python build_finetune_jsonl.py INPUT.json OUTPUT.jsonl --shuffle --seed 42
"""

import argparse
import json
import random
import sys
from pathlib import Path


SYSTEM_PROMPT = (
    "You are an expert assistant on the EU Gender Equality Strategy 2020-2025. "
    "Answer questions about the strategy's policy objectives, instruments, and "
    "concrete examples of compliance accurately and concisely, grounded in the "
    "Strategy's text and its illustrative legends."
)


def iter_chunks(data: dict):
    """Yield chunk dicts regardless of which of the two top-level shapes the JSON has."""
    if "chunks" in data:
        # Regulation shape
        yield from data["chunks"]
    elif "sources" in data:
        # Legends shape: nested per source file
        for f in data["sources"]:
            yield from f.get("chunks", [])
    else:
        raise ValueError(
            "Input JSON has neither 'chunks' nor 'sources' at the top level. "
            "Cannot determine where to read Q&A pairs from."
        )


def build_examples(data: dict):
    """Walk the JSON and yield one chat example dict per Q&A pair."""
    examples = []
    skipped_unknown = 0
    skipped_no_qa = 0

    for ch in iter_chunks(data):
        if ch.get("classification") == "unknown":
            skipped_unknown += 1
            continue
        pairs = ch.get("qa_pairs") or []
        if not pairs:
            skipped_no_qa += 1
            continue

        for p in pairs:
            q = (p.get("question") or "").strip()
            a = (p.get("answer") or "").strip()
            if not q or not a:
                continue

            examples.append({
                "messages": [
                    {"role": "system",    "content": SYSTEM_PROMPT},
                    {"role": "user",      "content": q},
                    {"role": "assistant", "content": a},
                ]
            })

    return examples, {
        "skipped_unknown_chunks": skipped_unknown,
        "skipped_chunks_without_qa": skipped_no_qa,
    }


def summarize(data: dict, examples):
    """Return a small report dict for the console."""
    by_tag = {}
    by_type = {}
    for ch in iter_chunks(data):
        if ch.get("classification") == "unknown":
            continue
        for p in ch.get("qa_pairs") or []:
            by_tag[p.get("tag", "?")] = by_tag.get(p.get("tag", "?"), 0) + 1
            t = p.get("type", "?")
            by_type[t] = by_type.get(t, 0) + 1
    return {"by_tag": by_tag, "by_type": by_type, "total": len(examples)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input_json", type=Path, help="Path to the input JSON file")
    ap.add_argument("output_jsonl", type=Path, help="Path to the output JSONL file")
    ap.add_argument("--shuffle", action="store_true", help="Shuffle examples before writing")
    ap.add_argument("--seed", type=int, default=42, help="Random seed for --shuffle (default: 42)")
    ap.add_argument("--system-prompt", type=str, default=None,
                    help="Override the default system prompt with a custom one")
    args = ap.parse_args()

    if args.system_prompt:
        global SYSTEM_PROMPT
        SYSTEM_PROMPT = args.system_prompt

    if not args.input_json.exists():
        print(f"ERROR: input file not found: {args.input_json}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(args.input_json.read_text(encoding="utf-8"))
    examples, skipped = build_examples(data)

    if args.shuffle:
        random.Random(args.seed).shuffle(examples)

    args.output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with args.output_jsonl.open("w", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    rep = summarize(data, examples)
    print(f"Wrote {rep['total']} examples to {args.output_jsonl}")
    print(f"  Skipped {skipped['skipped_unknown_chunks']} 'unknown' chunks")
    print(f"  Skipped {skipped['skipped_chunks_without_qa']} chunks without Q&A pairs")
    print("\nPer tag (classification):")
    for k, v in sorted(rep["by_tag"].items()):
        print(f"  {k:<35} {v}")
    print("\nPer type:")
    for k, v in sorted(rep["by_type"].items()):
        print(f"  {k:<25} {v}")


if __name__ == "__main__":
    main()