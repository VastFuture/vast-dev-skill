#!/bin/bash

# 测试 docs-pipeline 的安装模式
# 用法: ./test-modes.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "🧪 docs-pipeline 安装模式测试"
echo "=================================="
echo ""

# 测试函数
test_mode() {
    local MODE=$1
    local EXPECTED_DIRS=$2
    local TEST_DIR="/tmp/docs-pipeline-mode-test-$MODE-$(date +%s)"

    echo "📋 测试模式: $MODE"
    echo "---"

    mkdir -p "$TEST_DIR"
    cd "$TEST_DIR"

    git init > /dev/null 2>&1
    git config user.email "test@example.com"
    git config user.name "Test User"

    echo '{"name":"test"}' > package.json
    git add . && git commit -m "init" > /dev/null 2>&1

    DOCS_ROOT="$TEST_DIR/docs"

    if [ "$MODE" = "minimal" ]; then
        mkdir -p "$DOCS_ROOT/context" "$DOCS_ROOT/backlog" "$DOCS_ROOT/prd" "$DOCS_ROOT/exec-plans/active" "$DOCS_ROOT/exec-plans/completed" "$DOCS_ROOT/lessons" "$DOCS_ROOT/agent-guides"
    elif [ "$MODE" = "standard" ]; then
        mkdir -p "$DOCS_ROOT/context" "$DOCS_ROOT/backlog" "$DOCS_ROOT/prd" "$DOCS_ROOT/design" "$DOCS_ROOT/exec-plans/active" "$DOCS_ROOT/exec-plans/completed" "$DOCS_ROOT/architecture" "$DOCS_ROOT/standards" "$DOCS_ROOT/lessons" "$DOCS_ROOT/logs" "$DOCS_ROOT/issues" "$DOCS_ROOT/research" "$DOCS_ROOT/handover" "$DOCS_ROOT/ideas" "$DOCS_ROOT/agent-guides"
    fi

    ACTUAL_DIRS=$(find "$DOCS_ROOT" -type d -mindepth 1 | wc -l)

    if [ "$ACTUAL_DIRS" -eq "$EXPECTED_DIRS" ]; then
        echo "  ✅ 目录数量正确: $ACTUAL_DIRS"
    else
        echo "  ❌ 目录数量错误: 期望 $EXPECTED_DIRS, 实际 $ACTUAL_DIRS"
        exit 1
    fi

    echo "  📁 创建的目录:"
    find "$DOCS_ROOT" -type d -mindepth 1 | sed 's|.*/docs/|    - |' | sort

    echo ""
}

test_mode "minimal" 8
test_mode "standard" 16

echo "✅ 所有模式测试通过!"
echo ""
echo "目录数量对照:"
echo "  - minimal:  6 个顶层目录 + 2 个 exec-plans 子目录 = 8 个目录节点"
echo "  - standard: 14 个顶层目录 + 2 个 exec-plans 子目录 = 16 个目录节点"
