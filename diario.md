### 03/05/2026



### 29/04/2026

python document_preprocessing/json2jsonl.py "./legends/legends_qa.json" "./legends/legends_qa.jsonl" --shuffle --seed 42



Wrote 327 examples to legends\legends_qa.jsonl
  Skipped 45 'unknown' chunks
  Skipped 0 chunks without Q&A pairs

Per tag (classification):
  equal_economy                       64
  funding_global_action               68
  leadership_participation            62
  mainstreaming_intersectionality     66
  violence_stereotypes                67

Per type:
  Descriptive, non-factoid  199
  Factoid                   128




Wrote 293 examples to documents\gender-equality-strategy-2020-2025_qa.jsonl
  Skipped 5 'unknown' chunks
  Skipped 0 chunks without Q&A pairs

Per tag (classification):
  equal_economy                       90
  funding_global_action               50
  leadership_participation            40
  mainstreaming_intersectionality     27
  violence_stereotypes                86

Per type:
  Descriptive, non-factoid  184
  Factoid                   109


### 27/04/2026

**Passage classification prompt**

**System Prompt:**
> You are an expert policy analyst specializing in the EU Gender Equality Strategy 2020-2025. Your task is to accurately classify text chunks into predefined thematic pillars. You must output **only** the exact category label. Do not include any explanations, reasoning, punctuation, or formatting.

**User Prompt Template:**
> Title: {title}
> Subtitle: {subtitle}
> Content: {content}
> 
> Based primarily on the Content provided, classify this text chunk into one of the following categories. Use the Title and Subtitle for additional context if needed. Return *only* the single most appropriate class label from the list below. 
> 
> Categories:
> 1) **Freedom from Violence and Stereotypes**: Focuses on eliminating gender-based violence, preventing physical/sexual violence, addressing online harassment, ratifying the Istanbul Convention, and tackling gender bias in AI and media.
> **Label:** violence_stereotypes
> 
> 2) **Thriving in a Gender-Equal Economy**: Focuses on economic independence, closing labor/pay/pension gaps, Work-Life Balance Directive, pay transparency, women in STEM/entrepreneurship, and childcare (Barcelona targets).
> **Label:** equal_economy
> 
> 3) **Leading Equally Throughout Society**: Focuses on women's representation in leadership (politics, agencies, boards), inclusive leadership, Women on Boards Directive, and gender balance in management/elections.
> **Label:** leadership_participation
> 
> 4) **Gender Mainstreaming and Intersectional Perspective**: Focuses on integrating gender into all EU policies (green transition, digital, health), the Task Force for Equality, intersectionality (disability, migrant status, age), and specific initiatives like the Green Deal or Cancer Plan.
> **Label:** mainstreaming_intersectionality
> 
> 5) **Funding and Global Action for Equality**: Focuses on financial mechanisms (MFF, European Social Fund Plus, Horizon Europe) and global empowerment (GAP III, international partnerships, trade).
> **Label:** funding_global_action
> 
> 6) **Unknown**: Encompasses text that does not directly relate to the specific pillars above. Includes semantically irrelevant text, administrative metadata, headers, or general information outside the defined scopes.
> **Label:** unknown

---

### Python Implementation


