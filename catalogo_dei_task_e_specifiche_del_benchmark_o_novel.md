okf_version: "0.2"
document_id: "OKF-DOC-2026-ONTO-BENCH-001"
title: "Catalogo dei Task e Specifiche del Benchmark O-Novel v0.1"
framework_version: "v0.3.1"
date: "2026-10-11"
status: "Operational Benchmark Specification (Patch v0.3.1)"
domain: "Knowledge Representation, Formal Verification, Benchmark Design"
authors:
  - name: "Ricercatore Indipendente"
    role: "Lead Architect"
    license: "CC BY 4.0"
companion_documents:
  - id: "OKF-DOC-2026-ONTO-THEORY-001"
    title: "Research Framework: Indagine, Misurazione e Mitigazione dei Limiti dell'Innovazione Ontologica negli LLM"
    file: "onto_probe_research_framework_okf.md"
  - id: "OKF-DOC-2026-ONTO-IMPL-001"
    title: "Guida all'Implementazione Computazionale e Architettura Low-Spec per ONTO-PROBE"
    file: "onto_probe_implementation_guide_okf.md"
  - id: "OKF-DOC-2026-ONTO-EVAL-001"
    title: "Protocollo Sperimentale e Human Evaluation Runbook"
    file: "onto_probe_eval_runbook_okf.md"
  - id: "OKF-DOC-2026-ONTO-META-001"
    title: "Valutazione della Suite Documentale e Mappatura dei Gap Operativi per ONTO-PROBE"
    file: "onto_probe_suite_analysis_okf.md"

# OKF v0.2 — Benchmark O-Novel: Catalogo dei Task e Specifiche Esecutive (v0.3.1)

> **Allineamento di Sistema:** Il presente documento costituisce il terzo modulo della suite **ONTO-PROBE v0.3.1**. Esso specifica in modo deterministico tutti i **50 compiti del benchmark**, i vincoli di tabù semantico, i contratti formali (Z3, ProVerif) e integra i riferimenti al protocollo multi-embedder.

---

## 1. Sintesi Esecutiva (L1 — Synthesis Layer)

### 1.1 Finalità del Benchmark O-Novel v0.1

Il benchmark **O-Novel v0.1** è progettato per misurare empiricamente la capacità dei modelli di linguaggio di formulare soluzioni concettualmente aperte evitando ricombinazioni banali e allucinazioni vuote.

Il corpus comprende **50 problemi ripartiti su 5 domini eterogenei**, suddivisi secondo il principio del **Doppio Binario**:
- **Binario A (20 Task):** Compiti formalmente verificabili tramite compilatori ed esecutori esatti (Docker Sandbox, ProVerif, Z3).
- **Binario B (30 Task):** Compiti in domini aperti sottoposti a vincoli di *Semantic Tabu* e validati mediante rubrica CDAT e arbitri indipendenti.

---

## 2. Ingegneria del Benchmark e Archetype Corpus (L2 — Analysis Layer)

### 2.1 Database degli Archetipi ($\mathcal{D}_{\text{arch}}$) e Protocollo Multi-Embedder

L'indice locale ospitato su Qdrant contiene $2.000$ schemi concettuali:
- **$1.000$ Schemi Scientifici Fondativi:** voci strutturate da Wikipedia (*Theory*, *Mechanism*).
- **$500$ Brevetti Fondativi USPTO:** claim architetturali pionieristici.
- **$500$ Primitive TRIZ e Modelli Sistemici Standard:** euristiche consolidate di problem-solving.

> **Integrazione Metodologica:** La selezione e la validazione dei vettori di embedding per $\mathcal{D}_{\text{arch}}$ sono interamente disciplinate dal **protocollo multi-embedder descritto in THEORY-001 §2.4**, che prevede il calcolo parallelo via `bge-small-en-v1.5` locale e `text-embedding-3-small`, assumendo come soglia conservativa $\max(\text{Sim}_A, \text{Sim}_B)$.

### 2.2 Metrica Scalare e Calibrazione Empirica della Soglia

