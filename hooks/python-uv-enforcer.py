#!/usr/bin/env python3
"""
Python UV Enforcer Hook - 强制使用 uv 代替传统 Python 工具
"""

import json
import sys
import re


def main():
    try:
        # Read input from Claude Code
        input_data = json.load(sys.stdin)

        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        if tool_name == "Bash":
            command = tool_input.get("command", "")

            # Check for Python tools
            python_tools = [
                "pip",
                "pip3",
                "python",
                "python3",
                "pytest",
                "pylint",
                "flake8",
                "black",
                "mypy",
                "isort",
                "poetry",
                "pipenv",
                "conda",
                "virtualenv",
                "pyenv",
            ]

            # Check if command uses Python tools (but not venv or uv)
            pattern = r"^(" + "|".join(python_tools) + r")\b"
            if re.match(pattern, command) and not re.match(
                r"^(python3?\s+-m\s+venv|uv\s+)", command
            ):
                # ANSI color codes
                red = "\033[1;31m"
                yellow = "\033[1;33m"
                green = "\033[1;32m"
                blue = "\033[1;34m"
                reset = "\033[0m"

                error_msg = f"""{red}❌ Direct Python tool usage detected!{reset}
{yellow}📝 Command blocked:{reset} {command}
{green}✨ Use uv instead:{reset}"""

                # Provide specific suggestions
                if "pip" in command and "install" in command:
                    error_msg += "\n   uv pip install ..."
                elif command.startswith("python"):
                    error_msg += "\n   uv run python ..."
                elif command.startswith("pytest"):
                    error_msg += "\n   uv run pytest ..."
                elif command.startswith("black"):
                    error_msg += "\n   uv run black ..."
                elif command.startswith("mypy"):
                    error_msg += "\n   uv run mypy ..."
                else:
                    error_msg += f"\n   uv run {command}"

                error_msg += (
                    f"\n{blue}💡 Learn more:{reset} https://github.com/astral-sh/uv"
                )

                print(error_msg, file=sys.stderr)
                sys.exit(2)  # Exit code 2 = blocking error

        # If no violation, exit silently
        sys.exit(0)

    except Exception:
        # Silent failure - exit silently
        sys.exit(0)


if __name__ == "__main__":
    main()
