okf_version: "0.2"
document_id: "OKF-DOC-2026-ONTO-EVAL-001"
title: "Protocollo Sperimentale e Human Evaluation Runbook"
framework_version: "v0.3.1"
date: "2026-10-11"
status: "Operational Evaluation Runbook (Patch v0.3.1)"
domain: "Experimental Design, Inter-Rater Reliability, Statistics"
authors:
  - name: "Ricercatore Indipendente"
    role: "Lead Architect"
    license: "CC BY 4.0"
companion_documents:
  - id: "OKF-DOC-2026-ONTO-THEORY-001"
    title: "Research Framework: Indagine, Misurazione e Mitigazione dei Limiti dell'Innovazione Ontologica negli LLM"
    file: "THEORY-001.md"
  - id: "OKF-DOC-2026-ONTO-IMPL-001"
    title: "Guida all'Implementazione Computazionale e Architettura Low-Spec per ONTO-PROBE"
    file: "IMPL-001.md"
  - id: "OKF-DOC-2026-ONTO-BENCH-001"
    title: "Catalogo dei Task e Specifiche del Benchmark O-Novel v0.1"
    file: "BENCH-001.md"
  - id: "OKF-DOC-2026-ONTO-META-001"
    title: "Valutazione della Suite Documentale e Mappatura dei Gap Operativi per ONTO-PROBE"
    file: "META-001.md"

# OKF v0.2 — Protocollo Sperimentale e Human Evaluation Runbook: ONTO-PROBE (v0.3.1)

> **Allineamento di Sistema:** Il presente documento costituisce il quarto modulo esecutivo della suite **ONTO-PROBE v0.3.1**. Esso standardizza la procedura sperimentale in doppio cieco con separazione crittografica HMAC, i template per i giudici LLM, la scheda per i referee umani e il codice statistico per $\text{ICC}(2, k)$ e ANOVA a misure ripetute con gestione dei dati mancanti.

---

## 1. Sintesi Esecutiva (L1 — Synthesis Layer)

### 1.1 Obiettivo del Runbook

Per garantire che le conclusioni della ricerca posseggano rigore scientifico certificabile, la valutazione empirica elimina ogni soggettività non controllata.

Questo runbook:
1. **Governa il Doppio Cieco via HMAC:** Isola l'identificatore interno dal dossier esaminato tramite derivazione unidirezionale con chiave segreta, impedendo de-anonimizzazioni anche in caso di accesso ai log di audit.
2. **Definisce i Prompt dei Giudici LLM:** Uniforma le chiamate al panel di modelli eterogenei allo stato dell'arte al momento dell'esecuzione.
3. **Formalizza la Scheda per il Referee Umano ($L_3$):** Fornisce una rubrica su 4 dimensioni ortogonali con ancore semantiche precise.
4. **Fornisce lo Script di Analisi Statistica:** Elabora i record JSONL, gestisce esplicitamente i valori mancanti (`pairwise deletion` con warning) e calcola $\text{ICC}(2, k)$ e ANOVA a misure ripetute.

---

## 2. Disegno Sperimentale e Catena di Valutazione (L2 — Analysis Layer)

### 2.1 Schema della Matrice Sperimentale ($3 \times 5$)

