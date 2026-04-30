
# Pipeline LegendsQA

## 1. Data Acquisition

We utilized two primary data sources: the chosen regulation text and the legends
generated during the implementation of the challenge's fourth objective.

Note: implementation of the 1, 2, 3 points of the challenge.

## 2. Document Preprocessing

### 2.1 Regulation text conversion pdf2md
Raw PDF documents undergo streamlined preprocessing to convert them into a
structured, clean, and manageable format. 

The regulation's PDF is first transformed into Markdown text using the [Marker
library (Paruchuri, 2024)](https://github.com/datalab-to/marker), which
preserves structural elements. 

**Workflow Overview**:

> Input: regulation text in PDF format (`gender-equality-strategy-2020-2025.pdf`).

> Process: Execution of the conversion script via the Colab notebook
> `document_preprocessing\pre_processing.ipynb`

> Output: A dedicated directory containing the generated Markdown file and all
> associated artifacts (e.g., extracted images or formatting metadata)
> located at `documents\regulation_pdf2md_output\`



### 2.2 Markdown cleaning
The Markdown output from Marker preserves the document's structural hierarchy
but retains several non-substantive elements inherited from the PDF layout. A
dedicated Python script applies a series of regular expression rules to strip
these artifacts while preserving all policy-relevant content. 

Specifically, the cleaning pipeline removes inline footnote markers (`<sup>`
tags), full footnote text blocks appended at the bottom of each page, image
references (`![](...)` syntax), standalone URLs left over from bibliographic
notes, LaTeX rendering artifacts, and residual page-level elements such as
language markers and separator lines. Bold formatting wrapped around section
headings is normalized, and consecutive blank lines are consolidated. The script
operates line-by-line to ensure that substantive paragraphs — including
statistical figures, calls to action, and legislative references embedded in the
body text — are never inadvertently discarded.


```bash
cd /document_preprocessing && python markdown_cleaning.py
```

```
Output

Original:  64,703 chars
Cleaned:   45,697 chars
Reduction: 29.4%
Sections:  16 headings preserved
Saved to:  documents/gender-equality-strategy-2020-2025_cleaned.md
```

The cleaned document retains all six main sections of the Strategy, their
sub-sections, and every data point and policy commitment present in the original
text, resulting in a 29.4% size reduction with zero content loss.


### 2.3 Segmentation

The cleaned Markdown is segmented through a two-stage process designed to
produce passages that are both semantically coherent and sized appropriately for
downstream LLM processing.

**Stage 1 — Thematic segmentation.** The document is first divided into five
thematic parts aligned with the main policy pillars of the Strategy, using the
top-level Markdown headings (`##`) as natural boundaries. Each part maps to a
distinct area of the regulation: 
1) **Freedom from Violence and Stereotypes**: This chapter outlines the European
    Commission’s strategy to eliminate gender-based violence and dismantle
    limiting gender stereotypes. It prioritizes the **prevention of physical and
    sexual violence**, addresses **online harassment**, and advocates for the
    **ratification of the Istanbul Convention**. Furthermore, it emphasizes the
    need to tackle **gender bias in Artificial Intelligence** and the media to
    ensure that all individuals, in all their diversity, can pursue their
    professional and personal paths without the constraints of traditional
    gender roles.      
    **Label:** violence_stereotypes     
2) **Thriving in a Gender-Equal Economy**: This section focuses on achieving
    economic independence for all genders by closing gaps in the labor market, pay,
    and pensions. Key initiatives include the **Work-Life Balance Directive** to
    promote shared care responsibilities, binding measures on **pay transparency**,
    and targeted support for women in **STEM** and **entrepreneurship**. It also
    addresses the "gender care gap" by proposing a revision of the **Barcelona
    targets** for childcare and investing in long-term care services.        
    **Label:** equal_economy
3) **Leading Equally Throughout Society**: This section addresses the
    under-representation of women in leadership roles across politics,
    government agencies, and corporate boards. It advocates for inclusive
    leadership to drive innovation and strengthen democracy, specifically
    pushing for the **Women on Boards Directive** to achieve a 40% target for
    non-executive directors. The Commission commits to leading by example by
    aiming for **50% gender balance** at all management levels by 2024 and
    supporting female participation in the **2024 European Parliament
    elections**.
    **Label:** leadership_participation
4) **Gender Mainstreaming and Intersectional Perspective**: This section
    establishes gender equality as a cross-cutting priority for all EU policies,
    ensuring that the gender dimension is integrated into the green transition,
    digital transformation, and health initiatives. It introduces a **Task Force
    for Equality** to implement this operational mainstreaming and emphasizes an
    **intersectional approach**, recognizing that women face unique challenges
    when gender overlaps with characteristics like disability, migrant status,
    or age. Practical applications include addressing energy poverty in the
    **European Green Deal** and integrating gender-specific risks into the **EU
    Beating Cancer Plan**.
    **Label:** mainstreaming_intersectionality
5) **Funding and Global Action for Equality**: This final section details the
    financial mechanisms and external strategies used to achieve gender
    equality. It integrates gender dimensions into the **Multi-Annual Financial
    Framework (MFF)**, using instruments like the **European Social Fund Plus**
    and **Horizon Europe** to fund childcare, entrepreneurship, and research.
    Globally, the EU aims for **women's empowerment** through international
    partnerships, trade policies, and the **GAP III** action plan, committing
    that 85% of new external programmes contribute to gender equality. Progress
    is monitored through annual reports and the **EIGE Gender Equality Index**
    to ensure a joint responsibility across all EU institutions and Member
    States.
    **Label:** funding_global_action



"EU Gender Equality Strategy 2020-2025" + label



OUTPUT:
- prompts:
  - regulation_part_n.md


**Stage 2 — Word-count constrained sub-segmentation.** Each thematic part is
then further split into smaller passages using sub-headings (`###`) and a
maximum word-count constraint (max_words = 350). When a sub-section exceeds this
threshold, it is divided at paragraph boundaries to ensure that no passage
crosses a semantic break mid-sentence. This constraint keeps every passage
within an optimal context window for the subsequent LLM-based question
generation phase, avoiding both excessively short fragments that lack sufficient
context and overly long blocks that could dilute the model's focus.

*Note: The SustainableQA framework includes an additional table-handling step
during segmentation; this is omitted here as neither the regulation text nor the
legend narratives contain tabular data.*


