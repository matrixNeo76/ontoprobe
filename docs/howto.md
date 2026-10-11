# Guida operativa: come eseguire il collaudo CAA di ONTO-PROBE

Questa guida ti accompagna dall'inizio alla fine nell'esecuzione del primo collaudo empirico del framework ONTO-PROBE. Non serve esperienza di programmazione: segui i passi in ordine e alla fine avrai in mano i risultati.

---

## Cosa ti serve

1. **Un account Google** (per Google Colab, il modo più semplice)
2. **Un account HuggingFace** (per scaricare il modello Llama)
3. **Un browser** (Chrome, Firefox, Safari vanno tutti bene)
4. **Circa 1 ora** di tempo, di cui 30 minuti di attesa automatica

Niente installazioni sul tuo computer. Niente GPU. Tutto gratis.

---

## File necessari

Prima di iniziare, assicurati che nella cartella del progetto ci siano questi tre file (la guida è in `docs/`, gli script in `code/`):

| File | Cosa contiene |
|---|---|
| `howto.md` | Questa guida |
| `notebook_caa_smoke_test_v0_3_2.py` | Il collaudo da eseguire |
| `inspect_smoke_test_outputs.py` | L'analizzatore dei risultati |

Il nome corto `inspect_smoke_test_outputs.py` è quello usato nei comandi. Il materiale storico è in `archive/` e non serve per l'esecuzione.

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

## Passo 5 — Preparare il notebook in Colab (5 minuti)

Il file del collaudo è in formato `.py` con marcatori `# %%` (celle separate). Colab si aspetta un `.ipynb`, ma c'è una scorciatoia.

### Metodo consigliato — Conversione in una cella unica

1. Sul tuo computer, apri `notebook_caa_smoke_test_v0_3_2.py` con un editor di testo (Blocco Note su Windows, TextEdit su Mac vanno bene)
2. **Seleziona tutto** il contenuto (Ctrl+A / Cmd+A)
3. **Copia** (Ctrl+C / Cmd+C)
4. Torna su Colab
5. Nella prima cella di codice, **incolla** il contenuto (Ctrl+V)

Colab tratterà i marcatori `# %%` come semplici commenti. Il codice funzionerà correttamente anche in una cella unica, con un'unica accortezza: **eseguirai tutto in un colpo solo**, e se qualcosa va storto dovrai ripartire dall'inizio.

### Metodo alternativo — Celle separate

Se preferisci la struttura a celle (più comoda per il debug):

1. Dividi il contenuto del file `.py` in corrispondenza di ogni riga `# %%`
2. In Colab crea una cella di codice per ogni blocco (**"+ Codice"**) e incolla un blocco per cella
3. Esegui le celle in ordine, dall'alto verso il basso

(Rinominare il file `.py` in `.ipynb` non funziona: Colab si aspetta un formato JSON e rifiuterebbe il file.)

**Se non sei sicuro, usa il metodo consigliato.** Funziona sempre.

---

## Passo 6 — Eseguire il notebook (30 minuti di attesa)

