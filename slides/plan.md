
# Presentation Blueprint

## Pre-flight Meta

- **Source paper:** *The Legend Challenge: Embedding Ethical Compliance into LLMs through Champion Narratives in the Gender Equality Domain* — Bylyshi, El-Khazri, Ouardi (Univ. of Milan, Dept. of Computer Science).
- **Inferred audience:** Academic examiners (domain-adjacent: NLP / responsible AI).
- **Target structure:** Problem-Driven (Structure A) — start from compliance problem, build to method, deliver complementarity finding.
- **Target slide count:** 21 slides (~15–20 min talk).
- **Single-sentence key takeaway:** Legend-based and regulation-based fine-tuning teach *complementary* compliance competences — legends win on action/recognition, regulation wins on ontology/factoid recall — so deployment should be driven by the dominant risk profile, not by the aggregate score.
- **Narrative arc:** Compliance paradox → Sargsyan-Damiani's "legends" proposal → empirical gap (no test, no metric) → our 3 artifacts (Pipeline, GenderEqGLUE, CIP) → 3-3 split of per-task wins → complementarity routing.

---

## Slide 1 — Title

- **Core message:** Identification of the work.
- **On-slide content:**
  - Title: *The Legend Challenge: Embedding Ethical Compliance into LLMs through Champion Narratives in the Gender Equality Domain*
  - Authors: Fatmir Bylyshi · El-Khazri Hicham · Ouardi Ilyass (equal contribution)
  - Affiliation: Department of Computer Science, University of Milan
  - Anchor keywords: ethical AI · regulatory compliance · gender equality · LLMs · legends · GenderEqGLUE
- **Visual layout:** Centered title block (top 60%); authors + affiliation in a clean two-line block; a small "teaser" decorative element on the right — a stylized bar-chart silhouette showing three rising bars labeled `base`, `tuned-legends`, `tuned-regulation` (no axis values needed, purely iconographic).

---

## Slide 2 — The Compliance Paradox (Motivation)

- **Core message:** When AI systems are delegated to middle-management decisions under regulation, profit-optimization pressure structurally conflicts with social-cost considerations.
- **On-slide content:**
  - LLMs are increasingly delegated to middle-management decisions: hiring, procurement, performance review, contract review — all directly governed by regulation.
  - Managers pressured to cost-optimize may deploy AI tools lacking intrinsic social-cost considerations.
  - Result: automated decisions can clash with corporate values *and* external directives (EU, UN).
  - Implication: compliance must be embedded into the algorithmic architecture, not retrofitted via post-hoc filtering.
- **Visual layout:** Two-column conflict diagram. Left column "Cost optimization" (icon: downward arrow / dollar). Right column "Regulatory compliance" (icon: scales / EU stars). A red lightning bolt or collision symbol in the center labeled "Conflict of interest". Below: a single-line takeaway in larger type — *"Embed compliance into the model, not into the filter."*

---

## Slide 3 — The Sargsyan-Damiani Proposal: Legends

- **Core message:** Sargsyan and Damiani (2025) propose teaching compliance via *legends* — synthetic champion narratives — so the model learns compliance as a *capacity*, not a *lookup*.
- **On-slide content:**
  - A **legend** = a synthetic, idealised exemplar (a "champion profile") whose behaviour incarnates compliance.
  - Training intuition: fine-tuning on legends teaches compliance as a **capacity** exercised over novel inputs, not as a **lookup** against memorised regulatory vocabulary.
  - Contrast: fine-tuning on regulation text alone risks teaching the model to recognise the lexicon without applying the principle when the lexicon is absent or rephrased.
- **Visual layout:** A two-path schematic. Top path: "Regulation text → model" with a textbook icon, labeled *"learns lexicon"*. Bottom path: "Legend (story with named characters) → model" with a person/storyteller icon, labeled *"learns capacity"*. A question mark hovers over the bottom path — leads into Slide 4.

---

## Slide 4 — The Empirical Gap

