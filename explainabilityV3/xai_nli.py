"""
Analisi XAI a blocchi su GE-NLI
===============================

Analisi di interpretabilita' per occlusione di blocchi, ristretta al task
GE-NLI (entailment di conformita'), il task piu' rilevante per l'ipotesi del
progetto e l'unico in cui i modelli non saturano completamente.

DUE LIVELLI DI ANALISI

  Livello 1 — CAMPI INTERI
    Occlude l'intera premessa (comportamento organizzativo) e l'intera ipotesi
    (clausola normativa), separatamente. Risponde a: su quale dei due campi
    ciascun modello fonda la decisione?

  Livello 2 — FRASI
    Occlude una frase alla volta all'interno di premessa e ipotesi. Risponde a:
    quale parte del comportamento / della clausola porta il segnale?

  Entrambi i livelli sono disaggregati per label (entailment / contradiction /
  neutral), cosi' da agganciare l'ipotesi di complementarita' del paper.

METRICA
  importanza(blocco) = logprob(input completo) - logprob(input senza blocco)
  alto  => blocco causalmente necessario alla decisione
  ~0    => il modello decide anche senza
  <0    => rimuovere il blocco aiuta

La segmentazione in frasi e' deterministica (regex), senza alcun LLM: nessuna
componente soggettiva da dichiarare come limite.

Parallelizzato. NESSUN retry: un errore API interrompe l'esecuzione.

USO
  1. pip install openai numpy scipy matplotlib
  2. $env:OPENAI_API_KEY = "sk-..."
  3. compilare MODELS e GE_NLI_PATH qui sotto
  4. python xai_nli.py            -> calcola le attribuzioni
  5. python xai_nli.py --analyze  -> stampa tabelle, test e grafico
"""

import json
import os
import re
import random
import sys
import threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np

try:
    from openai import OpenAI
except ImportError:
    raise SystemExit("Manca il pacchetto openai. Esegui: pip install openai")

# =============================================================================
# CONFIG — DA COMPILARE
# =============================================================================

MODELS = {
    "base":             "gpt-4o-2024-08-06",
    "tuned-legends":    "ft:gpt-4o-2024-08-06:sesar-lab:legends-tuning:DaLddTIf",   # <-- COMPILA
    "tuned-regulation": "ft:gpt-4o-2024-08-06:sesar-lab:regulation-tuning:Da2T6Dzk",   # <-- COMPILA
}

GE_NLI_PATH = r"C:\Users\Fatmir Bylyshi\Desktop\UNIVERSITA'\MAGISTRALE\Sicurezza delle architetture orientate ai servizi\progetto\SOASEC-project\benchmark\task_pool\ge_nli\ge_nli.jsonl"

N_SAMPLE = 60           # item campionati, stratificati per label
SAMPLE_SEED = 42
N_THREADS = 8           # nessun retry: in caso di 429 ridurre questo valore
MAX_SENTENCES = 6       # limite di frasi analizzate per campo (controllo costi)

OUT_DIR = "./xai_nli_out"
OUT_JSON = os.path.join(OUT_DIR, "nli_attributions.json")

GENERIC_SYSPROMPT = (
    "You are an expert assistant on the EU Gender Equality Strategy 2020-2025. "
    "Answer questions about the strategy's policy objectives, instruments, and "
    "concrete examples of compliance accurately and concisely, grounded in the "
    "Strategy's text and its illustrative legends."
)

LOGPROB_FLOOR = -12.0
LABELS = ["entailment", "contradiction", "neutral"]

_print_lock = threading.Lock()
_client = None


def get_client():
    global _client
    if _client is None:
        _client = OpenAI()
    return _client


# =============================================================================
# DATI
# =============================================================================

def fix_mojibake(s):
    if isinstance(s, str) and ("\u00c3" in s or "\u00e2\u20ac" in s):
        try:
            return s.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            return s
    return s


