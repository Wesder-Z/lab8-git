"""Прикладная логика подготовки вопросов к ИИ-клиенту."""

from __future__ import annotations

import logging
from typing import Protocol


logger = logging.getLogger(__name__)


class TextClient(Protocol):
    """Минимальный интерфейс клиента, который умеет отвечать на запрос."""

    def ask(self, prompt: str) -> str:
        """Получить текстовый ответ на запрос."""


def build_prompt(question: str) -> str:
    """Сформировать понятный запрос для внешнего ИИ API."""
    if not isinstance(question, str):
        raise TypeError("Вопрос должен быть строкой")

    cleaned_question = question.strip()
    if not cleaned_question:
        raise ValueError("Вопрос не может быть пустым")

    return (
        "Ты помощник студента-программиста. Ответь на русском языке простыми "
        "словами и приведи небольшой пример, если он уместен.\n\n"
        f"Вопрос студента: {cleaned_question}"
    )


def ask_question(client: TextClient, question: str) -> str:
    """Подготовить вопрос, отправить его клиенту и вернуть ответ."""
    prompt = build_prompt(question)
    logger.info("Подготовлен вопрос длиной %d символов", len(question.strip()))
    answer = client.ask(prompt)
    logger.info("Получен ответ длиной %d символов", len(answer))
    return answer
