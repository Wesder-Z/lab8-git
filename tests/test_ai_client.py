from __future__ import annotations

from types import SimpleNamespace

import pytest

from study_assistant.ai_client import (
    AIClient,
    AIConfigurationError,
    AIRequestError,
)


class FakeResponses:
    def __init__(self, response=None, error=None) -> None:
        self.response = response
        self.error = error
        self.calls: list[dict[str, str]] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if self.error is not None:
            raise self.error
        return self.response


class FakeOpenAI:
    def __init__(self, responses: FakeResponses) -> None:
        self.responses = responses


def test_client_calls_responses_api_and_returns_text():
    responses = FakeResponses(SimpleNamespace(output_text="  Ответ модели  "))
    client = AIClient(model="test-model", client=FakeOpenAI(responses))

    assert client.ask("Вопрос") == "Ответ модели"
    assert responses.calls == [{"model": "test-model", "input": "Вопрос"}]


def test_client_wraps_api_error():
    responses = FakeResponses(error=RuntimeError("network"))
    client = AIClient(client=FakeOpenAI(responses))

    with pytest.raises(AIRequestError):
        client.ask("Вопрос")


def test_client_requires_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(AIConfigurationError):
        AIClient()