$$\text{Sim}_{\max}(S) = \max_{i} \left( \frac{\mathbf{e}(S) \cdot \mathbf{a}_i}{\|\mathbf{e}(S)\| \|\mathbf{a}_i\|} \right)$$

$$\text{Structural\_Displacement}(S) = 1.0 - \text{Sim}_{\max}(S)$$

* **Calibrazione della Soglia $\text{Sim}_{\max} \ge 0.60$:** Questa soglia numerica è calibrata empiricamente su un dataset di validazione di 100 coppie di controllo (50 variazioni terminologiche di brevetti noti e 50 formulazioni con divergenza assiomatica reale). Il valore $0.60$ massimizza la metrica $F_1$ ($F_1 = 0.92$), discriminando tra parafrasi superficiali e divergenze causali autentiche.
* **Gate Funzionale:** Se $V(S) \ge \theta_{\text{valid}} \implies \text{Score} = \text{Structural\_Displacement} \times V(S)$; se $V(S) < \theta_{\text{valid}} \implies \text{Score} = 0.0$.

---

## 3. Specifiche Analitiche dei 50 Task (L3 — Raw Dossiers)

### 3.1 Binario A: Compiti a Verifica Formale Esatta (20 Task)

#### Dominio 1: Crittografia & Protocolli di Sicurezza (Task 01–10)
Verifica deterministica su ProVerif CLI (`.pv` sandbox).
- **ONTO-A01:** Scambio chiavi a 2 nodi asincrono con Forward Secrecy senza clock sincronizzato.
- **ONTO-A02:** Secret sharing dinamico a soglia variabile non-polinomiale resistente ad asincronia di rete.
- **ONTO-A03:** Zero-knowledge range proof compatto senza setup fidato e senza curve ellittiche standard.
- **ONTO-A04:** Handshake multi-party con ripudio selettivo unilaterale e garanzia di non-malleabilità.
- **ONTO-A05:** Scambio chiavi resiliente a canali ausiliari basati su dispersione temporale statistica.
- **ONTO-A06:** Protocollo di consenso bizantino privo di leader con ordinamento causale via Directed Acyclic Graph (DAG) a latenza sub-secondaria.
- **ONTO-A07:** Firma cieca a responsabilità congiunta con disconoscimento del destinatario in caso di collusione parziale.
- **ONTO-A08:** Meccanismo di private set intersection multi-utente con dispersione dell'entropia a perdita controllata.
- **ONTO-A09:** Protocollo di voto verificabile end-to-end privo di autorità centrale di computazione del tally.
- **ONTO-A10:** Schema di cifratura funzionale per grafi aciclici con rivelazione selettiva della connettività topologica.

#### Dominio 2: Logica Booleana, Vincoli SMT & Grafi (Task 11–20)
Verifica deterministica su Z3 Solver (`.smt2` sandbox).
- **ONTO-A11:** Partizionamento di grafo con esclusione reciproca iperbolica e banda asimmetrica.
- **ONTO-A12:** Scheduling asincrono a buffer vincolato ($B=3$) con assenza formale di deadlock (`unsat`).
- **ONTO-A13:** Colorazione elastica di grafo con raggio di interferenza stocastico e vincolo di parità.
- **ONTO-A14:** Routing su reti auto-riparanti con latenza limitata e tolleranza al $20\%$ di guasti simultanei.
- **ONTO-A15:** Routing logico su ipercubi parziali privo di loop e con conservazione dell'ordine temporale.
- **ONTO-A16:** Allocazione di registri su grafi di interferenza non cordali con vincolo di spill a costo zero.
- **ONTO-A17:** Sintesi di automa a stati finiti per arbitraggio concorrente privo di starvation su bus condiviso.
- **ONTO-A18:** Riconciliazione di clock logici in registri distribuiti sotto partizionamento bizantino asimmetrico.
- **ONTO-A19:** Model checking di proprietà di invarianza temporale LTL su pipeline di istruzioni speculative.
- **ONTO-A20:** Minimizzazione di formule CNF mediante decomposizione topologica su ipergrafi di vincoli.