- **Core message:** The proposal is appealing but untested — no model has been fine-tuned on legends, and no metric exists to falsify the claim.
- **On-slide content:**
  - Sargsyan & Damiani offered a proposal **without** an empirical test, a measurement instrument, or a controlled comparison.
  - Standard benchmarks (GLUE, SuperGLUE) are deliberately *domain-agnostic* — they reward generic linguistic competence, not regulatory-compliance reasoning.
  - The one-sentence research question: *Does legend fine-tuning in fact produce a measurably different model from regulation-text fine-tuning, holding everything else constant?*
- **Visual layout:** A "missing pieces" graphic — three empty/dotted boxes labeled "Empirical test", "Measurement instrument", "Controlled comparison" — each with a red ❌. Below, the research question rendered in a quote-style block.

---

## Slide 5 — Our Three Contributions

- **Core message:** We deliver the three missing artifacts to enable the first controlled test of the Sargsyan-Damiani hypothesis.
- **On-slide content:**
  1. **Dataset-construction pipeline** — adapted from SustainableQA; produces matched legend-vs-regulation JSONL corpora.
  2. **GenderEqGLUE** — 5-task benchmark adapted one-to-one from GLUE/SuperGLUE for the EU Gender Equality Strategy 2020–2025.
  3. **Counterfactual Input Probing (CIP)** — behavioural-only explainability protocol for closed fine-tuning platforms (no logits / gradients).
- **Visual layout:** Three-panel horizontal layout, each panel an icon + 2-word label + one-line description: 🛠 *Pipeline* | 📊 *GenderEqGLUE* | 🔍 *CIP*. Use a consistent muted color per panel that will reappear on the section-divider slides.

---

## Slide 6 — Related Work: Embedding Ethics in LLMs

- **Core message:** Prior work splits between machine-readable regulation translation and direct text fine-tuning — but both leave the legends route untested.
- **On-slide content:**
  - **Route 1 — Machine-readable regulation:** X2RL semantic format (McLaughlin 2021); Denmark's digital-ready legislation (Motzfeldt 2018); Rules-as-Code U.S. public-benefits pilots (Naumova 2023) — require extensive prompting and human oversight to preserve equity.
  - **Route 2 — Fine-tune on regulation text:** IBM Alignment Studio (Achintalwar 2024) — authors themselves attribute limitations to the "literal-textual character" of the training signal.
  - **The gap this paper studies:** that literal-textual limitation is exactly what the legend route promises to overcome.
- **Visual layout:** Three-column comparison (Route 1 / Route 2 / *Our controlled study*). Bottom row: a "remaining challenge" arrow pointing from Route 2 to our work.

---

## Slide 7 — Related Work: NLU Benchmarks & Their Limit

- **Core message:** GLUE and SuperGLUE measure generic linguistic competence; none of their tasks probes *regulatory-compliance reasoning*.
- **On-slide content:**
  - GLUE / SuperGLUE compose scores across SST-2, MNLI, RTE, SQuAD, BoolQ, WSC, COPA, WinoBias.
  - Design choice = **deliberately domain-agnostic** → a high GLUE score reflects generic linguistic competence, *not* reasoning over a specific regulation's structure.
  - GenderEqGLUE adapts the five canonical templates **one-to-one** to the EU Gender Equality Strategy and anchors them in held-out passages.
- **Visual layout:** Mapping table — left column "GLUE/SuperGLUE template", right column "GenderEqGLUE adaptation": SST-2 → GE-CLS, MNLI/RTE → GE-NLI, SQuAD/BoolQ → GE-QA, WSC/WinoBias → GE-WSC, COPA → GE-NEXT. Arrow icons between columns.

---

## Slide 8 — Methodology: Pipeline Overview

- **Core message:** A 6-stage matched-corpus pipeline produces parallel legend / regulation JSONL files that differ *only* in source content.
- **On-slide content:**
  - Six stages: (1) PDF→Markdown preprocessing, (2) Legends generation, (3) Six-class pillar classification, (4) Two-stage span extraction, (5) Factoid + Non-factoid Q&A generation, (6) Fine-tuning on FineTuneDB Studio.
  - Both branches share preprocessing, classifier, extractor, generator, system prompt, chat format.
  - End-state: 327 legend JSONL lines vs. 293 regulation JSONL lines (~10% gap, treated as corpus-size baseline).
  - Backbone: `gpt-4o-2024-08-06`.