```
┌────────────────────────────────────────────────────────────────────────┐
│                     MATRICE SPERIMENTALE 3x5 (15 CELLE)                │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  Condizione C1 (Controllo 1):   Single-Agent Standard Prompting        │
│  Condizione C2 (Controllo 2):   Multi-Agent Conversazionale (Shared M.)│
│  Condizione C3 (Trattamento):   ONTO-PROBE (Isolato + Blind MAS + CAA) │
│                                                                        │
│  5 Domini di Test:                                                     │
│  D1: Crittografia   D2: Logica/SMT   D3: Sistemi   D4: Policy   D5: Info│
│                                                                        │
│  Campionamento Totale per la Valutazione Umana (L3):                   │
│  15 celle × 8-12 campioni = 120-180 dossier indipendenti (f = 0.25)    │
└────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Il Meccanismo di Mascheramento Crittografico (HMAC-Blinding)

Per prevenire qualsiasi incrocio tra log di audit e dossier sottoposti ai revisori:
1. **Anonimizzazione del Payload:** Rimozione di qualsiasi metadato, menzione dei ruoli ("World Builder", "Blind Solver"), model identifier o prompt intermedi.
2. **Derivazione Unidirezionale dell'ID Cieco:** Il runtime applica una funzione HMAC-SHA256 all'identificatore interno del campione:
   $$\text{Blind\_ID} = \text{"BLIND-SAMPLE-" } \| \; \text{HMAC}_{K_{\text{secret}}}(\text{Internal\_Sample\_ID})[0:12]$$
   La chiave crittografica $K_{\text{secret}}$ è conservata esclusivamente dal Principal Investigator in archivio cifrato e sigillata fino al termine della campagna di revisione.
3. **Randomizzazione dell'Ordine:** I dossier vengono somministrati secondo permutazione casuale bilanciata di Fisher-Yates.

---

## 3. Specifiche Operative e Strumenti (L3 — Raw Dossiers)

### 3.1 Template Standard dei Giudici LLM (Binario B)

Tutte le chiamate agli arbitri artificiali impiegano il medesimo system prompt e richiedono uno schema JSON deterministico. I modelli di frontiera impiegati (indicativamente Claude 3.5 Sonnet / successor, GPT-4o / successor, Gemini 1.5 Pro / successor) saranno congelati tramite commit/snapshot ID specifico registrato nella catena di audit:

```
SYSTEM PROMPT PER I GIUDICI LLM:
Sei un arbitro scientifico indipendente specializzato in epistemologia e teoria dei sistemi.
Valuta la proposta concettuale candidata rispetto al problema assegnato e agli archetipi tabù.
Valuta l'output con il massimo rigore. Non premiare l'oscurità lessicale o il gergo non funzionale.

FORMATO DI RISPOSTA RICHIESTO (STRETTAMENTE JSON):
{
  "appropriateness_score": <float da 1.0 a 5.0>,
  "logical_coherence_score": <float da 1.0 a 5.0>,
  "structural_novelty_score": <float da 1.0 a 5.0>,
  "taboo_violation_detected": <true/false>,
  "identified_known_archetypes": [<stringhe di eventuali modelli noti rilevati>],
  "reasoning_summary": "<massimo 150 parole>"
}

RUBRICA DI ANCORAGGIO:
Appropriateness (Validità Funzionale):
 1.0 = Completamente incoerente o dannoso per il contesto.
 2.0 = Non risolve il problema o ignora vincoli fisici/logici basilari.
 3.0 = Risolve parzialmente il problema, con lacune operative gravi.
 4.0 = Soluzione plausibile, implementabile e priva di contraddizioni.
 5.0 = Soluzione eccellente, efficiente e pienamente coerente.

Structural Novelty (Divergenza Ontologica):
 1.0 = Banale riscrittura di modelli noti (anche se espressa con neologismi).
 2.0 = Range extension o combinazione standard di due nozioni diffuse.
 3.0 = Adattamento metaforico di un modello consolidato da un altro settore.
 4.0 = Ristrutturazione causale non convenzionale, dipendenze atipiche.
 5.0 = Nuova ontologia relazionale non riconducibile ai framework noti.
```

---

### 3.2 Scheda di Valutazione per il Referee Umano ($L_3$)

I revisori esperti ricevono il dossier cieco e compilano il modulo standardizzato su **4 dimensioni ortogonali**:

```
══════════════════════════════════════════════════════════════════════════
               SCHEDA DI VALUTAZIONE CIECA — PROGETTO ONTO-PROBE
══════════════════════════════════════════════════════════════════════════
ID Campione Cieco: [ BLIND-SAMPLE-__________ ]
Data di Revisione: [ ____-____-________ ]
Esperto Referee ID: [ RATER-____ ]
Dominio Applicato: [ ] Ingegneria  [ ] Policy  [ ] Info/Scienza

1. VALIDITÀ FUNZIONALE E FATTIBILITÀ (Scala 1-5):
   [ ] 1 - Assurdo / Fisicamente o logicamente privo di senso (Puro rumore)
   [ ] 2 - Palesemente fallace su assunti basilari di dominio
   [ ] 3 - Funzionalmente incompleto (richiede postulati non dimostrati)
   [ ] 4 - Concettualmente plausibile e privo di contraddizioni interne
   [ ] 5 - Rigoroso, coerente e ingegneristicamente solido

