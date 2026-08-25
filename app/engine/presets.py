"""Preset enterprise scenarios for discussion and debate."""
from typing import Dict
from app.models.schemas import EnterpriseContext

PRESET_SCENARIOS: Dict[str, EnterpriseContext] = {
    "healthcare_m_and_a": EnterpriseContext(
        enterprise_name="Pan-European Healthcare & Hospital Network",
        industry="Healthcare & Life Sciences",
        annual_dbu_spend=850000.0,
        storage_tb=500.0,
        total_pyspark_jobs=140,
        lines_of_code=125000,
        mlflow_models_count=45,
        streaming_pipelines_count=16,
        powerbi_users_count=90,
        legacy_stored_procs=1000,
        m_and_a_acquisitions_per_year=3,
        primary_cloud="Azure",
        cloud_strategy="Multi-Cloud Resilience & EU DORA Exit Mandate",
        regulatory_framework="EU GDPR, EHDS & DORA Regulatory Framework",
        current_pain_points=[
            "High Azure Databricks spend with 35% cluster idle time during off-hours",
            "Slow M&A integration when onboarding acquired hospital EHR systems",
            "Regulatory pressure under EU DORA to prove vendor-independent cloud exit capability",
            "1,000+ unversioned T-SQL stored procedures running on legacy SQL Server instances"
        ],
        strategic_priorities=[
            "Achieve >35% reduction in annual data compute OpEx",
            "Standardize on open storage formats (Apache Iceberg / Delta UniForm)",
            "Empower hospital domain teams with self-service Data Mesh ownership",
            "Accelerate executive Power BI clinical dashboards to <1s load times"
        ]
    ),
    "retail_omnichannel": EnterpriseContext(
        enterprise_name="Global Omnichannel Retail & E-Commerce Group",
        industry="Retail & Consumer Goods",
        annual_dbu_spend=650000.0,
        storage_tb=300.0,
        total_pyspark_jobs=95,
        lines_of_code=80000,
        mlflow_models_count=20,
        streaming_pipelines_count=8,
        powerbi_users_count=220,
        legacy_stored_procs=350,
        m_and_a_acquisitions_per_year=1,
        primary_cloud="AWS",
        cloud_strategy="Single-Cloud Efficiency with High Concurrency BI",
        regulatory_framework="PCI-DSS & SOC2",
        current_pain_points=[
            "220 Power BI analysts experiencing 15+ second dashboard load delays due to SQL Warehouse slot queues",
            "Heavy Delta OPTIMIZE/VACUUM maintenance jobs driving up DBU consumption by 22%",
            "Spiky Black Friday / promotional analytics causing severe autoscaling budget spikes"
        ],
        strategic_priorities=[
            "Deliver sub-second DirectQuery performance for all 220 Power BI users",
            "Eliminate manual partition/clustering maintenance overhead",
            "Adopt true per-second compute billing for highly spiky promotional queries"
        ]
    ),
    "fintech_streaming": EnterpriseContext(
        enterprise_name="NextGen FinTech & Payment Gateway",
        industry="Financial Services & FinTech",
        annual_dbu_spend=1200000.0,
        storage_tb=750.0,
        total_pyspark_jobs=180,
        lines_of_code=160000,
        mlflow_models_count=60,
        streaming_pipelines_count=28,
        powerbi_users_count=60,
        legacy_stored_procs=200,
        m_and_a_acquisitions_per_year=1,
        primary_cloud="Multi-Cloud (AWS + Azure)",
        cloud_strategy="Multi-Cloud Active-Active & Zero Single-Vendor Dependency",
        regulatory_framework="PCI-DSS, ECB Guidelines & EU DORA",
        current_pain_points=[
            "High cost of running 24/7 Delta Live Tables (DLT) streaming pipelines for fraud detection",
            "Complex cross-cloud data access leading to egress billing spikes",
            "Risk of vendor lock-in with proprietary analytics engines"
        ],
        strategic_priorities=[
            "Real-time sub-second fraud detection analytics",
            "Zero single-vendor lock-in at the storage layer via Apache Iceberg",
            "Strict compliance with DORA multi-cloud business continuity rules"
        ]
    ),
    "adtech_spiky": EnterpriseContext(
        enterprise_name="Acuity Media & AdTech Intelligence",
        industry="AdTech & Digital Media",
        annual_dbu_spend=450000.0,
        storage_tb=600.0,
        total_pyspark_jobs=70,
        lines_of_code=50000,
        mlflow_models_count=15,
        streaming_pipelines_count=10,
        powerbi_users_count=40,
        legacy_stored_procs=50,
        m_and_a_acquisitions_per_year=0,
        primary_cloud="GCP",
        cloud_strategy="GCP Native Consolidation",
        regulatory_framework="GDPR & CCPA",
        current_pain_points=[
            "Extremely spiky ad-hoc queries paying 60-second Databricks cluster scale-down cooldown penalties",
            "Desire to run Gemini multimodal models directly on clickstream and video ad assets",
            "Overly complex Spark sysadmin and cluster debugging overhead"
        ],
        strategic_priorities=[
            "True per-second serverless execution with BigQuery Fluid Scaling",
            "Native in-situ Multimodal AI with Gemini SQL (`ML.GENERATE_TEXT`)",
            "Zero cluster provisioning or JVM memory tuning"
        ]
    )
}
