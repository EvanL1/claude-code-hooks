#!/usr/bin/env python3
"""
File Statistics Hook - 显示文件统计信息
当文件被创建或修改时，显示行数、字符数、函数数等信息
"""

import sys
import json
import os
import re


def count_functions(content, file_ext):
    """根据文件扩展名统计函数数量"""
    function_counts = {
        "python": len(re.findall(r"^\s*def\s+\w+", content, re.MULTILINE))
        + len(re.findall(r"^\s*async\s+def\s+\w+", content, re.MULTILINE)),
        "javascript": len(
            re.findall(
                r"function\s+\w+\s*\(|const\s+\w+\s*=\s*\(|^\s*\w+\s*\(",
                content,
                re.MULTILINE,
            )
        ),
        "java": len(
            re.findall(
                r"^\s*(public|private|protected)?\s*(static)?\s*\w+\s+\w+\s*\(",
                content,
                re.MULTILINE,
            )
        ),
        "go": len(re.findall(r"^\s*func\s+", content, re.MULTILINE)),
        "rust": len(re.findall(r"^\s*fn\s+\w+", content, re.MULTILINE)),
    }

    ext_map = {
        ".py": "python",
        ".js": "javascript",
        ".jsx": "javascript",
        ".ts": "javascript",
        ".tsx": "javascript",
        ".java": "java",
        ".go": "go",
        ".rs": "rust",
    }

    lang = ext_map.get(file_ext, None)
    return function_counts.get(lang, 0) if lang else 0


def analyze_file(file_path):
    """分析文件并返回统计信息"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.split("\n")
        file_ext = os.path.splitext(file_path)[1]

        stats = {
            "lines": len(lines),
            "characters": len(content),
            "words": len(content.split()),
            "functions": count_functions(content, file_ext),
            "classes": len(re.findall(r"^\s*class\s+\w+", content, re.MULTILINE)),
        }

        return stats
    except Exception:
        return None


def main():
    """主函数"""
    # 从stdin读取tool use信息
    tool_use_json = sys.stdin.read()
    tool_use = json.loads(tool_use_json)

    # 只处理Write和Edit工具
    if tool_use.get("tool") not in ["Write", "Edit", "MultiEdit"]:
        print(json.dumps({"decision": "allow"}))
        return

    file_path = tool_use.get("arguments", {}).get("file_path")
    if not file_path:
        print(json.dumps({"decision": "allow"}))
        return

    # 分析文件（如果已存在）
    stats = analyze_file(file_path)

    if stats:
        message = f"📊 文件统计: {os.path.basename(file_path)}\n"
        message += f"   行数: {stats['lines']}\n"
        message += f"   字符数: {stats['characters']}\n"
        message += f"   单词数: {stats['words']}\n"
        if stats["functions"] > 0:
            message += f"   函数数: {stats['functions']}\n"
        if stats["classes"] > 0:
            message += f"   类数: {stats['classes']}\n"

        print(json.dumps({"decision": "allow", "message": message}))
    else:
        print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
