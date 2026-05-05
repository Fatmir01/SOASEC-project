# GenderEqGLUE — Final Aggregate Report

**Benchmark:** GenderEqGLUE — five tasks evaluating an LLM on the
EU Gender Equality Strategy 2020-2025 domain, designed to test the
Sargsyan & Damiani (2025) hypothesis that legends-based fine-tuning
embeds regulatory understanding more effectively than fine-tuning on
the regulatory text itself.

**Models compared:**
- `base` — the open-pretrained backbone, no domain fine-tuning.
- `tuned-legends` — backbone fine-tuned on the QA-formatted legends
  corpus (§3 of the methodology).
- `tuned-regulation` — backbone fine-tuned on the QA-formatted EU
  Gender Equality Strategy 2020-2025 text (§4).

The two fine-tuning corpora were size-matched in JSONL line count,
per the constraint of point (7) of the challenge.

This document aggregates the five per-task reports
(`task1_ge_cls_final_report.md`, `task2_ge_nli_final_report.md`,
`task3_ge_qa_audit_report.md`, `task4_ge_wsc_final_report.md`,
`task5_ge_stance_final_report.md`) into the headline GenderEqGLUE
Score and discusses the cross-task pattern.

---

## 1. Aggregate GenderEqGLUE Score

The GenderEqGLUE Score is defined in §6.10 of the methodology as the
**unweighted arithmetic mean of the five per-task headline metrics**,
mirroring the original GLUE score. The headline metric per task is:

| Task       | Headline metric          |
|------------|--------------------------|
| GE-CLS     | Macro-F1                 |
| GE-NLI     | Accuracy                 |
| GE-QA      | (Factoid F1 + Bool Acc)/2|
| GE-WSC     | Accuracy                 |
| GE-STANCE  | Macro-F1                 |

| Model              | GE-CLS | GE-NLI | GE-QA  | GE-WSC | GE-STANCE | **GenderEqGLUE** |
|--------------------|-------:|-------:|-------:|-------:|----------:|-----------------:|
| base               | 0.833  | 0.899  | 0.929  | 0.930  |     0.833 |        **0.885** |
| tuned-legends      | 0.839  | 0.929  | 0.938  | 0.960  |     0.737 |        **0.881** |
| tuned-regulation   | **0.928** | 0.911 | **0.944** | 0.960 | **0.867** | **0.922** |

*(Bold marks the per-column maximum; ties in GE-WSC are bolded for
both `tuned-legends` and `tuned-regulation`.)*

**`tuned-regulation` is the strongest model at the aggregate level**,
with a GenderEqGLUE Score of 0.922 — a margin of +3.7 points over the
base and +4.1 points over `tuned-legends`. The aggregate ranking is
**tuned-regulation > base ≈ tuned-legends**, with the latter two
indistinguishable at the headline level (0.885 vs 0.881).

The wins-per-task tally compresses this picture:

| Model              | Wins (numerically) | Tasks won                            |
|--------------------|-------------------:|--------------------------------------|
| `tuned-regulation` |              4 / 5 | GE-CLS, GE-QA, GE-WSC (tied), GE-STANCE |
| `tuned-legends`    |              2 / 5 | GE-NLI, GE-WSC (tied)                |
| `base`             |              0 / 5 | —                                    |

`tuned-regulation` wins or ties on every task except GE-NLI;
`tuned-legends` wins outright only on GE-NLI, the task that §6.5
designates as the *central* test of the Sargsyan & Damiani (2025)
hypothesis. The base never tops a column.

## 2. Statistical significance

The §6.10 protocol applies McNemar's test to per-item correctness on
each task with binary or multi-class labels and bootstrap 95% CIs to
the headline metrics. Of the 12 pairwise McNemar comparisons run
across the four tasks where it is meaningful (GE-CLS does not have a
formal pairwise test in §6.4; GE-QA's audit defers the test to a
follow-up), **only one reaches α = 0.05**:

