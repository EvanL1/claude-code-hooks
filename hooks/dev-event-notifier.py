#!/usr/bin/env python3
"""
开发事件通知Hook - 捕获开发事件并记录日志
支持构建、测试、部署等事件（简化版本，仅记录）
"""

import sys
import json
import os
import re
from datetime import datetime


def detect_event_from_command(command):
    """从命令推断事件类型"""
    event_patterns = {
        # 构建相关
        r"(cargo|maven|gradle|npm|yarn|pnpm)\s+(build|compile)": (
            "build_start",
            "构建开始",
        ),
        r"cargo\s+check": ("build_check", "代码检查"),
        r"npm\s+run\s+build": ("build_start", "前端构建"),
        # 测试相关
        r"(cargo|npm|yarn|pytest|jest)\s+test": ("test_start", "测试开始"),
        r"mvn\s+test": ("test_start", "Maven测试"),
        # 部署相关
        r"aws\s+.*\s+deploy": ("deploy_start", "AWS部署"),
        r"docker\s+push": ("deploy_start", "Docker镜像推送"),
        r"git\s+push.*production": ("deploy_start", "生产环境部署"),
        # Git操作
        r"git\s+commit": ("code_commit", "代码提交"),
        r"git\s+push": ("code_push", "代码推送"),
        r"git\s+merge": ("code_merge", "代码合并"),
        # 安全相关
        r"npm\s+audit": ("security_check", "依赖安全检查"),
        r"cargo\s+audit": ("security_check", "Rust安全审计"),
    }

    for pattern, (event, description) in event_patterns.items():
        if re.search(pattern, command, re.IGNORECASE):
            return event, description

    return None, None


def log_event(event_type, description, command):
    """记录事件到日志文件"""
    try:
        log_dir = os.path.expanduser("~/.claude/logs/events")
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(
            log_dir, f"events_{datetime.now().strftime('%Y%m%d')}.log"
        )

        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "event_type": event_type,
            "description": description,
            "command": command,
            "user": os.environ.get("USER", "Unknown"),
            "cwd": os.getcwd(),
        }

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    except Exception:
        # 日志记录失败不应阻止命令执行
        pass


def main():
    """主函数"""
    try:
        # 从stdin读取hook数据
        tool_use_json = sys.stdin.read()
        tool_use = json.loads(tool_use_json)

        # 只处理Bash命令
        tool = tool_use.get("tool") or tool_use.get("tool_name")
        if tool != "Bash":
            sys.exit(0)

        # 获取命令
        arguments = tool_use.get("arguments") or tool_use.get("tool_input", {})
        command = arguments.get("command", "")

        # 检测事件类型
        event_type, description = detect_event_from_command(command)

        if event_type:
            # 记录事件到日志
            log_event(event_type, description, command)

            # 显示事件信息
            level_emoji = {
                "build": "🔨",
                "test": "🧪",
                "deploy": "🚀",
                "code": "💾",
                "security": "🔒",
            }

            category = event_type.split("_")[0]
            emoji = level_emoji.get(category, "📝")
            print(f"{emoji} {description}")

        # 始终允许命令执行
        sys.exit(0)

    except Exception:
        # 错误时不阻止操作
        sys.exit(0)


if __name__ == "__main__":
    main()
