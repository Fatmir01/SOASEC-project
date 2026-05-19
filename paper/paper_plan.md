# Paper Plan — *The Legend Challenge*

**Working title (candidate):** *The Legend Challenge: Embedding Ethical
Compliance into LLMs through Champion Narratives in the Gender Equality Domain*

**Source corpus this plan is grounded in:** `pipeline.md` ·
`genderEqGLUE_final_report_final.md` · `aggregate.json` ·
`SOASEC_Legend_Challenge_mod.pdf` (the challenge spec, Sargsyan & Damiani 2025
referenced as the central hypothesis) ·
`Ethical_AIRegulations_PaperErnestoGohar_final.pdf` (Sargsyan & Damiani 2025,
full text) · `genderequalitystrategy20202025.pdf` (target regulation).

**Convention.** Every directive below cites the document section that backs it.
Items the source does not cover are tagged `[MISSING IN SOURCE]` with the
resolution the writing agent must obtain before drafting.

---

## 0. Executive Summary (lock these before writing)

| Element | Locked value |
|---|---|
| Backbone model | `gpt-4o-2024-08-06` |
| Platform | FineTuneDB Studio (GUI-only, no logits/log-probs/internals) — `pipeline.md` §5.2 + §7 preamble |
| Comparison set | `base` (no domain FT) · `tuned-legends` · `tuned-regulation` |
| Headline benchmark | GenderEqGLUE — 5 tasks, unweighted-mean aggregate — `pipeline.md` §6.1 |
| Aggregate GenderEqGLUE Score | base **0.9036** · tuned-legends **0.9264** · tuned-regulation **0.9379** — `aggregate.json` |
| Central hypothesis | Sargsyan & Damiani (2025): To comparatively explore methods for embedding ethical AI directly into models. Using examples from gender equality, we demonstrate a novel approach to embedding regulations by using regulation text to generate "champion" positive examples, called "legends," that will inform the LLM model decision-making.|
| Verdict on hypothesis | Narrowly supported on **compliance-recognition** + **compliant-action selection** axes; does **not** generalise to ontology recognition or short-span factual recall — `final_report.md` §3.3, §6 |

---

## 1. Counterintuitive Planning (do this before story polish)

### 1.1 Rejection-risk table (sorted by Probability × Impact)

| # | Likely reviewer comment | P (1–5) | I (1–5) | P×I | Preemption move | Evidence already in source |
|---|---|:-:|:-:|:-:|---|---|
| R1 | "GenderEqGLUE is GLUE renamed; limited novelty." | 5 | 5 | 25 | Lead Methodology §6 with the **GLUE-analogue mapping table** showing what is *preserved* (input/output template, metric family) vs what is *generalised* (semantic anchoring, label space). It is something we want to keep our benchmark very close with Glue and SuperGlue. It's not rejection risk but what we want. | `pipeline.md` §6.1 task table; §6.2 "Task design: direct comparison with base glue tasks";|
| R2 | "n is small; gaps are within noise." | 5 | 5 | 25 | Treat as honest limitation, not flaw. (a) Pre-register the §6.10 protocol (bootstrap 95% CIs + McNemar) in Experimental Setup; (b) Report **all nine pairwise McNemar p-values** including non-significant ones (final report §2 table) to demonstrate honest reporting; (c) Pivot narrative from what model is better at doing what to the design of every step (train set generation, benchmark design, explainability) ||
| R3 | "Synthetic vignettes + LLM evaluator on GE-NEXT — latent affinity confound." | 4 | 4 | 16 | Treat as honest limitation, not flaw. Place §6.12.6 limitation **in the Experimental Setup**, not buried in Limitations. State mitigations explicitly (multi-generator-LLM mixing, manual paraphrasing of QC sample, fixed-seed shuffling of options); argue cross-model comparisons remain valid because all 3 models face identical items. | `pipeline.md` §6.12.6 |
| R4 | "No Cohen's κ — label noise unmeasured." | 4 | 3 | 12 | Frame §6.12.1–§6.12.3 honestly: internal-instrument scope, single-annotator pipeline, stratified manual spot-check (≈60 passages, 10/class). State the three preserved validities (per-class F1 = upper bound; within-CEB cross-task = OK; cross-model on same task = OK). | `pipeline.md` §6.12.1–§6.12.3 |
| R5 | "SHAP/LIME/IG would have been the right interpretability tool." | 4 | 3 | 12 | Treat as honest limitation, not flaw. Open §7 (Explainability) with the access constraint (FineTuneDB GUI-only: no logits, no internals, no batched API). Enumerate which methods this forecloses (SHAP, LIME, IG, attention rollout) and *why* (model internals or hundreds of calls/instance). Position CIP as the method that the access regime *admits*, not as a substitute for what is unavailable. | `pipeline.md` §7 preamble, §7.1 |
| R6 | "Backbone is too capable; ceiling compresses signal." | 4 | 3 | 12 | Treat as honest limitation, not flaw. Show GE-WSC ceiling (≥93% base) and CIP probing baseline (base = 86.7%) to argue effect sizes are floor-bounded by backbone strength. State the v2 path: harder coreference probe (GAP/BUG); harder GE-NEXT items. | `final_report.md` §5.3; `pipeline.md` §7.5 (probing limitations) |
| R7 | "Hypothesis support is qualitative; no statistically significant legends > regulation gap." | 4 | 4 | 16 | **Pre-emptively concede this** in Results and Discussion. State the power requirement explicitly: ~350–500 items to resolve. Pivot to **qualitative complementarity** as the substantive finding. | `final_report.md` §2 power note; §3.3 complementarity table |