| Task       | Comparison                         | p-value | Significant |
|------------|------------------------------------|--------:|-------------|
| GE-NLI     | base vs tuned-legends              |   0.180 | no          |
| GE-NLI     | base vs tuned-regulation           |   0.774 | no          |
| GE-NLI     | tuned-legends vs tuned-regulation  |   0.549 | no          |
| GE-WSC     | base vs tuned-legends              |   0.375 | no          |
| GE-WSC     | base vs tuned-regulation           |   0.250 | no          |
| GE-WSC     | tuned-legends vs tuned-regulation  |   1.000 | no          |
| GE-STANCE  | base vs tuned-legends              |   0.064 | borderline  |
| GE-STANCE  | base vs tuned-regulation           |   0.289 | no          |
| GE-STANCE  | tuned-legends vs tuned-regulation  | **0.004** | **yes**   |

The single statistically significant pairwise gap in the entire
benchmark is **`tuned-legends` < `tuned-regulation` on GE-STANCE**.
Every other inter-model gap, including the GE-NLI directional win for
`tuned-legends` and the GE-CLS dominance of `tuned-regulation`, sits
inside the noise band of the test set sizes used (n = 100–168 per
task). The two largest numerical gaps — the +9 macro-F1 gap on GE-CLS
and the −10 macro-F1 gap on GE-STANCE — are also the ones the human
reader is most tempted to interpret causally; only the second clears
the formal bar.

