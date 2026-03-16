from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AgentConfig:
    name: str = "JARVIS-Live"
    persona: str = (
        "High-agency multimodal assistant optimized for live voice, camera context, "
        "and spatial awareness."
    )


class JarvisAgent:
    def __init__(self, config: AgentConfig | None = None) -> None:
        self.config = config or AgentConfig()

    def system_prompt(self) -> str:
        now = datetime.utcnow().isoformat()
        return (
            f"You are {self.config.name}. Timestamp: {now}. "
            f"Persona: {self.config.persona} "
            "Respond concisely in voice-mode unless user asks for detail. "
            "Use spatial signals when available to tailor responses."
        )

    def build_text_response(self, transcript: str, spatial_summary: dict | None = None) -> str:
        if not transcript.strip():
            return "I didn't catch that—please repeat."

        if not spatial_summary or spatial_summary.get("status") != "ok":
            return f"Got it. You said: {transcript}. How should I help next?"

        attention = spatial_summary.get("attention", "center")
        return (
            f"Understood: {transcript}. "
            f"I also detect your attention state as {attention}. "
            "Do you want action mode, coding mode, or research mode?"
        )
