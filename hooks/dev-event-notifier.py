#!/usr/bin/env python3
"""
开发事件通知Hook - 捕获开发事件并发送通知
支持构建、测试、部署等事件
"""

import sys
import json
import subprocess
import os
import re

# 通知器二进制文件路径
NOTIFIER_PATH = os.path.expanduser(
    "~/.claude/notifiers/claude-notifier/target/release/claude-notifier"
)


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


def send_notification(event_type, title, content, level="info"):
    """调用Rust通知器发送通知"""
    if not os.path.exists(NOTIFIER_PATH):
        # 如果编译版本不存在，使用cargo run
        cmd = [
            "cargo",
            "run",
            "--manifest-path",
            os.path.expanduser("~/.claude/notifiers/claude-notifier/Cargo.toml"),
            "--",
            "hook",
        ]
    else:
        cmd = [NOTIFIER_PATH, "hook"]

    data = {"event": event_type, "title": title, "content": content, "level": level}

    try:
        result = subprocess.run(
            cmd, input=json.dumps(data), capture_output=True, text=True, timeout=5
        )
        return result.returncode == 0
    except Exception as e:
        print(f"通知发送失败: {str(e)}", file=sys.stderr)
        return False


def main():
    """主函数"""
    # 从stdin读取hook数据
    tool_use_json = sys.stdin.read()
    tool_use = json.loads(tool_use_json)

    # 只处理Bash命令
    if tool_use.get("tool") != "Bash":
        print(json.dumps({"decision": "allow"}))
        return

    command = tool_use.get("arguments", {}).get("command", "")

    # 检测事件类型
    event_type, description = detect_event_from_command(command)

    if event_type:
        # 获取用户信息
        user = os.environ.get("USER", "Unknown")

        # 构建通知内容
        title = f"{description} - {user}"
        content = f"命令: `{command}`\n路径: {os.getcwd()}"

        # 根据事件类型设置级别
        level = "info"
        if "deploy" in event_type:
            level = "warning"
        elif "security" in event_type:
            level = "critical"

        # 发送通知（异步，不阻塞命令执行）
        subprocess.Popen(
            ["python3", __file__, "--send", event_type, title, content, level],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    # 始终允许命令执行
    print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--send":
        # 独立进程发送通知
        _, _, event_type, title, content, level = sys.argv
        send_notification(event_type, title, content, level)
    else:
        main()
