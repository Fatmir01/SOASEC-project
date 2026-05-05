# Task 5 — GE-STANCE Final Report

**Gender Equality Stance Detection (CIVICS + curated)**

This report documents the results of the GE-STANCE task as defined in
`pipeline.md` §6.8 and aggregates them according to the reporting
protocol of §6.10.

---

## 1. Test set

GE-STANCE is a three-class classification task over the labels
`supportive`, `neutral`, and `against` with respect to gender equality.
The evaluated test set contains **120 items** drawn from two sources,
balanced by gold class:

| Source           | N  | Notes                                                 |
|------------------|---:|-------------------------------------------------------|
| `civics_filtered`| 28 | CIVICS items filtered on `gender inclusivity` and `anti-discrimination` labels |
| `curated`        | 92 | Statements written by the team and double-labelled internally |
| **Total**        | **120** |                                                |

Class distribution (balanced by construction at 40/40/40):

| Gold label    | N  |
|---------------|---:|
| `supportive`  | 40 |
| `neutral`     | 40 |
| `against`     | 40 |

The two sources are **not symmetric** in difficulty (cf. §3.2), and the
imbalance toward `curated` reflects the practical impossibility of
extracting `against` and `neutral` items from EU institutional sources,
which are uniformly supportive by construction (§6.8).

Predictions for the three models (`base`, `tuned-legends`,
`tuned-regulation`) are stored in `ge_stance_predictions_template.csv`.

## 2. Headline metric

The headline metric is **Macro-F1** across the three classes, with
bootstrap 95% confidence intervals (2000 resamples, `seed=42`).
Accuracy is reported alongside as a diagnostic.

| Model             | Macro-F1 | 95% CI           | Accuracy |
|-------------------|---------:|------------------|---------:|
| base              | 0.833    | [0.766, 0.892]   | 0.833    |
| tuned-legends     | 0.737    | [0.663, 0.811]   | 0.758    |
| tuned-regulation  | **0.867**| [0.806, 0.924]   | 0.867    |

`tuned-regulation` is the best model. **`tuned-legends` underperforms
the base** by about 10 macro-F1 points, and its 95% CI does not overlap
with that of `tuned-regulation`. This is the clearest pairwise gap we
observe on any GenderEqGLUE task, and it runs in the *opposite*
direction to the expectation in §6.8. This result is analysed in §6.

## 3. Diagnostic breakdowns

### 3.1 Per-class F1

| Class         | base   | tuned-legends | tuned-regulation |
|---------------|-------:|--------------:|-----------------:|
| `supportive`  | 0.740  | **0.500**     | 0.806            |
| `neutral`     | 0.773  | 0.724         | 0.822            |
| `against`     | 0.987  | 0.987         | 0.974            |

All three models near-perfectly identify `against` items. The model
ranking on macro-F1 is therefore driven by the two non-trivial classes,
`supportive` and `neutral`. The collapse of `tuned-legends` is fully
concentrated on the `supportive` class (F1 drops from 0.740 to 0.500),
while its `neutral` F1 stays close to the base.

### 3.2 Per-source Macro-F1

| Source            | base  | tuned-legends | tuned-regulation |
|-------------------|------:|--------------:|-----------------:|
| `civics_filtered` | 0.233 | 0.044         | 0.252            |
| `curated`         | 0.898 | 0.957         | 0.933            |

This breakdown reveals a **large source-induced effect** that the
headline metric averages over. All three models perform very well on
`curated` items (≥0.90 macro-F1) and very poorly on `civics_filtered`
items (≤0.26 macro-F1). The size and direction of the gap matters in
both directions:

- The `civics_filtered` items are public-sphere statements that are
  shorter, more colloquial and often ironic. They are out of
  distribution for all three models and dominate the failure modes.
- On the in-distribution `curated` items, `tuned-legends` is in fact
  the strongest model (0.957). Its weakness on the headline number is
  due almost entirely to the `civics_filtered` slice, where it is
  three times worse than the other two models on macro-F1.

This is the same diagnostic concern raised in §7.4 of the methodology
document about source/domain coupling, and it is the single most
important caveat for interpreting the headline score.

### 3.3 Confusion matrices

Rows are gold labels, columns are predictions, in the order
`[supportive, neutral, against]`.

**base**
```
              supp.  neu.  agai.
supportive  [   27 ,  13 ,   0 ]
neutral     [    6 ,  34 ,   0 ]
against     [    0 ,   1 ,  39 ]
```

**tuned-legends**
```
              supp.  neu.  agai.
supportive  [   14 ,  26 ,   0 ]
neutral     [    2 ,  38 ,   0 ]
against     [    0 ,   1 ,  39 ]
```

**tuned-regulation**
```
              supp.  neu.  agai.
supportive  [   29 ,  11 ,   0 ]
neutral     [    3 ,  37 ,   0 ]
against     [    0 ,   2 ,  38 ]
```

