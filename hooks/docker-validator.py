#!/usr/bin/env python3
import sys
import json
import re


def validate_docker_command(tool_use):
    """验证Docker命令，防止使用不当的镜像名称后缀"""

    if tool_use.get("tool_name") != "Bash":
        sys.exit(0)

    command = tool_use.get("tool_input", {}).get("command", "")

    # 检查是否是docker build命令
    if "docker build" in command or "docker tag" in command:
        # 查找 -t 标签参数
        tag_pattern = r"-t\s+([^\s]+)"
        matches = re.findall(tag_pattern, command)

        for tag in matches:
            # 检查是否包含不允许的后缀（注意：latest是允许的）
            bad_suffixes = ["-v2", "-v3", "-test", "-dev", "-prod", "-staging"]
            image_name = tag.split(":")[0]  # 获取镜像名称部分

            for suffix in bad_suffixes:
                if image_name.endswith(suffix):
                    clean_name = image_name[: -len(suffix)]
                    tag_part = tag.split(":")[1] if ":" in tag else "latest"
                    error_msg = f"镜像名称不应使用'{suffix}'后缀。建议使用: {clean_name}:{tag_part}"
                    print(error_msg, file=sys.stderr)
                    sys.exit(2)  # Exit code 2 = blocking error


if __name__ == "__main__":
    # 读取输入
    tool_use_json = sys.stdin.read()
    tool_use = json.loads(tool_use_json)

    validate_docker_command(tool_use)

    # 如果没有问题，静默退出
    sys.exit(0)
