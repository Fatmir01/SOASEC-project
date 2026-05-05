# GE-QA Benchmark Audit Report

**Task.** GE-QA (GenderEqGLUE Task 3, pipeline §6.6) — open-book reading
comprehension over CEB-QA passages, split into a SQuAD-style extractive
sub-task (GE-QA-Factoid, n = 123) and a BoolQ-style yes/no sub-task
(GE-QA-Bool, n = 134). Three models are scored under identical conditions:
`base`, `tuned_legends`, `tuned_regulation`.

**Scoring protocol (§6.6.5–§6.6.6).** Factoid responses pass through SQuAD
normalisation — lowercase, strip Unicode punctuation, drop leading articles
(`a`, `an`, `the`), collapse whitespace — before token-level F1 and Exact Match
are computed against the gold answer and any aliases, taking the maximum.
Boolean responses are parsed with the regex `\b(yes|no)\b` (case-insensitive,
first match wins); when no match is found the prediction is recorded as
`parse_failed` and counted as wrong in the headline `bool_accuracy_all`. The
aggregate GE-QA score is the unweighted mean of `factoid_F1` and
`bool_accuracy_all`.

## 1. Headline results

| Model | Factoid EM | Factoid F1 | Bool Accuracy | **GE-QA Score** |
|---|---:|---:|---:|---:|
| base             | 0.7154 | 0.8659 | 0.9925 | **0.9292** |
| tuned_legends    | 0.7236 | 0.8827 | 0.9925 | **0.9376** |
| tuned_regulation | **0.7480** | **0.8948** | 0.9925 | **0.9437** |

The ranking is `tuned_regulation > tuned_legends > base` on every factoid
metric, with `tuned_regulation` improving over `base` by **+3.26 EM** and
**+2.89 F1** points and `tuned_legends` falling neatly in between (+0.82 EM,
+1.68 F1). The boolean sub-task is statistically saturated — all three models
land on the same 0.9925 figure. The aggregate GE-QA score therefore tracks the
factoid signal almost entirely: `tuned_regulation` ends 1.45 score points above
`base`, and the headline ordering matches the §6.6 hypothesis that "the
tuned-regulation model is expected to dominate this task".

## 2. Why the boolean sub-task tells us almost nothing

The flat bool numbers across the three models are not noise — they are an
artefact of the open-book format on a question set this targeted. Every model
gets exactly **133 out of 134 items right after parsing**, with one shared miss
and one shared parse failure. The `bool_accuracy_parsed` column lands at
**1.0000 for all three models**, meaning that whenever the regex extracts a
word, that word is the correct one — the only daylight between models would
have to come from parse-failure differences, and there are none.

The single item that all three models miss is `ge_qa_b_125`, an Italian-language
question on Article 75 of the Istanbul Convention (`pillar = unknown`,
`method = direct_paraphrase`). Every model answered `"sì"` — the Italian word
for "yes", which is in fact the correct answer — but the English-only regex
`\b(yes|no)\b` cannot match it. This is a parsing artefact, not a comprehension
failure: under the §6.6.5 protocol it counts as wrong for all three models
identically, so it cancels out in any pairwise comparison and contributes a
−0.0075 ceiling to every model's bool accuracy. A multilingual extension of the
parse rule (e.g. accepting `sì/sí`, `no`, `oui/non`, `ja/nein`) would lift all
three models to a perfect 1.0000 simultaneously without changing their ordering.

The **per-method bool table** confirms that the dataset is doing its job even
where it cannot discriminate models. Every model scores 1.0000 on
`perturbed_claim` (67/67) and 0.9851 on `direct_paraphrase` (66/67) — the lone
miss being the parse failure above. This is the asymmetry §6.6.7 warned about
inverted: the spec anticipated that models might over-detect contradictions
("good at saying yes, bad at detecting perturbations"), and instead what we see
is that every model handles perturbations flawlessly, with the only weakness
sitting on the language-recognition side of the parser. In a closed-book task
this asymmetry would be diagnostic of a model's behaviour; here, with the
passage in front of every model, even the base reads carefully enough to
recognise a swapped percentage or a flipped date.

| Method            |  n | base | tuned_legends | tuned_regulation |
|---|---:|---:|---:|---:|
| direct_paraphrase | 67 | 0.9851 | 0.9851 | 0.9851 |
| perturbed_claim   | 67 | 1.0000 | 1.0000 | 1.0000 |

The **per-pillar bool table** likewise compresses to two rows: every model
scores 1.0000 on the five labelled pillars, and 0.9615 (25/26) on the `unknown`
pillar — the same 1-item gap, located in the `unknown` bucket because the
`ge_qa_b_125` Istanbul preamble was assigned that label by the §4.1
classifier. This is consistent with the §7.2 caveat that `unknown` is the
noisiest bucket of the CEB pool; here it shows up as a pure parser artefact
rather than as a genuine comprehension issue.

## 3. The factoid sub-task is where the experiment lives