The structure is the same in all three models — confusion is
overwhelmingly along the `supportive ↔ neutral` axis, never against
`against` — but the *direction* of the confusion is informative.
`tuned-legends` over-predicts `neutral` on supportive items (26 of
40 supportive items are mislabelled as neutral, and only 14 are
correctly identified). The base errs in the same direction but less
severely (13 of 40), and `tuned-regulation` actually slightly improves
over the base on this confusion (11 of 40). No model ever predicts
`against` for a `supportive` or `neutral` gold item.

## 4. Pairwise model comparison (McNemar)

| Comparison                                | n01 | n10 | statistic | p-value | significant (α=0.05) |
|-------------------------------------------|----:|----:|----------:|--------:|----------------------|
| base vs tuned-legends                     |  14 |   5 |     5.000 |  0.0636 | borderline           |
| base vs tuned-regulation                  |   2 |   6 |     2.000 |  0.2891 | no                   |
| tuned-legends vs tuned-regulation         |   3 |  16 |     3.000 |  **0.0044** | **yes**         |

The single statistically significant pairwise difference on the entire
GenderEqGLUE task suite is **tuned-legends < tuned-regulation on
GE-STANCE**. The base-vs-tuned-legends drop is borderline (p≈0.06) and
would likely become significant on a larger test set. The base-vs-
tuned-regulation gain is not significant: most of the +0.034 macro-F1
of tuned-regulation over the base is concentrated on items that the
base also handles correctly, leaving few discordant pairs.

## 5. GenderEqGLUE Score component

| Model             | GE-STANCE component (Macro-F1) |
|-------------------|-------------------------------:|
| base              | 0.833                          |
| tuned-legends     | 0.737                          |
| tuned-regulation  | 0.867                          |

## 6. Discussion

### 6.1 The result contradicts §6.8's prediction

§6.8 articulated the central expectation: *"Because legends embody
positive normative behaviour, the tuned-legends model is expected to
match or exceed the tuned-regulation model on this task — providing a
second piece of evidence, alongside GE-NLI, for the central hypothesis
of Sargsyan and Damiani (2025)."*

The observed result is the opposite: **tuned-legends is significantly
worse than tuned-regulation on GE-STANCE**, and this is the only
McNemar-significant pairwise difference in the entire benchmark. The
prediction is therefore not supported by GE-STANCE data.

### 6.2 Mechanism of the drop

The collapse of `tuned-legends` on the `supportive` class — and the
confusion matrix showing 26 `supportive → neutral` mispredictions —
suggests a specific failure mode rather than a general loss of
capability. A plausible reading is that the legends corpus, by
construction, narrates *positive* compliance behaviours but rarely
makes overtly *supportive* declarations. The fine-tuning may have
nudged the model toward describing gender-equality content in
descriptive/neutral language rather than explicitly endorsing
language. The model is not breaking — it is correctly recognising
that the items are on-topic for gender equality (none of the 40
supportive items are mislabelled as `against`) — but it is reluctant
to assign the `supportive` label.

The same effect is visible, in milder form, in the per-source
breakdown: on `curated` items, where the supportive examples are
written by the team to be unambiguously supportive, `tuned-legends`
is in fact the best model (0.957 macro-F1). The drop concentrates on
the more subtle `civics_filtered` items, where the supportive stance
is implicit rather than declared.

### 6.3 Reading the result against the central hypothesis

The hypothesis of Sargsyan and Damiani (2025) is that legends embed
*compliance* understanding more effectively than raw regulatory text.
Compliance is closer to GE-NLI (does this scenario meet the rule?)
than to GE-STANCE (does this statement endorse the value?). The two
tasks were grouped together in §6.8 as joint evidence for the
hypothesis, but the result here suggests they probe different things:
GE-STANCE rewards the ability to recognise endorsement language,
which is not a property the legends corpus emphasises. GE-NLI remains
the more direct test of the hypothesis.

We therefore read the GE-STANCE result not as a refutation of the
overall research programme but as evidence that the **scope** of the
"legends advantage" is narrower than §6.8 anticipated: it appears
where the task probes compliance-style reasoning, and it does not
appear (and may even reverse) where the task probes value-stance
classification.

### 6.4 Caveats

The 28-item `civics_filtered` slice is small, out-of-distribution for
all three models, and arithmetically dominates the negative result.
A larger, more carefully balanced curated set would tighten the CIs
and make the underlying mechanism easier to isolate. The current
finding should be read as suggestive rather than conclusive on
distribution-shifted data, while the overall ranking on the
in-distribution `curated` slice is robust.

## 7. Reproducibility

- Predictions: `evaluation/ge_stance/ge_stance_predictions_template.csv` (120 rows).
- Metric script: `evaluation/ge_stance/ge_stance_metrics.py`.
- Macro-F1 implementation: `sklearn.metrics.f1_score(average='macro', zero_division=0)` with fixed label order `[supportive, neutral, against]`.
- Bootstrap: 2000 resamples, `numpy` PCG64, `seed=42`.
- McNemar: `statsmodels.stats.contingency_tables.mcnemar`, exact binomial when `n01+n10 < 25`, asymptotic χ² with continuity correction otherwise.
- Per-model JSON output: `benchmark/genderegglue/results/stance_results.json`.
