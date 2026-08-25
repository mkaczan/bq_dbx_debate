"""Forensic calculation tools for the BigQuery Migration Strategist."""
from typing import Dict, Any
from app.config import (
    DEFAULT_DBU_PRICE_USD,
    DEFAULT_VM_INFRA_MARKUP,
    AVERAGE_ALL_PURPOSE_IDLE_PCT,
    DELTA_MAINTENANCE_TAX_RATIO,
    ESTIMATED_BIGQUERY_SAVINGS_PCT,
)


def analyze_databricks_telemetry(annual_dbu_spend: float, storage_tb: float, pyspark_jobs: int) -> Dict[str, Any]:
    """Analyzes Databricks infrastructure telemetry to uncover idle cluster waste and Delta maintenance taxes."""
    vm_infra_spend = annual_dbu_spend * (DEFAULT_VM_INFRA_MARKUP - 1.0)
    total_dbx_spend = annual_dbu_spend + vm_infra_spend

    idle_cluster_waste = annual_dbu_spend * 0.40 * AVERAGE_ALL_PURPOSE_IDLE_PCT * DEFAULT_VM_INFRA_MARKUP
    delta_maintenance_tax = annual_dbu_spend * DELTA_MAINTENANCE_TAX_RATIO * DEFAULT_VM_INFRA_MARKUP
    oom_driver_recovery_waste = pyspark_jobs * 12 * 85.0  # Estimated restart & debugging cost per job/month

    total_unnecessary_waste = idle_cluster_waste + delta_maintenance_tax + oom_driver_recovery_waste

    return {
        "annual_dbu_spend_usd": round(annual_dbu_spend, 2),
        "hyperscaler_vm_spend_usd": round(vm_infra_spend, 2),
        "total_current_databricks_spend_usd": round(total_dbx_spend, 2),
        "unnecessary_waste_breakdown": {
            "idle_interactive_cluster_waste_usd": round(idle_cluster_waste, 2),
            "delta_maintenance_tax_usd": round(delta_maintenance_tax, 2),
            "oom_driver_recovery_waste_usd": round(oom_driver_recovery_waste, 2),
            "total_annual_waste_usd": round(total_unnecessary_waste, 2),
        },
        "waste_percentage_of_total_bill": round((total_unnecessary_waste / total_dbx_spend) * 100, 1),
        "bigquery_fluid_scaling_impact": {
            "idle_capacity_billing": "$0 (True Per-Second Billing with Zero Cooldown)",
            "background_clustering_cost": "$0 (Autonomous, Zero Compute Billing in BigQuery)",
            "driver_oom_management": "Serverless Managed Executors (No JVM Tuning Required)"
        }
    }


def evaluate_powerbi_performance(concurrent_users: int, warehouse_size: str = "Medium") -> Dict[str, Any]:
    """Models Power BI concurrency bottlenecks on Databricks SQL vs BigQuery BI Engine + Fluid Scaling."""
    wh_slots = {"Small": 8, "Medium": 16, "Large": 32, "X-Large": 64}.get(warehouse_size, 16)
    simultaneous_dax = int(concurrent_users * 0.60)
    queue_ratio = max(1.0, simultaneous_dax / max(wh_slots, 1))

    dbx_load_time_sec = round(3.8 * queue_ratio, 2)
    bq_load_time_sec = 0.45  # Sub-second in-memory BI Engine acceleration
    speedup_factor = round(dbx_load_time_sec / bq_load_time_sec, 1)

    return {
        "concurrent_powerbi_users": concurrent_users,
        "databricks_sql_warehouse_size": warehouse_size,
        "databricks_warehouse_concurrency_limit": wh_slots,
        "estimated_simultaneous_dax_queries": simultaneous_dax,
        "databricks_queue_risk": "HIGH" if queue_ratio > 1.5 else "MEDIUM" if queue_ratio > 1.0 else "LOW",
        "databricks_avg_dashboard_load_time_sec": dbx_load_time_sec,
        "bigquery_bi_engine_load_time_sec": bq_load_time_sec,
        "performance_speedup_factor": f"{speedup_factor}x faster",
        "connector_impact": "DirectQuery native BigQuery connector supports Azure AD / Entra ID SSO with 0 DAX rewrite."
    }


def calculate_migration_tco(annual_dbu_spend: float) -> Dict[str, Any]:
    """Models 3-year TCO comparison between Databricks dual-billing and BigQuery Editions with Fluid Scaling."""
    vm_spend = annual_dbu_spend * (DEFAULT_VM_INFRA_MARKUP - 1.0)
    total_dbx_annual = annual_dbu_spend + vm_spend

    # BigQuery Editions + Spend CUDs + Fluid Scaling delivers ~45-55% net savings
    bq_annual_editions_cost = total_dbx_annual * (1.0 - ESTIMATED_BIGQUERY_SAVINGS_PCT)
    net_annual_savings = total_dbx_annual - bq_annual_editions_cost
    three_year_savings = net_annual_savings * 3.0

    return {
        "current_databricks_annual_spend": round(total_dbx_annual, 2),
        "bigquery_modeled_annual_spend": round(bq_annual_editions_cost, 2),
        "net_annual_savings_usd": round(net_annual_savings, 2),
        "net_3yr_savings_usd": round(three_year_savings, 2),
        "tco_reduction_percentage": f"{int(ESTIMATED_BIGQUERY_SAVINGS_PCT * 100)}%",
        "cost_drivers_eliminated": [
            "Dual-Bill Markup: Eliminated (Single unified Google Cloud invoice)",
            "60-Second Cooldown Tax: Eliminated via Fluid Scaling area-under-the-curve billing",
            "Delta Maintenance Jobs: Free background clustering in Capacitor engine",
            "Commitment Discounts: 3-Year Spend CUDs yield up to 40% discount across all editions"
        ]
    }


def generate_zero_copy_roadmap(storage_tb: float, pyspark_jobs: int) -> Dict[str, Any]:
    """Generates the Day-1 BigLake zero-copy roadmap and automated pipeline modernization timeline."""
    automated_transpile_pct = 78
    manual_refactor_jobs = int(pyspark_jobs * (1.0 - (automated_transpile_pct / 100.0)))
    estimated_migration_weeks = max(4, int(pyspark_jobs / 15))

    return {
        "storage_tb": storage_tb,
        "total_pyspark_jobs": pyspark_jobs,
        "automated_bqms_transpile_percentage": f"{automated_transpile_pct}%",
        "manual_review_jobs_count": manual_refactor_jobs,
        "estimated_total_timeline_weeks": estimated_migration_weeks,
        "phased_approach": [
            {
                "phase": "Phase 1: Day-1 Zero-Copy Federation",
                "duration": "1-2 Weeks",
                "action": "Register external Delta Lake / Iceberg tables via BigLake in-place without moving a single byte.",
                "value": "Instant BigQuery SQL and BI Engine querying over existing ADLS/S3 storage."
            },
            {
                "phase": "Phase 2: Power BI & SQL Warehouse Repointing",
                "duration": "2-3 Weeks",
                "action": "Point Power BI DirectQuery to BigQuery BI Engine. Decommission high-cost 24/7 Databricks SQL Warehouses.",
                "value": "Immediate 35% cost reduction and <1s dashboard response times."
            },
            {
                "phase": "Phase 3: Automated ETL Modernization",
                "duration": f"{estimated_migration_weeks - 4} Weeks",
                "action": "Transpile PySpark batch jobs to Dataproc Serverless with Lightning Engine (Velox C++) & Dataform SQLX.",
                "value": "2x faster execution than Photon at 0 DBU software licensing fee."
            }
        ]
    }
