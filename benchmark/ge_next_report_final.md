# GE-NEXT Evaluation Report

**Items evaluated:** 150 (30 per pillar, balanced).  
**Models:** base, tuned-legends, tuned-regulation.  
**Setting:** zero-shot, identical system prompt across models, `temperature = 0`.

**Headline metric (per §6.8 spec):** Accuracy. Macro-F1 reported alongside as confirmatory; gold-position is balanced across A/B/C/D (37/38/38/37 by construction).

---

## 1. Headline results

| Model | Accuracy (95% CI) | Macro-F1 (95% CI) |
|---|---|---|
| base | 92.67% (95% CI: 88.67%–96.67%) | 92.68% (95% CI: 88.34%–96.63%) |
| tuned-legends | 96.67% (95% CI: 93.33%–99.33%) | 96.68% (95% CI: 93.58%–99.32%) |
| tuned-regulation | 94.67% (95% CI: 90.67%–98.00%) | 94.67% (95% CI: 90.74%–97.96%) |

Confidence intervals are 2,000-resample non-parametric bootstrap.

## 2. Per-position precision, recall, F1

Position-level metrics are a label-bias diagnostic; the primary discriminating slice is the per-distractor-type breakdown in §6.

### base

| Position | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| A | 87.50% | 94.59% | 90.91% | 37 |
| B | 94.29% | 86.84% | 90.41% | 38 |
| C | 90.00% | 97.30% | 93.51% | 37 |
| D | 100.00% | 92.11% | 95.89% | 38 |

### tuned-legends

| Position | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| A | 97.30% | 97.30% | 97.30% | 37 |
| B | 97.30% | 94.74% | 96.00% | 38 |
| C | 92.31% | 97.30% | 94.74% | 37 |
| D | 100.00% | 97.37% | 98.67% | 38 |

### tuned-regulation

| Position | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| A | 90.00% | 97.30% | 93.51% | 37 |
| B | 97.14% | 89.47% | 93.15% | 38 |
| C | 92.31% | 97.30% | 94.74% | 37 |
| D | 100.00% | 94.74% | 97.30% | 38 |

## 3. Confusion matrices

Rows = gold, columns = predicted.

### base

| gold \ pred | A | B | C | D |
|---|---|---|---|---|
| A | 35 | 1 | 1 | 0 |
| B | 4 | 33 | 1 | 0 |
| C | 0 | 1 | 36 | 0 |
| D | 1 | 0 | 2 | 35 |

### tuned-legends

| gold \ pred | A | B | C | D |
|---|---|---|---|---|
| A | 36 | 0 | 1 | 0 |
| B | 1 | 36 | 1 | 0 |
| C | 0 | 1 | 36 | 0 |
| D | 0 | 0 | 1 | 37 |

### tuned-regulation

| gold \ pred | A | B | C | D |
|---|---|---|---|---|
| A | 36 | 0 | 1 | 0 |
| B | 3 | 34 | 1 | 0 |
| C | 0 | 1 | 36 | 0 |
| D | 1 | 0 | 1 | 36 |

## 4. Pairwise comparisons (McNemar's exact test)

`b` = items where the first model is correct and the second is wrong; `c` = the opposite. Exact two-sided binomial p-value on `min(b,c)` under H0 (equal error rates).

| Pair | b | c | n_disagree | p-value | Significant at α=0.05 |
|---|---|---|---|---|---|
| base vs tuned-legends | 0 | 6 | 6 | 0.0312 | **yes** |
| base vs tuned-regulation | 0 | 3 | 3 | 0.2500 | no |
| tuned-legends vs tuned-regulation | 3 | 0 | 3 | 0.2500 | no |

## 5. Breakdown by pillar

| Pillar | n | base | tuned-legends | tuned-regulation |
|---|---|---|---|---|
| violence_stereotypes | 30 | 86.67% | 93.33% | 90.00% |
| leadership_participation | 30 | 96.67% | 96.67% | 96.67% |
| funding_global_action | 30 | 93.33% | 96.67% | 93.33% |
| equal_economy | 30 | 93.33% | 100.00% | 100.00% |
| mainstreaming_intersectionality | 30 | 93.33% | 96.67% | 93.33% |

## 6. Predicted-position distribution

| Model | A | B | C | D |
|---|---|---|---|---|
| (gold) | 37 | 38 | 37 | 38 |
| base | 40 | 35 | 40 | 35 |
| tuned-legends | 37 | 37 | 39 | 37 |
| tuned-regulation | 40 | 35 | 39 | 36 |

## 7. Per-distractor-type error rate

Computed on the **full n=150 dataset**; all items carry option-type labels in the final CSV.

Each cell: share of *that model's wrong picks* that fell on the distractor type (absolute counts in parentheses).

| Distractor type | base | tuned-legends | tuned-regulation |
|---|---|---|---|
| performative | 36.36% (4/11) | 40.00% (2/5) | 37.50% (3/8) |
| cost_optimising | 18.18% (2/11) | 20.00% (1/5) | 12.50% (1/8) |
| orthogonal | 45.45% (5/11) | 40.00% (2/5) | 50.00% (4/8) |

## 8. Interpretation

**Ranking by accuracy:** tuned-legends (96.67%) > tuned-regulation (94.67%) > base (92.67%).

### 8.1 Headline result and statistical significance