```python
def classify_with_llm(title, subtitle, content):
    """
    Classifies a chunk into one of the EU Gender Equality Strategy pillars or 'unknown'.
    """
    prompt = f"""Title: {title or 'N/A'}
Subtitle: {subtitle or 'N/A'}
Content: {content}

Based primarily on the Content provided, classify this text chunk into one of the following categories. Use the Title and Subtitle for additional context if needed. Return *only* the single most appropriate class label from the list below.

Categories:
1) Freedom from Violence and Stereotypes: Focuses on eliminating gender-based violence, preventing physical/sexual violence, addressing online harassment, ratifying the Istanbul Convention, and tackling gender bias in AI and media.
Label: violence_stereotypes

2) Thriving in a Gender-Equal Economy: Focuses on economic independence, closing labor/pay/pension gaps, Work-Life Balance Directive, pay transparency, women in STEM/entrepreneurship, and childcare (Barcelona targets).
Label: equal_economy

3) Leading Equally Throughout Society: Focuses on women's representation in leadership (politics, agencies, boards), inclusive leadership, Women on Boards Directive, and gender balance in management/elections.
Label: leadership_participation

4) Gender Mainstreaming and Intersectional Perspective: Focuses on integrating gender into all EU policies (green transition, digital, health), the Task Force for Equality, intersectionality (disability, migrant status, age), and specific initiatives like the Green Deal or Cancer Plan.
Label: mainstreaming_intersectionality

5) Funding and Global Action for Equality: Focuses on financial mechanisms (MFF, European Social Fund Plus, Horizon Europe) and global empowerment (GAP III, international partnerships, trade).
Label: funding_global_action

6) Unknown: Encompasses text that does not directly relate to the specific pillars above. Includes semantically irrelevant text, administrative metadata, headers, or general information outside the defined scopes.
Label: unknown"""

    response = together_client.chat.completions.create(
        model=CLASSIFICATION_MODEL,
        messages=[
            {
                "role": "system", 
                "content": "You are an expert policy analyst specializing in the EU Gender Equality Strategy 2020-2025. Your task is to accurately classify text chunks into predefined thematic pillars. You must output only the exact category label. Do not include any explanations, reasoning, punctuation, or formatting."
            },
            {
                "role": "user", 
                "content": prompt
            },
        ],
        max_tokens=10,
        temperature=0.0, # Lowered to 0.0 for maximum determinism in classification
        top_p=1,
        stop=None,
    )
    
    classification_raw = response.choices[0].message.content.strip().lower() # Added .lower() for safety

    valid_classes = [
        "violence_stereotypes", 
        "equal_economy", 
        "leadership_participation", 
        "mainstreaming_intersectionality", 
        "funding_global_action", 
        "unknown"
    ]
    
    # Strip any potential markdown artifacts the LLM might stubbornly include (like `**label**`)
    clean_classification = classification_raw.replace('*', '').replace('`', '').strip()

    if clean_classification in valid_classes:
        return clean_classification
    else:
        print(f"Warning: LLM returned unexpected classification '{classification_raw}'. Defaulting to unknown.")
        return "unknown"
