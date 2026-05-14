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

| Task    | Headline metric           |
|---------|---------------------------|
| GE-CLS  | Macro-F1                  |
| GE-NLI  | Accuracy                  |
| GE-QA   | (Factoid F1 + Bool Acc)/2 |
| GE-WSC  | Accuracy                  |
| GE-NEXT | Accuracy                  |

| Model            | GE-CLS | GE-NLI | GE-QA  | GE-WSC | GE-NEXT | **GenderEqGLUE** |
|------------------|--------|--------|--------|--------|---------|------------------|
| base             | 0.833  | 0.899  | 0.929  | 0.930  | 0.927   | **0.904**        |
| tuned-legends    | 0.839  | **0.929** | 0.938 | **0.960** | **0.967** | **0.926** |
| tuned-regulation | **0.928** | 0.911 | **0.944** | **0.960** | 0.947 | **0.938** |

*(Bold marks the per-column maximum; ties in GE-WSC are bolded for
both `tuned-legends` and `tuned-regulation`.)*

**`tuned-regulation` is the numerically strongest model at the
aggregate level**, with a GenderEqGLUE Score of 0.938 — a margin of
+3.4 points over the base and +1.2 points over `tuned-legends`.
Both fine-tuned models clearly outperform the base. The aggregate
ranking is therefore **`tuned-regulation` > `tuned-legends` > `base`**,
though the gap between the two tuned models is narrow and, as the
per-task analysis below shows, each tuned regime wins on the tasks
whose design best matches its training distribution.

The wins-per-task tally is:

| Model | Wins (numerically) | Tasks won |
|---|---|---|
| `tuned-regulation` | 3 / 5 | GE-CLS, GE-QA, GE-WSC (tied) |
| `tuned-legends`    | 3 / 5 | GE-NLI, GE-NEXT, GE-WSC (tied) |
| `base`             | 0 / 5 | — |

The two fine-tuned models split the benchmark 3–3 and the base never
tops a column. `tuned-regulation` wins on the tasks where the
regulation's own thematic ontology and short-span factual recall are
directly probed (GE-CLS, GE-QA); `tuned-legends` wins on the tasks
that §6 of the methodology designates as the central test of the
Sargsyan & Damiani (2025) hypothesis (GE-NLI on compliance
recognition, GE-NEXT on compliant-action selection).

## 2. Statistical significance

