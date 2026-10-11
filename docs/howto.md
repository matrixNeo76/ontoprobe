# Guida operativa: come eseguire il collaudo CAA di ONTO-PROBE

Questa guida ti accompagna dall'inizio alla fine nell'esecuzione del primo collaudo empirico del framework ONTO-PROBE. Non serve esperienza di programmazione: segui i passi in ordine e alla fine avrai in mano i risultati.

---

## Cosa ti serve

1. **Un account Google** (per Google Colab, il modo più semplice)
2. **Un account HuggingFace** (per scaricare il modello Llama)
3. **Un browser** (Chrome, Firefox, Safari vanno tutti bene)
4. **Circa 1 ora e mezza** di tempo, di cui circa 45 minuti di attesa automatica

Niente installazioni sul tuo computer. Niente GPU. Tutto gratis.

---

## File necessari

Per eseguire il collaudo ti basta il notebook; gli altri file sono di supporto:

| File | Cosa contiene |
|---|---|
| `docs/howto.md` | Questa guida |
| `code/notebook_caa_smoke_test_v0_3_2.ipynb` | Il collaudo da eseguire in Colab |
| `code/inspect_smoke_test_outputs.py` | L'analizzatore dei risultati (scaricato in automatico dal notebook) |

Il materiale storico è in `archive/` e non serve per l'esecuzione.

---

## Passo 1 — Preparare l'accesso al modello (10 minuti, una tantum)

Il modello `Llama-3.1-8B-Instruct` è di Meta e richiede autorizzazione. È una formalità, di solito approvata in pochi minuti.

1. Vai su https://huggingface.co/join e crea un account
2. Vai su https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct
3. Clicca **"Agree and access repository"** e compila il modulo
4. Attendi l'email di approvazione (arriva di solito entro pochi minuti)
5. Vai su https://huggingface.co/settings/tokens
6. Clicca **"Create new token"** → tipo **"Read"** → nome qualsiasi (es. `onto-probe-test`)
7. **Copia il token che appare** (inizia con `hf_...`) e salvalo temporaneamente in un file di testo. **Non potrai rivederlo dopo.**

Questo token è la chiave d'accesso al modello.

---

## Passo 2 — Aprire Google Colab (2 minuti)

1. Vai su https://colab.research.google.com
2. Accedi con il tuo account Google
3. Clicca **"Nuovo notebook"**
4. Si apre una pagina con una cella di codice vuota

Ora hai un ambiente Python funzionante nel browser, senza installare nulla.

---

## Passo 3 — Attivare la GPU gratuita (1 minuto)

Colab ti dà una GPU gratis, ma devi richiederla esplicitamente.

1. Menu in alto: **"Runtime"** → **"Change runtime type"**
2. In **"Hardware accelerator"** scegli **"T4 GPU"**
3. Clicca **"Save"**

Verifica: in alto a destra dovresti vedere `T4` accanto a un'icona. Se lo vedi, sei pronto.

---

## Passo 4 — Configurare il token HuggingFace in Colab (2 minuti)

1. Nel pannello a sinistra di Colab, clicca sull'icona a forma di **chiave** (🔑) — si chiama "Secrets"
2. Clicca **"+ Add new secret"**
3. Nel campo **"Name"** scrivi esattamente: `HF_TOKEN`
4. Nel campo **"Value"** incolla il token del Passo 1 (quello che inizia con `hf_...`)
5. Attiva l'interruttore **"Notebook access"** a destra
6. Clicca **"Save"**

Fatto. Il notebook potrà accedere al modello senza che tu debba scrivere il token nel codice.

---

## Passo 5 — Aprire il notebook in Colab (2 minuti)

Il collaudo è un vero notebook Colab: `code/notebook_caa_smoke_test_v0_3_2.ipynb`. Non devi copiare né incollare codice.

### Metodo consigliato — Apri da GitHub

1. In Colab: **"File" → "Apri notebook" → scheda "GitHub"**
2. Incolla `matrixNeo76/ontoprobe` e scegli `code/notebook_caa_smoke_test_v0_3_2.ipynb`

Oppure apri direttamente: https://colab.research.google.com/github/matrixNeo76/ontoprobe/blob/main/code/notebook_caa_smoke_test_v0_3_2.ipynb

(Il link funziona quando le modifiche sono su `main`. Prima del merge, sostituisci `main` con il nome del branch.)

### Metodo alternativo — Carica il file

1. Scarica `notebook_caa_smoke_test_v0_3_2.ipynb` dal repository
2. In Colab: **"File" → "Carica notebook"** e seleziona il file

### Il file `.py`

`notebook_caa_smoke_test_v0_3_2.py` è la fonte del notebook (formato con marcatori `# %%`). Se lo modifichi, rigenera il `.ipynb` con `python tools/build_notebook.py`. Non va incollato in Colab.

---

## Passo 6 — Eseguire il notebook (circa 45 minuti di attesa)

1. Menu **"Runtime" → "Run all"** (Esegui tutto)
2. Se Colab chiede l'accesso ai Secrets, concedilo
3. **Aspetta** e osserva gli output sotto le celle
4. A fine esecuzione l'ultima cella scarica da sola lo zip dei risultati

### Cosa aspettarti durante l'esecuzione

