"""Databricks Principal Solutions Architect & Defense Advocate Agent."""
from typing import Dict, Any, List, Optional
from app.agents.base import BaseAgent
from app.tools.dbx_tools import (
    analyze_spark_compatibility,
    calculate_migration_risk,
    calculate_hidden_bq_costs,
    audit_databricks_optimization
)

DBX_SYSTEM_PROMPT = """
You are the Databricks Principal Solutions Architect & Lakehouse Defense Strategist.
Your mission is to critically interrogate BigQuery migration pitches, expose architectural loopholes in Google Cloud sales claims, quantify the hidden risks and catastrophic costs of migrating off Databricks, and construct an airtight case for retaining and optimizing Databricks in-place.

Key Architectural Loopholes & Weapons to deploy:
1. The 'Zero-Copy BigLake' Latency Mirage: External table queries over ADLS/S3 lack native Delta caching and Photon SIMD acceleration—queries run 3x-8x slower and incur heavy cross-cloud network egress penalties.
2. The 'bigframes' & PySpark Transpilation Trap: bigframes is a SQL transpiler, not Spark. It immediately fails on Python UDFs, distributed RDD transformations (mapPartitions), and custom MLlib pipelines, requiring 100+ engineer hours per pipeline.
3. True Total Cost of Migration (TCOM): Moving off Databricks triggers a 12-18 month engineering freeze, $1M+ in consultant rewriting fees, dual-run platform taxes, and high risk of data scientist attrition.
4. Hidden BigQuery Fees & Slot Starvation: Expose Storage Write API ingestion fees ($0.025/GB), BI Engine RAM reservations ($30.36/GB/mo), and morning BI queue freezes caused by fixed slot caps.
5. In-Place Databricks Optimization Playbook: Enabling Serverless Compute, Photon Engine, Liquid Clustering, and Spot Fleets yields 40-55% immediate cost reduction with ZERO migration risk.
6. Open Lakehouse & Unity Catalog (Apache 2.0): Unity Catalog is open-sourced; Delta UniForm allows tables to be read as Iceberg/Hudi simultaneously without data duplication, guaranteeing true multi-cloud portability and EU DORA compliance.

Dismantle vendor marketing claims with technical forensics, codebase incompatibilities, and realistic TCOM models.
"""


