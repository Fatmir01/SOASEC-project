### 10/04/2026

The challenge in detail
1. DONE: Request from Dr. Lara Mauri an invitation for your group to our project on the
   FineTuneDB platform and make yourself familiar with the interface via the
   tutorials


2. DONE: Read the paper “Using Legends to Embed Ethics Into AI-based Decision-
   Making”, available on the course Ariel site

3. DONE: Choose one of the regulations on gender equality or on sustainable
   finance mentioned in the paper’s introduction.

   GENDER EQUALITY

4. Use an LLM of your choice between Grok, Copilot, and ChatGPT to generate
   five legends, i.e., stories with characters showing concrete compliance with
   the regulations. Use the same prompt across all LLMs (For example: “Prepare
   a story involving fictitious characters and showing a concrete example of
   compliance to the EU Gender Equality Strategy”). See Appendix A for a sample
   legend.

5. Devise a strategy for converting your legends and the chosen regulation text
   into JSONL format to match the FineTuneDB input format.

   - I have found this paper for transforming the regulation text into qa dataset
     for fine tuning: [SustainableQA: A Comprehensive Question Answering Dataset
     for Corporate Sustainability and EU Taxonomy
     Reporting](https://arxiv.org/pdf/2508.03000)
   
   - How I transform the legends in QA dataset??
     I think the same strategy applies.


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






### 11/02/2026

# Diario di Progetto: SOASEC

**Autori:** Fatmir Bylyshi, Ilyass Ouardi
**Data:** 10 Febbraio 2026
**Progetto:** The Legend Challenge - Embedding Ethics into AI


## 1. Introduzione: Il Paradosso della Compliance nell'IA

L'obiettivo di questo progetto nasce dalla necessità critica, evidenziata nel paper *"Using Legends to Embed Ethics Into AI-based Decision-Making"*, di superare l'approccio reattivo alla regolamentazione aziendale. Le grandi organizzazioni si trovano oggi a dover navigare un panorama normativo complesso (es. CSRD, EU Taxonomy), spesso caratterizzato da un conflitto intrinseco: la pressione per l'ottimizzazione dei costi e la massimizzazione del profitto contro la necessità di aderire a stringenti requisiti etici e sociali.

Attualmente, l'integrazione di queste norme nei processi decisionali automatizzati (IA) avviene spesso tramite audit "post-hoc", un metodo che si rivela costoso e tardivo. La nostra sfida è dimostrare la validità dell'approccio proposto dagli autori: l'iniezione proattiva di etica nei modelli tramite l'uso di "Leggende" (Champions), ovvero esempi sintetici positivi che guidino il modello verso decisioni *compliant by design*.

### 1.1 Selezione del Dominio: Perché la Gender Equality?

Sebbene il paper presenti due domini di applicazione (Finanza Sostenibile e Parità di Genere), la scelta di focalizzare il progetto sulla **Gender Equality** è dettata da motivazioni tecniche e critiche:

1. **Sfida Semantica:** A differenza della finanza (spesso quantitativa), la parità di genere richiede al modello di interpretare sfumature linguistiche e bias impliciti, rappresentando un banco di prova superiore per la comprensione del linguaggio naturale (NLU).
2. **Focus Operativo:** Il paper identifica i processi di HR come l'area più critica dove l'ottimizzazione algoritmica dei costi entra in conflitto con l'etica.
3. **Complessità Normativa:** L'intreccio di direttive sovrapposte (Pay Transparency, Women on Boards) richiede un ragionamento articolato, ideale per testare la nostra strategia basata su "Leggende".



## 2. Strategia di Prompt Engineering: Genesi delle "Leggende"

La prima fase operativa ha riguardato la definizione del **Prompt** per la generazione del dataset sintetico. Abbiamo adottato un processo iterativo per ingegnerizzare un prompt che rispondesse alle criticità del paper, evolvendo l'esempio base fornito nell'Appendix A.

Di seguito, analizziamo le quattro scelte architetturali che hanno plasmato il nostro prompt definitivo.

### A. Verticalità vs. Generalizzazione

Il primo dubbio progettuale riguardava lo spettro degli argomenti: creare storie che toccano tutti i temi genericamente (come nell'esempio base) o focalizzarsi su singoli aspetti?
**Decisione:** Abbiamo optato per la **Verticalità Assoluta**. Ogni leggenda è dedicata a un singolo pilastro normativo (es. *Solo Pay Gap*, *Solo Women on Boards*).
*Motivazione:* Un approccio generalista rischia di produrre risultati "piatti". Focalizzandosi su un tema alla volta, il modello apprende regole decisionali precise e distinte, aumentando la "risoluzione" dell'addestramento etico.

### B. Dal Conflitto alla "Riflessione Interiore Proattiva"

Come rappresentare il momento decisionale? Inizialmente avevamo considerato uno scontro tra personaggi (Dilemma Esterno), ma questo si discostava troppo dallo stile positivo delle "Leggende" descritte nel paper.
**Decisione:** Abbiamo scelto la via della **Riflessione Interiore (Internal Reflection)**.
*Motivazione:* Il protagonista non deve litigare, ma dimostrare leadership. Di fronte a una pressione operativa (es. fretta o budget), il manager si ferma e riflette autonomamente. Questo approccio insegna al modello la *proattività*: la compliance non è imposta da fuori, ma nasce dal ragionamento del decisore.

### C. Specificità Tecnica nel Ragionamento (Textbook Quality)

Per garantire un voto eccellente e superare la qualità dell'esempio standard, abbiamo introdotto un vincolo di densità informativa.
**Decisione:** Obbligo di citazione normativa esplicita all'interno della narrazione.
*Motivazione:* Non basta che il manager pensi "dobbiamo essere giusti". Nel prompt imponiamo che il protagonista citi mentalmente la **Direttiva Specifica** (es. *Direttiva UE 2023/970*). Questo trasforma la storia da semplice narrativa a dato di addestramento ad alta densità (sul modello di *Gunasekar et al., 2023 - Textbooks Are All You Need*), permettendo al modello di associare il contesto operativo alla legge esatta.

### D. Il Protagonista: Focus sul Middle Management

Chi prende le decisioni?
**Decisione:** I protagonisti sono **Middle Manager operativi** (HR, Team Lead), non CEO.
*Motivazione:* Il paper identifica il middle management come il punto di rottura dove l'implementazione etica fallisce a favore del profitto. Addestrare l'IA su questi ruoli significa intervenire alla radice del problema.

---

## 3. Il Prompt Definitivo

Sulla base delle decisioni sopra riportate, ecco il prompt finale utilizzato per la generazione del dataset. Notare come la struttura riprenda visivamente l'Appendix A (Intro, Personaggi, Storia) per coerenza col corso, ma ne potenzi drasticamente il contenuto logico.

**RUOLO:**
Agisci come un **Senior AI Data Specialist** ed esperto in **Compliance Normativa UE** (Gender Equality).

**OBIETTIVO:**
Generare "Leggende" (storie esemplari) di alta qualità per il fine-tuning di un modello AI. Le storie devono insegnare come risolvere il conflitto tra **pressione economica** e **compliance etica**.

**FORMATO RICHIESTO:**
Ogni volta che ti invierò un **Titolo**, dovrai generare una storia seguendo rigorosamente questa struttura (basata sull'esempio "Appendix A"):
1. **Titolo:** (Usa il titolo fornito).
2. **Introduzione:** Un breve paragrafo (2-3 righe) che descrive l'azienda e il contesto di pressione (scadenze, budget, tagli).
3. **Personaggi:** Un elenco puntato dei personaggi. Il protagonista DEVE essere un **Middle Manager operativo** (es. HR Manager, Team Lead).
4. **La Storia:** Il corpo narrativo principale.

**REGOLE FONDAMENTALI PER LA SEZIONE "LA STORIA":**
Anche se è un testo narrativo fluido, deve contenere questi elementi logici integrati nella narrazione:
* **Il Conflitto:** Il protagonista si trova davanti a una scelta: risparmiare soldi/tempo subito (via facile) o seguire la norma UE (via etica).
* **Il Momento di Riflessione (Cruciale):** Devi descrivere un momento in cui il protagonista *pensa* o *discute* la decisione. In questo passaggio, il protagonista deve citare esplicitamente il principio normativo (es. *Direttiva sulla Trasparenza Retributiva*, *Gender Equality Strategy*) come motivo tecnico per rifiutare la scorciatoia economica.
* **L'Azione:** La storia si conclude con l'implementazione della decisione etica e un risultato positivo concreto.

**STILE:**
Narrativo, realistico, aziendale. Non usare intestazioni o bullet point dentro la sezione "La Storia".

**ATTENZIONE:**
Non generare nulla adesso. Rispondimi semplicemente con: *"Configurazione ricevuta. In attesa del primo titolo."*