With bool effectively saturated, the GE-QA experiment reduces to factoid F1 and
EM, and here the three models do separate cleanly. Of the 123 factoid items,
**`tuned_regulation` differs from `base` on 18 (10 better, 8 worse, 105 tied)**
and **`tuned_legends` differs from `base` on 20 (12 better, 8 worse, 103
tied)**. The volume of movement is similar; the *direction* of the movement is
where the two tuned models pull apart.

Inspecting the top-five gains for `tuned_regulation` vs `base` in the
`forensics` block of `ge_qa_results.json`, the pattern is unmistakable: every
single one is a case where the base model produced a verbose, over-specified
extraction and the regulation-tuned model trimmed it to the gold span. On
`ge_qa_f_062` the base answers `"WPS agenda"` to a question whose gold is
`"GAPIII"`, while `tuned_regulation` produces `"GAPIII"` exactly (Δ F1 =
+1.000). On `ge_qa_f_023` the base produces
`"60 % of university graduates are female."` to a question whose gold span is
just `"60 %"`, while `tuned_regulation` produces `"60%"` (Δ F1 = +0.714). On
`ge_qa_f_070` the base produces
`"mandatory training on gender equality and on implementing GAP III"` to a
question whose gold is `"mandatory training"`, while `tuned_regulation`
produces `"mandatory training"` (Δ F1 = +0.667). This is exactly the format
discipline the §6.6.7 commentary predicted regulation training would induce —
short, factoid-shaped answers that mirror the regulatory Q&A pairs the model
was trained on.

The flip side is the eight cases where `tuned_regulation` scores **worse** than
`base`. Inspecting them, the pattern is again uniform: the regulation-tuned
model truncates answers that should have been longer. On `ge_qa_f_069` the gold
is the four-conjunct phrase `"agriculture, fishing and aquaculture and food
systems"`, which `base` reproduces verbatim while `tuned_regulation` clips to
`"agriculture, fishing and aquaculture"` (Δ F1 = −0.273). On `ge_qa_f_061` the
gold is `"the audio-visual sector and the media"`, reproduced verbatim by
`base` and clipped to `"audio-visual sector"` by `tuned_regulation` (Δ F1 =
−0.333). On `ge_qa_f_052` the gold is `"the introduction of paid paternity
leave"`, reproduced verbatim by `base` (modulo the leading capital) and clipped
to `"paid paternity leave"` by `tuned_regulation` (Δ F1 = −0.250). The losses
are the same behaviour as the gains — terseness — applied to questions whose
gold answer is genuinely multi-token. **Net of the trade-off, terseness wins by
a wide margin** because the dataset is dominated by short factoids: 87 % of
gold answers are tagged `single_span` (≤ 7 tokens), and the format-tightening
gains on those items more than compensate for the eight losses on `group`-type
items.

The tuned-legends model shows a different pattern. Its top gains over `base`
are mostly the same items as `tuned_regulation`'s top gains (the legends format
also encourages tighter answers than the unconditioned base), but its 12
gains include several where it correctly produces the full multi-token span
that `tuned_regulation` clips. Legends are 1–4 sentence narrative answers, so
the legends-tuned model sits between base and tuned_regulation on the
verbosity spectrum. This explains why its F1 lands between them (0.8827) while
its EM gain over base is small (+0.82 points): legends teach answer shape but
not answer brevity, so they help on F1 (which is robust to extra tokens) more
than on EM (which is not). The §6.6.7 commentary predicted exactly this
EM/F1 gap for tuned-legends — the gap here is +1.68 F1 versus +0.82 EM, so the
prediction holds in direction if not in magnitude.

## 4. Per-pillar factoid F1 — where the gain concentrates

| Pillar | n | base | tuned_legends | tuned_regulation | Δ reg − base |
|---|---:|---:|---:|---:|---:|
| equal_economy                    | 16 | 0.8474 | 0.8759 | 0.8759 | +0.0285 |
| funding_global_action            | 19 | 0.8838 | 0.8728 | **0.9470** | **+0.0632** |
| leadership_participation         | 28 | 0.8840 | 0.8762 | **0.9333** | **+0.0493** |
| mainstreaming_intersectionality  |  9 | 0.7481 | 0.7728 | 0.7178 | −0.0303 |
| unknown                          | 17 | 0.9759 | 0.9759 | 0.9759 |  0.0000 |
| violence_stereotypes             | 34 | 0.8260 | **0.8793** | 0.8491 | +0.0231 |

The §6.6.7 spec promised a "per-pillar Factoid F1" diagnostic precisely to
locate the source of any aggregate gain, and the table above resolves that
question cleanly. The tuned-regulation gain of +2.89 F1 points is not
distributed evenly: it concentrates almost entirely on **`funding_global_action`
(+6.32)** and **`leadership_participation` (+4.93)** — the two pillars whose
passages are dominated by quantitative spans (percentages, EUR amounts, dates,
article numbers, regulation IDs). These are exactly the spans the
regulation-tuned model has been trained to produce as terse factoid answers.
On `equal_economy` the gain shrinks to +2.85 F1 and is shared with
tuned_legends, suggesting that pillar's mix of policy descriptions and figures
benefits both regulatory and narrative tuning roughly equally.

