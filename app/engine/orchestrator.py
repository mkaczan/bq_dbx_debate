"""Multi-Agent Debate Orchestrator Engine."""
import logging
from typing import Dict, Any, List, Optional
import uuid
import datetime

from app.models.schemas import (
    EnterpriseContext,
    DebateSession,
    DebateTurn,
    FinalVerdict,
    StartDebateRequest,
)
from app.agents.bq_strategist import BigQueryStrategistAgent
from app.agents.dbx_advocate import DatabricksAdvocateAgent
from app.agents.principal_architect import PrincipalArchitectAgent

logger = logging.getLogger(__name__)


class DebateOrchestrator:
    """Manages multi-agent debate sessions, step-by-step turn execution, and final synthesis."""

    def __init__(self):
        self.bq_agent = BigQueryStrategistAgent()
        self.dbx_agent = DatabricksAdvocateAgent()
        self.arch_agent = PrincipalArchitectAgent()
        self.sessions: Dict[str, DebateSession] = {}

    def create_session(self, context: EnterpriseContext, rounds: int = 2) -> DebateSession:
        """Initializes a new debate session."""
        session_id = str(uuid.uuid4())
        session = DebateSession(
            session_id=session_id,
            context=context,
            total_rounds=max(1, min(rounds, 4)),
            current_round=1,
            status="in_progress",
            turns=[]
        )
        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[DebateSession]:
        return self.sessions.get(session_id)

    def execute_next_turn(self, session_id: str) -> Optional[DebateTurn]:
        """Executes the next logical turn in the multi-agent debate sequence."""
        session = self.sessions.get(session_id)
        if not session:
            return None

        if session.status == "completed":
            return None

        turn_count = len(session.turns)
        context_dict = session.context.model_dump()
        history = [t.model_dump() for t in session.turns]

        # Determine which agent speaks
        # Filter agent turns (excluding user turns) to maintain debate progression
        agent_turns = [t for t in session.turns if t.speaker != "user"]
        agent_turn_count = len(agent_turns)
        max_speaker_turns = session.total_rounds * 2

        # Check if previous turn was a user intervention
        has_recent_user_prompt = len(session.turns) > 0 and session.turns[-1].speaker == "user"
        user_intervention_text = session.turns[-1].content if has_recent_user_prompt else ""

        if agent_turn_count < max_speaker_turns:
            # Alternate between BQ and DBX
            if agent_turn_count % 2 == 0:
                current_round = (agent_turn_count // 2) + 1
                session.current_round = current_round
                # BigQuery speaks
                tool_data = self.bq_agent.run_diagnostics(context_dict)
                if has_recent_user_prompt:
                    prompt = (
                        f"The Enterprise Executive directly intervened in the debate with the following question/challenge:\n"
                        f"{user_intervention_text}\n\n"
                        f"Address the executive's inquiry directly. Provide concrete technical architecture, Google BigQuery "
                        f"capabilities (Fluid Scaling, BI Engine, Dataproc Lightning Engine, BigLake), and financial metrics."
                    )
                elif current_round == 1:
                    prompt = (
                        f"Present the strategic and economic rationale for {session.context.enterprise_name} "
                        f"to migrate from Databricks to BigQuery."
                    )
                else:
                    prompt = (
                        f"Respond directly to the Databricks defense. Counter their arguments on PySpark rewrites, "
                        f"egress costs, and AI fragmentation with BigQuery Fluid Scaling and Dataproc Lightning Engine."
                    )
                content = self.bq_agent.generate_response(prompt, context_dict, history, tool_data)
                key_args = [
                    f"Fluid Scaling ($0 cooldown, {tool_data['tco_model']['tco_reduction_percentage']} savings)",
                    f"BI Engine acceleration down to {tool_data['powerbi_concurrency']['bigquery_bi_engine_load_time_sec']}s",
                    f"Dataproc Lightning Engine (Velox C++ SIMD) outperforming Photon"
                ]

                turn = DebateTurn(
                    round_number=current_round,
                    speaker=self.bq_agent.name,
                    speaker_display_name=self.bq_agent.role,
                    speaker_role=self.bq_agent.role,
                    avatar=self.bq_agent.avatar,
                    stance=self.bq_agent.stance,
                    content=content,
                    key_arguments=key_args,
                    tool_data=tool_data,
                    citations=["Google Cloud BigQuery Architecture Guide", "Velox / Gluten Benchmark Whitepaper", "BI Engine Docs"]
                )
            else:
                current_round = (agent_turn_count // 2) + 1
                session.current_round = current_round
                # Databricks speaks
                tool_data = self.dbx_agent.run_diagnostics(context_dict)
                if has_recent_user_prompt:
                    prompt = (
                        f"The Enterprise Executive directly intervened in the debate with the following question/challenge:\n"
                        f"{user_intervention_text}\n\n"
                        f"Address the executive's inquiry directly from the Databricks defense perspective. Expose architectural "
                        f"pitfalls in BigQuery, emphasize in-place optimization, Apache 2.0 Unity Catalog, and low TCOM."
                    )
                elif current_round == 1:
                    prompt = (
                        f"Interrogate the BigQuery pitch for {session.context.enterprise_name}. Expose the architectural "
                        f"loopholes in BigLake, calculate the massive TCOM refactoring costs, and present the in-place Databricks optimization playbook."
                    )
                else:
                    prompt = (
                        f"Rebut the BigQuery response. Re-emphasize Unity Catalog open source Apache 2.0 governance, "
                        f"MLflow single-pane-of-glass data science, and the fatal traps of BigQuery slot starvation."
                    )
                content = self.dbx_agent.generate_response(prompt, context_dict, history, tool_data)
                key_args = [
                    f"TCOM Migration Sunk Cost: ${tool_data['migration_risk_tcom']['total_cost_of_migration_tcom_usd']:,}",
                    f"In-Place Optimization: Save ${tool_data['inplace_optimization']['achievable_inplace_annual_savings_usd']:,}/yr in 14 days",
                    "Unity Catalog (Apache 2.0) + UniForm Multi-Cloud Sovereignty (DORA)"
                ]

                turn = DebateTurn(
                    round_number=current_round,
                    speaker=self.dbx_agent.name,
                    speaker_display_name=self.dbx_agent.role,
                    speaker_role=self.dbx_agent.role,
                    avatar=self.dbx_agent.avatar,
                    stance=self.dbx_agent.stance,
                    content=content,
                    key_arguments=key_args,
                    tool_data=tool_data,
                    citations=["Apache 2.0 Unity Catalog Spec", "Databricks Photon Whitepaper", "EU DORA Exit Mandate"]
                )

            session.turns.append(turn)
            return turn

        elif session.final_verdict is None:
            # Principal Architect delivers final verdict
            final_round = session.total_rounds + 1
            session.current_round = final_round

            verdict = self.arch_agent.evaluate_debate(session.context, history)
            prompt = (
                f"Deliver the authoritative final synthesis, MCDA scorecard analysis, financial trade-offs, "
                f"and 4-phase implementation roadmap for {session.context.enterprise_name}."
            )
            content = self.arch_agent.generate_response(prompt, context_dict, history, {"mcda": verdict.mcda_matrix.model_dump()})

            session.final_verdict = verdict
            session.status = "completed"

            turn = DebateTurn(
                round_number=final_round,
                speaker=self.arch_agent.name,
                speaker_display_name=self.arch_agent.role,
                speaker_role=self.arch_agent.role,
                avatar=self.arch_agent.avatar,
                stance=self.arch_agent.stance,
                content=content,
                key_arguments=[
                    f"Recommended Strategy: {verdict.recommended_strategy_title}",
                    f"Net Annual Savings: ${verdict.financial_impact_summary['net_annual_cost_savings_usd']:,}/yr",
                    f"Avoided Migration Sunk Capital: ${verdict.financial_impact_summary['upfront_migration_tcom_avoided_usd']:,}"
                ],
                tool_data={"verdict": verdict.model_dump()},
                citations=["Enterprise Architecture 6D Framework", "MCDA 7-Pillar Matrix", "Conway's Law & Team Topologies"]
            )
            session.turns.append(turn)
            return turn

        return None

    def inject_user_intervention(self, session_id: str, user_prompt: str) -> Optional[DebateTurn]:
        """Injects a user prompt/question into the live debate stream."""
        session = self.sessions.get(session_id)
        if not session:
            return None

        turn = DebateTurn(
            round_number=session.current_round,
            speaker="user",
            speaker_display_name="Enterprise Executive / User",
            speaker_role="Enterprise Decision Maker",
            avatar="👤",
            stance="Inquiry / Direct Challenge",
            content=f"**User Intervened in the Debate:**\n\n> *\"{user_prompt}\"*",
            key_arguments=["User injected specific operational constraint / question into the debate."],
            citations=[]
        )
        session.turns.append(turn)
        return turn

    def run_entire_debate(self, session_id: str) -> DebateSession:
        """Executes all turns until the debate is completed."""
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        while session.status != "completed":
            self.execute_next_turn(session_id)

        return session


# Global orchestrator singleton instance
orchestrator = DebateOrchestrator()
