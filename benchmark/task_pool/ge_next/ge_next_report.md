# GE-NEXT Evaluation Report

**Items evaluated:** 150 (30 per pillar, balanced). 
**Models:** base, tuned-legends, tuned-regulation. 
**Setting:** zero-shot, identical system prompt across models, `temperature = 0`.

**Headline metric (per §6.8 spec):** Accuracy. Macro-F1 reported alongside as confirmatory; gold-position is approximately balanced across A/B/C/D (37/38/37/38).

---

## 1. Headline results

| Model | Accuracy (95% CI) | Macro-F1 (95% CI) |
|---|---|---|
| base | 92.00% (95% CI: 87.33%–96.00%) | 92.00% (95% CI: 87.39%–96.06%) |
| tuned-legends | 98.67% (95% CI: 96.67%–100.00%) | 98.66% (95% CI: 96.55%–100.00%) |
| tuned-regulation | 94.00% (95% CI: 90.00%–97.33%) | 93.98% (95% CI: 89.92%–97.44%) |

Confidence intervals are 2,000-resample non-parametric bootstrap.

## 2. Per-position precision, recall, F1

Position-level metrics serve as a label-bias diagnostic; the discriminating slice for GE-NEXT is the per-distractor-type breakdown in §6.

### base

| Position | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| A | 87.50% | 94.59% | 90.91% | 37 |
| B | 91.67% | 86.84% | 89.19% | 38 |
| C | 91.89% | 91.89% | 91.89% | 37 |
| D | 97.30% | 94.74% | 96.00% | 38 |

### tuned-legends

| Position | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| A | 100.00% | 97.30% | 98.63% | 37 |
| B | 97.44% | 100.00% | 98.70% | 38 |
| C | 97.30% | 97.30% | 97.30% | 37 |
| D | 100.00% | 100.00% | 100.00% | 38 |

### tuned-regulation

| Position | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| A | 90.00% | 97.30% | 93.51% | 37 |
| B | 94.44% | 89.47% | 91.89% | 38 |
| C | 94.44% | 91.89% | 93.15% | 37 |
| D | 97.37% | 97.37% | 97.37% | 38 |

## 3. Pairwise comparisons (McNemar's exact test)

`b` = items where the first model is correct and the second is wrong; `c` = the opposite. Exact two-sided binomial p-value on `min(b,c)` under H0 (equal error rates).

| Pair | b | c | n_disagree | p-value | Significant at α=0.05 |
|---|---|---|---|---|---|
| base vs tuned-legends | 1 | 11 | 12 | 0.0063 | **yes** |
| base vs tuned-regulation | 0 | 3 | 3 | 0.2500 | no |
| tuned-legends vs tuned-regulation | 8 | 1 | 9 | 0.0391 | **yes** |

## 4. Breakdown by pillar

| Pillar | n | base | tuned-legends | tuned-regulation |
|---|---|---|---|---|
| violence_stereotypes | 30 | 90.00% | 96.67% | 93.33% |
| leadership_participation | 30 | 93.33% | 96.67% | 93.33% |
| funding_global_action | 30 | 93.33% | 100.00% | 93.33% |
| equal_economy | 30 | 90.00% | 100.00% | 96.67% |
| mainstreaming_intersectionality | 30 | 93.33% | 100.00% | 93.33% |

## 5. Predicted-position distribution

Useful for spotting positional bias (e.g. a model that gravitates to a particular letter). Gold is near-uniform across positions by construction.

| Model | A | B | C | D |
|---|---|---|---|---|
| (gold) | 37 | 38 | 37 | 38 |
| base | 40 | 36 | 37 | 37 |
| tuned-legends | 36 | 39 | 37 | 38 |
| tuned-regulation | 40 | 36 | 36 | 38 |

## 6. Per-distractor-type error rate

The most informative diagnostic for GE-NEXT. When a model is wrong, *which* of the three typed distractors does it pick? Computed on the 100-item v1 subset (IDs 001–020 per pillar) for which option-type labels are available. The remaining 50 items carry predictions but no per-option type assignment at the time of evaluation and are excluded from this slice only.

Each cell reports the share of *that model's wrong picks* that fell on a distractor of the given type.

| Distractor type | base | tuned-legends | tuned-regulation |
|---|---|---|---|
| performative | 28.57% (2/7) | 50.00% (1/2) | 20.00% (1/5) |
| cost_optimising | 14.29% (1/7) | 0.00% (0/2) | 20.00% (1/5) |
| orthogonal | 57.14% (4/7) | 50.00% (1/2) | 60.00% (3/5) |

## 7. Interpretation

**Ranking by accuracy:** tuned-legends (98.67%) > tuned-regulation (94.00%) > base (92.00%).

