# Roadmap

Stato del progetto ONTO-PROBE: cosa è stato fatto, cosa resta da fare e quali azioni spettano al proprietario del repository.

> **Stato generale: pre-esecuzione.** Protocollo, codice e infrastruttura sono pronti e testati offline, ma **nessun esperimento reale è stato ancora eseguito**: non esistono risultati. Il passo che sblocca tutto il resto è il pilota black-box (sezione "Azioni per il proprietario").

Legenda: ✅ fatto · 🔄 in corso · ⬜ da fare · 👤 azione del proprietario

---

## 1. Fatto finora

### 1.1 Documentazione e protocollo
- ✅ Suite documentale completa in `docs/`: teoria (`THEORY-001`), implementazione (`IMPL-001`), benchmark (`BENCH-001`), protocollo di valutazione (`EVAL-001`), analisi della suite (`META-001`), guide operative (`howto.md`, `howto-blackbox.md`).
- ✅ Ripristinati i documenti e gli script originali completi, che erano stati sostituiti da riscritture condensate e lacunose; i file di refactor sono in `archive/`.
- ✅ Revisione di correttezza dei documenti, con correzioni su: intervallo di confidenza per 0/168, power analysis (N ≥ 159, pianificato 165–180), direzione della soglia di novità (`Sim_max < τ`), stato di prontezza, isolamento e semantica del verificatore Z3, scheda del referee su 5 domini, ICC sui soli campioni completi.
- ✅ README in inglese (principale) e italiano (`README.it.md`), con confronto tra i due percorsi di esecuzione.

### 1.2 Percorso black-box via API (nessuna GPU)
- ✅ Pipeline completa in `code/run_blackbox.py` e `code/blackbox/`: tre condizioni (C1 singolo agente, C2 multi-agente con memoria condivisa, C3 pipeline ONTO-PROBE isolata), 30 task del Binario B estratti da `BENCH-001`.
- ✅ Giudici LLM alla cieca con rubrica di `EVAL-001`, ID ciechi HMAC e catena di audit a hash.
- ✅ Statistica con sola libreria standard: ICC(2,k), gate funzionale, contrasti con bootstrap, escalation ai referee umani.
- ✅ Fasi riprendibili, stima di costo, client simulato (`--mock`) per prove a secco.
- ✅ 22 test offline, compreso il client HTTP verificato contro un server locale finto.

### 1.3 Percorso white-box CAA (GPU)
- ✅ Notebook di collaudo per Colab (`.ipynb` generato dal sorgente `.py`), con token da Colab Secrets e download dei risultati.
- ✅ Collaudo reso interpretabile: controlli con vettori casuali a norma uguale, più semi, rumore di fondo, 7 criteri di successo. La logica di analisi è stata verificata con dati sintetici.

### 1.4 Repository e infrastruttura
- ✅ Licenze (`LICENSE` Apache-2.0, `LICENSE-DOCS` CC BY 4.0), `NOTICE`, `CITATION.cff` (Francesco Iavarone, alias `matrixNeo76`).
- ✅ `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CHANGELOG.md`, template per issue e PR, `CODEOWNERS`.
- ✅ `AGENTS.md` e `CLAUDE.md` per agenti LLM, con le regole di integrità della ricerca.
- ✅ CI su GitHub Actions: test su Python 3.9–3.13, prova simulata della pipeline, verifica che notebook e lista dei task non siano obsoleti. Dependabot per le Actions.
- ✅ Corretto un difetto emerso dalla CI: `tasks_b.json` e il notebook erano esclusi dal `.gitignore` e quindi assenti da `main`.

### 1.5 Cosa non è ancora stato verificato
- Il percorso con un'API reale non è mai stato eseguito (solo client simulato e server locale finto).
- Il notebook CAA non è mai stato eseguito su una GPU.
- Il default dei nomi dei modelli (generatore e giudici) è un esempio e può essere obsoleto.

---

## 2. Azioni per il proprietario 👤

Ordinate per priorità. Le prime due sbloccano il lavoro; le altre sono impostazioni del repository che solo il proprietario può cambiare.

