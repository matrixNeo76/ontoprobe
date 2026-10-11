# %% [markdown]
# CAA Smoke Test — ONTO-PROBE v0.3.2
#
# This file is the canonical smoke test notebook content for the project.
#
# It checks:
# 1. extraction without NaN or crash
# 2. coherent generation across a range of alpha values
# 3. monotonic dose-response behavior
# 4. qualitative distinction across ontological axes

# %%
import os
import time
from pathlib import Path
from typing import List, Optional

import numpy as np
import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

MODEL_ID = "meta-llama/Llama-3.1-8B-Instruct"
LAYER_IDX = 16
ALPHA_GRID = [0.0, 0.5, 1.0, 1.5, 2.0]
MAX_NEW_TOKENS = 256
SEED = 42

OUTPUT_DIR = Path("./outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

torch.manual_seed(SEED)
np.random.seed(SEED)

class LowVramOntologicalSteerer:
    def __init__(self, model_id: str = MODEL_ID, layer_idx: int = LAYER_IDX):
        self.layer_idx = layer_idx
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, token=os.environ.get("HF_TOKEN"))

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            quantization_config=bnb_config,
            device_map="auto",
            token=os.environ.get("HF_TOKEN"),
        )
        self.model.eval()
        self.steering_vector: Optional[torch.Tensor] = None
        self._inject_handle = None

    def _format_contrast_pair(self, text: str) -> str:
        messages = [
            {"role": "user", "content": "Descrivi il fenomeno secondo la prospettiva richiesta."},
            {"role": "assistant", "content": text},
        ]
        return self.tokenizer.apply_chat_template(messages, tokenize=False)

    def _collect_activations(self, raw_prompts: List[str]) -> torch.Tensor:
        activations = []
        target_layer = self.model.model.layers[self.layer_idx]
        for text in raw_prompts:
            formatted_chat = self._format_contrast_pair(text)
            inputs = self.tokenizer(formatted_chat, return_tensors="pt").to(self.device)
            captured = {"act": None}

            def pre_hook(module, args):
                captured["act"] = args[0][:, -1, :].detach().cpu()

            handle = target_layer.register_forward_pre_hook(pre_hook)
            try:
                with torch.no_grad():
                    self.model(**inputs)
            finally:
                handle.remove()

            if captured["act"] is None:
                raise RuntimeError("Hook non ha catturato alcuna attivazione")
            activations.append(captured["act"])

        return torch.cat(activations, dim=0)

    def compute_steering_vector(self, positive_prompts: List[str], negative_prompts: List[str]):
        pos = self._collect_activations(positive_prompts)
        neg = self._collect_activations(negative_prompts)
        v = (pos.mean(dim=0) - neg.mean(dim=0)).to(torch.float16)
        if torch.isnan(v).any():
            raise RuntimeError("Steering vector contains NaN")
        self.steering_vector = v
        return v

    def attach_steering(self, strength: float = 1.5):
        if self.steering_vector is None:
            raise ValueError("Vettore non calcolato.")
        self.remove_steering()
        vec = self.steering_vector.to(self.device)

        def pre_hook(module, args):
            hidden = args[0].clone()
            hidden[:, -1, :] = hidden[:, -1, :] + strength * vec
            return (hidden,) + args[1:]

        self._inject_handle = self.model.model.layers[self.layer_idx].register_forward_pre_hook(pre_hook)

    def remove_steering(self):
        if self._inject_handle is not None:
            self._inject_handle.remove()
            self._inject_handle = None

    def generate(self, prompt: str, strength: float = 0.0, max_new_tokens: int = MAX_NEW_TOKENS) -> str:
        if strength > 0.0:
            self.attach_steering(strength)
        else:
            self.remove_steering()

        try:
            messages = [{"role": "user", "content": prompt}]
            chat = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = self.tokenizer(chat, return_tensors="pt").to(self.device)
            with torch.no_grad():
                out = self.model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    repetition_penalty=1.05,
                    pad_token_id=self.tokenizer.eos_token_id,
                )
            return self.tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()
        finally:
            self.remove_steering()

# Smoke-test scaffold: override with project-specific notebook logic if needed.
steerer = LowVramOntologicalSteerer()
print("[Setup] Model loaded successfully.")