The result aligns with the §6.8 prediction: GE-NEXT is the most direct probe of the compliance-versus-cost arbitrage that motivates the legend hypothesis, and **tuned-legends leads on aggregate accuracy** by 6.67 points over the base and 4.67 points over tuned-regulation. Unlike GE-NLI, where the legends advantage was directional but not statistically separable on n = 168, here on n = 150 **both pairwise comparisons involving tuned-legends clear α = 0.05**: base vs tuned-legends (b = 1, c = 11, p = 0.0063) and tuned-legends vs tuned-regulation (b = 8, c = 1, p = 0.0391). The base-vs-regulation comparison (b = 0, c = 3, p = 0.2500) does not separate the two models. GE-NEXT is the first task in the benchmark on which the legend-hypothesis prediction is formally significant under the McNemar protocol.

### 7.1 Error-pattern asymmetry between models

The discordance counts (b, c) under McNemar are themselves the most informative slice of the comparison. Against the base, tuned-legends recovers 11 items that the base misses and loses only 1. Against tuned-regulation, tuned-legends recovers 8 items that the regulation-tuned model misses and loses only 1. The error-overlap is therefore highly asymmetric: the items tuned-legends gets right are mostly a strict superset of the items the other two get right. This is the cleanest qualitative signature in the benchmark of a competence the legends teach and the regulation training does not — the four-beat identify → design → implement → measure arc that every gold option in GE-NEXT mirrors.

### 7.2 Per-distractor-type breakdown (diagnostic)

The per-distractor-type slice in §6 was designed as the §6.8 diagnostic on which kind of failure each model is prone to when wrong. On the v1 subset (n = 100, the items for which option-type labels are available), tuned-legends produces only **2** wrong picks in total against **7** for the base and **5** for tuned-regulation. The denominator on tuned-legends is therefore too small to characterise the distribution of its errors reliably, and this diagnostic should be read as suggestive only. The base and the regulation-tuned model both fall on the *orthogonal* distractor most often when wrong (57% and 60% of their wrong picks respectively), consistent with a failure mode in which the model selects a plausible but pillar-mismatched action. The performative distractor is selected at a moderate rate by the base (29%) and a lower rate by tuned-regulation (20%); these numbers should not be over-read given the small absolute error counts. A v2 extension that lifts the v1 subset to ~300 items would allow this diagnostic to be interpreted with confidence; on the current data the headline accuracy and the McNemar significance carry the result.

### 7.3 Per-pillar reading

The per-pillar pattern (§4) is broadly consistent with the aggregate. Tuned-legends matches or exceeds the other two models on every pillar; on no pillar is it the worst of the three. Per-pillar n = 30 yields wide effective CIs (≈ ±18 points), so per-pillar gaps should be read as directional rather than separately significant.

### 7.4 Label-distribution bias

The predicted-position distribution (§5) shows no systematic letter-position bias for any of the three models — predicted counts are close to the gold distribution across A/B/C/D for every model. This matters because the gold position is uniformly distributed by construction; any positional bias would inflate or deflate accuracy on a position-specific subset. The absence of bias licenses the interpretation that the discriminating signal is option-content, not option-position.

### 7.5 Take-aways for the thesis

1. **GE-NEXT is the first task in GenderEqGLUE on which the legend hypothesis clears formal significance.** The base-vs-legends comparison (p = 0.0063) and the regulation-vs-legends comparison (p = 0.0391) both reject the null of equal error rates at α = 0.05. The GE-NLI result was directional and consistent with the hypothesis but did not clear the bar on n = 168; GE-NEXT clears it on n = 150.
2. **The result tracks the §6.8 prediction.** GE-NEXT was framed in the pipeline document as the most direct probe of whether the legends embed a *decision pattern* rather than mere regulatory content. The headline acc gap to tuned-regulation (4.67 pts) and the highly asymmetric McNemar discordance (b = 8, c = 1) support that framing: tuned-regulation's stronger raw regulatory recall does not translate into action-selection accuracy when the options are competing substantive-style proposals, while the legend corpus — which exposes the model to substantive compliance enacted across diverse scenarios — does.
3. **The cost-optimising distractor is not the dominant failure mode** on the v1 subset, contrary to the §6.8 framing. All three models reject the cost-optimising option readily; the dominant non-substantive error is the *orthogonal* distractor, with the performative distractor second. The legend advantage in GE-NEXT is therefore most accurately characterised as protection against misdirected and performative substitution rather than against cost-driven deferral. This is a refinement of the §6.8 hypothesis, not a refutation of it: the underlying *decision pattern* the legends embed protects against all three non-substantive failure modes, but the cost-driven one is the easiest of the three for the base model to discriminate without legend training.
4. **Statistical robustness.** The McNemar significance on n = 150 is non-marginal (p = 0.006 for base-vs-legends, p = 0.039 for regulation-vs-legends) and survives the small-sample exact-binomial protocol. A v2 extension would tighten the CIs further and allow the per-distractor-type slice (§6) to be interpreted with the confidence the headline result already enjoys.
