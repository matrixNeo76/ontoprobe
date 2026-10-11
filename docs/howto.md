# Guida operativa: come eseguire il collaudo CAA di ONTO-PROBE

Questa guida accompagna dall'inizio alla fine nell'esecuzione del primo collaudo empirico del framework ONTO-PROBE.

## Cosa ti serve

1. Un account Google
2. Un account Hugging Face
3. Un browser
4. Circa 1 ora di tempo

## File necessari

Assicurati che la cartella `code/` contenga:

- `notebook_caa_smoke_test_v0_3_2.py`
- `inspect_smoke_test_outputs.py`

## Passo 1 — Preparare il modello

1. Crea un account Hugging Face
2. Richiedi l'accesso a `meta-llama/Llama-3.1-8B-Instruct`
3. Genera un token di lettura
4. Salvalo in un secret di Colab come `HF_TOKEN`

## Passo 2 — Aprire Colab

1. Vai su https://colab.research.google.com
2. Crea un nuovo notebook
3. Seleziona T4 GPU in Runtime → Change runtime type

## Passo 3 — Eseguire il notebook

In Collab, incolla il contenuto di `code/notebook_caa_smoke_test_v0_3_2.py` in una cella e avvialo.

## Passo 4 — Verificare i risultati

Al termine, controlla i file in `outputs/` e poi esegui:

```bash
python code/inspect_smoke_test_outputs.py --alpha 1.5
```

## Riepilogo

Il workflow ufficiale della repo usa:

- `docs/` per la documentazione
- `code/` per gli script eseguibili
- `outputs/` per i risultati prodotti dal runtime
