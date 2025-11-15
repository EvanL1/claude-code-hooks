#!/usr/bin/env python3
"""
Naming restrictions hook for Claude Code
Prevents only the worst naming conventions
"""

import json
import sys
import re
import os


def check_naming(name, context="file"):
    """Check if a name violates basic naming conventions"""

    # Convert to lowercase for case-insensitive checking
    name_lower = name.lower()

    # Only restrict the most problematic patterns
    restricted_patterns = [
        # Very generic single words (only when used alone)
        r"^(simple|simplify|complex|basic|test|temp|tmp|new|old)$",
        # Numbered versions without context - MORE STRICT
        r"^(test|temp|tmp|file|data|function)\d*",  # Now catches test, test1, test123 etc
        r"^v\d+$",
        # Bad prefixes and suffixes - MORE STRICT
        r"^(new|old|temp|tmp|test)_",  # Catches new_test, old_version etc
        r"_(copy|backup|old|new|temp|tmp|test)(\d+)?$",
        r"_(final|latest|updated)_final$",
        # Meaningless names
        r"^(foo|bar|baz|abc|xyz|asdf|qwerty)$",
        r"^[a-z]$",  # Single letters
        # Multiple version indicators
        r"(new|old|temp|test).*\d+.*v\d+",
    ]

    # Check each pattern
    for pattern in restricted_patterns:
        if re.search(pattern, name_lower):
            return True, pattern

    return False, None


def main():
    try:
        # Read input from Claude Code
        input_data = json.load(sys.stdin)

        # Extract the relevant field based on tool type
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        name_to_check = None
        context = "file"

        if tool_name in ["Write", "Edit", "MultiEdit"]:
            name_to_check = tool_input.get("file_path", "")
            context = "file"
        elif tool_name == "Bash":
            command = tool_input.get("command", "")
            # Only check obvious file creation
            if any(cmd in command for cmd in ["touch ", "mkdir "]):
                parts = command.split()
                for i, part in enumerate(parts):
                    if part in ["touch", "mkdir"] and i + 1 < len(parts):
                        name_to_check = parts[i + 1]
                        context = "file/directory"
                        break

        if name_to_check:
            # Extract just the filename without extension
            basename = os.path.basename(name_to_check)
            name_without_ext = os.path.splitext(basename)[0]

            # Check the name (without extension)
            has_violation, pattern = check_naming(name_without_ext, context)

            if has_violation:
                # Build suggestion message
                suggestions = []
                if (
                    "simple" in name_without_ext.lower()
                    or "complex" in name_without_ext.lower()
                ):
                    suggestions.append(
                        "Be more specific: authentication_handler, data_processor"
                    )
                elif re.search(r"\d+$", name_without_ext):
                    suggestions.append(
                        "Use dates instead: feature_20250105, or descriptive: user_auth_v2"
                    )
                elif "test" in name_without_ext.lower():
                    suggestions.append(
                        "Name after what you're testing: test_user_login, test_api_endpoints"
                    )
                elif (
                    "temp" in name_without_ext.lower()
                    or "tmp" in name_without_ext.lower()
                ):
                    suggestions.append("Use purpose: draft_proposal, work_in_progress")
                else:
                    suggestions.append("Use descriptive names that explain the purpose")

                suggestion_text = " ".join(suggestions)

                # Output error to stderr and exit with code 2
                error_msg = f"⚠️  Poor {context} naming detected: '{basename}'. {suggestion_text}"
                print(error_msg, file=sys.stderr)
                sys.exit(2)  # Exit code 2 = blocking error

        # If no violations, exit silently
        sys.exit(0)

    except Exception:
        # Don't block on errors - exit silently
        sys.exit(0)


if __name__ == "__main__":
    main()
