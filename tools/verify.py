"""Запустить локальную проверку проекта без обращения к внешнему API."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    """Выполнить компиляцию, flake8 и pytest."""
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(ROOT / "src")
    commands = [
        [sys.executable, "-m", "compileall", "-q", "."],
        [sys.executable, "-m", "flake8", "."],
        [sys.executable, "-m", "pytest", "-q"],
    ]
    for command in commands:
        print(f"$ {' '.join(command)}")
        subprocess.run(command, cwd=ROOT, env=environment, check=True)


if __name__ == "__main__":
    main()