- [ ] 👤 **Eseguire il pilota black-box con la chiave OpenRouter.** È la prima prova con un'API reale e produce i primi dati. Passi:
  1. Creare un account su [OpenRouter](https://openrouter.ai) e ricaricare pochi euro; **impostare un limite di spesa**.
  2. Esportare la chiave: `export ONTO_API_KEY="..."`.
  3. Controllare sul sito del provider i nomi dei modelli e, se servono, impostare `ONTO_GEN_MODEL` e `ONTO_JUDGE_MODELS` (devono essere almeno tre famiglie diverse; il generatore non dovrebbe coincidere con un giudice).
  4. Stimare il costo: `python code/run_blackbox.py estimate --limit 6`.
  5. Lanciare il pilota: `python code/run_blackbox.py all --run-id pilot --limit 6`.
  6. Consegnare `outputs/blackbox/pilot/report.md` (rimuovendo eventuali dati sensibili) per la lettura e la revisione dei risultati. Dettagli in [`docs/howto-blackbox.md`](docs/howto-blackbox.md).
- [ ] 👤 **Attivare le segnalazioni private di sicurezza**: Settings → Code security → *Private vulnerability reporting*. `SECURITY.md` rimanda a quel link, che finché non è attivo non funziona.
- [ ] 👤 **Impostare descrizione e topic del repository** (Settings): suggeriti `llm`, `interpretability`, `benchmark`, `activation-steering`, `evaluation`.
- [ ] 👤 **Proteggere `main`**: richiedere PR e CI verde prima del merge (Settings → Branches).
- [ ] 👤 **Rivedere la traduzione inglese del README** e decidere se tradurre anche `docs/howto-blackbox.md`.
- [ ] 👤 **Decidere se eseguire il collaudo white-box** (Colab T4 gratuita o una GPU a noleggio) oppure rimandarlo. Non blocca il black-box.
- [ ] 👤 **Individuare i referee umani** per la valutazione cieca dei dossier in disaccordo (vedi 3.4); serve prima di una campagna completa.

---

## 3. Da implementare

### 3.1 Prossimo passo (dipende dal pilota)
- ⬜ Leggere il report del pilota e correggere i difetti emersi dall'uso reale (parsing dei giudici, costi effettivi, tempi, nomi dei modelli).
- ⬜ Verificare che l'ICC tra giudici sia accettabile; se è basso, rivedere rubrica e scelta dei giudici **prima** di guardare gli esiti per condizione.
- ⬜ Scalare ai 30 task del Binario B, con più repliche per cella, solo se il pilota è sano.

### 3.2 Completare la misura
- ⬜ **Database degli archetipi** (2.000 voci: schemi scientifici, brevetti, primitive TRIZ) e calcolo di `Sim_max` con il protocollo multi-embedder di `THEORY-001` §2.4. Oggi il report non usa la distanza dagli archetipi.
- ⬜ **Calibrazione di τ** su 100 coppie di controllo costruite a mano; la soglia 0,60 è provvisoria e va fissata prima della campagna completa.
- ⬜ **Binario A** (20 task formali Z3/ProVerif): verificatore containerizzato su rete isolata, traduzione delle soluzioni in formule, integrazione nel report.
- ⬜ Espandere le schede dei task: oggi solo B21 e B35 hanno una scheda estesa (rilascio benchmark v0.1.1).

### 3.3 Rigore sperimentale
- ⬜ **Pre-registrare** soglie, metriche e criteri di lettura prima della campagna completa, per evitare di adattarli ai risultati.
- ⬜ Controlli aggiuntivi sui giudici: ordine delle opzioni, lunghezza dei testi, favoritismo verso il proprio modello generatore.
- ⬜ **Verificare sulla fonte originale i dati di Matarmaa 2026** su cui poggia la premessa empirica (in particolare il 15,5% di classificazione non dettagliato).

### 3.4 Valutazione umana
- ⬜ Strumento per distribuire i dossier ciechi ai referee e raccogliere le schede (`blind_dossiers.jsonl` esiste già).
- ⬜ Calcolo dell'accordo uomo–giudici LLM e regola finale per i casi in disaccordo.

### 3.5 White-box CAA
- ⬜ Eseguire il collaudo su GPU e leggere `report.txt` e `control_table.csv`.
- ⬜ Se il collaudo passa: più coppie contrastanti per asse (10–20) e più semi (5–10); poi integrare lo steering nella condizione C3 con modello aperto.
- ⬜ Verificare che gli assi catturino davvero "sostanza/processo" e non un'altra dimensione (es. astratto/concreto).

### 3.6 Qualità del progetto
- ⬜ Test per le parti ancora scoperte: fasi `judge`/`analyze` con errori parziali, interruzioni di rete a metà, tabù vuoti.
- ⬜ Badge di CI nel README; eventuale `pyproject.toml` se il codice verrà distribuito come pacchetto.
- ⬜ Traduzione inglese delle guide in `docs/`.

### 3.7 Rilascio v0.4.0 (dalla roadmap di `META-001`)
- ⬜ Scorporare il Data Management Plan in un documento autonomo (`OKF-DOC-2026-ONTO-DMP-001`).
- ⬜ Scorporare il glossario in un modulo autonomo (`OKF-DOC-2026-ONTO-GLOSS-001`).
- ⬜ Benchmark espanso v0.1.1 con schede estese per tutti i 50 task.

---

## 4. Decisioni aperte

| Decisione | Opzioni | Quando serve |
|---|---|---|
| Quali modelli usare come generatore e giudici | Famiglie diverse; il generatore fuori dal pannello dei giudici | Prima del pilota |
| Se rendere pubblici i risultati nulli | Sì (raccomandato dal protocollo) / dopo revisione | Dopo il pilota |
| Come reclutare i referee umani | Colleghi, esperti di dominio, piattaforma esterna | Prima della campagna completa |
| Se dedicare tempo al white-box | Subito / dopo il black-box / mai | Dopo il pilota |

## 5. Come si aggiorna questo file

Aggiornare le caselle e le sezioni a ogni PR che cambia lo stato del progetto, insieme a [`CHANGELOG.md`](CHANGELOG.md). Una voce passa a ✅ solo quando è fatta **e verificata**, non quando è scritta.