### 1.2 Minimal Defensible Claim (the smallest claim that survives attack)

> When evaluated on a single backbone (the GPT-4o family) fine-tuned via
> FineTuneDB Studio under size-matched JSONL corpora, the results on the
> GenderEqGLUE benchmark reveal that the two fine-tuning regimes teach
> complementary competencies. The regulation-based regime secured a 1.2-point
> lead in the aggregate score, primarily winning on tasks that match the
> regulation's internal thematic and lexical structure (GE-CLS, GE-QA
> short-span). However, the legend-based regime demonstrated superior reasoning
> in applied scenarios: it improved upon both the base and regulation models on
> GE-NEXT (compliant-action selection), and tied or led on the two tasks
> designated a priori as central tests of the Sargsyan-Damiani hypothesis
> (GE-NLI and GE-WSC parity).


### 1.3 Fallback Narrative (predefined, do not improvise)

If a reviewer attacks the headline aggregate or the lone-significant-test
framing, pivot to **qualitative complementarity** (Rule 5 fallback type: *better
behaviour on hard subsets*):

| Reasoning competence | Best model | Evidence |
|---|---|---|
| Recognising compliance (entailment) | `tuned-legends` | `final_report.md` §3.3; GE-NLI 0.9286 vs 0.9107 |
| Selecting compliant action | `tuned-legends` | `final_report.md` §3.1; GE-NEXT McNemar p=0.0312 |
| Detecting violations (contradiction) | `tuned-regulation` | `final_report.md` §3.3 |
| Ontology classification | `tuned-regulation` | `aggregate.json` GE-CLS 0.9284 vs 0.8393 |
| Gender-parity invariance | `tuned-legends` | `final_report.md` §3.3 |
| Long-form factoid extraction | `tuned-legends` | `final_report.md` §3.3 |
| Short-span factoid extraction | `tuned-regulation` | `final_report.md` §3.3 |

### 1.4 Honest weakness (Rule 4 — Buy trust with one declared failure)

**Chosen failure case to highlight:** we need more data for tuning and for
benchmark evaluation. better access to the model internals and more compute
power. 

---

## 2. Story Design

### 2.1 TCICA (Task → Challenge → Insight → Contributions → Advantage)

**Task.** Empirically test whether **narrative-exemplar ("legend") fine-tuning**
embeds regulatory compliance into an LLM more effectively than fine-tuning on
the **raw regulatory text**, on a single regulatory domain (EU Gender Equality
Strategy 2020–2025, COM(2020) 152 final). — `pipeline.md` lines 1–28;
`SOASEC_Legend_Challenge_mod.pdf` p.1.

**Challenge.** Three converging gaps make a direct test difficult:
1. **Hypothesis is untested.** Sargsyan & Damiani (2025) propose legends as a
   way to *embed ethics as inductive bias rather than stylistic veneer* but
   provide neither empirical evaluation nor a measurement instrument. —
   `Ethical_AIRegulations_PaperErnestoGohar_final.pdf` §VI; `pipeline.md` §7.1.
2. **Benchmarks are domain-agnostic.** GLUE/SuperGLUE measure general-purpose
   NLU; no existing benchmark targets *compliance reasoning* (recognising
   compliance, selecting compliant actions, generalising across the pillars of a
   regulation). — `pipeline.md` §6 preamble.
3. **Industrial fine-tuning platforms foreclose standard XAI.** FineTuneDB
   Studio is GUI-only — generated text is the sole output, no logits, no
   internals, no batched API. SHAP, LIME, Integrated Gradients, attention
   rollout all require what the platform does not expose. — `pipeline.md` §7
   preamble; §7.1.

**Insight.** Three observations align:
- Two models can reach the same aggregate accuracy via qualitatively distinct
  reasoning pathways; aggregate scores cannot discriminate **inductive bias**
  from **lexical mimicry**. — `pipeline.md` §7.4.3, §7.4.5.
- The competence the hypothesis is really about is **compliance reasoning**, not
  factual recall. So the benchmark must include tasks built to expose it
  (compliance entailment, compliant-action selection) alongside the standard NLU
  palette. — `pipeline.md` §6.5 ("central task"), §6.8 ("most direct probe").
- The access constraint that forecloses gradient-based XAI is itself a feature:
  it is the realistic deployment regime for ethics-tuned models in industry. A
  **behavioural-only** explainability protocol is what production deployments
  will actually require. — `pipeline.md` §7.1 (mid).

**Contributions.** Three concrete technical novelties:
1. **GenderEqGLUE — a 5-task benchmark for regulatory-compliance reasoning
   anchored in the EU Gender Equality Strategy 2020-2025.** GE-CLS (SST-2 ↦
   6-class pillar classification), GE-NLI (MNLI/RTE ↦ compliance entailment),
   GE-QA (SQuAD + BoolQ ↦ regulation reading comprehension), GE-WSC (WinoBias
   as-is ↦ stereotype-aware coreference with Gender Parity Score), GE-NEXT (COPA
   ↦ compliant-action selection with a four-type distractor typology). Three
   tasks share a single **Common Evaluation Base (CEB)** of 217 EU passages from
   four held-out documents (Roadmap for Women's Rights 2025; GAP III 2021–2025;
   Council Conclusions on Closing the Gender Pay Gap 2019; Directive (EU)
   2022/2381 on Women on Boards), stratified 1/3 each into CEB-CLS / CEB-QA /
   CEB-NLI by `sklearn.train_test_split` with `seed=42`. — `pipeline.md` §6.1,
   §6.2, §6.3.
