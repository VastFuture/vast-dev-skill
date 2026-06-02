#!/bin/bash

# docs-pipeline 实际运行测试脚本
# 用法: ./test-pipeline.sh

set -e

TEST_DIR="/tmp/docs-pipeline-test-$(date +%s)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$SCRIPT_DIR/assets/templates"

echo "🧪 docs-pipeline 实际运行测试"
echo "=================================="
echo "测试目录: $TEST_DIR"
echo "模板目录: $TEMPLATES_DIR"
echo ""

# 1. 创建测试目录
echo "📁 Step 1: 创建测试目录..."
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# 2. 初始化 git 仓库
echo "📦 Step 2: 初始化 git 仓库..."
git init
git config user.email "test@example.com"
git config user.name "Test User"

# 3. 创建模拟项目结构
echo "📂 Step 3: 创建模拟项目结构..."
mkdir -p src/{auth,api,utils}
mkdir -p tests

cat > package.json << 'EOF'
{
  "name": "test-project",
  "version": "1.0.0",
  "scripts": {
    "test": "jest",
    "lint": "eslint src/",
    "build": "tsc"
  }
}
EOF

cat > src/index.ts << 'EOF'
export function main() {
  console.log("Hello World");
}
EOF

cat > src/auth/login.ts << 'EOF'
export function login(username: string, password: string) {
  // TODO: implement
  return { success: true };
}
EOF

cat > README.md << 'EOF'
# Test Project

A sample project for testing docs-pipeline.
EOF

git add .
git commit -m "initial commit"

# 4. 模拟 docs-pipeline 初始化（使用真实模板）
echo ""
echo "🚀 Step 4: 模拟 docs-pipeline 初始化..."
echo ""

# 创建 docs 目录结构
DOCS_ROOT="$TEST_DIR/docs"
mkdir -p "$DOCS_ROOT/context"
mkdir -p "$DOCS_ROOT/backlog"
mkdir -p "$DOCS_ROOT/prd"
mkdir -p "$DOCS_ROOT/design"
mkdir -p "$DOCS_ROOT/exec-plans/active"
mkdir -p "$DOCS_ROOT/exec-plans/completed"
mkdir -p "$DOCS_ROOT/ideas"
mkdir -p "$DOCS_ROOT/research"
mkdir -p "$DOCS_ROOT/handover"
mkdir -p "$DOCS_ROOT/issues"
mkdir -p "$DOCS_ROOT/lessons"

echo "✅ 目录结构创建完成"

# 5. 复制真实模板文件
echo ""
echo "📝 Step 5: 复制真实模板文件..."

# 复制 context 模板
cp "$TEMPLATES_DIR/context/project-context.md" "$DOCS_ROOT/context/"
cp "$TEMPLATES_DIR/context/ai-autonomy-policy.md" "$DOCS_ROOT/context/"
cp "$TEMPLATES_DIR/context/codebase-map.md" "$DOCS_ROOT/context/"
cp "$TEMPLATES_DIR/context/source-of-truth-and-precedence.md" "$DOCS_ROOT/context/"

# 复制 docs 根目录模板
cp "$TEMPLATES_DIR/docs-CLAUDE.md" "$DOCS_ROOT/CLAUDE.md"
cp "$TEMPLATES_DIR/docs-index.md" "$DOCS_ROOT/index.md"

# 复制 README 模板
cp "$TEMPLATES_DIR/docs-backlog/README.md" "$DOCS_ROOT/backlog/"
cp "$TEMPLATES_DIR/prd-README.md" "$DOCS_ROOT/prd/"
cp "$TEMPLATES_DIR/docs-design/README.md" "$DOCS_ROOT/design/"
cp "$TEMPLATES_DIR/exec-plans-README.md" "$DOCS_ROOT/exec-plans/"
cp "$TEMPLATES_DIR/ideas-README.md" "$DOCS_ROOT/ideas/"
cp "$TEMPLATES_DIR/research-README.md" "$DOCS_ROOT/research/"
cp "$TEMPLATES_DIR/handover-README.md" "$DOCS_ROOT/handover/"
cp "$TEMPLATES_DIR/issues-README.md" "$DOCS_ROOT/issues/"
cp "$TEMPLATES_DIR/lessons-README.md" "$DOCS_ROOT/lessons/"

