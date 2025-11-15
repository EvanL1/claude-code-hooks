#!/usr/bin/env python3
"""
Java Build Check Hook - Java构建和代码质量检查
在Maven/Gradle构建时提供最佳实践建议
"""

import sys
import json
import os


def check_java_command(command):
    """检查Java相关命令"""
    messages = []

    # Maven相关检查
    if "mvn" in command:
        # 建议使用wrapper
        if "mvn " in command and os.path.exists("./mvnw"):
            messages.append("💡 建议: 使用 ./mvnw 而不是 mvn 以确保版本一致性")

        # 跳过测试警告
        if "-DskipTests" in command or "-Dmaven.test.skip=true" in command:
            messages.append("⚠️ 注意: 跳过了测试，请确保代码质量")

        # 建议清理
        if "package" in command and "clean" not in command:
            messages.append("💡 建议: 使用 'mvn clean package' 确保干净构建")

        # 部署检查
        if "deploy" in command:
            messages.append("⚠️ 注意: 即将部署到Maven仓库，请确认版本号和内容")

    # Gradle相关检查
    if "gradle" in command or "./gradlew" in command:
        # 建议使用wrapper
        if "gradle " in command and os.path.exists("./gradlew"):
            messages.append("💡 建议: 使用 ./gradlew 而不是 gradle 以确保版本一致性")

        # 跳过测试警告
        if "-x test" in command:
            messages.append("⚠️ 注意: 跳过了测试，请确保代码质量")

        # 发布检查
        if "publish" in command:
            messages.append("⚠️ 注意: 即将发布制品，请确认版本号")

    # Spring Boot特定检查
    if "spring-boot:run" in command:
        messages.append("💡 提示: 使用 -Dspring-boot.run.profiles=dev 指定开发环境配置")

    # JVM参数建议
    if "java -jar" in command:
        if "-Xmx" not in command:
            messages.append("💡 建议: 考虑添加 -Xmx 参数限制最大堆内存")
        if "prod" in command.lower() and "-XX:+UseG1GC" not in command:
            messages.append("💡 建议: 生产环境考虑使用 -XX:+UseG1GC 垃圾收集器")

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

        # 检查Java相关命令
        java_keywords = ["java", "mvn", "gradle", "gradlew", "jar"]
        if any(keyword in command for keyword in java_keywords):
            messages = check_java_command(command)
            if messages:
                print("\n".join(messages))

        # 总是允许操作
        sys.exit(0)

    except Exception:
        # 错误时不阻止操作
        sys.exit(0)


if __name__ == "__main__":
    main()
