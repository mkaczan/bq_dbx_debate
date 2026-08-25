"""FastAPI web server and REST API for the BQ vs Databricks Debate App."""
import os
import json
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse, FileResponse

from app.models.schemas import (
    EnterpriseContext,
    DebateSession,
    DebateTurn,
    StartDebateRequest,
    StepDebateRequest,
    InterveneDebateRequest,
    FinalVerdict
)
from app.engine.orchestrator import orchestrator
from app.engine.presets import PRESET_SCENARIOS
from app.tools.bq_tools import analyze_databricks_telemetry, evaluate_powerbi_performance, calculate_migration_tco, generate_zero_copy_roadmap
from app.tools.dbx_tools import analyze_spark_compatibility, calculate_migration_risk, calculate_hidden_bq_costs, audit_databricks_optimization
from app.tools.arch_tools import evaluate_mcda_matrix

app = FastAPI(
    title="BigQuery vs Databricks Strategic Debate Arena",
    description="Multi-Agent AI Debate System between BigQuery Strategist, Databricks Advocate, and Independent Principal Architect.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/presets")
def get_presets() -> Dict[str, Any]:
    """Returns all available preset enterprise scenarios."""
    return {k: v.model_dump() for k, v in PRESET_SCENARIOS.items()}


@app.post("/api/debate/start", response_model=DebateSession)
def start_debate(req: StartDebateRequest) -> DebateSession:
    """Initializes a new multi-agent debate session with custom or preset context."""
    session = orchestrator.create_session(context=req.context, rounds=req.rounds)
    return session


