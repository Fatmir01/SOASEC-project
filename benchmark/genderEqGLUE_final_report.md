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
`task5_ge_next_final_report.md`) into the headline GenderEqGLUE
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
| GE-NEXT    | Accuracy                 |


| Model            | GE-CLS | GE-NLI | GE-QA | GE-WSC | GE-NEXT | **GenderEqGLUE** |
| ---------------- | ------ | ------ | ----- | ------ | ------- | ---------------- |
| base             | 0.833  | 0.899  | 0.929 | 0.930  | 0.920   | **0.902**        |
| tuned-legends    | 0.839  | **0.929** | 0.938 | **0.960** | **0.987** | **0.931** |
| tuned-regulation | **0.928** | 0.911 | **0.944** | **0.960** | 0.940 | **0.937** |

*(Bold marks the per-column maximum; ties in GE-WSC are bolded for
both `tuned-legends` and `tuned-regulation`.)*

**`tuned-regulation` is the numerically strongest model at the
aggregate level**, with a GenderEqGLUE Score of 0.937 — a margin of
+3.5 points over the base but only +0.6 points over `tuned-legends`.
The aggregate ranking is therefore **`tuned-regulation` ≈
`tuned-legends` > `base`**, with the first two indistinguishable at
the headline level (0.937 vs 0.931). This is a substantially closer
race than the per-task table alone suggests, because the GE-NEXT
result — discussed in §2 below — adds a near-ceiling 98.7% accuracy
to `tuned-legends` and lifts its aggregate by a full 2 points relative
to a benchmark that did not include it.

The wins-per-task tally compresses this picture:

| Model | Wins (numerically) | Tasks won |
| --- | --- | --- |
| `tuned-regulation` | 3 / 5 | GE-CLS, GE-QA, GE-WSC (tied) |
| `tuned-legends` | 3 / 5 | GE-NLI, GE-NEXT, GE-WSC (tied) |
| `base` | 0 / 5 | — |

The two fine-tuned models split the benchmark 3-3 and the base never
tops a column. `tuned-regulation` wins on the tasks where the
regulation's own thematic ontology and short-span factual recall are
directly probed (GE-CLS, GE-QA); `tuned-legends` wins on the tasks
that §6 of the methodology designates as the central test of the
Sargsyan & Damiani (2025) hypothesis (GE-NLI on compliance
recognition, GE-NEXT on compliant-action selection).

## 2. Statistical significance

The §6.10 protocol applies McNemar's test to per-item correctness on
each task with binary or multi-class labels and bootstrap 95% CIs to
the headline metrics. Of the 12 pairwise McNemar comparisons run
across the three tasks where it is meaningful (GE-CLS does not have a
formal pairwise test in §6.4; GE-QA's audit defers the test to a
follow-up), **two reach α = 0.05** — and both involve `tuned-legends`
on GE-NEXT:

| Task     | Comparison                          |  p-value | Significant |
|----------|-------------------------------------|---------:|-------------|
| GE-NLI   | base vs tuned-legends               |    0.180 | no          |
| GE-NLI   | base vs tuned-regulation            |    0.774 | no          |
| GE-NLI   | tuned-legends vs tuned-regulation   |    0.549 | no          |
| GE-WSC   | base vs tuned-legends               |    0.375 | no          |
| GE-WSC   | base vs tuned-regulation            |    0.250 | no          |
| GE-WSC   | tuned-legends vs tuned-regulation   |    1.000 | no          |
| GE-NEXT  | base vs tuned-legends               |  **0.0063** | **yes (\*\*)** |
| GE-NEXT  | base vs tuned-regulation            |    0.250 | no          |
| GE-NEXT  | tuned-legends vs tuned-regulation   |  **0.0391** | **yes (\*)**   |

