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

    # 危险操作模式
    dangerous_patterns = [
        (r"git\s+push\s+.*\s+--force", "强制推送可能会覆盖远程历史，请确认操作"),
        (r"git\s+reset\s+--hard", "硬重置会丢失未提交的更改，请确认操作"),
        (r"git\s+clean\s+-[fd]", "清理操作会删除未跟踪的文件，请确认操作"),
    ]

    # 检查是否操作受保护分支
    for branch in protected_branches:
        if f"git push origin :{branch}" in command:
            return {"decision": "block", "message": f"❌ 阻止删除受保护分支 '{branch}'"}

        if re.search(f"git\s+branch\s+-[dD].*{branch}", command):
            return {"decision": "block", "message": f"❌ 阻止删除受保护分支 '{branch}'"}

    # 检查危险操作
    for pattern, warning in dangerous_patterns:
        if re.search(pattern, command):
            return {"decision": "allow", "message": f"⚠️ 警告: {warning}"}

    # 检查是否提交敏感文件
    if "git add" in command or "git commit" in command:
        sensitive_patterns = [
            ".env",
            ".env.local",
            ".env.production",
            "secrets.",
            "credentials.",
            "password",
            ".pem",
            ".key",
            "id_rsa",
            "id_dsa",
        ]

        for pattern in sensitive_patterns:
            if pattern in command:
                return {
                    "decision": "allow",
                    "message": f"⚠️ 注意: 可能包含敏感文件 '{pattern}'，请确认是否应该提交",
                }

    return {"decision": "allow"}


def main():
    """主函数"""
    tool_use_json = sys.stdin.read()
    tool_use = json.loads(tool_use_json)

    if tool_use.get("tool") != "Bash":
        print(json.dumps({"decision": "allow"}))
        return

    command = tool_use.get("arguments", {}).get("command", "")

    # 只检查git命令
    if "git" in command:
        result = check_git_command(command)
        print(json.dumps(result))
    else:
        print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
