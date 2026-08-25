"""Forensic calculation tools for the Databricks Defense Advocate."""
from typing import Dict, Any
from app.config import (
    ENGINEER_HOURLY_RATE_USD,
    STORAGE_WRITE_API_GB_COST,
    BI_ENGINE_RAM_GB_MONTHLY_COST,
    DEFAULT_VM_INFRA_MARKUP,
)


def analyze_spark_compatibility(
    pyspark_jobs: int,
    lines_of_code: int,
    mlflow_models: int,
    streaming_pipelines: int
) -> Dict[str, Any]:
    """Analyzes codebase complexity and calculates the severe engineering friction of rewriting PySpark to BigQuery."""
    # Estimated incompatible pattern instances
    python_udf_count = int(pyspark_jobs * 0.35)
    rdd_ops_count = int(pyspark_jobs * 0.20)
    dlt_streaming_count = streaming_pipelines
    ml_graph_count = mlflow_models

    udf_hours = python_udf_count * 8.0
    rdd_hours = rdd_ops_count * 14.0
    streaming_hours = dlt_streaming_count * 24.0
    ml_hours = ml_graph_count * 20.0
    tuning_hours = (pyspark_jobs // 2) * 3.0

    total_rewrite_hours = udf_hours + rdd_hours + streaming_hours + ml_hours + tuning_hours
    total_refactoring_cost_usd = total_rewrite_hours * ENGINEER_HOURLY_RATE_USD

    return {
        "workload_profile": {
            "total_pyspark_jobs": pyspark_jobs,
            "lines_of_code": lines_of_code,
            "mlflow_registered_models": mlflow_models,
            "streaming_pipelines": streaming_pipelines,
        },
        "friction_breakdown": {
            "python_and_pandas_udfs": {
                "instances": python_udf_count,
                "severity": "CRITICAL",
                "rewrite_hours": udf_hours,
                "issue": "bigframes translates strictly to SQL AST. Python bytecode cannot run inside the BigQuery engine."
            },
            "low_level_spark_rdd_apis": {
                "instances": rdd_ops_count,
                "severity": "CRITICAL",
                "rewrite_hours": rdd_hours,
                "issue": "BigQuery has no partition distribution control or distributed RDD pointers."
            },
            "streaming_and_dlt": {
                "instances": dlt_streaming_count,
                "severity": "HIGH",
                "rewrite_hours": streaming_hours,
                "issue": "DLT pipelines must be re-architected in Apache Beam (Dataflow), Pub/Sub, and Storage Write API."
            },
            "mlflow_and_distributed_ml": {
                "instances": ml_graph_count,
                "severity": "HIGH",
                "rewrite_hours": ml_hours,
                "issue": "MLflow model registry and PyTorch/Scikit pipelines require rebuilding in Vertex AI custom containers."
            },
        },
        "total_engineering_rewrite_hours": round(total_rewrite_hours, 1),
        "total_refactoring_consulting_cost_usd": round(total_refactoring_cost_usd, 2),
        "verdict": "CRITICAL RISK: bigframes is a transpiler, not Spark. Real-world refactoring will take 9-18 months."
    }


def calculate_migration_risk(
    annual_dbu_spend: float,
    pyspark_jobs: int,
    lines_of_code: int,
    storage_tb: float
) -> Dict[str, Any]:
    """Calculates Total Cost of Migration (TCOM), dual-licensing overlap, and business disruption risk."""
    spark_compat = analyze_spark_compatibility(pyspark_jobs, lines_of_code, 25, 10)
    refactoring_cost = spark_compat["total_refactoring_consulting_cost_usd"]

    # Typical enterprise migration takes 12-18 months
    migration_months = 12
    dual_run_overlap_tax = (annual_dbu_spend * DEFAULT_VM_INFRA_MARKUP / 12.0) * migration_months * 0.40
    data_egress_and_validation_cost = storage_tb * 1024 * 0.02 * 1.5  # Egress + multi-run validation
    talent_retraining_cost = 120000.0  # Training 20 data engineers & data scientists on GCP

    total_tcom = refactoring_cost + dual_run_overlap_tax + data_egress_and_validation_cost + talent_retraining_cost

    return {
        "migration_duration_months": migration_months,
        "total_cost_of_migration_tcom_usd": round(total_tcom, 2),
        "tcom_component_breakdown": {
            "pyspark_codebase_refactoring_usd": round(refactoring_cost, 2),
            "dual_platform_parallel_run_tax_usd": round(dual_run_overlap_tax, 2),
            "data_egress_and_validation_usd": round(data_egress_and_validation_cost, 2),
            "team_retraining_and_productivity_dip_usd": round(talent_retraining_cost, 2),
        },
        "roi_payback_period_years": round(total_tcom / (annual_dbu_spend * 0.35), 2),
        "operational_risks": [
            "12-18 month engineering freeze on business features while pipelines are refactored",
            "Data scientist churn due to loss of native MLflow and collaborative Databricks notebooks",
            "Silent regression bugs during stored procedure and SQL translation"
        ]
    }


def calculate_hidden_bq_costs(
    storage_tb: float,
    streaming_daily_gb: float = 2500.0,
    bi_engine_ram_gb: int = 128,
    peak_concurrent_slots: int = 600
) -> Dict[str, Any]:
    """Exposes hidden BigQuery architectural charges, ingestion fees, and slot starvation risks."""
    annual_storage_write_api_cost = (streaming_daily_gb * 365.0) * STORAGE_WRITE_API_GB_COST
    annual_bi_engine_ram_cost = bi_engine_ram_gb * BI_ENGINE_RAM_GB_MONTHLY_COST * 12.0
    biglake_cross_cloud_egress_cost = (storage_tb * 0.20 * 1024) * 0.08 * 12.0  # Monthly scan egress from AWS/Azure
    slot_overage_buffer_usd = peak_concurrent_slots * 0.06 * 8 * 250  # On-demand slot burst charges

    total_hidden_fees = (
        annual_storage_write_api_cost
        + annual_bi_engine_ram_cost
        + biglake_cross_cloud_egress_cost
        + slot_overage_buffer_usd
    )

    return {
        "annual_hidden_costs_usd": round(total_hidden_fees, 2),
        "breakdown": {
            "storage_write_api_ingestion_usd": round(annual_storage_write_api_cost, 2),
            "bi_engine_ram_reservations_usd": round(annual_bi_engine_ram_cost, 2),
            "biglake_cross_cloud_egress_usd": round(biglake_cross_cloud_egress_cost, 2),
            "slot_contention_and_burst_overage_usd": round(slot_overage_buffer_usd, 2),
        },
        "architectural_loopholes": [
            "BigLake external table queries on ADLS/S3 suffer 3x-8x latency penalty and lack native Photon SIMD speed",
            "Multi-cloud scanning incurs heavy network egress fees back to Google Cloud",
            "Fixed slot allocations lead to morning BI queue stalls or budget-busting auto-scale bursts"
        ]
    }


def audit_databricks_optimization(annual_dbu_spend: float) -> Dict[str, Any]:
    """Calculates immediate in-place savings on Databricks with zero migration risk."""
    serverless_sql_savings = annual_dbu_spend * 0.25 * 0.35  # Instant scale-to-zero on BI compute
    photon_engine_savings = annual_dbu_spend * 0.30 * 0.28   # 2-3x execution speedup reduces cluster runtime
    liquid_clustering_savings = annual_dbu_spend * 0.18 * 0.60 # Eliminates manual OPTIMIZE/VACUUM cron overhead
    spot_instance_savings = (annual_dbu_spend * 0.35) * 0.50  # 70-90% discount on Azure/AWS VM compute

    total_inplace_savings = (
        serverless_sql_savings
        + photon_engine_savings
        + liquid_clustering_savings
        + spot_instance_savings
    )
    optimized_annual_spend = (annual_dbu_spend * DEFAULT_VM_INFRA_MARKUP) - total_inplace_savings

    return {
        "current_total_annual_spend_usd": round(annual_dbu_spend * DEFAULT_VM_INFRA_MARKUP, 2),
        "achievable_inplace_annual_savings_usd": round(total_inplace_savings, 2),
        "optimized_annual_spend_usd": round(optimized_annual_spend, 2),
        "immediate_cost_reduction_pct": f"{int((total_inplace_savings / (annual_dbu_spend * DEFAULT_VM_INFRA_MARKUP)) * 100)}%",
        "implementation_timeline_days": 14,
        "upfront_migration_cost_usd": 0,
        "business_disruption_risk": "ZERO (Executed entirely within current Databricks workspace)"
    }
