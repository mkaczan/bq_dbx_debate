"""Pydantic data models and schemas for the Debate application."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import uuid
import datetime


class EnterpriseContext(BaseModel):
    """Enterprise customer workload profile and strategic context."""
    enterprise_name: str = Field(default="Global Enterprise Corp", description="Name of the enterprise")
    industry: str = Field(default="Healthcare & Life Sciences", description="Industry vertical")
    annual_dbu_spend: float = Field(default=750000.0, description="Annual Databricks DBU spend in USD")
    storage_tb: float = Field(default=350.0, description="Total Lakehouse data volume in Terabytes")
    total_pyspark_jobs: int = Field(default=120, description="Count of distinct PySpark/batch ETL jobs")
    lines_of_code: int = Field(default=95000, description="Estimated lines of custom PySpark/SQL code")
    mlflow_models_count: int = Field(default=35, description="Number of production MLflow registered models")
    streaming_pipelines_count: int = Field(default=12, description="Count of streaming / DLT pipelines")
    powerbi_users_count: int = Field(default=75, description="Concurrent Power BI / Tableau analysts")
    legacy_stored_procs: int = Field(default=600, description="Count of legacy T-SQL/PL-SQL stored procedures")
    m_and_a_acquisitions_per_year: int = Field(default=2, description="Rate of subsidiary/M&A system ingestions per year")
    primary_cloud: str = Field(default="Azure", description="Current primary cloud (Azure, AWS, GCP, Multi-Cloud)")
    cloud_strategy: str = Field(default="Multi-Cloud Resilience & Exit Readiness", description="Corporate cloud strategy")
    regulatory_framework: str = Field(default="GDPR & EU DORA Compliance", description="Compliance requirements")
    current_pain_points: List[str] = Field(
        default_factory=lambda: [
            "High Databricks bill driven by idle cluster uptime and Delta OPTIMIZE maintenance",
            "Slow Power BI dashboard loads during peak morning hours due to SQL Warehouse queuing",
            "Upcoming DORA audit requiring proven cloud exit capability and multi-cloud resilience",
            "Heavy technical debt with 600 legacy stored procedures across acquired hospital systems"
        ]
    )
    strategic_priorities: List[str] = Field(
        default_factory=lambda: [
            "Reduce 3-year data platform OpEx by >30%",
            "Accelerate executive BI dashboard responsiveness to <1s",
            "Avoid proprietary storage lock-in via Open Table Formats (Iceberg / UniForm)",
            "Enable decentralized domain Data Mesh without increasing sysadmin overhead"
        ]
    )


class DebateTurn(BaseModel):
    """A single turn/speech by an agent or user in the debate."""
    turn_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    round_number: int
    speaker: str  # 'bigquery_strategist', 'databricks_advocate', 'principal_architect', 'user'
    speaker_display_name: str
    speaker_role: str
    avatar: str
    stance: str
    content: str
    key_arguments: List[str] = Field(default_factory=list)
    tool_data: Optional[Dict[str, Any]] = None
    citations: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())


class MCDAScore(BaseModel):
    """Multi-Criteria Decision Analysis scorecard evaluated by the Principal Architect."""
    weights: Dict[str, float]
    scores_by_option: Dict[str, Dict[str, float]]
    weighted_totals: Dict[str, float]
    winning_option_key: str
    winning_option_name: str


class PhasedRoadmapStep(BaseModel):
    """A phase in the recommended implementation blueprint."""
    phase: str
    timeline: str
    action: str
    key_deliverable: str
    risk_mitigation: str


class FinalVerdict(BaseModel):
    """Authoritative verdict and strategic synthesis by the Independent Principal Architect."""
    recommended_strategy_title: str
    recommended_option_key: str
    executive_summary: str
    mcda_matrix: MCDAScore
    key_tradeoffs: List[str]
    financial_impact_summary: Dict[str, Any]
    phased_roadmap: List[PhasedRoadmapStep]
    architectural_principles: List[str]


class DebateSession(BaseModel):
    """Complete debate session containing context, turn history, and verdict."""
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    context: EnterpriseContext
    total_rounds: int = 2
    current_round: int = 0
    status: str = "initialized"  # 'initialized', 'in_progress', 'completed', 'error'
    turns: List[DebateTurn] = Field(default_factory=list)
    final_verdict: Optional[FinalVerdict] = None


class StartDebateRequest(BaseModel):
    context: EnterpriseContext
    rounds: int = 2


class StepDebateRequest(BaseModel):
    session_id: str


class InterveneDebateRequest(BaseModel):
    session_id: str
    user_prompt: str