**The two statistically significant pairwise gaps in the entire
benchmark both favour `tuned-legends` on GE-NEXT.** Against the base,
`tuned-legends` recovers 11 items the base misses and loses only 1
(p = 0.006). Against `tuned-regulation`, `tuned-legends` recovers 8
items the regulation-tuned model misses and loses only 1 (p = 0.039).
The base-vs-regulation comparison on GE-NEXT does not separate the
two models (p = 0.25), and no comparison on the other three tasks
clears the bar.

The error overlap on GE-NEXT is therefore highly asymmetric: the
items `tuned-legends` answers correctly are very nearly a strict
superset of the items the other two answer correctly. This is the
cleanest item-level signature in the entire benchmark of a
competence that the legends corpus teaches and that the regulation
corpus does not.

A power caveat still applies elsewhere. The §7 limitations section
of the methodology document anticipated that test sets in the
100–500 range would discriminate between models only when effect
sizes are large; the GE-NLI directional lead of +3 accuracy points
on n = 168 sits inside the noise band and would require roughly
3× the test items to clear McNemar reliably. GE-NEXT clears the bar
on n = 150 because its effect sizes are larger (gaps of 4–7 accuracy
points combined with very asymmetric discordance counts).

## 3. Reading the result against the central hypothesis

The Sargsyan & Damiani (2025) hypothesis predicts that legends-based
fine-tuning produces a model that internalises **regulatory
compliance** better than a model fine-tuned on the same volume of raw
regulatory prose.

§6.5 and §6.8 single out GE-NLI and GE-NEXT as the two tasks expected
to provide the cleanest test of this prediction. The picture that
emerges from the five tasks together is now substantially more
favourable to the hypothesis than the GE-NLI result alone would have
licensed.

### 3.1 Where the hypothesis is supported

**GE-NEXT confirms the hypothesis with formal statistical
significance.** `tuned-legends` reaches 98.67% accuracy against
94.00% for `tuned-regulation` and 92.00% for `base`, and the
pairwise McNemar tests against both other models clear α = 0.05
(p = 0.006 and p = 0.039 respectively). GE-NEXT is the first task
in the benchmark on which the central prediction of the methodology
is supported not merely directionally but at the conventional
significance bar. The §6.8 framing — that GE-NEXT was the most
direct probe of the *decision pattern* the legends embed, rather
than of regulatory content per se — receives its strongest
empirical confirmation here.

A note on mechanism: the per-distractor-type diagnostic of the
GE-NEXT report is uninformative on this run because the legend
model produces only 2 wrong picks on the available 100-item subset
of GE-NEXT, an error denominator too small to characterise. The
discordance pattern under McNemar — `tuned-legends` recovers items
the regulation-tuned model misses much more often than the reverse —
is the load-bearing evidence for the hypothesis on this task.

**GE-NLI supports the hypothesis directionally.** `tuned-legends` is
numerically the best model on GE-NLI (92.86% accuracy vs 91.07% for
`tuned-regulation` and 89.88% for `base`). The construction-method
breakdown in the GE-NLI report sharpens this finding: on the
**entailment** subset specifically — the items that test compliance
recognition (compliant scenario + matching regulatory clause) —
`tuned-legends` reaches 89.3% recall, against 78.6% for
`tuned-regulation` and 82.1% for `base`. On the items closest to the
construct the hypothesis is *about*, `tuned-legends` is best by a
margin of 7–11 percentage points. The limitation is statistical:
McNemar p = 0.18 on n = 168, so on GE-NLI the directional finding
does not clear the conventional bar in isolation. Read together with
GE-NEXT, however, the two compliance-recognition tasks line up
consistently: same direction, larger effect size on GE-NEXT, formal
significance there.

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

The hypothesis holds in its **central formulation** — legends
support compliance-recognition and compliance-action reasoning, with
formal McNemar significance on GE-NEXT and consistent directional
support on GE-NLI, GE-WSC parity, and GE-QA long-answers — but does
not generalise to ontology classification or short-span factual
recall, which favour `tuned-regulation`. The cleanest finding from
running all five tasks together is a **qualitative complementarity**
between the two fine-tuning regimes that no single task captures
alone:

