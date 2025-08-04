#!/usr/bin/env python3
"""
Commit Message Filter Hook - 过滤提交消息中的特定内容
阻止包含Claude自动生成标识的提交
"""

import sys
import json
import re


def check_commit_message(command):
    """检查提交消息是否包含需要过滤的内容"""

    # 需要过滤的内容模式
    blocked_patterns = [
        r"🤖\s*Generated with\s*\[Claude Code\]",
        r"Co-Authored-By:\s*Claude\s*<noreply@anthropic\.com>",
        r"Generated with.*Claude.*Code",
        r"Claude\s*<noreply@anthropic\.com>",
    ]

    # 检查是否是git commit命令
    if "git commit" in command:
        for pattern in blocked_patterns:
            if re.search(pattern, command, re.IGNORECASE | re.MULTILINE):
                return {
                    "decision": "block",
                    "message": "❌ 提交消息包含自动生成的Claude标识，请使用自定义的提交消息",
                }

    return {"decision": "allow"}


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

    # 检查提交消息
    result = check_commit_message(command)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
