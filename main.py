"""Точка входа для запуска CLI без предварительной установки пакета."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from study_assistant.cli import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
