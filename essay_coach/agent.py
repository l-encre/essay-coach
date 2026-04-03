"""
Essay Coach Agent definition using CrewAI
"""

from __future__ import annotations

from typing import Any, Dict

from essay_coach.tools import ModelEssayTool


class EssayCoachAgent:
	"""
	Single coach agent wrapper.

	Current capability:
	- Get one model essay from local dataset.
	"""

	def __init__(self) -> None:
		self.model_essay_tool = ModelEssayTool()

	def get_model_essay(self) -> Dict[str, Any]:
		"""
		Fetch one model essay for agent context.

		Note:
			Current implementation uses random selection.
		"""
		return self.model_essay_tool.get_model_essay()