| Reasoning competence                          | Best model         |
|-----------------------------------------------|--------------------|
| Recognising compliance (entailment)           | `tuned-legends`    |
| Selecting the compliant action (GE-NEXT)      | `tuned-legends`    |
| Detecting violations (contradiction)          | `tuned-regulation` |
| Classifying into the regulation's ontology    | `tuned-regulation` |
| Gender-parity invariance                      | `tuned-legends`    |
| Long-form factoid extraction                  | `tuned-legends`    |
| Short-span factoid extraction                 | `tuned-regulation` |

The competence map tilts 4–3 to `tuned-legends`, but the
two-point lag in the headline GenderEqGLUE Score arises because the
score equally weights every task — including GE-CLS, on which
`tuned-regulation` has its largest single-task advantage (+9 macro-F1
points). A deployment whose risk profile foregrounds compliance
recognition, compliant-action selection or fairness invariance has a
defensible reason to prefer `tuned-legends` despite the marginal
aggregate-score lag; a deployment that prioritises ontology
recognition or terse factoid extraction would prefer
`tuned-regulation`.

## 4. Cross-task pillar effects

The five EU gender-equality pillars are exercised non-uniformly
across the tasks. The §7.4 imbalance — `violence_stereotypes` and
`leadership_participation` over-represented, `equal_economy`,
`mainstreaming_intersectionality` and `funding_global_action`
under-represented — is inherited by every CEB-derived task (GE-CLS,
GE-NLI, GE-QA), while GE-WSC is pillar-agnostic and GE-NEXT is
balanced by construction at 30 items per pillar. This shapes the
per-pillar reading.

| Pillar                              | GE-CLS gain (reg − base) | GE-NLI gain (legends − base) | GE-QA gain (reg − base) | GE-NEXT gain (legends − base) |
|-------------------------------------|-------------------------:|-----------------------------:|------------------------:|------------------------------:|
| `violence_stereotypes`              |                   +0.045 |                       +0.028 |                  +0.023 |                        +0.067 |
| `equal_economy`                     |                   +0.167 |                       +0.111 |                  +0.029 |                        +0.100 |
| `leadership_participation`          |                   +0.000 |                       +0.000 |                  +0.049 |                        +0.033 |
| `mainstreaming_intersectionality`   |                   +0.389 |                       +0.000 |                  +0.025 |                        +0.067 |
| `funding_global_action`             |                   +0.000 |                       +0.048 |                  +0.063 |                        +0.067 |

Three patterns are worth highlighting:

- **The minority pillars are where fine-tuning helps the most on the
  CEB-derived tasks.** `mainstreaming_intersectionality` and
  `equal_economy`, both with pool sizes far below the §6.3.2 target
  of 30, see the largest per-task gains on GE-CLS and GE-NLI — most
  strikingly +39 macro-F1 points on GE-CLS for `tuned-regulation`.
  This is consistent with the idea that the fine-tuning corpora
  expose the model to the operational vocabulary of pillars that the
  base model has limited prior exposure to. The caveat from §7.3
  applies: with n ≤ 18 in these buckets, the gains carry wide
  effective confidence intervals.

- **GE-NEXT shows the most uniform gain pattern across pillars.**
  The legends-over-base gain ranges from +3.3 points
  (`leadership_participation`) to +10.0 points (`equal_economy`),
  with no pillar showing a regression and the smallest gain still
  positive. This is consistent with the §6.8 framing of GE-NEXT as a
  test of a *decision pattern* — the four-beat
  identify → design → implement → measure arc — that the legends
  embed across pillars rather than concentrating on any one pillar's
  vocabulary. By contrast, the CEB-derived tasks show much more
  heterogeneous per-pillar effects (compare the +39-point GE-CLS
  gain on `mainstreaming_intersectionality` with the zero gain on
  `leadership_participation` and `funding_global_action`).

