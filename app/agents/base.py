"""Base agent class with LLM invocation and fallback reasoning."""
import os
import json
import logging
from typing import Dict, Any, List, Optional
from app.config import DEFAULT_MODEL, GEMINI_API_KEY

logger = logging.getLogger(__name__)


class BaseAgent:
    """Base AI Agent implementing prompt dispatch, tool invocation, and LLM communication."""

    def __init__(self, name: str, role: str, avatar: str, stance: str, system_prompt: str):
        self.name = name
        self.role = role
        self.avatar = avatar
        self.stance = stance
        self.system_prompt = system_prompt
        self.model_name = DEFAULT_MODEL
        self.api_key = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
        self._genai_client = None

        if self.api_key:
            try:
                from google import genai
                self._genai_client = genai.Client(api_key=self.api_key)
                logger.info(f"Initialized Google GenAI client for agent: {self.name}")
            except Exception as e:
                logger.warning(f"Could not initialize Google GenAI SDK: {e}. Will use intelligent reasoning engine.")

    def generate_response(
        self,
        prompt: str,
        context_data: Dict[str, Any],
        conversation_history: List[Dict[str, Any]],
        tool_results: Optional[Dict[str, Any]] = None
    ) -> str:
        """Invokes Gemini LLM if available, otherwise falls back to intelligent domain synthesis."""
        if self._genai_client:
            try:
                # Format conversation history
                history_text = "\n".join([
                    f"[{msg.get('speaker_display_name', msg.get('speaker'))} ({msg.get('stance')})]:\n{msg.get('content')}\n"
                    for msg in conversation_history[-6:]
                ])

                tools_text = json.dumps(tool_results, indent=2) if tool_results else "No specific tool output."
                context_text = json.dumps(context_data, indent=2)

                full_prompt = f"""
{self.system_prompt}

=== ENTERPRISE WORKLOAD CONTEXT ===
{context_text}

=== LIVE DIAGNOSTIC TOOL DATA & FORENSICS ===
{tools_text}

=== RECENT DEBATE TURNS & TRANSCRIPT ===
{history_text}

=== CURRENT INSTRUCTION / OBJECTION TO ADDRESS ===
{prompt}

Deliver your response in crisp, highly structured Markdown. Use bullet points, bold highlights, concrete financial numbers ($), performance speedup factors, and architectural precision. Emphasize your key stance.
"""
                response = self._genai_client.models.generate_content(
                    model=self.model_name,
                    contents=full_prompt
                )
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                logger.error(f"Gemini API call failed: {e}. Falling back to structured heuristic synthesis.")

        # Fallback to intelligent deterministic reasoning
        return self._generate_fallback(prompt, context_data, conversation_history, tool_results)

    def _generate_fallback(
        self,
        prompt: str,
        context_data: Dict[str, Any],
        conversation_history: List[Dict[str, Any]],
        tool_results: Optional[Dict[str, Any]] = None
    ) -> str:
        """Must be implemented by subclasses to provide rich offline responses."""
        raise NotImplementedError("Subclasses must implement _generate_fallback")
