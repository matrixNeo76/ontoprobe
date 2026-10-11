---
okf_version: "0.2"
document_id: "OKF-DOC-2026-ONTO-THEORY-001"
title: "Research Framework: Indagine, Misurazione e Mitigazione dei Limiti dell'Innovazione Ontologica negli LLM"
framework_version: "v0.3.1"
date: "2026-10-11"
status: "Operational Research Framework (Patch v0.3.1)"
domain: "Mechanistic Interpretability, Epistemology of AI, Multi-Agent Systems"
authors:
  - name: "Ricercatore Indipendente"
    role: "Principal Investigator / Lead Architect"
    license: "CC BY 4.0"
companion_documents:
  - id: "OKF-DOC-2026-ONTO-IMPL-001"
    title: "Guida all'Implementazione Computazionale e Architettura Low-Spec per ONTO-PROBE"
    file: "IMPL-001.md"
  - id: "OKF-DOC-2026-ONTO-BENCH-001"
    title: "Catalogo dei Task e Specifiche del Benchmark O-Novel v0.1"
    file: "BENCH-001.md"
  - id: "OKF-DOC-2026-ONTO-EVAL-001"
    title: "Protocollo Sperimentale e Human Evaluation Runbook"
    file: "EVAL-001.md"
  - id: "OKF-DOC-2026-ONTO-META-001"
    title: "Valutazione della Suite Documentale e Mappatura dei Gap Operativi per ONTO-PROBE"
    file: "META-001.md"
---

# OKF v0.2 — Research Framework: Innovazione Ontologica negli LLM (v0.3.1)

> **Allineamento di Sistema:** Il presente documento costituisce il pilastro teorico-epistemologico della suite **ONTO-PROBE v0.3.1**. Redatto nello standard **Google Open Knowledge Format (OKF) v0.2**, stabilisce i fondamenti della chiusura rappresentazionale degli LLM, le modalità di mitigazione via isolamento informativo e le condizioni di falsificabilità sperimentale.

---

## 0. Changelog del Framework di Ricerca

### 0.1 Transizione da v0.1 a v0.2 (Fondazione Concettuale)
- Formulazione iniziale dell'architettura multi-agente **ONTO-PROBE**.
- Definizione del benchmark di novità **O-Novel** e DMP iniziale.

### 0.2 Transizione da v0.2 a v0.2.1 (Riformulazione Epistemologica)
- Riconfigurazione in chiave falsificazionista dei confini dell'apprendimento statistico.
- Sostituzione della soglia scalare con gating multi-criterio di validità funzionale.

### 0.3 Transizione da v0.2.1 a v0.3.0 (Chiusura dei Gap Metodologici)
- Ridenominazione in *No New Basis Principle* (congettura empirico-strutturale).
- Formalizzazione canonica di Contrastive Activation Addition (CAA).
- Power Analysis ANOVA per effetto moderato ($f = 0.25$, $N \ge 159$ per potenza 0.80; campione pianificato $N = 165\text{--}180$).
- Introduzione del protocollo multi-embedder contro distorsioni OOD.

### 0.4 Release v0.3.1 (Rifinitura Operativa e Blinding)
- **HMAC-Blinding:** Separazione crittografica unidirezionale tra identificatore interno e ID cieco pubblico.
- **Safety Triad:** Inclusione formalizzata della manipolazione cognitiva accanto ai rischi CBRN e cyber-exploit.
- **Risoluzione Bug Runtime:** Correzione dei ruoli nei messaggi API e protezione degli steering vector da input vuoti.

---

## 1. Sintesi Esecutiva (L1 — Synthesis Layer)

### 1.1 Scopo del Programma Scientifico

Questo programma di ricerca indaga se e in quale misura i Large Language Model (LLM) possano generare **innovazione ontologica autentica** ($O\text{-novelty}$), ovvero strutture causali, relazioni esplicative e predicati non riducibili per interpolazione o omomorfismo al convesso dei pattern assorbiti durante il pre-training.

L'infrastruttura assume una postura **falsificazionista**: se la chiusura geometrica dell'architettura transformer è invalicabile, il protocollo misura empiricamente la massima distanza raggiungibile prima della degenerazione sintattica, documentando i limiti operativi delle reti neurali autoregressive.

### 1.2 Domanda di Ricerca Fondamentale