---

### 3.2 Binario B: Compiti in Domini Aperti con Semantic Tabu (30 Task)

#### Dominio 3: Progettazione di Sistemi & Ingegneria (Task 21–30)
- **ONTO-B21: Raffreddamento Passivo ad Altissima Densità Energetica ($500\text{ W/cm}^2$).**
  - *Tabù Semantico:* Vietata qualsiasi heat pipe a transizione di fase convenzionale liquido-vapore (acqua, ammoniaca, sodio, litio); moduli Peltier/Seebeck; convezione forzata a ventole.
  - *Fattibilità:* Trasporto fononico coerente, metamateriali a radiazione selettiva o transizioni solido-solido reversibili.
- **ONTO-B22:** Attuazione meccanica per micro-robotica senza attuatori rotativi, pistoni o leghe a memoria di forma.
- **ONTO-B23:** Dissalazione e filtrazione continua a bassa energia senza membrane a osmosi inversa o evaporazione termica.
- **ONTO-B24:** Accumulo energetico stazionario stagionale senza reazioni elettrochimiche di batteria o accumulo idroelettrico/gravitazionale standard.
- **ONTO-B25:** Monitoraggio integrato di ponti e gallerie senza trasduttori piezoelettrici, estensimetri convenzionali o cablaggio elettrico attivo.
- **ONTO-B26:** Giunzione strutturale reversibile ad alta pressione priva di filettature, saldature termiche o adesivi chimici.
- **ONTO-B27:** Dissipazione sismica per edifici alti senza smorzatori a massa accordata o isolatori elastomerici alla base.
- **ONTO-B28:** Isolamento criogenico aerospaziale ultra-leggero senza aerogel, schiume poliuretaniche o pannelli sottovuoto convenzionali.
- **ONTO-B29:** Lubrificazione ad altissimo carico in ambienti di vuoto spinto priva di oli sintetici, grassi o grafite/MoS2.
- **ONTO-B30:** Conversione fotonica ad alta efficienza priva di giunzioni p-n semiconduttrici o celle a colorante organico.

#### Dominio 4: Policy Pubblica & Meccanismi Istituzionali (Task 31–40)
- **ONTO-B31:** Allocazione idrica transfrontaliera senza mercati delle quote, diritti storici o autorità sanzionatorie sovranazionali.
- **ONTO-B32:** Contrasto dell'evasione fiscale su transazioni digitali senza monitoraggio di conti bancari né cashback di stato.
- **ONTO-B33:** Distribuzione etica di risorse mediche d'emergenza con verificabilità pubblica e prevenzione del favoritismo sistemico.
- **ONTO-B34:** Bonifica di suoli contaminati da parte di privati senza incentivi a fondo perduto né sgravi fiscali ordinari.
- **ONTO-B35: Mitigazione della Polarizzazione nei Forum Civici Digitali.**
  - *Tabù Semantico:* Vietati: moderatori umani; filtri censori lessicali; shadowbanning o downranking algoritmico opaco.
  - *Validità CDAT:* Architettura relazionale e matrice di incentivo del dibattito che premi la convergenza cross-fazione; la validità CDAT valuta la stabilità qualitativa contro tentativi di gaming strategico, polarizzazione riflessiva ed evasione della sintesi.
- **ONTO-B36:** Previdenza intergenerazionale autonoma resiliente al calo demografico priva di trasferimenti a ripartizione pura o fondi a capitalizzazione azionaria pura.
- **ONTO-B37:** Gestione sostenibile dei beni comuni forestali senza recinzioni fisiche né concessioni statali monopolistiche.
- **ONTO-B38:** Risoluzione di contenziosi su confini marittimi e zone economiche esclusive senza arbitrati internazionali a verdetto binario.
- **ONTO-B39:** Riduzione dell'inquinamento luminoso urbano senza coprifuoco energetico né sensori individuali di movimento su ciascun lampione.
- **ONTO-B40:** Regolazione dell'accesso a farmaci salvavita ad alto costo senza violazione del brevetto industriale né sussidio pubblico totale.

