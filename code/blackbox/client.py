"""Client per API compatibili con OpenAI (chat/completions) e client simulato per i test.

Configurazione tramite variabili d'ambiente:
  ONTO_API_KEY   chiave API (obbligatoria, tranne in modalità --mock)
  ONTO_API_BASE  endpoint base (default: https://openrouter.ai/api/v1, che dà accesso a
                 modelli di più fornitori con una sola chiave)
Solo libreria standard: nessuna dipendenza da installare.
"""
import hashlib
import json
import os
import random
import time
import urllib.error
import urllib.request
from typing import Dict, List, Optional

DEFAULT_BASE = "https://openrouter.ai/api/v1"


class LLMError(RuntimeError):
    pass


class LLMClient:
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None,
                 timeout: int = 120, max_retries: int = 4):
        self.api_key = api_key or os.environ.get("ONTO_API_KEY", "")
        self.base_url = (base_url or os.environ.get("ONTO_API_BASE") or DEFAULT_BASE).rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.calls = 0
        self.tokens_in = 0
        self.tokens_out = 0
        if not self.api_key:
            raise LLMError("ONTO_API_KEY non impostata. Esporta la chiave oppure usa --mock.")

    def chat(self, model: str, system: str, user: str, temperature: float = 0.7,
             max_tokens: int = 1500) -> str:
        return self.chat_messages(model, [{"role": "system", "content": system},
                                          {"role": "user", "content": user}],
                                  temperature, max_tokens)

    def chat_messages(self, model: str, messages: List[Dict[str, str]],
                      temperature: float = 0.7, max_tokens: int = 1500) -> str:
        body = json.dumps({"model": model, "messages": messages,
                           "temperature": temperature, "max_tokens": max_tokens}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions", data=body, method="POST",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"})
        last = None
        for attempt in range(self.max_retries):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    data = json.loads(r.read().decode("utf-8"))
                self.calls += 1
                usage = data.get("usage") or {}
                self.tokens_in += usage.get("prompt_tokens", 0)
                self.tokens_out += usage.get("completion_tokens", 0)
                return data["choices"][0]["message"]["content"] or ""
            except urllib.error.HTTPError as e:
                last = f"HTTP {e.code}: {e.read().decode('utf-8', 'ignore')[:200]}"
                e.close()
                if e.code not in (408, 409, 429, 500, 502, 503, 504):
                    break
            except (urllib.error.URLError, TimeoutError, KeyError, json.JSONDecodeError) as e:
                last = f"{type(e).__name__}: {e}"
            time.sleep(2 ** attempt)
        raise LLMError(f"Chiamata fallita per il modello {model}: {last}")


class MockClient:
    """Client deterministico e offline, per test e prove a secco della pipeline."""

    def __init__(self):
        self.calls = 0
        self.tokens_in = 0
        self.tokens_out = 0

    def chat(self, model: str, system: str, user: str, temperature: float = 0.7,
             max_tokens: int = 1500) -> str:
        return self.chat_messages(model, [{"role": "system", "content": system},
                                          {"role": "user", "content": user}], temperature, max_tokens)

    def chat_messages(self, model, messages, temperature=0.7, max_tokens=1500) -> str:
        self.calls += 1
        joined = "\n".join(m["content"] for m in messages)
        h = int(hashlib.sha256((model + joined).encode("utf-8")).hexdigest(), 16)
        rng = random.Random(h)
        if "FORMATO DI RISPOSTA RICHIESTO" in messages[0]["content"]:  # giudice
            return json.dumps({
                "appropriateness_score": round(rng.uniform(2.0, 5.0), 1),
                "logical_coherence_score": round(rng.uniform(2.0, 5.0), 1),
                "structural_novelty_score": round(rng.uniform(1.0, 4.5), 1),
                "taboo_violation_detected": rng.random() < 0.1,
                "identified_known_archetypes": ["archetipo-demo"],
                "reasoning_summary": "Valutazione simulata.",
            })
        return f"[mock:{model}] soluzione simulata {h % 100000} per: {messages[-1]['content'][:80]}"
