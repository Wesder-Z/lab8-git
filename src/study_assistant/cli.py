"""Командная строка учебного приложения."""

from __future__ import annotations

import argparse
import logging

from .ai_client import AIClient, AIConfigurationError, AIRequestError
from .logging_config import configure_logging
from .service import ask_question


logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Создать парсер аргументов CLI."""
    parser = argparse.ArgumentParser(
        description="Задать вопрос внешнему ИИ API через OpenAI SDK"
    )
    parser.add_argument("question", help="Текст вопроса студента")
    parser.add_argument(
        "--model",
        help="Имя модели; по умолчанию используется OPENAI_MODEL или gpt-5.5",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Включить подробное журналирование",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Запустить CLI и вернуть код завершения процесса."""
    parser = build_parser()
    args = parser.parse_args(argv)
    configure_logging(args.verbose)

    try:
        client = AIClient(model=args.model)
        answer = ask_question(client, args.question)
    except (AIConfigurationError, AIRequestError, TypeError, ValueError) as error:
        logger.error("Ошибка: %s", error)
        return 1

    print(answer)
    return 0
