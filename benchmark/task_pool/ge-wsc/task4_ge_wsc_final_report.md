# Task 4 — GE-WSC Final Report

**Stereotype-Aware Coreference (WinoBias)**

This report documents the results of the GE-WSC task as defined in
`pipeline.md` §6.7 and aggregates them according to the reporting
protocol of §6.10.

---

## 1. Test set

GE-WSC reuses the open-source **WinoBias** dataset (Zhao et al., 2018)
without any modification, drawing items from the four canonical subsets.
The evaluated test set contains **100 items**, balanced across subsets:

| Subset       | N  | Description                                                    |
|--------------|---:|----------------------------------------------------------------|
| `type1_pro`  | 25 | Type-1 sentences whose gold antecedent matches the stereotype  |
| `type1_anti` | 25 | Type-1 sentences whose gold antecedent contradicts it          |
| `type2_pro`  | 25 | Type-2 sentences whose gold antecedent matches the stereotype  |
| `type2_anti` | 25 | Type-2 sentences whose gold antecedent contradicts it          |

Type-1 sentences require world knowledge to resolve coreference (no
explicit syntactic cue), Type-2 sentences contain syntactic cues that
make resolution unambiguous in principle. The two `_pro` / `_anti`
variants of each type share the same surface form and differ only in
which professional role is referenced by the pronoun, isolating the
contribution of stereotype to the model's decision.

Predictions for the three models (`base`, `tuned-legends`,
`tuned-regulation`) are stored in `ge_wsc_predictions_template.csv`.

## 2. Headline metric

The headline metric is **accuracy** averaged across the four subsets.
Bootstrap 95% confidence intervals (2000 resamples, `seed=42`) are
reported alongside.

| Model             | Accuracy | 95% CI           |
|-------------------|---------:|------------------|
| base              |    0.930 | [0.880, 0.980]   |
| tuned-legends     |    0.960 | [0.920, 0.990]   |
| tuned-regulation  |    0.960 | [0.920, 0.990]   |

The two fine-tuned variants are tied at the headline level, and both
show a small numerical gain over the base. The confidence intervals
overlap substantially, so the gain is not separable from sampling noise
on a 100-item set.

## 3. Per-subset accuracy

Per-subset accuracy is the most informative breakdown for this task,
since it exposes whether errors concentrate on stereotype-aligned or
stereotype-contradicting items.

| Subset       | base   | tuned-legends | tuned-regulation |
|--------------|-------:|--------------:|-----------------:|
| `type1_pro`  | 0.920  | 0.920         | 0.960            |
| `type1_anti` | 0.880  | 0.920         | 0.880            |
| `type2_pro`  | 1.000  | 1.000         | 1.000            |
| `type2_anti` | 0.920  | 1.000         | 1.000            |

All three models saturate Type-2 `_pro` and reach near-saturation on
Type-2 `_anti`. The harder cases — Type-1, where world knowledge is
required — are also where the small inter-model differences appear.

## 4. Gender Parity Score

The Gender Parity Score, as defined in §6.7, is the absolute difference
between accuracy on `_pro` and `_anti` items. A model whose decisions
are independent of the stereotype direction has a parity score of zero.

| Model             | parity (Type-1) | parity (Type-2) | Gender Parity Score (mean) |
|-------------------|----------------:|----------------:|---------------------------:|
| base              | 0.040           | 0.080           | **0.060**                  |
| tuned-legends     | 0.000           | 0.000           | **0.000**                  |
| tuned-regulation  | 0.080           | 0.000           | **0.040**                  |

`tuned-legends` reaches a perfect parity score (the same accuracy on
`_pro` and `_anti` items in both types). `tuned-regulation` is parity-
neutral on Type-2 but slightly *worse* than the base on Type-1 parity:
its gain comes entirely from `_pro` items (0.92 → 0.96), which widens
the pro/anti gap. This is the kind of asymmetric improvement that the
parity score is designed to detect.

## 5. Pairwise model comparison (McNemar)

We apply McNemar's test on per-item correctness to test whether two
models differ significantly on the same set of items. The contingency
counts `n01` and `n10` report how many items only model A (resp. only
model B) gets right. With small discordant counts (<25), the exact
binomial variant is used; otherwise the asymptotic χ² with continuity
correction.

| Comparison                                | n01 | n10 | statistic | p-value | significant (α=0.05) |
|-------------------------------------------|----:|----:|----------:|--------:|----------------------|
| base vs tuned-legends                     |   1 |   4 |     1.000 |  0.3750 | no                   |
| base vs tuned-regulation                  |   0 |   3 |     0.000 |  0.2500 | no                   |
| tuned-legends vs tuned-regulation         |   2 |   2 |     2.000 |  1.0000 | no                   |

No pairwise comparison reaches significance. The +0.030 gap between the
base and the two tuned variants rests on a handful of discordant items
and cannot be distinguished from noise on a 100-item sample. This is
the same conclusion suggested by the overlapping bootstrap CIs in §2.

## 6. Discussion

**Comparison with §6.7 expectations.** §6.7 explicitly states that
*"the bias originates in the pretraining distribution rather than in
the fine-tuning corpus, we do not expect either fine-tuned model to
outperform the base on this task — and the result, whatever it is, is
informative"*. The observed result is consistent with this prediction:
both fine-tuned models score within 0.03 of the base, all three differ
within sampling noise, and McNemar fails to reject the null in any
pairwise comparison.

**Note on the absolute level.** The base model already achieves 93%
accuracy on a balanced WinoBias sample. This is high relative to the
60–70% range typical of mid-sized encoder models on the same benchmark,
but consistent with what current instruction-tuned generative LLMs of
the size used in this project (cf. §3 of the diary on fine-tuning
backbone choice) achieve on the four-subset average. The headline
score should therefore be interpreted as a **near-ceiling result** on
this particular dataset, which mechanically compresses the visible
discriminative range between the three models. A harder coreference
benchmark would likely separate the three models more cleanly; on
WinoBias they are essentially indistinguishable.

**Parity reading.** The most informative outcome at this scale is the
parity score rather than the accuracy. `tuned-legends` is the only
model that achieves perfect parity on both types simultaneously,
suggesting that the legends fine-tuning corpus — which by construction
features gender-balanced characters in non-stereotypical roles —
nudges the model toward more uniform handling of pro- and anti-
stereotype items. We do not over-interpret this finding, however,
since it rests on differences of one or two items per subset.

## 7. GenderEqGLUE Score component

For the aggregate score the GE-WSC component is the **accuracy**
(§6.10):

| Model             | GE-WSC component (accuracy) |
|-------------------|----------------------------:|
| base              | 0.930                       |
| tuned-legends     | 0.960                       |
| tuned-regulation  | 0.960                       |

The Gender Parity Score is reported as a **separate diagnostic** and
does not enter the aggregate score, in line with the SuperGLUE practice
of reporting Winogender outside the headline number.

## 8. Reproducibility

- Predictions: `evaluation/ge_wsc/ge_wsc_predictions_template.csv` (100 rows).
- Metric script: `evaluation/ge_wsc/ge_wsc_metrics.py`.
- Bootstrap: 2000 resamples, `numpy` PCG64, `seed=42`.
- McNemar: `statsmodels.stats.contingency_tables.mcnemar`, exact
  binomial when `n01+n10 < 25`, asymptotic χ² with continuity
  correction otherwise.
- Per-model JSON output: `benchmark/genderegglue/results/wsc_results.json`.
