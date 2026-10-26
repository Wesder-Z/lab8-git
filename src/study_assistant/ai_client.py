"""Клиент внешнего OpenAI Responses API."""

from __future__ import annotations

import logging
import os
from typing import Any

from openai import OpenAI


logger = logging.getLogger(__name__)


class AIConfigurationError(RuntimeError):
    """Конфигурация внешнего API неполна."""


class AIRequestError(RuntimeError):
    """Внешний API не смог обработать запрос."""


class AIClient:
    """Отправлять текстовые вопросы через официальный Python SDK OpenAI."""

    def __init__(self, model: str | None = None, client: Any | None = None) -> None:
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-5.5")
        if client is not None:
            self._client = client
            return

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise AIConfigurationError(
                "Задайте переменную окружения OPENAI_API_KEY перед запуском"
            )
        self._client = OpenAI(api_key=api_key)

    def ask(self, prompt: str) -> str:
        """Отправить запрос через Responses API и вернуть текст ответа."""
        if not isinstance(prompt, str):
            raise TypeError("Запрос должен быть строкой")
        if not prompt.strip():
            raise ValueError("Запрос не может быть пустым")

        logger.info("Отправка запроса модели %s", self.model)
        try:
            response = self._client.responses.create(
                model=self.model,
                input=prompt,
            )
        except Exception as error:
            logger.exception("Ошибка внешнего ИИ API")
            raise AIRequestError("Не удалось получить ответ от ИИ API") from error

        answer = str(getattr(response, "output_text", "") or "").strip()
        if not answer:
            raise AIRequestError("ИИ API вернул пустой ответ")

        logger.info("Ответ модели получен успешно")
        return answer