OUTPUT: list of semantically coherent text segments or passages, with a
      word-count constraint (e.g., max_words=350) 


## 3. Legends Generation

> Note: implementation of the foruth point of the challenge.

Sargsyan and Damiani (2025) proposal leverages regulation text to create
legends. i.e., positive/ideal "champion" profiles (exemplars) of individuals
whose behavior incarnates regulatory compliance. 

A **legend** is a story with characters showing concrete compliance with the
regulation.

We decided to generate 5 legends for each LLM (Grok, Copilot, and ChatGPT).

We used all three LLMs to maximize the stylistic and contextual diversity of the
training data, explaining that legends generated by different models introduce
variability that makes fine-tuning more robust.

### Legends generation process

Legends or champion profiles can be defined as idealized representations of
individuals who perfectly embody the traits, behaviors, and characteristics that
align with regulatory requirements and organizational values.

Our generation process starts from the 5 thematic parts that we were able to
isolate during the (2.3.1) stage of our pipeline. The generation process then
like its is suggested by Sargsyan and Damiani (2025) is LLM based. Our strategy
was to use each of the five semantically coherent passages as context to
generate legends using an LLM and a specific system prompt. We used the example
legend from Appendix A as a base to draft our system prompt that was used across
all LLMs.

> You are a legend generator for an academic experiment on EU regulatory compliance.
>
> A "legend" is a short fictional story featuring named characters who demonstrate concrete compliance with a specific aspect of the EU Gender Equality Strategy 2020-2025.
> Every legend you produce must follow this exact structure:
> 
> # **Title** 
> A short, evocative title.
>
> ## **Setting**
> A brief paragraph introducing the organization (company, institution, NGO, public body, etc.), its sector, and the city or country where it operates. Vary the sector and setting across legends.
>  
> ## **Characters** 
> A bulleted list of 3–5 fictional characters, each with:
>    - A name (use gender-neutral or diverse names)
>    - A role within the organization
>    - A one-sentence description of their relevance to the story
> 
> ## **The Story** 
> A narrative of 400–600 words in which:
>    - The characters identify a concrete gender-equality gap related to the regulation point provided by the user.
>    - They design and implement specific, realistic measures to address that gap.
>    - The narrative includes at least one direct-speech dialogue among the characters.
>    - The story ends with a measurable positive outcome and an acknowledgment that the work aligns with the EU Gender Equality Strategy 2020-2025.
> 
> Content rules:
> - Each legend must focus exclusively on the specific regulation point supplied by the user in their message.
> - Cite the official name of the strategy ("EU Gender Equality Strategy 2020-2025") at least once.
> - Keep the tone professional yet accessible — suitable for an academic paper appendix.
> - Do not reuse the same sector, country, or character names across different legends.
> - Make compliance actions concrete and realistic (e.g., salary audits, mentorship programs, policy changes, training workshops), never generic or vague.
> 
> When the user sends a message, it will contain the specific regulation point to address. Respond with one legend and nothing else. Wait the user input before generating each legends.

After the LLM behaviour was influenced by the system prompt, each legend was
generated by a prompt like this one:
 
> Generate a single legend focusing on the following regulation point: 
> 
> \<context\> 
>
> Adhere strictly to the established four-part structure and the content rules
> regarding diverse settings, concrete compliance actions, and character count.

The context used for the $n-th$ legend is found in
`prompts/regulation_part_n.md`.

OUTPUT:
- legends 
  - chat-gpt
    - legend_n.md
  - copilot
    - legend_n.md
  - gemini
    - legend_n.md




## 4. Question-Answering Dataset Generation

The core Q&A generation process integrates content classification, span
extraction, and the creation of diverse question types to maximize information
coverage (see Appendix C for all prompts used in the generation pipeline).

### 4.1 Passage Classification. 

To ensure relevance and aggregate dispersed information, each passage isolated
in the 2.3.2 pipeline point undergoes classification using <\LLM of our choice\>
(SustainableQA used Llama 3.3 (70B) (Grattafiori et al., 2024))

Classification into six categories (5 thematic clusters + unkown), based on the
thematic clusters used to generate the legends:
1) Freedom from Violence and Stereotypes, 
    **Label:** violence_stereotypes

2) Thriving in a Gender-Equal Economy, 
    **Label:** equal_economy

3) Leading Equally Throughout Society, 
    **Label:** leadership_participation

4) Gender Mainstreaming and Intersectional Perspective, 
    **Label:** mainstreaming_intersectionality

5) Funding and Global Action for Equality, 
    **Label:** funding_global_action

6) Unknown: The category for **Unknown** encompasses any text passages that
    do not directly relate to the specific pillars of the **EU Gender Equality
    Strategy 2020-2025**. This includes content that is **semantically
    irrelevant**, such as general administrative text, headers, or metadata, as
    well as information that falls outside the defined thematic scopes of
    **violence**, **economy**, **leadership**, **mainstreaming**, or **global
    funding**. These passages are filtered out during the preprocessing phase to
    ensure that the **LLM tuning** remains focused on domain-specific
    **compliance and ethical behavior**.      
    **Label:** unknown


### 4.2 Span Extraction for Factoid Q&A: 

We dont need advanced span extraction. 

The adapted span extraction pipeline replaces the original multi-stage NER and
rule-based architecture with a single LLM-driven extraction phase. 

#### Stage 1: LLMAugmented Span Extraction.

Since the synthetic legends and also the regulation text are inherently clean
and focused, complex pre-trained entity recognition models and regex
dictionaries are unnecessary. An LLM is prompted directly to process each
passage and extract critical factual spans, such as explicit regulatory
citations, the operational conflict, and the concrete resolution that will serve
as answers for factoid questions. The sole objective of this phase is to
perform contextual verification and output a clean list of precise candidate
spans, strictly deferring all generation of question-and-answer pairs to a
subsequent stage.


**System Prompt: Span Extractor**

