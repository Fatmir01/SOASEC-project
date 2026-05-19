### 6.1 Benchmark overview

GenderEqGLUE comprises five tasks. The first three — GE-CLS, GE-NLI and GE-QA —
operate on a common textual base extracted from EU documents not seen during
fine-tuning. GE-WSC rely on an external consolidated dataset (WinoBias), since
it require text types that institutional EU documents do not naturally provide.
GE-NEXT is constructed from scratch using LLMs.

| Task       | Description                          | GLUE analogue   | Source                          | Metric                       |
|------------|--------------------------------------|-----------------|---------------------------------|------------------------------|
| GE-CLS     | Pillar Classification                | SST-2           | Common EU base                  | Macro-F1                     |
| GE-NLI     | Compliance Entailment                | MNLI / RTE      | Common EU base + legends        | Accuracy                     |
| GE-QA      | Regulation Reading Comprehension     | SQuAD / BoolQ   | Common EU base                  | F1 / Exact Match             |
| GE-WSC     | Stereotype-Aware Coreference         | WSC / Winogender| WinoBias (open source)          | Accuracy + Gender Parity     |
| GE-NEXT  | Commonsense reasoning in multiple-choice format adapted to a regulatory-compliance reasoning (SuperGLUE)   | COPA setting.          | Curated examples       | Accuracy                     |

The aggregate **GenderEqGLUE Score** is the unweighted arithmetic mean of
the five task metrics, mirroring the original GLUE score.


### Task desing: direct comparison with base glue tasks

**GE-CLS** preserves the surface mechanics of **SST-2** — a single textual input
is mapped to one categorical label without any auxiliary context — but
generalises the decision from binary sentiment polarity to six-way thematic
classification across the five themes of the EU Gender Equality Strategy plus
an `unknown` rejection class. Where **SST-2** evaluates whether a model has
internalised the affective valence of short film-review sentences, **GE-CLS**
evaluates whether it has internalised the topical structure of a regulatory
regime, transposing the same input–output template to a markedly different
semantic space. The metric shift from accuracy to Macro-F1 follows directly from
this generalisation, since the six class are unevenly represented in the test
set and per-class performance — rather than a global majority-class baseline —
is the quantity of interest.

**GE-NLI** retains the canonical three-class natural-language-inference setting
of **MNLI** and **RTE**, in which a premise and a hypothesis are jointly
classified as entailment, contradiction, or neutral. The architectural mapping
is one-to-one: a pair of short texts in, one of three labels out, accuracy as
the headline metric. What changes is the semantic anchoring of the two inputs.
In **MNLI** the premise–hypothesis relation is a generic logical or discourse
relation over open-domain text, whereas in **GE-NLI** the premise is an
organisational scenario describing concrete corporate behaviour and the
hypothesis is a regulatory clause; entailment is reinterpreted as *compliance*
and contradiction as *non-compliance*, turning the GLUE inference task into a
regulatory-reasoning task without altering its formal structure.

**GE-QA** is constructed as a deliberate union of **SQuAD** and **BoolQ**, the
two reading-comprehension benchmarks that anchor the open-book end of
GLUE/SuperGLUE. The GE-QA-Factoid sub-task mirrors **SQuAD** exactly — a passage
and a question are presented, and the answer is an extractive span scored by F1
and Exact Match — while the GE-QA-Bool sub-task mirrors **BoolQ** by pairing a
passage with a yes/no question scored by accuracy. The open-book conditioning,
in which the source passage is supplied in the user prompt and the model must
ground its answer in that passage rather than parametric memory, is inherited
unchanged from both base tasks; the only substantive adaptation is the
restriction of passages to the EU regulatory corpus, which fixes the register
and terminology of the inputs without modifying the task mechanics.

