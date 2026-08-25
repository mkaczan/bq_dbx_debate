"""BigQuery Enterprise Migration Strategist Agent."""
from typing import Dict, Any, List, Optional
from app.agents.base import BaseAgent
from app.tools.bq_tools import (
    analyze_databricks_telemetry,
    evaluate_powerbi_performance,
    calculate_migration_tco,
    generate_zero_copy_roadmap
)

BQ_SYSTEM_PROMPT = """
You are the Google BigQuery Enterprise Migration Strategist & Databricks Compete Specialist.
Your mission is to construct undeniable, mathematically sound, evidence-backed architectural arguments for migrating from Databricks to Google BigQuery.

Key Strategic Pillars to champion:
1. Fluid Scaling (True Per-Second Billing with Zero Cooldown): Eliminates the 60-second idle tax and cuts spiky query costs by up to 97%.
2. Dataproc Serverless with Lightning Engine: Native C++ vectorized execution (Velox / Gluten) delivering up to 2x faster performance than Databricks Photon at $0 DBU software markup.
3. BigLake Zero-Copy Federation: Query Delta Lake / Apache Iceberg tables in-place inside Azure ADLS Gen2 / AWS S3 with zero data egress and zero downtime on Day 1.
4. BI Engine Sub-Second Acceleration: Eliminates DAX queue bottlenecks for Power BI users (<600ms query latency) with zero dashboard or report rework.
5. Autonomous Background Clustering: Free autonomous storage optimization in Capacitor, eliminating the 15-30% 'Delta Maintenance Tax' (OPTIMIZE / VACUUM).
6. In-Situ Multimodal AI: Run Gemini multimodal models, embeddings, and BQML directly inside SQL queries without moving data to separate clusters.

Address objections sharply, cite concrete metrics ($ savings, latencies, concurrency limits), and expose legacy cluster sysadmin overhead.
"""


class BigQueryStrategistAgent(BaseAgent):
    """BigQuery Migration Strategist."""

    def __init__(self):
        super().__init__(
            name="bigquery_strategist",
            role="Google BigQuery Enterprise Strategist",
            avatar="🚀",
            stance="Migrate to Google Cloud & BigQuery",
            system_prompt=BQ_SYSTEM_PROMPT
        )

    def run_diagnostics(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Runs BQ forensic tools on the customer workload."""
        annual_dbus = context.get("annual_dbu_spend", 750000.0)
        storage_tb = context.get("storage_tb", 350.0)
        pyspark_jobs = context.get("total_pyspark_jobs", 120)
        pbi_users = context.get("powerbi_users_count", 75)

        telemetry = analyze_databricks_telemetry(annual_dbus, storage_tb, pyspark_jobs)
        powerbi = evaluate_powerbi_performance(pbi_users, "Medium")
        tco = calculate_migration_tco(annual_dbus)
        roadmap = generate_zero_copy_roadmap(storage_tb, pyspark_jobs)

        return {
            "telemetry_forensics": telemetry,
            "powerbi_concurrency": powerbi,
            "tco_model": tco,
            "zero_copy_roadmap": roadmap
        }

    def _generate_fallback(
        self,
        prompt: str,
        context_data: Dict[str, Any],
        conversation_history: List[Dict[str, Any]],
        tool_results: Optional[Dict[str, Any]] = None
    ) -> str:
        tools = tool_results or self.run_diagnostics(context_data)
        telemetry = tools.get("telemetry_forensics", {})
        tco = tools.get("tco_model", {})
        pbi = tools.get("powerbi_concurrency", {})
        roadmap = tools.get("zero_copy_roadmap", {})

        ent_name = context_data.get("enterprise_name", "Enterprise")
        dbu_spend = context_data.get("annual_dbu_spend", 750000.0)

        # Check if initial round or rebuttal
        is_rebuttal = len(conversation_history) > 1

        if not is_rebuttal:
            return f"""### 🎯 Executive Case for Google BigQuery Modernization: {ent_name}

To achieve true capital efficiency, sub-second BI responsiveness, and eliminate cluster sysadmin overhead, **{ent_name}** should execute a phased migration to Google Cloud:

#### 1. Demolishing the Dual-Bill & Delta Maintenance Tax
- **Current Annual Databricks Drain**: **${telemetry.get('total_current_databricks_spend_usd', dbu_spend*1.35):,} / year** (DBUs + Hyperscaler VM markup).
- **Identified Pure Infrastructure Waste**: **${telemetry.get('unnecessary_waste_breakdown', {}).get('total_annual_waste_usd', 220000):,} / year** ({telemetry.get('waste_percentage_of_total_bill', 28)}% of total bill) spent on idle interactive clusters and manual `OPTIMIZE`/`VACUUM` compaction routines.
- **BigQuery Fluid Scaling Advantage**: BigQuery's true per-second billing (`area-under-the-curve`) has **zero cooldown penalty** and autonomous background clustering at **$0 extra cost**, instantly unlocking **${tco.get('net_annual_savings_usd', 450000):,} / year net savings** ({tco.get('tco_reduction_percentage', '45%')} TCO reduction).

#### 2. Accelerating Power BI from {pbi.get('databricks_avg_dashboard_load_time_sec', 7.6)}s to <0.5s
- With **{pbi.get('concurrent_powerbi_users', 75)} concurrent analysts**, Databricks SQL Warehouses suffer severe DAX slot queuing ({pbi.get('databricks_queue_risk', 'HIGH')} queue risk).
- **BigQuery BI Engine** accelerates DirectQuery down to **{pbi.get('bigquery_bi_engine_load_time_sec', 0.45)}s** ({pbi.get('performance_speedup_factor', '8x faster')}) with native Entra ID / Azure AD SSO and **zero report redesign**.

#### 3. Day-1 Zero-Copy Federation via BigLake
- Eliminate the fear of a 12-month rewrite. **BigLake queries your {roadmap.get('storage_tb', 350)} TB of Delta Lake tables in-place** inside Azure ADLS Gen2 with **0 downtime** and **$0 egress** on Day 1.
- Modernize batch ETL to **Dataproc Serverless with Lightning Engine (Velox C++)**, delivering up to **2x faster execution than Databricks Photon** at **0 DBU software licensing fee**.
"""
        else:
            return f"""### 🛡️ BigQuery Counter-Rebuttal & Myth-Busting

Let's dismantle the fear-based objections regarding refactoring risks, lock-in, and streaming:

#### 1. The 'PySpark Rewrite' Myth vs Dataproc Lightning Engine
- We do **not** force teams into pure SQL. **Dataproc Serverless with Lightning Engine** provides **100% drop-in API compatibility for existing PySpark DataFrame and Spark SQL code**.
- Vectorized execution is powered by **native C++ SIMD (Apache Gluten & Velox)**—outperforming Databricks Photon by up to **2x on Parquet/Delta data** without paying premium Photon DBU multipliers.

#### 2. Openness: BigLake & Apache Iceberg Parity
- BigQuery is fully open: **BigLake natively reads Delta Lake, Apache Iceberg, and Apache Hudi**.
- Google Cloud does not lock data into proprietary silos. Tables can reside in Cloud Storage or Azure ADLS, queryable across platforms while BigQuery provides enterprise governance and sub-second BI caching.

#### 3. Real-Time Streaming & AI Consolidation
- Replace fragile custom Delta Live Table (DLT) maintenance with **BigQuery continuous streaming & Storage Write API** or **Cloud Dataflow** with built-in auto-healing.
- Run **multimodal Gemini models directly inside standard BigQuery SQL** (`ML.GENERATE_TEXT`) without spinning up separate MLflow clusters or custom GPU VMs.
"""