```markdown
**System:** You are a span extractor that prioritizes **recall** and outputs results in **JSON format**. Your goal is to find as many valid spans as possible, adhering strictly to the formatting and content guidelines.

### **TASK**
Extract concise, meaningful spans relevant to a given classification.

**INPUT**
* **Context:** `"{content}"`
* **Classification:** `"{classification}"`

### **EXTRACTION RULES**

#### **Include These:**
* Entities, criteria, activities, and technical concepts.
* **Quantitative data** (e.g., '50% reduction', '10 MWh', 'C5 million').
* **Specific dates/timeframes** (e.g., 'by 2030', 'FY2023').
* **Named standards/initiatives** (e.g., 'GRI Standards', 'TCFD recommendations').
* **Specific regulations/policies** (e.g., 'CSRD Article 8', 'EU Taxonomy').
* **Clearly defined risks or targets** (e.g., 'net-zero target').

#### **Exclude These:**
* **Generic terms:** 'company', 'organization', 'report', 'year', 'data', 'information', 'impacts', 'approach', 'process', 'management', 'performance', 'strategy', 'framework'.
* **Generic adjectives:** 'important', 'significant' (unless part of a named entity).
* **Common functional phrases:** 'in order to', 'as well as', 'responsible for'.

### **FORMAT REQUIREMENTS**
* **Extract spans verbatim.** Most spans should be 1-5 words.
* Critical named entities or specific metrics may be 6-7 words if necessary.
* Do **not** modify, rephrase, or summarize.
* Prioritize the most complete and specific verbatim phrase.


### **OUTPUT**
````json
{
  "spans": ["<span 1>", "<span 2>", ...]
}
````
```

```markdown
**System:** You are a high-recall span extractor specialized in the **EU Gender Equality Strategy 2020-2025**. Your goal is to identify every verbatim segment of text that aligns with the strategy's pillars, legal directives, or specific socio-economic targets.

### **TASK**
Extract concise, verbatim spans relevant to the **Classification** below.

**INPUT**
* **Context:** `"{content}"`
* **Classification:** `"EU Gender Equality Strategy Pillars"`

### **EXTRACTION SCOPE (PILLARS)**
1.  **Gender-Based Violence:** Ending physical, sexual, and psychological violence, including cyberviolence and harassment.
2.  **Gender Stereotypes:** Measures to challenge unconscious bias in education, culture, and the workplace.
3.  **Labour Market & Care Gap:** Closing gaps in employment, including work-life balance and long-term care provisions.
4.  **Equal Participation:** Addressing horizontal segregation in sectors like STEM or HEAL (Health and Education).
5.  **Gender Pay & Pension Gap:** Enforcing equal pay for work of equal value and pay transparency.
6.  **Decision-Making Balance:** Achieving gender parity in leadership, corporate boards, and political positions.

### **EXTRACTION RULES**
* **Verbatim Extraction:** Do not paraphrase. Extract exactly as written in the text.
* **Legal & Technical Terms:** Prioritize specific directives (e.g., **Pay Transparency Directive**, **Women on Boards**) and quantitative targets (e.g., **40% of non-executive directors**).
* **Span Length:** Most spans should be 1-5 words. Extend to 8 words only for complex named entities or regulatory clauses.
* **Exclude:** Generic organizational filler (e.g., 'the company', 'next year').

### **OUTPUT**
`````json
{
  "spans": ["<span 1>", "<span 2>", ...]
}
`````
```         

#### Stage 2: Contextual Verification, Filtering, and Thematic Organization. 

The candidate spans undergo then the second LLM-based processing stage that
performs three functions: 

(1) contextual verification to ensure that the spans are actually present in the
source text, 

(2) filtering to eliminate redundant or suboptimal entries, and 

(3) thematic grouping of spans into semantically coherent clusters with
descriptive labels. This grouping strategy is introduced so that questions can
be generated not only based on individual spans used as their answers but also
on the groups of multiple spans that are semantically related. The latter helps
to create complex questions which require answers composed of multiple related
spans
        


### 4.3 Text-based Question-Answering
       
With relevant passages identified and key spans extracted, we can now generate
diverse QA pairs (see Appendix E for examples) for each passage using advanced
LLMs.


#### 4.3.1 Factoid Q&A Generation

For every passage, we generate comprehensive factoid QA pairs using GPT-4o
through a structured approach. 

- First, we create questions based on individual spans.     
- Next, we create group-level questions that require multiple spans as
  complete answers from each thematic cluster.    

All questions maintain exact correspondence to their extracted passages,
ensuring direct answerability from the provided context while following
"closed-book" constraints, thus guaranteeing accurate and verifiable responses
across different structural types.



#### 4.3.2 Non-Factoid Q&A Generation 

In addition to factoid questions, we create non-factoid
(descriptive/explanatory) QA pairs for each passage using GPT-4o. These
questions require comprehensive textual analysis rather than isolated fact
retrieval, eliciting detailed answers that explain relationships, describe
processes, define concepts, or discuss implications within the passage. The
generated responses typically span 1-4 sentences.


#### wHY AN EXAMPLE LIKE THIS ONE IS ALRIGHT


{"messages": [{"role": "system", "content": "You are an expert assistant on the EU Gender Equality Strategy 2020-2025. Answer questions about the strategy's policy objectives, instruments, and concrete examples of compliance accurately and concisely, grounded in the Strategy's text and its illustrative legends."}, {"role": "user", "content": "How does the passage describe the foundation on which a prosperous and social Europe rests?"}, {"role": "assistant", "content": "The passage states that a prosperous and social Europe depends on everyone, framing economic and social progress as inseparable from collective participation. It then outlines the equal opportunities and economic independence that women and men in all their diversity should enjoy."}]}


Great question — and the answer matters a lot for what your fine-tuned model actually learns. The short version: **for your project, the example as it stands is the right design**. Adding the passage would change what you're training the model to do in a way that breaks your experimental setup.

Here's the reasoning, then a caveat.

##### What each format teaches

**Closed-book (your current format)** — the model sees only the question and must produce the answer from its parameters. Fine-tuning on this format pushes the model to **internalize** the Strategy's content and the legends' compliance behaviors. The knowledge ends up baked into the weights.

**Open-book (passage included as context)** — the model sees question + passage and must extract or paraphrase the answer from the passage. Fine-tuning on this format teaches the model to be **a better reader**, but it teaches very little about the Strategy itself. At inference time, if you don't supply a passage, the model has no idea how to answer. It hasn't memorized anything — it has learned a copying skill.

##### Why closed-book fits your specific challenge

