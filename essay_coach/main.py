"""
Main entry point for the Essay Coach application
"""

from __future__ import annotations

from typing import Dict, List, Optional

from essay_coach.agent import EssayCoachAgent, VALID_TRAINING_TYPES
from essay_coach.config import Config


class EssayCoach:
	"""
	Main application wrapper for essay coaching.
	"""

	def __init__(self, config: Optional[Config] = None) -> None:
		self.config = config or Config()
		self.agent = EssayCoachAgent(self.config)

	def train(
		self,
		training_type: str,
		user_message: str,
		conversation_history: Optional[List[Dict[str, str]]] = None,
	) -> Dict[str, object]:
		"""
		Unified entry point for all training types.

		Args:
			training_type: One of "opening", "closing", "language",
			               "transitions", "evidence", "argumentation".
			user_message: Latest user input.
			conversation_history: Existing dialogue history (pass the value
			                      returned from the previous call to continue
			                      a session).

		Returns:
			{
				"assistant_reply": str,
				"conversation_history": list
			}
		"""
		return self.agent.training_chat(
			training_type=training_type,
			user_message=user_message,
			conversation_history=conversation_history,
		)

	def opening_training(
		self,
		user_message: str,
		conversation_history: Optional[List[Dict[str, str]]] = None,
	) -> Dict[str, object]:
		"""Backward-compatible wrapper — prefer train(type='opening', ...)."""
		return self.train("opening", user_message, conversation_history)