- **Visual layout:** Horizontal flow diagram with two parallel tracks (LEGENDS track on top in one accent color, REGULATION track on bottom in a second). Six stage-boxes are shared/merged in the middle; both tracks converge into a single "JSONL" output node at the right. Annotation under the merged stages: *"only source content varies"*.

---

## Slide 9 — Pipeline Stage Detail: Legends Generation

- **Core message:** 15 legends are synthesised by 3 different commercial LLMs (5 per pillar each) using one fixed structural template — multi-LLM mixing maximises stylistic diversity.
- **On-slide content:**
  - Generators (April 2026, web interfaces): GPT-5.4 Pro · Gemini 3 Pro · Microsoft Copilot.
  - Each produces 5 legends, one per Strategy pillar → **15 legends total** (5 × 3).
  - Fixed legend format: Title · Setting · 3–5 named characters · 400–600-word narrative arc · ≥1 direct-speech dialogue · measurable outcome · explicit acknowledgement of the EU Gender Equality Strategy 2020–2025.
  - 15 narratives expand to **327 closed-book Q&A pairs** after extraction + generation stages.
- **Visual layout:** Funnel/expansion diagram: three generator logos at top → 15 legend cards in the middle → "327 Q&A pairs" at the bottom. To the right, a callout listing the 5 pillars: `violence_stereotypes`, `equal_economy`, `leadership_participation`, `mainstreaming_intersectionality`, `funding_global_action`.

---

## Slide 10 — Fine-Tuning Protocol & Controlled Comparison

- **Core message:** Every axis except corpus content is held constant — same backbone, same system prompt, same chat format, ~matched line count.
- **On-slide content:**
  - **Held constant:** backbone (`gpt-4o-2024-08-06`); system prompt (verbatim across both runs); JSONL chat structure (system + user + assistant turns); hyperparameters (externally controlled by FineTuneDB Studio).
  - **Varies (the only experimental variable):** JSONL content — legends vs. regulation.
  - **Line counts:** legends 327 (199 non-factoid + 128 factoid) / regulation 293 (184 non-factoid + 109 factoid). Pillar distribution differs by construction.
  - **Cost of this guarantee:** closed-platform access — no logits / gradients → motivates CIP (Slide 13).
- **Visual layout:** A balance-scale metaphor with two pans labeled "tuned-legends (327)" and "tuned-regulation (293)". Above the pans, a row of "✓ matched" tags (backbone, system prompt, format, hyperparams). Below, a single red "✗ varies" tag labeled "corpus content".

---

## Slide 11 — GenderEqGLUE: The Five Tasks

- **Core message:** GenderEqGLUE adapts five GLUE/SuperGLUE templates one-to-one, anchored in a held-out Common Evaluation Base of 217 EU passages.
- **On-slide content (compact table):**

| Task | What it measures | GLUE analogue | Source | Metric |
|---|---|---|---|---|
| GE-CLS | Pillar classification (6-class) | SST-2 | CEB-CLS (72) | Macro-F1 |
| GE-NLI | Compliance entailment (3-class) | MNLI / RTE | CEB-NLI (168 triples) | Accuracy |
| GE-QA | Reading comprehension (open-book) | SQuAD / BoolQ | CEB-QA | F1 / EM + accuracy |
| GE-WSC | Stereotype-aware coreference | WSC / Winogender | WinoBias as-is | Accuracy + Parity |
| GE-NEXT | Compliant-action selection (4-choice) | COPA | Curated vignettes (150) | Accuracy |

