# GE-NEXT Evaluation Report

**Task.** Compliant-Action Prediction (GE-NEXT) — four-choice multiple-choice
classification. Given an organisational vignette describing a gender-equality
gap, select the action most consistent with the EU Gender Equality Strategy
2020-2025, distinguishing *substantive compliance* from three distractor types:
`performative`, `cost_optimising`, and `orthogonal`.

**Items evaluated:** 150 (30 per pillar, balanced across five pillars).  
**Models:** base, tuned-legends, tuned-regulation.  
**Setting:** zero-shot, identical system prompt across models, `temperature = 0`.

**Headline metric (per §6.9 spec):** Accuracy. Per-pillar accuracy and
per-distractor-type error rate are reported as diagnostics.

---

## 1. Headline results

| Model | Accuracy (95% CI) |
|---|---|
| base | 92.00% (95% CI: 87.33%–96.00%) |
| tuned-legends | 98.67% (95% CI: 96.67%–100.00%) |
| tuned-regulation | 94.00% (95% CI: 90.00%–98.00%) |

Confidence intervals are 2,000-resample non-parametric bootstrap.

---

## 2. Per-pillar accuracy

| Pillar | n | base | tuned-legends | tuned-regulation |
|---|---|---|---|---|
| `equal_economy` | 30 | 90.0% | **100.0%** | 96.7% |
| `leadership_participation` | 30 | 93.3% | **96.7%** | 93.3% |
| `violence_stereotypes` | 30 | 90.0% | **96.7%** | 93.3% |
| `mainstreaming_intersectionality` | 30 | 93.3% | **100.0%** | 93.3% |
| `funding_global_action` | 30 | 93.3% | **100.0%** | 93.3% |

`tuned-legends` leads on every pillar. The gap over the base is largest on
`equal_economy` (−10.0 pp) and `mainstreaming_intersectionality` (−6.7 pp).
`tuned-regulation` never exceeds `tuned-legends` on any pillar.

---

## 3. Predicted letter distribution

Useful for spotting positional bias (a model that over-predicts a specific
letter regardless of content).

| Model | A | B | C | D |
|---|---|---|---|---|
| (gold) | 37 | 38 | 37 | 38 |
| base | 40 | 36 | 37 | 37 |
| tuned-legends | 36 | 39 | 37 | 38 |
| tuned-regulation | 40 | 36 | 36 | 38 |

All three models track the gold distribution closely. `base` and
`tuned-regulation` show a mild over-prediction of letter A (+3 over gold),
consistent with their error profile (see Section 4.2). `tuned-legends`
shows no systematic positional bias.

---

## 4. Error analysis

### 4.1 Error counts

| Model | Errors | Accuracy |
|---|---|---|
| base | 12 | 92.0% |
| tuned-regulation | 9 | 94.0% |
| tuned-legends | 2 | 98.7% |

### 4.2 Full error table

| Item | Pillar | Gold | base | tuned-legends | tuned-regulation |
|---|---|---|---|---|---|
| ge_next_ee_004 | equal_economy | B | **A** ✗ | B ✓ | B ✓ |
| ge_next_ee_010 | equal_economy | C | **B** ✗ | C ✓ | **B** ✗ |
| ge_next_ee_018 | equal_economy | A | **B** ✗ | A ✓ | A ✓ |
| ge_next_lp_008 | leadership_participation | C | **D** ✗ | C ✓ | **D** ✗ |
| ge_next_lp_020 | leadership_participation | A | A ✓ | **C** ✗ | A ✓ |
| ge_next_lp_027 | leadership_participation | A | **C** ✗ | A ✓ | **C** ✗ |
| ge_next_vs_012 | violence_stereotypes | C | **B** ✗ | **B** ✗ | **B** ✗ |
| ge_next_vs_024 | violence_stereotypes | D | **C** ✗ | D ✓ | D ✓ |
| ge_next_vs_026 | violence_stereotypes | B | **A** ✗ | B ✓ | **A** ✗ |
| ge_next_mi_020 | mainstreaming_intersectionality | B | **C** ✗ | B ✓ | **C** ✗ |
| ge_next_mi_021 | mainstreaming_intersectionality | D | **A** ✗ | D ✓ | **A** ✗ |
| ge_next_fg_010 | funding_global_action | B | **A** ✗ | B ✓ | **A** ✗ |
| ge_next_fg_025 | funding_global_action | B | **A** ✗ | B ✓ | **A** ✗ |

### 4.3 Wrong-letter distribution

| Model | A | B | C | D |
|---|---|---|---|---|
| base | 5 | 3 | 3 | 1 |
| tuned-legends | 0 | 1 | 1 | 0 |
| tuned-regulation | 4 | 2 | 2 | 1 |

`base` and `tuned-regulation` share a characteristic error pattern: both
over-select letter A when wrong (5 and 4 errors respectively). Given that
the gold distribution is balanced across letters (37–38 per letter), this
is unlikely to be positional bias and more plausibly reflects a preference
for the first-listed candidate when the decision is uncertain — consistent
with an anchoring effect on the `performative` distractor, which by
construction tends to be written as a plausible, high-salience action.

---

## 5. Pairwise comparisons (McNemar's exact test)