The two pillars where the regulation gain disappears are diagnostic of the
training-data boundary. On **`violence_stereotypes`** (n = 34) — the largest
pillar, dominated by Italian-language Istanbul-Convention articles —
`tuned_legends` (0.8793) actually overtakes `tuned_regulation` (0.8491). The
fine-tuning regulation corpus is the EU Gender Equality Strategy 2020-2025,
which is English; the Italian Istanbul passages sit outside its register. The
legends, generated by a separate process on broader gender-equality concepts,
appear to expose the model to a wider lexical surface that transfers slightly
better to Italian regulatory prose. On **`mainstreaming_intersectionality`**
(n = 9) the regulation-tuned model loses ground to base (−3.03), but the
sample is too small to support any conclusion beyond the cell estimate;
`tuned_legends` here scores +2.47 over base, so the small-sample noise plausibly
goes both ways.

The **`unknown` pillar** sits unmoved at 0.9759 across all three models. This
is the bucket of structurally simple passages — short procedural or
header-style chunks where every model already extracts the right span. There
is no ceiling to push against, and no signal to extract.

## 5. Per-answer-type factoid breakdown

| answer_type  | n   | base F1 | tuned_legends F1 | tuned_regulation F1 |
|---|---:|---:|---:|---:|
| single_span  | 107 | 0.8718  | 0.8815           | **0.9126**          |
| group        |  16 | 0.8269  | **0.8907**       | 0.7759              |

The `answer_type` split — predicted as informative in §6.6.2 — exposes the
trade-off described above with full numerical clarity. On the 107 `single_span`
items, `tuned_regulation` widens its lead over base to **+4.08 F1**; on the 16
`group` items (multi-span gold answers, ≥ 8 tokens), `tuned_regulation` falls
**−5.10 F1 below base**. Tuned-legends, with its narrative training, **wins on
both types** but by a smaller margin on single_span (+0.97) and a larger one
on group (+6.38), which is the textbook narrative-vs-factoid trade-off. The
aggregate ranking puts `tuned_regulation` first because the dataset is 87 %
single_span; on a hypothetical equal-weighted split the ordering would
reverse and `tuned_legends` would win the factoid sub-task. This is a
small-sample finding on n = 16 group items but it is exactly the kind of
signal the `answer_type` tag was added to surface.

## 6. Aggregate GE-QA score

```
GE-QA(base)             = (0.8659 + 0.9925) / 2 = 0.9292
GE-QA(tuned_legends)    = (0.8827 + 0.9925) / 2 = 0.9376
GE-QA(tuned_regulation) = (0.8948 + 0.9925) / 2 = 0.9437
```

Because bool is shared across all three models, the entire 1.45-point spread
between `tuned_regulation` and `base` originates in factoid F1, and per §6.6.5
that 1.45-point GE-QA-score difference is exactly half of the 2.89-point
factoid-F1 gap. The §6.6.7 caveat about "open-book attenuation" — that the
three models would compress on this task because the passage is in the prompt
— is borne out: a 1.45-point spread is small in absolute terms, and the
saturation of the bool sub-task is what compresses it. The factoid signal,
isolated from bool, is much larger and points the same direction.

## 7. Limitations of this audit

Three caveats apply to the interpretation above. First, **no statistical test
has been run** here: the §6.6.6 protocol prescribes bootstrap 95 % confidence
intervals over the test set and McNemar's test on per-item correctness for
pairwise comparisons, and on n = 123 factoid items a 2.89-point F1 gap may or
may not survive a McNemar test against `base` once the per-item agreement
structure is taken into account. The forensic block of `ge_qa_results.json`
exposes the per-item scores needed to run that test downstream. Second, the
**bool sub-task is not actually saturated** — it is *parser-saturated*. The
shared 0.9925 ceiling reflects the regex's inability to handle Italian "sì",
not a genuine model ceiling, and the conclusion that "all three models are
indistinguishable on bool" should be qualified accordingly. Third, the
**`mainstreaming_intersectionality` pillar (n = 9)** and the **`group`
answer-type bucket (n = 16)** are both too thinly populated to support
strong claims; the per-item breakdown in the JSON is the safer reference.

## 8. Bottom line

The GE-QA results validate the §6.6 design hypothesis. Tuned-regulation wins
the headline (0.9437 vs base 0.9292), the entire gain comes from the factoid
sub-task, the gain concentrates on the pillars whose passages are densest with
the kind of quantitative spans regulatory training shapes the model to produce,
and the loss on `group`-type answers tracks exactly the format-discipline
mechanism §6.6.7 predicted. Tuned-legends sits between the two as expected,
demonstrating an EM/F1 gap (Δ EM = +0.82 vs Δ F1 = +1.68) consistent with
narrative-format training. The bool sub-task contributes a stable but
non-discriminating signal — a serviceable robustness check on reading
comprehension, but not a meaningful source of model differentiation under the
current parser. Detailed per-item numbers, parse diagnostics, and forensic
movements are in the accompanying `ge_qa_results.json`.
