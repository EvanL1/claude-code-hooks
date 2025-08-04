#!/usr/bin/env python3
"""
AWS Safety Check Hook - AWS操作安全检查
检查AWS CLI命令，防止误操作生产环境
"""

import sys
import json
import re
import os


def check_aws_command(command):
    """检查AWS命令的安全性"""
    messages = []

    # 检查是否设置了配置文件
    if "aws" in command and "--profile" not in command:
        messages.append("💡 建议: 使用 --profile 参数明确指定AWS配置文件")

    # 危险操作检查
    dangerous_operations = {
        r"aws\s+.*\s+delete": "删除操作，请确认目标资源",
        r"aws\s+.*\s+terminate": "终止操作，将永久删除资源",
        r"aws\s+.*\s+remove": "移除操作，请确认操作对象",
        r"aws\s+s3\s+rm.*--recursive": "递归删除S3对象，请谨慎操作",
        r"aws\s+cloudformation\s+delete-stack": "删除CloudFormation栈将删除所有相关资源",
        r"aws\s+rds\s+delete-db": "删除RDS数据库实例，请确认已备份",
        r"aws\s+ec2\s+terminate-instances": "终止EC2实例，数据将丢失",
    }

    for pattern, warning in dangerous_operations.items():
        if re.search(pattern, command, re.IGNORECASE):
            messages.append(f"⚠️ 危险操作: {warning}")

    # 生产环境检查
    prod_indicators = ["prod", "production", "prd"]
    for indicator in prod_indicators:
        if indicator in command.lower():
            messages.append("🚨 警告: 可能在操作生产环境，请格外小心")
            break

    # S3操作检查
    if "s3" in command:
        # 公开访问检查
        if "--acl public-read" in command or "--acl public-read-write" in command:
            messages.append("⚠️ 安全警告: 设置了公开访问权限，请确认是否有必要")

        # 同步操作检查
        if "s3 sync" in command and "--delete" in command:
            messages.append("⚠️ 注意: sync --delete 会删除目标中源不存在的文件")

    # IAM操作检查
    if "iam" in command:
        if "attach-" in command and "AdministratorAccess" in command:
            messages.append("🚨 安全警告: 正在附加管理员权限，请确认必要性")

        if "create-access-key" in command:
            messages.append("🔐 安全提醒: 创建访问密钥后请妥善保管，避免泄露")

    # Lambda操作检查
    if "lambda" in command and "update-function-code" in command:
        messages.append("💡 提示: 更新Lambda代码前建议先创建版本或别名")

    # DynamoDB操作检查
    if "dynamodb" in command:
        if "delete-table" in command:
            messages.append("⚠️ 警告: 删除DynamoDB表将永久丢失所有数据")

        if "update-table" in command and "--billing-mode" in command:
            messages.append("💰 注意: 更改计费模式可能影响成本")

    # 成本相关操作
    cost_operations = ["run-instances", "create-db-instance", "create-cluster"]
    for op in cost_operations:
        if op in command:
            messages.append("💰 成本提醒: 此操作会产生AWS费用，请注意成本控制")
            break

    # 区域检查
    if "--region" not in command and "AWS_DEFAULT_REGION" not in os.environ:
        messages.append("💡 建议: 使用 --region 参数明确指定AWS区域")

    return messages


def main():
    """主函数"""
    tool_use_json = sys.stdin.read()
    tool_use = json.loads(tool_use_json)

    if tool_use.get("tool") != "Bash":
        print(json.dumps({"decision": "allow"}))
        return

    command = tool_use.get("arguments", {}).get("command", "")

    # 检查AWS命令
    if "aws " in command:
        messages = check_aws_command(command)
        if messages:
            print(json.dumps({"decision": "allow", "message": "\n".join(messages)}))
        else:
            print(json.dumps({"decision": "allow"}))
    else:
        print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
