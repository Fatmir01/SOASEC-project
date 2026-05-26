# The Legend Challenge — Speaker Notes

Bylyshi · El-Khazri · Ouardi · UNIMI · Defense, June 2026

---

## Slide 01 — Title

*(No spoken notes — title card.)*

---

## Slide 02 — The Compliance Paradox

The starting point: LLMs are being deployed for middle-management work — hiring,
procurement, performance review, contract review. All of those domains are
regulated. Managers under cost pressure may deploy AI tools that have no
intrinsic social-cost considerations. So the model can take a corner-cutting
action that conflicts with both corporate values and EU/UN directives. The
implication we'll build on: compliance has to be embedded into the model itself,
not retrofitted via post-hoc filtering.

---

## Slide 03 — Sargsyan–Damiani Proposal

Sargsyan and Damiani, 2025, propose a route — teach compliance via legends. A
legend is a synthetic idealised exemplar, a champion profile. The intuition:
fine-tune on legends and you teach compliance as a capacity exercised over novel
inputs. Fine-tune on regulation text alone and you risk teaching the lexicon —
the model learns to recognise the words without applying the principle. That
contrast is the question this work is built around.

---

## Slide 04 — The Empirical Gap

The proposal is appealing, but it had three things missing: no empirical test,
no measurement instrument, no controlled comparison. General benchmarks like
GLUE don't help — they're deliberately domain-agnostic. So the one-sentence
research question we work to is: does legend fine-tuning produce a measurably
different model from regulation-text fine-tuning, holding everything else
constant.

---

## Slide 05 — Three Contributions

Our contribution is three artifacts: the pipeline that produces matched
legend-vs-regulation corpora; GenderEqGLUE, the five-task benchmark; and CIP, a
behavioural-only probing protocol for closed fine-tuning platforms. Those three
together let us run the comparison the original proposal couldn't.

---

## Slide 06 — Related Work · Embedding Ethics

Prior work splits roughly in two directions. Route one: translate regulation
into a machine-readable format — X2RL, the Danish digital-ready legislation
programme, the U.S. Rules-as-Code pilots. Route two: fine-tune the model on
regulation text directly — IBM's Alignment Studio. The authors of Alignment
Studio themselves note that the literal-textual character of the training signal
is a limitation. That limitation is precisely what the legend route promises to
overcome — and that's the gap we test.

---

## Slide 07 — Related Work · NLU Benchmarks

Why don't general benchmarks suffice. GLUE and SuperGLUE were deliberately built
to be domain-agnostic. So a high GLUE score is evidence of generic linguistic
competence, not regulatory-compliance reasoning. GenderEqGLUE adapts five
canonical GLUE/SuperGLUE templates one-to-one and anchors them in held-out
passages from the EU Gender Equality Strategy.

---

## Slide 08 — Pipeline Overview

The pipeline has six stages: PDF preprocessing, legends generation, pillar
classification, two-stage span extraction, Q&A generation, fine-tuning. Both the
legends branch and the regulation branch share every stage except the source
content. End-state: 327 legend lines, 293 regulation lines — about a 10% gap
that we treat as a corpus-size baseline. Backbone: gpt-4o-2024-08-06.

---

## Slide 09 — Legends Generation

On legend generation specifically: we use three different commercial LLMs in
April 2026 — GPT-5.4 Pro, Gemini 3 Pro, Microsoft Copilot. Each produces five
legends, one per pillar. That gives fifteen legends total. The mixing across
generators maximises stylistic diversity so the fine-tuned model doesn't just
memorise one author's voice. The fifteen narratives expand to 327 closed-book
Q&A pairs.

---

## Slide 10 — Fine-tuning Protocol

On the fine-tuning protocol: every axis except corpus content is held constant.
Same backbone, same system prompt verbatim, same JSONL chat format, the same
hyperparameters under FineTuneDB Studio's control. The only experimental
variable is the corpus content. The cost of that guarantee is closed-platform
access — no logits, no gradients — which is what motivates CIP later.

---

## Slide 11 — GenderEqGLUE · Five Tasks

GenderEqGLUE has five tasks adapted one-to-one from GLUE/SuperGLUE templates.
Pillar classification from SST-2. Compliance entailment from MNLI/RTE. Reading
comprehension from SQuAD/BoolQ. Stereotype-aware coreference from WSC and
Winogender. Compliant-action selection from COPA. The Common Evaluation Base —
217 EU passages — is held out from training entirely. Aggregate is the
unweighted mean of the five headline metrics.

---

## Slide 12 — GE-NLI & GE-NEXT