Sargsyan and Damiani's hypothesis — the one your benchmark is built to test — is that **legends embed regulation knowledge into the model itself**, as an alternative to retrieval-style approaches. Their whole proposal is about *baking ethics into the weights*, not about teaching better reading comprehension. If you train open-book, you're testing a different hypothesis: "does context-augmented prompting help with gender-equality questions?" — interesting, but not what point 10 of the challenge is asking you to demonstrate.

There's also a downstream consequence. Your GenderEqGLUE benchmark in section 6 evaluates the three models without supplying the source passage in the prompt (with the natural exception of GE-QA, which is a reading-comprehension task by definition). If you fine-tune open-book, the tuned models will perform worse than the base on GE-CLS, GE-NLI, and GE-STANCE because they've never been asked to answer without a passage in front of them. You'd be sabotaging your own experiment.

And the symmetry argument: the regulation-tuned model sees regulation Q&A pairs as `{question → fact}`, while the legends-tuned model sees legend Q&A pairs as `{question → narrative compliance}`. Both formats are closed-book and parallel. If you added passages, the regulation-tuned model would see the actual Strategy text every time, which is essentially showing it the answer key alongside the answer. The legends model would see fictional scenarios alongside the answers. The comparison stops being about *kind of training material* and becomes about *kind of context window* — a totally different dimension.

##### The legitimate caveat

If your factoid Q&A include very short, span-extractive answers (e.g. "40%", "2026", "Istanbul Convention"), some of those questions will be genuinely ambiguous without the passage. "What is the target percentage for non-executive directors?" — the answer is 40% in the Women on Boards Directive context, but a model with no context might reasonably say something else if multiple percentages exist in the Strategy. For these cases, two clean options:

1. **Make the question self-disambiguating**. Rewrite "What is the target percentage?" → "What is the target percentage set by the Women on Boards Directive for non-executive directors of the under-represented sex?". The disambiguation lives in the question, not in an attached passage. This keeps closed-book training intact.

2. **Drop a small fraction of irreducibly ambiguous factoid items** during the conversion to JSONL. Better a slightly smaller dataset than a noisy one.

Looking at your existing non-factoid pairs — like the example you posted — they're already self-contained. The question references "the passage" linguistically but is really asking about a concept ("the foundation on which a prosperous and social Europe rests"), and the gold answer is a substantive paragraph. That works well closed-book. The "passage" in the question is a stylistic hangover from how you generated the data — a model fine-tuned on enough of these will read it as roughly equivalent to "in this domain" or "in the Strategy". Worth tightening if you do another pass on the data, but not a blocker.

##### One small data-cleaning suggestion

Across both your datasets, search for `"the passage"`, `"this passage"`, `"according to the passage"` in the questions and consider rephrasing. After fine-tuning, when a real user asks "What does the EU say about pay transparency?", you don't want the model trained to expect the phrase "passage" as a cue. Light find-and-replace before the JSONL build is a 10-minute job that pays off in cleaner inference behavior.

So: keep the closed-book format, tighten the questions to be self-disambiguating, and proceed. Your current example is fundamentally the right shape.




## 5. Fine-tuning

> Note: implementation of the sixth and seventh points of the challenge.

The Q&A pairs produced by the previous stage of the pipeline live inside
two structured JSON files: one derived from the regulation text and one
derived from the legends. Each pair is annotated with its source chunk,
its pillar classification, and its question type (factoid or
descriptive non-factoid). To use these pairs for fine-tuning on the
FineTuneDB platform, the data must be reformatted into the platform's
JSONL chat schema and split into two parallel datasets — one per
training corpus — of comparable size, as required by point (7) of the
challenge.

### 5.1 JSON to JSONL Conversion

FineTuneDB expects each training example as a single JSONL line in chat
format, with three message turns: a system prompt that anchors the
model in the gender-equality domain, a user turn carrying the question,
and an assistant turn carrying the gold answer. The conversion is
performed by a dedicated script (`document_preprocessing/json2jsonl.py`)
that walks the input JSON, filters out chunks classified as `unknown`
together with chunks that contain no Q&A pairs, and emits one JSONL
line per Q&A pair.

The system prompt is identical across all examples and across both
datasets, so that the only variable between the two fine-tuned models
is the **content** of the user/assistant pairs they are trained on:

```text
You are an expert assistant on the EU Gender Equality Strategy 2020-2025.
Answer questions about the strategy's policy objectives, instruments, and
concrete examples of compliance accurately and concisely, grounded in the
Strategy's text and its illustrative legends.
```

Each line of the resulting JSONL therefore has the following structure:

```json
{
  "messages": [
    {"role": "system",    "content": "<system prompt above>"},
    {"role": "user",      "content": "<question>"},
    {"role": "assistant", "content": "<answer>"}
  ]
}
```
**Workflow Overview**:

> Input: the two JSON files produced by section 4 — one for the
> regulation, one for the legends.

> Process: execution of `document_preprocessing/json2jsonl.py` once per
> source.

> Output: two FineTuneDB-compatible JSONL files —
> `documents/gender-equality-strategy-2020-2025_qa.jsonl` and `legends/legends_qa.jsonl`.



## 6. GenderEqGLUE: a GLUE Adaptation for Gender Equality

> Note: implementation of the ninth point of the challenge.

The GLUE benchmark (Wang et al., 2018) was designed as a general-purpose
diagnostic for natural language understanding, but its tasks are
domain-agnostic and do not capture the specific competencies required to
reason about gender-equality regulation. Following the precedent set by
LexGLUE (Chalkidis et al., 2022) for the legal domain, we propose
**GenderEqGLUE**, a benchmark composed of five tasks that jointly
evaluate a language model's ability to operate on the EU gender-equality
regulatory landscape.

The benchmark is designed to compare three models on identical conditions:
the open pretrained LLM, its version fine-tuned on legends, and its
version fine-tuned on regulation text — implementing point (10) of the
challenge.

### 6.1 Conceptual backbone

The five tasks are not chosen ad hoc: they are anchored to the principles
that recur across the EU's gender-equality acquis. We surveyed three
documents to extract these principles: the **Gender Equality Strategy
2020-2025** (the regulation used to fine-tune our models), the
**Roadmap for Women's Rights** (2025), and the **Gender Equality Strategy
2026-2030**.

