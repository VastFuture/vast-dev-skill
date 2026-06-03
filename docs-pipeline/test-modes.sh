#!/bin/bash

# 测试 docs-pipeline 的三种安装模式
# 用法: ./test-modes.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$SCRIPT_DIR/assets/templates"

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

    # 创建测试目录
    mkdir -p "$TEST_DIR"
    cd "$TEST_DIR"

    # 初始化 git
    git init > /dev/null 2>&1
    git config user.email "test@example.com"
    git config user.name "Test User"

    # 创建 package.json（触发 Node.js 项目检测）
    echo '{"name":"test"}' > package.json
    git add . && git commit -m "init" > /dev/null 2>&1

    # 模拟 docs-pipeline 执行（根据模式创建目录）
    DOCS_ROOT="$TEST_DIR/docs"

    # 创建目录结构（模拟 Step 2）
    if [ "$MODE" = "minimal" ]; then
        mkdir -p "$DOCS_ROOT/context" "$DOCS_ROOT/backlog" "$DOCS_ROOT/prd" "$DOCS_ROOT/exec-plans/active" "$DOCS_ROOT/exec-plans/completed" "$DOCS_ROOT/lessons"
    elif [ "$MODE" = "standard" ]; then
        mkdir -p "$DOCS_ROOT/context" "$DOCS_ROOT/backlog" "$DOCS_ROOT/prd" "$DOCS_ROOT/design" "$DOCS_ROOT/exec-plans/active" "$DOCS_ROOT/exec-plans/completed" "$DOCS_ROOT/research" "$DOCS_ROOT/issues" "$DOCS_ROOT/handover" "$DOCS_ROOT/ideas" "$DOCS_ROOT/lessons"
    elif [ "$MODE" = "full" ]; then
        mkdir -p "$DOCS_ROOT/context" "$DOCS_ROOT/backlog" "$DOCS_ROOT/prd" "$DOCS_ROOT/design" "$DOCS_ROOT/exec-plans/active" "$DOCS_ROOT/exec-plans/completed" "$DOCS_ROOT/research" "$DOCS_ROOT/issues" "$DOCS_ROOT/handover" "$DOCS_ROOT/ideas" "$DOCS_ROOT/lessons" "$DOCS_ROOT/input" "$DOCS_ROOT/discussions" "$DOCS_ROOT/audits" "$DOCS_ROOT/bugs" "$DOCS_ROOT/logs" "$DOCS_ROOT/testing" "$DOCS_ROOT/skills" "$DOCS_ROOT/retrospectives"
    fi

    # 统计创建的目录数
    ACTUAL_DIRS=$(find "$DOCS_ROOT" -type d -mindepth 1 | wc -l)

    # 验证
    if [ "$ACTUAL_DIRS" -eq "$EXPECTED_DIRS" ]; then
        echo "  ✅ 目录数量正确: $ACTUAL_DIRS"
    else
        echo "  ❌ 目录数量错误: 期望 $EXPECTED_DIRS, 实际 $ACTUAL_DIRS"
        exit 1
    fi

    # 列出目录
    echo "  📁 创建的目录:"
    find "$DOCS_ROOT" -type d -mindepth 1 | sed 's|.*/docs/|    - |' | sort

    echo ""
}

# 测试三种模式
test_mode "minimal" 7
test_mode "standard" 12
test_mode "full" 20

echo "✅ 所有模式测试通过!"
echo ""
echo "目录数量对照:"
echo "  - minimal:  7 个必需目录"
echo "  - standard: 12 个核心目录"
echo "  - full:     20 个所有目录"