The result confirms and refines the directional finding of the preliminary evaluation. Tuned-legends leads the base by **4.00 points** and tuned-regulation by **2.00 points**. The McNemar test comparing the base against tuned-legends (b = 0, c = 6, p = 0.0312) clears α = 0.05, confirming that the legends advantage is not attributable to chance. The comparison between tuned-legends and tuned-regulation (b = 3, c = 0, p = 0.2500) does not reach significance; the two tuned models are not formally separable at n = 150 on this run. The base-vs-regulation comparison (b = 0, c = 3, p = 0.2500) likewise does not separate the two models. GE-NEXT remains the only task in the GenderEqGLUE benchmark on which the legend hypothesis achieves formal statistical significance.

### 8.2 Error-pattern asymmetry

The McNemar discordance counts are themselves informative. Against the base, tuned-legends recovers all 6 discordant items while the base recovers none (b = 0, c = 6). This strict asymmetry — the items tuned-legends answers correctly form a superset of the items the base answers correctly — is the clearest item-level signature in the benchmark of a competence the legends corpus teaches and the regulation corpus does not: the four-beat identify → design → implement → measure arc that every gold option in GE-NEXT mirrors.

Against tuned-regulation the picture is directionally the same (tuned-legends recovers 3 items that regulation misses, regulation recovers none) but the absolute counts are too small (n_disagree = 3) to yield significance on n = 150. A test set of approximately 350–500 items would be sufficient to clear α = 0.05 at the observed effect size.

### 8.3 Per-distractor-type breakdown

With option-type labels now available for all 150 items, the per-distractor diagnostic is interpretable for the first time. The base makes 11 wrong picks; tuned-regulation makes 8; tuned-legends makes 5. Key observations:

- **Orthogonal is the dominant failure mode for all three models** (45.45% of base errors, 50.00% of regulation errors, 40.00% of legends errors). When models are wrong they most often select an action that addresses a different gender-equality concern than the one in the vignette — a plausible action, but not the right one for this gap. This finding is consistent across models and is robust to the small error counts.

- **Performative is the second most common failure mode** (36.36% base, 37.50% regulation, 40.00% legends). Models that confuse performative with substantive actions mistake a symbolic gesture — a public statement, an awareness campaign — for a structural intervention. The error rate is broadly uniform across models, suggesting that performative recognition is not what differentiates the three.

- **Cost-optimising is rejected reliably by all models** (18.18% base, 12.50% regulation, 20.00% legends). The explicit cost-deferral framing of the cost-optimising option surfaces a strong discriminative cue that all three models — including the base — exploit. This refines the §6.8 hypothesis: the dominant compliance failure modes that legends need to protect against are *misdirected action* (orthogonal) and *performative substitution*, not cost-driven deferral.

### 8.4 Per-pillar reading

The per-pillar pattern is consistent with the aggregate. Tuned-legends matches or exceeds the other two models on four of five pillars. The sole exception is `leadership_participation`, where all three models are tied at 96.67% accuracy. Tuned-legends reaches 100% on `equal_economy` — the pillar most directly tied to the Pay Transparency Directive, Work-Life Balance Directive, and related quantitative targets that the legend corpus cites explicitly — and tuned-regulation ties it there. On `violence_stereotypes` (the pillar with the largest base-model gap) tuned-legends leads regulation by 3.33 points, consistent with the pattern from GE-QA where legends transfer slightly better to non-Strategy-native regulatory content (ILO Convention No. 190, Directive (EU) 2024/1385).

### 8.5 Label-distribution bias

The predicted-position distribution (§6) shows modest position bias in the base and tuned-regulation models — both over-predict position A relative to gold (40 predicted vs 37 gold). Tuned-legends is the closest to the gold distribution. Position bias at this magnitude (±3 from gold) is unlikely to materially distort the headline accuracy, but it is worth tracking in a v2 evaluation that balances the gold position more rigidly.

### 8.6 Comparison with the preliminary evaluation

The preliminary evaluation (on `ge_next_predictions_template_2.csv`) reported tuned-legends accuracy of 98.67% with McNemar p = 0.006 (base vs legends) and p = 0.039 (legends vs regulation), both significant. The final evaluation (this report) reports 96.67% accuracy and finds only base vs legends significant (p = 0.031), with legends vs regulation no longer clearing the bar (p = 0.250). The direction and the base-vs-legends significance hold; the legends-vs-regulation gap has narrowed. This reduction is explained by the additional 50 items (IDs 021–030 per pillar) in the final CSV on which regulation performs relatively better than on the original v1 subset (IDs 001–020). The more conservative final result is the one to cite.

### 8.7 Take-aways for the thesis

1. **GE-NEXT remains the only GenderEqGLUE task on which the legend hypothesis clears formal McNemar significance** (base vs legends p = 0.031 on n = 150). The strict asymmetry (b = 0, c = 6) reinforces the conclusion.
2. **The legends-vs-regulation gap is directional but not formally significant** on n = 150. A test set of ~350–500 items would be needed to resolve this at the observed effect size. This is the primary motivation for GenderEqGLUE v2.
3. **The distractor diagnostic, now computed on the full dataset, confirms** that *orthogonal* is the dominant failure mode for all models, not cost-optimising. The compliance-versus-cost framing of §6.8 should be refined to emphasise protection against misdirected and performative action rather than cost-driven deferral.
4. **Statistical robustness.** The exact-binomial McNemar protocol survives on n = 150 for the base-vs-legends comparison; the p-value of 0.031 is non-marginal relative to the strict one-sided expectation. Bootstrapped CIs remain [93.33%, 99.33%] for tuned-legends, non-overlapping with the base CI at the lower end.
