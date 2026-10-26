from __future__ import annotations

import logging

from study_assistant.ai_client import AIClient


class FakeResponses:
    def create(self, **kwargs):
        return type("Response", (), {"output_text": "Ответ"})()


class FakeOpenAI:
    responses = FakeResponses()


def test_ai_client_writes_operation_to_log(caplog):
    client = AIClient(client=FakeOpenAI())

    with caplog.at_level(logging.INFO, logger="study_assistant.ai_client"):
        client.ask("Проверка журналирования")

    assert "Отправка запроса модели" in caplog.text
    assert "Ответ модели получен успешно" in caplog.text