2. **A SustainableQA-derived dataset-construction pipeline** for converting
   unstructured regulatory text and synthetic legends into matched closed-book
   fine-tuning corpora. Stages: PDF→Markdown (Marker library); regex Markdown
   cleaning (29.4% size reduction with zero content loss, 16 headings
   preserved); two-stage segmentation (5 thematic parts ↔ regulation pillars;
   `max_words=350` sub-segmentation); six-class LLM pillar classification
   (Gemini 3 Pro); two-stage LLM span extraction (high-recall extractor →
   contextual verification + thematic clustering); factoid + non-factoid Q&A
   generation; JSON→JSONL conversion with a fixed system prompt and a deliberate
   **closed-book** chat format. — `pipeline.md` §2.1–§2.3, §4.1–§4.3, §5.1.
3. **Counterfactual Input Probing (CIP) — a behavioural-only explainability
   framework for closed fine-tuning environments.** One prediction per pillar
   (×5) is subjected to three controlled input variants — *Variant A* original
   baseline; *Variant B* keyword-stripped (regulatory vocabulary removed,
   semantics preserved); *Variant C* adversarially framed (five named frames:
   meritocracy camouflage, cost-efficiency pressure, cultural relativism,
   phased-implementation deferral, scientific-integrity framing). 45 evaluations
   total (5 pillars × 3 variants × 3 models). Binary scoring on position
   maintenance produces both quantitative robustness rates and qualitatively
   distinct *reasoning pathways* (regulatory-authority invocation vs structural
   reasoning vs principled-rebuttal mode). — `pipeline.md` §7.2.1, §7.2.2, §7.3,
   §7.4.

**Advantage.** The full triple — benchmark + pipeline + CIP — produces a richer
verdict than any single component could. The benchmark establishes the headline
numbers; the pipeline supplies the matched corpora that make the comparison fair
(size-matched JSONL, identical system prompt, identical closed-book format); CIP
surfaces the *mode* of reasoning that aggregate scores conceal. The combined
finding — **`tuned-regulation` leads aggregate by 1.2 pts; `tuned-legends` wins
on base and `tuned-regulation` on 3 central gender equality tasks; CIP shows
`tuned-legends` is the only model that engages adversarial frames analytically
rather than authoritatively** — is more informative about what each training
regime actually teaches than the aggregate would suggest.

### 2.2 Module Motivation Mapping (drives Methodology subsection structure)

| Module | What it does | Why it's needed | Technical advantage |
|---|---|---|---|
| **§2 Preprocessing** | PDF→MD via Marker; regex cleanup; 2-stage segmentation (5 thematic parts × `max_words=350`) | Raw EU PDFs are layout-noisy; downstream LLM Q&A needs semantically coherent, length-bounded passages | 29.4% size reduction, all 16 headings preserved, no content loss (`pipeline.md` §2.2) |
| **§3 Legends generation** | 5 thematic parts × 3 LLMs (Gemini, Copilot, ChatGPT) ⇒ 15 legends; structured prompt enforcing title/setting/characters/story format with measurable outcome | Sargsyan-Damiani's hypothesis requires *narrative exemplars*; multi-LLM mix maximises stylistic diversity for FT robustness | Each legend instantiates the *identify gap → design measure → implement → measurable outcome* four-beat arc that GE-NEXT later probes (`pipeline.md` §3, §6.8) |
| **§4.1 Pillar classification** | 6-class LLM classifier (Gemini 3 Pro): 5 pillars + `unknown` | The same taxonomy must label legends, regulation, CEB; downstream GE-CLS uses this label space | Single taxonomy unifies training and evaluation labels |
| **§4.2 Span extraction (2-stage)** | Stage 1 high-recall LLM extractor; Stage 2 contextual verification + thematic clustering with `Individual` fallback | SustainableQA's NER+regex multi-stage stack is unnecessary on clean regulatory/legend text; LLM is sufficient | Spans are verbatim, deduplicated, grouped — enables both single-span and group-level Q&A |
| **§4.3 Q&A generation** | Factoid (verbatim-span answers) + non-factoid (1–4 sentence descriptive answers); both via Gemini 3 Pro with rule-checked output | Two question types cover both fact recall and explanatory reasoning | Validation against Context (Rule 2) and mandatory self-correction checklist (`pipeline.md` §4.3.1) |
| **§4.3 Closed-book design** | Training JSONL drops the passage; only `(question, answer)` pairs are kept | Open-book training teaches reading comprehension, not regulatory internalisation; the hypothesis is about baking ethics into weights | The chosen format isolates the *internalisation* signal the hypothesis predicts (`pipeline.md` §4.3 "Closed-book format") |
| **§5 Fine-tuning** | JSON→JSONL conversion (identical system prompt across both datasets, size-matched line counts); FineTuneDB Studio FT of the chosen backbone | Per challenge point (7): the only variable between the two FT runs must be the **content** of the user/assistant pairs | Comparison is clean: same backbone, same system prompt, same format, same line count — only the corpus differs |
| **§6 GenderEqGLUE** | 5 tasks, 3 from CEB, 1 from WinoBias as-is, 1 LLM-synthesised; common eval protocol (temperature 0, fixed prompts) | GLUE/SuperGLUE are domain-agnostic; need a benchmark that probes regulatory-compliance reasoning | Each task is a deliberate adaptation of a named GLUE/SuperGLUE base task — direct comparability with the NLU literature |
| **§7 Counterfactual Input Probing** | Variant A/B/C protocol on 1 item per pillar; binary scoring; qualitative response analysis | Aggregate accuracy cannot discriminate inductive bias from lexical mimicry; standard XAI is foreclosed by FineTuneDB | Surfaces the *reasoning pathway* each model uses — the qualitative dimension on which the hypothesis really rests (`pipeline.md` §7.4.5–§7.4.6) |