2. RIDUCIBILITÀ AD ARCHETIPI NOTI (Scala 1-5):
   [ ] 1 - Riconducibile immediatamente a: ______________________________
   [ ] 2 - Estensione scalare marginale di framework noti
   [ ] 3 - Ibrido chimerico di due concetti ordinari
   [ ] 4 - Divergenza marcata, relazioni causali insolite
   [ ] 5 - Non mappabile su alcun modello teorico consolidato

3. INTEGRITÀ SEMANTICA VS ILLUSIONE LESSICALE (Scala 1-5):
   [ ] 1 - Puro gergo alieno/allucinatorio che maschera banalità o assurdità
   [ ] 2 - Prevalenza di terminologia opaca con debole sostanza causale
   [ ] 3 - Equilibrio tra formalismo astratto e contenuto operativo
   [ ] 4 - Linguaggio rigoroso con corrispondenza concettuale chiara
   [ ] 5 - Formalismo impeccabile ed essenziale, privo di ridondanza

4. TRASFERIBILITÀ E ISOMORFISMO ASTRATTO (Scala 1-5):
   [ ] 1 - Vincolato strettamente a un caso limite non generalizzabile
   [ ] 2 - Difficilmente trasferibile ad altri problemi dello stesso settore
   [ ] 3 - Principio isolabile applicabile a contesti analoghi limitati
   [ ] 4 - Schema relazionale robusto ed esportabile tra domini affini
   [ ] 5 - Struttura assiomatica fondamentale di portata universale

5. NOTE ANALITICHE SINTETICHE:
   ______________________________________________________________________
══════════════════════════════════════════════════════════════════════════
```

---

### 3.3 Script Standalone di Calcolo Statistico (`evaluate_metrics.py`)

Lo script gestisce esplicitamente il disallineamento nei dati e la cancellazione a coppie (pairwise):

```python
#!/usr/bin/env python3
"""
evaluate_metrics.py — Statistical Evaluation Harness for ONTO-PROBE (v0.3.1)
Calcola ICC(2,k), ANOVA a misure ripetute e gestisce missing data con avvisi espliciti.
"""

import json
import logging
import numpy as np
import pandas as pd
from scipy import stats
import pingouin as pg

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def load_evaluation_records(jsonl_path: str) -> pd.DataFrame:
    records = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return pd.DataFrame(records)

def compute_inter_rater_icc(df_ratings: pd.DataFrame) -> dict:
    """
    Calcola ICC(2,k) (Two-way random effects, average raters, absolute agreement).
    Richiede colonne: ['sample_id', 'rater_id', 'score'].
    Esegue pairwise dropping e verifica bilanciamento del design.
    """
    initial_len = len(df_ratings)
    cleaned = df_ratings[['sample_id', 'rater_id', 'score']].dropna()
    
    if len(cleaned) < initial_len:
        logging.warning("Rilevati valori mancanti nei rating. Applicata pairwise deletion (%d record rimossi).", 
                        initial_len - len(cleaned))
        
    if cleaned.empty or cleaned['score'].std() == 0:
        return {
            "icc_value": 0.0,
            "ci95": [0.0, 0.0],
            "p_value": 1.0,
            "is_reliable": False,
            "note": "Insufficient data or zero variance"
        }
        
    # Verifica matrice completa per pingouin
    crosstab = pd.crosstab(cleaned['sample_id'], cleaned['rater_id'])
    if not (crosstab == 1).all().all():
        logging.warning("Design non perfettamente bilanciato tra tutti i rater. "
                        "ICC(2,k) calcolato sui campioni con intersezione completa.")

    try:
        icc_table = pg.intraclass_corr(
            data=cleaned,
            targets='sample_id',
            raters='rater_id',
            ratings='score'
        )
        icc_2k = icc_table[icc_table['Type'] == 'ICC2k'].iloc[0]
        icc_val = float(icc_2k['ICC'])
        
        return {
            "icc_value": icc_val,
            "ci95": [float(icc_2k['CI95%'][0]), float(icc_2k['CI95%'][1])],
            "p_value": float(icc_2k['pval']),
            "is_reliable": bool(icc_val >= 0.60) # Soglia Cicchetti (1994)
        }
    except Exception as e:
        logging.error("Errore durante il calcolo ICC: %s", str(e))
        return {
            "icc_value": 0.0,
            "ci95": [0.0, 0.0],
            "p_value": 1.0,
            "is_reliable": False,
            "note": f"Computation error: {str(e)}"
        }

