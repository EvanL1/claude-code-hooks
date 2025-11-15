#!/usr/bin/env python3
"""
NPM Safety Check Hook - NPM/Yarn操作安全检查
检查包安装、发布等操作的安全性
"""

import sys
import json
import re


def check_npm_command(command):
    """检查npm/yarn命令的安全性"""
    messages = []

    # 危险的npm操作
    dangerous_operations = {
        r"npm\s+publish": "即将发布包到npm registry，请确认版本和内容",
        r"npm\s+unpublish": "取消发布会影响依赖此包的用户",
        r"npm\s+link": "全局链接包可能影响其他项目",
        r"npm\s+install\s+.*--global": "全局安装包会影响系统环境",
        r"npm\s+install\s+.*--force": "强制安装可能导致依赖冲突",
        r"npm\s+audit\s+fix\s+--force": "强制修复可能引入破坏性更改",
        r"yarn\s+publish": "即将发布包到registry",
        r"yarn\s+link": "全局链接包可能影响其他项目",
    }

    # 检查危险操作
    for pattern, warning in dangerous_operations.items():
        if re.search(pattern, command, re.IGNORECASE):
            messages.append(f"⚠️ 注意: {warning}")

    # 检查是否安装了已知的有问题的包
    suspicious_packages = [
        "node-ipc",  # 曾有恶意代码事件
        "colors",  # 曾有恶意代码事件
        "faker",  # 已被作者删除
    ]

    for pkg in suspicious_packages:
        if f"install {pkg}" in command or f"add {pkg}" in command:
            messages.append(f"⚠️ 警告: 包 '{pkg}' 曾有安全问题，请谨慎使用")

    # 建议使用 npm ci 而不是 npm install 在CI环境
    if "npm install" in command and ("CI" in command or "ci" in command.lower()):
        messages.append(
            "💡 建议: 在CI环境中使用 'npm ci' 而不是 'npm install' 以获得更快和更可靠的安装"
        )

    return messages


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

        # 检查npm/yarn命令
        if any(cmd in command for cmd in ["npm", "yarn", "pnpm"]):
            messages = check_npm_command(command)
            if messages:
                # 输出警告到stdout，不阻止操作
                print("\n".join(messages))

        # 总是允许操作
        sys.exit(0)

    except Exception:
        # 错误时不阻止操作
        sys.exit(0)


if __name__ == "__main__":
    main()