This table maps 1:1 to Method subsections (each row = one subsection) and to
ablation thinking (every module is independently described and has a per-row
motivation that the writing agent can lift directly).

---

## 3. Claim-to-Evidence Mapping (every claim has a number)

| Claim (must appear in Abstract / Introduction / Results) | Evidence in source | Asset to cite |
|---|---|---|
| C1. `tuned-regulation` leads aggregate at GenderEqGLUE 0.9379, beating tuned-legends 0.9264 and base 0.9036 | `aggregate.json` `genderEqGLUE_score`; `final_report.md` §1 | **Table 1** (5-task headline + aggregate) |
| C2. Wins split 3–3 between the two FT regimes; base wins none | `final_report.md` §1 "wins-per-task tally"; `aggregate.json` `wins_per_model` | **Table 2** (wins per task) |
| C3. The **only** McNemar-significant pairwise gap in the benchmark is GE-NEXT base vs tuned-legends, p=0.0312, b=0/c=6 | `final_report.md` §2 table; `aggregate.json` `significance_summary.GE-NEXT` | **Table 3** (full pairwise McNemar matrix) |
| C4. GE-NLI (compliance recognition) is directionally consistent with the hypothesis but underpowered: tuned-legends 0.9286 vs base 0.8988 (Δ=+3.0 pts); p=0.180 vs base; ≈3× test items needed | `aggregate.json` GE-NLI; `final_report.md` §2 power note | **Table 1 row 2** + power-note text box in §2 |
| C5. GE-WSC ties at 0.96 (tuned-legends = tuned-regulation, both > base 0.93); the parity-score diagnostic on the anti-stereotype subset is itself part of the GE-WSC score per §6.7 | `aggregate.json` GE-WSC; `pipeline.md` §6.7 metric definition | **Table 1 row 4** |
| C6. CIP aggregate robustness: base = tuned-regulation = 13/15 (86.7%); tuned-legends = 14/15 (93.3%). Qualitatively distinct failure modes despite numerical tie. | `pipeline.md` §7.3 Table 7.2; §7.4.1 | **Table 7** (CIP aggregate) + **Table 6** (CIP per-pillar) |
| C7. `tuned-regulation` collapses on `mainstreaming_intersectionality` (1/3) where base reaches 3/3; `tuned-legends` recovers Variants A and B on this pillar. Direct evidence of representational binding to vocabulary in regulation FT. | `pipeline.md` §7.3 Table 7.1; §7.4.3 (paragraphs on MI failure); §7.4.4 (legends recovery on MI) | **Table 6** rows 10–12; **Discussion §X** qualitative excerpts |
| C8. The legend-tuned model engages adversarial frames via *active frame analysis* (identifying rhetorical structure, naming the flaw) — a reasoning *mode* the other two models do not exhibit. | `pipeline.md` §7.4.4; §7.4.5 (synthesis) | Discussion: paired response excerpts (regulation vs legends on `leadership_participation` Variant C: "Directive's 40% threshold not conditional on underperformance" vs "meritocracy argument conflates current performance with optimal future composition") — `pipeline.md` §7.4.3, §7.4.4 |
| C9. The dominant failure mode the legends protect against on GE-NEXT is *orthogonal* distractors (45.5% of base errors; 50.0% of regulation errors), not cost-deferral as the §6.8 design hypothesised. This refines the Sargsyan-Damiani framing empirically. | `final_report.md` §3.1; §6 conclusion 4 | **Figure / Table 4** (per-distractor-type error rate) |
| C10. Closed-book training format is a deliberate design choice tied to the hypothesis: open-book FT teaches reading comprehension, closed-book FT forces internalisation. | `pipeline.md` §4.3 "Closed-book format" subsection | Methodology §5 design-rationale box |
| C11. FineTuneDB GUI-only access forecloses SHAP, LIME, Integrated Gradients, attention rollout — CIP is the methodology the access regime admits. | `pipeline.md` §7 preamble; §7.1 | Methodology §7 opening paragraph |

**Coverage check:** Every contribution (§2.1 above) is provable from at least
three independent claim rows. No row depends on a single sentence.

---

## 4. Section Blueprint — exact contents

> The writing agent treats each bullet as a directive. Numbers, tables, and
> figure IDs reference Asset Allocation §5.

### 4.1 Abstract (≈220–260 words)

Single paragraph. Order:
1. **One sentence framing** — Sargsyan & Damiani (2025) proposed legends as a
   way to embed regulatory ethics; the proposal has not been empirically tested.
2. **One sentence task** — We compare legend-based FT against regulation-text FT
   on a single regulation (EU Gender Equality Strategy 2020-2025) with a single
   backbone, holding the system prompt, training format, and JSONL line count
   constant.