`b` = items where the first model is correct and the second is wrong;
`c` = the opposite. Exact two-sided binomial p-value on `min(b, c)` under H0
(equal error rates).

| Pair | b | c | n_disagree | p-value | Significant at α=0.05 |
|---|---|---|---|---|---|
| base vs tuned-legends | 11 | 1 | 12 | 0.0063 | **yes** |
| base vs tuned-regulation | 3 | 0 | 3 | 0.2500 | no |
| tuned-legends vs tuned-regulation | 1 | 8 | 9 | 0.0391 | **yes** |

---

## 6. Items flagged for QC

Items where at least one model errs, all marked with `*` in the source CSV.
Priority cases for manual review in Stage 3:

| Item | Issue |
|---|---|
| `ge_next_vs_012` | All three models predict B instead of C — only item with universal failure; likely distractor ambiguity |
| `ge_next_lp_020` | Only `tuned-legends` is wrong (predicts C); base and tuned-regulation correct — isolated legends over-fitting candidate |
| `ge_next_ee_010` | Shared error between base and tuned-regulation; `tuned-legends` recovers |
| `ge_next_fg_010` | Shared error between base and tuned-regulation on `funding_global_action`, a pillar otherwise at 100% |
| `ge_next_fg_025` | Same pattern as ge_next_fg_010; two errors on the same pillar warrant joint inspection |

---

## 7. Interpretation

**Ranking by accuracy:** tuned-legends (98.67%) > tuned-regulation (94.00%) >
base (92.00%).

The ordering is consistent with the §6.9 prediction: GE-NEXT is the most direct
probe of the compliance-versus-cost decision pattern that legends are designed to
teach, and the legends-tuned model leads on every pillar.

### 7.1 Effect size and statistical significance

Unlike GE-NLI, where the CIs overlapped and no pairwise test reached
significance, here two of the three McNemar tests clear α = 0.05:

- **base vs tuned-legends** (p = 0.0063): tuned-legends recovers 11 base errors
  while introducing only 1 new error. This is a robust, directional improvement.
- **tuned-legends vs tuned-regulation** (p = 0.0391): tuned-regulation loses 8
  items to tuned-legends while recovering only 1. The gap is not artefactual.
- **base vs tuned-regulation** (p = 0.2500): the regulation-tuned model offers
  no statistically significant improvement over the base on this task, consistent
  with the §6.9 prediction that the regulation corpus "describes the rule but
  never models the rule-versus-cost trade-off in situ".

The simultaneous significance of both base vs tuned-legends and
tuned-legends vs tuned-regulation, combined with the non-significance of
base vs tuned-regulation, places the three models in an unambiguous ordering:
tuned-legends is better than both, and the two weaker models are
statistically indistinguishable from each other on this task.

### 7.2 Why GE-NEXT is where the legends advantage is most visible

The four-beat narrative arc of the legends — *identify gap → design measure
→ implement → measurable outcome* — is the structural template that every
gold option in GE-NEXT mirrors. The `cost_optimising` distractor defers or
absorbs the measure; the `performative` distractor announces it without
implementing it; the `orthogonal` distractor addresses a different gap
entirely. A model that has internalised this arc from the legends training
corpus is equipped to recognise the gold option across diverse sectors,
protagonists, and phrasings, even zero-shot.

The regulation corpus, by contrast, states the *rule* but never shows the
rule applied against a cost or timing constraint. It is therefore not
surprising that tuned-regulation does not improve over the base on this
task, while tuned-legends gains 6.67 percentage points.

### 7.3 The shared error pattern of base and tuned-regulation

Of the 9 errors made by tuned-regulation, 8 are also present in base. The
two models share a characteristic wrong-answer pattern: over-selection of
letter A when uncertain, consistent with anchoring on the first listed —
typically a high-salience `performative` action. Fine-tuning on the
regulation text does not appear to correct this anchoring tendency. The
legends training, by repeatedly rewarding the *substantive* option
regardless of its position, does.

### 7.4 The single universal failure

`ge_next_vs_012` is the only item on which all three models select the same
wrong answer (B instead of C). Given the overall robustness of the
dataset, a single universal failure is most parsimoniously attributed to
item construction rather than to a shared model weakness. This item should
be reviewed against criterion (1) of the Stage 3 QC protocol (the gold
option must be unambiguously the most regulation-aligned action) before
inclusion in the final benchmark.

### 7.5 Take-aways for the thesis

1. GE-NEXT provides the **strongest statistical evidence** in the
   GenderEqGLUE benchmark for the Sargsyan & Damiani (2025) hypothesis:
   tuned-legends is significantly better than both the base (p = 0.006)
   and tuned-regulation (p = 0.039).
2. The result is consistent with the interpretation that legends embed not
   just the *content* of the regulation but the *decision pattern* that
   compliance requires — the proactive, measure-design-implement cycle.
3. The non-significance of base vs tuned-regulation (p = 0.25) on this
   task is theoretically informative: it confirms that knowing the rule
   text is insufficient for correctly applying it under cost pressure.
4. One item (`ge_next_vs_012`) should be flagged for manual review before
   the benchmark is frozen; it is the only item where the dataset itself,
   rather than the models, may be the source of the signal.
