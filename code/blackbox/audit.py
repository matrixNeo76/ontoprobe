"""Blinding HMAC e catena di audit a 5 campi (IMPL-001 §3.4, THEORY-001 §3.5)."""
import hashlib
import hmac
import json
import os
import secrets
import time
from pathlib import Path
from typing import Any, Dict


def load_or_create_key(path: Path) -> bytes:
    """Chiave segreta del PI. Per un doppio cieco reale va conservata FUORI dalla cartella condivisa con i referee."""
    env = os.environ.get("ONTO_HMAC_KEY")
    if env:
        return env.encode("utf-8")
    if path.exists():
        return path.read_bytes().strip()
    path.parent.mkdir(parents=True, exist_ok=True)
    key = secrets.token_hex(32).encode("utf-8")
    path.write_bytes(key)
    try:
        path.chmod(0o600)
    except OSError:
        pass
    return key


def blind_id(key: bytes, internal_id: str) -> str:
    digest = hmac.new(key, internal_id.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"BLIND-SAMPLE-{digest[:12]}"


class AuditChain:
    """Hash chain: Hash_i = SHA256(prev || internal_id || timestamp || stage || payload_hash)."""

    def __init__(self, path: Path):
        self.path = path
        self.last_hash = "0" * 64
        if path.exists():
            with path.open(encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        self.last_hash = json.loads(line)["block_hash"]

    def append(self, internal_id: str, stage: str, payload: Dict[str, Any]) -> str:
        ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        payload_hash = hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
        block_hash = hashlib.sha256(
            f"{self.last_hash}{internal_id}{ts}{stage}{payload_hash}".encode("utf-8")).hexdigest()
        rec = {"internal_sample_id": internal_id, "timestamp": ts, "stage": stage,
               "payload_hash": payload_hash, "prev_hash": self.last_hash, "block_hash": block_hash}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        self.last_hash = block_hash
        return block_hash

    @staticmethod
    def verify(path: Path) -> bool:
        prev = "0" * 64
        with path.open(encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                r = json.loads(line)
                raw = f"{prev}{r['internal_sample_id']}{r['timestamp']}{r['stage']}{r['payload_hash']}"
                if r["prev_hash"] != prev or hashlib.sha256(raw.encode("utf-8")).hexdigest() != r["block_hash"]:
                    return False
                prev = r["block_hash"]
        return True
