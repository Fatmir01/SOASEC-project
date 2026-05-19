# GE-NLI Evaluation Report

**Task.** Compliance Entailment (GE-NLI) — three-class classification 
(`entailment` / `contradiction` / `neutral`) given a premise (organisational 
scenario) and a hypothesis (regulatory clause).

**Items evaluated:** 168 (gold balanced: 56 / 56 / 56). 
**Models:** base, tuned-legends, tuned-regulation. 
**Setting:** zero-shot, identical system prompt across models, `temperature = 0`.

**Headline metric (per §6.5 spec):** Accuracy. Macro-F1 reported alongside 
for class-balance robustness (the test set is perfectly balanced, so the two 
metrics coincide closely; in this report Macro-F1 should be read as 
confirmatory).

---

## 1. Headline results

| Model | Accuracy (95% CI) | Macro-F1 (95% CI) |
|---|---|---|
| base | 89.88% (95% CI: 85.12%–94.05%) | 90.03% (95% CI: 85.30%–94.22%) |
| tuned-legends | 92.86% (95% CI: 88.69%–96.43%) | 92.94% (95% CI: 88.54%–96.51%) |
| tuned-regulation | 91.07% (95% CI: 86.31%–95.24%) | 91.06% (95% CI: 86.49%–95.22%) |

Confidence intervals are 2,000-resample non-parametric bootstrap.

## 2. Per-class precision, recall, F1

### base

| Class | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| entailment | 95.83% | 82.14% | 88.46% | 56 |
| contradiction | 100.00% | 89.29% | 94.34% | 56 |
| neutral | 78.57% | 98.21% | 87.30% | 56 |

### tuned-legends

| Class | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| entailment | 96.15% | 89.29% | 92.59% | 56 |
| contradiction | 100.00% | 91.07% | 95.33% | 56 |
| neutral | 84.62% | 98.21% | 90.91% | 56 |

### tuned-regulation

| Class | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| entailment | 95.65% | 78.57% | 86.27% | 56 |
| contradiction | 100.00% | 96.43% | 98.18% | 56 |
| neutral | 80.88% | 98.21% | 88.71% | 56 |

## 3. Confusion matrices

Rows = gold, columns = predicted.

### base

| gold \ pred | entailment | contradiction | neutral |
|---|---|---|---|
| entailment | 46 | 0 | 10 |
| contradiction | 1 | 50 | 5 |
| neutral | 1 | 0 | 55 |

### tuned-legends

| gold \ pred | entailment | contradiction | neutral |
|---|---|---|---|
| entailment | 50 | 0 | 6 |
| contradiction | 1 | 51 | 4 |
| neutral | 1 | 0 | 55 |

### tuned-regulation

| gold \ pred | entailment | contradiction | neutral |
|---|---|---|---|
| entailment | 44 | 0 | 12 |
| contradiction | 1 | 54 | 1 |
| neutral | 1 | 0 | 55 |

## 4. Pairwise comparisons (McNemar's exact test)

`b` = items where the first model is correct and the second is wrong; 
`c` = the opposite. Exact two-sided binomial p-value on `min(b, c)` under H0 (equal error rates).

| Pair | b | c | n_disagree | p-value | Significant at α=0.05 |
|---|---|---|---|---|---|
| base vs tuned-legends | 2 | 7 | 9 | 0.1797 | no |
| base vs tuned-regulation | 5 | 7 | 12 | 0.7744 | no |
| tuned-legends vs tuned-regulation | 7 | 4 | 11 | 0.5488 | no |

## 5. Breakdown by premise pillar

Accuracy per pillar of the premise (a low-support pillar will have a wide effective CI; the n column is shown to flag this).

| Pillar | n | base | tuned-legends | tuned-regulation |
|---|---|---|---|---|
| violence_stereotypes | 72 | 87.50% | 90.28% | 84.72% |
| leadership_participation | 45 | 93.33% | 93.33% | 95.56% |
| funding_global_action | 21 | 90.48% | 95.24% | 95.24% |
| equal_economy | 18 | 83.33% | 94.44% | 94.44% |
| mainstreaming_intersectionality | 12 | 100.00% | 100.00% | 100.00% |

## 6. Breakdown by construction method

Accuracy per method used to produce the (premise, hypothesis, label) triple. 
Each method maps to a different gold class:
- `llm_generated_premise` → gold = entailment (compliant scenario + matching clause)
- `llm_perturbed_premise` → gold = contradiction (perturbed scenario + matching clause)
- `cross_pillar_pairing` → gold = neutral (compliant scenario + clause from a different pillar)

This breakdown is therefore equivalent to per-class accuracy, but the labelling 
makes the construction-time mechanism explicit.

| Method | gold | n | base | tuned-legends | tuned-regulation |
|---|---|---|---|---|---|
| llm_generated_premise | entailment | 56 | 82.14% | 89.29% | 78.57% |
| llm_perturbed_premise | contradiction | 56 | 89.29% | 91.07% | 96.43% |
| cross_pillar_pairing | neutral | 56 | 98.21% | 98.21% | 98.21% |

## 7. Predicted label distribution

Useful for spotting label bias (e.g. a model that over-predicts `neutral`).

| Model | entailment | contradiction | neutral |
|---|---|---|---|
| (gold) | 56 | 56 | 56 |
| base | 48 | 50 | 70 |
| tuned-legends | 52 | 51 | 65 |
| tuned-regulation | 46 | 54 | 68 |

## 8. Interpretation