| Fase | Tempo | Segnale di successo |
|---|---|---|
| Installazione librerie | 2-3 min | Messaggi di pip che finiscono con "Successfully installed..." |
| Configurazione parametri | 1 sec | Vedi stampati "Modello: ...", "Layer di intervento: 16" |
| Caricamento del modello | 3-5 min | Vedi "VRAM totale: 15.0 GB → budget GPU: 13 GiB" e "Modello caricato in XXXs" |
| Estrazione dei 3 vettori | 1-2 min | Vedi "Vettore estratto — norma L2: ..." tre volte |
| Generazione dei 84 output (3 semi) | 15-20 min | Vedi il contatore `[n/84]` e alla fine "Completata: 84 output" |
| Calcolo delle metriche | 8-12 min | Vedi una tabella con PPL, trigrammi, similarità (media sui semi) |
| Valutazione dei criteri | 1 sec | Vedi la tabella del controllo casuale e "✅ PASS" o "❌ FAIL" per ciascuno dei 7 criteri |
| Report finale e grafici | 1 min | Vedi "REPORT CAA SMOKE TEST" e due grafici |

### Se qualcosa va storto

- **"Runtime disconnected"** → la sessione Colab è scaduta per inattività. Ricarica la pagina e riesegui dall'inizio.
- **"CUDA out of memory"** → la GPU non ce la fa. Vai su Runtime → Disconnect and delete runtime, poi ricomincia. Se succede di nuovo, nella cella "Configurazione globale" del notebook cambia `MAX_NEW_TOKENS = 256` in `MAX_NEW_TOKENS = 128`, oppure riduci `SEEDS` a due semi.
- **"Repository not found" o errore 401** → il token HuggingFace non è impostato bene. Torna al Passo 4.
- **"NameError: name 'xxx' is not defined"** → hai saltato una cella. Usa **"Runtime" → "Run all"**.

---

## Passo 7 — Scaricare i risultati (1 minuto)

L'ultima cella crea `caa_smoke_test_output.zip` e ne avvia il download. Se il download viene bloccato dal browser, apri il pannello cartella (📁) e scaricalo da lì. Lo zip contiene:

- `results_with_metrics.csv` (i dati completi, con colonne `kind` e `seed`)
- `report.txt` (il verdetto)
- `control_table.csv` (effetto degli assi reali contro i controlli casuali)
- `caa_smoke_test_plots.png` (i grafici)
- `qualitative_dossier.md` (il dossier di ispezione)

---

## Passo 8 — Ispezione qualitativa (già inclusa)

La penultima cella del notebook scarica `inspect_smoke_test_outputs.py` dal repository e mostra i tre assi ontologici a $\alpha = 1.5$ con il testo generato e le metriche, salvando anche il dossier Markdown.

Se la cella non riesce a scaricare lo script (ad esempio prima del merge su `main`: modifica `REPO_REF` con il nome del branch), carica a mano `code/inspect_smoke_test_outputs.py` nel pannello cartella (📁) e lancia in una nuova cella:

```python
!python inspect_smoke_test_outputs.py --input caa_smoke_test_output/results_with_metrics.csv --alpha 1.5
```

### Comandi alternativi utili

```python
# Progressione dose-risposta per un singolo asse
!python inspect_smoke_test_outputs.py --axis asse1_sostanza_processo

# Confronto a un α diverso
!python inspect_smoke_test_outputs.py --alpha 2.0

# Un altro seed (di default si mostra il più basso); i controlli casuali compaiono come assi random_*
!python inspect_smoke_test_outputs.py --alpha 1.5 --seed 43

# Salva il dossier Markdown in un percorso a scelta
# (il dossier viene sempre esportato; di default in ./caa_smoke_test_output/qualitative_dossier.md)
!python inspect_smoke_test_outputs.py --alpha 1.5 --export-md ./dossier.md
```

---

## Cosa fare dopo aver visto i risultati

Il notebook produce un verdetto binario su 7 criteri. I due che contano di più sono quelli di controllo: l'effetto dell'asse deve superare sia quello di un **vettore casuale della stessa norma** sia il **rumore di fondo** tra semi diversi.

**ESITO PASS** → la CAA produce un effetto sistematico e specifico. Non dimostra che l'asse catturi davvero la dimensione ontologica voluta: leggi i testi con `inspect_smoke_test_outputs.py` e confronta gli assi con i controlli `random_*` prima di procedere al collaudo dell'Embedder.

**ESITO FAIL** → il report ti dice quale criterio è fallito. Se falliscono i criteri 6 o 7, l'effetto non è distinguibile da rumore o da una spinta casuale: aumenta le coppie contrastanti per asse, prova un altro layer e rilancia. **Conserva sempre `report.txt` e `control_table.csv`**: anche un esito negativo è un dato.

---

## Se ti blocchi

I tre punti in cui le persone si bloccano più spesso:

1. **Il token HuggingFace** (Passo 1): se l'accesso al modello è negato, aspetta 24 ore o scrivi a Meta tramite il form
2. **La GPU T4 non disponibile** (Passo 3): Colab a volte non ne ha libere. Riprova dopo qualche minuto o in un altro orario
3. **L'accesso ai Secrets** (Passo 4): se la cella "Token HuggingFace" segnala un errore, controlla che `HF_TOKEN` esista e che "Notebook access" sia attivo

---

## Riepilogo dei file e del loro ruolo

| File | Quando si usa |
|---|---|
| `howto.md` | Lo leggi prima e durante, per seguire i passi |
| `notebook_caa_smoke_test_v0_3_2.ipynb` | Passo 5-6: lo apri in Colab ed esegui tutto |
| `notebook_caa_smoke_test_v0_3_2.py` | Fonte del notebook: si modifica solo se vuoi cambiare il collaudo |
| `inspect_smoke_test_outputs.py` | Passo 8: scaricato in automatico dal notebook |

Nient'altro è necessario. Buon collaudo.