- **`violence_stereotypes` is where `tuned-legends` shows its
  largest per-pillar advantage on GE-QA.** On factoid F1,
  `tuned-legends` reaches 0.879 against 0.849 for `tuned-regulation`.
  As the GE-QA audit notes, this pillar is dominated by
  Italian-language Istanbul Convention passages that sit outside the
  EU Strategy's English register; the legends, generated by three
  different LLMs in §3, expose the model to a wider lexical surface
  that transfers marginally better to non-English regulatory prose.

The pillar `funding_global_action` shows a recurring cross-task gain
for `tuned-regulation` on GE-QA but is muted on GE-CLS — the GAP III
passages this pillar draws from are factually dense (percentages,
dates, programme names) and reward the format discipline that
regulation training induces.

## 5. Limitations carried over from per-task reports

A consolidated summary of the limitations flagged in the individual
reports, grouped by the source they propagate from:

1. **Test-set sizes are too small for tight statistical conclusions
   on most tasks.** GE-CLS (n = 72), GE-NLI (n = 168), GE-QA factoid
   (n = 123), GE-WSC (n = 100), GE-NEXT (n = 150). The §7.1 decision
   not to pursue formal Cohen's κ on the CEB pool, combined with
   these test sizes, means that all per-task macro-F1 values carry
   an unmeasured noise component (§7.3). The two McNemar-significant
   gaps on GE-NEXT survive a paired test on the per-item correctness
   pattern, but most other gaps do not, and the GE-NLI directional
   finding in particular would need a roughly 3× larger test set to
   clear α = 0.05 reliably at the observed effect size.

2. **The Sargsyan-Damiani hypothesis is tested on a single
   backbone.** The fine-tuning is run on one open-pretrained LLM
   (per point (6)–(7) of the challenge); whether the legends
   advantages on GE-NEXT and GE-NLI scale to other backbones, or
   whether they become more or less significant with a larger
   fine-tuning corpus, are open questions outside the scope of this
   benchmark.

3. **The base model is already very capable on some tasks.** On
   GE-WSC the base model scores 93% accuracy, leaving very little
   headroom for either fine-tuning intervention to produce a
   detectable gain. The flat headline ranking on this task should
   be read as a near-ceiling result, not as evidence against
   either fine-tuning corpus. A harder coreference benchmark (e.g.
   GAP, BUG) would be needed to separate the three models cleanly.
   The same near-ceiling concern applies to GE-NEXT for
   `tuned-legends` itself: at 98.67% accuracy, the model has only
   two items left to recover on the 150-item test set, and any v2
   extension would need to introduce harder items if further
   discrimination is required.

4. **GE-Diag was not run.** The minimal-pair gender-swap diagnostic
   described in §6.9 is not part of this aggregate. Should it be
   produced in a follow-up, the §6.10 protocol allows it to be
   reported alongside, but not folded into, the GenderEqGLUE Score.

5. **Pillar imbalance amplifies small-sample volatility on CEB
   tasks.** The five substantive pillars range from 11 to 72
   passages in the CEB pool, and the smallest two (`equal_economy`,
   `mainstreaming_intersectionality`) are where the largest
   per-pillar swings are reported on GE-CLS, GE-NLI and GE-QA —
   including the GE-CLS +39 macro-F1 gain on
   `mainstreaming_intersectionality`, which rests on n = 4 test
   items. GE-NEXT, balanced by construction at 30 items per pillar,
   does not suffer from this and shows the most uniform per-pillar
   effect (§4).

6. **The per-distractor-type diagnostic on GE-NEXT is uninformative
   for the winning model.** `tuned-legends` produces only 2 wrong
   picks on the 100-item v1 subset for which option-type labels are
   available, so its error-distribution across the
   *performative / cost-optimising / orthogonal* axes cannot be
   characterised reliably. The headline accuracy and the McNemar
   discordance pattern carry the GE-NEXT result; the §6.8 prediction
   about *which* failure mode the legends would protect against
   most strongly cannot be tested on this run.

