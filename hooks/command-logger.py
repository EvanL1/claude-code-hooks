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
    log_dir = os.path.expanduser("~/.claude/logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(
        log_dir, f"commands_{datetime.now().strftime('%Y%m%d')}.log"
    )

    # 构建日志条目
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tool = tool_use.get("tool", "Unknown")

    log_entry = {
        "timestamp": timestamp,
        "tool": tool,
    }

    # 根据工具类型记录不同信息
    if tool == "Bash":
        log_entry["command"] = tool_use.get("arguments", {}).get("command", "")
    elif tool in ["Write", "Edit", "MultiEdit"]:
        log_entry["file"] = tool_use.get("arguments", {}).get("file_path", "")
    elif tool == "Read":
        log_entry["file"] = tool_use.get("arguments", {}).get("file_path", "")
    elif tool in ["Grep", "Glob"]:
        log_entry["pattern"] = tool_use.get("arguments", {}).get("pattern", "")
        log_entry["path"] = tool_use.get("arguments", {}).get("path", ".")

    # 写入日志
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception:
        # 日志记录失败不应阻止命令执行
        pass

    return {"decision": "allow"}


def main():
    """主函数"""
    tool_use_json = sys.stdin.read()
    tool_use = json.loads(tool_use_json)

    result = log_command(tool_use)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
