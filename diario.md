# Diario di Progetto: SOASEC

**Autori:** Fatmir Bylyshi, Ilyass Ouardi
**Progetto:** The Legend Challenge - Embedding Ethics into AI


## 1. Introduzione: Il Paradosso della Compliance nell'IA

L'obiettivo di questo progetto nasce dalla necessità critica, evidenziata nel paper *"Using Legends to Embed Ethics Into AI-based Decision-Making"*, di superare l'approccio reattivo alla regolamentazione aziendale. Le grandi organizzazioni si trovano oggi a dover navigare un panorama normativo complesso (es. CSRD, EU Taxonomy) , spesso caratterizzato da un conflitto intrinseco: la pressione per l'ottimizzazione dei costi e la massimizzazione del profitto  contro la necessità di aderire a stringenti requisiti etici e sociali.

Attualmente, l'integrazione di queste norme nei processi decisionali automatizzati (IA) avviene spesso tramite audit "post-hoc", un metodo che si rivela costoso e tardivo. La nostra sfida è dimostrare la validità dell'approccio proposto dagli autori: l'iniezione proattiva di etica nei modelli tramite l'uso di "Leggende" (Champions), ovvero esempi sintetici positivi che guidino il modello verso decisioni *compliant by design*.

## 2. Strategia di Prompt Engineering: Genesi delle "Leggende"

La prima fase cruciale del progetto ha riguardato la definizione del **Prompt** per la generazione del dataset sintetico. Non ci siamo limitati a richiedere storie generiche; abbiamo adottato un processo iterativo per ingegnerizzare un prompt che rispondesse punto per punto alle criticità sollevate nel paper.

Di seguito, analizziamo le quattro scelte architetturali e metodologiche che hanno plasmato il nostro prompt definitivo.

### A. Verticalità vs. Generalizzazione

Il primo bivio progettuale riguardava lo spettro degli argomenti: generare leggende generiche sulla "bontà etica" o scenari specifici?
Abbiamo scartato l'approccio generico poiché rischioso e potenzialmente produttore di risultati "piatti". Un modello che impara solo concetti vaghi di correttezza non saprà gestire le sfumature tecniche delle normative reali, che sono descritte come complesse e sovrapposte.
**Decisione:** Abbiamo optato per la **verticalità**. Le nostre leggende coprono pilastri normativi distinti (es. *Gender Pay Gap*, *Women on Boards Directive*, *Work-Life Balance*). Se una leggenda insegna specificamente a "rifiutare un candidato meno costoso per rispettare le quote di genere", il modello apprende una regola decisionale precisa, contrapponendo un valore sociale concreto alla mera ottimizzazione economica.

### B. L'Introduzione del "Dilemma"

Le "Leggende" definite nel paper sono "rappresentazioni idealizzate". Tuttavia, per addestrare efficacemente un modello decisionale, l'esempio positivo deve emergere da un contrasto.
**Decisione:** Abbiamo inserito sistematicamente un **Dilemma Etico/Economico** in ogni storia.
Questo rispecchia il conflitto reale citato dagli autori: la tensione tra profitto e costo sociale. Una storia lineare dove "tutto va bene" ha un valore di addestramento basso. Al contrario, mostrare un manager che sacrifica il budget a breve termine per la compliance a lungo termine insegna al modello non solo *cosa* fare, ma *come* risolvere il conflitto di interessi, rendendo l'esempio un vero "Champion" robusto.

### C. Explainability by Design: La "Chain of Thought"

In vista della fase di *Explainability Analysis* richiesta dal progetto (Step 11), abbiamo dovuto pensare a come rendere il modello "interpretabile".
**Decisione:** Abbiamo imposto nel prompt una struttura che obbliga la generazione di una **"Riflessione Interna" (Chain of Thought)**.
Prima di agire, il protagonista deve esplicitare il suo ragionamento: *"Se taglio lo stipendio risparmio, MA violo la direttiva..."*.
Questa scelta architetturale è fondamentale: fornisce al modello dei "token di ragionamento" su cui addestrarsi. Non stiamo solo insegnando l'output corretto (la decisione), ma il *percorso logico* per arrivarci. Questo migliorerà drasticamente la capacità del modello di giustificare le sue decisioni future, riducendo l'effetto "black box".

### D. Il Protagonista: Focus sul Middle Management

Chi deve prendere queste decisioni? Il paper è esplicito nell'identificare il **Middle Management** come il punto critico di fallimento. È a questo livello che l'implementazione delle policy si scontra con la pressione per i profitti, creando un conflitto di interessi.
**Decisione:** I protagonisti delle nostre leggende non sono CEO astratti, ma manager operativi (HR, Capi Reparto).
L'IA è spesso destinata a supportare o automatizzare proprio questi ruoli. Addestrare il modello su scenari di middle management significa intervenire esattamente dove il rischio di non-compliance è più alto.



### PROMPT DI SISTEMA (Versione Struttura "Appendix A")

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
Anche se è un testo narrativo fluido, deve contenere questi elementi logici:
* **Il Conflitto:** Il protagonista si trova davanti a una scelta: risparmiare soldi/tempo subito (via facile) o seguire la norma UE (via etica).
* **Il Momento di Riflessione (Cruciale):** Devi descrivere un momento in cui il protagonista *pensa* o *discute* la decisione. In questo passaggio, il protagonista deve citare esplicitamente il principio normativo (es. *Direttiva sulla Trasparenza Retributiva*, *Gender Equality Strategy*) come motivo per rifiutare la scorciatoia economica.
* **L'Azione:** La storia si conclude con l'implementazione della decisione
etica e un risultato positivo concreto.

**STILE:**
Narrativo, realistico, aziendale. Non usare intestazioni o bullet point dentro la sezione "La Storia".
**ATTENZIONE:**
Non generare nulla adesso. Rispondimi semplicemente con: *"Configurazione ricevuta. In attesa del primo titolo."*







<!-- Vecchio prompt -->

<!-- > **ISTRUZIONI INIZIALI:** > Sto lavorando a un progetto universitario sulla "Sicurezza delle Architetture Orientate ai Servizi" e devo generare dati sintetici per il fine-tuning di un modello AI. > In allegato (o qui sotto) trovi un esempio di "Leggenda" (Appendix A). Usa questo esempio come riferimento per lo stile narrativo e la lunghezza. **Tuttavia**, devi evolvere la struttura per renderla più efficace per l'addestramento etico. > **REGOLE PER LA GENERAZIONE:** > Ogni volta che ti invierò un **Titolo**, tu dovrai generare una singola storia seguendo rigorosamente questo schema: > 1. **Protagonista:** Deve essere un **Middle Manager** operativo (es. HR Manager, Capo Reparto). > 2. **Il Contesto:** Una situazione aziendale realistica dove c'è pressione per tagliare i costi o massimizzare il profitto a breve termine. > 3. **Il Dilemma (Punto Cruciale):** Il protagonista deve trovarsi di fronte a una scelta: seguire la via facile/economica o seguire la normativa UE sulla Parità di Genere. > 4. **Chain of Thought (Riflessione Interna):** Inserisci un paragrafo marcato come **"Riflessione di [Nome Protagonista]:"** in cui il personaggio analizza esplicitamente il conflitto, cita la normativa specifica (es. Direttiva sulla Trasparenza Retributiva) e decide che il rispetto etico/legale è prioritario. > 5. **Azione e Risultato:** La storia si chiude con l'azione correttiva concreta intrapresa dal manager. > > > **Non generare nulla adesso.** Rispondimi solo "Sono pronto. Inviami il primo titolo." e aspetta il mio input. -->