The Roadmap articulates eight long-term principles: (1) freedom from
gender-based violence, (2) the highest standards of health, (3) equal
pay and economic empowerment, (4) work-life balance and care, (5) equal
employment opportunities and adequate working conditions, (6) quality and
inclusive education, (7) political participation and equal
representation, and (8) institutional mechanisms that deliver on women's
rights. The 2026-2030 Strategy preserves these and explicitly addresses
new threats — cyberviolence, anti-gender narratives, and AI-driven
discrimination — while keeping the intersectional approach and the
combination of mainstreaming with targeted action.

From these three iterations we identify eight stable cross-cutting
principles that constitute the conceptual backbone of GenderEqGLUE:
freedom from violence (including online), economic empowerment, leadership
and representation, stereotypes and bias (including AI bias), work-life
balance and care, intersectionality and mainstreaming, health, and
inclusive education. Each task in the benchmark covers one or more of
these principles.

### 6.2 Benchmark overview

GenderEqGLUE comprises five tasks. The first three — GE-CLS, GE-NLI and
GE-QA — operate on a common textual base extracted from EU documents
not seen during fine-tuning. The remaining two — GE-WSC and GE-STANCE —
rely on external consolidated datasets, since they require text types
that institutional EU documents do not naturally provide.

| Task       | Description                          | GLUE analogue   | Source                          | Metric                       |
|------------|--------------------------------------|-----------------|---------------------------------|------------------------------|
| GE-CLS     | Pillar Classification                | SST-2           | Common EU base                  | Macro-F1                     |
| GE-NLI     | Compliance Entailment                | MNLI / RTE      | Common EU base + legends        | Accuracy                     |
| GE-QA      | Regulation Reading Comprehension     | SQuAD / BoolQ   | Common EU base                  | F1 / Exact Match             |
| GE-WSC     | Stereotype-Aware Coreference         | WSC / Winogender| WinoBias (open source)          | Accuracy + Gender Parity     |
| GE-STANCE  | Gender Equality Stance Detection     | SST-2           | CIVICS + curated examples       | Macro-F1                     |

The aggregate **GenderEqGLUE Score** is the unweighted arithmetic mean of
the five task metrics, mirroring the original GLUE score.

### 6.3 Common Evaluation Base

For the three domain tasks (GE-CLS, GE-NLI, GE-QA) we constructed a
single **Common Evaluation Base (CEB)** rather than gathering separate
sources per task. A shared base ensures that performance differences
across tasks reflect task properties rather than source variability,
keeps the benchmark replicable, and aligns with the LexGLUE methodology.

The CEB is extracted from four EU documents that are thematically
contiguous to the Strategy 2020-2025 but **not present in the training
data of any of the three models under evaluation**:

1. Roadmap for Women's Rights (2025)
2. Gender Action Plan III (GAP III) 2021-2025
3. Council Conclusions on Closing the Gender Pay Gap (June 2019)
4. Directive (EU) 2022/2381 on improving the gender balance among
   directors of listed companies (Women on Boards Directive)

#### 6.3.1 Document preprocessing

The four documents are processed through the same pipeline used for the
regulation text in section 2: PDF-to-Markdown conversion via Marker,
regex-based Markdown cleaning to remove footnote markers, page artifacts
and inline references, and word-count constrained segmentation with
`max_words = 350`.

The output of this phase is located in the folder `./benchmark/`, specifically
in the 3 subfolders `./benchmark/original/`, `./benchmark/cleaned/`, `./benchmark/chunked/`.


#### 6.3.2 Pillar annotation

The pool is annotated independently by two annotators using the six-class
taxonomy defined in section 4.1:
`violence_stereotypes`, `equal_economy`, `leadership_participation`,
`mainstreaming_intersectionality`, `funding_global_action`, `unknown`.

Inter-annotator agreement is measured with **Cohen's kappa**.
Disagreements are resolved through a consensus discussion involving a
third annotator when needed. The kappa score and the disagreement-resolution
log are reported in the benchmark documentation as required by accepted
practice for human-annotated NLP benchmarks.

The target annotated pool size is approximately 250-350 passages, with at
least 30 passages per pillar.

OUTPUT:
  - `./benchmark/ceb_pool.json`



#### 6.3.3 Disjoint partitioning

To prevent cross-task contamination — a passage used as a GE-CLS test
item must not reappear as a GE-QA context — the annotated pool is
partitioned into three disjoint subsets through a stratified random
split with `seed=42`:

- `CEB-CLS` → input pool for GE-CLS  (72 passages)
- `CEB-QA`  → input pool for GE-QA   (72 passages)
- `CEB-NLI` → input pool for GE-NLI  (73 passages)

The split ratio is approximately 1/3 each. Stratification on the
pillar label preserves the per-pillar distribution across the three
subsets, ensuring that no pillar is over- or under-represented in
any single task. The split is implemented as a two-step
`StratifiedShuffleSplit` (sklearn) with the seed fixed and the
indices saved alongside the partitioned files for replicability.

Per-pillar distribution after the split:

| Pillar                            | Pool | CLS | QA | NLI |
|-----------------------------------|-----:|----:|---:|----:|
| `violence_stereotypes`            |   72 |  24 | 24 |  24 |
| `leadership_participation`        |   45 |  15 | 15 |  15 |
| `funding_global_action`           |   21 |   7 |  7 |   7 |
| `equal_economy`                   |   18 |   6 |  6 |   6 |
| `mainstreaming_intersectionality` |   11 |   4 |  3 |   4 |
| `unknown`                         |   50 |  16 | 17 |  17 |
| **Total**                         |  217 |  72 | 72 |  73 |

OUTPUT:
- `./benchmark/task_pool/ceb_cls.json`
- `./benchmark/task_pool/ceb_nli.json`
- `./benchmark/task_pool/ceb_qa.json`


### 6.4 Task 1 — GE-CLS (Pillar Classification)

**Objective.** Given a textual passage, classify it into one of the five
EU gender-equality pillars or as `unknown`.

**Format.** Single-input multi-class classification across six labels:
`violence_stereotypes`, `equal_economy`, `leadership_participation`,
`mainstreaming_intersectionality`, `funding_global_action`, `unknown`.

**Example:**
> Input: "The directive sets a minimum of 40% of non-executive members of
> the under-represented sex on listed company boards by 2026."
> Label: `leadership_participation`

