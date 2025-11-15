#!/usr/bin/env python3
"""
Cargo Auto Format Hook - 自动格式化和检查Rust代码
在cargo build/check后提醒运行fmt和clippy
"""

import sys
import json
import os


def should_run_format(command):
    """判断是否应该提醒格式化"""
    cargo_commands = ["cargo build", "cargo check", "cargo test"]
    return any(cmd in command for cmd in cargo_commands)


def main():
    """主函数"""
    try:
        tool_use_json = sys.stdin.read()
        tool_use = json.loads(tool_use_json)

        # 只处理Bash命令
        tool = tool_use.get("tool") or tool_use.get("tool_name")
        if tool != "Bash":
            sys.exit(0)

        # 获取命令
        arguments = tool_use.get("arguments") or tool_use.get("tool_input", {})
        command = arguments.get("command", "")

        # 如果是cargo相关命令，提醒格式化
        if should_run_format(command):
            # 检查是否是Rust项目
            if os.path.exists("./Cargo.toml"):
                print(
                    "💡 提示: 构建完成后建议运行 'cargo fmt' 和 'cargo clippy' 检查代码质量"
                )

        # 总是允许操作
        sys.exit(0)

    except Exception:
        # 错误时不阻止操作
        sys.exit(0)


if __name__ == "__main__":
    main()
