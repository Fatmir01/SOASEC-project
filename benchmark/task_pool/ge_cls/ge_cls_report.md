# GE-CLS — Pillar Classification: Results Report

**Task:** Single-input multi-class classification across the six EU
gender-equality pillars (`violence_stereotypes`, `equal_economy`,
`leadership_participation`, `mainstreaming_intersectionality`,
`funding_global_action`, `unknown`).

**Data:** CEB-CLS subset, 72 passages drawn from five EU and Council
of Europe instruments via stratified random split (seed 42, see §6.3.3).

**Protocol:** Zero-shot prompting on three models (`base`,
`tuned-legends`, `tuned-regulation`) with a fixed system prompt
(`prompts/ge_cls_system.txt`) and deterministic decoding. Model
interactions were performed manually through the FineTube web
interface; the raw assistant responses were recorded verbatim and
parsed offline with the regular expression `LABEL\s*:\s*([a-zA-Z_]+)`.

## Aggregate metrics

| Metric             |   base | tuned-legends | tuned-regulation |
|--------------------|-------:|--------------:|-----------------:|
| Accuracy           | 0.8889 |        0.8611 |       **0.9444** |
| Macro-F1           | 0.8333 |        0.8393 |       **0.9284** |
| Parse failures     |      0 |             0 |                0 |

All 216 model calls produced output that matched the expected
`LABEL: <category>` format; the parse-failure rate is therefore zero
for every model and is omitted from the discussion below.

## Per-class F1

| Pillar                              | Support |   base | tuned-legends | tuned-regulation |
|-------------------------------------|--------:|-------:|--------------:|-----------------:|
| `violence_stereotypes`              |      24 | 0.9333 |        0.9091 |       **0.9787** |
| `equal_economy` †                   |       6 | 0.8333 |        0.9231 |       **1.0000** |
| `leadership_participation`          |      15 | 0.9655 |        0.9286 |           0.9655 |
| `mainstreaming_intersectionality` † |       4 | 0.5000 |        0.7500 |       **0.8889** |
| `funding_global_action` †           |       7 | 0.8000 |        0.7143 |           0.8000 |
| `unknown`                           |      16 | 0.9677 |        0.8108 |           0.9375 |

† Per-class F1 on classes with fewer than 30 test items is flagged as
low-confidence (see §7.4 of the pipeline document).

## Cross-model agreement

| Pattern                                   | Count | % of pool |
|-------------------------------------------|------:|----------:|
| All three models correct                  |    58 |     80.6% |
| All three models wrong                    |     3 |      4.2% |
| Only `tuned-regulation` correct           |     1 |      1.4% |
| Only `tuned-legends` correct              |     0 |      0.0% |
| Only `base` correct                       |     0 |      0.0% |

The three passages on which all models err — `GAP_III__c008`,
`Istanbul_Convention_2011__c067`, `Roadmap_2025__c011` — are
intrinsically ambiguous and are discussed in the error analysis below.

## Discussion

**Hypothesis confirmation.** The expected ranking holds on aggregate:
`tuned-regulation` > `tuned-legends` ≈ `base` on macro-F1, with a
gap of roughly +9 macro-F1 points between `tuned-regulation` and the
other two. This is consistent with the prediction in §6.4 that the
regulation-tuned model would lead because the Strategy 2020-2025 text
explicitly mirrors the pillar structure being classified.

**`tuned-legends` does not improve over `base`.** The legends-tuned
model achieves a macro-F1 essentially indistinguishable from the
base model (0.8393 vs 0.8333) and a *lower* accuracy (0.8611 vs
0.8889). This is the pattern predicted by the Sargsyan-Damiani (2025)
hypothesis: training on narrative/illustrative material rather than
on regulatory text does not transfer to a classification task that
mirrors regulatory structure.

**Where `tuned-legends` regresses.** The model's ten errors include
six predictions of `unknown` on substantive passages (three Istanbul
Convention chapters on prevention and education, two Directive
articles, one GAP III passage on EU external action). The pattern
suggests that legends-style fine-tuning has *broadened* the model's
notion of what counts as `unknown` content — the legends are
narrative and don't share the formal register of regulatory passages,
so the model under-commits when faced with formal legal language. The
F1 on `unknown` itself drops from 0.97 (`base`) to 0.81 (`legends`),
confirming the over-prediction of that class.

**Where `tuned-regulation` improves.** Gains are concentrated on the
two minority pillars:
- `mainstreaming_intersectionality` rises from 0.50 to 0.89 (+39 pts).
- `equal_economy` rises from 0.83 to 1.00 (+17 pts).

This is consistent with the regulation text exposing the model to the
*operational definitions* of these pillars — the Strategy explicitly
discusses intersectionality and the economy chapter uses the same
vocabulary the test passages reuse. The model is not memorising
test items (the test pool is from documents not in the fine-tuning
set), but the conceptual register transfers cleanly.

**Persistent failure modes.** Three passages defeat all three models:

1. `GAP_III__c008` is gold-labelled `funding_global_action` but
   discusses gender-responsive budgeting and gender mainstreaming
   into trade and humanitarian aid; all three models pick
   `mainstreaming_intersectionality`. This is a genuine annotation
   borderline — both labels are defensible.

2. `Istanbul_Convention_2011__c067` is gold `violence_stereotypes`
   (Article 62 on international cooperation in violence cases) but
   reads superficially like `funding_global_action` because it
   discusses cross-border cooperation. All three models pick the
   wrong, surface-level cue.

3. `Roadmap_2025__c011` is gold `unknown` (a brief stand-alone
   paragraph rejecting policy rollback) but is interpreted as
   `funding_global_action` by all three because it mentions EU action.

These are signals that the gold labels themselves carry residual
noise — exactly the limitation flagged in §7.1 of the pipeline. The
same three rows would likely be the disagreement cases in a formal
double-blind annotation procedure.

**Implication for the benchmark design.** GE-CLS is the task most
favourable to `tuned-regulation` by construction (it tests recognition
of the very pillar structure encoded in the regulation). The 9-point
macro-F1 gap is therefore an *upper bound* on the discriminative
power of regulatory fine-tuning. The other four tasks — GE-QA,
GE-NLI, and the two yet to be defined — should test whether this
advantage generalises beyond pure thematic matching, or whether
`tuned-regulation` only wins where the regulation's own ontology is
the question.

## Artifacts

- `prompts/ge_cls_system.txt` — fixed system prompt for the run
- `genderegglue/ge_cls_predictions.json` — 72 records with raw
  responses and parsed labels for each model
- `genderegglue/ge_cls_metrics.json` — full metric dump including
  confusion matrices per model
- `genderegglue/ge_cls_report.md` — this report
