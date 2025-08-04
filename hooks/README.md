# Claude Code Hooks Collection

这是一套用于增强Claude Code开发体验的hooks脚本集合。

## 已安装的Hooks

### 1. 终端UI美化 (terminal-ui.sh)
- **触发时机**: 用户提交prompt时
- **功能**: 显示美化的终端界面，包含时间、路径和模式信息

### 2. Docker镜像命名验证 (docker-validator.py)
- **触发时机**: 执行docker build/tag命令前
- **功能**: 阻止使用不规范的镜像名称后缀（如-v2, -test等）
- **建议**: 使用标准tag格式，如 `myapp:1.0` 而不是 `myapp-v2`

### 3. 文件统计信息 (file-stats.py)
- **触发时机**: 文件写入/编辑后
- **功能**: 显示文件的行数、字符数、函数数等统计信息

### 4. Cargo自动格式化 (cargo-auto-format.py)
- **触发时机**: 执行cargo build/check/test命令时
- **功能**: 提醒运行cargo fmt和clippy进行代码格式化和质量检查

### 5. Git安全检查 (git-safety-check.py)
- **触发时机**: 执行git命令前
- **功能**: 
  - 阻止删除受保护分支（main, master, production等）
  - 警告危险操作（force push, hard reset等）
  - 提醒敏感文件提交（.env, .pem, credentials等）

### 6. NPM安全检查 (npm-safety-check.py)
- **触发时机**: 执行npm/yarn/pnpm命令前
- **功能**:
  - 警告发布操作
  - 提醒已知有问题的包
  - 建议CI环境使用npm ci

### 7. Java构建检查 (java-build-check.py)
- **触发时机**: 执行Maven/Gradle命令时
- **功能**:
  - 建议使用wrapper确保版本一致性
  - 警告跳过测试
  - 提供JVM参数建议

### 8. AWS安全检查 (aws-safety-check.py)
- **触发时机**: 执行AWS CLI命令前
- **功能**:
  - 警告删除/终止等危险操作
  - 检测生产环境操作
  - S3公开访问权限警告
  - IAM权限安全提醒
  - 成本相关操作提醒

### 9. 命令日志记录 (command-logger.py)
- **触发时机**: 所有工具使用前
- **功能**: 记录所有执行的命令到 `~/.claude/logs/` 目录

## 配置管理

所有hooks配置存储在 `~/.config/claude-code/settings.json` 中。

## 添加新Hook

1. 在 `/Users/lyf/.claude/hooks/` 目录创建新的脚本文件
2. 设置执行权限: `chmod +x your-hook.py`
3. 在 `settings.json` 中添加相应配置

## 禁用Hooks

如需临时禁用所有hooks：
```bash
claude-code --no-hooks
```

或设置环境变量：
```bash
export CLAUDE_CODE_NO_HOOKS=1
```