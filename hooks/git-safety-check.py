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
    # 检查是否使用 --no-verify 跳过hooks - 直接阻止
    # 只检测作为命令参数的 --no-verify，不检测引号内或heredoc内的
    # 方法：排除在引号内和heredoc内的内容
    import shlex

    # 简单检测：--no-verify 作为独立参数（前后有空格或在行首/行尾）
    if re.search(r'(^|\s)--no-verify(\s|$)', command):
        # 进一步检查：确保不在引号或heredoc内
        # 检测是否在 -m "..." 或 <<'EOF' ... EOF 之间
        in_quotes = False
        in_heredoc = False

        # 简化检测：如果命令中有 -m "..." 或 <<'EOF'，检查 --no-verify 的位置
        msg_match = re.search(r'-m\s+["\'].*?["\']', command)
        heredoc_match = re.search(r'<<["\']?EOF["\']?.*?EOF', command, re.DOTALL)

        verify_pos = command.find('--no-verify')
        safe_in_message = False

        if msg_match and msg_match.start() < verify_pos < msg_match.end():
            safe_in_message = True
        if heredoc_match and heredoc_match.start() < verify_pos < heredoc_match.end():
            safe_in_message = True

        if not safe_in_message:
            print("❌ 禁止使用 --no-verify 跳过Git Hooks验证！", file=sys.stderr)
            sys.exit(2)

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

        if re.search(rf"git\s+branch\s+-[dD].*{branch}", command):
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
