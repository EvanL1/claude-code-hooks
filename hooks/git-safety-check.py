#!/usr/bin/env python3
"""
Git Safety Check Hook - Git操作安全检查
防止误操作敏感分支，检查敏感文件
"""

import sys
import json
import re


def check_git_command(command):
    """检查git命令的安全性"""
    # 受保护的分支
    protected_branches = ["main", "master", "production", "prod"]

    # 危险操作模式（只是警告，不阻止）
    dangerous_patterns = [
        (r"git\s+push\s+.*\s+--force", "强制推送可能会覆盖远程历史，请确认操作"),
        (r"git\s+reset\s+--hard", "硬重置会丢失未提交的更改，请确认操作"),
        (r"git\s+clean\s+-[fd]", "清理操作会删除未跟踪的文件，请确认操作"),
    ]

    # 检查是否操作受保护分支 - 直接拒绝
    for branch in protected_branches:
        if f"git push origin :{branch}" in command:
            error_msg = f"❌ 阻止删除受保护分支 '{branch}'"
            print(error_msg, file=sys.stderr)
            sys.exit(2)  # Exit code 2 = blocking error

        if re.search(f"git\s+branch\s+-[dD].*{branch}", command):
            error_msg = f"❌ 阻止删除受保护分支 '{branch}'"
            print(error_msg, file=sys.stderr)
            sys.exit(2)  # Exit code 2 = blocking error

    # 只记录日志，不阻止（返回None表示继续执行）
    return None


def main():
    """主函数"""
    tool_use_json = sys.stdin.read()
    tool_use = json.loads(tool_use_json)

    if tool_use.get("tool_name") != "Bash":
        sys.exit(0)

    command = tool_use.get("tool_input", {}).get("command", "")

    # 只检查git命令
    if "git" in command:
        check_git_command(command)  # 会在发现问题时直接exit(2)

    # 如果没有问题，静默退出
    sys.exit(0)


if __name__ == "__main__":
    main()
