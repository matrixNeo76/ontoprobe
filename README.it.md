# ONTO-PROBE

🌐 [English](README.md) · **Italiano**

Un progetto di ricerca per rispondere a una domanda: **un modello linguistico (LLM) può inventare idee davvero nuove, oppure rimescola soltanto ciò che ha già visto in addestramento?**

Per "idee nuove" si intendono nuove relazioni causali, nuovi predicati e nuovi schemi esplicativi che non siano una semplice interpolazione o ricombinazione di modelli noti (gli *archetipi*).

> **Stato: pre-esecuzione.** Documentazione e codice sono completi e testati offline, ma **nessun esperimento reale è stato ancora eseguito**: non ci sono risultati. Il repository oggi è un protocollo pronto da lanciare, non una conferma di alcuna ipotesi.

## L'idea in breve

Il progetto parte da un'ipotesi da mettere alla prova, non da una tesi da difendere. L'ipotesi è il *No New Basis Principle*: un modello addestrato su un vocabolario fisso non può generare dimensioni concettuali davvero ortogonali a quelle del suo corpus. Se è vera, l'esperimento lo mostrerà misurando fino a dove si spinge la divergenza prima che l'output diventi incoerente. Se è falsa, emergeranno soluzioni valide e lontane dagli archetipi. In entrambi i casi il risultato è informativo.

Per misurarlo il progetto combina:

- **un benchmark di 50 problemi** (O-Novel): 20 con risposta verificabile da un programma (Z3, ProVerif) e 30 aperti, con divieti sulle soluzioni ovvie (i *tabù semantici*);
- **tre condizioni a confronto**: un singolo agente, più agenti che condividono la memoria, e la pipeline ONTO-PROBE con agenti isolati e vincoli di generazione;
- **una valutazione alla cieca**: giudici LLM eterogenei e, dove non concordano, referee umani, con identificatori mascherati (HMAC) e una catena di audit;
- **un controllo statistico**: accordo tra giudici (ICC), intervalli di confidenza e verifica che l'effetto superi il rumore.

## Due modi di eseguirlo

| | **Black-box via API** | **White-box CAA** |
|---|---|---|
| Cosa fa | Chiede soluzioni a modelli commerciali e le fa valutare alla cieca da altri modelli | Entra nelle attivazioni di Llama-3.1-8B e le sposta lungo assi ontologici (*Contrastive Activation Addition*) |
| Hardware | Nessuno: basta Python e una chiave API | GPU NVIDIA con almeno 8 GB (es. Colab T4 gratuita) |
| Costo | Pochi centesimi per il pilota (stima, da verificare sui prezzi reali) | Gratuito su Colab, circa 45 minuti |
| Stato | Pipeline completa, testata offline; mai eseguita con un'API reale | Notebook pronto; mai eseguito |
| Guida | [`docs/howto-blackbox.md`](docs/howto-blackbox.md) | [`docs/howto.md`](docs/howto.md) |

**Se non hai una GPU, parti dal black-box.** Il collaudo white-box è un controllo preliminare sulla tecnica di steering, non una condizione per il resto.

## Come iniziare

### Senza GPU (black-box)

```bash
# 1. Prova a secco: offline, gratis, i numeri sono casuali ma verifica che tutto giri
python code/run_blackbox.py all --run-id prova --limit 6 --mock

# 2. Stima di chiamate e costo
python code/run_blackbox.py estimate --limit 6

# 3. Pilota reale (serve una chiave API, vedi la guida)
export ONTO_API_KEY="la-tua-chiave"
python code/run_blackbox.py all --run-id pilot --limit 6
```

Il risultato è `outputs/blackbox/pilot/report.md`. Requisiti: Python 3.9+, nessuna libreria da installare.

### Con una GPU (white-box)

Apri il notebook in Colab e scegli "Runtime → Run all":
[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/matrixNeo76/ontoprobe/blob/main/code/notebook_caa_smoke_test_v0_3_2.ipynb)

Servono un account HuggingFace con accesso a Llama-3.1-8B-Instruct e il token salvato nei Secrets di Colab (`HF_TOKEN`). Tutti i passi sono in [`docs/howto.md`](docs/howto.md).

### Test

```bash
python -m unittest discover -s code/tests
```

22 test, tutti offline.

## Cosa contiene

```text
├── docs/            documentazione del progetto (vedi tabella sotto)
├── code/
│   ├── run_blackbox.py                     avvio dell'esperimento black-box
│   ├── blackbox/                           condizioni, giudici, statistiche, audit
│   ├── notebook_caa_smoke_test_v0_3_2.ipynb  collaudo CAA per Colab (generato)
│   ├── notebook_caa_smoke_test_v0_3_2.py   sorgente del notebook
│   ├── inspect_smoke_test_outputs.py       ispezione qualitativa dei risultati CAA
│   └── tests/                              test offline
├── tools/           generatori: notebook .ipynb e lista dei task
├── outputs/         risultati generati (ignorata da git)
└── archive/         materiale storico e note di revisione
```

| Documento | A cosa serve |
|---|---|
| [`THEORY-001`](docs/THEORY-001.md) | Quadro teorico, definizione di novità ontologica, metodologia, rischi |
| [`IMPL-001`](docs/IMPL-001.md) | Architettura tecnica e codice di riferimento |
| [`BENCH-001`](docs/BENCH-001.md) | Catalogo dei 50 task e specifiche del benchmark |
| [`EVAL-001`](docs/EVAL-001.md) | Protocollo sperimentale, rubriche dei giudici, scheda del referee umano, statistica |
| [`META-001`](docs/META-001.md) | Valutazione della suite, glossario, roadmap |
| [`howto-blackbox.md`](docs/howto-blackbox.md) | Guida passo-passo al percorso via API |
| [`howto.md`](docs/howto.md) | Guida passo-passo al collaudo CAA su Colab |

I documenti teorici sono in italiano e seguono il formato OKF v0.2.

## Limiti da conoscere

- **Misura la novità percepita da giudici LLM**, non una novità ontologica dimostrata. Un risultato positivo va confermato con referee umani.
- **Il black-box non fa steering interno**: il seed sintattico è un surrogato di ciò che la CAA farebbe sulle attivazioni.
- **Manca la distanza dagli archetipi**: il database da 2.000 voci non è stato costruito e la soglia τ è provvisoria.
- **I 20 task formali (Binario A)** non sono ancora inclusi nel percorso black-box.
- **Pochi task, intervalli larghi**: il pilota da 6 task verifica la pipeline e stima il rumore; non basta per concludere.
- **Premesse da verificare**: i dati empirici di partenza (Matarmaa 2026) non sono stati controllati sulla fonte.

## Contribuire e citare

Vedi [`CONTRIBUTING.md`](CONTRIBUTING.md), il [Codice di condotta](CODE_OF_CONDUCT.md) e [`SECURITY.md`](SECURITY.md). Per citare il progetto usa [`CITATION.cff`](CITATION.cff). Le istruzioni per gli agenti LLM sono in [`AGENTS.md`](AGENTS.md).

## Cosa questo repository non afferma

Non sostiene che gli LLM possano o non possano raggiungere un'innovazione ontologica autentica. Fornisce un modo per porre la domanda in forma verificabile.

## Licenza

- Documentazione (`docs/`): CC BY 4.0
- Codice (`code/`): Apache 2.0

Testi completi: [`LICENSE`](LICENSE) (Apache-2.0) e [`LICENSE-DOCS`](LICENSE-DOCS) (CC BY 4.0).
