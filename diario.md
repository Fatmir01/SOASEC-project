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

   Regolamentazione: EU Gender Equality Strategy 2020-2025 Te la confermo come
   scelta migliore per questi motivi:
   - Ha obiettivi concreti e discreti (pay gap, women on boards, violenza di
   genere, stereotipi, partecipazione al mercato del lavoro) che si prestano
   bene sia alla generazione di legends sia alla creazione di task per il
   benchmark.
   - L'Appendix A del progetto mostra già un esempio di legend su questa
   regolamentazione, quindi hai un riferimento chiaro su cosa ci si aspetta.
   - Il paper del professore la usa come esempio principale, il che ti allinea
   con le aspettative.


   Esiste anche la EU Gender Equality Strategy 2026-2030: aggiornare o usare
   quella vecchia??

4. Use an LLM of your choice between Grok, Copilot, and ChatGPT to generate
   five legends, i.e., stories with characters showing concrete compliance with
   the regulations. Use the same prompt across all LLMs (For example: “Prepare
   a story involving fictitious characters and showing a concrete example of
   compliance to the EU Gender Equality Strategy”). See Appendix A for a sample
   legend.

   - Abbiamo deciso di generare 15 leggende, 5 per ogni LLM: all'orale possiamo
   dire che abbiamo sfruttato tutti e tre gli LLM per massimizzare la diversità
   stilistica e contestuale dei dati di training, spiegando che leggende
   generate da modelli diversi introducono variabilità che rende il fine-tuning
   più robusto.

   - Abbiamo introdotto un passaggio di quality check per eliminare eventuali
   leggende troppo simili tra loro (ad esempio se due LLM hanno prodotto storie
   quasi identiche sullo stesso pilastro). 
   
   Claude: Da quello che ho letto, le 15 sono sufficientemente diverse — stessi
   temi ma contesti, personaggi e soluzioni differenti.

   Faccio l'analisi e poi creo il file corretto. Ecco cosa ho trovato:
   Problemi individuati:

   - Copilot Legend 2 cita la "Employment Equality Directive (2000/78/EC)" — è
   sbagliato. Quella direttiva copre discriminazione per religione, disabilità,
   età, orientamento sessuale, ma non il genere. Va sostituita con la Direttiva
   2006/54/CE. 
   
   - Copilot Legend 4 è ambientata in Svizzera. La Svizzera non è membro
   UE — è debole come esempio di compliance EU anche con la nota "operating across
   the EU." Cambio il paese. 
   
   - Pillar 2 (AI/stereotipi): le 3 leggende sono le più
   simili tra loro (tutte: AI screening CV → bias → audit → fix). Sono comunque
   sufficientemente diverse per contesto e soluzioni, quindi le tengo, ma rafforzo
   le differenze. 
   
   - Alcune leggende di ChatGPT hanno riferimenti normativi troppo
   vaghi — aggiungo i riferimenti precisi alla Strategy (sezione e pagina).

   - Uniformo il formato di tutte e 15 (stessa struttura, stessi heading).




5. Devise a strategy for converting your legends and the chosen regulation text
   into JSONL format to match the FineTuneDB input format.


   - I have found this paper for transforming the regulation and legends text
     into qa dataset for fine tuning: [SustainableQA: A Comprehensive Question
     Answering Dataset for Corporate Sustainability and EU Taxonomy
     Reporting](https://arxiv.org/pdf/2508.03000)

   SustainableQA dataset generation pipeline adattata al nostro caso specifico:

   - Data acquisition: sostituita dai punti precedenti di generazione delle
     leggende e il testo della regolamentazione già disponibile.

   - Document preprocessing:  Raw PDF reports undergo streamlined preprocessing
      to convert them into a structured, clean, and manageable format. 

      1. The regulation's PDF is first transformed into Markdown text using the
      Marker library (Paruchuri, 2024), which preserves structural elements. 

      [Marker library (Paruchuri, 2024)](https://github.com/datalab-to/marker)

      Input: file della regolamentaione in PDF 
         `gender-equality-strategy-2026-2030.pdf`

      Process: script che usa marker library per trasformare questo file in md
         `document_preprocessing\pre_processing.py`

      Output: gender-equality-strategy-2026-2030.md
         `documents\pre_processing_output\gender-equality-strategy-2020-2025.md`


      2. The Markdown is then cleaned to remove non-substantive elements such as
      footnotes, images, and page markers, while consolidating blank lines and
      removing empty heading sections.

         - Post-processing sul file Markdown generato tramite regole regex.

         Cleaning: ./gender-equality-strategy-2020-2025.md
         Original: 64723 chars
         Cleaned:  64188 chars
         Reduction: 0.8%

         `documents\gender-equality-strategy-2020-2025_cleaned.md`

      3. Finally, the cleaned text is segmented into semantically coherent
      passages based on markdown headings, with a word-count constraint (e.g.,
      max_words=350) applied to ensure each passage remains within an optimal
      context window for subsequent LLM-based processing. 

         - Questa fase si basa su una segmentazione basata sugli heading con
           vincolo di max parole.

            Total passages: 42
            Word counts: min=5, max=348, avg=202

         - (mettiamo il codice della funzione python della segmentazione?)

            

      Note: SustainableQA prevedeva una diversa gestione delle tabelle cosa a
      noi non utile in quanto ne il testo della regolamentazione ne quello delle
      leggende ne contiene.


   - Q&N dataset generation:


     - FASE 1 — Content Classification (equivalente a SustainableQA §3.3) Ogni
      leggenda è stata classificata per pillar della Strategy usando keyword matching.
      Risultato: 3 legends per ciascuno dei 5 pilastri, nessun contenuto "Unknown"
      scartato. Tutte le regolamentazioni citate sono state identificate
      automaticamente. All'orale: "Ho classificato ogni leggenda per pillar tematico
      per garantire copertura completa della Strategy e per taggare ogni coppia Q&A
      con il suo dominio normativo."


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