#!/usr/bin/env python3
"""
Command Logger Hook - 命令日志记录
记录所有执行的命令到日志文件，方便回溯和审计
"""

import sys
import json
import os
from datetime import datetime


def log_command(tool_use):
    """记录命令到日志文件"""
    try:
        log_dir = os.path.expanduser("~/.claude/logs")
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(
            log_dir, f"commands_{datetime.now().strftime('%Y%m%d')}.log"
        )

        # 构建日志条目
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tool = tool_use.get("tool") or tool_use.get("tool_name", "Unknown")

        log_entry = {
            "timestamp": timestamp,
            "tool": tool,
        }

        # 根据工具类型记录不同信息
        arguments = tool_use.get("arguments") or tool_use.get("tool_input", {})

        if tool == "Bash":
            log_entry["command"] = arguments.get("command", "")
        elif tool in ["Write", "Edit", "MultiEdit"]:
            log_entry["file"] = arguments.get("file_path", "")
        elif tool == "Read":
            log_entry["file"] = arguments.get("file_path", "")
        elif tool in ["Grep", "Glob"]:
            log_entry["pattern"] = arguments.get("pattern", "")
            log_entry["path"] = arguments.get("path", ".")

        # 写入日志
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    except Exception:
        # 日志记录失败不应阻止命令执行
        pass


def main():
    """主函数"""
    try:
        tool_use_json = sys.stdin.read()
        tool_use = json.loads(tool_use_json)

        log_command(tool_use)

        # 总是允许操作
        sys.exit(0)

    except Exception:
        # 错误时不阻止操作
        sys.exit(0)


if __name__ == "__main__":
    main()