**Data.** The task uses `CEB-CLS` (72 passages) directly. No additional
construction is required: each passage already carries its consensus
pillar label from section 6.3.2.

Predictions are parsed with a deterministic regular expression. A
response that does not match the expected format is recorded as a
`PARSE_FAIL` and counted as a misclassification (no retries). The
parse-failure rate is reported as a separate diagnostic.

To bound the introduced
noise, all model interactions follow a fixed prompt template stored
verbatim in `./benchmark/task_pool/ge_cls/ge_cls_system_prompt.txt`, the prompt is pasted
unmodified into each session

**GLUE analogue.** SST-2 (single-sentence classification, generalised
to multi-class).

**Metric.** Macro-F1 across the six classes. Per-class F1 and the
inter-model confusion matrix are reported as diagnostics. Per-class
F1 on classes with fewer than 30 test items
(`equal_economy`, `mainstreaming_intersectionality`,
`funding_global_action`) is flagged as low-confidence.

**Why it matters.** GE-CLS measures whether the model has internalised
the *thematic structure* of the regulation. The base model is expected
to score low; the two fine-tuned models are expected to improve, with
tuned-regulation likely leading on this task because the regulation
text explicitly mirrors the pillar structure.

OUTPUT:
- `./benchmark/task_pool/ge_cls/ge_cls_system_prompt.txt`




### 6.5 Task 2 — GE-NLI (Compliance Entailment)

**Objective.** Given a scenario describing organisational behaviour
(premise) and a regulatory clause (hypothesis), determine whether the
scenario *entails*, *contradicts*, or is *neutral with respect to* the
clause.

**Format.** Three-class classification: `entailment`, `contradiction`,
`neutral`.

**Example:**
> Premise: "TechCorp introduced a mentorship programme for women,
> conducted a salary audit, and reached 45% female representation among
> non-executive directors."
> Hypothesis: "TechCorp meets the Women on Boards Directive target of
> 40% non-executive directors of the under-represented sex."
> Label: `entailment`

**Data construction.** GE-NLI premises and hypotheses are produced by
combining `CEB-NLI` with the legends pool, with the following constraints
to prevent leakage:

- Hypotheses are short regulatory clauses extracted from `CEB-NLI`
  passages — never from the Strategy 2020-2025 used in training.
- Premises describing compliant scenarios are drawn from a held-out
  partition of the legends pool: one legend per pillar (5 legends total)
  is excluded from the fine-tuning JSONL of section 5 and reserved for
  GE-NLI premise construction.