class DatabricksAdvocateAgent(BaseAgent):
    """Databricks Defense Advocate."""

    def __init__(self):
        super().__init__(
            name="databricks_advocate",
            role="Databricks Principal Solutions Architect",
            avatar="⚡",
            stance="Retain & Optimize Databricks Lakehouse",
            system_prompt=DBX_SYSTEM_PROMPT
        )

    def run_diagnostics(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Runs DBX defense tools and loophole calculators."""
        annual_dbus = context.get("annual_dbu_spend", 750000.0)
        storage_tb = context.get("storage_tb", 350.0)
        pyspark_jobs = context.get("total_pyspark_jobs", 120)
        loc = context.get("lines_of_code", 95000)
        mlflow_models = context.get("mlflow_models_count", 35)
        streaming = context.get("streaming_pipelines_count", 12)

        compat = analyze_spark_compatibility(pyspark_jobs, loc, mlflow_models, streaming)
        risk = calculate_migration_risk(annual_dbus, pyspark_jobs, loc, storage_tb)
        hidden = calculate_hidden_bq_costs(storage_tb)
        optimization = audit_databricks_optimization(annual_dbus)

        return {
            "spark_compatibility": compat,
            "migration_risk_tcom": risk,
            "hidden_bq_costs": hidden,
            "inplace_optimization": optimization
        }

    def _generate_fallback(
        self,
        prompt: str,
        context_data: Dict[str, Any],
        conversation_history: List[Dict[str, Any]],
        tool_results: Optional[Dict[str, Any]] = None
    ) -> str:
        tools = tool_results or self.run_diagnostics(context_data)
        compat = tools.get("spark_compatibility", {})
        risk = tools.get("migration_risk_tcom", {})
        hidden = tools.get("hidden_bq_costs", {})
        opt = tools.get("inplace_optimization", {})

        ent_name = context_data.get("enterprise_name", "Enterprise")
        dbu_spend = context_data.get("annual_dbu_spend", 750000.0)

        is_rebuttal = len(conversation_history) > 1

        if not is_rebuttal:
            return f"""### ⚠️ Architectural Defense & Forensic Reality Check: {ent_name}

Before **{ent_name}** commits to a high-risk, multi-million-dollar migration sinkhole, let's look at the cold technical and financial facts:

#### 1. The Catastrophic Total Cost of Migration (TCOM)
- **The $1.5M+ Migration Trap**: A migration of **{context_data.get('total_pyspark_jobs', 120)} PySpark pipelines** and **{context_data.get('lines_of_code', 95000):,} LOC** will require **{compat.get('total_engineering_rewrite_hours', 1800):,.0f} engineering refactoring hours** (**${compat.get('total_refactoring_consulting_cost_usd', 315000):,}** in direct coding costs).
- **Total TCOM**: When factoring in a **{risk.get('migration_duration_months', 12)}-month dual-platform parallel run tax**, egress fees, and team retraining, the true migration cost is **${risk.get('total_cost_of_migration_tcom_usd', 1250000):,}**, requiring a **{risk.get('roi_payback_period_years', 4.8)}-year payback period**!

#### 2. The 3 Fatal Loopholes in the BigQuery Pitch
1. **'BigLake Zero-Copy' Latency Mirage**: Running external table queries against ADLS Gen2 from BigQuery lacks native Photon C++ SIMD vectorization and Delta file skipping. Queries run **3x to 8x slower** and incur continuous cross-cloud network egress fees (**${hidden.get('breakdown', {}).get('biglake_cross_cloud_egress_usd', 68000):,}/yr**).
2. **`bigframes` Is NOT Spark**: `bigframes` is merely a SQL compiler. It **instantly crashes** on custom Python UDFs, distributed RDDs (`mapPartitions`), and MLflow models.
3. **Hidden BigQuery Fees**: Storage Write API ($0.025/GB), dedicated BI Engine RAM ($30.36/GB/mo), and slot contention overages add **${hidden.get('annual_hidden_costs_usd', 185000):,}/yr** in unbudgeted surcharges.

#### 3. The Modern Databricks In-Place Optimization Alternative
- We can deliver an immediate **${opt.get('achievable_inplace_annual_savings_usd', 420000):,} / year cost reduction** ({opt.get('immediate_cost_reduction_pct', '42%')} savings) in **14 days** with **$0 upfront migration spend** and **ZERO operational risk**:
  - Enable **Serverless SQL** (instant sub-second scale-to-zero for Power BI).
  - Activate **Photon Engine & Liquid Clustering** (eliminates manual OPTIMIZE/VACUUM overhead).
  - Deploy **Spot Fleets** (70-90% discount on Azure VM compute).
  - Maintain **Open Unity Catalog (Apache 2.0)** and **Delta UniForm (Iceberg)** for total multi-cloud data sovereignty and EU DORA compliance.
"""
        else:
            return f"""### 💥 Databricks Rebuttal: Exposing the Google Cloud Silos

Google Cloud claims seamlessness, but enterprise practitioners know the operational reality:

#### 1. Data & AI Fragmentation: 1 Workspace vs 8 GCP Portals
- On Databricks, data engineering, feature stores, **MLflow experiment tracking, model registry, Ray distributed clusters, and Mosaic AI** operate in a **single unified collaborative workspace**.
- Migrating to GCP fractures your data science team across BigQuery, Vertex AI Workbench, Vertex Pipelines, Vertex Feature Store, Artifact Registry, and Cloud Functions—each with disconnected IAM, separate quotas, and disjointed UX.

#### 2. Openness: Unity Catalog (Apache 2.0) vs BigQuery Monolith
- Databricks open-sourced **Unity Catalog under Apache 2.0**. With **UniForm (Universal Format)**, your Delta tables can be read natively as Apache Iceberg or Apache Hudi with zero data duplication.
- BigQuery's storage engine (Capacitor) and Dremel execution scheduler are proprietary to Google Cloud. Migrating core data warehouse assets into BigQuery destroys multi-cloud portability and directly threatens **EU DORA exit readiness**.

#### 3. Real-Time Streaming: DLT Notebooks vs Cloud Dataflow Nightmare
- Databricks Delta Live Tables (DLT) provides declarative, auto-scaling streaming pipelines with built-in data quality expectations (`EXPECT ... ON VIOLATION`) in a single Python notebook.
- Replicating this on GCP requires managing Apache Beam / Cloud Dataflow (separate Java runtime), Cloud Pub/Sub, and Storage Write API—trading 1 elegant engine for 3 complex distributed systems.
"""
