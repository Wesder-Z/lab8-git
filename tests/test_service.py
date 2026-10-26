from __future__ import annotations

import pytest

from study_assistant.service import ask_question, build_prompt


class FakeClient:
    def __init__(self) -> None:
        self.prompts: list[str] = []

    def ask(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return "Готовый ответ"


def test_build_prompt_normalizes_question():
    prompt = build_prompt("  Что такое SQL?  ")

    assert "Вопрос студента: Что такое SQL?" in prompt
    assert prompt.startswith("Ты помощник студента-программиста")


def test_ask_question_uses_text_client():
    client = FakeClient()

    assert ask_question(client, "Объясни JOIN") == "Готовый ответ"
    assert len(client.prompts) == 1
    assert "Объясни JOIN" in client.prompts[0]


@pytest.mark.parametrize("question", ["", "   "])
def test_empty_question_is_rejected(question):
    with pytest.raises(ValueError):
        build_prompt(question)