**Ranking by accuracy:** tuned-legends (92.86%) > tuned-regulation (91.07%) > base (89.88%).

The ordering matches the §6.5 prediction *qualitatively*: GE-NLI is the
benchmark's central test of compliance recognition, the competence that
legends are designed to teach, so tuned-legends is expected to lead and
does. The *magnitude* of the lead is small, however, and the
interpretation has to be read carefully against the statistical
evidence.

### 8.1 Effect size and statistical significance

The three 95% bootstrap CIs overlap heavily. None of the three pairwise
McNemar tests rejects the null of equal error rates at α = 0.05:

- base vs tuned-legends:    p = 0.18 (b = 2, c = 7)
- base vs tuned-regulation: p = 0.77 (b = 5, c = 7)
- tuned-legends vs tuned-regulation: p = 0.55 (b = 7, c = 4)

The closest to significance is base vs tuned-legends, with five more
items recovered by tuned-legends than lost — directionally consistent
with the central hypothesis, but on n = 168 not enough to clear the bar.
This is a power problem, not (necessarily) a null effect: a 3-percentage-
point gap on a balanced 3-class task is non-trivial but requires roughly
500–800 items to be reliably detected by McNemar at this effect size.

What the data *do* license is the weaker claim: **on this dataset, the
two fine-tuning regimes do not measurably hurt the base, and the
legends regime shows a directional advantage on the central compliance-
recognition task that is consistent with the Sargsyan & Damiani (2025)
hypothesis**. A stronger claim awaits a larger test set.

### 8.2 Where the legends advantage actually sits

The construction-method breakdown (Section 6) is the most informative
slice in this report, because each method produces a single gold class
and the differences between models concentrate cleanly:

| Gold class | base | tuned-legends | tuned-regulation |
|---|---|---|---|
| entailment (compliant scenario)        | 82.1% | **89.3%** | 78.6% |
| contradiction (perturbed scenario)     | 89.3% | 91.1%     | **96.4%** |
| neutral (cross-pillar pairing)         | 98.2% | 98.2%     | 98.2% |

Two findings stand out.

**On entailment, tuned-legends gains 7.1 points over the base, while
tuned-regulation actually loses 3.6 points.** The legends-trained model
is the only one that improves at recognising compliance — the exact
ability legends are designed to teach. The regulation-trained model,
trained on dense regulatory prose, becomes *more* skeptical of
compliance scenarios and over-classifies them as `neutral` (12/56 vs
6/56 for legends). This is the cleanest qualitative confirmation of the
central hypothesis in the dataset.

**On contradiction, the picture inverts: tuned-regulation gains 7.1
points over the base, tuned-legends only 1.8.** Detecting that "15%
female representation" violates a "40% target" requires precise factual
recall against the regulatory text — which is exactly what the
regulation corpus trains. The legends corpus, full of *compliant*
scenarios by construction, gives weaker signal for spotting numeric
violations.

**On neutral, all three models are saturated at 98.2%** — the
cross-pillar pairing is so semantically distinct from the hypothesis
that the task is trivially solved zero-shot. This subset carries no
discriminative information between models.

So the headline accuracy gap obscures a more interesting pattern: the
two fine-tuning regimes are not just *quantitatively close* but
*qualitatively complementary*. Legends teach compliance recognition;
regulation text teaches violation detection. This is exactly the
prediction §6.5 makes implicitly when it argues that legends "embed
regulatory understanding" while regulation prose anchors "factual
recall".

### 8.3 Per-pillar reading

Per-pillar accuracies (Section 5) are mostly stable across models, with
two exceptions worth flagging:

- **violence_stereotypes (n = 72, the largest bucket):** tuned-legends
  84.7% vs tuned-regulation 90.3%. The regulation-tuned model loses
  ground here. Given that violence_stereotypes contains a high density
  of legal references (Istanbul Convention, Victims' Rights Directive,
  ILO conventions), this is unexpected and worth re-checking by
  inspecting the items where tuned-regulation flipped a correct base
  prediction to wrong.
- **equal_economy (n = 18):** the base scores 83.3%, both fine-tuned
  models score 94.4%. With n = 18 the effective CI is wide (≈ ±15
  points) so this should be reported as suggestive, not conclusive.

The other three pillars are flat across models within sampling noise.

### 8.4 Label-distribution bias

All three models over-predict `neutral` relative to gold (gold = 56;
base = 70, legends = 65, regulation = 68). This is a classic NLI
artifact: when the model is uncertain, `neutral` is the safe default.
The bias is mildest in tuned-legends (+9 over gold) and worst in base
(+14). No model under-predicts `contradiction` materially.

### 8.5 Take-aways for the thesis

1. The §6.5 prediction holds *directionally* — tuned-legends leads, in
   line with the Sargsyan & Damiani hypothesis — but the gap is not
   statistically significant on n = 168.
2. The construction-method breakdown reveals a *qualitative*
   complementarity that the headline accuracy hides: legends help with
   recognising compliance, regulation text helps with detecting
   violations. This is arguably more interesting than the headline
   number.
3. The neutral subset is saturated and uninformative; future versions
   of the dataset should make `neutral` items harder (e.g. by drawing
   the cross-pillar hypothesis from a *thematically adjacent* pillar
   rather than an arbitrary one).
4. To test the central hypothesis with statistical power, the test set
   would need to grow to roughly 3× its current size, *or* the
   fine-tuning intervention would need to produce a larger absolute
   effect (e.g. by training for more epochs or on a larger legends
   corpus).
