"""Test offline del percorso black-box. Esecuzione: python -m unittest discover -s code/tests"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from blackbox import pipeline as P  # noqa: E402
from blackbox.audit import AuditChain, blind_id  # noqa: E402
from blackbox.client import LLMClient, LLMError, MockClient  # noqa: E402
from blackbox.judges import JudgeParseError, parse_judgment  # noqa: E402
from blackbox.stats import aggregate_dossier, bootstrap_diff, icc2k  # noqa: E402

GOOD = {"appropriateness_score": 4, "logical_coherence_score": 3.5, "structural_novelty_score": 3,
        "taboo_violation_detected": False, "identified_known_archetypes": [], "reasoning_summary": "ok"}


class TestStats(unittest.TestCase):
    def test_icc2k_shrout_fleiss(self):
        # Esempio di Shrout & Fleiss (1979): ICC(2,k) = 0.62
        m = [[9, 2, 5, 8], [6, 1, 3, 2], [8, 4, 6, 8], [7, 1, 2, 6], [10, 5, 6, 9], [6, 2, 4, 7]]
        self.assertAlmostEqual(icc2k(m), 0.62, places=2)

    def test_icc_none_when_too_small(self):
        self.assertIsNone(icc2k([[1, 2]]))

    def test_gate_zeroes_novelty_on_low_appropriateness(self):
        j = [dict(GOOD, appropriateness_score=1.5, structural_novelty_score=5.0) for _ in range(3)]
        agg = aggregate_dossier(j)
        self.assertFalse(agg["gate_passed"])
        self.assertEqual(agg["gated_novelty"], 0.0)

    def test_gate_zeroes_novelty_on_taboo_majority(self):
        j = [dict(GOOD, taboo_violation_detected=True), dict(GOOD, taboo_violation_detected=True), dict(GOOD)]
        agg = aggregate_dossier(j)
        self.assertTrue(agg["taboo_leak"])
        self.assertEqual(agg["gated_novelty"], 0.0)

    def test_gated_novelty_normalised(self):
        j = [dict(GOOD, structural_novelty_score=5.0) for _ in range(3)]
        self.assertAlmostEqual(aggregate_dossier(j)["gated_novelty"], 1.0)

    def test_escalation_on_disagreement(self):
        j = [dict(GOOD, structural_novelty_score=1.0), dict(GOOD, structural_novelty_score=4.0), dict(GOOD)]
        self.assertTrue(aggregate_dossier(j)["escalate_to_human"])

    def test_bootstrap_detects_clear_difference(self):
        a = {f"t{i}": 0.8 for i in range(8)}
        b = {f"t{i}": 0.2 for i in range(8)}
        r = bootstrap_diff(a, b)
        self.assertAlmostEqual(r["mean_diff"], 0.6)
        self.assertGreater(r["ci_low"], 0)

    def test_bootstrap_needs_three_tasks(self):
        self.assertIsNone(bootstrap_diff({"a": 1.0}, {"a": 0.0}))


class TestJudgeParsing(unittest.TestCase):
    def test_parses_json_with_surrounding_text(self):
        out = parse_judgment("Ecco:\n```json\n" + json.dumps(GOOD) + "\n```")
        self.assertEqual(out["appropriateness_score"], 4.0)

    def test_rejects_out_of_range(self):
        with self.assertRaises(JudgeParseError):
            parse_judgment(json.dumps(dict(GOOD, appropriateness_score=7)))

    def test_rejects_missing_field(self):
        bad = dict(GOOD); del bad["structural_novelty_score"]
        with self.assertRaises(JudgeParseError):
            parse_judgment(json.dumps(bad))

    def test_rejects_non_json(self):
        with self.assertRaises(JudgeParseError):
            parse_judgment("non lo so")

    def test_accepts_string_boolean(self):
        self.assertTrue(parse_judgment(json.dumps(dict(GOOD, taboo_violation_detected="true")))["taboo_violation_detected"])


class TestAudit(unittest.TestCase):
    def test_chain_verifies_and_detects_tampering(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "audit.jsonl"
            chain = AuditChain(p)
            for i in range(3):
                chain.append(f"id{i}", "generation", {"x": i})
            self.assertTrue(AuditChain.verify(p))
            lines = p.read_text().splitlines()
            rec = json.loads(lines[1]); rec["stage"] = "manomesso"; lines[1] = json.dumps(rec)
            p.write_text("\n".join(lines) + "\n")
            self.assertFalse(AuditChain.verify(p))

    def test_blind_id_deterministic_and_keyed(self):
        self.assertEqual(blind_id(b"k", "a"), blind_id(b"k", "a"))
        self.assertNotEqual(blind_id(b"k", "a"), blind_id(b"k2", "a"))
        self.assertTrue(blind_id(b"k", "a").startswith("BLIND-SAMPLE-"))


class TestTasks(unittest.TestCase):
    def test_thirty_binary_b_tasks(self):
        tasks = P.load_tasks()
        self.assertEqual(len(tasks), 30)
        self.assertEqual({t["id"] for t in tasks}, {f"ONTO-B{n}" for n in range(21, 51)})

    def test_limit_is_balanced_across_domains(self):
        doms = [t["domain"] for t in P.load_tasks(limit=6)]
        self.assertEqual({d: doms.count(d) for d in set(doms)}, {"system_design": 2, "policy": 2, "information_theory": 2})


class TestHttpClient(unittest.TestCase):
    """Il client reale contro un server locale che imita /chat/completions."""

    def _serve(self, statuses):
        import threading
        from http.server import BaseHTTPRequestHandler, HTTPServer
        seen = {"auth": None, "body": None, "n": 0}

        class H(BaseHTTPRequestHandler):
            def do_POST(self):
                seen["n"] += 1
                seen["auth"] = self.headers.get("Authorization")
                seen["body"] = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                code = statuses[min(seen["n"] - 1, len(statuses) - 1)]
                payload = json.dumps({"choices": [{"message": {"content": "ciao"}}],
                                      "usage": {"prompt_tokens": 7, "completion_tokens": 3}}
                                     if code == 200 else {"error": "x"}).encode()
                self.send_response(code); self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload))); self.end_headers(); self.wfile.write(payload)

            def log_message(self, *a):
                pass

        srv = HTTPServer(("127.0.0.1", 0), H)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        self.addCleanup(srv.shutdown)
        return f"http://127.0.0.1:{srv.server_port}", seen

    def test_success_and_headers(self):
        base, seen = self._serve([200])
        c = LLMClient(api_key="k", base_url=base)
        self.assertEqual(c.chat("m", "sys", "usr"), "ciao")
        self.assertEqual(seen["auth"], "Bearer k")
        self.assertEqual(seen["body"]["messages"][0]["role"], "system")
        self.assertEqual((c.tokens_in, c.tokens_out), (7, 3))

    def test_retries_on_server_error(self):
        import blackbox.client as bc
        orig, bc.time.sleep = bc.time.sleep, lambda *_: None
        self.addCleanup(setattr, bc.time, "sleep", orig)
        base, seen = self._serve([500, 200])
        self.assertEqual(LLMClient(api_key="k", base_url=base).chat("m", "s", "u"), "ciao")
        self.assertEqual(seen["n"], 2)

    def test_no_retry_on_auth_error(self):
        base, seen = self._serve([401])
        with self.assertRaises(LLMError):
            LLMClient(api_key="k", base_url=base).chat("m", "s", "u")
        self.assertEqual(seen["n"], 1)

    def test_missing_key_raises(self):
        import os
        old = os.environ.pop("ONTO_API_KEY", None)
        try:
            with self.assertRaises(LLMError):
                LLMClient()
        finally:
            if old is not None:
                os.environ["ONTO_API_KEY"] = old


class TestEndToEnd(unittest.TestCase):
    def test_mock_run_and_resume(self):
        judges = ["m1", "m2", "m3"]
        with tempfile.TemporaryDirectory() as d:
            run = Path(d) / "r"
            client = MockClient()
            tasks = P.load_tasks(limit=6)
            n = P.generate(client, run, tasks, "gen", reps=1, n_worlds=2, log=lambda *_: None)
            self.assertEqual(n, 18)
            self.assertEqual(client.calls, 6 * (1 + 3 + 6))
            nj = P.judge(client, run, judges, log=lambda *_: None)
            self.assertEqual(nj, 54)
            summary = P.analyze(run, judges)
            self.assertEqual(summary["n_judged"], 18)
            self.assertEqual(set(summary["conditions"]), {"C1", "C2", "C3"})
            self.assertTrue((run / "report.md").exists())
            self.assertTrue(AuditChain.verify(run / "audit.jsonl"))
            # i giudici non devono ricevere condizione, ruoli o modello: il prompt contiene solo problema e testo
            blind = [json.loads(l) for l in (run / "blind_dossiers.jsonl").read_text().splitlines()]
            self.assertEqual(set(blind[0]), {"blind_id", "problem", "taboo", "text"})
            # riprendibilità: rilanciando non si rifà nulla
            c2 = MockClient()
            self.assertEqual(P.generate(c2, run, tasks, "gen", reps=1, n_worlds=2, log=lambda *_: None), 0)
            self.assertEqual(P.judge(c2, run, judges, log=lambda *_: None), 0)
            self.assertEqual(c2.calls, 0)


if __name__ == "__main__":
    unittest.main()