def load_jsonl(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read().lstrip("\ufeff")
    try:
        obj = json.loads(raw)
        if isinstance(obj, list):
            return obj
        if isinstance(obj, dict):
            for k in ("items", "data", "rows", "records"):
                if isinstance(obj.get(k), list):
                    return obj[k]
            return [obj]
    except json.JSONDecodeError:
        pass
    rows = []
    for line in raw.splitlines():
        line = line.strip().rstrip(",")
        if line and line not in ("[", "]"):
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


SENT_RE = re.compile(r'(?<=[.!?])\s+(?=[A-Z"(])')


def split_sentences(text):
    """Segmentazione per frase, deterministica (nessun LLM)."""
    parts = [p.strip() for p in SENT_RE.split(text.strip()) if p.strip()]
    return parts if parts else ([text.strip()] if text.strip() else [])


def sample_items(path, n, seed):
    rows = load_jsonl(path)
    for r in rows:
        r["premise"] = fix_mojibake(r.get("premise", ""))
        r["hypothesis"] = fix_mojibake(r.get("hypothesis", ""))

    rng = random.Random(seed)
    by = defaultdict(list)
    for r in rows:
        if r.get("premise") and r.get("hypothesis") and r.get("label"):
            by[r["label"]].append(r)
    for v in by.values():
        rng.shuffle(v)

    picks, labels = [], sorted(by.keys())
    i = 0
    while len(picks) < n and any(by[k] for k in labels):
        k = labels[i % len(labels)]
        if by[k]:
            picks.append(by[k].pop())
        i += 1

    items = []
    for r in picks[:n]:
        items.append({
            "id": str(r.get("id", "")),
            "label": r["label"],
            "pillar": r.get("pillar_premise"),
            "premise": r["premise"],
            "hypothesis": r["hypothesis"],
            "premise_sents": split_sentences(r["premise"])[:MAX_SENTENCES],
            "hypothesis_sents": split_sentences(r["hypothesis"])[:MAX_SENTENCES],
        })
    return items


# =============================================================================
# SCORING
# =============================================================================

def build_prompt(premise, hypothesis):
    return (
        "Given a PREMISE describing organisational behaviour and a HYPOTHESIS "
        "stating a regulatory clause, decide the relationship:\n"
        "entailment (premise is compliant with the hypothesis), "
        "contradiction (premise violates it), "
        "neutral (unrelated or insufficient information).\n\n"
        f"PREMISE:\n{premise}\n\nHYPOTHESIS:\n{hypothesis}\n\n"
        "Respond with a single line in exactly this format:\n"
        "LABEL: <entailment|contradiction|neutral>\n"
        "Do not add explanations."
    )


def target_logprob(model, premise, hypothesis, target, top_k=20):
    resp = get_client().chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": GENERIC_SYSPROMPT},
            {"role": "user", "content": build_prompt(premise, hypothesis)},
        ],
        temperature=0, max_tokens=8, logprobs=True, top_logprobs=top_k,
    )
    ch = resp.choices[0]
    content = ch.logprobs.content if ch.logprobs else None
    if not content:
        return LOGPROB_FLOOR

    tgt = target.strip().lower()
    best = LOGPROB_FLOOR
    for tok in content:
        cands = [(tok.token, tok.logprob)]
        for alt in (tok.top_logprobs or []):
            cands.append((alt.token, alt.logprob))
        for text, lp in cands:
            t = text.strip().lower().strip(":.")
            if t and len(t) >= 2 and tgt.startswith(t):
                best = max(best, lp)
    return best


def drop_sentence(sents, idx):
    return " ".join(s for i, s in enumerate(sents) if i != idx)


def process_item(item):
    gold = item["label"]
    per_model = {}

    for mname, mstr in MODELS.items():
        full = target_logprob(mstr, item["premise"], item["hypothesis"], gold)

        # Livello 1 — campi interi
        lp_no_prem = target_logprob(mstr, "", item["hypothesis"], gold)
        lp_no_hyp = target_logprob(mstr, item["premise"], "", gold)
        fields = {
            "premise": full - lp_no_prem,
            "hypothesis": full - lp_no_hyp,
        }

        # Livello 2 — frasi
        prem_sents, hyp_sents = item["premise_sents"], item["hypothesis_sents"]
        sent_imp = {"premise": [], "hypothesis": []}
        if len(prem_sents) > 1:
            for i in range(len(prem_sents)):
                occl = drop_sentence(prem_sents, i)
                lp = target_logprob(mstr, occl, item["hypothesis"], gold)
                sent_imp["premise"].append(full - lp)
        if len(hyp_sents) > 1:
            for i in range(len(hyp_sents)):
                occl = drop_sentence(hyp_sents, i)
                lp = target_logprob(mstr, item["premise"], occl, gold)
                sent_imp["hypothesis"].append(full - lp)

        per_model[mname] = {
            "full_logprob": full,
            "fields": fields,
            "sentences": sent_imp,
        }

    with _print_lock:
        lps = {k: round(v["full_logprob"], 2) for k, v in per_model.items()}
        print(f"  {item['id']:16s} {item['label']:14s} full_lp={lps}")

    return {
        "id": item["id"], "label": item["label"], "pillar": item.get("pillar"),
        "n_premise_sents": len(item["premise_sents"]),
        "n_hypothesis_sents": len(item["hypothesis_sents"]),
        "premise_sents": item["premise_sents"],
        "hypothesis_sents": item["hypothesis_sents"],
        "models": per_model,
    }