3. **One sentence on the benchmark** — Introduce GenderEqGLUE: five tasks
   (GE-CLS, GE-NLI, GE-QA, GE-WSC, GE-NEXT) adapted one-to-one from
   GLUE/SuperGLUE templates and built on a held-out Common Evaluation Base of
   217 EU passages.
4. **One sentence on CIP** — Introduce Counterfactual Input Probing as the
   behavioural-only explainability protocol designed for closed (GUI-only)
   fine-tuning environments where SHAP/LIME/IG/attention rollout are
   inaccessible.
5. **Headline numbers** — `tuned-regulation` leads aggregate (0.938);
   `tuned-legends` is second (0.926); base last (0.904). The wins split 3–3.
6. **The one significant finding** — On GE-NEXT the §6.8 hypothesis-central
   task, tuned-legends is the **better** model.
7. **Synthesis sentence** — The two regimes teach **complementary competences**:
   legends teach compliance recognition and compliant-action selection;
   regulation text teaches ontology recognition and short-span factual recall.
8. **Closing — actionable takeaway** — Deployment choice should be governed by
   the dominant risk profile of the application.



### 4.2 Introduction (2 pages, 5 paragraphs)

¶1 — **The regulatory-compliance problem in LLM deployment.** Open from Sargsyan
& Damiani's framing of the implementation conflict (middle management's
cost-minimising incentives vs regulatory directives, `sargsyan §II`). Make the
case that regulation embedding is a live deployment problem.

¶2 — **The Sargsyan-Damiani proposal in detail.** Describe legends as "champion
profiles" — idealised exemplars derived from regulation that train the model to
recognise compliance as a *capacity*, not a *lookup*. State the unstated
empirical question: *does legend FT in fact produce a different model than
regulation-text FT?*

¶3 — **Why prior work cannot answer this.** see Sargsyan & Damiani's framing


¶4 — **Our three contributions** (the §2.1 contributions list, in the order:
pipeline ⇒ benchmark ⇒ CIP). One sentence per contribution. End the paragraph
with the **minimal defensible claim** (§1.2 above) verbatim.

¶5 — **Roadmap.** §2 pipeline; §3 benchmark construction; §4 results; §5 CIP; §6
discussion; §7 limitations; §8 conclusion.

**Place the Teaser Figure (Figure 1) at the top of the first page** — see Asset
Allocation §5.

### 4.3 Background / Related Work (1 page)

