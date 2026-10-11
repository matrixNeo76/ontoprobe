# Guida operativa: esperimento black-box via API (senza GPU)

Questa guida esegue il **Binario B** di ONTO-PROBE (30 task aperti con tabù semantici) usando solo API di modelli commerciali. Non servono GPU, né Colab, né installazioni: bastano Python 3.9+ e una chiave API. Il codice usa solo la libreria standard.

## Cosa fa

Per ogni task genera una soluzione in tre condizioni (EVAL-001 §2.1):

| Condizione | Procedura | Chiamate per task |
|---|---|---|
| **C1** | Singolo agente, prompt standard | 1 |
| **C2** | Tre agenti (proponente, critico, sintetizzatore) con memoria condivisa | 3 |
| **C3** | ONTO-PROBE: seed sintattico-relazionale, 2 mondi sintetici isolati, rilevatore di invarianti, Extractor | 6 |

Poi tre giudici LLM eterogenei valutano ogni soluzione **alla cieca** (vedono solo problema, tabù e testo; mai condizione, ruoli o modello) con la rubrica di EVAL-001 §3.1. Il report finale confronta le condizioni con intervalli di confidenza e calcola l'accordo tra giudici (ICC).

## Preparazione (5 minuti)

1. Crea un account su [OpenRouter](https://openrouter.ai) (una sola chiave dà accesso a modelli di più fornitori, necessario per avere giudici eterogenei) e ricarica pochi euro di credito.
2. Esporta la chiave:
   ```bash
   export ONTO_API_KEY="la-tua-chiave"
   ```
3. Controlla i nomi dei modelli sul sito del provider e, se servono, impostali (i default sono esempi che possono diventare obsoleti):
   ```bash
   export ONTO_GEN_MODEL="openai/gpt-4o-mini"
   export ONTO_JUDGE_MODELS="anthropic/claude-3.5-haiku,openai/gpt-4o-mini,google/gemini-2.0-flash-001"
   ```
   Con un provider diverso (es. OpenAI diretto) imposta anche `ONTO_API_BASE`, ma i giudici dovranno essere tutti del suo catalogo e perdi l'eterogeneità.

## Esecuzione

Dalla radice del repository:

```bash
# 1. Prova a secco, offline e gratis: verifica che tutto giri (i numeri sono casuali)
python code/run_blackbox.py all --run-id prova --limit 6 --mock

# 2. Stima di chiamate e costo prima di spendere
python code/run_blackbox.py estimate --limit 6

# 3. Pilota reale: 6 task (2 per dominio), 18 dossier, circa 114 chiamate
python code/run_blackbox.py all --run-id pilot --limit 6

# 4. Campagna completa: 30 task (aggiungi --reps 2 per più campioni)
python code/run_blackbox.py all --run-id completo --limit 30
```

Le fasi si possono lanciare da sole (`generate`, `judge`, `analyze`) e sono **riprendibili**: se la rete cade, rilancia lo stesso comando e riparte da dove si era fermato senza rifare (né ripagare) le chiamate già completate.

Per scegliere task specifici: `--tasks ONTO-B21 ONTO-B35`.

## Risultati

Tutto è in `outputs/blackbox/<run-id>/` (cartella ignorata da git):

| File | Contenuto |
|---|---|
| `report.md` | Tabella per condizione, contrasti con IC 95%, ICC tra giudici |
| `report.json` | Gli stessi dati in formato leggibile da programmi |
| `generations.jsonl` | Soluzioni finali e tracce intermedie di ogni agente |
| `judgments.jsonl` | Giudizi grezzi di ogni giudice, indicizzati per ID cieco |
| `blind_dossiers.jsonl` | Dossier anonimi (solo ID cieco, problema, testo) da dare ai referee umani |
| `audit.jsonl` | Catena di hash a 5 campi di ogni generazione e giudizio |
| `.hmac_key` | Chiave segreta del blinding. **Per un doppio cieco reale tienila fuori dalla cartella condivisa con i referee** |

## Come leggere il report

- **Novità (gated, 0–1):** novità media dei giudici normalizzata, azzerata se l'appropriatezza media è < 2,5 o se la maggioranza dei giudici vede un tabù violato (EVAL-001 §4).
- **Contrasti C3−C1 e C3−C2:** se l'intervallo di confidenza include 0, la differenza non è distinguibile dal rumore. Con 6 task è quasi sempre così: il pilota serve a verificare la pipeline e stimare costi e rumore, non a concludere.
- **ICC < 0,60:** i giudici non concordano. In quel caso la misura non è affidabile e i dossier andrebbero valutati da referee umani (usa `blind_dossiers.jsonl`).
- **"Da escalare a umano":** quota di dossier in cui i giudici differiscono di almeno 2 punti.

## Limiti da conoscere

1. **Misura la novità percepita da LLM**, non una novità ontologica dimostrata. Un esito positivo va confermato con referee umani.
2. **Manca la distanza dagli archetipi** (database da 2.000 voci non costruito, THEORY-001 §2.4): il report non la usa.
3. **I giudici possono favorire il proprio stile:** il modello generatore compare anche tra i giudici. Per ridurre il rischio usa per i giudici modelli diversi da quello che genera.
4. **Il ramo black-box non fa steering interno.** Il seed sintattico è un surrogato di quello che la CAA farebbe sulle attivazioni (THEORY-001 §3.2.2).
5. **I 20 task del Binario A** (verificabili con Z3/ProVerif) non sono ancora inclusi: richiedono il verificatore formale e la traduzione delle soluzioni in formule.
6. **Il costo mostrato è una stima** basata su prezzi medi che puoi cambiare con `--price-in` e `--price-out`.

## Test

```bash
python -m unittest discover -s code/tests
```

I test sono offline: verificano ICC (contro l'esempio di Shrout & Fleiss), gate, parsing dei giudici, catena di audit, riprendibilità e il flusso completo con il client simulato.

## Rigenerare i task

I 30 task sono estratti da `docs/BENCH-001.md` in `code/blackbox/data/tasks_b.json`. Se modifichi il documento: `python tools/build_tasks.py`.
