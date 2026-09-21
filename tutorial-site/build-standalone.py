import json

with open("tutorial-site/assets/skills-data.json", "r", encoding="utf-8") as f:
    skills_json = f.read()

with open("tutorial-site/assets/style.css", "r", encoding="utf-8") as f:
    css = f.read()

with open("tutorial-site/assets/app.js", "r", encoding="utf-8") as f:
    js = f.read()

html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Vast Dev Skills 教学实战平台</title>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <style>
{css}
  </style>
</head>
<body>

  <!-- Navigation Bar -->
  <header class="site-header">
    <div class="header-container">
      <a href="#" class="brand-link">
        <div class="brand-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="16 18 22 12 16 6"></polyline>
            <polyline points="8 6 2 12 8 18"></polyline>
          </svg>
        </div>
        <div class="brand-meta">
          <h1>Vast Dev Skills</h1>
          <span>工程架构与技能实战教程</span>
        </div>
      </a>

      <!-- Search Field -->
      <div class="search-wrapper">
        <span class="search-icon">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </span>
        <input type="text" id="search-input" class="search-input" placeholder="搜索技能、应用场景或指令...">
      </div>

      <!-- Stats -->
      <div>
        <span class="counter-pill">收录技能: <strong id="total-counter">0</strong></span>
      </div>
    </div>
  </header>

  <!-- Main Layout -->
  <div class="main-layout">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-title">分类索引</div>
      <ul id="sidebar-menu" class="sidebar-menu">
        <!-- populated by JS -->
      </ul>
    </aside>

    <!-- Content Area -->
    <main class="content-area">
      <div class="section-header">
        <h2 id="current-section-title" class="section-title">全部技能指南</h2>
      </div>

      <div id="cards-grid" class="cards-grid">
        <!-- populated by JS -->
      </div>
    </main>
  </div>

  <!-- Detail Modal -->
  <div id="detail-modal" class="modal-overlay">
    <div class="modal-window">
      <div class="modal-header">
        <div class="modal-title-box">
          <h2 id="modal-skill-title">技能教学详情</h2>
          <div id="modal-skill-path" class="modal-path"></div>
        </div>
        <button id="modal-close-btn" class="close-button" title="关闭">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <div class="modal-scroll">
        <!-- Action Callout -->
        <div class="action-box">
          <div class="action-label">调用指令模板</div>
          <div class="prompt-bar">
            <span id="prompt-text-display" class="prompt-text"></span>
            <button id="copy-prompt-btn" class="copy-button" onclick="copyPromptCommand()">拷贝指令</button>
          </div>
        </div>

        <!-- Mermaid Flowchart with Interactive Pan, Zoom & Fullscreen -->
        <div id="diagram-section" class="diagram-section">
          <div class="diagram-header">
            <div class="diagram-title">工作流执行拓扑</div>
            <!-- Apple Style Zoom & Fullscreen Control Capsule -->
            <div style="display: flex; align-items: center;">
              <div class="diagram-controls">
                <button class="diagram-ctrl-btn" onclick="zoomOut()" title="缩小">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                </button>
                <span id="zoom-indicator" class="zoom-indicator">100%</span>
                <button class="diagram-ctrl-btn" onclick="zoomIn()" title="放大">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                </button>
                <button class="diagram-ctrl-btn" onclick="resetZoom()" title="重置视图">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path><polyline points="3 3 3 8 8 8"></polyline></svg>
                </button>
                <button class="diagram-ctrl-btn" onclick="toggleFullscreen()" title="全屏查看">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 3 21 3 21 9"></polyline><polyline points="9 21 3 21 3 15"></polyline><line x1="21" y1="3" x2="14" y2="10"></line><line x1="3" y1="21" x2="10" y2="14"></line></svg>
                </button>
              </div>
              <button class="fullscreen-close-btn" onclick="toggleFullscreen()" title="退出全屏">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
              </button>
            </div>
          </div>
          
          <div id="diagram-viewport" class="diagram-viewport">
            <div id="diagram-canvas" class="diagram-canvas"></div>
            <div class="pan-hint">可鼠标拖拽平移 / 滚轮缩放 / 双击重置</div>
          </div>
        </div>

        <!-- Markdown Tutorial Documentation -->
        <div id="tutorial-markdown" class="tutorial-body"></div>
      </div>
    </div>
  </div>

  <footer class="site-footer">
    <p>Vast Dev Skills 教学实战平台 &bull; 遵循 Human Interface Guidelines 规范 &bull; 零冗余工程架构</p>
  </footer>

  <script>
  window.__SKILLS_DATA__ = {skills_json};
  {js}
  </script>
</body>
</html>
"""

with open("tutorial-site/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Updated index.html with fullscreen mode.")