> Gli LLM attuali possono generare innovazione ontologica autentica — definita come l'introduzione di relazioni causali non mappabili per omomorfismo diretto sul database degli archetipi consolidati — o operano necessariamente entro una chiusura concettuale fissa?
>
> **Sotto-domanda operativa:** Qualora il *No New Basis Principle* imponga un limite strutturale invalicabile, quali condizioni al contorno (isolamento informativo asimmetrico, activation steering ortogonale, validazione avversariale) massimizzano la divergenza preservando la validità funzionale, e come si distingue tale divergenza dal puro collasso allucinatorio?

### 1.3 Stato dell'Arte e Fondamento Empirico

Ricerche empiriche recenti (Matarmaa 2026) su sette modelli di frontiera ($N = 168$ proposte analizzate) evidenziano un tasso di novità ontologica stretta nullo:

$$\hat{p} = 0/168 = 0.000 \quad (\text{limite superiore unilaterale al } 95\%\text{: } \approx 0.018, \text{ regola del tre; Clopper–Pearson bilaterale: } \approx 0.022)$$

*(Con zero successi l'intervallo di confidenza non è degenere: il valore osservato è compatibile con tassi reali fino a circa 2%. Gli intervalli qui riportati sono ricalcolati dal solo conteggio $0/168$, non tratti dalla fonte.)*

Il $98.2\%$ delle risposte è risultato riconducibile a ontologie preesistenti, collocandosi interamente entro il *convex hull* dei dati di pre-training. Le tre categorie principali, che sommano $82.7\%$, sono:
- **Range Extension** ($20.2\%$): estrapolazione quantitativa o scalare di categorie note.
- **Hybrid Combination** ($44.6\%$): fusione chimerica di concetti discreti preesistenti.
- **Functional Recombination** ($17.9\%$): riassegnazione di funzioni ordinarie a contesti superficialmente eterogenei.

Il residuo ($98.2\% - 82.7\% = 15.5\%$) è attribuito dalla fonte ad altre forme di riconducibilità non dettagliate in questo documento; la ripartizione completa va verificata sul testo originale di Matarmaa 2026.

Tale evidenza corrobora il **No New Basis Principle**: la discesa del gradiente su un vocabolario discreto fisso $\mathcal{V}$ non può generare dimensioni semantiche ortogonali non espresse nel corpus di pre-training.

---

## 2. Ingegneria dei Sistemi ed Epistemologia (L2 — Analysis Layer)

### 2.1 Tassonomia dei Limiti Epistemici

```
┌────────────────────────────────────────────────────────────────────────┐
│                    LIVELLI DI LIMITAZIONE EPISTEMICA                   │
├────────────────────────────────────────────────────────────────────────┤
│ 1. RAPPRESENTAZIONALE: Chiusura geometrica del convex hull di training │
│ 2. MECCANICO:          Collasso della diversità nei loop multi-agente  │
│ 3. VALUTATIVO:         Distorsione ed effetto OOD negli embedder       │
│ 4. FUNZIONALE:         Trade-off tra divergenza concettuale e coerenza │
│ 5. OPERATIVO:          Saturazione del carico degli esperti umani (L3) │
└────────────────────────────────────────────────────────────────────────┘
```

| Livello | Meccanismo di Limite | Manifestazione Fenomenica | Strategia di Mitigazione ONTO-PROBE |
|---|---|---|---|
| **Rappresentazionale** | No New Basis Principle | Rigidità assiomatica e riuso di pattern | Activation Steering (CAA) lungo assi ontologici primitivi |
| **Meccanico** | *Diversity Collapse* | Convergenza verso la media statistica | Architettura agentica *Blind* a isolamento priva di sessione |
| **Valutativo** | Distorsione OOD dell'Embedder | Falsi positivi su gergo vuoto e falsi negativi | Protocollo di validazione multi-embedder incrociato |
| **Funzionale** | Rumore scambiato per novità | Pura allucinazione incoerente | Gating di validità funzionale obbligatorio |
| **Operativo** | Sovraccarico di review | Affaticamento e disallineamento dei giudici | Campionamento stratificato con Power Analysis ($f=0.25$) |

### 2.2 Il Paradosso della Chiusura: Approccio Metodologico

Se un sistema multi-agente è composto da modelli vincolati al medesimo sottospazio rappresentazionale, la loro interazione discorsiva non può, per mera ricorsione, sintetizzare una nuova dimensione concettuale.

**Postura Falsificazionista:**
Il framework non promette il superamento ontologico, ma **traccia la frontiera di rottura empirica**:
1. Spinge il modello alla massima divergenza ammissibile tramite vincoli di *Semantic Tabu* e iniezione latente.
2. Monitora la soglia di transizione di fase in cui l'output cessa di essere coerente e degenera in allucinazione non testabile.
3. Se l'output non evade il database degli archetipi neppure in condizioni di massimo isolamento e steering ortogonale, lo studio fornisce la dimostrazione sperimentale formale della chiusura rappresentazionale.

### 2.3 Definizione Operativa di Novità Ontologica ($O\text{-novelty}$)

Differenziandosi dalla tassonomia di Margaret Boden ($P\text{-novelty}$ psicologica e $H\text{-novelty}$ storica):
- **O-Novelty (Novità Ontologica):** Si realizza quando un candidato formula un sistema di entità e dipendenze causali $\mathcal{R}'$ che **non ammette un omomorfismo strutturale diretto** verso i modelli codificati nel database degli archetipi $\mathcal{D}_{\text{arch}}$, soddisfacendo simultaneamente condizioni rigorose di validità funzionale $V(S)$.

$$\text{O-Novelty}(S) \iff (\text{Sim}_{\max}(S, \mathcal{D}_{\text{arch}}) < \tau) \;\land\; (V(S) \ge \theta_{\text{valid}})$$

### 2.4 Protocollo di Sanity Check per l'Embedder e Mitigazione OOD

L'impiego di un singolo modello di embedding introduce il rischio di **distorsione rappresentazionale**: proiettare concetti genuinamente alieni su uno spazio addestrato su corpora umani standard può schiacciarli verso coordinate casuali o fallaci.

Per neutralizzare questa asimmetria, ONTO-PROBE adotta un triplice controllo:
1. **Confronto Multi-Embedder Incrociato:** La distanza $\text{Sim}_{\max}$ viene calcolata in parallelo mediante due modelli ad architettura e famiglia disgiunte:
   - Modello A (Locale denso): `bge-small-en-v1.5` (384 dim, bi-encoder compatto ottimizzato per similarità semantica).
   - Modello B (Commerciale ad alta capacità): `text-embedding-3-small` (1536 dim).
   Il punteggio di similarità ammesso è il valore conservativo $\max(\text{Sim}_A, \text{Sim}_B)$.
2. **Stress-Test con Testi di Alienità Sintetica Controllata:** Prima dell'inferenza sperimentale, l'indice vettoriale viene calibrato immettendo payload artificiali composti da:
   - *Controllo Negativo (Gergo privo di senso):* Stringhe generate combinando neologismi casuali privi di coerenza logica; la metrica deve registrare elevata distanza ma il Gate Funzionale deve azzerare il punteggio finale.
   - *Controllo Positivo (Paradigmi storici traslati):* Teorie storiche pionieristiche (es. transizione dal calorico alla termodinamica cinetica) private del lessico originario; la metrica deve rilevare la divergenza relazionale corretta.
3. **Limite Dichiarato:** Nessuna metrica di embedding è assunta come oracolo perfetto; la divergenza vettoriale funge da filtro di primo livello e deve essere convalidata dal doppio binario di verifica.

---

## 3. Metodologia Dettagliata (L3 — Raw Dossiers)

### 3.1 Architettura Multi-Agente ONTO-PROBE

```
┌────────────────────────────────────────────────────────────────────────┐
│                        TOPOLOGIA ONTO-PROBE v0.3.1                     │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│   [SEED GENERATOR]                                                     │
│   ├── White-Box: Contrastive Activation Addition su Residual Stream    │
│   └── Black-Box: Vincolo Sintattico-Relazionale (Semantic Tabu)        │
│          │                                                             │
│          ▼                                                             │
│   [WORLD BUILDER] (N Istanze Parallele)                                │
│   └── Riceve solo il seed. Genera assiomi e dinamiche esplicative.     │
│       Ignora completamente il problema reale target.                   │
│          │                                                             │
│          ▼                                                             │
│   [BLIND SOLVER] (N Risolutori Isolati)                                │
│   └── Risolve configurazioni astratte nelle leggi del mondo sintetico. │
│          │                                                             │
│          ▼                                                             │
│   [CROSS-WORLD ISOMORPHISM DETECTOR]                                   │
│   └── Estrae le relazioni invarianti conservate tra mondi indipendenti.│
│          │                                                             │
│          ▼                                                             │
│   [EXTRACTOR & REALITY MAPPER]                                         │
│   └── Mappa le relazioni invarianti sul problema empirico target.      │
│          │                                                             │
│          ▼                                                             │
│   [VERIFICATION ENGINE] ─────────────────────────────────────────────┐  │
│   ├── Binario A (Formale): Sandbox Docker + Solver SMT / Z3 / ProVerif│  │
│   ├── Binario B (Aperto):  Rubrica CDAT Multi-LLM + ICC(2,k)        │  │
│   └── Safety Monitor:      Constitutional Halt Gate + HMAC Blinding  │  │
│                                                                      ▼  │
│                                                [AUDIT RECEIPT CHAIN]    │
└────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Condizionamento del Seed Ontologico

#### 3.2.1 Modalità White-Box: Contrastive Activation Addition (CAA)
Nei modelli open-weight, l'intervento agisce direttamente sul residual stream $\mathbf{h}^{(L)}$ a un layer intermedio $L$ (es. layer 16 in architetture da 32 layer), orientando l'attivazione lungo assi ontologici primitivi:
- Asse 1: *Ontologia della Sostanza (oggetti discreti)* $\longleftrightarrow$ *Ontologia del Processo (flussi continui)*
- Asse 2: *Causalità Meccanica Deterministica* $\longleftrightarrow$ *Causalità Sistemica Relazionale*
- Asse 3: *Struttura Gerarchica Rigida* $\longleftrightarrow$ *Topologia Eterarchica Distribuita*

$$\mathbf{v}_{\text{onto}} = \frac{1}{|P|} \sum_{p \in P} \mathbf{a}_L(p) - \frac{1}{|N|} \sum_{n \in N} \mathbf{a}_L(n)$$

$$\mathbf{h}^{(L)}_{\text{steered}} = \mathbf{h}^{(L)} + \alpha \cdot \mathbf{v}_{\text{onto}}, \quad \alpha \in [1.0, 2.0]$$

#### 3.2.2 Modalità Black-Box: Vincoli Sintattico-Relazionali
Per i modelli interrogati via API, il seed impone vincoli negativi e grammaticali:
```
VINCOLO DI GENERAZIONE ASSIOMATICA:
1. È vietato l'uso di predicati di causalità meccanica nota o transmodale.
2. Il sistema NON può essere formulato come flusso di particelle o scambio di pacchetti.
3. Le relazioni causali devono essere descritte unicamente secondo la sintassi:
   «Lo stato di X determina la suscettibilità di transizione di Y attraverso l'inerzia di Z».
4. Qualsiasi richiamo a metafore fisiche, biologiche o computazionali standard
   comporta l'invalidazione immediata dell'output.
```

### 3.3 Motore di Validazione a Doppio Binario

1. **Binario A (Verifica Formale Esatta):** Applicato a crittografia, logica booleana e vincoli SMT. Il candidato sintetizza formule eseguibili in sandbox Docker effimera priva di rete (**Z3** o **ProVerif**). La validità è binaria ($1.0$ se le asserzioni sono soddisfatte, $0.0$ in caso di errore logico o mancata convergenza).
2. **Binario B (Domini Aperti / Rubrica CDAT):** Applicato a progettazione sistemica, policy e teoria dell'informazione. Tre giudici LLM eterogenei valutano l'appropriatezza e la coerenza. Se l'accordo inter-giudice $\text{ICC}(2, k) < 0.60$, il dossier scala all'arbitro umano ($L_3$).

### 3.4 Protocollo L3: Power Analysis per il Campionamento Umano

La determinazione della taglia campionaria per i referee umani ($0.2\text{ FTE} \approx 8\text{ ore/settimana}$) è dimensionata per rilevare un **effetto moderato** ($f = 0.25$):

$$\alpha = 0.05, \quad \text{Power } (1 - \beta) = 0.80, \quad \text{Effect Size } f = 0.25, \quad k = 3 \text{ condizioni}$$

L'analisi della varianza (ANOVA a misure ripetute) su 3 condizioni generative (C1: Single, C2: MAS standard, C3: ONTO-PROBE) attraverso i 5 domini sperimentali ($15\text{ celle}$):
- **Campione per cella:** $n = 11\text{--}12$ valutazioni cieche indipendenti.
- **Volume totale:** $N = 165\text{--}180$ valutazioni complessive.
- **Verifica della potenza:** per un'ANOVA a una via con $k = 3$, $f = 0.25$, $\alpha = 0.05$ servono $N \ge 159$ totali per potenza $0.80$ (con $N = 120$ la potenza scende a $\approx 0.68$; con $N = 165$ è $\approx 0.82$; con $N = 180$ è $\approx 0.86$). Il disegno a misure ripetute sui task è più efficiente di quello a gruppi indipendenti, quindi $N = 165$ è una stima conservativa.
- **Domini coperti:** la valutazione umana copre tutti e 5 i domini. Per i domini del Binario A (D1, D2) la validità funzionale è stabilita dal verificatore formale; il referee valuta le restanti dimensioni della scheda (cfr. EVAL-001 §3.2).
- **Impegno operativo stimato:** Con $30\text{ minuti}$ per dossier, il fabbisogno complessivo è di **$83\text{--}90\text{ ore}$** su 12 mesi, gestibile da 0.2 FTE ($\approx 8$ ore/settimana, oltre 400 ore/anno).

### 3.5 Safety Monitoring Layer e Catena di Audit Crittografica

1. **Constitutional Halt Gate:**
   Un parser deterministico locale intercetta i token intermedi prima della mappatura sul dominio reale, arrestando il ciclo in presenza di pattern correlati a:
   - *Rischio CBRN:* Sintesi o rilascio di precursori tossici, patogeni o materiali fissili.
   - *Cyber-Exploit:* Generazione di codice di iniezione zero-day, protocolli di offuscamento payload o bypass di credenziali.
   - *Manipolazione Cognitiva:* Euristiche coercitive psicologiche, dark patterns persuasivi o exploit di consenso conversazionale.
2. **Catena Immutabile delle Ricevute (5 Campi):**
   Ogni transizione scrive un record canonico in formato JSONL calcolato come:
   $$\text{Block}_{i} = \langle \text{internal\_sample\_id}, \text{timestamp}, \text{stage}, \text{payload\_hash}, \text{prev\_hash} \rangle$$
   $$\text{Hash}_i = \text{SHA256}(\text{prev\_hash} \,\|\, \text{internal\_sample\_id} \,\|\, \text{timestamp} \,\|\, \text{stage} \,\|\, \text{payload\_hash})$$

---

## 4. Risorse, Budget e Dimensionamento

### 4.1 Team di Ricerca (Profilo Accademico Istituzionale)

| Ruolo | Responsabilità Primarie | Impegno (FTE) |
|---|---|---|
| **Principal Investigator (PI)** | Direzione scientifica, epistemologia, disegno sperimentale | 0.5 |
| **Postdoc Researcher** | Interpretabilità meccanicistica, PyTorch, steering vettoriale | 1.0 |
| **Dottorando di Ricerca** | Sviluppo pipeline, gestione micro-container, orchestrazione | 1.0 |
| **Data Scientist** | Metriche di embedding, calcolo ICC, clustering archetipi | 0.5 |
| **Esperti di Dominio** | Valutazione qualitativa cieca L3 (Design, Scienza, Policy) | 0.2 |
| **Safety & Legal Auditor** | Monitoraggio Constitutional Halt Gate, conformità etica | 0.2 |

### 4.2 Raccordo dei Costi: Scala Istituzionale vs. Operatività Standalone

1. **Budget Accademico Istituzionale (€500.000/anno):** Riflette la scala formale per la candidatura a macro-grant europei (ERC Consolidator, Horizon Europe Cluster 2), coprendo stipendi tabellari per 3.4 FTE, cluster GPU distribuiti per sweep massivi su centinaia di modelli, audit esterni e Open Access.
2. **Profilo Operativo Standalone (~€1.200/anno):** Rappresenta la configurazione effettiva e immediatamente praticabile dal ricercatore indipendente, fondata su workstation consumer (GPU $\le 16\text{ GB}$), container locali CPU a costo zero (Z3, Docker, Qdrant) e consumo mirato di API efficienti ($< €100/\text{mese}$).

---

## 5. Matrice di Gestione dei Rischi

| Rischio Identificato | Prob. | Impatto | Protocollo di Mitigazione Attivo |
|---|---|---|---|
| **Esito Nullo Globale ($O\text{-novelty} = 0$)** | Alta | Basso | L'esito negativo costituisce pubblicazione di rilievo: convalida empirica del No New Basis Principle. |
| **Collasso della Diversità nel MAS** | Alta | Alto | Isolamento informativo radicale a stati disaccoppiati (Stateless Message Passing). |
| **Degenerazione da Steering Vettoriale** | Media | Alto | Vincolo del fattore di scala $\alpha \in [1.0, 2.0]$ e monitoraggio della perplessità. |
| **Allucinazione scambiata per Novità** | Alta | Alto | Gate di validità funzionale obbligatorio (Binario A deterministico / Binario B ICC). |
| **Jailbreak Ontologico Involontario** | Media | Alto | Constitutional Halt Gate con arresto deterministico basato su regex/classificatori. |
| **Saturazione degli Esperti Umani** | Alta | Medio | Power analysis statistica con limite rigoroso a $180$ revisioni totali in doppio cieco. |

---

## 6. Opportunità Istituzionali e Pubblicazioni

- **Venue Accademiche:** International Conference on Computational Creativity (ICCC), NeurIPS Track on Generative Models, Association for Computational Linguistics (ACL), Nature Machine Intelligence.
- **Bandi Consorziali:**
  - *MIT-HPI AI and Creativity Hub (MHACH):* Programma congiunto MIT-Hasso Plattner Institut, ciclo 2027–2028.
  - *Horizon Europe Cluster 2:* Bandi su intelligenza artificiale per le industrie creative e culturali (CCSI) 2026–2027.

---

## 7. SOURCES Block

- [Matarmaa 2026](https://www.ontology-of-designing.ru/article/2026_3(61)/Ontology_Of_Designing_2026_3_опт-397-414_J.O._Matarmaa.pdf) → Operational limits of ontological innovation in LLMs
- [Lin et al. 2026](https://ar5iv.labs.arxiv.org/html/2505.21116) → Creativity in LLM-based Multi-Agent Systems: A Survey
- [Nakajima et al. 2026](https://aclanthology.org/2026.findings-eacl.138/) → Conditional Divergent Association Task (CDAT) Benchmarking
- [Turner et al. 2023](https://arxiv.org/abs/2308.10248) → Activation Addition: Steering Without Optimization
- [Rimsky et al. 2024](https://aclanthology.org/2024.acl-long.657/) → Steering Llama 2 via Contrastive Activation Addition
- [de Moura & Bjørner 2008](https://doi.org/10.1007/978-3-540-78800-3_24) → Z3: An Efficient SMT Solver
- [Blanchet 2016](https://proverif.inria.fr/) → Formal Verification of Cryptographic Protocols via ProVerif
- [Cicchetti 1994](https://doi.org/10.1037/1040-3590.6.4.284) → Guidelines, criteria, and rules of thumb for evaluating normed and standardized assessment instruments
- [Cohen 1988](https://www.utstat.toronto.edu/~brunner/oldclass/378f16/readings/CohenPower.pdf) → Statistical Power Analysis for the Behavioral Sciences
- [Vassilev 2026](https://doi.org/10.1109/MSEC.2026.3678214) → NIST Standards: Continuous Auditing for Adversarial AI Systems
- [OKF v0.2 Specification 2026](https://cloud.google.com/blog) → Google Open Knowledge Format Standard Layout
- [ONTO-PROBE Implementation Guide 2026](IMPL-001.md) → OKF-DOC-2026-ONTO-IMPL-001
- [ONTO-PROBE Benchmark Catalog 2026](BENCH-001.md) → OKF-DOC-2026-ONTO-BENCH-001
- [ONTO-PROBE Evaluation Runbook 2026](EVAL-001.md) → OKF-DOC-2026-ONTO-EVAL-001
- [ONTO-PROBE Suite Analysis 2026](META-001.md) → OKF-DOC-2026-ONTO-META-001