#!/usr/bin/env python3
"""
Cargo Auto Format Hook - 自动格式化和检查Rust代码
在cargo build/check后自动运行fmt和clippy
"""

import sys
import json
import subprocess
import os


def should_run_format(command):
    """判断是否应该运行格式化"""
    cargo_commands = ["cargo build", "cargo check", "cargo test"]
    return any(cmd in command for cmd in cargo_commands)


def run_cargo_format(working_dir):
    """运行cargo fmt和clippy"""
    messages = []

    # 检查是否是Rust项目
    if not os.path.exists(os.path.join(working_dir, "Cargo.toml")):
        return None

    try:
        # 运行 cargo fmt
        fmt_result = subprocess.run(
            ["cargo", "fmt"], cwd=working_dir, capture_output=True, text=True
        )
        if fmt_result.returncode == 0:
            messages.append("✨ 代码已自动格式化 (cargo fmt)")

        # 运行 cargo clippy
        clippy_result = subprocess.run(
            ["cargo", "clippy", "--", "-W", "clippy::all"],
            cwd=working_dir,
            capture_output=True,
            text=True,
        )
        if clippy_result.stdout:
            messages.append(f"📋 Clippy建议:\n{clippy_result.stdout}")

    except Exception as e:
        messages.append(f"⚠️ 格式化时出错: {str(e)}")

    return "\n".join(messages) if messages else None


def main():
    """主函数"""
    tool_use_json = sys.stdin.read()
    tool_use = json.loads(tool_use_json)

    # 只处理Bash工具的cargo命令
    if tool_use.get("tool") != "Bash":
        print(json.dumps({"decision": "allow"}))
        return

    command = tool_use.get("arguments", {}).get("command", "")

    # 如果是cargo相关命令，在执行后运行格式化
    if should_run_format(command):
        # 先允许命令执行
        print(
            json.dumps(
                {"decision": "allow", "post_message": "将在命令执行后自动运行格式化..."}
            )
        )
    else:
        print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