- **CEB:** 217 EU passages held-out from training (Roadmap for Women's Rights 2025 · GAP III · Council Conclusions on Pay Gap 2019 · Directive 2022/2381).
- **Aggregate:** unweighted arithmetic mean of the five headline metrics.
- **Visual layout:** Render the table above as a clean styled table (no LaTeX rules). Use a column-strip accent color matching the GenderEqGLUE color in Slide 5. To the right of the table, a small donut showing the open-book vs. closed-book split (4 closed-book : 1 open-book = GE-QA only).

---

## Slide 12 — Two Central Tasks for the Hypothesis: GE-NLI & GE-NEXT

- **Core message:** GE-NLI probes compliance *recognition*, GE-NEXT probes compliant-action *selection* — the two tasks designed *a priori* as the hypothesis-central tests.
- **On-slide content:**
  - **GE-NLI:** 168 triples (56 per class: entailment / contradiction / neutral). Premise = organisational scenario; hypothesis = regulatory clause. 5-stage construction (clause extraction → compliant scenario → factual perturbation → cross-pillar pairing → balance verification).
  - **GE-NEXT:** 150 vignettes (30 per pillar). Each = middle-manager protagonist + quantified gap + four candidate actions, with a fixed distractor typology:
    - **Substantive-compliant** (gold)
    - **Performative** — symbolic gesture, no measurable KPIs
    - **Cost-optimising** — defer / minimise / absorb cost at the expense of the objective
    - **Orthogonal** — addresses a *different* gender-equality concern
  - GE-NEXT is the direct probe of the *compliance-vs-cost arbitrage* at the centre of the Sargsyan-Damiani conflict.
- **Visual layout:** Split-panel layout. Left panel = GE-NLI as a triangle diagram (3 vertices: entailment / contradiction / neutral). Right panel = GE-NEXT as a 4-option radial showing one gold action (green check) and three labelled distractor types (performative / cost-optimising / orthogonal) with distinct icons.

---

## Slide 13 — Counterfactual Input Probing (CIP)

- **Core message:** Closed-platform access blocks SHAP / LIME / Integrated Gradients / attention rollout — CIP is the behavioural-only protocol the access constraint *admits*.
- **On-slide content:**
  - **Why CIP?** FineTuneDB Studio is GUI-only: no logits, no gradients, no internals, no batched API. Generated text is the sole observable.
  - **Protocol:** For each of 5 pillars, one base vignette (GE-NEXT format) is run in three variants:
    - **Variant A — Original Baseline:** full regulatory vocabulary present.
    - **Variant B — Keyword-Stripped:** domain terminology removed, semantic content preserved.
    - **Variant C — Adversarially Framed:** full content + competing discursive frame (meritocracy camouflage / cost-efficiency pressure / cultural relativism / phased-implementation deferral / scientific-integrity framing).
  - **Scoring:** binary (1 = position maintained / 0 = position abandoned). Total: 5 pillars × 3 variants × 3 models = **45 evaluations**.
  - **Logic:** A model with structural reasoning maintains position under B and C; a model relying on lexical mimicry fails under B.
- **Visual layout:** Vertical 3-step ladder showing A → B → C with annotations: "lexical cues present" / "lexical cues stripped" / "adversarial frame added". To the right, an "access constraints" box showing four crossed-out methods (SHAP, LIME, IG, Attention Rollout) and one highlighted method (CIP).

---

## Slide 14 — Headline Results

- **Core message:** `tuned-regulation` leads the aggregate at 0.938 — but both fine-tuned models clearly beat the base, and per-task wins split 3–3.
- **On-slide content (the headline table):**

| Model | GE-CLS | GE-NLI | GE-QA | GE-WSC | GE-NEXT | **GenderEqGLUE** |
|---|---|---|---|---|---|---|
| base | 0.833 | 0.899 | 0.929 | 0.930 | 0.927 | 0.904 |
| tuned-legends | 0.839 | **0.929** | 0.938 | **0.960** | **0.967** | 0.926 |
| tuned-regulation | **0.928** | 0.911 | **0.944** | **0.960** | 0.947 | **0.938** |

- Aggregate ranking: **tuned-regulation ≈ tuned-legends > base** (+3.4 pts and +2.2 pts over base, respectively).
- Per-task wins: **3–3 split** between the two fine-tuned regimes; base wins zero.
- **Visual layout:** Grouped vertical bar chart, x-axis = the 6 columns (5 tasks + Aggregate), 3 bars per group. Color encoding: base = grey, tuned-legends = teal, tuned-regulation = violet (matching the Figure 1 teaser in the paper). Y-axis from 0.80 to 1.00 to make the differences readable. Bold the per-task winner. Below the chart, a one-line takeaway: *"Two fine-tuned models, three wins each — no dominance."*

---

## Slide 15 — Where the Wins Go (Per-Task Pattern)

- **Core message:** The 3-3 split is not random — `tuned-regulation` wins on tasks matching the regulation's lexical/thematic structure; `tuned-legends` wins on the two hypothesis-central reasoning tasks.
- **On-slide content:**
  - **tuned-regulation wins:** GE-CLS · GE-QA · GE-WSC (tied) — pillar ontology + short-span factoid + ceiling-tied coreference.
  - **tuned-legends wins:** GE-NLI · GE-NEXT · GE-WSC (tied) — compliance recognition + compliant-action selection + ceiling-tied coreference.
  - The aggregate score *conceals* this partition; it must be read alongside the per-task results, not instead of them.
- **Visual layout:** Two stacked card panels side-by-side. Left card (violet header) "Regulation wins:" → CLS, QA, WSC(=) with sub-labels (Ontology / Factoid / Tied). Right card (teal header) "Legends wins:" → NLI, NEXT, WSC(=) with sub-labels (Compliance recognition / Action selection / Tied). Center divider with a small "3–3" badge.

---

## Slide 16 — Behind the GE-WSC Tie: The Parity Diagnostic

- **Core message:** The two fine-tuned models tie on GE-WSC accuracy (0.96), but only `tuned-legends` achieves perfect gender parity — same destination, different routes.
- **On-slide content:**
  - GE-WSC accuracy: base 0.93 / tuned-legends 0.96 / tuned-regulation 0.96 (tie).
  - **Gender Parity Score** = |acc(pro-stereotype) − acc(anti-stereotype)|; **0 = stereotype-invariant**.
  - `tuned-legends`: parity = **0.000** across both WinoBias types — perfect.
  - `tuned-regulation`: mean parity = **0.040** (Type-1 = 0.080 — slightly worse than base's 0.040; Type-2 = 0.000). Its accuracy gain comes entirely from pro-stereotype items, widening the pro/anti gap on Type-1.
  - Interpretation: only `tuned-legends` satisfies the fairness criterion the parity diagnostic formalises.
- **Visual layout:** Two side-by-side mini bar charts — one for pro-stereotype accuracy, one for anti-stereotype accuracy — three bars each (base / legends / regulation). Annotate the gap visually with a bracket on the regulation pair. A "Parity = 0" badge over the legends pair (green check).

---

## Slide 17 — CIP Robustness Results

- **Core message:** The aggregate CIP scores compress almost flat (the backbone is already strong), so the *qualitative response character*, not the aggregate, carries the analytic load.
- **On-slide content (the aggregate CIP table):**

| Model | Var. A | Var. B | Var. C | Total / 15 | Robustness |
|---|---|---|---|---|---|
| base | 5/5 | 4/5 | 4/5 | 13/15 | 86.7% |
| tuned-regulation | 5/5 | 4/5 | 4/5 | 13/15 | 86.7% |
| tuned-legends | 5/5 | **5/5** | 4/5 | **14/15** | **93.3%** |

- Failure distribution differs: base fails on `equal_economy` C + `violence_stereotypes` B; `tuned-regulation` fails twice on `mainstreaming_intersectionality` (B + C); `tuned-legends` fails once (`mainstreaming_intersectionality` C).
- Convergent failure: all three models struggle on `mainstreaming_intersectionality` Variant C — likely a property of the *frame* (phased-implementation deferral), not of the models.
- **Honest disclaimer (must appear):** at n=15 the aggregate gap is too small for strong inferential claims; the framework surfaces patterns for replication, not established findings.
- **Visual layout:** The aggregate table above (styled), accompanied by a small 5×3 heat-grid (pillars on Y, variants on X) for each model showing the 0/1 cells. Place the "n=15 caveat" in a muted note box at the bottom.

---

## Slide 18 — The Headline Finding: Complementarity, Not Dominance

- **Core message:** Legends and regulation teach *complementary* compliance competences — routing the model to its task is the deployment question, not which is "better".
- **On-slide content (complementarity routing table):**

| Reasoning competence | Best model | Evidence |
|---|---|---|
| Recognising compliance (entailment) | tuned-legends | GE-NLI 0.929 vs 0.911 |
| Selecting the compliant action | tuned-legends | GE-NEXT 0.967 |
| Detecting violations (contradiction) | tuned-regulation | GE-NLI contradiction subset |
| Classifying into the regulation's ontology | tuned-regulation | GE-CLS 0.928 vs 0.839 |
| Long-form factoid extraction | tuned-legends | GE-QA-Factoid long-answer subset |
| Short-span factoid extraction | tuned-regulation | GE-QA-Factoid short-span subset |

- **Deployment implication:** a deployment whose risk profile foregrounds compliance recognition / compliant-action selection / fairness invariance has a defensible reason to prefer `tuned-legends` despite the 1.2-point aggregate-score lag.
- **Visual layout:** Render the routing table with a colored badge in the "Best model" column (teal for legends, violet for regulation). Visually separate the table into two halves with a subtle background tint — "Legends regime" half (top three rows) vs "Regulation regime" half (bottom three rows reordered if needed). At the bottom, a horizontal "risk-profile router" diagram: a question ("What does your deployment fail at?") → two arrows, one labeled "Misjudging compliance" → legends; one labeled "Misclassifying ontology" → regulation.

---

## Slide 19 — Limitations (Declared Scope, Not Buried Caveat)

- **Core message:** Five concrete limitations bound the study; each one points to a specific replication direction.
- **On-slide content:**
  - **Small test sets:** GE-CLS n=72, GE-NLI n=168, GE-QA-Factoid n=123, GE-WSC n=100, GE-NEXT n=150, CIP n=15.
  - **Single backbone:** only `gpt-4o-2024-08-06`. Backbone generalisability untested.
  - **Discriminative ceiling:** the backbone is already very strong (GE-WSC base = 0.93; tuned-legends GE-NEXT = 0.967), compressing the headroom against which fine-tuning effects can be measured.
  - **GE-NEXT synthetic-text / LLM-evaluator latent affinity:** vignettes and options are LLM-generated; cross-model comparisons remain valid but *absolute* GE-NEXT accuracy should be read as indicative.
  - **Data-and-access deficit:** small test sets + single backbone + closed platform together — the single most consequential operational constraint.
- **Visual layout:** Five-row layout, each row = limitation label (bold) + one-line consequence + a small target icon (📐 small N / 🧬 single model / 🎯 ceiling / 🔁 evaluator affinity / 🔒 access). Avoid bullets — use a clean vertical card stack.

---

## Slide 20 — Conclusion & Future Work

- **Core message:** First empirical test of the Sargsyan-Damiani hypothesis: supported in its central formulation, scoped by complementarity — and the framework is designed to scale to v2.
- **On-slide content:**
  - **Three artifacts delivered:** SustainableQA-derived pipeline · GenderEqGLUE · CIP.
  - **Three conclusions:**
    1. `tuned-regulation` leads aggregate (0.938 vs 0.926 vs 0.904); both fine-tuned models clearly beat base; per-task wins split 3–3.
    2. Hypothesis **supported** in central formulation: legends are strongest on GE-NEXT; GE-NLI directional, GE-WSC parity, CIP qualitative findings all corroborate.
    3. Hypothesis **does not generalise** to ontology classification or short-span factoid recall — legends and regulation teach *complementary* competences.
  - **Future: GenderEqGLUE v2** — ≥500 items per task, harder GE-NEXT items, harder coreference probes (GAP, BUG), multi-backbone replication.
- **Visual layout:** Three-column "Contributions / Conclusions / Next" layout. Each column has 3 rows of one-line takeaways with consistent iconography. A small "v2 →" arrow at the right edge pointing off-slide signals continuation.

---

## Slide 21 — Thank You / Q&A

- **Core message:** Open for questions; keep contact and paper anchors visible.
- **On-slide content:**
  - "Thank you — questions?"
  - Authors: Bylyshi · El-Khazri · Ouardi
  - Contact: `{fatmir.bylyshi, hicham.elkhazri, ilyass.ouardi}@studenti.unimi.it`
  - Affiliation: Department of Computer Science, University of Milan
- **Visual layout:** Minimalist. Large "Questions?" centered. Authors + emails in a small block. Optional decorative element: the 3-bar teaser silhouette from Slide 1 (visual bookend).

---

# Backup Slides (Post-"Thank You", for Q&A only)

## B1 — Full Pipeline Diagram (paper Figure 2 reproduced for Q&A)

- **Core message:** End-to-end pipeline with both branches expanded.
- **On-slide content:** The complete 7-stage version — preprocessing → legends generation (legend branch only) → six-class pillar classification → two-stage span extraction → factoid + non-factoid Q&A generation → fine-tuning, with both branches' line counts, pillar distributions, and JSONL formats.
- **Layout:** Reproduce `pipeline_combined.pdf` layout but redesigned for projection (thicker lines, larger labels).

## B2 — Common Evaluation Base Composition

- **Core message:** 217 EU passages held out from training across four documents, stratified per-pillar.
- **On-slide content:** CEB per-pillar table (paper Table 2): `violence_stereotypes` 72 (24/24/24) · `leadership_participation` 45 (15/15/15) · `funding_global_action` 21 (7/7/7) · `equal_economy` 18 (6/6/6) · `mainstreaming_intersectionality` 11 (4/3/4) · `unknown` 50 (16/17/17) · **Total 217 (72/72/73)**.
- **Layout:** The table, plus an "anticipated reviewer concern" callout: *the three minority pillars (`equal_economy`, `mainstreaming_intersectionality`, `funding_global_action`) carry low support — per-class F1 for n<30 is flagged low-confidence.*

## B3 — Cross-Task Pillar Gains

- **Core message:** Where fine-tuning helps most, per pillar.
- **On-slide content:** Table 4 from the paper — per-pillar performance gains (winning fine-tuned model − base) across GE-CLS, GE-NLI, GE-QA, GE-NEXT, with the n=6 / n=4 minority-pillar caveat.
- **Layout:** Heatmap-styled table where darker green = larger positive gain.

## B4 — Full 45-Cell CIP Matrix

- **Core message:** Complete CIP scoring matrix (paper Table 7).
- **On-slide content:** All 5 pillars × 3 variants × 3 models = 45 binary cells, plus per-pillar totals. Highlight the two `tuned-regulation` failures concentrated on `mainstreaming_intersectionality` (B + C) and the convergent failure on `mainstreaming_intersectionality` Variant C across models.
- **Layout:** 15-row table with checkmark/cross cells.

## B5 — Example GE-NEXT Vignette (Inés Lobato)

- **Core message:** A concrete look at what GE-NEXT items look like.
- **On-slide content:** The Inés Lobato vignette (paper Box, `box:ge_next_example`):
  - **Vignette:** Inés Lobato, Head of People at a Madrid logistics company with 380 employees, has completed the firm's first salary audit following the transposition of the Pay Transparency Directive. The audit reveals a 9% unexplained gender pay gap concentrated in the operations division, affecting 42 women. Inés must propose a remediation plan to the board.
  - **A.** Company-wide statement (*performative*)
  - **B.** Defer to next fiscal year (*cost-optimising*)
  - **C.** 24-month banded remediation plan with quarterly adjustments + Works-Council disclosure (***substantive-compliant — gold***)
  - **D.** Six-month external diversity-training programme (*orthogonal*)
  - **Label: C**
- **Layout:** Vignette text in a card at top; four options as labeled cards below with their distractor-type tags color-coded. Gold option visually highlighted.

## B6 — CIP Variant Construction (Single Example)

- **Core message:** What A / B / C look like on the same underlying scenario.
- **On-slide content:** Reproduce the `cip_protocol_variants_leadership_participation.pdf` figure logic — same semantic problem under three lexical/framing conditions.
- **Layout:** Three side-by-side text columns labeled A / B / C with the regulatory-vocabulary terms highlighted in A, stripped in B, and embedded in an antagonist's voice in C.

## B7 — Anticipated Question: "Why not just use SHAP/LIME?"

- **Core message:** Each canonical explainability method assumes a level of model access FineTuneDB does not grant.
- **On-slide content:** Four canonical methods, why each is blocked:
  - **SHAP** — needs gradients or large per-instance evaluation budgets.
  - **LIME** — needs hundreds of forward passes per explanation; impractical on a metered, unbatched API.
  - **Integrated Gradients** — needs gradients (blocked).
  - **Attention rollout** — needs access to attention weights through the transformer stack (blocked).
  - FineTuneDB Studio surfaces **only generated text** → CIP borrows LIME's perturbation logic at the text level.
- **Layout:** Four crossed-out method cards + one highlighted CIP card explaining the substitution logic.

## B8 — Anticipated Question: "What's a 'legend' look like?"

- **Core message:** Concrete shape of the training signal.
- **On-slide content:** The legend-generation system prompt structure (from `lst:legend_system_prompt`):
  - **Title** — short, evocative.
  - **Setting** — organisation, sector, country (varied across legends).
  - **Characters** — 3–5 named characters with role + one-line description.
  - **The Story** — 400–600 words, ≥1 direct-speech dialogue, concrete gender-equality gap addressed by specific measures, measurable positive outcome, explicit acknowledgement of the Strategy.
  - Content rules: focus on one regulation point, cite "EU Gender Equality Strategy 2020–2025" at least once, no reused sectors/countries/character names.
- **Layout:** Side-by-side: left column = format spec (the bullet list above); right column = a stylised mock legend card showing each element.

---

# Timing Budget (~20-min slot, recommended)

| Section | Slides | Target Duration |
|---|---|---|
| Opening + Motivation (1–4) | 4 | 3 min |
| Contributions + Related Work (5–7) | 3 | 2 min |
| Methodology (8–10) | 3 | 3 min |
| Benchmark + CIP (11–13) | 3 | 3 min |
| Results (14–17) | 4 | 5 min |
| Complementarity + Limits + Conclusion (18–20) | 3 | 3 min |
| Q&A (21) | 1 | open |
| **Total** | **21** | **≈ 19 min** |

---

# Design Cues for the Next (Artifact) Phase

A few cross-slide design constants the visual phase should lock in early so the deck reads as a single artefact:

- **Three-color model palette:** keep `base` = neutral grey, `tuned-legends` = teal, `tuned-regulation` = violet across every chart, table cell, and badge (matches the paper's Figure 1 teaser).
- **Three-artifact accent palette:** keep one accent color each for Pipeline / GenderEqGLUE / CIP and reuse those on every slide that touches that artifact.
- **Pillar iconography:** the five EU pillars (`violence_stereotypes`, `equal_economy`, `leadership_participation`, `mainstreaming_intersectionality`, `funding_global_action`) recur across at least six slides — assign each a small icon early and reuse.
- **Claim-style titles:** every slide title is the *message*, not the *topic*. Slide 14 is "Headline results" only in this blueprint; the actual on-slide title should read something like *"`tuned-regulation` wins aggregate; per-task wins split 3–3."*
- **One idea per slide:** Slide 11 (the GenderEqGLUE table) is the densest; the visual phase should consider whether the open-vs-closed-book donut is essential or should slide off to a backup. Everything else is one idea per slide.
- **No animations:** if step-by-step build is needed (e.g., the parallel-pipeline reveal on Slide 8), use multiple slides rather than animation — robust to PDF fallback.

