# Dev Workflow Hooks for Claude Code

[English](#english) | [中文](#中文)

A comprehensive collection of powerful hooks for Claude Code to enhance your development workflow.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/EvanL1/claude-code-hooks/pulls)

## Features

- Safety First: Protect against dangerous operations with 6 blocking hooks
- Automation: Auto-format code, check dependencies with 3 tool hooks
- Analytics: File statistics and command logging
- Enhanced UI: Beautiful terminal interface
- Notifications: Integration with claude-notifier
- Extensible: Easy to add custom hooks

## Quick Start

### One-line Install

curl -sSL https://raw.githubusercontent.com/EvanL1/claude-code-hooks/main/install.sh | bash

### Manual Install

git clone https://github.com/EvanL1/claude-code-hooks.git
cd dev-workflow-hooks
./install.sh

## Hook Overview - 15 Total Hooks

### Blocking Hooks (6) - Enforce safety rules
1. rust-mod-restriction - Prevent mod.rs creation
2. naming-restrictions - Enforce naming conventions  
3. python-uv-enforcer - Enforce uv for Python
4. git-safety-check - Protect main branches
5. commit-message-filter - Filter auto-generated commits
6. docker-validator - Validate Docker naming

### Warning Hooks (4) - Best practices
7. aws-safety-check - Cloud operation warnings
8. npm-safety-check - Package alerts
9. cargo-auto-format - Rust reminders
10. java-build-check - Java best practices

### Audit Hooks (3) - Logging
11. file-stats - File statistics
12. command-logger - Command audit
13. dev-event-notifier - Event notifications

### UI Enhancement (1)
14. terminal-ui - Terminal interface

### Event Support (1)
15. dev-event-notifier - Notifications

## Configuration

Hooks are configured in ~/.config/claude-code/settings.json

See settings-template.json for complete examples.

## Contributing

Contributions welcome! Submit Pull Requests.

## License

MIT License - See LICENSE file

---

# Dev Workflow Hooks for Claude Code (Chinese)

一套完整的 Claude Code hooks 集合，用于增强开发工作流程。

## 特性

- 安全第一：6个阻止型hooks强制执行安全规范
- 自动化：3个工具型hooks用于代码自动格式化
- 分析统计：文件统计和命令审计记录
- 增强界面：美化的终端界面
- 通知集成：与 claude-notifier 集成
- 可扩展：轻松添加自定义 hooks

## 快速开始

### 一键安装

curl -sSL https://raw.githubusercontent.com/EvanL1/claude-code-hooks/main/install.sh | bash

### 手动安装

git clone https://github.com/EvanL1/claude-code-hooks.git
cd dev-workflow-hooks
./install.sh

## Hook 概览 - 共15个

### 阻止型Hooks（6个）- 强制执行安全规范
1. rust-mod-restriction - 防止创建mod.rs文件
2. naming-restrictions - 强制执行命名规范
3. python-uv-enforcer - 强制使用uv工具
4. git-safety-check - 保护主分支
5. commit-message-filter - 过滤自动生成的提交消息
6. docker-validator - 验证Docker镜像命名

### 警告型Hooks（4个）- 提供最佳实践建议
7. aws-safety-check - 云操作安全提醒
8. npm-safety-check - 包管理器操作警告
9. cargo-auto-format - Rust格式化提醒
10. java-build-check - Java构建最佳实践

### 审计型Hooks（3个）- 日志记录和统计
11. file-stats - 显示文件统计信息
12. command-logger - 记录所有执行的命令
13. dev-event-notifier - 构建/测试/部署事件通知

### UI增强型（1个）
14. terminal-ui - 美化的终端界面

### 事件型Hooks（1个）
15. dev-event-notifier - 事件通知系统

## 配置

在 ~/.config/claude-code/settings.json 或 .claude/settings.json 中配置hooks

详见 settings-template.json 获取完整配置示例。

## 许可证

本项目采用 MIT 许可证

---

## Hook Technical Details

### Configuration & Customization

Hooks are configured in ~/.config/claude-code/settings.json

Example configuration:
{
  "hooks": {
    "matchers": [
      {
        "name": "rust-mod-restriction",
        "hook": "${CLAUDE_PLUGIN_ROOT}/hooks/rust-mod-restriction.py",
        "matcher": "Write|Edit|MultiEdit"
      },
      {
        "name": "naming-restrictions",
        "hook": "${CLAUDE_PLUGIN_ROOT}/hooks/naming-restrictions.py",
        "matcher": "Write|Edit|MultiEdit|Bash"
      }
    ]
  }
}

### Hook Exit Codes

- Exit Code 0: Allow operation
- Exit Code 2: Block operation

### Disable Specific Hooks

Remove or comment out hooks in settings.json

### Disable All Hooks Temporarily

export CLAUDE_CODE_NO_HOOKS=1

### Create Custom Hooks

1. Create script in ~/.claude/hooks/
2. Make executable: chmod +x your-hook.py
3. Add to settings.json

Hook scripts receive tool usage data via stdin:

#!/usr/bin/env python3
import sys
import json

tool_use = json.loads(sys.stdin.read())
# Your logic here
exit(0)  # Allow

---

## Features Summary

15 Total Hooks with:
- 6 blocking hooks for strict safety
- 4 warning hooks for best practices
- 3 audit hooks for logging
- 1 UI enhancement hook
- 1 event notification hook

Exit code 2 mechanism: Simple, reliable, and effective

---

## Contributing

Fork the repository and submit pull requests at:
https://github.com/EvanL1/claude-code-hooks

---

## License

MIT License - See LICENSE file

For more information and updates, visit:
https://github.com/EvanL1/claude-code-hooks

