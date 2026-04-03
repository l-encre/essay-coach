"""
Configuration management for Essay Coach
"""

import os
from dotenv import load_dotenv


class Config:
    """
    Configuration class for Essay Coach
    """

    def __init__(self):
        """Initialize configuration from environment variables"""
        load_dotenv()

        # OpenAI-Compatible Configuration
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4")
        self.openai_base_url = os.getenv("OPENAI_BASE_URL", "").strip() or None

        # CrewAI Configuration
        self.crewai_debug = os.getenv("CREWAI_DEBUG", "False").lower() == "true"

        # Application Configuration
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

    def validate(self) -> bool:
        """
        Validate configuration

        Returns:
            True if configuration is valid, raises exception otherwise
        """
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        return True