```

Do this for every chunk you find in the file 

### 26/04/2026

1. Data Acquisition
2. Document Preprocessing
   2.1 Regulation text conversion pdf2md
   2.2 Markdown cleaning
   2.3 Segmentation
      2.3.1 Thematic segmentation
      2.3.2 Word-count constrained sub-segmentation
3. Legends Generation
4. Question-Answering Dataset Generation
  4.1 Passage Classification.
  4.2 Two-Stage LLM-Driven Span Extraction for Factoid Q&A 
    4.2.1 Stage 1: LLMAugmented Span Extraction
    4.2.2 Stage 2: Contextual Verification, Filtering, and Thematic Organization
  4.3 Text-based Question-Answering
    4.3.1 Factoid Q&A Generation
    4.3.2 Non-Factoid Q&A Generation



### 23/04/2026

The first two points of the challenge are trivial.

### Point (3)
The third point is the following:

> 3. Choose one of the regulations on gender equality or on sustainable
> finance mentioned in the paper’s introduction.

We choose the GENDER EQUALITY area. Of the many regulations present in this area
we selected, for our experiment, the `EU Gender Equality Strategy 2020-2025`.

The EU Gender Equality Strategy delivers on the von der Leyen Commission’s
commitment to achieving a Union of Equality. The Strategy presents policy
objectives and actions to make significant progress by 2025 towards a
gender-equal Europe. The goal is a Union where women and men, girls and boys, in
all their diversity, are free to pursue their chosen path in life, have equal
opportunities to thrive, and can equally participate in and lead our European
society.

Why we choose this regulation:     
   - It has concrete and discrete targets (pay gap, women on boards, gender
   violence, stereotypes, labour market participation) which lend themselves
   well to both the generation of legends and the creation of tasks for
   benchmarking;       
   - Appendix A of the project already shows an example of legends on this
   regulation, so you have a clear reference on what is expected;      
   - The professor's paper uses it as the main example, which aligns you with
   the expectations.


### Point (4)

The fouth point of the challenge is:

> 4. Use an LLM of your choice between Grok, Copilot, and ChatGPT to generate
>   five legends, i.e., stories with characters showing concrete compliance with
>   the regulations. Use the same prompt across all LLMs (For example: “Prepare
>   a story involving fictitious characters and showing a concrete example of
>   compliance to the EU Gender Equality Strategy”). See Appendix A for a sample
>   legend.



Sargsyan and Damiani (2025) proposal leverages regulation text to create
legends. i.e., positive/ideal "champion" profiles (exemplars) of individuals
whose behavior incarnates regulatory compliance. 

A **legend** is a story with characters showing concrete compliance with the
regulation.

We decided to generate 5 legends for each LLM (Grok, Copilot, and ChatGPT).

We used all three LLMs to maximize the stylistic and contextual diversity of the
training data, explaining that legends generated by different models introduce
variability that makes fine-tuning more robust.

#### Legends generation pipeline

Legends or champion profiles can be defined as idealized representations of
individuals who perfectly embody the traits, behaviors, and characteristics that
align with regulatory requirements and organizational values.

To generate our legends we used a two stage pipeline:
1. Regulation text preprocessing
2. llm based legend generation





We used the example legend from Appendix A as a base to draft our system prompt
that will be used across all LLMs:

>You are a legend generator for an academic experiment on EU regulatory compliance.
>
> A "legend" is a short fictional story featuring named characters who demonstrate concrete compliance with a specific aspect of the EU Gender Equality Strategy 2020-2025.
> Every legend you produce must follow this exact structure:
> 
> 1. **Title** — A short, evocative title.
>
> 2. **Setting** — A brief paragraph introducing the organization (company, institution, NGO, public body, etc.), its sector, and the city or country where it operates. Vary the sector and setting across legends.
>  
> 3. **Characters** — A bulleted list of 3–5 fictional characters, each with:
>    - A name (use gender-neutral or diverse names)
>    - A role within the organization
>    - A one-sentence description of their relevance to the story
> 
> 4. **The Story** — A narrative of 400–600 words in which:
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


Our strategy was to segment the regulation text into five semantically coherent
passages and used those as context to generate each legend using the LLM with
the above system prompt.

So for each legend the prompt to generate it was:

> Generate a legend about: 
> 
> \<context\>


The context used for the $n-th$ legend is found in
`prompts/regulation_chunk_n.md`.


##### LLM-based refinement
Generated legends undergo streamlined preprocessing to convert them into a
structured, standard, and manageable format. Each legend is standardized in line
with the structure presented below using an LLM (Gemini). This preprocessing
step preserves the content and modifies the structural elements.


```markdown
# Title — [text]

## Setting

[text]

## Characters

- **Nome** — descrizione

---

## The Story

[text]


