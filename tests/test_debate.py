"""Unit and integration tests for bq_dbx_debate application."""
import unittest
from app.models.schemas import EnterpriseContext, DebateSession, DebateTurn, StartDebateRequest, StepDebateRequest, InterveneDebateRequest
from app.engine.presets import PRESET_SCENARIOS
from app.engine.orchestrator import DebateOrchestrator
from app.tools.bq_tools import (
    analyze_databricks_telemetry,
    evaluate_powerbi_performance,
    calculate_migration_tco,
    generate_zero_copy_roadmap,
)
from app.tools.dbx_tools import (
    analyze_spark_compatibility,
    calculate_migration_risk,
    calculate_hidden_bq_costs,
    audit_databricks_optimization,
)
from app.tools.arch_tools import evaluate_mcda_matrix
from app.agents.bq_strategist import BigQueryStrategistAgent
from app.agents.dbx_advocate import DatabricksAdvocateAgent
from app.agents.principal_architect import PrincipalArchitectAgent


class TestDebateApp(unittest.TestCase):

    def setUp(self):
        self.preset_keys = list(PRESET_SCENARIOS.keys())
        self.sample_context = PRESET_SCENARIOS["healthcare_m_and_a"]

    def test_presets_exist(self):
        self.assertGreaterEqual(len(self.preset_keys), 4)
        for key, ctx in PRESET_SCENARIOS.items():
            self.assertIsInstance(ctx, EnterpriseContext)
            self.assertGreater(ctx.annual_dbu_spend, 0)
            self.assertGreater(ctx.storage_tb, 0)
            self.assertGreater(ctx.total_pyspark_jobs, 0)

    def test_bq_tools(self):
        telemetry = analyze_databricks_telemetry(750000.0, 350.0, 120)
        self.assertIn("total_current_databricks_spend_usd", telemetry)
        self.assertIn("unnecessary_waste_breakdown", telemetry)
        self.assertGreater(telemetry["waste_percentage_of_total_bill"], 0)

        pbi = evaluate_powerbi_performance(75, "Medium")
        self.assertIn("performance_speedup_factor", pbi)
        self.assertLess(pbi["bigquery_bi_engine_load_time_sec"], pbi["databricks_avg_dashboard_load_time_sec"])

        tco = calculate_migration_tco(750000.0)
        self.assertIn("net_annual_savings_usd", tco)
        self.assertGreater(tco["net_annual_savings_usd"], 0)

        roadmap = generate_zero_copy_roadmap(350.0, 120)
        self.assertEqual(len(roadmap["phased_approach"]), 3)

    def test_dbx_tools(self):
        compat = analyze_spark_compatibility(120, 95000, 35, 12)
        self.assertIn("friction_breakdown", compat)
        self.assertGreater(compat["total_engineering_rewrite_hours"], 0)

        risk = calculate_migration_risk(750000.0, 120, 95000, 350.0)
        self.assertIn("total_cost_of_migration_tcom_usd", risk)
        self.assertGreater(risk["total_cost_of_migration_tcom_usd"], 0)

        hidden = calculate_hidden_bq_costs(350.0)
        self.assertIn("annual_hidden_costs_usd", hidden)
        self.assertGreater(hidden["annual_hidden_costs_usd"], 0)

        opt = audit_databricks_optimization(750000.0)
        self.assertIn("achievable_inplace_annual_savings_usd", opt)
        self.assertGreater(opt["achievable_inplace_annual_savings_usd"], 0)

    def test_arch_mcda_tool(self):
        mcda = evaluate_mcda_matrix(self.sample_context)
        self.assertIn("option_1_bigquery_migration", mcda.weighted_totals)
        self.assertIn("option_2_databricks_status_quo_tuning", mcda.weighted_totals)
        self.assertIn("option_3_open_lakehouse_data_mesh", mcda.weighted_totals)
        self.assertAlmostEqual(sum(mcda.weights.values()), 1.0, places=1)
        self.assertIsNotNone(mcda.winning_option_key)

    def test_agent_responses(self):
        bq_agent = BigQueryStrategistAgent()
        dbx_agent = DatabricksAdvocateAgent()
        arch_agent = PrincipalArchitectAgent()

        ctx_dict = self.sample_context.model_dump()

        bq_diag = bq_agent.run_diagnostics(ctx_dict)
        self.assertIn("telemetry_forensics", bq_diag)
        bq_res = bq_agent.generate_response("Pitch BQ", ctx_dict, [], bq_diag)
        self.assertIn("BigQuery", bq_res)

        dbx_diag = dbx_agent.run_diagnostics(ctx_dict)
        self.assertIn("spark_compatibility", dbx_diag)
        dbx_res = dbx_agent.generate_response("Defend DBX", ctx_dict, [{"speaker": "bigquery_strategist", "content": bq_res}], dbx_diag)
        self.assertIn("Databricks", dbx_res)

        verdict = arch_agent.evaluate_debate(self.sample_context, [])
        self.assertIsNotNone(verdict.recommended_strategy_title)
        self.assertGreater(len(verdict.phased_roadmap), 0)

    def test_orchestrator_flow(self):
        orch = DebateOrchestrator()
        session = orch.create_session(self.sample_context, rounds=1)
        self.assertEqual(session.status, "in_progress")
        self.assertEqual(len(session.turns), 0)

        # Turn 1: BQ
        t1 = orch.execute_next_turn(session.session_id)
        self.assertIsNotNone(t1)
        self.assertEqual(t1.speaker, "bigquery_strategist")

        # Turn 2: DBX
        t2 = orch.execute_next_turn(session.session_id)
        self.assertIsNotNone(t2)
        self.assertEqual(t2.speaker, "databricks_advocate")

        # Turn 3: Architect Verdict (since rounds=1 -> 2 speaker turns + 1 verdict)
        t3 = orch.execute_next_turn(session.session_id)
        self.assertIsNotNone(t3)
        self.assertEqual(t3.speaker, "principal_architect")
        self.assertEqual(session.status, "completed")
        self.assertIsNotNone(session.final_verdict)

    def test_orchestrator_user_intervention(self):
        orch = DebateOrchestrator()
        session = orch.create_session(self.sample_context, rounds=2)
        t1 = orch.execute_next_turn(session.session_id)
        self.assertIsNotNone(t1)

        user_turn = orch.inject_user_intervention(session.session_id, "What about EU DORA regulation?")
        self.assertEqual(user_turn.speaker, "user")
        self.assertIn("EU DORA", user_turn.content)


if __name__ == "__main__":
    unittest.main()
