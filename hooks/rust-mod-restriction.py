#!/usr/bin/env python3
"""
Rust mod.rs restriction hook for Claude Code
Prevents creation of mod.rs files in Rust projects
"""

import json
import sys
import os


def main():
    try:
        # Read input from Claude Code
        input_data = json.load(sys.stdin)

        # Extract the relevant field based on tool type
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        file_path = None

        # Check Write, Edit, and MultiEdit tools
        if tool_name in ["Write", "Edit", "MultiEdit"]:
            file_path = tool_input.get("file_path", "")

        # Check if the file path contains mod.rs
        if file_path:
            basename = os.path.basename(file_path)

            # Block if the file is mod.rs
            if basename == "mod.rs":
                error_msg = """🚫 不允许创建或修改 mod.rs 文件！

根据项目规范，Rust 代码不应使用 mod.rs 的方式组织。
请使用其他方式组织模块，例如：
  - 使用 lib.rs 或 main.rs 中的 mod 声明
  - 使用独立的模块文件（如 module_name.rs）
  - 使用目录名加模块文件（如 module_name/submodule.rs，在 module_name.rs 中声明）"""

                print(error_msg, file=sys.stderr)
                sys.exit(2)  # Exit code 2 = blocking error

        # If no violations, exit silently
        sys.exit(0)

    except Exception:
        # Don't block on errors - exit silently
        sys.exit(0)


if __name__ == "__main__":
    main()