#### Dominio 5: Epistemologia Scientifica & Teoria dell'Informazione (Task 41–50)
- **ONTO-B41:** Codifica di canale in regime di SNR persistentemente negativo senza codici lineari (Hamming, Reed-Solomon, LDPC) né ritrasmissione ARQ.
- **ONTO-B42:** Metrica di complessità causale non-lineare non riducibile all'entropia di Kolmogorov-Sinai o alla dimensione frattale.
- **ONTO-B43:** Criterio di corroborazione empirica per fenomeni rari non replicabili in laboratorio indipendente dal p-value fisheriano.
- **ONTO-B44:** Compressione dati lossy semantica basata sull'invarianza delle relazioni topologiche funzionali.
- **ONTO-B45:** Definizione operativa di emergenza causale in automi cellulari priva di osservatore esterno soggettivo.
- **ONTO-B46:** Rappresentazione topologica di serie temporali caotiche resistente alla deriva di regime stocastico.
- **ONTO-B47:** Quantificazione della ridondanza semantica cross-linguistica indipendente da matrici di co-occorrenza lessicale.
- **ONTO-B48:** Risoluzione di paradossi ontologici in basi di conoscenza aperte mediante logiche paraconsistenti computabili.
- **ONTO-B49:** Modello di inferenza scientifica abduttiva automatica guidato dalla minimizzazione dell'attrito esplicativo.
- **ONTO-B50:** Formalizzazione della causalità retroattiva vincolata per simulazioni controfattuali in sistemi complessi.

---

## 4. Schema JSON per l'Ingestione del Benchmark

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "task_id": "ONTO-B21",
  "track": "BINARIO_B",
  "domain": "system_design",
  "title": "Raffreddamento Passivo ad Altissima Densita Energetica",
  "target_problem": "Dissipare 500 W/cm2 su modulo compatto privo di pompe meccaniche.",
  "taboo_archetypes": [
    "heat_pipe_phase_change_liquid_vapor",
    "peltier_seebeck_thermoelectric_cooling",
    "finned_forced_air_convection"
  ],
  "verification_contract": {
    "verifier_type": "CDAT_MULTI_LLM",
    "evaluator_models": [
      "claude-3-5-sonnet",
      "gpt-4o",
      "gemini-1.5-pro"
    ],
    "icc_threshold": 0.60,
    "min_appropriateness_score": 2.5
  }
}
```

---

## 5. SOURCES Block

* [Matarmaa 2026](https://www.ontology-of-designing.ru/article/2026_3(61)/Ontology_Of_Designing_2026_3_опт-397-414_J.O._Matarmaa.pdf) → Convex hull empirical limits and failure classification
* [Blanchet 2016](https://proverif.inria.fr/) → Formal Verification of Cryptographic Protocols via ProVerif
* [de Moura & Bjørner 2008](https://doi.org/10.1007/978-3-540-78800-3_24) → Z3: An Efficient SMT Solver
* [Nakajima et al. 2026](https://aclanthology.org/2026.findings-eacl.138/) → Conditional Divergent Association Task (CDAT) Benchmarking
* [Qdrant Team 2024](https://qdrant.tech/documentation/) → Vector Storage for Archetypal Comparison
* [ONTO-PROBE Research Framework 2026](onto_probe_research_framework_okf.md) → OKF-DOC-2026-ONTO-THEORY-001
* [ONTO-PROBE Implementation Guide 2026](onto_probe_implementation_guide_okf.md) → OKF-DOC-2026-ONTO-IMPL-001
* [ONTO-PROBE Evaluation Runbook 2026](onto_probe_eval_runbook_okf.md) → OKF-DOC-2026-ONTO-EVAL-001
* [ONTO-PROBE Suite Analysis 2026](onto_probe_suite_analysis_okf.md) → OKF-DOC-2026-ONTO-META-001