Four subsections, each one short paragraph:
- **§3.1 Embedding ethics in LLMs.** Sargsyan & Damiani 2025; alternative
  approaches (post-hoc auditing, Rules-as-Code, digital-ready legislation — all
  cited inside the Sargsyan paper §V; the writing agent can pull citations 17–24
  from that section's bibliography). `[MISSING IN SOURCE: full bibliography
  numbers; obtain from the PDF or sketch placeholders.]`
- **§3.2 NLU benchmarks and their domain-agnostic limit.** GLUE (Wang et al.
  2018, cited in `pipeline.md` §6); SuperGLUE; the regulatory-NLU gap.
- **§3.3 Domain QA generation pipelines.** SustainableQA (Wattenberg et al.,
  arXiv:2508.03000) — the framework GenderEqGLUE's pipeline adapts. Cite by URL;
  note explicitly what is preserved vs simplified (no table handling; LLM
  replaces NER+regex).
- **§3.4 Explainability under closed access.** SHAP (Lundberg & Lee 2017), LIME
  (Ribeiro et al. 2016), Integrated Gradients (Sundararajan et al. 2017),
  attention rollout (Abnar & Zuidema 2020) — all named in `pipeline.md` §7.1;
  each requires what FineTuneDB Studio does not expose. Position behavioural
  probing (LIME's perturbation logic, executed at text level only) as the
  available alternative.

### 4.4 Methodology (the longest section: 6–8 pages)

Follow Module Motivation Mapping §2.2 row order. Per-subsection structure:
**motivation → design → technical advantage**, ≈ 1 paragraph each.

**§4.1 Pipeline overview.** Insert **Figure 2 (the pipeline diagram)** here; do
*not* try to explain the pipeline in prose first. The figure is the visual
backbone.

**§4.2 Preprocessing.** PDF→MD (Marker); regex cleaner (state the 29.4%,
64,703→45,697, 16 headings); 2-stage segmentation (5 thematic parts ↔ pillars;
`max_words=350`). Quote the five pillar names verbatim from `pipeline.md` §2.3.

**§4.3 Legends generation.** Three LLMs × five thematic parts = 15 legends.
Quote the system prompt verbatim (boxed code block from `pipeline.md` §3 lines
232–265). Emphasise the four-beat narrative arc that GE-NEXT later probes.

**§4.4 Six-class pillar classification.** Classifier prompt verbatim from
`pipeline.md` §4.1. Note the deliberate addition of `unknown` as a rejection
class.

**§4.5 Two-stage span extraction.** Verbatim spans (length 1–8 words);
contextual verification + thematic clustering with `Individual` fallback. Insert
**Code Snippet 1** (span-extractor system prompt, `pipeline.md` §4.2 lines
400–429).

**§4.6 Q&A generation (Factoid + Non-Factoid).** Insert **Q&A Example Box** (the
two JSON examples from `pipeline.md` §4.3 lines 656–672 — "two women-led
solar-maintenance micro-enterprises" and the Hugo second-earners case). Explain
the closed-book rationale via the boxed sub-subsection from `pipeline.md` §4.3
("Closed-book format" / "Why closed-book fits our specific challenge").

**§4.7 JSON→JSONL conversion + fine-tuning.** Insert **Code Snippet 2** (the
JSONL chat-format example from `pipeline.md` §4.3 lines 686–701). State the
size-matched line-count constraint (challenge point 7). from `pipeline.md` §5.1
lines 785-810. State the backbone.

### 4.5 Experimental Setup — GenderEqGLUE (3–4 pages)

**§5.1 Benchmark overview.** Insert **Table 0** (the §6.1 task table: Task /
Description / GLUE analogue / Source / Metric). State the unweighted-mean
aggregation rule.

**§5.2 GLUE-analogue mapping (R1 preemption).** Walk through the five mappings:
SST-2↦GE-CLS, MNLI/RTE↦GE-NLI, SQuAD+BoolQ↦GE-QA, WSC/Winogender↦GE-WSC,
COPA↦GE-NEXT. For each, state what is preserved (input/output template, metric
family) and what is generalised (semantic anchoring, label space). Lift directly
from `pipeline.md` §6.2.

**§5.3 Common Evaluation Base.** Four source documents (Roadmap 2025; GAP III;
Council Conclusions on Pay Gap 2019; Directive 2022/2381). 217 passages. Insert
**Table CEB-1** (per-pillar distribution from `pipeline.md` §6.3.2). State the
stratified 1/3 split with `seed=42` and insert **Code Snippet 3** (the
`train_test_split` block from `pipeline.md` §6.3.3 lines 978–1009).

**§5.4 Per-task construction.** One subsection per task, each ½–¾ page:
- **§5.4.1 GE-CLS** — 72 passages directly, fixed system prompt (`pipeline.md`
  §6.4); Macro-F1 metric.
- **§5.4.2 GE-NLI** — five-stage construction (hypothesis extraction → premise
  generation → contradiction perturbation → neutral cross-pillar pairing →
  balancing). Final 168 triples (56 per class). Insert **JSON example** from
  `pipeline.md` §6.5 lines 1422–1432.
- **§5.4.3 GE-QA** — Factoid (SQuAD-style) + Bool (BoolQ-style). Insert **Bool
  QA construction box** (Method A direct paraphrase vs Method B perturbed claim,
  from `pipeline.md` §6.6.3). Note the deliberate exclusion of "passage silent
  on the claim" as a Bool answer (would conflict with GE-NLI neutral).
- **§5.4.4 GE-WSC** — WinoBias as-is, four subsets (`type1_pro`, `type1_anti`,
  `type2_pro`, `type2_anti`). Accuracy + Gender Parity Score. State the
  domain-mismatch caveat (`pipeline.md` §6.12.5) here, not in Limitations.
- **§5.4.5 GE-NEXT** — Vignette + four-option distractor typology (performative
  / cost-optimising / orthogonal / substantive-compliant). Insert **GE-NEXT
  Example Box** (the Inés Lobato example verbatim from `pipeline.md` §6.8 lines
  1806–1828). Place the §6.12.6 synthetic-construction caveats in this section
  (R3 preemption).

**§5.5 Statistical protocol.** Bootstrap 95% CIs (2000 resamples, seed=42) on
headline metrics. McNemar's test on per-item correctness for pairwise model
comparisons. Insert this paragraph **before** Results so the reader knows the
test protocol was pre-registered — R2 preemption.

### 4.6 Results (3–4 pages)

**§6.1 Aggregate.** Insert **Table 1** (5 tasks × 3 models + GenderEqGLUE
column). Two paragraphs: (a) `tuned-regulation` leads aggregate by 1.2 pts over
tuned-legends, 3.4 pts over base; (b) the wins split 3–3, base wins none.

**§6.2 Per-task analysis.** Five short subsections (one paragraph each):
- **§6.2.1 GE-CLS** — `tuned-regulation` dominates (Macro-F1 0.928 vs 0.839 vs
  0.833). Note minority-pillar variance flagged low-confidence.
- **§6.2.2 GE-NLI** — `tuned-legends` leads numerically (0.929 vs 0.911 vs
  0.899). McNemar p=0.180 (NS). Frame this as the **directional core finding**
  that needs ~3× the test items to clear formal significance.
- **§6.2.3 GE-QA** — `tuned-regulation` leads aggregate (0.944 vs 0.938 vs
  0.929). The factoid-EM vs factoid-F1 gap diagnostic for tuned-legends (format
  mismatch, not knowledge loss — `pipeline.md` §6.6.7).
- **§6.2.4 GE-WSC** — tuned-legends = tuned-regulation = 0.96; base = 0.93.
  Gender Parity diagnostic favours tuned-legends per `final_report.md` §3.3.
- **§6.2.5 GE-NEXT — the headline finding.** Insert **Table 3** (the 9-row
  McNemar matrix). `tuned-legends` 0.967 vs base 0.927: McNemar p=0.0312,
  b=0/c=6 fully one-sided. State this is the **only** McNemar-significant gap in
  the benchmark and it favours the hypothesis.

**§6.3 Cross-task pillar effects.** Insert **Table 5** (`final_report.md` §4
cross-task pillar table). Highlight that GE-NEXT gains are more pillar-uniform
than CEB-derived tasks — consistent with probing a decision pattern, not pillar
vocabulary.


### 4.7 Explainability & Counterfactual Input Probing (3–4 pages)

**§7.1 Motivation.** Open with the access constraint (R5 preemption). Insert the
SHAP/LIME/IG/attention-rollout enumeration verbatim from `pipeline.md` §7.1.
State the methodological move: behavioural probing executes LIME's perturbation
logic at the text level.

**§7.2 Protocol.** Variant A (Original) / Variant B (Keyword-Stripped) / Variant
C (Adversarially Framed). The five adversarial frames named one per pillar.
Binary scoring criterion. Insert **CIP Variant Example Box** (`pipeline.md`
§7.2.1 — the keyword-stripped substitutions, e.g. "one group" for "women",
"documented allocation policy" for "Women on Boards Directive threshold").

**§7.3 Aggregate robustness.** Insert **Table 7** (CIP aggregate, `pipeline.md`
§7.3 Table 7.2). The headline numerical finding: base = tuned-regulation =
13/15; tuned-legends = 14/15. State the chapter's analytical move (the §7.3
paragraph at lines 2426–2443 of pipeline.md) — that aggregate scores are an
*inadequate instrument* and analytical traction lies in pillar-level +
qualitative response patterns.

**§7.4 Per-pillar and qualitative analysis.** Insert **Table 6** (CIP
per-pillar, `pipeline.md` §7.3 Table 7.1). Four short subsections following
`pipeline.md` §7.4.2–§7.4.4:
- **§7.4.1 Base model — surface reasoning, scenario-dependent success.** Lift
  the `equal_economy` Variant C failure analysis (cost-efficiency frame is
  operationally legitimate, lacks identifiable rhetorical flaw — `pipeline.md`
  §7.4.2 close).
- **§7.4.2 Regulation-tuned model — same aggregate, different failure
  structure.** Insert verbatim the **`leadership_participation` Variant C
  response** ("the Directive's 40% threshold is not conditional on
  underperformance…"). Highlight the **MI collapse** (Variants B and C both
  fail). C7.
- **§7.4.3 Legend-tuned model — distinctive reasoning character.** Insert
  verbatim the **MI Variant B response** ("People facing overlapping
  disadvantages are the most underserved by single-dimension plans…"). Insert
  the paired `leadership_participation` Variant C contrast ("meritocracy
  argument conflates current performance with optimal future composition"). C8.
- **§7.4.4 The Mainstreaming-Intersectionality Variant C convergent failure.**
  All three models partially fail. Use this to argue that adversarial frames are
  not equally informative across pillars — methodological implication for future
  probing (`pipeline.md` §7.4.4 close; §7.4.5 finding 3).

**§7.5 Theoretical implications for the hypothesis.** Lift §7.4.6 — aggregate
scores do *not* produce clean confirmation; qualitative findings are stronger;
the empirical signature of the hypothesis lies in *reasoning character* more
than *aggregate robustness*.

### 4.8 Discussion (1.5–2 pages)

Three subsections:
- **§8.1 Where the hypothesis is supported.** GE-NEXT,
  GE-NLI (directional + underpowered), GE-WSC parity (tied at ceiling), CIP
  qualitative findings.
- **§8.2 Where the hypothesis is not supported.** GE-CLS (ontology
  classification favours regulation FT); GE-QA short-span (regulation FT
  format-tightening helps); CIP aggregate (no significant separation in 15
  items).
- **§8.3 Complementarity, not dominance.** Insert **Table 8** = the §3.3
  competence-routing table from `final_report.md`. Practical implication:
  deployment choice should be governed by which competence the application
  prioritises.

### 4.9 Limitations (1 page)

Lift `pipeline.md` §6.12 + §7.5 + `final_report.md` §5, condensed. Six bullets:
1. Test-set sizes (n ≤ 168 on most tasks; ~3× needed for GE-NLI; 350–500 needed
   for legends-vs-regulation on GE-NEXT).
2. Single backbone — backbone-generalisation is open.
3. Backbone is already very capable — discriminative ceiling is compressed
   (GE-WSC 0.93 base, tuned-legends 0.967 on GE-NEXT both near ceiling).
4. No formal Cohen's κ (single-annotator pipeline + stratified spot-check;
   relative rankings preserved).
5. Document-pillar coupling in CEB (minority pillars dominated by one source
   document — `pipeline.md` §6.12.4).
6. GE-WSC domain mismatch (WinoBias as-is, general-domain probe — `pipeline.md`
   §6.12.5).
7. GE-NEXT synthetic-text + LLM-evaluator latent affinity (mitigations applied,
   but residual risk — `pipeline.md` §6.12.6).
8. CIP sample = 15 — insufficient for inferential conclusions; binary scoring
   under-resolves response quality (`pipeline.md` §7.5).

### 4.10 Conclusion (≈400 words)

Reproduce `final_report.md` §6 conclusions, paraphrased into running prose:
1. `tuned-regulation` leads aggregate; `tuned-legends` is competitive; both
   clearly beat base.
2. The hypothesis is supported in its central formulation (GE-NEXT formal,
   GE-NLI directional, GE-WSC parity, GE-QA long-answer all corroborate; CIP
   reasoning-character finding qualifies it).
3. Legends and regulation teach complementary competences.
4. The orthogonal-distractor finding refines the original §6.8 hypothesis
   (failure mode protected against is *misdirected action*, not cost-deferral).
5. v2 roadmap — larger N, double-blind annotation with κ, harder GE-NEXT, harder
   coreference benchmark, multi-backbone replication.

### 4.11 Reproducibility appendix (½ page)

Lift the per-task deliverable paths from `pipeline.md` (e.g.
`benchmark/genderegglue/ge_nli.jsonl`, `aggregate.json`,
`task1_ge_cls_final_report.md`, etc.) as a single deliverables table. State the
random seeds: stratified split `seed=42`; bootstrap `seed=42`, 2000 resamples;
option-shuffle fixed seed in GE-NEXT.

---

## 5. Asset Allocation

### 5.1 Figures

| ID | Title | Type | Placement | Source |
|---|---|---|---|---|
| **Figure 1 (Teaser)** | "What each FT regime teaches" — side-by-side accuracy bars per task + a callout box for the lone McNemar-significant gap (GE-NEXT, p=0.031) | Bar chart + annotation | Top of page 1, referenced in Intro ¶4 | `aggregate.json` + `final_report.md` §6 |
| **Figure 2 (Pipeline)** | End-to-end pipeline: PDF → MD cleaned → 5 thematic parts → (legends branch / regulation branch) → spans → factoid + non-factoid Q&A → JSONL → FT → GenderEqGLUE eval → CIP probing | Process diagram with two parallel branches converging on FT, then diverging into 5 tasks | First page of Methodology (§4.1) | `pipeline.md` §1–§7 |
| **Figure 3 (CIP protocol)** | Variant A/B/C construction diagram for one pillar (suggest `leadership_participation`) with the meritocracy-camouflage adversarial frame and the keyword-stripping map | Schematic with three panels | Opening of §7.2 | `pipeline.md` §7.2.1 |
| **Figure 4** | Per-distractor-type error breakdown on GE-NEXT (stacked bars: performative / cost-optimising / orthogonal / N/A per model) | Stacked bar chart | §6.4 | `final_report.md` §3.1 |

### 5.2 Tables (ordered as they appear)

| ID | Title | Section | Source |
|---|---|---|---|
| **Table 0** | GenderEqGLUE task overview (Task / Description / GLUE analogue / Source / Metric) | §5.1 | `pipeline.md` §6.1 |
| **Table CEB-1** | CEB pool per-pillar distribution + 3-way split | §5.3 | `pipeline.md` §6.3.2, §6.3.3 |
| **Table 1** | Per-task headline scores + GenderEqGLUE Score | §6.1 + Abstract | `aggregate.json`; `final_report.md` §1 |
| **Table 2** | Wins per task (3–3 split between FT regimes) | §6.1 | `final_report.md` §1 |
| **Table 3** | Full pairwise McNemar matrix (9 rows incl. NS rows) | §6.2.5 + §5.5 | `final_report.md` §2; `aggregate.json` `significance_summary` |
| **Table 4** | Per-distractor-type error rate on GE-NEXT | §6.4 | `final_report.md` §3.1 |
| **Table 5** | Cross-task pillar effects (5 pillars × 4 task-gains) | §6.3 | `final_report.md` §4 |
| **Table 6** | CIP per-pillar scoring matrix (15 rows × 3 variants) | §7.4 | `pipeline.md` §7.3 Table 7.1 |
| **Table 7** | CIP aggregate robustness (3 rows × 3 variants + total) | §7.3 | `pipeline.md` §7.3 Table 7.2 |
| **Table 8** | Complementarity routing (reasoning competence → best model) | §8.3 | `final_report.md` §3.3 |

### 5.3 Code/JSON snippets (boxed in the paper)

| ID | Content | Section | Source |
|---|---|---|---|
| **Snippet 1** | Span Extractor system prompt | §4.5 | `pipeline.md` §4.2 lines 400–429 |
| **Q&A Example Box** | Factoid + Non-Factoid example JSON | §4.6 | `pipeline.md` §4.3 lines 656–672 |
| **JSONL Format Box** | Closed-book chat-format training line | §4.7 | `pipeline.md` §4.3 lines 686–701 |
| **Snippet 3** | CEB stratified 1/3 split | §5.3 | `pipeline.md` §6.3.3 lines 978–1009 |
| **GE-NLI Example** | One JSONL line from `ge_nli.jsonl` | §5.4.2 | `pipeline.md` §6.5 lines 1422–1432 |
| **Bool QA Construction Box** | Method A direct paraphrase vs Method B perturbed claim | §5.4.3 | `pipeline.md` §6.6.3 |
| **GE-NEXT Example Box** | Inés Lobato vignette + 4 options | §5.4.5 | `pipeline.md` §6.8 lines 1806–1828 |
| **CIP Variant Box** | Keyword-stripped substitution table for one pillar | §7.2 | `pipeline.md` §7.2.1 |
| **CIP Response Pair 1** | `leadership_participation` Variant C — regulation response vs legend response | §7.4.2/§7.4.3 | `pipeline.md` §7.4.3, §7.4.4 |
| **CIP Response Pair 2** | `mainstreaming_intersectionality` Variant B — regulation collapse vs legend recovery | §7.4.3 | `pipeline.md` §7.4.4 |


---

## 6. Handoff Checklist for the Paper-Writing Agent

- [ ] Story summary (TCICA) — §2.1 above
- [ ] Module Motivation Mapping table — §2.2 above
- [ ] Claim-to-evidence mapping (12 rows) — §3 above
- [ ] Rejection-risk table (R1–R7) — §1.1 above
- [ ] Minimal defensible claim + fallback narrative + honest weakness —
  §1.2–§1.4 above
- [ ] Section blueprint (Abstract → Conclusion) with per-section directives — §4
  above
- [ ] Asset allocation (figures, tables, code/JSON snippets, exact placement) —
  §5 above
- [ ] Source-gap log (G1–G6) — §6 above
- [ ] Timeline — §7 above

