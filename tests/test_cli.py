from __future__ import annotations

from study_assistant.cli import build_parser


def test_cli_parser_accepts_question_and_model():
    args = build_parser().parse_args(["Что такое API?", "--model", "test-model"])

    assert args.question == "Что такое API?"
    assert args.model == "test-model"