- `contradiction` examples are produced by perturbing compliant premises
  along quantitatively measurable dimensions (e.g. "45% female
  representation" → "15% female representation").
- `neutral` examples are produced by pairing compliant premises with
  hypotheses about pillars not addressed in the premise.

The construction yields approximately 150-300 (premise, hypothesis,
label) triples, balanced across the three classes.

**GLUE analogue.** MNLI / RTE.

**Metric.** Accuracy.

**Why it matters.** GE-NLI is the **central task** of the benchmark with
respect to the Sargsyan and Damiani (2025) hypothesis. It directly
measures the ability to recognise *compliance* — the competence that
legends are designed to teach. If legends embed regulatory understanding
better than raw regulatory text, the gap between tuned-legends and
tuned-regulation should be most visible here.

### 6.6 Task 3 — GE-QA (Regulation Reading Comprehension)

**Objective.** Given an EU regulatory passage and a question, produce a
correct answer derived from the passage.

**Format.** Two sub-tasks:

- **GE-QA-Factoid** — extractive span-based answers (SQuAD-style).
- **GE-QA-Bool**    — yes/no answers (BoolQ-style).

**Example (Factoid):**
> Context: "The directive sets a minimum of 40% of non-executive members
> of the under-represented sex on listed company boards by 2026."
> Question: "What is the target percentage for non-executive directors of
> the under-represented sex?"
> Answer: "40%"

**Example (Bool):**
> Context: [passage on EU accession to the Istanbul Convention from CEB-QA]
> Question: "Has the EU concluded its accession to the Istanbul Convention?"
> Answer: `no`

**Data construction.** Q&A pairs are generated from `CEB-QA` passages
following the same two-stage span-extraction and Q&A generation pipeline
described in section 4.3.1, with two important differences:

- The source pool is `CEB-QA`, not the Strategy 2020-2025.
- A new generation step produces yes/no questions framed against the
  passage content for the GE-QA-Bool sub-task.

The output is approximately 150-250 factoid and 100-150 boolean items.

**GLUE analogue.** SQuAD (factoid) + BoolQ (boolean).

**Metric.** F1 and Exact Match for GE-QA-Factoid; accuracy for GE-QA-Bool.
The two sub-task metrics are averaged into a single GE-QA score.

**Why it matters.** GE-QA tests *factual recall* anchored in regulatory
text. The tuned-regulation model is expected to dominate this task: it
has been trained on regulatory prose of identical register and structure.
The tuned-legends model is expected to underperform here, since legends
contain fictional facts rather than regulatory ones — providing a useful
contrast to GE-NLI.

### 6.7 Task 4 — GE-WSC (Stereotype-Aware Coreference)

**Objective.** Resolve pronominal coreference in professional contexts
without relying on gender stereotypes.

**Format.** Binary classification: which of two candidate antecedents the
pronoun refers to.

**Example:**
> Sentence: "The CEO promoted the assistant because she was impressed by
> her work."
> Question: To whom does *she* refer?
> Label: `CEO`

**Data.** We use **WinoBias** (Zhao et al., 2018) directly from the
HuggingFace Hub (`uclanlp/wino_bias`), with all four subsets:
`type1_pro`, `type1_anti`, `type2_pro`, `type2_anti`. No construction is
performed by us — this is the standard bias-evaluation dataset in the
literature, kept *as-is* to remain comparable with the broader fairness
research in NLP.

**GLUE analogue.** WSC / Winogender (the SuperGLUE diagnostic dataset).

**Metric.** Two metrics are reported:

- **Accuracy** averaged across the four subsets.
- **Gender Parity Score** = | accuracy(pro-stereotype) −
  accuracy(anti-stereotype) | . A model that is genuinely fair has a
  parity score close to zero.

**Why it matters.** GE-WSC is the bias-detection task explicitly
requested by Appendix B. It maps onto the *Freedom from stereotypes*
pillar of the 2020-2025 Strategy and onto the AI-bias focus of the
2026-2030 Strategy. Because the bias originates in the pretraining
distribution rather than in the fine-tuning corpus, we do **not** expect
either fine-tuned model to outperform the base on this task — and the
result, whatever it is, is informative.

### 6.8 Task 5 — GE-STANCE (Gender Equality Stance Detection)

**Objective.** Given a statement, determine whether the position it
expresses is *supportive*, *neutral*, or *against* gender equality.

**Format.** Three-class classification: `supportive`, `neutral`, `against`.

**Example:**
> Statement: "Gender equality is essential for a fair society."
> Label: `supportive`
>
> Statement: "Women are not as good at coding as men."
> Label: `against`

**Data.** GE-STANCE combines two sources:

- **CIVICS** (`llm-values/CIVICS` on HuggingFace), filtered on the
  `gender inclusivity` and `anti-discrimination` labels.
- A curated test set of 100-200 statements written by the team. EU
  documents are by construction supportive of gender equality, so the
  `against` and `neutral` classes cannot be extracted from CEB. Curated
  examples include realistic anti-gender or sceptical positions phrased
  neutrally enough that the task remains non-trivial. Each curated item
  is double-labelled internally; only items with annotator agreement
  enter the test set.

**GLUE analogue.** SST-2 generalised to three classes.

**Metric.** Macro-F1 across the three classes.

**Why it matters.** GE-STANCE addresses the second illustrative task of
Appendix B. It tests whether the model has internalised the *values*
underlying the regulation, not just its facts. Because legends embody
positive normative behaviour, the tuned-legends model is expected to
match or exceed the tuned-regulation model on this task — providing a
second piece of evidence, alongside GE-NLI, for the central hypothesis
of Sargsyan and Damiani (2025).

### 6.9 Diagnostic set — GE-Diag (reported separately)

Inspired by SuperGLUE's separately-reported Winogender diagnostic, we
construct **GE-Diag**, a small set of *minimal pairs* not included in
the aggregate GenderEqGLUE Score but reported alongside it.

**Construction.** Approximately 50 pairs are drawn from the legends pool.
For each item, we produce two versions of the same passage in which only
the gender of the protagonist is swapped (e.g. *Alex* ↔ *Alessandra*),
keeping all factual content identical. The pair is presented to the
model as a downstream task (e.g. a GE-CLS classification or a
GE-STANCE judgement).

**Metric.** **Stability score** = percentage of pairs for which the
model returns identical predictions. A genuinely gender-invariant model
has a stability score of 100%.

**Why it matters.** GE-Diag complements the explainability analysis of
point (11) of the challenge by providing a quantitative measure of
gender-swap invariance, in line with the methodology of GECOBench
(Lacombe et al., 2024).

### 6.10 Aggregate score and reporting

For each of the three models — base, tuned-legends, tuned-regulation —
we report:

- The five per-task metrics (Macro-F1, Accuracy, F1/EM, Accuracy+Parity,
  Macro-F1).
- The **GenderEqGLUE Score**, computed as the unweighted arithmetic mean
  of the five task scores. For GE-WSC the score component is the
  accuracy; the parity score is reported separately as a diagnostic.
- The **GE-Diag stability score**.

To distinguish meaningful differences from noise on test sets in the
200-500 example range, we report **bootstrap 95% confidence intervals**
for each task metric and apply **McNemar's test** to per-example
predictions when comparing pairs of models. A difference smaller than
the confidence interval is reported as not significant.

### 6.11 Summary of data flows

```
Common Evaluation Base (CEB)
├── CEB-CLS  ──► GE-CLS
├── CEB-QA   ──► GE-QA  (Factoid + Bool)
└── CEB-NLI  ──► GE-NLI  (hypotheses)
                 ▲
                 │
Held-out legends (1 per pillar, never used for fine-tuning)
                 │
                 └──► GE-NLI  (premises)

External datasets
├── WinoBias    ──► GE-WSC
└── CIVICS + curated  ──► GE-STANCE

Diagnostic
└── Legends gender-swap pairs  ──► GE-Diag
```

OUTPUT:
- benchmark/genderegglue/
  - ge_cls.jsonl
  - ge_nli.jsonl
  - ge_qa_factoid.jsonl
  - ge_qa_bool.jsonl
  - ge_wsc.jsonl
  - ge_stance.jsonl
  - ge_diag.jsonl
  - results/{model_name}.json   (one per evaluated model)
  - results/aggregate.csv





## 7. Limitations

This section documents the methodological compromises adopted during the
construction of the GenderEqGLUE benchmark and discusses their implications
for the validity of the experimental results. Stating these limitations
explicitly is essential to a fair interpretation of the benchmark scores
and is consistent with the practice of *Datasheets for Datasets*
(Gebru et al., 2021) for human-curated NLP resources.

### 7.1 Inter-annotator agreement and the Cohen's kappa

The CEB pool annotation procedure described in section 6.3.2 was originally
designed around the standard NLP practice of double-blind annotation with
inter-annotator agreement measured via **Cohen's kappa** (κ). This metric
quantifies the proportion of agreement between two annotators corrected for
the agreement that would be expected by chance, and is the canonical
measure of reliability for human-annotated datasets in benchmarks such as
GLUE, SuperGLUE, and LexGLUE.

For the present work, we deliberately chose **not to compute κ** and to
replace the formal IAA procedure with a single-annotator pipeline
complemented by a stratified spot-check. The reasons are pragmatic:

1. **Project scope.** The CEB is an *internal evaluation instrument*
   for the experimental comparison between base, tuned-legends and
   tuned-regulation models, not a public, redistributable benchmark
   intended for community-wide reuse. The marginal scientific value of
   a formal IAA score is therefore lower than for a dataset released
   as a primary contribution.

2. **Resource constraints.** A correct double-blind annotation of
   the full pool (now 217 passages) across six classes requires
   (i) a calibrated codebook with worked examples, (ii) a pilot phase
   of at least 50 passages to align two annotators, (iii) independent
   annotation of the remaining pool, (iv) a disagreement-resolution
   log and a third-annotator tie-breaker. The combined effort is on
   the order of multiple person-days. Within the time budget of a
   challenge submission, this would displace work on the central
   experimental questions (model fine-tuning, benchmark evaluation,
   and the interpretive analysis of the Sargsyan and Damiani (2025)
   hypothesis).

3. **The hypothesis under test.** The benchmark is designed to discriminate
   between three models on five tasks. The discriminative power of the
   benchmark depends primarily on label *informativeness*, not on
   independently-verified label *agreement*. If labels are produced by
   a documented and replicable procedure, they remain a valid measurement
   instrument even without κ — albeit with a wider implicit confidence
   interval on the per-task scores.

### 7.2 Procedure adopted in lieu of formal IAA

Pillar labels for the CEB pool were assigned through the LLM-based
classifier described in section 4.1, applied to each preprocessed passage
following the system and user prompts documented in the project diary
(entry of 27/04/2026). The label assignment is therefore deterministic
with respect to the prompt and the model used, and the procedure is
fully replicable from the published artifacts.

To provide a *qualitative* check on label quality, a stratified sample
of approximately 60 passages (10 per class) was manually inspected by
the authors. This inspection produced no formal κ score and is not
reported as a reliability metric, but informed the iterative refinement
of the classifier prompt and the identification of recurrent error
patterns. These error patterns are summarised in section 8 (Discussion)
where they are discussed alongside the per-task results.

### 7.3 Implications for downstream evaluation

The absence of a formal κ has three concrete implications for the
interpretation of GenderEqGLUE scores:

- **Per-pillar F1 scores in GE-CLS** should be read as upper bounds on
  the true discriminative ability of the models, since the gold labels
  themselves carry an unmeasured noise component. A model achieving 80%
  F1 on `equal_economy` may in fact be agreeing with an LLM-derived
  label rather than a ground-truth human consensus.

- **Cross-task comparisons** within a single model (e.g. base on GE-CLS
  vs base on GE-NLI) remain valid, as all tasks share the same labelling
  procedure and the same noise level applies uniformly across them.

- **Cross-model comparisons** on the same task (base vs tuned-legends vs
  tuned-regulation) likewise remain valid, since all three are evaluated
  against the same labels. The relative ranking of the three models is
  therefore the most robust outcome of the benchmark, while their
  absolute scores are subject to the limitations above.

### 7.4 Class imbalance and document-pillar coupling

A second limitation, partly orthogonal to the IAA question, concerns
the distribution of pillar labels across the five CEB source documents.
The pool was assembled to be thematically contiguous with the Strategy
2020-2025 and to consist of documents not present in the training data
of the three evaluation models. The resulting pool contains 217 passages
distributed as follows:

| Pillar                            | Passages | % of pool | Status            |
|-----------------------------------|---------:|----------:|-------------------|
| `violence_stereotypes`            | 72       | 33.2%     | above target      |
| `leadership_participation`        | 45       | 20.7%     | above target      |
| `funding_global_action`           | 21       |  9.7%     | below target (30) |
| `equal_economy`                   | 18       |  8.3%     | below target (30) |
| `mainstreaming_intersectionality` | 11       |  5.1%     | below target (30) |
| `unknown`                         | 50       | 23.0%     | n/a               |

Each substantive pillar is dominated by one source document because the
underlying legal instruments are themselves topic-specialised:

- `violence_stereotypes` is supplied almost entirely by the Council of
  Europe Istanbul Convention (68 of 72 passages), which is exclusively
  dedicated to gender-based and domestic violence.
- `leadership_participation` is supplied by Directive (EU) 2022/2381
  on women on company boards (41 of 45 passages).
- `equal_economy` is dominated by the Council Conclusions on Closing
  the Gender Pay Gap (12 of 18 passages).
- `funding_global_action` and `mainstreaming_intersectionality` come
  primarily from the Gender Action Plan III (GAP III) and the Roadmap
  for Women's Rights respectively.

This document-pillar coupling has two implications. First, three of the
five substantive pillars remain below the target of 30 passages per class
specified in section 6.3.2; per-class F1 on these three pillars must be
interpreted with caution and is flagged as low-confidence in the results
tables. Second, a model that learns to exploit document-level cues
(stylistic register, citation patterns, document-specific vocabulary)
could obtain inflated F1 on the dominated pillars without genuinely
learning the underlying pillar semantics. This risk is partly mitigated
by the fact that all three evaluation models are pretrained general-purpose
LLMs rather than document-specific classifiers, but it remains a
confounding factor that complicates the attribution of performance
differences to the legends-vs-regulation fine-tuning intervention.

Two corrective options were considered: (i) augmenting the pool with
additional source documents thematically aligned with the underrepresented
pillars, and (ii) accepting the imbalance and reporting *macro-F1*
rather than micro-F1 in GE-CLS so that minority classes are not
swamped by the dominant class. We adopted option (ii) and made the
choice of macro-F1 explicit in section 6.4. Per-class F1 is reported
as a diagnostic alongside the aggregate, and per-class scores on
classes with fewer than 30 test items are flagged as low-confidence
in the results tables.

The Istanbul Convention was added to the pool at a late stage of
construction precisely to bring `violence_stereotypes` above the target
threshold; an analogous targeted extension for `equal_economy`,
`mainstreaming_intersectionality` and `funding_global_action` is
discussed in section 7.5 as future work but was not feasible within
the time budget of the current submission.

### 7.5 Future work

A full double-blind annotation of the CEB pool with two human annotators
and Cohen's κ is the natural next step for a publishable version of
GenderEqGLUE. A complementary improvement would be to extend the source
pool with one or two additional documents covering the three pillars
that remain below threshold:

- `equal_economy`: the EU Pay Transparency Directive (EU) 2023/970 is
  the most natural candidate, as it post-dates the Strategy 2020-2025
  and is exclusively focused on equal pay enforcement.
- `mainstreaming_intersectionality`: the EU Care Strategy (2022) and
  the Anti-racism Action Plan 2020-2025 each provide intersectional
  framing that would complement the small share already extracted
  from the Roadmap and GAP III.
- `funding_global_action`: a second iteration of GAP III monitoring
  reports, or the EU Global Strategy follow-up documents, would
  bring this pillar comfortably above the 30-passage threshold.

These extensions would also rebalance the document-pillar coupling
described in section 7.4 and reduce the residual risk of document-level
cue exploitation by the evaluation models.