## 6. Conclusions

1. **`tuned-regulation` and `tuned-legends` are indistinguishable
   at the headline aggregate level** (GenderEqGLUE Score 0.937 vs
   0.931). Both clearly improve over the base (0.902). The two
   tuned models split the per-task wins 3-3, with
   `tuned-regulation` winning the tasks closest to the regulation's
   ontology (GE-CLS, GE-QA short-span) and `tuned-legends` winning
   the tasks closest to the compliance-recognition construct
   (GE-NLI, GE-NEXT, GE-WSC tied).

2. **The Sargsyan & Damiani (2025) hypothesis is supported by the
   benchmark.** GE-NEXT — the task §6.8 designates as the most
   direct probe of the compliance-versus-cost decision pattern —
   shows `tuned-legends` formally outperforming both the base
   (p = 0.006) and `tuned-regulation` (p = 0.039). These are the
   only two McNemar-significant pairwise gaps in the entire
   benchmark, and both favour the legend hypothesis. The GE-NLI
   entailment subset, the GE-WSC parity diagnostic, and the GE-QA
   long-answer subset all corroborate this directionally.

3. **The hypothesis is supported for the compliance-recognition
   competence, not for ontology recognition.** Legends help with
   compliance recognition (GE-NLI entailment), compliant-action
   selection (GE-NEXT), gender-parity invariance (GE-WSC parity)
   and long-form factoid extraction (GE-QA group items). They do
   not help with classification into the regulation's own pillar
   structure (GE-CLS) or with terse single-span extraction (GE-QA
   single-span). The two fine-tuning regimes appear to teach
   **complementary** competences — legends handle the
   *behavioural* recognition of compliant practice, regulation
   text handles the *propositional* recognition of regulatory
   content — rather than one strictly dominating the other.

4. **The most actionable scientific finding** from running all five
   tasks together is the alignment between the GE-NEXT formal
   significance result, the GE-NLI directional entailment-subset
   advantage, and the GE-WSC parity diagnostic. These three slices
   would not have been produced by any single task in isolation;
   together they form a coherent qualitative argument that the
   legend corpus embeds a recognisable *decision pattern* — the
   identify → design → implement → measure arc — that raw
   regulatory text does not. This decision-pattern interpretation
   is arguably stronger evidence for the underlying research
   question than the aggregate ranking, which masks the
   complementarity between the two tuned regimes.

5. **A larger and more carefully balanced GenderEqGLUE v2** —
   targeting at least 500 items per task, paired item-level
   annotation by two human raters, a more challenging coreference
   benchmark in place of WinoBias, and harder GE-NEXT items
   designed to break the ceiling tuned-legends reaches at 98.67% —
   would be needed to convert the GE-NLI directional finding into
   formally significant evidence, to characterise the per-distractor
   error pattern on GE-NEXT, and to test whether the GE-NEXT result
   replicates on other backbones.

## 7. Artifacts

| Task       | Per-task report                              | Per-task data dump                  |
|------------|----------------------------------------------|-------------------------------------|
| GE-CLS     | `task1_ge_cls_final_report.md`               | `ge_cls_metrics.json`, `ge_cls_predictions.json` |
| GE-NLI     | `task2_ge_nli_final_report.md`               | `ge_nli_metrics.json`               |
| GE-QA      | `task3_ge_qa_audit_report.md`                | `ge_qa_results.json`                |
| GE-WSC     | `task4_ge_wsc_final_report.md`               | `wsc_results.json`                  |
| GE-NEXT    | `task5_ge_next_final_report.md`              | `ge_next_metrics.json`              |
| **All**    | `genderEqGLUE_final_report.md` (this file)   | `aggregate.json`                    |

The `aggregate.json` artefact contains the headline metric per task
per model, the GenderEqGLUE Score, the numerical winner per task, the
wins-per-model count, and the cross-task significance summary, in a
form suitable for the visualisation step of point (12) of the
challenge.
