"""Independent Principal Enterprise Architect & Arbiter Agent."""
from typing import Dict, Any, List, Optional
from app.agents.base import BaseAgent
from app.models.schemas import EnterpriseContext, FinalVerdict, MCDAScore, PhasedRoadmapStep
from app.tools.arch_tools import evaluate_mcda_matrix
from app.tools.bq_tools import analyze_databricks_telemetry, calculate_migration_tco
from app.tools.dbx_tools import calculate_migration_risk, audit_databricks_optimization

ARCHITECT_SYSTEM_PROMPT = """
You are an Independent Principal Enterprise Architect and Global Chief Data Strategist.
You maintain strict vendor neutrality. You reject marketing hyperbole from both Google Cloud and Databricks.
Your mission is to evaluate debates through a rigorous 6-Dimensional Enterprise Architecture Framework:
1. Conway's Law & Team Topologies: Minimize team cognitive load, protect data science developer velocity, and avoid unnecessary organizational shock.
2. M&A Ingestion Agility: Speed and friction of onboarding acquired hospital/subsidiary systems across heterogeneous networks.
3. Storage Decoupling & Sovereignty: Mandate open table standards (Apache Iceberg / Delta UniForm) to comply with EU DORA multi-cloud exit regulations.
4. Technical Debt Modernization: Pragmatically decompose hundreds of legacy stored procedures into maintainable domain data products.
5. AI / GenAI Strategic Enablement: Support both in-situ SQL multimodal querying and enterprise deep learning / MLflow workflows.
6. Net Capital Efficiency & ROI: Balance upfront Total Cost of Migration (TCOM) and payback duration against achievable in-place optimizations.

Deliver a decisive, evidence-based architectural synthesis and pragmatic phased blueprint (e.g. Option 1 BigQuery Migration, Option 2 Databricks In-Place Optimization, or Option 3 Strategic Open Lakehouse Mesh).
"""