# 复制模板文件
cp "$TEMPLATES_DIR/prd-TEMPLATE.md" "$DOCS_ROOT/prd/TEMPLATE.md"
cp "$TEMPLATES_DIR/exec-plans-TEMPLATE.md" "$DOCS_ROOT/exec-plans/TEMPLATE.md"
cp "$TEMPLATES_DIR/handover-TEMPLATE.md" "$DOCS_ROOT/handover/TEMPLATE.md"
cp "$TEMPLATES_DIR/issues-TEMPLATE.md" "$DOCS_ROOT/issues/TEMPLATE.md"

echo "✅ 模板文件复制完成"

# 6. 创建根级 AI 代理模板（使用真实模板）
echo ""
echo "🤖 Step 6: 创建根级 AI 代理模板..."

# 复制根级模板
cp "$TEMPLATES_DIR/CLAUDE.md" "$TEST_DIR/"
cp "$TEMPLATES_DIR/AGENTS.md" "$TEST_DIR/"
cp "$TEMPLATES_DIR/MBTI_DEV_TRAPS.md" "$TEST_DIR/"
cp "$TEMPLATES_DIR/karpathy-guidelines.md" "$TEST_DIR/"
cp "$TEMPLATES_DIR/output-modes.md" "$TEST_DIR/"
cp "$TEMPLATES_DIR/engineering-rules.md" "$TEST_DIR/"
cp "$TEMPLATES_DIR/plan-mode.md" "$TEST_DIR/"
cp "$TEMPLATES_DIR/requirement-confirmation.md" "$TEST_DIR/"
cp "$TEMPLATES_DIR/content-organization.md" "$TEST_DIR/"
cp "$TEMPLATES_DIR/mcp.json" "$TEST_DIR/.mcp.json"

# 创建 .claude/commands/ideas.md
mkdir -p "$TEST_DIR/.claude/commands"
cp "$TEMPLATES_DIR/commands/ideas.md" "$TEST_DIR/.claude/commands/"

echo "✅ 根级 AI 代理模板创建完成"

# 7. 验证文件完整性
echo ""
echo "🔍 Step 7: 验证文件完整性..."
echo ""

echo "根目录文件:"
ls -la "$TEST_DIR" | grep -E "\.(md|json)$"

echo ""
echo "docs/ 目录文件:"
find "$DOCS_ROOT" -name "*.md" | sort

echo ""
echo "context/ 目录文件:"
ls -la "$DOCS_ROOT/context/"

# 8. 验证文件内容质量
echo ""
echo "📊 Step 8: 验证文件内容质量..."
echo ""

echo "关键文件行数统计:"
echo "- CLAUDE.md (根): $(wc -l < "$TEST_DIR/CLAUDE.md") 行"
echo "- AGENTS.md (根): $(wc -l < "$TEST_DIR/AGENTS.md") 行"
echo "- docs/CLAUDE.md: $(wc -l < "$DOCS_ROOT/CLAUDE.md") 行"
echo "- docs/index.md: $(wc -l < "$DOCS_ROOT/index.md") 行"
echo "- context/project-context.md: $(wc -l < "$DOCS_ROOT/context/project-context.md") 行"
echo "- context/ai-autonomy-policy.md: $(wc -l < "$DOCS_ROOT/context/ai-autonomy-policy.md") 行"
echo "- context/codebase-map.md: $(wc -l < "$DOCS_ROOT/context/codebase-map.md") 行"

