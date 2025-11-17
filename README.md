# Dev Workflow Hooks for Claude Code

[English](#english) | [中文](#中文)

<a name="english"></a>

## English Version

### Overview

A comprehensive collection of 15 Git hooks designed to enforce development standards, best practices, and security protocols in Claude Code projects. These hooks provide automated validation, auditing, and terminal beautification to ensure code quality and consistency across your development workflow.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/EvanL1/claude-code-hooks)
[![GitHub](https://img.shields.io/badge/GitHub-EvanL1-blue.svg)](https://github.com/EvanL1/claude-code-hooks)

### Features

The hook collection consists of 15 specialized validation and audit hooks:

- **6 Blocking Hooks** - Enforce critical safety and naming standards
- **4 Warning Hooks** - Recommend best practices with alerts
- **3 Audit Hooks** - Log operations and provide statistics
- **1 UI Hook** - Beautify terminal output
- **Exit Code 2** - Fail gracefully with meaningful status codes

### Quick Start

#### One-Line Installation

```bash
curl -sSL https://raw.githubusercontent.com/EvanL1/claude-code-hooks/master/install.sh | bash
```

#### Manual Installation

```bash
git clone https://github.com/EvanL1/claude-code-hooks.git
cd claude-code-hooks
./install.sh
```

### Hooks Reference

#### Blocking Hooks (6)

##### 1. rust-mod-restriction

**Purpose:** Enforce Rust module organization standards

**Behavior:**
- Blocks creation and editing of `mod.rs` files
- Prevents non-standard Rust module structure
- Enforces modern Rust best practices

**Example:**
```bash
# This will be blocked:
touch src/utils/mod.rs

# Suggested approach:
# Use lib.rs or main.rs with pub mod declarations
```

---

##### 2. naming-restrictions

**Purpose:** Ensure descriptive and meaningful file names

**Behavior:**
- Blocks generic names: `test.py`, `temp1.txt`, `foo.py`, `v1.py`, etc.
- Requires context-specific naming conventions
- Fails fast with clear error messages

**Example:**
```bash
# Blocked names:
test.py, temp.txt, data.json, v2.py, foo.js

# Suggested names:
test_user_authentication.py, draft_proposal_2024.txt, user_data.json, payment_service_v2.py, api_router.js
```

---

##### 3. python-uv-enforcer

**Purpose:** Standardize Python package management with `uv`

**Behavior:**
- Blocks direct usage of `pip`, `python`, `pytest`
- Enforces `uv` as the standard Python tool
- Ensures consistent environment management

**Example:**
```bash
# Blocked:
pip install requests
python script.py
pytest tests/

# Use instead:
uv pip install requests
uv run python script.py
uv run pytest tests/
```

---

##### 4. git-safety-check

**Purpose:** Protect critical branches from accidental deletion or forced updates

**Behavior:**
- Prevents branch deletion on: `main`, `master`, `production`, `prod`
- Protects from dangerous git operations
- Maintains branch integrity

**Protected Branches:**
- `main`
- `master`
- `production`
- `prod`

---

##### 5. commit-message-filter

**Purpose:** Ensure meaningful, custom commit messages

**Behavior:**
- Blocks auto-generated commit messages
- Enforces intentional commit messaging
- Prevents pollution of commit history

**Filtered Messages:**
- Messages containing "Generated with Claude Code"
- Auto-generated messages without customization

---

##### 6. docker-validator

**Purpose:** Enforce Docker image naming standards

**Behavior:**
- Blocks invalid Docker image name patterns
- Prevents outdated versioning practices
- Enforces semantic versioning with tags

**Blocked Patterns:**
```
Images with -v2, -v3, -test, -dev, -prod suffixes
Examples: myapp-v2, backend-test, frontend-prod
```

**Recommended Approach:**
```
# Use tags for versioning:
myapp:1.0
myapp:latest
backend-service:prod
frontend:dev
api-gateway:stable
```

---

#### Warning Hooks (4)

##### 7. aws-safety-check

**Purpose:** Alert on potentially dangerous AWS operations

**Behavior:**
- Warns before destructive AWS operations
- Recommends review of command parameters
- Provides safety confirmations

---

##### 8. npm-safety-check

**Purpose:** Prevent common NPM/Yarn mistakes

**Behavior:**
- Warns about npm install without lock files
- Suggests best practices for dependency management
- Alerts on deprecated packages

---

##### 9. cargo-auto-format

**Purpose:** Encourage Rust code formatting standards

**Behavior:**
- Reminds to run `cargo fmt`
- Enforces consistent code style
- Suggests `cargo clippy` for linting

---

##### 10. java-build-check

**Purpose:** Promote Java build best practices

**Behavior:**
- Warns about missing tests before build
- Suggests Maven/Gradle best practices
- Alerts on common configuration issues

---

#### Audit Hooks (3)

##### 11. file-stats

**Purpose:** Collect and report file operation statistics

**Behavior:**
- Logs all file operations
- Provides statistics on modifications
- Generates audit reports

---

##### 12. command-logger

**Purpose:** Maintain comprehensive command audit trail

**Behavior:**
- Records all executed commands
- Logs command parameters and results
- Creates searchable audit logs

---

##### 13. dev-event-notifier

**Purpose:** Send notifications for important development events

**Behavior:**
- Alerts on critical operations
- Notifies of hook violations
- Provides event statistics

---

#### UI Hook (1)

##### 14. terminal-ui

**Purpose:** Enhance terminal output with visual formatting

**Behavior:**
- Beautifies error and warning messages
- Adds color coding for different message types
- Improves readability of console output

---

### Configuration

The hooks are configured via the `.claude/claude.hook` configuration file:

```json
{
  "hooks": {
    "matchers": [
      {
        "name": "rust-mod-restriction",
        "hook": "./hooks/rust-mod-restriction.py",
        "matcher": "Write|Edit|MultiEdit"
      },
      {
        "name": "naming-restrictions",
        "hook": "./hooks/naming-restrictions.py",
        "matcher": "Write|Edit"
      },
      {
        "name": "python-uv-enforcer",
        "hook": "./hooks/python-uv-enforcer.py",
        "matcher": "Bash"
      },
      {
        "name": "git-safety-check",
        "hook": "./hooks/git-safety-check.py",
        "matcher": "Bash"
      },
      {
        "name": "commit-message-filter",
        "hook": "./hooks/commit-message-filter.py",
        "matcher": "Bash"
      },
      {
        "name": "docker-validator",
        "hook": "./hooks/docker-validator.py",
        "matcher": "Bash|Write|Edit"
      }
    ]
  }
}
```

### Customization

#### Modify Protected Branches

Edit the `git-safety-check.py` hook to add or remove protected branches:

```python
PROTECTED_BRANCHES = ['main', 'master', 'production', 'prod', 'develop']
```

#### Adjust Naming Rules

Customize blocked names in `naming-restrictions.py`:

```python
BLOCKED_PATTERNS = ['test', 'temp', 'foo', 'v[0-9]+', 'untitled']
```

#### Disable Specific Hooks

Comment out hooks in `.claude/claude.hook` to disable them:

```json
{
  "matchers": [
    {
      "name": "rust-mod-restriction",
      "hook": "./hooks/rust-mod-restriction.py",
      "matcher": "Write|Edit|MultiEdit",
      "enabled": false
    }
  ]
}
```

#### Customize Docker Rules

Modify patterns in `docker-validator.py`:

```python
BLOCKED_SUFFIXES = ['-v2', '-v3', '-test', '-dev', '-prod']
```

### Examples

#### Example: Running Python with uv

```bash
# Before (would be blocked):
pip install requests
python main.py

# After:
uv pip install requests
uv run python main.py
```

#### Example: Creating Docker Images

```bash
# Before (would be blocked):
docker build -t myimage with suffix patterns .

# After:
docker build -t myimage:2.0 .
docker tag myimage:2.0 myimage:latest
```

#### Example: Naming Files Correctly

```bash
# Before (would be blocked):
touch test.py
touch temp1.txt

# After:
touch test_user_auth.py
touch temp_migration_proposal.txt
```

### Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-hook`)
3. Commit your changes
4. Push to your branch
5. Submit a Pull Request

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Support

For issues, questions, or suggestions:
- Open an issue on [GitHub](https://github.com/EvanL1/claude-code-hooks/issues)
- Check existing documentation and examples
- Review hook source code for detailed behavior

---

<a name="中文"></a>

## 中文版本

### 项目概述

一套包含 15 个 Git 钩子的综合解决方案，旨在为 Claude Code 项目强制执行开发规范、最佳实践和安全协议。这些钩子提供自动化验证、审计和终端美化功能，确保代码质量和开发工作流的一致性。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/EvanL1/claude-code-hooks)
[![GitHub](https://img.shields.io/badge/GitHub-EvanL1-blue.svg)](https://github.com/EvanL1/claude-code-hooks)

### 特性

钩子集合包括 15 个专门的验证和审计钩子：

- **6 个阻止钩子** - 强制执行关键的安全和命名标准
- **4 个警告钩子** - 提示最佳实践的建议
- **3 个审计钩子** - 记录操作和提供统计信息
- **1 个 UI 钩子** - 美化终端输出
- **退出代码 2** - 以有意义的状态代码优雅地失败

### 快速开始

#### 一行命令安装

```bash
curl -sSL https://raw.githubusercontent.com/EvanL1/claude-code-hooks/master/install.sh | bash
```

#### 手动安装

```bash
git clone https://github.com/EvanL1/claude-code-hooks.git
cd claude-code-hooks
./install.sh
```

### 钩子参考

#### 阻止钩子（6 个）

##### 1. rust-mod-restriction

**用途：** 强制执行 Rust 模块组织标准

**行为：**
- 阻止创建和编辑 `mod.rs` 文件
- 防止非标准的 Rust 模块结构
- 强制采用现代 Rust 最佳实践

**示例：**
```bash
# 这将被阻止：
touch src/utils/mod.rs

# 建议做法：
# 在 lib.rs 或 main.rs 中使用 pub mod 声明
```

---

##### 2. naming-restrictions

**用途：** 确保文件名具有描述性和意义

**行为：**
- 阻止通用名称：`test.py`、`temp1.txt`、`foo.py`、`v1.py` 等
- 要求符合上下文的命名约定
- 快速失败并显示清晰的错误消息

**示例：**
```bash
# 被阻止的名称：
test.py, temp.txt, data.json, v2.py, foo.js

# 建议的名称：
test_user_authentication.py, draft_proposal_2024.txt, user_data.json, payment_service_v2.py, api_router.js
```

---

##### 3. python-uv-enforcer

**用途：** 使用 `uv` 标准化 Python 包管理

**行为：**
- 阻止直接使用 `pip`、`python`、`pytest`
- 强制使用 `uv` 作为标准 Python 工具
- 确保一致的环境管理

**示例：**
```bash
# 被阻止：
pip install requests
python script.py
pytest tests/

# 改用：
uv pip install requests
uv run python script.py
uv run pytest tests/
```

---

##### 4. git-safety-check

**用途：** 保护关键分支免遭意外删除或强制更新

**行为：**
- 防止删除分支：`main`、`master`、`production`、`prod`
- 保护免受危险的 git 操作
- 维护分支完整性

**受保护的分支：**
- `main`
- `master`
- `production`
- `prod`

---

##### 5. commit-message-filter

**用途：** 确保有意义的自定义提交消息

**行为：**
- 阻止自动生成的提交消息
- 强制有意图的提交消息
- 防止污染提交历史

**被过滤的消息：**
- 包含 "Generated with Claude Code" 的消息
- 没有自定义的自动生成消息

---

##### 6. docker-validator

**用途：** 强制执行 Docker 镜像命名标准

**行为：**
- 阻止无效的 Docker 镜像名称模式
- 防止过时的版本管理做法
- 强制使用带标签的语义版本控制

**被阻止的模式：**
```
带有-v2、-v3、-test、-dev、-prod后缀的镜像
示例：myapp-v2、backend-test、frontend-prod
```

**推荐做法：**
```
# 使用标签进行版本控制：
myapp:1.0
myapp:latest
backend-service:prod
frontend:dev
api-gateway:stable
```

---

#### 警告钩子（4 个）

##### 7. aws-safety-check

**用途：** 对可能危险的 AWS 操作发出警告

**行为：**
- 在破坏性 AWS 操作前发出警告
- 建议检查命令参数
- 提供安全确认

---

##### 8. npm-safety-check

**用途：** 防止常见的 NPM/Yarn 错误

**行为：**
- 警告没有锁定文件的 npm 安装
- 建议依赖项管理最佳实践
- 警告已弃用的包

---

##### 9. cargo-auto-format

**用途：** 推荐 Rust 代码格式化标准

**行为：**
- 提醒运行 `cargo fmt`
- 强制一致的代码风格
- 建议使用 `cargo clippy` 进行代码检查

---

##### 10. java-build-check

**用途：** 推荐 Java 构建最佳实践

**行为：**
- 警告构建前缺少测试
- 建议 Maven/Gradle 最佳实践
- 警告常见的配置问题

---

#### 审计钩子（3 个）

##### 11. file-stats

**用途：** 收集和报告文件操作统计

**行为：**
- 记录所有文件操作
- 提供修改统计
- 生成审计报告

---

##### 12. command-logger

**用途：** 维护完整的命令审计跟踪

**行为：**
- 记录所有执行的命令
- 记录命令参数和结果
- 创建可搜索的审计日志

---

##### 13. dev-event-notifier

**用途：** 发送重要开发事件的通知

**行为：**
- 关键操作的警报
- 钩子违规通知
- 事件统计

---

#### UI 钩子（1 个）

##### 14. terminal-ui

**用途：** 使用视觉格式增强终端输出

**行为：**
- 美化错误和警告消息
- 为不同消息类型添加颜色编码
- 改进控制台输出的可读性

---

### 配置

钩子通过 `.claude/claude.hook` 配置文件进行配置：

```json
{
  "hooks": {
    "matchers": [
      {
        "name": "rust-mod-restriction",
        "hook": "./hooks/rust-mod-restriction.py",
        "matcher": "Write|Edit|MultiEdit"
      },
      {
        "name": "naming-restrictions",
        "hook": "./hooks/naming-restrictions.py",
        "matcher": "Write|Edit"
      },
      {
        "name": "python-uv-enforcer",
        "hook": "./hooks/python-uv-enforcer.py",
        "matcher": "Bash"
      },
      {
        "name": "git-safety-check",
        "hook": "./hooks/git-safety-check.py",
        "matcher": "Bash"
      },
      {
        "name": "commit-message-filter",
        "hook": "./hooks/commit-message-filter.py",
        "matcher": "Bash"
      },
      {
        "name": "docker-validator",
        "hook": "./hooks/docker-validator.py",
        "matcher": "Bash|Write|Edit"
      }
    ]
  }
}
```

### 自定义

#### 修改受保护的分支

编辑 `git-safety-check.py` 钩子以添加或删除受保护的分支：

```python
PROTECTED_BRANCHES = ['main', 'master', 'production', 'prod', 'develop']
```

#### 调整命名规则

自定义 `naming-restrictions.py` 中的被阻止名称：

```python
BLOCKED_PATTERNS = ['test', 'temp', 'foo', 'v[0-9]+', 'untitled']
```

#### 禁用特定钩子

在 `.claude/claude.hook` 中注释钩子以禁用它们：

```json
{
  "matchers": [
    {
      "name": "rust-mod-restriction",
      "hook": "./hooks/rust-mod-restriction.py",
      "matcher": "Write|Edit|MultiEdit",
      "enabled": false
    }
  ]
}
```

#### 自定义 Docker 规则

修改 `docker-validator.py` 中的模式：

```python
BLOCKED_SUFFIXES = ['-v2', '-v3', '-test', '-dev', '-prod']
```

### 示例

#### 示例：使用 uv 运行 Python

```bash
# 之前（会被阻止）：
pip install requests
python main.py

# 之后：
uv pip install requests
uv run python main.py
```

#### 示例：创建 Docker 镜像

```bash
# 之前（会被阻止）：
docker build -t myimage with problematic suffixes .

# 之后：
docker build -t myimage:2.0 .
docker tag myimage:2.0 myimage:latest
```

#### 示例：正确命名文件

```bash
# 之前（会被阻止）：
touch test.py
touch temp1.txt

# 之后：
touch test_user_auth.py
touch temp_migration_proposal.txt
```

### 贡献

欢迎贡献！请遵循以下准则：

1. Fork 仓库
2. 创建功能分支（`git checkout -b feature/amazing-hook`）
3. 提交更改
4. 推送到您的分支
5. 提交拉取请求

### 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

### 支持

如有问题、疑问或建议：
- 在 [GitHub](https://github.com/EvanL1/claude-code-hooks/issues) 上提出问题
- 查看现有文档和示例
- 查看钩子源代码了解详细行为