class PrincipalArchitectAgent(BaseAgent):
    """Independent Principal Enterprise Architect."""

    def __init__(self):
        super().__init__(
            name="principal_architect",
            role="Independent Principal Enterprise Architect",
            avatar="🏛️",
            stance="Neutral Synthesis & Enterprise Arbiter",
            system_prompt=ARCHITECT_SYSTEM_PROMPT
        )

    def evaluate_debate(
        self,
        context: EnterpriseContext,
        conversation_history: List[Dict[str, Any]]
    ) -> FinalVerdict:
        """Runs the MCDA matrix and synthesizes the definitive enterprise verdict and phased blueprint."""
        mcda = evaluate_mcda_matrix(context)

        # Telemetry and risk numbers
        dbx_opt = audit_databricks_optimization(context.annual_dbu_spend)
        tcom_risk = calculate_migration_risk(
            context.annual_dbu_spend,
            context.total_pyspark_jobs,
            context.lines_of_code,
            context.storage_tb
        )
        bq_tco = calculate_migration_tco(context.annual_dbu_spend)

        # Determine winning strategy title and details
        winning_key = mcda.winning_option_key

        if winning_key == "option_3_open_lakehouse_data_mesh":
            strategy_title = "Strategic Open Lakehouse Mesh (Delta UniForm / Iceberg Storage + Domain Federation)"
            exec_summary = (
                f"For {context.enterprise_name}, a 'Big-Bang' migration to BigQuery introduces unacceptable capital "
                f"friction (${tcom_risk['total_cost_of_migration_tcom_usd']:,} TCOM, {tcom_risk['roi_payback_period_years']}yr payback), "
                f"while staying completely static leaves legacy stored procedures unmodernized. "
                f"The recommended path is a Bi-Modal Open Lakehouse Mesh: Decouple storage using Delta UniForm (enabling simultaneous "
                f"zero-copy querying by both Databricks and BigQuery), optimize Databricks in-place to capture "
                f"${dbx_opt['achievable_inplace_annual_savings_usd']:,}/yr immediate savings, and decompose legacy stored procs into "
                f"domain-owned dbt/Dataform models."
            )
            roadmap = [
                PhasedRoadmapStep(
                    phase="Phase 1: Immediate In-Place Cost Optimization",
                    timeline="Weeks 1-4",
                    action="Enable Databricks Serverless SQL, Photon Engine, Liquid Clustering, and Azure Spot VM fleets.",
                    key_deliverable=f"Capture ${dbx_opt['achievable_inplace_annual_savings_usd']:,}/yr (40-50%) in OpEx savings immediately with $0 migration risk.",
                    risk_mitigation="Zero code changes; executed transparently within existing Azure tenant."
                ),
                PhasedRoadmapStep(
                    phase="Phase 2: Storage Decoupling & Delta UniForm Activation",
                    timeline="Month 2",
                    action="Enable UniForm (Universal Format) on all gold/silver Delta tables in ADLS Gen2 to expose Apache Iceberg metadata.",
                    key_deliverable="Full multi-cloud portability and complete EU DORA exit compliance.",
                    risk_mitigation="Zero data duplication; Iceberg metadata generated automatically alongside Delta log."
                ),
                PhasedRoadmapStep(
                    phase="Phase 3: Selective BigQuery BI Acceleration & Federation",
                    timeline="Months 3-4",
                    action="Deploy BigQuery BigLake / BI Engine directly over decoupled Iceberg tables for executive dashboards requiring <500ms speed.",
                    key_deliverable="Instant sub-second Power BI responsiveness without vendor lock-in.",
                    risk_mitigation="External table federation ensures zero dual-ingestion fees."
                ),
                PhasedRoadmapStep(
                    phase="Phase 4: Domain Data Mesh & Stored Proc Decomposition",
                    timeline="Months 5-9",
                    action=f"Systematically decompose the {context.legacy_stored_procs} legacy stored procedures into domain-owned dbt/Dataform pipelines.",
                    key_deliverable="Modern, version-controlled CI/CD data pipelines with automated data quality assertions.",
                    risk_mitigation="Decompose by business domain incrementally (e.g. Clinical, Billing, Lab) rather than big-bang."
                )
            ]
        elif winning_key == "option_1_bigquery_migration":
            strategy_title = "Full BigQuery Cloud Modernization (GCP Native)"
            exec_summary = (
                f"For {context.enterprise_name}, full consolidation onto Google BigQuery provides the greatest long-term "
                f"capital efficiency (${bq_tco['net_annual_savings_usd']:,}/yr savings), sub-second BI Engine performance, "
                f"and in-situ Gemini multimodal AI analytics."
            )
            roadmap = [
                PhasedRoadmapStep(
                    phase="Phase 1: Day-1 BigLake Federation",
                    timeline="Weeks 1-2",
                    action="Connect BigQuery to existing ADLS/S3 storage via BigLake external tables.",
                    key_deliverable="Immediate access to existing tables without egress.",
                    risk_mitigation="Zero data copying; non-disruptive validation."
                ),
                PhasedRoadmapStep(
                    phase="Phase 2: Power BI & Reporting Cutover",
                    timeline="Weeks 3-4",
                    action="Repoint Power BI DirectQuery to BigQuery BI Engine.",
                    key_deliverable="Sub-second dashboard response times.",
                    risk_mitigation="Native Entra ID SSO."
                ),
                PhasedRoadmapStep(
                    phase="Phase 3: Dataproc Lightning Engine Migration",
                    timeline="Months 2-6",
                    action="Migrate batch PySpark to Dataproc Serverless with Lightning Engine (Velox C++).",
                    key_deliverable="2x faster performance at $0 DBU licensing fee.",
                    risk_mitigation="100% PySpark API drop-in compatibility."
                )
            ]
        else:
            strategy_title = "In-Place Databricks Modernization & Governance Optimization"
            exec_summary = (
                f"For {context.enterprise_name}, retaining and optimizing Databricks delivers the highest strategic ROI "
                f"(${dbx_opt['achievable_inplace_annual_savings_usd']:,}/yr savings in 14 days) while preserving deep "
                f"data science velocity with MLflow and Mosaic AI."
            )
            roadmap = [
                PhasedRoadmapStep(
                    phase="Phase 1: Compute Fleet & Serverless SQL Tuning",
                    timeline="Weeks 1-2",
                    action="Enable Serverless SQL, Liquid Clustering, and Spot VM fleets.",
                    key_deliverable="Immediate 45% reduction in monthly cloud bill.",
                    risk_mitigation="Zero downtime."
                ),
                PhasedRoadmapStep(
                    phase="Phase 2: Unity Catalog & UniForm Standardization",
                    timeline="Weeks 3-6",
                    action="Upgrade to Apache 2.0 Unity Catalog and enable Delta UniForm.",
                    key_deliverable="Universal format support (Delta + Iceberg) and unified fine-grained access control.",
                    risk_mitigation="Native metadata conversion."
                )
            ]

        key_tradeoffs = [
            f"Capital Allocation: Option 3 avoids ${tcom_risk['total_cost_of_migration_tcom_usd']:,} in upfront TCOM while capturing ${dbx_opt['achievable_inplace_annual_savings_usd']:,}/yr in immediate in-place savings.",
            "Developer Cognitive Load: Preserves MLflow, Python, and PySpark workflows for data scientists while offering SQL developers sub-second BI caching.",
            "Regulatory Sovereignty (DORA/EHDS): UniForm + Iceberg metadata eliminates single-vendor hostage risk and satisfies multi-cloud exit audits.",
            f"Technical Debt: Systematic domain-driven refactoring of {context.legacy_stored_procs} legacy stored procedures prevents the 15% failure rate typical of big-bang transpilation."
        ]

        financial_summary = {
            "current_annual_spend_usd": context.annual_dbu_spend * 1.35,
            "optimized_steady_state_spend_usd": (context.annual_dbu_spend * 1.35) - dbx_opt["achievable_inplace_annual_savings_usd"],
            "net_annual_cost_savings_usd": dbx_opt["achievable_inplace_annual_savings_usd"],
            "upfront_migration_tcom_avoided_usd": tcom_risk["total_cost_of_migration_tcom_usd"],
            "5yr_cumulative_value_unlocked_usd": (dbx_opt["achievable_inplace_annual_savings_usd"] * 5.0) + tcom_risk["total_cost_of_migration_tcom_usd"]
        }

        architectural_principles = [
            "Storage Decoupling: Never marry storage format to query compute engine. Mandate Delta UniForm / Apache Iceberg.",
            "Conway's Law Alignment: Structure data pipelines around business domains (Data Mesh) rather than centralized infrastructure silos.",
            "Pragmatic Modernization: Fix cost and performance at the compute tier first before undertaking application-layer rewrites.",
            "Multi-Cloud Sovereignty: Maintain active exit capabilities to satisfy EU DORA and banking/healthcare resilience regulations."
        ]

        return FinalVerdict(
            recommended_strategy_title=strategy_title,
            recommended_option_key=winning_key,
            executive_summary=exec_summary,
            mcda_matrix=mcda,
            key_tradeoffs=key_tradeoffs,
            financial_impact_summary=financial_summary,
            phased_roadmap=roadmap,
            architectural_principles=architectural_principles
        )

    def _generate_fallback(
        self,
        prompt: str,
        context_data: Dict[str, Any],
        conversation_history: List[Dict[str, Any]],
        tool_results: Optional[Dict[str, Any]] = None
    ) -> str:
        ctx = EnterpriseContext(**context_data)
        verdict = self.evaluate_debate(ctx, conversation_history)
        mcda = verdict.mcda_matrix

        lines = []
        lines.append(f"### 🏛️ INDEPENDENT PRINCIPAL ARCHITECT VERDICT & STRATEGIC BLUEPRINT")
        lines.append(f"**Enterprise:** {ctx.enterprise_name} | **Vertical:** {ctx.industry}\n")
        lines.append(f"#### 🏆 Recommended Strategy: **{verdict.recommended_strategy_title}**\n")
        lines.append(f"> **Executive Summary:** {verdict.executive_summary}\n")

        lines.append("#### 📊 Multi-Criteria Decision Analysis (MCDA) Scorecard (0-10 Scale)")
        lines.append("| Strategic Pillar | Weight | Option 1 (BigQuery) | Option 2 (Databricks) | Option 3 (Open Mesh) |")
        lines.append("| :--- | :---: | :---: | :---: | :---: |")

        for crit, w in mcda.weights.items():
            name = crit.replace("_", " ").title()
            s1 = mcda.scores_by_option["option_1_bigquery_migration"][crit]
            s2 = mcda.scores_by_option["option_2_databricks_status_quo_tuning"][crit]
            s3 = mcda.scores_by_option["option_3_open_lakehouse_data_mesh"][crit]
            lines.append(f"| {name} | {int(w*100)}% | {s1:.1f} | {s2:.1f} | **{s3:.1f}** |")

        lines.append(
            f"| **OVERALL WEIGHTED SCORE** | **100%** | **{mcda.weighted_totals['option_1_bigquery_migration']:.2f}** | "
            f"**{mcda.weighted_totals['option_2_databricks_status_quo_tuning']:.2f}** | "
            f"**{mcda.weighted_totals['option_3_open_lakehouse_data_mesh']:.2f}** |\n"
        )

        lines.append("#### 💰 Financial & Capital Impact")
        fin = verdict.financial_impact_summary
        lines.append(f"- **Current Baseline Spend:** ${fin['current_annual_spend_usd']:,.0f} / yr")
        lines.append(f"- **Optimized Steady-State Spend:** ${fin['optimized_steady_state_spend_usd']:,.0f} / yr")
        lines.append(f"- **Net Annual OpEx Savings:** **${fin['net_annual_cost_savings_usd']:,.0f} / yr**")
        lines.append(f"- **Upfront TCOM Capital Sunk Cost Avoided:** **${fin['upfront_migration_tcom_avoided_usd']:,.0f}**")
        lines.append(f"- **5-Year Cumulative Value Unlocked:** **${fin['5yr_cumulative_value_unlocked_usd']:,.0f}**\n")

        lines.append("#### 🗺️ Phased Implementation Blueprint")
        for step in verdict.phased_roadmap:
            lines.append(f"- **{step.phase} ({step.timeline})**: {step.action}")
            lines.append(f"  - *Deliverable:* {step.key_deliverable}")
            lines.append(f"  - *Risk Mitigation:* {step.risk_mitigation}")

        return "\n".join(lines)