This is a power problem more than a null result. The §7 limitations
section of the methodology document explicitly acknowledged that test
sets in the 100–500 range would discriminate between models only when
effect sizes are large; the 4-point GenderEqGLUE Score gap between
`tuned-regulation` and the other two is concentrated on GE-CLS and
GE-STANCE (the two tasks where the gold labels most directly mirror
the regulation's own ontology) and is suggestive but not formally
proven on a per-item basis.

## 3. Reading the result against the central hypothesis

The Sargsyan & Damiani (2025) hypothesis predicts that legends-based
fine-tuning produces a model that internalises **regulatory
compliance** better than a model fine-tuned on the same volume of raw
regulatory prose. §6.5 and §6.8 single out GE-NLI and GE-STANCE as the
two tasks expected to provide the cleanest test of this prediction.
The picture that emerges from the five tasks together is more
nuanced than a single yes/no.

### 3.1 Where the hypothesis is supported

**GE-NLI (the central test) supports the hypothesis directionally.**
`tuned-legends` is numerically the best model on GE-NLI (92.86%
accuracy vs 91.07% for `tuned-regulation` and 89.88% for `base`).
The construction-method breakdown in the GE-NLI report sharpens this
finding: on the **entailment** subset specifically — the items that
test compliance recognition (compliant scenario + matching regulatory
clause) — `tuned-legends` reaches 89.3% recall, against 78.6% for
`tuned-regulation` and 82.1% for `base`. This is the single cleanest
qualitative confirmation of the hypothesis in the benchmark: on the
items closest to the construct the hypothesis is *about*,
`tuned-legends` is best by a margin of 7–11 percentage points. The
limitation is statistical: McNemar p = 0.18 on n = 168, so the
directional finding does not clear the conventional bar.

**GE-WSC parity supports the hypothesis at the diagnostic level.**
On the WinoBias gender-parity diagnostic (§6.7), `tuned-legends` is
the only model that achieves a parity score of 0.000 on both Type-1
and Type-2 simultaneously — the same accuracy on `_pro` and `_anti`
items in both subsets. The base shows a 0.060 average parity gap;
`tuned-regulation` shows 0.040. The legends corpus, by construction
gender-balanced and explicitly framed against role stereotypes, is
the plausible source of this parity gain. The headline accuracy is
indistinguishable between the two tuned models, so this parity result
is the only WSC-level signal that separates them, and it goes in the
direction the hypothesis would predict.

**GE-QA on the long-answer subset and the violence_stereotypes
pillar.** On the 16 `group`-type factoid items (multi-token gold
answers ≥ 8 tokens), `tuned-legends` wins (F1 0.891 vs 0.776 for
`tuned-regulation` and 0.827 for `base`). On the 34
`violence_stereotypes` factoid items — dominated by Italian-language
Istanbul Convention passages outside the EU Strategy's English
register — `tuned-legends` again leads (0.879 vs 0.849 for
`tuned-regulation`). The legends, being narrative, transfer to
multi-token spans and to lexically diverse text in a way that the
formal regulatory prose does not.

### 3.2 Where the hypothesis is not supported

**GE-CLS is dominated by `tuned-regulation`** (macro-F1 0.928 vs
0.839 for `tuned-legends` and 0.833 for `base`), and `tuned-legends`
fails to improve on the base. The methodology document anticipated
this in §6.4: GE-CLS tests recognition of the regulation's own pillar
ontology, and the tuned-regulation corpus exposes the model directly
to the operational definitions of each pillar. The legends, written
as narrative compliance vignettes, do not encode the pillar taxonomy
in a form the classifier head can latch onto. The hypothesis is
therefore not in tension with this result — GE-CLS was always going
to be the most favourable task for `tuned-regulation`.

**GE-STANCE is the strongest counter-evidence.** `tuned-legends`
loses to `tuned-regulation` by roughly 10 macro-F1 points (0.737 vs
0.867), and this is the only pairwise gap in the benchmark that
clears McNemar at α = 0.05 (p = 0.004). The GE-STANCE report locates
the failure mode precisely: `tuned-legends` over-predicts `neutral`
on items that are gold-labelled `supportive` (26 of 40 supportive
items mislabelled as neutral, vs 13 of 40 for the base and 11 of 40
for `tuned-regulation`). The legends corpus narrates compliance
behaviour rather than declaring stance, and the fine-tuning appears
to have nudged the model toward descriptive/neutral language at the
expense of recognising endorsement language. This is a real
limitation of the legends approach for stance-style tasks, and §6.8's
prediction that legends would help on GE-STANCE is not borne out.

**GE-QA aggregate ranks `tuned-regulation` first.** The gap is small
(0.944 vs 0.938 for `tuned-legends`) and the audit shows that it
arises mechanically from the dataset's bias toward short single-span
answers (87% of factoid items): regulation training shapes the model
to produce terse, factoid-shaped extractions, which wins on the
single-span majority. On the long-answer subset and on
non-English passages the tuned-legends advantage reappears. The
overall ranking is therefore more about answer-shape preferences
than about compliance understanding per se.

### 3.3 Synthesis

The hypothesis holds in its **narrowest formulation** — legends
support compliance-recognition reasoning, as evidenced on GE-NLI
entailment items and the GE-WSC parity diagnostic — but does **not**
generalise to the broader benchmark in the way §6.5 and §6.8 jointly
predicted. The cleanest finding from running all five tasks together
is in fact a **qualitative complementarity** between the two
fine-tuning regimes that no single task captures alone:

| Reasoning competence                          | Best model         |
|-----------------------------------------------|--------------------|
| Recognising compliance (entailment)           | `tuned-legends`    |
| Detecting violations (contradiction)          | `tuned-regulation` |
| Classifying into the regulation's ontology    | `tuned-regulation` |
| Endorsement/stance detection                  | `tuned-regulation` |
| Gender-parity invariance                      | `tuned-legends`    |
| Long-form factoid extraction                  | `tuned-legends`    |
| Short-span factoid extraction                 | `tuned-regulation` |

These are not equally weighted in the headline GenderEqGLUE Score, so
the score itself ranks `tuned-regulation` first; but the per-task
breakdown shows that the two fine-tuning corpora train two genuinely
different competences, and a real-world deployment that cared
specifically about compliance recognition or fairness invariance
would have a defensible reason to prefer `tuned-legends` despite its
lower aggregate score.

## 4. Cross-task pillar effects

The five EU gender-equality pillars are exercised non-uniformly
across the tasks. The §7.4 imbalance — `violence_stereotypes` and
`leadership_participation` over-represented, `equal_economy`,
`mainstreaming_intersectionality` and `funding_global_action`
under-represented — is inherited by every CEB-derived task (GE-CLS,
GE-NLI, GE-QA), while the two external-source tasks (GE-WSC,
GE-STANCE) are pillar-agnostic. This shapes the per-pillar reading.

| Pillar                              | GE-CLS gain (reg − base) | GE-NLI gain (legends − base) | GE-QA gain (reg − base) |
|-------------------------------------|-------------------------:|-----------------------------:|------------------------:|
| `violence_stereotypes`              |                   +0.045 |                       +0.028 |                  +0.023 |
| `equal_economy`                     |                   +0.167 |                       +0.111 |                  +0.029 |
| `leadership_participation`          |                   +0.000 |                       +0.000 |                  +0.049 |
| `mainstreaming_intersectionality`   |                   +0.389 |                       +0.000 |                  +0.025 |
| `funding_global_action`             |                   +0.000 |                       +0.048 |                  +0.063 |

Two patterns are worth highlighting:

- **The minority pillars are where fine-tuning helps the most.**
  `mainstreaming_intersectionality` and `equal_economy`, both with
  pool sizes far below the §6.3.2 target of 30, see the largest
  per-task gains — most strikingly +39 macro-F1 points on GE-CLS
  for `tuned-regulation`. This is consistent with the idea that the
  fine-tuning corpora expose the model to the operational vocabulary
  of pillars that the base model has limited prior exposure to. The
  caveat from §7.3 applies: with n ≤ 18 in these buckets, the gains
  carry wide effective confidence intervals.

- **`violence_stereotypes` is where `tuned-legends` shows its only
  per-pillar advantage.** On GE-QA factoid F1, `tuned-legends`
  reaches 0.879 against 0.849 for `tuned-regulation`. As the GE-QA
  audit notes, this pillar is dominated by Italian-language Istanbul
  Convention passages that sit outside the EU Strategy's English
  register; the legends, generated by three different LLMs in §3,
  expose the model to a wider lexical surface that transfers
  marginally better to non-English regulatory prose.

The pillar `funding_global_action` shows a recurring cross-task gain
for `tuned-regulation` on GE-QA but is muted on GE-CLS — the GAP III
passages this pillar draws from are factually dense (percentages,
dates, programme names) and reward the format discipline that
regulation training induces.

## 5. Limitations carried over from per-task reports

A consolidated summary of the limitations flagged in the individual
reports, grouped by the source they propagate from:

1. **Test-set sizes are too small for tight statistical conclusions.**
   GE-CLS (n = 72), GE-NLI (n = 168), GE-QA factoid (n = 123),
   GE-WSC (n = 100), GE-STANCE (n = 120). The §7.1 decision not to
   pursue formal Cohen's κ on the CEB pool, combined with these
   test sizes, means that all per-task macro-F1 values carry an
   unmeasured noise component (§7.3). The McNemar-significant
   GE-STANCE result is robust to this — it survives a paired test
   on the actual per-item correctness pattern — but most other
   gaps are not.

2. **The Sargsyan-Damiani hypothesis is tested on a single
   backbone.** The fine-tuning is run on one open-pretrained LLM
   (per point (6)–(7) of the challenge); whether the legends
   advantage on GE-NLI scales to other backbones, or whether it
   becomes more or less significant with a larger fine-tuning
   corpus, are open questions outside the scope of this benchmark.

3. **The base model is already very capable on some tasks.** On
   GE-WSC the base model scores 93% accuracy, leaving very little
   headroom for either fine-tuning intervention to produce a
   detectable gain. The flat headline ranking on this task should
   be read as a near-ceiling result, not as evidence against
   either fine-tuning corpus. A harder coreference benchmark (e.g.
   GAP, BUG) would be needed to separate the three models cleanly.

4. **GE-Diag was not run.** The minimal-pair gender-swap diagnostic
   described in §6.9 is not part of this aggregate. Should it be
   produced in a follow-up, the §6.10 protocol allows it to be
   reported alongside, but not folded into, the GenderEqGLUE Score.

5. **Pillar imbalance amplifies small-sample volatility.** The five
   substantive pillars range from 11 to 72 passages in the CEB
   pool, and the smallest two (`equal_economy`, `mainstreaming_intersectionality`)
   are where the largest per-pillar swings are reported — including
   the GE-CLS +39 macro-F1 gain on `mainstreaming_intersectionality`,
   which rests on n = 4 test items.

## 6. Conclusions

1. **`tuned-regulation` wins the aggregate GenderEqGLUE Score** at
   0.922, ahead of `base` (0.885) and `tuned-legends` (0.881). The
   gap is concentrated on GE-CLS and GE-STANCE — the two tasks where
   the regulation's own ontology and value-stance are directly probed.

2. **`tuned-legends` does not improve over the base on the
   aggregate**, but does win directionally on GE-NLI (the central
   compliance-recognition task) and ties on GE-WSC. Its single
   statistically significant pairwise gap goes the *wrong* way
   (loss to `tuned-regulation` on GE-STANCE, p = 0.004).

3. **The Sargsyan & Damiani (2025) hypothesis is supported in its
   narrowest reading and not in its broader formulation.** Legends
   help with compliance recognition (GE-NLI entailment) and with
   gender-parity invariance (GE-WSC parity score), but do not
   generalise to value-stance classification or to recognition of
   the regulation's own thematic structure. The two fine-tuning
   regimes appear to teach **complementary** competences — legends
   handle compliance and fairness, regulation text handles ontology
   recognition and violation detection — rather than one strictly
   dominating the other.

4. **The most actionable scientific finding** from running all five
   tasks together is the **qualitative complementarity** revealed by
   the GE-NLI construction-method breakdown (entailment vs
   contradiction) and the GE-STANCE per-source breakdown
   (`curated` vs `civics_filtered`). These per-slice findings are
   not visible in the headline GenderEqGLUE Score and would not have
   been produced by either task in isolation. They are arguably
   stronger evidence for the underlying research question than the
   aggregate ranking.

5. **A larger and more carefully balanced GenderEqGLUE v2** —
   targeting at least 500 items per task, paired item-level
   annotation by two human raters, and a more challenging coreference
   benchmark in place of WinoBias — would be needed to convert the
   directional findings of this run into formally significant ones.

## 7. Artifacts

| Task       | Per-task report                              | Per-task data dump                  |
|------------|----------------------------------------------|-------------------------------------|
| GE-CLS     | `task1_ge_cls_final_report.md`               | `ge_cls_metrics.json`, `ge_cls_predictions.json` |
| GE-NLI     | `task2_ge_nli_final_report.md`               | `ge_nli_metrics.json`               |
| GE-QA      | `task3_ge_qa_audit_report.md`                | `ge_qa_results.json`                |
| GE-WSC     | `task4_ge_wsc_final_report.md`               | `wsc_results.json`                  |
| GE-STANCE  | `task5_ge_stance_final_report.md`            | `stance_results.json`               |
| **All**    | `genderEqGLUE_final_report.md` (this file)   | `aggregate.json`                    |

The `aggregate.json` artefact contains the headline metric per task
per model, the GenderEqGLUE Score, the numerical winner per task, the
wins-per-model count, and the cross-task significance summary, in a
form suitable for the visualisation step of point (12) of the
challenge.