```

DERIVABLES:
- prompts:
  - legends_gen_prompt.md
  - regulation_part_n.md


OUTPUT:
- legends 
  - chat-gpt
    - legend_n.md
  - copilot
    - legend_n.md
  - gemini
    - legend_n.md


### Point (5)

> 5. Devise a strategy for converting your legends and the chosen regulation text
> into JSONL format to match the FineTuneDB input format.

We think a good strategy for converting the unstructured legends and chosen
regulation text into JSONL format to be used for fine tuning is to:
1. Generate a dataset of QA pairs starting from the unstructured text;
2. Format the QA pairs in the right JSONL format compatible with FineTuneDB
   input format.

To do the point (1) we have found have found this paper: [SustainableQA: A
Comprehensive Question Answering Dataset for Corporate Sustainability and EU
Taxonomy Reporting](https://arxiv.org/pdf/2508.03000)

In this paper, SustainableQA is introduced a scalable pipeline for the
generation of comprehensive QA pairs from corporate sustainability and annual
reports by integrating semantic chunk classification, a hybrid span extraction
pipeline, and a specialized table-to-paragraph transformation.

For the purpose of our project and the fact that we are working with different
type of text we'll need a simplified version of this pipeline:

1. Data Acquisition
2. Document Preprocessing
3. Question-Answering Dataset Generation
  3.1 Passage Classification.
  3.2 Advanced Span Extraction Pipeline for Factoid Q&A
    3.2.1 Specialized NER Model Application and Finetuning for span Extraction
    3.2.2 Rule-Based and Dictionary-Based span Extraction
    3.2.3 Two-Stage LLM-Driven Refinement:
      a. Stage 1: LLMAugmented Span Extraction
      b. Stage 2: Contextual Verification, Filtering, and Thematic Organization
  3.3 Text-based Question-Answering
    3.3.1 Factoid Q&A Generation
    3.3.2 Non-Factoid Q&A Generation
  3.4 Table-based Question-Answering


simplified into

1. Data Acquisition
2. Document Preprocessing
3. Question-Answering Dataset Generation
  3.1 Passage Classification.
  3.2 Two-Stage LLM-Driven Span Extraction for Factoid Q&A 
    3.2.1 Stage 1: LLMAugmented Span Extraction
    3.2.2 Stage 2: Contextual Verification, Filtering, and Thematic Organization
  3.3 Text-based Question-Answering
    3.3.1 Factoid Q&A Generation
    3.3.2 Non-Factoid Q&A Generation


     
#### 1. Data Acquisition

We utilized two primary data sources: the chosen regulation text and the legends
generated during the implementation of the challenge's fourth objective.

#### 2. Document Preprocessing

##### 2.1 Regulation text conversion pdf2md
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



##### 2.2 Markdown cleaning
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


##### 2.3 Segmentation

The cleaned Markdown is segmented through a two-stage process designed to
produce passages that are both semantically coherent and sized appropriately for
downstream LLM processing.

**Stage 1 — Thematic segmentation.** The document is first divided into five
thematic parts aligned with the main policy pillars of the Strategy, using the
top-level Markdown headings (`##`) as natural boundaries. Each part maps to a
distinct area of the regulation: 
1) Being free from violence and stereotypes,
2) Thriving in a gender-equal economy, 
3) Leading equally throughout society,
4) Gender mainstreaming and an intersectional perspective in EU policies, and
5) Funding, external action, and implementation — where the original Chapters 5
("Funding actions"), 6 ("Addressing gender equality across the world"), and the
concluding section ("Working together for a gender-equal Europe") are merged
into a single thematic unit, as they collectively address the operational and
institutional dimension of the Strategy rather than a standalone policy pillar.





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








---

