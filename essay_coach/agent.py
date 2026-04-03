"""
Essay Coach Agent definition using CrewAI
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from openai import OpenAI

from essay_coach.config import Config
from essay_coach.prompts.templates import OPENING_TRAINING_SYSTEM_PROMPT, TRAINING_PROMPTS
from essay_coach.tools import ModelEssayTool

VALID_TRAINING_TYPES = tuple(TRAINING_PROMPTS.keys())


class EssayCoachAgent:
	"""
	Single coach agent wrapper.

	Current capability:
	- Get one model essay from local dataset.
	- Run specialized training sessions (opening, closing, language, transitions, evidence, argumentation).
	"""

	def __init__(self, config: Optional[Config] = None) -> None:
		self.config = config or Config()
		self.model_essay_tool = ModelEssayTool()

	def get_model_essay(self) -> Dict[str, Any]:
		"""
		Fetch one model essay for agent context.

		Note:
			Current implementation uses random selection.
		"""
		return self.model_essay_tool.get_model_essay()

	def _training_chat(
		self,
		system_prompt: str,
		user_message: str,
		conversation_history: Optional[List[Dict[str, str]]] = None,
	) -> Dict[str, Any]:
		"""
		Core tool-calling loop shared by all training types.

		Args:
			system_prompt: The system prompt for the specific training type.
			user_message: Latest user input.
			conversation_history: Existing dialogue history (list of role/content dicts).

		Returns:
			{
				"assistant_reply": str,
				"conversation_history": List[Dict[str, str]]
			}
		"""
		self.config.validate()

		history: List[Dict[str, str]] = list(conversation_history or [])
		messages: List[Dict[str, Any]] = [
			{"role": "system", "content": system_prompt},
			*history,
			{"role": "user", "content": user_message},
		]

		client_kwargs: Dict[str, Any] = {"api_key": self.config.openai_api_key}
		if self.config.openai_base_url:
			client_kwargs["base_url"] = self.config.openai_base_url

		client = OpenAI(**client_kwargs)
		tools = [
			{
				"type": "function",
				"function": {
					"name": "get_model_essay",
					"description": "Get one model essay sample from local JSONL dataset.",
					"parameters": {
						"type": "object",
						"properties": {},
						"additionalProperties": False,
					},
				},
			}
		]

		assistant_reply = ""
		max_tool_rounds = 8
		tool_round = 0

		while True:
			response = client.chat.completions.create(
				model=self.config.openai_model,
				messages=messages,
				tools=tools,
				tool_choice="auto",
				temperature=0.7,
			)

			message = response.choices[0].message
			tool_calls = message.tool_calls or []

			if tool_calls:
				tool_round += 1
				if tool_round > max_tool_rounds:
					assistant_reply = '本轮专训已达到范文检索上限，请你回复"继续"，我将重新开始筛选并出题。'
					messages.append({"role": "assistant", "content": assistant_reply})
					break

				assistant_tool_calls: List[Dict[str, Any]] = []
				for tool_call in tool_calls:
					assistant_tool_calls.append(
						{
							"id": tool_call.id,
							"type": "function",
							"function": {
								"name": tool_call.function.name,
								"arguments": tool_call.function.arguments,
							},
						}
					)

				messages.append(
					{
						"role": "assistant",
						"content": message.content or "",
						"tool_calls": assistant_tool_calls,
					}
				)

				for tool_call in tool_calls:
					tool_name = tool_call.function.name

					if tool_name == "get_model_essay":
						tool_result = self.get_model_essay()
					else:
						tool_result = {"error": f"Unknown tool: {tool_name}"}

					messages.append(
						{
							"role": "tool",
							"tool_call_id": tool_call.id,
							"content": json.dumps(tool_result, ensure_ascii=False),
						}
					)

				continue

			assistant_reply = message.content or ""
			messages.append({"role": "assistant", "content": assistant_reply})
			break

		new_history = history + [
			{"role": "user", "content": user_message},
			{"role": "assistant", "content": assistant_reply},
		]

		return {
			"assistant_reply": assistant_reply,
			"conversation_history": new_history,
		}

	def training_chat(
		self,
		training_type: str,
		user_message: str,
		conversation_history: Optional[List[Dict[str, str]]] = None,
	) -> Dict[str, Any]:
		"""
		Unified entry point for all training types (Route B).

		Args:
			training_type: One of "opening", "closing", "language",
			               "transitions", "evidence", "argumentation".
			user_message: Latest user input.
			conversation_history: Existing dialogue history.

		Returns:
			{
				"assistant_reply": str,
				"conversation_history": List[Dict[str, str]]
			}
		"""
		if training_type not in TRAINING_PROMPTS:
			raise ValueError(
				f"Unknown training_type: '{training_type}'. "
				f"Valid options: {list(TRAINING_PROMPTS.keys())}"
			)
		system_prompt = TRAINING_PROMPTS[training_type]
		return self._training_chat(system_prompt, user_message, conversation_history)

	def opening_training_chat(
		self,
		user_message: str,
		conversation_history: Optional[List[Dict[str, str]]] = None,
	) -> Dict[str, Any]:
		"""Backward-compatible wrapper for opening training."""
		return self._training_chat(
			OPENING_TRAINING_SYSTEM_PROMPT, user_message, conversation_history
		)
