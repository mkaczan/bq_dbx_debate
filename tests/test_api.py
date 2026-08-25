"""API endpoint integration tests."""
import unittest
from fastapi.testclient import TestClient
from app.server.api import app
from app.engine.presets import PRESET_SCENARIOS


class TestApiEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.sample_context = PRESET_SCENARIOS["healthcare_m_and_a"].model_dump()

    def test_get_presets(self):
        response = self.client.get("/api/presets")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("healthcare_m_and_a", data)
        self.assertIn("retail_omnichannel", data)

    def test_start_debate(self):
        payload = {
            "context": self.sample_context,
            "rounds": 1
        }
        response = self.client.post("/api/debate/start", json=payload)
        self.assertEqual(response.status_code, 200)
        session = response.json()
        self.assertIn("session_id", session)
        self.assertEqual(session["status"], "in_progress")
        self.assertEqual(len(session["turns"]), 0)

    def test_step_debate_flow(self):
        start_res = self.client.post("/api/debate/start", json={"context": self.sample_context, "rounds": 1})
        session_id = start_res.json()["session_id"]

        step1 = self.client.post("/api/debate/step", json={"session_id": session_id})
        self.assertEqual(step1.status_code, 200)
        data1 = step1.json()
        self.assertIsNotNone(data1["turn"])
        self.assertEqual(data1["turn"]["speaker"], "bigquery_strategist")
        self.assertFalse(data1["is_completed"])

        step2 = self.client.post("/api/debate/step", json={"session_id": session_id})
        self.assertEqual(step2.status_code, 200)
        data2 = step2.json()
        self.assertEqual(data2["turn"]["speaker"], "databricks_advocate")

        step3 = self.client.post("/api/debate/step", json={"session_id": session_id})
        self.assertEqual(step3.status_code, 200)
        data3 = step3.json()
        self.assertEqual(data3["turn"]["speaker"], "principal_architect")
        self.assertTrue(data3["is_completed"])
        self.assertIsNotNone(data3["session"]["final_verdict"])

    def test_run_all_and_export(self):
        start_res = self.client.post("/api/debate/start", json={"context": self.sample_context, "rounds": 1})
        session_id = start_res.json()["session_id"]

        run_all = self.client.post("/api/debate/run-all", json={"session_id": session_id})
        self.assertEqual(run_all.status_code, 200)
        session = run_all.json()
        self.assertEqual(session["status"], "completed")
        self.assertIsNotNone(session["final_verdict"])

        md_res = self.client.get(f"/api/export/markdown/{session_id}")
        self.assertEqual(md_res.status_code, 200)
        self.assertIn("Strategic Enterprise Data Platform Debate", md_res.text)

    def test_user_intervention(self):
        start_res = self.client.post("/api/debate/start", json={"context": self.sample_context, "rounds": 2})
        session_id = start_res.json()["session_id"]

        self.client.post("/api/debate/step", json={"session_id": session_id})

        intervene_res = self.client.post("/api/debate/intervene", json={
            "session_id": session_id,
            "user_prompt": "Can we achieve sub-second Power BI refreshes without migrating storage?"
        })
        self.assertEqual(intervene_res.status_code, 200)
        data = intervene_res.json()
        self.assertIsNotNone(data["user_turn"])
        self.assertIsNotNone(data["agent_turn"])

    def test_diagnostics_tool(self):
        response = self.client.post("/api/tools/diagnostics", json=self.sample_context)
        self.assertEqual(response.status_code, 200)
        diag = response.json()
        self.assertIn("bigquery_forensics", diag)
        self.assertIn("databricks_forensics", diag)
        self.assertIn("mcda_matrix", diag)

    def test_static_index_html(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("BigQuery vs Databricks Strategic Debate Arena", response.text)

    def test_health_and_json_export(self):
        health = self.client.get("/api/health")
        self.assertEqual(health.status_code, 200)
        self.assertEqual(health.json()["status"], "healthy")

        start_res = self.client.post("/api/debate/start", json={"context": self.sample_context, "rounds": 1})
        session_id = start_res.json()["session_id"]
        json_res = self.client.get(f"/api/export/json/{session_id}")
        self.assertEqual(json_res.status_code, 200)
        self.assertEqual(json_res.json()["session_id"], session_id)


if __name__ == "__main__":
    unittest.main()
