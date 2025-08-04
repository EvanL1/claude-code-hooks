# Claude Code Hooks Collection 🪝

[English](#english) | [中文](#中文)

A comprehensive collection of useful hooks for Claude Code to enhance your development workflow. These hooks provide safety checks, automation, notifications, and improved developer experience.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/yourusername/claude-code-hooks/pulls)

## ✨ Features

- 🛡️ **Safety First**: Protect against dangerous operations
- 🤖 **Automation**: Auto-format code, check dependencies
- 📊 **Analytics**: File statistics and command logging
- 🎨 **Enhanced UI**: Beautiful terminal interface
- 🔔 **Notifications**: Integration with [claude-notifier](https://github.com/EvanL1/claude-notifier)
- 🔧 **Extensible**: Easy to add custom hooks

## 📦 Quick Start

### One-line Install

```bash
curl -sSL https://raw.githubusercontent.com/yourusername/claude-code-hooks/main/install.sh | bash
```

### Manual Install

```bash
git clone https://github.com/yourusername/claude-code-hooks.git
cd claude-code-hooks
./install.sh
```

## 🪝 Available Hooks

### 1. 🎨 Terminal UI Enhancement (`terminal-ui.sh`)
Beautiful terminal interface with time, path, and mode display.

### 2. 🐳 Docker Validator (`docker-validator.py`)
- Prevents bad image naming patterns (e.g., `-v2`, `-test`)
- Enforces proper tagging conventions

### 3. 📊 File Statistics (`file-stats.py`)
- Shows line count, character count, functions, and classes
- Triggered after file modifications

### 4. 🦀 Cargo Auto Format (`cargo-auto-format.py`)
- Reminds to run `cargo fmt` and `cargo clippy`
- Triggered on Rust builds

### 5. 🔒 Git Safety Check (`git-safety-check.py`)
- Protects main branches from deletion
- Warns about force push and hard reset
- Alerts on sensitive file commits

### 6. 📦 NPM Safety Check (`npm-safety-check.py`)
- Warns about publishing operations
- Alerts on problematic packages
- Suggests `npm ci` for CI environments

### 7. ☕ Java Build Check (`java-build-check.py`)
- Recommends using wrapper scripts
- Warns when skipping tests
- Provides JVM optimization tips

### 8. ☁️ AWS Safety Check (`aws-safety-check.py`)
- Warns about destructive operations
- Detects production environment actions
- Alerts on public S3 permissions
- Cost operation reminders

### 9. 📝 Command Logger (`command-logger.py`)
- Logs all commands to `~/.claude/logs/`
- Useful for auditing and debugging

### 10. 🚫 Commit Message Filter (`commit-message-filter.py`)
- Blocks auto-generated commit signatures
- Enforces custom commit messages

### 11. 🔔 Dev Event Notifier (`dev-event-notifier.py`)
- Sends notifications for build/test/deploy events
- Integrates with [claude-notifier](https://github.com/EvanL1/claude-notifier)

## ⚙️ Configuration

Hooks are configured in `~/.config/claude-code/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [...],
    "PreToolUse": [...],
    "PostToolUse": [...]
  }
}
```

See [examples/settings.json](examples/settings.json) for a complete configuration example.

## 🔧 Customization

### Disable Specific Hooks

Remove or comment out hooks in your `settings.json`.

### Disable All Hooks Temporarily

```bash
claude-code --no-hooks
# or
export CLAUDE_CODE_NO_HOOKS=1
```

### Create Custom Hooks

1. Create a script in `~/.claude/hooks/`
2. Make it executable: `chmod +x your-hook.py`
3. Add to `settings.json`

Hook scripts receive tool usage data via stdin and should output JSON:

```python
#!/usr/bin/env python3
import sys
import json

tool_use = json.loads(sys.stdin.read())
# Your logic here
print(json.dumps({"decision": "allow"}))
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-hook`)
3. Commit your changes (`git commit -m 'Add amazing hook'`)
4. Push to the branch (`git push origin feature/amazing-hook`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for [Claude Code](https://claude.ai/code) by the community
- Notification support via [claude-notifier](https://github.com/EvanL1/claude-notifier)

---

<a name="中文"></a>

# Claude Code Hooks 集合 🪝

一套全面的 Claude Code hooks 集合，用于增强您的开发工作流程。这些 hooks 提供安全检查、自动化、通知和改进的开发体验。

## ✨ 特性

- 🛡️ **安全第一**：防止危险操作
- 🤖 **自动化**：自动格式化代码、检查依赖
- 📊 **分析统计**：文件统计和命令日志
- 🎨 **增强界面**：美化的终端界面
- 🔔 **通知集成**：与 [claude-notifier](https://github.com/EvanL1/claude-notifier) 集成
- 🔧 **可扩展**：轻松添加自定义 hooks

## 📦 快速开始

### 一键安装

```bash
curl -sSL https://raw.githubusercontent.com/yourusername/claude-code-hooks/main/install.sh | bash
```

### 手动安装

```bash
git clone https://github.com/yourusername/claude-code-hooks.git
cd claude-code-hooks
./install.sh
```

## 🪝 可用的 Hooks

1. **终端UI美化** - 美化的终端界面显示
2. **Docker验证器** - 防止不规范的镜像命名
3. **文件统计** - 显示文件统计信息
4. **Cargo自动格式化** - Rust代码格式化提醒
5. **Git安全检查** - 保护重要分支和敏感文件
6. **NPM安全检查** - 包管理器操作警告
7. **Java构建检查** - Maven/Gradle最佳实践
8. **AWS安全检查** - 云操作安全提醒
9. **命令日志** - 记录所有执行的命令
10. **提交消息过滤** - 过滤自动生成的提交信息
11. **开发事件通知** - 构建/测试/部署通知

## ⚙️ 配置

详见 [examples/settings.json](examples/settings.json) 获取完整配置示例。

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

## 📝 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。