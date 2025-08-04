#!/bin/bash
# Claude Code Hooks Installer

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Paths
HOOKS_SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/hooks"
HOOKS_DEST_DIR="$HOME/.claude/hooks"
CONFIG_DIR="$HOME/.config/claude-code"
CONFIG_FILE="$CONFIG_DIR/settings.json"
EXAMPLE_CONFIG="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/examples/settings.json"

echo -e "${BLUE}🪝 Claude Code Hooks Installer${NC}"
echo ""

# Check if running from cloned repo
if [ ! -d "$HOOKS_SOURCE_DIR" ]; then
    echo -e "${RED}Error: hooks directory not found!${NC}"
    echo "Please run this script from the claude-code-hooks directory."
    exit 1
fi

# Create directories
echo -e "${YELLOW}Creating directories...${NC}"
mkdir -p "$HOOKS_DEST_DIR"
mkdir -p "$CONFIG_DIR"
mkdir -p "$HOME/.claude/logs"

# Backup existing hooks
if [ -d "$HOOKS_DEST_DIR" ] && [ "$(ls -A $HOOKS_DEST_DIR 2>/dev/null)" ]; then
    BACKUP_DIR="$HOOKS_DEST_DIR.backup.$(date +%Y%m%d_%H%M%S)"
    echo -e "${YELLOW}Backing up existing hooks to $BACKUP_DIR${NC}"
    cp -r "$HOOKS_DEST_DIR" "$BACKUP_DIR"
fi

# Copy hooks
echo -e "${YELLOW}Installing hooks...${NC}"
cp -r "$HOOKS_SOURCE_DIR"/* "$HOOKS_DEST_DIR/"
chmod +x "$HOOKS_DEST_DIR"/*.py
chmod +x "$HOOKS_DEST_DIR"/*.sh

# Count installed hooks
HOOK_COUNT=$(ls -1 "$HOOKS_DEST_DIR"/*.{py,sh} 2>/dev/null | wc -l)
echo -e "${GREEN}✓ Installed $HOOK_COUNT hooks${NC}"

# Handle configuration
if [ -f "$CONFIG_FILE" ]; then
    echo -e "${YELLOW}Existing configuration found at $CONFIG_FILE${NC}"
    echo -e "${YELLOW}Creating example configuration at $CONFIG_FILE.example${NC}"
    cp "$EXAMPLE_CONFIG" "$CONFIG_FILE.example"
    echo ""
    echo -e "${BLUE}To use the full hooks configuration, you can:${NC}"
    echo "1. Manually merge settings from $CONFIG_FILE.example"
    echo "2. Or backup your current config and use: cp $CONFIG_FILE.example $CONFIG_FILE"
else
    echo -e "${YELLOW}Creating configuration...${NC}"
    cp "$EXAMPLE_CONFIG" "$CONFIG_FILE"
    echo -e "${GREEN}✓ Configuration created at $CONFIG_FILE${NC}"
fi

# Create logs directory
echo -e "${YELLOW}Setting up logs directory...${NC}"
touch "$HOME/.claude/logs/.gitkeep"
echo -e "${GREEN}✓ Logs will be saved to ~/.claude/logs/${NC}"

echo ""
echo -e "${GREEN}🎉 Installation complete!${NC}"
echo ""
echo -e "${BLUE}Installed hooks:${NC}"
echo "  • Terminal UI Enhancement"
echo "  • Docker Validator"
echo "  • File Statistics"
echo "  • Cargo Auto Format"
echo "  • Git Safety Check"
echo "  • NPM Safety Check"
echo "  • Java Build Check"
echo "  • AWS Safety Check"
echo "  • Command Logger"
echo "  • Commit Message Filter"
echo "  • Dev Event Notifier"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Review/edit configuration: $CONFIG_FILE"
echo "2. Test hooks: claude-code"
echo "3. Disable hooks temporarily: export CLAUDE_CODE_NO_HOOKS=1"
echo ""
echo -e "${GREEN}Happy coding with Claude Code! 🚀${NC}"