Two tasks are central to the hypothesis, by design. GE-NLI probes whether the
model recognises compliance — does this scenario entail this regulatory clause.
GE-NEXT probes whether the model selects the compliant action given four
candidates. GE-NEXT has a fixed distractor typology: substantive-compliant gold,
performative gesture, cost-optimising defer-or-minimise, and orthogonal. GE-NEXT
is the direct probe of the compliance-versus-cost arbitrage at the centre of the
original conflict.

---

## Slide 13 — CIP Protocol

On CIP. FineTuneDB Studio is a GUI-only platform. No logits, no gradients, no
batched API. Generated text is the only observable. That blocks SHAP, LIME,
integrated gradients, attention rollout — all of them. CIP is the protocol the
access constraint admits. For each of five pillars we run one base vignette in
three variants — original baseline, keyword-stripped, adversarially framed.
Binary scoring. 45 evaluations total. A model with structural reasoning
maintains its position under B and C. A model relying on lexical mimicry fails
under B.

---

## Slide 14 — Headline Results

The headline result. tuned-regulation wins the aggregate at 0.938. tuned-legends
is at 0.926. Base is at 0.904. Both fine-tuned models clearly beat base. But the
per-task wins split three to three. Base wins nothing. That's the picture you
should hold in your head for the rest of the talk.

---

## Slide 15 — Where the Wins Go

Where the wins go is the interesting part. tuned-regulation wins on the tasks
that match the regulation's lexical and thematic structure — pillar
classification, short-span factoid, and a coreference tie. tuned-legends wins on
the two hypothesis-central reasoning tasks — compliance entailment and
compliant-action selection — and ties on coreference. The aggregate score
conceals this partition; it has to be read alongside the per-task results, not
instead of them.

---

## Slide 16 — GE-WSC Parity Diagnostic

Look closer at the coreference tie. Both fine-tuned models hit 0.96. But the
Gender Parity Score — the absolute gap between pro-stereotype and
anti-stereotype accuracy — is zero for tuned-legends, 0.04 for tuned-regulation.
tuned-regulation's accuracy gain comes entirely from pro-stereotype items, which
widens the gap on Type-1. Same destination, different routes — and only
tuned-legends satisfies the fairness criterion the parity diagnostic formalises.

---

## Slide 17 — CIP Robustness

On the CIP results: aggregates compress almost flat because the backbone is
already strong. tuned-legends scores 14 of 15, the other two score 13. The
aggregate gap is too small at n=15 to support strong inferential claims, and we
say so plainly. What's analytically useful is the qualitative response character
— and the failure distribution, which is informative. All three models converge
on failing the mainstreaming/intersectionality Variant C — that's likely a
property of the frame, not the model.

---

## Slide 18 — Complementarity

The headline finding. Legends and regulation teach complementary compliance
competences. tuned-legends is better at recognising compliance, selecting
compliant action, and long-form factoid extraction. tuned-regulation is better
at detecting violations, classifying into the regulation's ontology, and
short-span factoid extraction. So the deployment question is not which is
'better'. It's: what does your deployment fail at, and which regime do we route
to.

---

## Slide 19 — Limitations

Limitations, declared up front. Small test sets — n=72, n=168, n=123, n=100,
n=150, n=15. Single backbone. The backbone has a discriminative ceiling that
compresses the headroom against which fine-tuning effects can be measured.
There's a latent affinity between LLM-generated GE-NEXT vignettes and an LLM
evaluator — cross-model comparisons remain valid but absolute GE-NEXT accuracy
is indicative. And the underlying data-and-access deficit — small N, single
backbone, closed platform — is the single most consequential constraint.

---

## Slide 20 — Conclusion & Future Work

To conclude. We deliver three artifacts: pipeline, GenderEqGLUE, CIP. Three
conclusions: tuned-regulation leads aggregate; both fine-tuned models clearly
beat base; the per-task wins split three to three. The hypothesis is supported
in its central formulation — legends are strongest on GE-NEXT. The hypothesis
does not generalise — legends and regulation teach complementary competences. v2
of the framework is the path forward: at least 500 items per task, harder
GE-NEXT items, harder coreference probes, multi-backbone replication.

---

## Slide 21 — Thank You / Q&A

Thank you. Open for questions.

---

## Backup Slides (B1–B8)

*(No prepared spoken notes — surface on demand during Q&A.)*

- **B1** — Full pipeline diagram
- **B2** — CEB composition
- **B3** — Per-pillar gains
- **B4** — Full CIP matrix
- **B5** — GE-NEXT example (Inés Lobato vignette)
- **B6** — CIP variant construction
- **B7** — Why not SHAP / LIME?
- **B8** — What is a legend?
