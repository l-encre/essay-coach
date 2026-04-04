"""
Main entry point for the Essay Coach application
"""

from __future__ import annotations

from typing import Dict, List, Optional

from essay_coach.agent import EssayCoachAgent
from essay_coach.config import Config


class EssayCoach:
	"""
	Main application wrapper for essay coaching.
	"""

	def __init__(self, config: Optional[Config] = None) -> None:
		self.config = config or Config()
		self.agent = EssayCoachAgent(self.config)

	def chat(
		self,
		user_message: str,
		conversation_history: Optional[List[Dict[str, str]]] = None,
	) -> Dict[str, object]:
		"""
		Unified auto-training chat entry.

		LLM decides the most suitable training focus each round.
		"""
		return self.agent.chat(
			user_message=user_message,
			conversation_history=conversation_history,
		)
