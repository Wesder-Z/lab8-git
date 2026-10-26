"""Пакет учебного CLI-приложения с интеграцией OpenAI API."""

from .ai_client import AIClient, AIConfigurationError, AIRequestError
from .service import ask_question, build_prompt

__all__ = [
    "AIClient",
    "AIConfigurationError",
    "AIRequestError",
    "ask_question",
    "build_prompt",
]