1. Posiziona il cursore sulla cella con il codice
2. Premi **Shift + Invio** (o clicca sull'icona ▶ a sinistra della cella)
3. Appare una rotellina accanto alla cella: sta eseguendo
4. **Aspetta** e osserva gli output che appaiono sotto la cella
5. Quando la rotellina sparisce, l'esecuzione è conclusa

### Cosa aspettarti durante l'esecuzione

| Fase | Tempo | Segnale di successo |
|---|---|---|
| Installazione librerie | 2-3 min | Messaggi di pip che finiscono con "Successfully installed..." |
| Configurazione parametri | 1 sec | Vedi stampati "Modello: ...", "Layer di intervento: 16" |
| Caricamento del modello | 3-5 min | Vedi "VRAM totale: 15.0 GB → budget GPU: 13 GiB" e "Modello caricato in XXXs" |
| Estrazione dei 3 vettori | 1-2 min | Vedi "Vettore estratto — norma L2: ..." tre volte |
| Generazione dei 19 output | 3-5 min | Vedi il testo scorrere e alla fine "Completata: 19 output" |
| Calcolo delle metriche | 5-8 min | Vedi una tabella con PPL, trigrammi, similarità |
| Valutazione dei criteri | 1 sec | Vedi "✅ PASS" o "❌ FAIL" per ciascun criterio |
| Report finale e grafici | 1 min | Vedi "REPORT CAA SMOKE TEST" e due grafici |

### Se qualcosa va storto

- **"Runtime disconnected"** → la sessione Colab è scaduta per inattività. Ricarica la pagina e riesegui dall'inizio.
- **"CUDA out of memory"** → la GPU non ce la fa. Vai su Runtime → Disconnect and delete runtime, poi ricomincia. Se succede di nuovo, apri il file `.py` con un editor, cerca `MAX_NEW_TOKENS = 256` e cambialo in `MAX_NEW_TOKENS = 128`.
- **"Repository not found" o errore 401** → il token HuggingFace non è impostato bene. Torna al Passo 4.
- **"NameError: name 'xxx' is not defined"** → hai saltato una cella. Riesegui tutto dall'inizio.

---

## Passo 7 — Scaricare i risultati (1 minuto)

Al termine dell'esecuzione, il notebook ha salvato tutto nella cartella `caa_smoke_test_output` dentro Colab.

1. Nel pannello a sinistra di Colab, clicca sull'icona a forma di **cartella** (📁)
2. Trovi la cartella `caa_smoke_test_output`
3. Aprila e scarica sul tuo computer questi tre file:
   - `results_with_metrics.csv` (i dati completi)
   - `report.txt` (il verdetto)
   - `caa_smoke_test_plots.png` (i grafici)

---

## Passo 8 — Eseguire lo script di ispezione (5 minuti)

Lo script di ispezione analizza gli output e ti mostra i tre assi ontologici fianco a fianco. Si esegue sempre in Colab.

1. Nel pannello cartella a sinistra (📁), clicca sull'icona **"Upload"** (freccia su)
2. Seleziona il file `inspect_smoke_test_outputs.py` dal tuo computer
3. Apri una **nuova cella di codice** in fondo al notebook Colab
4. Incolla questo comando e premi Shift+Invio:

```python
!python inspect_smoke_test_outputs.py --alpha 1.5
```

L'output apparirà nella cella: vedrai il baseline, poi i tre assi ontologici a $\alpha = 1.5$, ciascuno con il testo generato e le metriche.

### Comandi alternativi utili

```python
# Progressione dose-risposta per un singolo asse
!python inspect_smoke_test_outputs.py --axis asse1_sostanza_processo

# Confronto a un α diverso
!python inspect_smoke_test_outputs.py --alpha 2.0

# Salva il dossier Markdown in un percorso a scelta
# (il dossier viene sempre esportato; di default in ./caa_smoke_test_output/qualitative_dossier.md)
!python inspect_smoke_test_outputs.py --alpha 1.5 --export-md ./dossier.md
```

---

## Cosa fare dopo aver visto i risultati

Il notebook produce un verdetto binario:

**ESITO PASS** → la CAA funziona, il framework regge, si può procedere al collaudo dell'Embedder (fase successiva).

**ESITO FAIL** → il report ti dice quale criterio è fallito e cosa ritoccare ($\alpha$ massimo, layer, coppie contrastanti). In questo caso, **conserva il contenuto di `report.txt`** e analizza i criteri falliti prima di rilanciare.

---

## Se ti blocchi

I tre punti in cui le persone si bloccano più spesso:

1. **Il token HuggingFace** (Passo 1): se l'accesso al modello è negato, aspetta 24 ore o scrivi a Meta tramite il form
2. **La GPU T4 non disponibile** (Passo 3): Colab a volte non ne ha libere. Riprova dopo qualche minuto o in un altro orario
3. **Il copia-incolla del codice** (Passo 5): se perdi pezzi, i marcatori `# %%` non vanno rimossi — devono restare come commenti

---

## Riepilogo dei file e del loro ruolo

| File | Quando si usa |
|---|---|
| `howto.md` | Lo leggi prima e durante, per seguire i passi |
| `notebook_caa_smoke_test_v0_3_2.py` | Passo 5-6: lo incolli in Colab per eseguire il collaudo |
| `inspect_smoke_test_outputs.py` | Passo 8: lo carichi in Colab per analizzare i risultati |

Nient'altro è necessario. Buon collaudo.