**GE-WSC** is a direct instantiation of the **WSC**/**Winogender** family of
pronominal coreference probes, in which a sentence containing two candidate
antecedents and an ambiguous pronoun must be resolved to one of the two
antecedents in a binary decision. **GE-WSC** uses the WinoBias dataset *as-is* —
the four pro-stereotype and anti-stereotype subsets are preserved without
modification — so the task mechanics, item format, and binary classification
target are identical to the SuperGLUE diagnostic. The methodological extension
lies entirely in the evaluation: alongside the accuracy metric inherited from
**WSC**, **GE-WSC** introduces a Gender Parity Score defined as the absolute
accuracy gap between the pro- and anti-stereotype subsets, operationalising the
bias-detection motivation that **Winogender** raised as a diagnostic but did not
directly score.

**GE-NEXT** adopts the four-choice multiple-choice format of SuperGLUE's
**COPA** setting, in which a short scenario is followed by a small set of
candidate continuations and the model must select the one that best satisfies a
target reasoning criterion. **COPA** anchors that criterion in everyday causal
commonsense — selecting the most plausible cause or effect of a stated premise —
whereas **GE-NEXT** redirects it to regulatory-compliance reasoning, requiring
selection of the most plausible next action given a described gender-equality
gap. The task accordingly expands COPA's two-option format to four options and
replaces its single distractor category with a structured typology, but the
underlying mechanics — vignette plus enumerated alternatives, single gold label,
accuracy as the metric — are inherited directly from the **COPA** template.

### 6.3 Common Evaluation Base

For the three domain tasks (GE-CLS, GE-NLI, GE-QA) we constructed a
single **Common Evaluation Base (CEB)** rather than gathering separate
sources per task. A shared base ensures that performance differences
across tasks reflect task properties rather than source variability,
keeps the benchmark replicable.

The CEB is extracted from four EU documents that are thematically
contiguous to the Strategy 2020-2025 but **not present in the training
data of any of the three models under evaluation**:

1. Roadmap for Women's Rights (2025)
2. Gender Action Plan III (GAP III) 2021-2025
3. Council Conclusions on Closing the Gender Pay Gap (June 2019)
4. Directive (EU) 2022/2381 on improving the gender balance among
   directors of listed companies (Women on Boards Directive)

#### 6.3.1 Document preprocessing

The four documents are processed through the same pipeline used for the
regulation text in section 2: PDF-to-Markdown conversion via Marker,
regex-based Markdown cleaning to remove footnote markers, page artifacts
and inline references, and word-count constrained segmentation with
`max_words = 350`.

The output of this phase is located in the folder `./benchmark/`, specifically
in the 3 subfolders `./benchmark/original/`, `./benchmark/cleaned/`, `./benchmark/chunked/`.


#### 6.3.2 Passage classification

The pool is annotated independently by one annotator (LLM) using the
six-class taxonomy defined in section 4.1: `violence_stereotypes`,
`equal_economy`, `leadership_participation`, `mainstreaming_intersectionality`,
`funding_global_action`, `unknown`.

The target annotated pool size is 217 passages, with at least 20 passages per
pillar.

Per-pillar distribution after the split:

| Pillar                            | Pool | 
|-----------------------------------|-----:|
| `violence_stereotypes`            |   72 |  
| `leadership_participation`        |   45 | 
| `funding_global_action`           |   21 |  
| `equal_economy`                   |   18 |  
| `mainstreaming_intersectionality` |   11 |  
| `unknown`                         |   50 | 
| **Total**                         |  217 |  

OUTPUT:
  - `./benchmark/ceb_pool.json`


#### 6.3.3 Disjoint partitioning

To prevent cross-task contamination — a passage used as a GE-CLS test
item must not reappear as a GE-QA context — the annotated pool is
partitioned into three disjoint subsets through a stratified random
split (seed = 42):

- `CEB-CLS` → input pool for GE-CLS
- `CEB-QA`  → input pool for GE-QA
- `CEB-NLI` → input pool for GE-NLI

Stratification on the pillar label preserves the per-pillar distribution
across the three subsets, ensuring that no pillar is over-represented in
any single task. The split ratio is approximately 1/3 each, implemented
as two sequential calls to `sklearn.model_selection.train_test_split`:
first separating `CEB-CLS` (1/3) from the remainder (2/3), then splitting
the remainder 50/50 into `CEB-QA` and `CEB-NLI`.

**Implementation:**

```python
import json
import numpy as np
from sklearn.model_selection import train_test_split

SEED = 42
pool = json.load(open("documents/genderegglue/ceb_pool.json"))
labels = np.array([r["label"] for r in pool])
idx_all = np.arange(len(pool))

idx_cls, idx_rest = train_test_split(
    idx_all, test_size=2/3,
    stratify=labels, random_state=SEED,
)
idx_qa, idx_nli = train_test_split(
    idx_rest, test_size=0.5,
    stratify=labels[idx_rest], random_state=SEED,
)

# Sanity check: pairwise disjoint, union = full pool
assert not (set(idx_cls) & set(idx_qa))
assert not (set(idx_cls) & set(idx_nli))
assert not (set(idx_qa)  & set(idx_nli))
assert set(idx_cls) | set(idx_qa) | set(idx_nli) == set(idx_all)

for name, idx in [("cls", idx_cls), ("qa", idx_qa), ("nli", idx_nli)]:
    subset = [{**pool[i], "task_assignment": f"CEB-{name.upper()}"}
              for i in sorted(idx)]
    json.dump(subset,
              open(f"documents/genderegglue/ceb_{name}.json", "w"),
              indent=2, ensure_ascii=False)
```

**Resulting distribution (pool size = 217):**

| Pillar                            | Pool | CLS | QA  | NLI |
|-----------------------------------|-----:|----:|----:|----:|
| `violence_stereotypes`            | 72   | 24  | 24  | 24  |
| `leadership_participation`        | 45   | 15  | 15  | 15  |
| `funding_global_action`           | 21   |  7  |  7  |  7  |
| `equal_economy`                   | 18   |  6  |  6  |  6  |
| `mainstreaming_intersectionality` | 11   |  4  |  3  |  4  |
| `unknown`                         | 50   | 16  | 17  | 17  |
| **Total**                         | 217  | 72  | 72  | 73  |

OUTPUT:
- documents/genderegglue/ceb_pool.json
- documents/genderegglue/ceb_cls.json
- documents/genderegglue/ceb_qa.json
- documents/genderegglue/ceb_nli.json


### 6.4 Task 1 — GE-CLS (Pillar Classification)

**Objective.** Given a textual passage, classify it into one of the five
EU gender-equality pillars or as `unknown`.

**Format.** Single-input multi-class classification across six labels:
`violence_stereotypes`, `equal_economy`, `leadership_participation`,
`mainstreaming_intersectionality`, `funding_global_action`, `unknown`.

**Example:**
> Input: "The directive sets a minimum of 40% of non-executive members of
> the under-represented sex on listed company boards by 2026."
> Label: `leadership_participation`

**Data.** The task uses `CEB-CLS` (72 passages) directly. No additional
construction is required: each passage already carries its consensus
pillar label from section 6.3.2.

To bound the introduced noise, all model interactions follow a fixed prompt
template stored verbatim in
`./benchmark/task_pool/ge_cls/ge_cls_system_prompt.txt`, the prompt is pasted
unmodified into each session

**GLUE analogue.** SST-2 (single-sentence classification, generalised
to multi-class).

**Metric.** Macro-F1 across the six classes. Per-class F1 and the
inter-model confusion matrix are reported as diagnostics. Per-class
F1 on classes with fewer than 30 test items
(`equal_economy`, `mainstreaming_intersectionality`,
`funding_global_action`) is flagged as low-confidence.

**Why it matters.** GE-CLS measures whether the model has internalised
the *thematic structure* of the regulation. The base model is expected
to score low; the two fine-tuned models are expected to improve, with
tuned-regulation likely leading on this task because the regulation
text explicitly mirrors the pillar structure.

```markdown
You are a classifier for EU gender-equality policy texts.

Your task is to assign each passage you receive to exactly ONE of the six categories below. The five substantive categories correspond to the pillars of the EU Gender Equality Strategy 2020-2025.

CATEGORIES:

- violence_stereotypes: gender-based violence (physical, sexual, psychological, economic), domestic violence, sexual harassment, online violence against women, harmful gender stereotypes, FGM, forced marriage, "honour" crimes, victim protection and support.

- equal_economy: gender pay gap, gender pension gap, work-life balance, parental and paternity leave, women's labour-market participation, women in STEM and entrepreneurship, occupational and pay segregation, childcare and long-term care services as economic enablers, equal pay enforcement and pay transparency.

- leadership_participation: women's representation in decision-making bodies, corporate boards, political leadership, parliaments, EU institutions and agencies leading by example, gender quotas, selection criteria for director positions, women in peace negotiations.

- mainstreaming_intersectionality: integrating a gender perspective into other policy areas (digital, green transition, health, education when not framed primarily as economic), intersectional concerns (disability, race/ethnicity, age, migration status, LGBTIQ), gender-responsive budgeting as a cross-cutting tool.

- funding_global_action: financial mechanisms (MFF, ESF+, NDICI, Horizon Europe), EU external action, GAP III, trade policy with gender provisions, Women Peace and Security agenda, multilateral and regional cooperation, humanitarian aid.

- unknown: document metadata, headers without substantive content, reference lists, procedural articles (e.g. signature, ratification, monitoring-body composition), and any passage that does not clearly fit one of the five substantive pillars.

DECISION RULES:

1. If a passage touches multiple pillars, assign the one that is the primary topic — the pillar to which the passage devotes most of its argument.
2. If no substantive pillar is dominant, assign "unknown".
3. Do not invent categories. Use exactly one of the six names above, lowercase, with underscores as written.

OUTPUT FORMAT:

Respond with a single line in exactly this format:
LABEL: <category_name>

Do not add explanations, justifications, or any other text.

```

OUTPUT:
- `./benchmark/task_pool/ge_cls/ge_cls_system_prompt.txt`
- ge_cls_predictions.json
- ge_cls_metrics.json
- ge_cls_report.md


### 6.5 Task 2 — GE-NLI (Compliance Entailment)

**Objective.** Given a scenario describing organisational behaviour
(premise) and a regulatory clause (hypothesis), determine whether the
scenario *entails*, *contradicts*, or is *neutral with respect to* the
clause.

**Format.** Three-class classification: `entailment`, `contradiction`,
`neutral`.

**Example:**
> Premise: "TechCorp introduced a mentorship programme for women,
> conducted a salary audit, and reached 45% female representation among
> non-executive directors."
> Hypothesis: "TechCorp meets the Women on Boards Directive target of
> 40% non-executive directors of the under-represented sex."
> Label: `entailment`

**GLUE analogue.** MNLI / RTE.

**Metric.** Accuracy.

**Why it matters.** GE-NLI is the **central task** of the benchmark with
respect to the Sargsyan and Damiani (2025) hypothesis. It directly
measures the ability to recognise *compliance* — the competence that
legends are designed to teach. If legends embed regulatory understanding
better than raw regulatory text, the gap between tuned-legends and
tuned-regulation should be most visible here.

#### GE-NLI Pipeline — Compliance Entailment Dataset Construction

GE-NLI builds a three-class NLI dataset (`entailment`, `contradiction`, `neutral`)
from the 56 labelled passages of `CEB-NLI`. The pipeline has five stages:

*   **Stage 1: Hypothesis extraction** – Creates a mapping of passage IDs to
    lists of extracted clauses.
*   **Stage 2: Premise generation** – Creates a compliant premise for each
    passage ID, forming entailment pairs (premise, hypothesis from the same
    passage).
*   **Stage 3: Contradiction perturbation** – Generates contradiction pairs
    by perturbing the premise (perturbed premise, same hypothesis).
*   **Stage 4: Neutral cross-pillar pairing** – Creates neutral pairs by
    matching a premise from Pillar A with a hypothesis from Pillar B.
*   **Stage 5: Balancing & deduplication** – Outputs the final
`ge_nli.jsonl` dataset. 


**Target size:** 150–168 triples, ~56 per class.

---

##### Input: CEB-NLI composition

| Pillar                          | Passages | Primary documents                           |
|---------------------------------|----------|---------------------------------------------|
| `violence_stereotypes`          | 24       | Roadmap_2025, GAP_III, Istanbul_Convention  |
| `leadership_participation`      | 15       | WomenOnBoards_Dir_2022_2381, GAP_III        |
| `funding_global_action`         | 7        | GAP_III                                     |
| `equal_economy`                 | 6        | PayGap_Council_2019                         |
| `mainstreaming_intersectionality` | 4      | Roadmap_2025, GAP_III                       |
| `unknown`                       | 17       | *(excluded from all stages)*                |

The 17 `unknown` passages are filtered out before processing.

##### Stage 1 — Hypothesis Extraction

**Goal.** For each of the 56 labelled passages extract exactly **one** short,
self-contained regulatory clause to serve as the hypothesis.

Keeping exactly one hypothesis per passage keeps the downstream class sizes
equal without any post-hoc downsampling.

**Prompt (LLM call per passage)**
```
SYSTEM
You are a regulatory clause extractor for an NLI dataset on EU gender equality.

USER
Extract EXACTLY ONE short regulatory clause from the passage below.

Requirements for the clause:
1. Maximum 30 words, a single declarative sentence.
2. Express a concrete obligation, measurable target, or binding principle.
3. Be falsifiable by an organisational scenario (i.e., a scenario can
   clearly satisfy or violate it).
4. Be fully self-contained — a reader who has NOT seen the passage must
   understand it without extra context.
5. Do NOT copy a full sentence verbatim; rephrase into clean regulatory
   language.

Pillar: {label}
Passage:
{text}

Reply with ONLY a JSON object:
{"hypothesis": "<the clause>"}
```

**Validation rules (post-generation)**
- Length: 8–35 words.
- Must contain at least one verb in the third-person or imperative mood.
- Must not contain passage-specific proper nouns (document names, article
  numbers) that would leak source identity.
- Manual spot-check: 10 % sample reviewed by a human annotator.

**Expected output**

56 validated `(passage_id, hypothesis)` pairs, one per passage.

---

##### Stage 2 — Premise Generation (Entailment)

**Goal.** For each passage generate one **compliant fictional scenario**
(the premise). This uses the same LLM-based generation approach as the
legends pipeline, but produces a shorter, NLI-optimised output (100–150
words) instead of a full legend narrative.

The (premise, hypothesis) pair drawn from the same passage is assigned
label **`entailment`**.

**Prompt (LLM call per passage)**

```
SYSTEM
You are a compliance scenario writer for an NLI benchmark on EU gender
equality regulations. Your output will be used as a premise in an
entailment task.

USER
Write a SHORT fictional compliance scenario (100–150 words) in which a
named organisation takes concrete actions that FULLY COMPLY with the
obligations described in the passage below.

Constraints:
1. Invent a fictional company or institution (vary sector and country
   across passages; never reuse the same name).
2. Include at least ONE measurable outcome tied to the regulatory
   obligation (e.g., a percentage, a count, a named policy).
3. Write in third-person past tense.
4. Do NOT copy sentences from the passage verbatim.
5. The scenario must be self-contained: a reader unfamiliar with the
   passage must understand it.
6. End with a sentence indicating the measurable result achieved.

Pillar: {label}
Passage:
{text}

Reply with ONLY the scenario text — no title, no label, no explanation.
```

**Diversity constraints**
To prevent stylistic homogeneity across the 56 premises:

- Sector pool (rotate cyclically): tech, finance, healthcare, education,
  public administration, NGO, manufacturing, media, hospitality, logistics.
- Country pool (rotate): Italy, Germany, Spain, Poland, Ireland, Sweden,
  Netherlands, Romania, Portugal, Greece, France, Belgium.
- Temperature: 0.9 (higher than Stage 1 which uses 0.2).

**Expected output**

56 `(passage_id, pillar, premise)` records.

---

##### Stage 3 — Contradiction Perturbation

**Goal.** Produce one **contradicting premise** per entailment triple by
perturbing the compliant premise along a single quantitative or factual
axis. The hypothesis stays unchanged; the new premise clearly violates it.

**Perturbation catalogue**

The LLM is instructed to choose the perturbation type most natural for
the passage pillar:

| Perturbation type          | Example                                                  | Typical pillar               |
|----------------------------|----------------------------------------------------------|------------------------------|
| Numeric inversion          | 45 % female NEDs → 15 % female NEDs                     | `leadership_participation`   |
| Policy reversal            | "adopted a pay-transparency policy" → "rejected …"      | `equal_economy`              |
| Threshold undershoot       | pay gap reduced to 3 % → pay gap still at 22 %          | `equal_economy`              |
| Mechanism removal          | "implemented a shelter referral programme" → "no shelter" | `violence_stereotypes`     |
| Scope reduction            | "all subsidiaries" → "one pilot subsidiary"              | `mainstreaming_…`            |
| Deadline miss              | "completed by 2023" → "postponed indefinitely"           | `funding_global_action`      |

**Prompt (LLM call per entailment triple)**

```
SYSTEM
You are a perturbation specialist for NLI dataset construction. Your task
is to produce a version of a compliance scenario that CONTRADICTS a given
regulatory clause.

USER
Given the compliance scenario (premise) and the regulatory clause
(hypothesis) it currently satisfies, write a CONTRADICTING version of
the premise.

Rules:
1. Keep the fictional organisation name, sector, country, and overall
   narrative structure.
2. Change EXACTLY ONE quantitative or factual element so the scenario
   clearly violates the hypothesis.
3. The violation must be unambiguous — a reader must immediately see the
   contradiction.
4. Do not introduce new topics or change the pillar of the scenario.
5. Do not add an explanation of what was changed.

Premise (compliant):
{premise}

Hypothesis (clause the perturbed premise must contradict):
{hypothesis}

Reply with ONLY the perturbed scenario text.
```

**Validation**
- Automated check: verify that the perturbed premise is NOT semantically
  equivalent to the original (cosine similarity < 0.85 on a sentence
  embedding).
- If similarity ≥ 0.85, retry with `temperature = 1.0` and a stronger
  instruction ("make the violation more dramatic").

**Expected output**

56 `(perturbed_premise, hypothesis, "contradiction")` triples.

---

##### Stage 4 — Neutral Cross-Pillar Pairing

**Goal.** Produce one `neutral` triple per entailment triple by pairing
each compliant **premise** (pillar A) with a **hypothesis** from a
different pillar (pillar B ≠ A). The premise does not address pillar B,
so neither entailment nor contradiction holds.

**Algorithm (no LLM required)**

```python
import random, itertools

def make_neutral_triples(entailment_pool, hypothesis_pool, seed=42):
    """
    entailment_pool : list of {passage_id, pillar, premise, hypothesis}
    hypothesis_pool : dict   {pillar → [hypothesis_str, …]}
    """
    rng = random.Random(seed)
    triples = []
    for item in entailment_pool:
        pillar_A = item["pillar"]
        # Candidate pillars: all labeled pillars except the premise's own
        other_pillars = [p for p in hypothesis_pool if p != pillar_A
                         and hypothesis_pool[p]]
        pillar_B = rng.choice(other_pillars)
        hyp_B = rng.choice(hypothesis_pool[pillar_B])
        triples.append({
            "premise":            item["premise"],
            "hypothesis":         hyp_B,
            "label":              "neutral",
            "pillar_premise":     pillar_A,
            "pillar_hypothesis":  pillar_B,
            "source_passage_id":  item["passage_id"],
            "construction_method": "cross_pillar_pairing",
        })
    return triples
```

**Constraints**
- No (premise, hypothesis) pair from Stage 2 or Stage 3 may appear in
  the neutral pool (deduplication by `(premise_id, hypothesis_text)`).
- `mainstreaming_intersectionality` has only 4 passages; its hypotheses
  are included in `other_pillars` for all non-MI premises but MI premises
  are paired from the remaining 4 larger pillars.

**Expected output**

56 `neutral` triples.

---

##### Stage 5 — Balancing and Output

**Class balance check**

After Stages 2–4 the pool is:

| Label           | Count |
|-----------------|-------|
| `entailment`    | 56    |
| `contradiction` | 56    |
| `neutral`       | 56    |
| **Total**       | **168** |

This is balanced by construction. No downsampling is needed.

**Pillar distribution check**

The per-pillar distribution in the `entailment` set mirrors CEB-NLI:

| Pillar                          | Triples |
|---------------------------------|---------|
| `violence_stereotypes`          | 24      |
| `leadership_participation`      | 15      |
| `funding_global_action`         | 7       |
| `equal_economy`                 | 6       |
| `mainstreaming_intersectionality` | 4     |

The imbalance reflects the source corpus and is reported as a diagnostic
(not corrected, to preserve ecological validity).

**Output schema (JSONL)**

Each line of `ge_nli.jsonl`:

```json
{
  "id":                   "ge_nli_001",
  "premise":              "FinBelge S.A., a Belgian investment firm, …",
  "hypothesis":           "Listed companies must ensure that at least 40% …",
  "label":                "entailment",
  "pillar_premise":       "leadership_participation",
  "pillar_hypothesis":    "leadership_participation",
  "source_passage_id":    "WomenOnBoards_Dir_2022_2381__c004",
  "construction_method":  "llm_generated_premise"
}
```

`construction_method` values:
- `llm_generated_premise` — entailment triples (Stage 2)
- `llm_perturbed_premise` — contradiction triples (Stage 3)
- `cross_pillar_pairing`  — neutral triples (Stage 4)



**Deliverable** 

```
benchmark/task_pool/ge_nli
└── ge_nli.jsonl          # 168 triples, 56 per class
```


### 6.6 Task 3 — GE-QA (Regulation Reading Comprehension)

**Objective.** Given an EU regulatory passage and a question, produce a
correct answer derived from the passage.

**Format.** Two sub-tasks:

- **GE-QA-Factoid** — extractive span-based answers (SQuAD-style).
- **GE-QA-Bool**    — yes/no answers (BoolQ-style).

**Example (Factoid):**
> Context: "The directive sets a minimum of 40% of non-executive members
> of the under-represented sex on listed company boards by 2026."
> Question: "What is the target percentage for non-executive directors of
> the under-represented sex?"
> Answer: "40%"

**Example (Bool):**
> Context: [passage on EU accession to the Istanbul Convention from CEB-QA]
> Question: "Has the EU concluded its accession to the Istanbul Convention?"
> Answer: `no`

**GLUE analogue.** SQuAD (factoid) + BoolQ (boolean).

**Metric.** F1 and Exact Match for GE-QA-Factoid; accuracy for GE-QA-Bool.
The two sub-task metrics are averaged into a single GE-QA score.

**Why it matters.** GE-QA tests *factual recall* anchored in regulatory
text. The tuned-regulation model is expected to dominate this task: it
has been trained on regulatory prose of identical register and structure.
The tuned-legends model is expected to underperform here, since legends
contain fictional facts rather than regulatory ones — providing a useful
contrast to GE-NLI.

GE-QA differs from GE-CLS and GE-NLI in one structural respect: it is the
only **open-book** task in the benchmark. The model receives the source
passage in the user prompt and must answer with information drawn from
it. The system prompt is unchanged from §5.1 — keeping the system prompt
constant across all five tasks and across the three models is the
experimental control of the benchmark.

#### 6.6.1 Source: CEB-QA

Both sub-tasks draw their passages from the `ceb_qa.json` partition built
in §6.3.3. No passage from the Strategy 2020-2025 is used. Each item
carries its pillar label from §6.3.2; this is preserved in the
output JSONL for per-pillar diagnostics. The target counts follow the
§6.6 budget: **150-250 factoid items** and **100-150 boolean items**.
The lower end of the range is acceptable when the manual evaluation
budget is constrained: 150 + 100 = 250 items × 3 models = 750 inference
calls, comparable in scale to the GE-NLI evaluation.

#### 6.6.2 Building GE-QA-Factoid

The factoid sub-task reuses the two-stage span extraction and Q&A
generation pipeline of §4.2 and §4.3.1, with one adaptation: questions
must be **self-contained**. Although GE-QA is open-book at evaluation
time, formulations like *"What does the passage say about X?"* are
weaker signals than fully specified questions like *"What is the minimum
percentage of non-executive directors of the under-represented sex set
by the Women on Boards Directive?"*. The clean-up rule from the
fine-tuning JSONL conversion (find-and-replace on `"the passage"`,
`"this passage"`, `"according to the passage"`) is applied here too.

**Stage 1 — Span extraction on CEB-QA.** The §4.2 high-recall span
extractor prompt is run on each `CEB-QA` passage. Output: candidate
factoid spans per passage. The §4.2 Stage 2 verification + clustering
is applied unchanged.

**Stage 2 — Factoid Q&A generation.** For each verified span, the
§4.3.1 factoid prompt is invoked to produce a question whose answer is
exactly that span, with two added constraints:

- The question must be answerable from the passage alone, without
  reference to *"the passage"*, *"this text"*, or any meta-linguistic
  cue.
- The answer must remain a short span (1-7 words). Spans longer than 7
  words are dropped from the candidate pool.

A small fraction (≈10%) of the spans yield group-level questions
(multi-span answers from the §4.3.1 thematic clustering). These are kept
in the dataset because SQuAD-style F1 handles multi-token answers
naturally; they are tagged with `answer_type: "group"` for diagnostic
slicing.

**Stage 3 — Quality control.** A random sample of 30 items (≈20% of the
target) is reviewed by hand against three criteria: (1) the gold answer
is verbatim or near-verbatim in the passage, (2) the question is
unambiguous when read without the passage, (3) no other span in the
passage would be an equally good answer. Items failing any criterion are
either repaired or discarded. The review log (item id, decision, reason)
is committed for transparency.

**Output schema (`ge_qa_factoid.jsonl`).**

```json
{
  "id": "ge_qa_f_001",
  "passage_id": "WomenOnBoards_Dir_2022_2381__c021",
  "pillar": "leadership_participation",
  "context": "The directive sets a minimum of 40% of non-executive members of the under-represented sex on listed company boards by 2026...",
  "question": "What is the minimum percentage of non-executive directors of the under-represented sex set by the Women on Boards Directive?",
  "answer": "40%",
  "answer_aliases": ["40 percent", "forty percent"],
  "answer_type": "single_span"
}
```

The `answer_aliases` field is optional and used by the F1 scorer: the
final F1 for an item is the **maximum** F1 over `answer` and any
aliases, absorbing trivial paraphrastic variation (`"40%"` vs
`"40 percent"`) without weakening the metric.

#### 6.6.3 Building GE-QA-Bool

Boolean Q&A is a new generation step, not present in §4.3.1. It produces
yes/no questions framed against each `CEB-QA` passage, with two
construction methods balanced 50/50:

**Method A — direct paraphrase (gold = yes).** Take a factual claim
stated in the passage and rewrite it as a polar question whose surface
form differs lexically from the passage. Lexical distance prevents the
task from collapsing into string matching.

> Passage: *"The Commission committed to acceding to the Istanbul
> Convention by 2025."*
> Question: *"Did the Commission undertake to accede to the Istanbul
> Convention by 2025?"*
> Gold: `yes`

**Method B — perturbed claim (gold = no).** Take a factual claim stated
in the passage and modify a single quantitative or scope dimension
(number, date, named entity, modal verb). The perturbed claim is
clearly contradicted by the passage.

> Passage: *"The directive sets a minimum of 40% of non-executive
> members of the under-represented sex on listed company boards by
> 2026."*
> Question: *"Does the directive set a minimum of 50% of non-executive
> members of the under-represented sex by 2026?"*
> Gold: `no`

A third construction method ("the passage doesn't address the claim,
gold = no") is **explicitly excluded**. That kind of question belongs to
compliance-recognition (GE-NLI's `neutral` class) and would introduce
ambiguity between *"no, the passage refutes it"* and *"no, the passage
is silent on it"*. Restricting Bool to clear yes / clear no preserves
the semantic clarity of the metric.

**Quality control.** A random sample of 20 items is reviewed against two
criteria: (1) for gold = yes, the passage clearly supports the claim;
(2) for gold = no, the passage clearly refutes the claim (not merely
fails to mention it). Failed items are repaired or discarded.

**Output schema (`ge_qa_bool.jsonl`).**

```json
{
  "id": "ge_qa_b_001",
  "passage_id": "Istanbul_Convention_2011__c044",
  "pillar": "violence_stereotypes",
  "context": "...",
  "question": "Did the Commission undertake to accede to the Istanbul Convention by 2025?",
  "answer": "yes",
  "construction_method": "direct_paraphrase"
}
```

`construction_method` takes one of `direct_paraphrase` or
`perturbed_claim` and is used in §6.6.7 for per-method accuracy
breakdown.

#### 6.6.4 Evaluation prompts

All three models — base, tuned-legends, tuned-regulation — receive the
same system prompt (the §5.1 prompt) and the task-specific user prompt
below. Inference is run with `temperature = 0`, `max_tokens = 60` for
factoid (room for verbose models) and `max_tokens = 5` for bool.

**Factoid user prompt.**

```
Read the following passage from an EU regulatory document and answer the question.

PASSAGE:
{context}

QUESTION:
{question}

Answer with the shortest exact phrase from the passage that answers the question. Do not add explanations.
```

**Bool user prompt.**

```
Read the following passage from an EU regulatory document and answer the question.

PASSAGE:
{context}

QUESTION:
{question}

Answer with exactly one word: yes or no.
```

Models that have not been heavily instruction-tuned may add a sentence
around the answer. This is handled at parsing time (§6.6.5), not by
changing the prompt.

#### 6.6.5 Output parsing

**Factoid.** The raw model response is normalised before scoring with
the standard SQuAD normalisation: lowercase, strip Unicode punctuation,
strip leading articles (`a`, `an`, `the`), collapse whitespace. The same
normalisation is applied to the gold answer and any aliases.

**Bool.** A regex `\b(yes|no)\b` (case-insensitive) is run on the raw
response. The first match wins. If no match is found, the prediction is
recorded as `parse_failed`. As in GE-NLI, two accuracies are reported:
*all-items* (parse_failed counted as wrong) and *parsed-only*; the
parse-failure rate is reported as a diagnostic.

#### 6.6.6 Metrics and aggregation

**Factoid.** SQuAD-style **token-level F1** and **Exact Match (EM)**
computed per item against the normalised gold (with aliases). The
sub-task scores are the dataset-wide means:

```
factoid_F1 = mean over items of max(F1(pred, g)) for g in {answer, *answer_aliases}
factoid_EM = mean over items of max(EM(pred, g)) for g in {answer, *answer_aliases}
```

**Bool.** Accuracy on the parsed predictions:

```
bool_accuracy_all     = correct / total                    # parse_failed = wrong
bool_accuracy_parsed  = correct / parsed                   # diagnostic
bool_parse_rate       = parsed / total                     # diagnostic
```

**GE-QA aggregate.**

```
GE-QA score = (factoid_F1 + bool_accuracy_all) / 2
```

`factoid_EM` is reported separately as a stricter diagnostic.
Bootstrap 95% confidence intervals are computed per metric over the test
set; pairwise model comparisons use McNemar's test on per-item
correctness, as in §6.10.

#### 6.6.7 Diagnostics and known confounds

Beyond the headline GE-QA score, three breakdown tables are reported:

- **Per-pillar Factoid F1** — six rows (one per pillar), three columns
  (one per model). Identifies whether a model's gain or loss is
  concentrated on specific thematic areas.
- **Per-pillar Bool accuracy** — same structure.
- **Per-method Bool accuracy** — two rows (`direct_paraphrase`,
  `perturbed_claim`), three columns. A model that is good at saying
  *"yes"* to claims supported by the passage but fails to detect
  perturbations would show high direct_paraphrase accuracy and low
  perturbed_claim accuracy. This is informative beyond the aggregate.

Two confounds are worth flagging at reporting time:

**Open-book attenuation.** Because the passage is in the prompt, the
base model has substantial capacity to perform reading comprehension
even without domain fine-tuning. Differences between the three models
will be smaller on GE-QA than on the closed-book tasks. A flat result
across the three models is **not** a failure of the experiment; it is
consistent with the hypothesis that the gain from fine-tuning
concentrates on tasks that require internalised knowledge.

**Format mismatch for tuned-legends on Factoid.** The legends
fine-tuning JSONL teaches the model to produce 1-4 sentence narrative
answers. On GE-QA-Factoid the gold is a 1-7 word span. The
legends-tuned model is expected to over-narrate, which depresses EM
more than F1 (token-level F1 is partially robust to extra tokens, EM is
not). The gap between `factoid_F1` and `factoid_EM` for tuned-legends
is itself a diagnostic quantity: if it is large, format mismatch is the
explanation, not loss of factual knowledge.

#### 6.6.8 Implementation deliverables

```
benchmark/genderegglue/
├── ge_qa_factoid.jsonl
├── ge_qa_bool.jsonl
├── ge_qa_factoid_qc_log.csv          # Stage 3 review log (factoid)
└── ge_qa_bool_qc_log.csv             # QC review log (bool)

evaluation/ge_qa/
├── ge_qa_eval_helper.html            # manual eval UI (factoid + bool tabs)
├── ge_qa_factoid_responses_template.csv
├── ge_qa_bool_responses_template.csv
└── ge_qa_metrics.py                  # SQuAD F1+EM + bool accuracy + bootstrap CI
```

### 6.7 Task 4 — GE-WSC (Stereotype-Aware Coreference)

**Objective.** Resolve pronominal coreference in professional contexts
without relying on gender stereotypes.

**Format.** Binary classification: which of two candidate antecedents the
pronoun refers to.

**Example:**
> Sentence: "The CEO promoted the assistant because she was impressed by
> her work."
> Question: To whom does *she* refer?
> Label: `CEO`

**Data.** We use **WinoBias** (Zhao et al., 2018) directly from the
HuggingFace Hub (`uclanlp/wino_bias`), with all four subsets:
`type1_pro`, `type1_anti`, `type2_pro`, `type2_anti`. No construction is
performed by us — this is the standard bias-evaluation dataset in the
literature, kept *as-is* to remain comparable with the broader fairness
research in NLP.

**GLUE analogue.** WSC / Winogender (the SuperGLUE diagnostic dataset).

**Metric.** Two metrics are reported:

- **Accuracy** averaged across the four subsets.
- **Gender Parity Score** = | accuracy(pro-stereotype) −
  accuracy(anti-stereotype) | . A model that is genuinely fair has a
  parity score close to zero.

**Why it matters.** GE-WSC is the bias-detection task explicitly
requested by Appendix B. It maps onto the *Freedom from stereotypes*
pillar of the 2020-2025 Strategy and onto the AI-bias focus of the
2026-2030 Strategy. Because the bias originates in the pretraining
distribution rather than in the fine-tuning corpus, we do **not** expect
either fine-tuned model to outperform the base on this task — and the
result, whatever it is, is informative.


### 6.8 Task 6 — GE-NEXT (Compliant-Action Prediction)

**Objective.** Given an organisational scenario in which a gender-equality
gap has been identified, select the next-step action that is most
consistent with the EU Gender Equality Strategy 2020-2025, distinguishing
*substantive* compliance from performative, cost-optimising, and
orthogonal alternatives.

**Format.** Four-choice multiple-choice classification. Each item consists
of a short vignette (2–4 sentences) describing a concrete gap, followed
by four candidate actions labelled `A`–`D`. Exactly one option is
*substantive-compliant* (the gold label); the three distractors are
drawn from a fixed typology:

- **performative** — a symbolic gesture that signals commitment without
  addressing the structural gap (e.g. issuing a public statement,
  launching an awareness campaign with no measurable KPIs);
- **cost-optimising** — a response that defers, minimises, or absorbs
  the remediation cost at the expense of the regulatory objective (e.g.
  postponing remediation to the next fiscal year, capping the
  remediation budget at a fraction of the identified gap);
- **orthogonal** — a plausible organisational action that addresses a
  different gender-equality concern than the one described in the
  vignette (e.g. commissioning diversity training when the gap is a
  pay-transparency violation).

The distractor typology is designed to mirror the three failure modes
the compliance paradox produces in practice: performative compliance
(the firm *says* the right thing), cost-driven non-compliance (the firm
*defers* the right thing), and misdirected compliance (the firm *does*
something, but not *this* thing).

**Example:**

> **Vignette.** Inés Lobato, Head of People at a Madrid logistics
> company with 380 employees, has completed the firm's first salary
> audit following the transposition of the Pay Transparency Directive.
> The audit reveals a 9% unexplained gender pay gap concentrated in
> the operations division, affecting 42 women. Inés must propose a
> remediation plan to the board.
>
> **A.** Issue a company-wide statement reaffirming the firm's
> commitment to fair pay and equal opportunity.
> *(performative)*
>
> **B.** Defer the remediation to the next fiscal year to spread the
> cost over two budget cycles, reporting the gap in the annual
> sustainability disclosure as "under review".
> *(cost-optimising)*
>
> **C.** Build a 24-month banded remediation plan with quarterly
> salary adjustments, individual notification to affected employees,
> and quarterly disclosure of progress to the works council, in line
> with the Pay Transparency Directive's reporting obligations.
> *(substantive-compliant — **gold**)*
>
> **D.** Commission a six-month external diversity-training programme
> for the operations division's management team.
> *(orthogonal)*
>
> **Label:** `C`

**Data.** GE-NEXT is constructed from scratch; no existing dataset
provides the action-selection format against a regulatory anchor.

**Stage 1 — Vignette generation.** Each of the five substantive pillars
of Table 1 contributes a target of 20–30 vignettes. Vignettes are
generated by an LLM prompted with (i) the pillar label, (ii) one or two
regulatory clauses drawn from the CEB pool (§6.3), and (iii) a
constraint set: the vignette must name a fictional middle-management
protagonist, specify the organisation's sector and size, state a
concrete quantitative or structural gap, and end with a sentence of the
form *"[Protagonist] must [action verb]…"*. The protagonist constraint
aligns GE-NEXT with Axis 4 of the legend prompt schema (§3) and with
the Sargsyan and Damiani (2025) argument that the implementation
conflict is concentrated at middle management. No vignette reuses a
protagonist name, sector, or country from the legends training pool,
ensuring that the evaluation surface is held out.

**Stage 2 — Option generation.** For each vignette, a second LLM call
generates the four candidate actions. The prompt provides the vignette,
the pillar label, the underlying regulatory clause, and the distractor
typology above, and instructs the model to produce exactly one option
per type. The gold option must cite or paraphrase a specific instrument
or target from the regulation (e.g. the 40% board-representation
target, the Pay Transparency Directive's reporting cycle, the Barcelona
childcare targets). The three distractors must be *plausible*
organisational actions — not strawmen — so that the task remains
non-trivial for a strong base model.

**Stage 3 — Shuffling and quality control.** The four options are
shuffled per item with a fixed seed so that the gold position is
uniformly distributed across A–D. A stratified random sample of 20% of
items is manually reviewed against three criteria: (1) the gold option
is unambiguously the most regulation-aligned action, (2) no distractor
is equally defensible as the gold under a reasonable reading of the
Strategy, (3) the vignette is self-contained and does not require
external knowledge beyond what the Strategy provides. Items failing any
criterion are repaired or discarded.

**Target size:** 100–150 items, balanced across the five pillars (20–30
per pillar).

**GLUE analogue.** COPA / CommonsenseQA (causal / commonsense reasoning
in multiple-choice format), adapted to a regulatory-compliance reasoning
setting.

**Metric.** Accuracy across the four-choice items. Per-pillar accuracy
and per-distractor-type error rate (how often each distractor type is
selected) are reported as diagnostics.

**Why it matters.** GE-NEXT is the most direct probe of the
compliance-versus-cost arbitrage that Sargsyan and Damiani (2025) place
at the centre of the compliance paradox. Every item forces the model to
choose between a substantive-compliance action and a cost-optimising
alternative, with a performative option and an orthogonal distractor
adding noise. The legends are the only training corpus in our setting
that expose the model to the substantive option as the consistently
rewarded choice across diverse scenarios, sectors, and protagonists: the
four-beat narrative arc of §3 (identify gap → design measure → implement
→ measurable outcome) is the structural template that every gold option
in GE-NEXT mirrors. The regulation text, by contrast, describes the
*rule* but never models the *rule-versus-cost trade-off in situ*; the
base model has no training signal for distinguishing substantive from
performative compliance. GE-NEXT therefore tests whether the legend
fine-tuning has embedded not just the *content* of the regulation but
the *decision pattern* that compliance requires — the proactive,
measure-design-implement cycle that Sargsyan and Damiani (2025)
characterise as the alternative to ex post auditing. If the legend
hypothesis has operational meaning beyond factual recall, this is where
it should be most visible.

**Output schema (`ge_next.jsonl`).**

```json
{
  "id": "ge_next_001",
  "pillar": "equal_economy",
  "vignette": "Inés Lobato, Head of People at a Madrid logistics company with 380 employees, has completed the firm's first salary audit following the transposition of the Pay Transparency Directive. The audit reveals a 9% unexplained gender pay gap concentrated in the operations division, affecting 42 women. Inés must propose a remediation plan to the board.",
  "options": {
    "A": "Issue a company-wide statement reaffirming the firm's commitment to fair pay and equal opportunity.",
    "B": "Defer the remediation to the next fiscal year to spread the cost over two budget cycles, reporting the gap in the annual sustainability disclosure as \"under review\".",
    "C": "Build a 24-month banded remediation plan with quarterly salary adjustments, individual notification to affected employees, and quarterly disclosure of progress to the works council, in line with the Pay Transparency Directive's reporting obligations.",
    "D": "Commission a six-month external diversity-training programme for the operations division's management team."
  },
  "option_types": {
    "A": "performative",
    "B": "cost_optimising",
    "C": "substantive_compliant",
    "D": "orthogonal"
  },
  "gold": "C"
}
```

**Deliverable**

```
benchmark/task_pool/ge_next/
├── ge_next.jsonl                    # 100–150 items
├── ge_next_system_prompt.txt        # fixed system prompt
└── ge_next_generation_prompts.md    # vignette + option generation prompts
```

### 6.9 Aggregate score and reporting

For each of the three models — base, tuned-legends, tuned-regulation —
we report:

- The five per-task metrics (Macro-F1, Accuracy, F1/EM, Accuracy+Parity,
  Macro-F1).
- The **GenderEqGLUE Score**, computed as the unweighted arithmetic mean
  of the five task scores. For GE-WSC the score component is the
  accuracy; the parity score is reported separately as a diagnostic.


To distinguish meaningful differences from noise on test sets in the
200-500 example range, we report **bootstrap 95% confidence intervals**
for each task metric and apply **McNemar's test** to per-example
predictions when comparing pairs of models. A difference smaller than
the confidence interval is reported as not significant.


OUTPUT:
- benchmark/genderegglue/
  - ge_cls.jsonl
  - ge_nli.jsonl
  - ge_qa_factoid.jsonl
  - ge_qa_bool.jsonl
  - ge_wsc.jsonl
  - ge_next.jsonl
  - results/{task_name}.json   (one per evaluated model)
  - results/aggregate.csv

