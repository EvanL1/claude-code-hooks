#!/usr/bin/env python3
import sys
import json
import re


def validate_docker_command(tool_use):
    """验证Docker命令，防止使用不当的镜像名称后缀"""

    if tool_use.get("tool") != "Bash":
        return {"decision": "allow"}

    command = tool_use.get("arguments", {}).get("command", "")

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
                    return {
                        "decision": "block",
                        "message": f"镜像名称不应使用'{suffix}'后缀。建议使用: {clean_name}:{tag_part}",
                    }

    return {"decision": "allow"}


if __name__ == "__main__":
    # 读取输入
    tool_use_json = sys.stdin.read()
    tool_use = json.loads(tool_use_json)

    result = validate_docker_command(tool_use)

    print(json.dumps(result))
    sys.exit(0 if result.get("decision") == "allow" else 1)