def run_condition_anova(df_results: pd.DataFrame) -> dict:
    """
    Esegue ANOVA a misure ripetute confrontando C1 (Single), C2 (MAS), C3 (ONTO-PROBE).
    Richiede colonne: ['task_id', 'condition', 'novelty_score'].
    """
    cleaned = df_results[['task_id', 'condition', 'novelty_score']].dropna()
    
    aov = pg.rm_anova(
        data=cleaned,
        dv='novelty_score',
        within='condition',
        subject='task_id'
    )
    
    f_stat = float(aov['F'].iloc[0])
    p_val = float(aov['p-unc'].iloc[0])
    np2 = float(aov['ng2'].iloc[0])
    
    posthoc = pg.pairwise_tests(
        data=cleaned,
        dv='novelty_score',
        within='condition',
        subject='task_id',
        padjust='bonf'
    )
    
    return {
        "F_statistic": f_stat,
        "p_value": p_val,
        "effect_size_eta2": np2,
        "significant": bool(p_val < 0.05),
        "posthoc_table": posthoc[['A', 'B', 'T', 'p-corr', 'hedges']].to_dict(orient='records')
    }

if __name__ == "__main__":
    print("ONTO-PROBE Statistical Harness Inizializzato (v0.3.1).")
```

---

## 4. Matrice di Decisione per l'Escalation dei Risultati

| Esito della Valutazione | Condizione Metrica | Azione del Framework |
|---|---|---|
| **Accordo Giudici Artificiali Elevato** | $\text{ICC}(2, k) \ge 0.60$ e $\text{Appr} \ge 2.5$ | Registrazione del punteggio; chiusura del task. *(Soglia $\ge 0.60$ basata su Cicchetti 1994 per affidabilità 'Good')*. |
| **Disaccordo tra Giudici LLM** | $\text{ICC}(2, k) < 0.60$ | **Escalation automatica a L3:** invio del dossier al referee umano in cieco via ID HMAC. |
| **Bassa Validità / Rumore** | $\text{Appr} < 2.5$ | Punteggio finale azzerato ($O\text{-novelty} = 0.0$); classificazione come *Nonsense/Hallucination*. |
| **Violazione Guardrail Tabù** | Flag `taboo_violation = true` | Marcatura come *Archetype Leak*; rigetto immediato del payload. |

---

## 5. SOURCES Block

* [Cicchetti 1994](https://doi.org/10.1037/1040-3590.6.4.284) → Guidelines for evaluating agreement on normed assessment instruments
* [Cohen 1988](https://www.utstat.toronto.edu/~brunner/oldclass/378f16/readings/CohenPower.pdf) → Statistical Power Analysis for the Behavioral Sciences
* [Shrout & Fleiss 1979](https://doi.org/10.1037/0033-2909.86.2.420) → Intraclass Correlations: Uses in Assessing Rater Reliability
* [Nakajima et al. 2026](https://aclanthology.org/2026.findings-eacl.138/) → Inter-Rater Baselines in Multi-LLM Evaluation
* [Pingouin Statistics 2024](https://pingouin-stats.org/) → Statistical Package for Python (ANOVA & ICC)
* [ONTO-PROBE Research Framework 2026](THEORY-001.md) → OKF-DOC-2026-ONTO-THEORY-001
* [ONTO-PROBE Implementation Guide 2026](IMPL-001.md) → OKF-DOC-2026-ONTO-IMPL-001
* [ONTO-PROBE Benchmark Catalog 2026](BENCH-001.md) → OKF-DOC-2026-ONTO-BENCH-001
* [ONTO-PROBE Suite Analysis 2026](META-001.md) → OKF-DOC-2026-ONTO-META-001