# Revisione Tecnica e Diagnostica: CAA Smoke Test Notebook (ONTO-PROBE v0.3.1)

Questo notebook traduce in modo magistrale un protocollo sperimentale complesso di interpretabilità meccanicistica in un workflow empirico lineare, autosufficiente ed eseguibile su hardware consumer.

**Livello di competenza rilevato:** **Outstanding**.

---

## 1. Contesto e Standard di Valutazione

* **Ambito:** Ingegneria computazionale dei modelli linguistici, interpretabilità meccanicistica (Activation Engineering).
* **Standard di riferimento:** Linee guida di riproducibilità sperimentale per conferenze di machine learning di primo piano (NeurIPS / ICLR) e validazione empirica a basso costo.
* **Criteri diagnostici:**
  1. *Stabilità a runtime:* assenza di deadlock, gestione VRAM, prevenzione di memory leak.
  2. *Fedeltà metodologica alla CAA:* corretta intercettazione dei residui e coerenza della formulazione.
  3. *Discriminabilità delle metriche:* affidabilità dei criteri di abort automatici.
  4. *Azione operativa:* prontezza per l'ispezione qualitativa umana.

---

## 2. Aree di Crescita e Rifiniture Chirurgiche

Il notebook è strutturato in modo esemplare, ma prima di avviare il runtime su Google Colab o workstation locale è fondamentale sanare tre potenziali trappole a runtime:

* **Disallineamento di tokenizzazione tra contrast pair e generazione:**
  * *Testo analizzato (Cella 6):* `inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)` all'interno di `_collect_activations()`.
  * *Problema identificato:* In `_collect_activations`, i prompt contrastanti sono tokenizzati come stringhe raw prive di template conversazionale, mentre in `generate()` il prompt target viene incapsulato tramite `apply_chat_template()`. Su modelli istruiti come *Llama-3.1-8B-Instruct*, l'hidden state estratto al termine di una stringa nuda non coincide con il confine semantico in cui inizia la risposta dell'assistente (`<|start_header_id|>assistant<|end_header_id|>\n\n`).
  * *Azione correttiva:* Uniformare l'estrazione applicando il chat template anche alle coppie di contrasto, garantendo che il vettore $\mathbf{v}_{\text{onto}}$ catturi esattamente lo stato latente all'avvio della generazione.

* **Dipendenza di serializzazione Parquet mancante:**
  * *Testo analizzato (Cella 2 e Cella 14):* Cella 2 installa le librerie principali ma omette `pyarrow`, mentre Cella 14 invoca `df_results.to_parquet(...)`.
  * *Problema identificato:* Su ambienti puliti privi di pre-installazioni (es. ambienti Docker o macchine locali con venv freschi), Pandas solleverà un `ImportError` al termine dell'intero ciclo di generazione, rischiando di interrompere l'esecuzione prima del calcolo delle metriche.
  * *Azione correttiva:* Inserire esplicitamente `pyarrow` nel comando di installazione di Cella 2 oppure affiancare un blocco di salvataggio CSV preventivo immediato.

* **Isolamento del tensore nel forward pre-hook di iniezione:**
  * *Testo analizzato (Cella 6):* `hidden[:, -1, :] = hidden[:, -1, :] + strength * vec` all'interno del `pre_hook`.
  * *Problema identificato:* La mutazione in-place su uno slice di `args[0]` all'interno del pre-hook può innescare interferenze sui buffer della KV-cache durante la generazione autoregressiva token per token.
  * *Azione correttiva:* Applicare un clone esplicito: `hidden = hidden.clone()` prima dell'alterazione dello slice, garantendo che lo stato iniettato non corrompa riferimenti contigui in memoria.

---

## 3. Selezione del Prossimo Passo Operativo

Delle tre opzioni proposte, la scelta prioritaria è l'**Opzione 2 (Script di ispezione qualitativa)**:

1. **Priorità epistemologica:** Le metriche quantitative (PPL < 200, similarità decrescente) certificano solo l'assenza di collasso linguistico; non possono dimostrare se $\alpha = 1.5$ introduca una transizione concettuale genuina (es. da oggetti discreti a flussi di processo) o una mera diversione lessicale.
2. **Supporto immediato al test:** Non appena completerai l'esecuzione del notebook, disporrai dello strumento per caricare i file esportati (`results_with_metrics.csv` o `.parquet`) ed esaminare gli output fianco a fianco, validando le 4 domande della sezione 3.3 prima di passare a qualsiasi altro modulo.

---

## 4. Domanda Guida per il Test

Durante l'esecuzione a $\alpha = 2.0$, il testo mantiene una struttura causale ingegneristica plausibile o inizia a manifestare disaccoppiamento metaforico?