echo ""
echo "检查关键内容:"
echo "- docs/index.md 包含任务路由表: $(grep -q "任务路由" "$DOCS_ROOT/index.md" && echo "✅" || echo "❌")"
echo "- ai-autonomy-policy.md 包含判定规则: $(grep -q "判定规则" "$DOCS_ROOT/context/ai-autonomy-policy.md" && echo "✅" || echo "❌")"
echo "- project-context.md 包含验证命令说明: $(grep -q "验证命令前置条件" "$DOCS_ROOT/context/project-context.md" && echo "✅" || echo "❌")"
echo "- codebase-map.md 包含模块状态: $(grep -q "模块状态" "$DOCS_ROOT/context/codebase-map.md" && echo "✅" || echo "❌")"

echo ""
echo "检查模板文件:"
echo "- prd/TEMPLATE.md: $(test -f "$DOCS_ROOT/prd/TEMPLATE.md" && echo "✅" || echo "❌")"
echo "- exec-plans/TEMPLATE.md: $(test -f "$DOCS_ROOT/exec-plans/TEMPLATE.md" && echo "✅" || echo "❌")"
echo "- handover/TEMPLATE.md: $(test -f "$DOCS_ROOT/handover/TEMPLATE.md" && echo "✅" || echo "❌")"
echo "- issues/TEMPLATE.md: $(test -f "$DOCS_ROOT/issues/TEMPLATE.md" && echo "✅" || echo "❌")"

# 9. 模拟 Claude Code 使用场景
echo ""
echo "🎯 Step 9: 模拟 Claude Code 使用场景..."
echo ""

echo "场景 1: 读取项目上下文"
if [ -f "$DOCS_ROOT/context/project-context.md" ]; then
  echo "  ✅ 可以读取 project-context.md"
  echo "  📝 内容预览: $(head -5 "$DOCS_ROOT/context/project-context.md" | tail -1)"
else
  echo "  ❌ 无法读取 project-context.md"
fi

echo ""
echo "场景 2: 查找任务路由"
if grep -q "任务路由" "$DOCS_ROOT/index.md"; then
  echo "  ✅ 可以找到任务路由表"
  echo "  📝 路由表示例:"
  grep -A 3 "任务类型" "$DOCS_ROOT/index.md" | head -4
else
  echo "  ❌ 无法找到任务路由表"
fi

echo ""
echo "场景 3: 查找自主级别判定规则"
if grep -q "判定规则" "$DOCS_ROOT/context/ai-autonomy-policy.md"; then
  echo "  ✅ 可以找到自主级别判定规则"
else
  echo "  ❌ 无法找到自主级别判定规则"
fi

echo ""
echo "场景 4: 使用模板文件"
if [ -f "$DOCS_ROOT/prd/TEMPLATE.md" ]; then
  echo "  ✅ 可以使用 PRD 模板"
  echo "  📝 模板预览: $(head -3 "$DOCS_ROOT/prd/TEMPLATE.md" | tail -1)"
else
  echo "  ❌ 无法使用 PRD 模板"
fi

# 10. 总结
echo ""
echo "📊 测试总结"
echo "=================================="
echo ""

TOTAL_FILES=$(find "$TEST_DIR" -name "*.md" | wc -l)
DOCS_FILES=$(find "$DOCS_ROOT" -name "*.md" | wc -l)
ROOT_FILES=$(find "$TEST_DIR" -maxdepth 1 -name "*.md" | wc -l)

echo "总文件数: $TOTAL_FILES"
echo "- docs/ 目录: $DOCS_FILES 个 .md 文件"
echo "- 根目录: $ROOT_FILES 个 .md 文件"

echo ""
echo "目录结构:"
tree "$DOCS_ROOT" 2>/dev/null || find "$DOCS_ROOT" -type d | sort | sed 's|[^/]*/|  |g'

echo ""
echo "✅ 测试完成!"
echo ""
echo "📁 测试目录: $TEST_DIR"
echo ""
echo "下一步:"
echo "1. 查看生成的文件: ls -la $TEST_DIR"
echo "2. 检查 docs/ 内容: cat $DOCS_ROOT/index.md"
echo "3. 测试 Claude Code 集成: cd $TEST_DIR && claude"
