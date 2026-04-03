"""
Model essay tool for JSONL dataset.
"""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any, Dict, List


class ModelEssayTool:
    """
    Provide `get_model_essay` from `data/essays/dataset.jsonl`.

    Current implementation uses random selection.
    """

    def __init__(self) -> None:
        self.dataset_path = (
            Path(__file__).resolve().parents[2] / "data" / "essays" / "dataset.jsonl"
        )

    def get_model_essay(self) -> Dict[str, Any]:
        """
        Get one model essay record.

        Returns:
            {
                "custom_id": str,
                "title": str,
                "prompt": str,
                "essay_content": str,
            }

        Note:
            This method currently selects one record randomly.
        """
        records = self._load_all_records()
        selected = random.choice(records)
        return self._normalize_record(selected)

    def _load_all_records(self) -> List[Dict[str, Any]]:
        if not self.dataset_path.exists():
            raise FileNotFoundError(f"Dataset file not found: {self.dataset_path}")

        records: List[Dict[str, Any]] = []
        with self.dataset_path.open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    records.append(json.loads(stripped))
                except json.JSONDecodeError as error:
                    raise ValueError(
                        f"Invalid JSONL at line {line_number} in {self.dataset_path}"
                    ) from error

        if not records:
            raise ValueError(f"No valid records found in dataset: {self.dataset_path}")

        return records

    def _normalize_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        messages = record.get("messages", [])
        if not isinstance(messages, list):
            messages = []

        prompt = self._extract_first_message_content(messages, role="user")
        essay_content = self._extract_first_message_content(messages, role="assistant")

        if not essay_content:
            raise ValueError(
                f"Record {record.get('custom_id', '<unknown>')} does not contain assistant content"
            )

        return {
            "custom_id": record.get("custom_id", ""),
            "title": record.get("title", ""),
            "prompt": prompt,
            "essay_content": essay_content,
        }

    @staticmethod
    def _extract_first_message_content(messages: List[Dict[str, Any]], role: str) -> str:
        for message in messages:
            if message.get("role") == role:
                content = message.get("content", "")
                if isinstance(content, str):
                    return content
        return ""