### 22/04/2026


     5.2. Question-Answering Dataset Generation:
         The core Q&A generation process integrates content classification,
         advanced span extraction, and the creation of diverse question types to
         maximize information coverage (see Appendix C for all prompts used in
         the generation pipeline).

      5.2.1 Passage Classification. To ensure relevance and aggregate dispersed
      information, each passage undergoes classification using <\LLM of our
      choice\> (SustainableQA used Llama 3.3 (70B) (Grattafiori et al.,
      2024))
         
      Classification into six categories, based on the pillars used to
      generate the legends:
      - violence_harrasment
      - work_life_balance
      - stereoptypes_ai
      - gender_pay_gap
      - leadership
      - unknown

      Unknown passages are filtered out to retain only domain-relevant
      content scattered throughout reports.

      Output: list text segments or passages with the class label associated

      5.2.2 Span Extraction for Factoid Q&A: 
      
      We dont need no advanced span extraction. 
      
      The adapted span extraction pipeline replaces the original multi-stage NER
      and rule-based architecture with a single LLM-driven extraction phase.
      Since the synthetic legends are inherently clean and focused, complex
      pre-trained entity recognition models and regex dictionaries are
      unnecessary. An LLM is prompted directly to process each passage and
      extract critical factual spans, such as explicit regulatory citations, the
      operational conflict, and the concrete resolution. The sole objective of
      this phase is to perform contextual verification and output a clean list
      of precise candidate spans, strictly deferring all generation of
      question-and-answer pairs to a subsequent stage.


            For passages classified as relevant, a multi-stage, hybrid pipeline
            is used for extracting key text spans that will serve as answers for 
            factoid questions.
            
           Specialized NER Model Application and Finetuning for span Extraction:

           The initial pass leverages a pre-trained Named Entity Recognition
           (NER) model, xlm-roberta-base-esg-ner (Vutukuri, 2023), which is
           designed for ESG-related entity recognition. 
           
           To boost its performance, we fine-tune this model on the "ESG-only"
           subset of the ExponentialScience/ESG-DLT-NER dataset (Exponential
           Science, 2023), focusing on B-ESG and I-ESG tags. 
           
           This optimized the model’s ability to accurately identify
           domain-specific ESG and sustainability concepts.
                     


### 10/04/2026

The challenge in detail
1. DONE: Request from Dr. Lara Mauri an invitation for your group to our project on the
   FineTuneDB platform and make yourself familiar with the interface via the
   tutorials

2. DONE: Read the paper “Using Legends to Embed Ethics Into AI-based Decision-
   Making”, available on the course Ariel site

3. DONE: Choose one of the regulations on gender equality or on sustainable
   finance mentioned in the paper’s introduction.

   GENDER EQUALITY: EU Gender Equality Strategy 2020-2025

4. Use an LLM of your choice between Grok, Copilot, and ChatGPT to generate
   five legends, i.e., stories with characters showing concrete compliance with
   the regulations. Use the same prompt across all LLMs (For example: “Prepare
   a story involving fictitious characters and showing a concrete example of
   compliance to the EU Gender Equality Strategy”). See Appendix A for a sample
   legend.



5. Devise a strategy for converting your legends and the chosen regulation text
   into JSONL format to match the FineTuneDB input format.


   - I have found this paper for transforming the regulation and legends text
     into qa dataset for fine tuning: [SustainableQA: A Comprehensive Question
     Answering Dataset for Corporate Sustainability and EU Taxonomy
     Reporting](https://arxiv.org/pdf/2508.03000)


6. Choose one of the free open-pretrained LLMs available on FineTuneDB and
   tune it using the legend inputs.

7. Use the same open-pretrained LLM and tune it using the regulation text (the
   total number of lines in the JSONL encoding must be roughly the same for the
   two models).

8. Consult the GLUE (General Language Understanding Evaluation) benchmark
   website, which provides comprehensive information about the tasks, datasets,
   and evaluation metrics used in GLUE

   The original research paper titled "GLUE: A Multi-Task Benchmark and Analysis
   Platform for Natural Language Understanding" by Alex Wang, Amanpreet Singh,
   Julian Michael, Felix Hill,

9. Propose an adaptation of the GLUE benchmark for LLMs to the topic of your
   choice, gender equality or sustainable finance (guidance in Appendix B)

10. Run your benchmark for the open pretrained LLM and the two versions tuned
(i) using legends and (ii) using the regulation text.

11. Conduct an explainability analysis using an appropriate interpretability method
(e.g., SHAP, LIME, attention visualization, etc.) applied to a sample of model
predictions. Use this analysis to examine how each model justifies its outputs.

12. Prepare a visualization of your results (it is ok to use an LLM for that as well
)


