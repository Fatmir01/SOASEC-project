
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


TODO: give names to the thematic clusters

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