def run():
    os.makedirs(OUT_DIR, exist_ok=True)
    for k, v in MODELS.items():
        if "XXXXXX" in v:
            raise SystemExit(f"[CONFIG] Model-string per '{k}' non compilata.")

    items = sample_items(GE_NLI_PATH, N_SAMPLE, SAMPLE_SEED)
    dist = defaultdict(int)
    for it in items:
        dist[it["label"]] += 1
    print(f"Item campionati: {len(items)}  {dict(dist)}")
    print(f"Thread: {N_THREADS}\n")

    results, done = [], 0
    with ThreadPoolExecutor(max_workers=N_THREADS) as ex:
        futs = [ex.submit(process_item, it) for it in items]
        for fut in as_completed(futs):
            results.append(fut.result())
            done += 1
            if done % 10 == 0:
                json.dump(results, open(OUT_JSON, "w", encoding="utf-8"),
                          ensure_ascii=False, indent=2)
                print(f"  ... checkpoint {done}/{len(items)}")

    json.dump(results, open(OUT_JSON, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"\nOK -> {OUT_JSON}  ({len(results)} item)")
    print("Ora esegui: python xai_nli.py --analyze")


# =============================================================================
# ANALISI
# =============================================================================

def _wilcoxon(a, b):
    try:
        from scipy.stats import wilcoxon
    except ImportError:
        return None, None
    d = np.array(a) - np.array(b)
    if len(a) < 6 or np.allclose(d, 0):
        return None, None
    return wilcoxon(a, b)


def _fmt_p(p, mean_a, mean_b):
    """Segnala la significativita' SOLO se anche l'effect size e' non banale.
    Un p-value piccolo con medie identiche e' rumore numerico, non un risultato."""
    if p is None:
        return ""
    if abs(mean_a - mean_b) < 0.01:
        return f"  p={p:.4f} (effect size trascurabile: NON riportare)"
    return f"  p={p:.4f}" + ("  *SIGNIFICATIVO*" if p < 0.05 else "")


def analyze():
    if not os.path.exists(OUT_JSON):
        raise SystemExit(f"Manca {OUT_JSON}. Esegui prima: python xai_nli.py")
    data = json.load(open(OUT_JSON, encoding="utf-8"))
    print(f"Item caricati: {len(data)}\n")

    # ---- saturazione ----
    print("=" * 74)
    print("SATURAZIONE (full_logprob > -0.05 => modello certo, nessun segnale)")
    print("=" * 74)
    n_all = sum(1 for d in data
                if all(m["full_logprob"] > -0.05 for m in d["models"].values()))
    print(f"item con TUTTI i modelli saturi: {n_all}/{len(data)} "
          f"({100*n_all/len(data):.0f}%)")
    for m in MODELS:
        lps = [d["models"][m]["full_logprob"] for d in data]
        sat = sum(1 for lp in lps if lp > -0.05)
        print(f"  {m:18s} mediana={np.median(lps):+.3f}  media={np.mean(lps):+.3f}"
              f"  saturi={sat}/{len(lps)}")

    # ---- livello 1: campi interi ----
    print("\n" + "=" * 74)
    print("LIVELLO 1 — IMPORTANZA DEI CAMPI INTERI")
    print("=" * 74)
    header = f"{'campo':14s}" + "".join(f"{m:>20s}" for m in MODELS)
    print(header)
    print("-" * len(header))
    for field in ["premise", "hypothesis"]:
        row = f"{field:14s}"
        for m in MODELS:
            vals = [d["models"][m]["fields"][field] for d in data]
            row += f"{np.mean(vals):>13.3f} (n={len(vals):>2d})"
        print(row)

    print("\n--- Wilcoxon appaiato: tuned-legends vs tuned-regulation ---")
    for field in ["premise", "hypothesis"]:
        a = [d["models"]["tuned-legends"]["fields"][field] for d in data]
        b = [d["models"]["tuned-regulation"]["fields"][field] for d in data]
        _, p = _wilcoxon(a, b)
        print(f"  {field:14s} legends={np.mean(a):+.3f}  "
              f"regulation={np.mean(b):+.3f}{_fmt_p(p, np.mean(a), np.mean(b))}")

    # ---- livello 1 disaggregato per label ----
    print("\n" + "=" * 74)
    print("LIVELLO 1 — DISAGGREGATO PER LABEL")
    print("=" * 74)
    for lab in LABELS:
        sub = [d for d in data if d["label"] == lab]
        if not sub:
            continue
        print(f"\n{lab.upper()}  (n={len(sub)})")
        print(f"  {'campo':12s}" + "".join(f"{m:>20s}" for m in MODELS))
        for field in ["premise", "hypothesis"]:
            row = f"  {field:12s}"
            for m in MODELS:
                vals = [d["models"][m]["fields"][field] for d in sub]
                row += f"{np.mean(vals):>20.3f}"
            print(row)
        a = [d["models"]["tuned-legends"]["fields"]["hypothesis"] for d in sub]
        b = [d["models"]["tuned-regulation"]["fields"]["hypothesis"] for d in sub]
        _, p = _wilcoxon(a, b)
        if p is not None:
            print(f"    -> hypothesis: legends={np.mean(a):+.3f} vs "
                  f"regulation={np.mean(b):+.3f}{_fmt_p(p, np.mean(a), np.mean(b))}")

    # ---- livello 2: frasi ----
    print("\n" + "=" * 74)
    print("LIVELLO 2 — CONCENTRAZIONE DEL SEGNALE SULLE FRASI")
    print("(media dell'importanza della frase piu' importante di ciascun campo)")
    print("=" * 74)
    for field in ["premise", "hypothesis"]:
        print(f"\n{field}:")
        for m in MODELS:
            maxes = [max(d["models"][m]["sentences"][field]) for d in data
                     if d["models"][m]["sentences"][field]]
            if maxes:
                print(f"  {m:18s} media del massimo={np.mean(maxes):+.3f}"
                      f"  (item con >1 frase: {len(maxes)})")

    # ---- grafico ----
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, 2, figsize=(13, 5))

        x, width = np.arange(2), 0.25
        for i, m in enumerate(MODELS):
            means = [np.mean([d["models"][m]["fields"][f] for d in data])
                     for f in ["premise", "hypothesis"]]
            axes[0].bar(x + i * width, means, width, label=m)
        axes[0].set_xticks(x + width)
        axes[0].set_xticklabels(["premise", "hypothesis"])
        axes[0].set_ylabel("importanza media (caduta di log-prob)")
        axes[0].set_title("Importanza dei campi (tutti gli item)")
        axes[0].axhline(0, color="black", linewidth=0.8)
        axes[0].legend(fontsize=8)

        xl = np.arange(len(LABELS))
        for i, m in enumerate(MODELS):
            means = []
            for lab in LABELS:
                sub = [d for d in data if d["label"] == lab]
                means.append(np.mean([d["models"][m]["fields"]["hypothesis"]
                                      for d in sub]) if sub else 0)
            axes[1].bar(xl + i * width, means, width, label=m)
        axes[1].set_xticks(xl + width)
        axes[1].set_xticklabels(LABELS, fontsize=9)
        axes[1].set_ylabel("importanza dell'ipotesi")
        axes[1].set_title("Dipendenza dalla clausola normativa, per label")
        axes[1].axhline(0, color="black", linewidth=0.8)
        axes[1].legend(fontsize=8)

        plt.tight_layout()
        out = os.path.join(OUT_DIR, "nli_importance.png")
        plt.savefig(out, dpi=150)
        print(f"\nGrafico -> {out}")
    except ImportError:
        print("\n[info] matplotlib non installato: grafico saltato")

    print("\nFatto.")


if __name__ == "__main__":
    if "--analyze" in sys.argv:
        analyze()
    else:
        run()
