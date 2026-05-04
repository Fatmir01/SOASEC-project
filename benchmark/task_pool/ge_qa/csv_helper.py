"""Build CSV response templates for the GE-QA evaluation."""
import csv
import json

FACT = [json.loads(l) for l in open('./benchmark/task_pool/ge_qa/ge_qa_factoid.jsonl', encoding='utf-8')]
BOOL = [json.loads(l) for l in open('./benchmark/task_pool/ge_qa/ge_qa_bool.jsonl', encoding='utf-8')]
 
# ---- Factoid response template ----------------------------------------
fact_path = './benchmark/task_pool/ge_qa/ge_qa_factoid_responses_template.csv'
with open(fact_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    w.writerow([
        'id',
        'passage_id',
        'pillar',
        'answer_type',
        'gold_answer',
        'gold_aliases',          # semicolon-separated
        'base_response',         # to fill in manually
        'tuned_legends_response',
        'tuned_regulation_response',
    ])
    for it in FACT:
        aliases = ';'.join(it.get('answer_aliases', []))
        w.writerow([
            it['id'],
            it['passage_id'],
            it['pillar'],
            it['answer_type'],
            it['answer'],
            aliases,
            '', '', '',          # response cells left blank for manual entry
        ])
print(f"Wrote {fact_path}: {len(FACT)} rows")

# ---- Bool response template -------------------------------------------
bool_path = './benchmark/task_pool/ge_qa/ge_qa_bool_responses_template.csv'
with open(bool_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    w.writerow([
        'id',
        'passage_id',
        'pillar',
        'construction_method',
        'gold_answer',
        'base_response',
        'tuned_legends_response',
        'tuned_regulation_response',
    ])
    for it in BOOL:
        w.writerow([
            it['id'],
            it['passage_id'],
            it['pillar'],
            it['construction_method'],
            it['answer'],
            '', '', '',
        ])
print(f"Wrote {bool_path}: {len(BOOL)} rows")

# Sanity preview
print("\n--- factoid template (first 3 rows) ---")
with open(fact_path, encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i < 3:
            print(line.rstrip())
print("\n--- bool template (first 3 rows) ---")
with open(bool_path, encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i < 3:
            print(line.rstrip())