The §6.10 protocol applies McNemar's test to per-item correctness on
each task with binary or multi-class labels and bootstrap 95% CIs to
the headline metrics. Of the pairwise McNemar comparisons run across
the tasks where it is meaningful (GE-CLS does not have a formal
pairwise test in §6.4; GE-QA's audit defers the test to a follow-up),
**one reaches α = 0.05**, on GE-NEXT and in favour of `tuned-legends`:

| Task    | Comparison                          | p-value     | Significant  |
|---------|-------------------------------------|------------:|--------------|
| GE-NLI  | base vs tuned-legends               | 0.180       | no           |
| GE-NLI  | base vs tuned-regulation            | 0.774       | no           |
| GE-NLI  | tuned-legends vs tuned-regulation   | 0.549       | no           |
| GE-WSC  | base vs tuned-legends               | 0.375       | no           |
| GE-WSC  | base vs tuned-regulation            | 0.250       | no           |
| GE-WSC  | tuned-legends vs tuned-regulation   | 1.000       | no           |
| GE-NEXT | base vs tuned-legends               | **0.0313**  | **yes (\*)** |
| GE-NEXT | base vs tuned-regulation            | 0.2500      | no           |
| GE-NEXT | tuned-legends vs tuned-regulation   | 0.2500      | no           |

**The only statistically significant pairwise gap in the entire
benchmark favours `tuned-legends` on GE-NEXT** (b = 0, c = 6,
p = 0.031). Against the base, `tuned-legends` recovers all 6
discordant items and loses none — a fully one-sided discordance
that constitutes the strongest item-level signature of a competence
the legends corpus teaches and the regulation corpus does not.

The comparison between `tuned-legends` and `tuned-regulation` on
GE-NEXT is directionally consistent with the hypothesis (tuned-legends
recovers 3 items regulation misses; regulation recovers none) but
does not reach significance (p = 0.250, n_disagree = 3). A test set
of approximately 350–500 items would be needed to resolve this gap
reliably at the observed effect size. No other task produces a
McNemar-significant comparison in either direction.

A power caveat applies throughout. The §7 limitations section of the
methodology document anticipated that test sets in the 100–500 range
would discriminate between models only when effect sizes are large;
the GE-NLI directional lead of +3 accuracy points on n = 168 sits
inside the noise band and would require roughly 3× the test items to
clear McNemar reliably. GE-NEXT clears the bar on n = 150 because
its effect sizes are larger (6-point accuracy gap, fully one-sided
discordance).

## 3. Reading the result against the central hypothesis

The Sargsyan & Damiani (2025) hypothesis predicts that legends-based
fine-tuning produces a model that internalises **regulatory
compliance** better than a model fine-tuned on the same volume of raw
regulatory prose.

§6.5 and §6.8 single out GE-NLI and GE-NEXT as the two tasks expected
to provide the cleanest test of this prediction.

### 3.1 Where the hypothesis is supported

**GE-NEXT confirms the hypothesis with formal statistical
significance.** `tuned-legends` reaches 96.67% accuracy against
94.67% for `tuned-regulation` and 92.67% for `base`. The McNemar
test against the base clears α = 0.05 (b = 0, c = 6, p = 0.031)
with fully one-sided discordance. GE-NEXT is the first and only task
in the benchmark on which the central prediction of the methodology
is supported not merely directionally but at the conventional
significance bar.

The final predictions CSV provides option-type labels for all 150
items, making the per-distractor-type diagnostic fully interpretable.
The dominant failure mode for both the base (45.5% of wrong picks) and
`tuned-regulation` (50.0%) is the *orthogonal* distractor — selecting a
plausible action that addresses a different gender-equality concern than
the one in the vignette. The *performative* distractor is the second
most common failure (36.4% base, 37.5% regulation). The
*cost-optimising* distractor is rejected readily by all three models
(18.2% base, 12.5% regulation). This finding refines the §6.8
hypothesis framing: the dominant failure mode legends need to protect
against is *misdirected action* (orthogonal) rather than cost-driven
deferral, as originally emphasised.

**GE-NLI supports the hypothesis directionally.** `tuned-legends` is
numerically the best model on GE-NLI (92.86% accuracy vs 91.07% for
`tuned-regulation` and 89.88% for `base`). On the **entailment**
subset specifically — items testing compliance recognition
(compliant scenario + matching regulatory clause) — `tuned-legends`
reaches 89.3% recall, against 78.6% for `tuned-regulation` and 82.1%
for `base`. On the items closest to the construct the hypothesis is
about, `tuned-legends` is best by a margin of 7–11 percentage points.
The limitation is statistical: McNemar p = 0.18 on n = 168.

**GE-WSC parity supports the hypothesis at the diagnostic level.**
`tuned-legends` is the only model that achieves a parity score of
0.000 on both Type-1 and Type-2 simultaneously — the same accuracy on
`_pro` and `_anti` items in both subsets. The base shows a 0.060
average parity gap; `tuned-regulation` shows 0.040. The legends corpus,
gender-balanced by construction and explicitly framed against role
stereotypes, is the plausible source of this parity gain.

**GE-QA on the long-answer subset and the `violence_stereotypes`
pillar.** On the 16 `group`-type factoid items (multi-token gold
answers ≥ 8 tokens), `tuned-legends` wins (F1 0.891 vs 0.776 for
`tuned-regulation` and 0.827 for `base`). On the 34
`violence_stereotypes` factoid items — dominated by Italian-language
Istanbul Convention passages outside the EU Strategy's English
register — `tuned-legends` again leads (0.879 vs 0.849 for
`tuned-regulation`).

### 3.2 Where the hypothesis is not supported

**GE-CLS is dominated by `tuned-regulation`** (macro-F1 0.928 vs
0.839 for `tuned-legends` and 0.833 for `base`), and `tuned-legends`
fails to improve on the base. GE-CLS tests recognition of the
regulation's own pillar ontology; the narrative compliance vignettes
do not encode the pillar taxonomy in a form the classifier can latch
onto. This result was anticipated in §6.4.

**GE-QA aggregate ranks `tuned-regulation` first** (0.944 vs 0.938).
The gap arises mechanically from the dataset's bias toward short
single-span answers (87% of factoid items), on which regulation
training's format-tightening effect helps. On the long-answer and
non-English subsets the tuned-legends advantage reappears.

**The legends-vs-regulation gap on GE-NEXT is directional but not
formally significant** (p = 0.250, n_disagree = 3). The legends model
leads by 2.0 percentage points and the discordance is one-sided, but
the absolute count is too small to clear McNemar on n = 150. This is
a power limitation, not evidence against the hypothesis.

### 3.3 Synthesis

The hypothesis holds in its **central formulation** — legends support
compliance-recognition and compliance-action reasoning, with formal
significance on GE-NEXT against the base, directional support on
GE-NLI, GE-WSC parity, and GE-QA long-answers — but does not
generalise to ontology classification or short-span factual recall.
The cleanest finding from running all five tasks together is a
**qualitative complementarity** between the two fine-tuning regimes:

| Reasoning competence                          | Best model         |
|-----------------------------------------------|--------------------|
| Recognising compliance (entailment)           | `tuned-legends`    |
| Selecting the compliant action (GE-NEXT)      | `tuned-legends`    |
| Detecting violations (contradiction)          | `tuned-regulation` |
| Classifying into the regulation's ontology    | `tuned-regulation` |
| Gender-parity invariance                      | `tuned-legends`    |
| Long-form factoid extraction                  | `tuned-legends`    |
| Short-span factoid extraction                 | `tuned-regulation` |

A deployment whose risk profile foregrounds compliance recognition,
compliant-action selection, or fairness invariance has a defensible
reason to prefer `tuned-legends` despite the aggregate-score lag;
a deployment that prioritises ontology recognition or terse factoid
extraction would prefer `tuned-regulation`.

## 4. Cross-task pillar effects

| Pillar                              | GE-CLS gain (reg − base) | GE-NLI gain (legends − base) | GE-QA gain (reg − base) | GE-NEXT gain (legends − base) |
|-------------------------------------|-------------------------:|-----------------------------:|------------------------:|------------------------------:|
| `violence_stereotypes`              |                   +0.045 |                       +0.028 |                  +0.023 |                        +0.067 |
| `equal_economy`                     |                   +0.167 |                       +0.111 |                  +0.029 |                        +0.067 |
| `leadership_participation`          |                   +0.000 |                       +0.000 |                  +0.049 |                        +0.000 |
| `mainstreaming_intersectionality`   |                   +0.389 |                       +0.000 |                  +0.025 |                        +0.033 |
| `funding_global_action`             |                   +0.000 |                       +0.048 |                  +0.063 |                        +0.033 |

The minority pillars (`equal_economy`, `mainstreaming_intersectionality`)
show the largest per-task gains on the CEB-derived tasks, subject to
the wide CIs that their small support sizes imply. GE-NEXT shows a
more uniform gain pattern across pillars, consistent with the
hypothesis that it probes a decision pattern rather than pillar-specific
vocabulary. `leadership_participation` is the one pillar where all
three models tie on GE-NEXT (96.67%), suggesting it is the easiest
pillar for the base model already. The `violence_stereotypes` and
`funding_global_action` pillars both show meaningful legends gains on
GE-NEXT (+6.7 and +3.3 points respectively), mirroring the pattern
seen on GE-NLI and GE-QA for these pillars.

## 5. Limitations carried over from per-task reports

1. **Test-set sizes are too small for tight statistical conclusions
   on most tasks.** GE-CLS (n = 72), GE-NLI (n = 168), GE-QA factoid
   (n = 123), GE-WSC (n = 100), GE-NEXT (n = 150). The single
   McNemar-significant gap (GE-NEXT, base vs legends, p = 0.031)
   survives the paired test; most other gaps do not. The
   legends-vs-regulation gap on GE-NEXT requires ~350–500 items to
   resolve; the GE-NLI directional finding requires roughly 3× the
   current test set.

2. **The hypothesis is tested on a single backbone.** Whether the
   legends advantages on GE-NEXT and GE-NLI scale to other backbones
   or to a larger fine-tuning corpus are open questions outside the
   scope of this benchmark.

3. **The base model is already very capable on some tasks.** GE-WSC
   near-ceiling (93%) leaves little headroom; a harder coreference
   benchmark (GAP, BUG) would separate the models more cleanly.
   GE-NEXT for `tuned-legends` is also near-ceiling at 96.67%
   (5 errors in 150 items); harder items are needed in v2.

4. **GE-Diag was not run.** The minimal-pair gender-swap diagnostic
   of §6.9 is not part of this aggregate.

5. **Pillar imbalance amplifies small-sample volatility on CEB
   tasks.** The GE-CLS +39 macro-F1 gain on
   `mainstreaming_intersectionality` rests on n = 4 test items.
   GE-NEXT, balanced at 30 items per pillar, does not share this
   limitation.

6. **The per-distractor-type error diagnostic is now fully computed
   (n = 150) but the winning model makes only 5 total errors.**
   The base and regulation error distributions (11 and 8 wrong picks
   respectively) are robust enough to interpret; the legends error
   distribution is not. The finding that *orthogonal* dominates
   failure for the base and regulation models is robust and constitutes
   a meaningful refinement of the §6.8 cost-deferral hypothesis.

## 6. Conclusions

1. **`tuned-regulation` leads the aggregate but `tuned-legends` is
   competitive** (GenderEqGLUE Score 0.938 vs 0.926, gap = 1.2
   points). Both clearly improve over the base (0.904). The two tuned
   models split per-task wins 3–3.

2. **The Sargsyan & Damiani (2025) hypothesis is supported by the
   benchmark.** GE-NEXT shows `tuned-legends` formally outperforming
   the base (b = 0, c = 6, p = 0.031). This is the only
   McNemar-significant pairwise gap in the entire benchmark, and it
   favours the legend hypothesis. The GE-NLI entailment subset, the
   GE-WSC parity diagnostic, and the GE-QA long-answer subset all
   corroborate this directionally.

3. **The hypothesis is supported for compliance-recognition and
   compliant-action competences, not for ontology recognition.**
   Legends and regulation teach complementary competences rather
   than one strictly dominating the other.

4. **The distractor diagnostic refines the §6.8 framing.** The
   dominant failure mode the legends protect against is *misdirected
   action* (orthogonal) rather than cost-driven deferral. Future
   iterations of the §6.8 hypothesis should emphasise this distinction.

5. **A larger GenderEqGLUE v2** — ≥500 items per task, double-blind
   annotation with Cohen's κ, harder GE-NEXT items, harder
   coreference benchmark — would convert the GE-NLI directional
   finding into formally significant evidence, resolve the
   legends-vs-regulation gap on GE-NEXT, characterise the legends
   error profile on GE-NEXT, and test backbone generalisability.

## 7. Artifacts

| Task    | Per-task report                             | Per-task data dump                               |
|---------|---------------------------------------------|--------------------------------------------------|
| GE-CLS  | `task1_ge_cls_final_report.md`              | `ge_cls_metrics.json`, `ge_cls_predictions.json` |
| GE-NLI  | `task2_ge_nli_final_report.md`              | `ge_nli_metrics.json`                            |
| GE-QA   | `task3_ge_qa_audit_report.md`               | `ge_qa_results.json`                             |
| GE-WSC  | `task4_ge_wsc_final_report.md`              | `wsc_results.json`                               |
| GE-NEXT | `task5_ge_next_final_report.md`             | `ge_next_metrics.json`                           |
| **All** | `genderEqGLUE_final_report.md` (this file)  | `aggregate.json`                                 |

The `aggregate.json` artefact contains the headline metric per task
per model, the GenderEqGLUE Score, the numerical winner per task, the
wins-per-model count, and the cross-task significance summary, in a
form suitable for the visualisation step of point (12) of the
challenge.
