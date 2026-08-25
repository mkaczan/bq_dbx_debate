"""Multi-Criteria Decision Analysis (MCDA) matrix tool for the Principal Architect."""
from typing import Dict, Any
from app.models.schemas import EnterpriseContext, MCDAScore


def evaluate_mcda_matrix(context: EnterpriseContext) -> MCDAScore:
    """Evaluates 7-dimensional enterprise architecture trade-offs dynamically adjusted to customer context."""
    # Dynamic weight calculation based on context
    w_m_and_a = 0.15 + (0.05 if context.m_and_a_acquisitions_per_year >= 2 else 0.0)
    w_reg = 0.15 + (0.05 if "DORA" in context.regulatory_framework or "GDPR" in context.regulatory_framework else 0.0)
    w_legacy = 0.15 + (0.05 if context.legacy_stored_procs > 500 else 0.0)
    w_storage = 0.15 + (0.05 if "Multi-Cloud" in context.cloud_strategy else 0.0)
    w_org = 0.15
    w_ai = 0.10
    w_tco = 0.15

    # Normalize weights to sum to 1.0
    total_raw_w = w_m_and_a + w_reg + w_legacy + w_storage + w_org + w_ai + w_tco
    weights = {
        "m_and_a_agility": round(w_m_and_a / total_raw_w, 2),
        "org_operating_model": round(w_org / total_raw_w, 2),
        "regulatory_sovereignty_dora": round(w_reg / total_raw_w, 2),
        "technical_debt_modernization": round(w_legacy / total_raw_w, 2),
        "storage_neutrality_open_formats": round(w_storage / total_raw_w, 2),
        "ai_ml_maturity": round(w_ai / total_raw_w, 2),
        "capital_efficiency_5yr_tco": round(w_tco / total_raw_w, 2),
    }
    # Ensure exact 1.0 sum
    diff = 1.0 - sum(weights.values())
    weights["m_and_a_agility"] = round(weights["m_and_a_agility"] + diff, 2)

    # Option 1: Big-Bang BigQuery Migration (GCP Monolith)
    # Option 2: Databricks In-Place Optimization (Status Quo Tuning)
    # Option 3: Strategic Open Lakehouse Mesh (Delta UniForm / Iceberg + Domain Federation)
    scores = {
        "option_1_bigquery_migration": {
            "m_and_a_agility": 5.0,           # Slower to ingest disparate Azure/on-prem sources across cloud boundary
            "org_operating_model": 4.5,       # High cognitive load; team retraining from PySpark/Python to SQL/GCP
            "regulatory_sovereignty_dora": 4.0, # Cross-cloud DPIA hurdles; proprietary Capacitor engine violates exit mandates
            "technical_debt_modernization": 7.0, # BQMS and Dataform automate T-SQL transpilation
            "storage_neutrality_open_formats": 4.0, # Proprietary Capacitor storage and BQ SQL dialect
            "ai_ml_maturity": 7.5,            # Strong Gemini in-situ SQL, but Vertex AI is fragmented across separate portals
            "capital_efficiency_5yr_tco": 4.5, # Devastated by $1.5M-$3M upfront TCOM and 4-6 year payback period
        },
        "option_2_databricks_status_quo_tuning": {
            "m_and_a_agility": 7.5,           # Spark connects to everything; native Azure integration
            "org_operating_model": 8.0,       # Zero team disruption; happy data engineers & data scientists
            "regulatory_sovereignty_dora": 8.0, # Single-cloud compliance, but high stickiness to Databricks runtime
            "technical_debt_modernization": 5.5, # Leaves legacy stored procedures as unmodernized technical debt
            "storage_neutrality_open_formats": 8.0, # Delta Lake format + Apache Unity Catalog
            "ai_ml_maturity": 9.0,            # Industry-standard MLflow, Mosaic AI, collaborative notebooks
            "capital_efficiency_5yr_tco": 8.5, # Immediate 40-50% cost cut with $0 upfront migration spend
        },
        "option_3_open_lakehouse_data_mesh": {
            "m_and_a_agility": 9.5,           # Domain teams ingest acquired EHRs/systems via standardized Lakehouse ports
            "org_operating_model": 9.0,       # Decentralized Data Product ownership; low cognitive load across domains
            "regulatory_sovereignty_dora": 9.5, # Full multi-cloud exit capability via Apache Iceberg / Delta UniForm
            "technical_debt_modernization": 9.0, # Decomposes stored procedures into modular dbt / Dataform domain models
            "storage_neutrality_open_formats": 10.0, # UniForm allows simultaneous read by BigQuery, Databricks, Snowflake
            "ai_ml_maturity": 9.0,            # Unified MLflow + specialized GenAI endpoints across clouds
            "capital_efficiency_5yr_tco": 8.8, # Eliminates migration sinkholes while unlocking 40%+ OpEx optimization
        }
    }

    weighted_totals = {}
    for opt_key, opt_scores in scores.items():
        w_sum = sum(opt_scores[k] * weights[k] for k in weights)
        weighted_totals[opt_key] = round(w_sum, 2)

    winning_key = max(weighted_totals, key=weighted_totals.get)
    names = {
        "option_1_bigquery_migration": "Option 1: Big-Bang BigQuery Migration (GCP Monolith)",
        "option_2_databricks_status_quo_tuning": "Option 2: Databricks In-Place Optimization (Azure Baseline)",
        "option_3_open_lakehouse_data_mesh": "Option 3: Strategic Open Lakehouse Mesh (Delta UniForm + Domain Federation)"
    }

    return MCDAScore(
        weights=weights,
        scores_by_option=scores,
        weighted_totals=weighted_totals,
        winning_option_key=winning_key,
        winning_option_name=names[winning_key]
    )