@app.post("/api/debate/step")
def step_debate(req: StepDebateRequest) -> Dict[str, Any]:
    """Executes the next turn in the active debate session."""
    session = orchestrator.get_session(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    turn = orchestrator.execute_next_turn(req.session_id)
    return {
        "turn": turn.model_dump() if turn else None,
        "session": session.model_dump(),
        "is_completed": session.status == "completed"
    }


@app.post("/api/debate/run-all", response_model=DebateSession)
def run_all_turns(req: StepDebateRequest) -> DebateSession:
    """Executes all turns and concludes the debate with the Principal Architect's final verdict."""
    session = orchestrator.get_session(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    completed_session = orchestrator.run_entire_debate(req.session_id)
    return completed_session


@app.post("/api/debate/intervene")
def user_intervention(req: InterveneDebateRequest) -> Dict[str, Any]:
    """Injects user question/constraint and triggers agent response."""
    session = orchestrator.get_session(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    user_turn = orchestrator.inject_user_intervention(req.session_id, req.user_prompt)
    # Automatically execute a follow-up response turn
    agent_turn = orchestrator.execute_next_turn(req.session_id)

    return {
        "user_turn": user_turn.model_dump() if user_turn else None,
        "agent_turn": agent_turn.model_dump() if agent_turn else None,
        "session": session.model_dump()
    }


@app.get("/api/debate/{session_id}", response_model=DebateSession)
def get_debate_session(session_id: str) -> DebateSession:
    """Retrieves session details and full debate transcript."""
    session = orchestrator.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@app.post("/api/tools/diagnostics")
def run_all_tools(context: EnterpriseContext) -> Dict[str, Any]:
    """Runs all forensic calculation tools across BQ, DBX, and Architecture frameworks."""
    bq_telemetry = analyze_databricks_telemetry(context.annual_dbu_spend, context.storage_tb, context.total_pyspark_jobs)
    bq_powerbi = evaluate_powerbi_performance(context.powerbi_users_count)
    bq_tco = calculate_migration_tco(context.annual_dbu_spend)
    bq_roadmap = generate_zero_copy_roadmap(context.storage_tb, context.total_pyspark_jobs)

    dbx_compat = analyze_spark_compatibility(context.total_pyspark_jobs, context.lines_of_code, context.mlflow_models_count, context.streaming_pipelines_count)
    dbx_risk = calculate_migration_risk(context.annual_dbu_spend, context.total_pyspark_jobs, context.lines_of_code, context.storage_tb)
    dbx_hidden = calculate_hidden_bq_costs(context.storage_tb)
    dbx_opt = audit_databricks_optimization(context.annual_dbu_spend)

    mcda = evaluate_mcda_matrix(context)

    return {
        "bigquery_forensics": {
            "telemetry": bq_telemetry,
            "powerbi": bq_powerbi,
            "tco": bq_tco,
            "roadmap": bq_roadmap
        },
        "databricks_forensics": {
            "compatibility": dbx_compat,
            "tcom_risk": dbx_risk,
            "hidden_costs": dbx_hidden,
            "inplace_optimization": dbx_opt
        },
        "mcda_matrix": mcda.model_dump()
    }


@app.get("/api/export/markdown/{session_id}", response_class=PlainTextResponse)
def export_markdown_report(session_id: str) -> str:
    """Exports the entire debate transcript, MCDA score, and final blueprint as Markdown."""
    session = orchestrator.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    lines = []
    lines.append(f"# 🏛️ Strategic Enterprise Data Platform Debate & Verdict")
    lines.append(f"**Target Enterprise:** {session.context.enterprise_name} | **Industry:** {session.context.industry}")
    lines.append(f"**Session ID:** `{session.session_id}` | **Date:** {session.created_at[:10]}\n")
    lines.append(f"---\n")

    lines.append("## 🏢 Enterprise Workload Context")
    lines.append(f"- **Annual DBU Spend:** ${session.context.annual_dbu_spend:,.2f}")
    lines.append(f"- **Total Storage:** {session.context.storage_tb} TB")
    lines.append(f"- **PySpark ETL Jobs:** {session.context.total_pyspark_jobs} ({session.context.lines_of_code:,} LOC)")
    lines.append(f"- **Power BI Concurrent Analysts:** {session.context.powerbi_users_count}")
    lines.append(f"- **Legacy Stored Procedures:** {session.context.legacy_stored_procs}")
    lines.append(f"- **Regulatory Posture:** {session.context.regulatory_framework}")
    lines.append(f"- **Cloud Strategy:** {session.context.cloud_strategy}\n")

    lines.append("## 🎙️ Multi-Agent Debate Transcript\n")
    for turn in session.turns:
        lines.append(f"### {turn.avatar} Round {turn.round_number} - {turn.speaker_display_name} (`{turn.stance}`)\n")
        lines.append(turn.content)
        lines.append("\n" + "-"*60 + "\n")

    if session.final_verdict:
        v = session.final_verdict
        lines.append("## 🏆 Final Principal Architect Verdict")
        lines.append(f"### Strategy: **{v.recommended_strategy_title}**\n")
        lines.append(f"> {v.executive_summary}\n")

        lines.append("### 💰 Financial & Capital Impact")
        fin = v.financial_impact_summary
        lines.append(f"- **Current Baseline Spend:** ${fin['current_annual_spend_usd']:,.0f}/yr")
        lines.append(f"- **Optimized Steady-State Spend:** ${fin['optimized_steady_state_spend_usd']:,.0f}/yr")
        lines.append(f"- **Net Annual OpEx Savings:** ${fin['net_annual_cost_savings_usd']:,.0f}/yr")
        lines.append(f"- **Avoided Migration TCOM Sunk Capital:** ${fin['upfront_migration_tcom_avoided_usd']:,.0f}")
        lines.append(f"- **5-Year Value Unlocked:** ${fin['5yr_cumulative_value_unlocked_usd']:,.0f}\n")

        lines.append("### 🗺️ Phased Implementation Blueprint")
        for p in v.phased_roadmap:
            lines.append(f"- **{p.phase} ({p.timeline})**: {p.action}")
            lines.append(f"  - *Deliverable:* {p.key_deliverable}")
            lines.append(f"  - *Risk Mitigation:* {p.risk_mitigation}")

    return "\n".join(lines)


@app.get("/api/export/json/{session_id}")
def export_json_report(session_id: str) -> Dict[str, Any]:
    """Exports full session state, turns, tool outputs, and verdict in JSON format."""
    session = orchestrator.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session.model_dump()


@app.get("/api/health")
def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "BigQuery vs Databricks Debate Arena",
        "version": "1.0.0"
    }


# Mount static directory for frontend UI
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

