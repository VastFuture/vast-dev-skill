// Vast Dev Skills Apple Design & Interactive Mermaid Engine with Pan, Zoom & Fullscreen
let allSkills = [];
let currentCategory = 'all';
let searchQuery = '';

// Pan & Zoom State
let zoomLevel = 1.0;
let panX = 0;
let panY = 0;
let isPanning = false;
let startX = 0;
let startY = 0;
let isFullscreen = false;

// Apple HIG SVG Icon System
const SVG_ICONS = {
  apple: `<svg width="18" height="18" viewBox="0 0 170 170" fill="currentColor"><path d="M150.37 130.25c-2.45 5.66-5.35 10.87-8.71 15.66-4.58 6.53-8.33 11.05-11.22 13.56-4.48 4.12-9.28 6.23-14.42 6.35-3.69 0-8.14-1.05-13.32-3.18-5.19-2.12-9.97-3.17-14.34-3.17-4.58 0-9.49 1.05-14.75 3.17-5.26 2.13-9.5 3.24-12.74 3.35-4.35.13-9.16-1.9-14.42-6.08-3.7-3.08-7.77-7.94-12.21-14.58-6.97-10.45-12.26-21.78-15.87-33.99-3.61-12.2-5.42-23.75-5.42-34.64 0-14.24 3.73-25.75 11.2-34.54 7.47-8.78 16.74-13.3 27.81-13.56 5.01 0 10.51 1.25 16.49 3.76 5.98 2.5 9.77 3.81 11.36 3.91 1.85-.2 5.92-1.6 12.21-4.21 6.29-2.61 11.66-3.81 16.12-3.6 12.29.63 21.94 4.88 28.94 12.75-10.67 6.47-15.9 15.35-15.69 26.65.21 8.8 3.53 16.1 9.97 21.91 6.44 5.81 14.15 9.21 23.13 10.2-2.18 6.53-4.9 13.06-8.16 19.59zM119.22 31.84c0-7.39 2.66-14.41 7.98-21.05 5.32-6.64 11.88-10.79 19.68-12.44.22 1.3.33 2.4.33 3.29 0 7.4-2.83 14.51-8.5 21.34-5.66 6.83-12.29 10.79-19.89 11.87-.22-1.08-.33-2.09-.33-3.01z"/></svg>`,
  all: `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1.5"></rect><rect x="14" y="3" width="7" height="7" rx="1.5"></rect><rect x="14" y="14" width="7" height="7" rx="1.5"></rect><rect x="3" y="14" width="7" height="7" rx="1.5"></rect></svg>`,
  'code-review': `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>`,
  pm: `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>`,
  'pm-lenny': `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>`,
  visualization: `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>`,
  workflow: `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>`,
  content: `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>`,
  'ai-cli': `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="14" x2="23" y2="14"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="14" x2="4" y2="14"></line></svg>`,
  tools: `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path></svg>`
};

function renderSimpleMarkdown(md) {
  if (!md) return '';
  return md
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/```([a-zA-Z0-9_\-]*)\n([\s\S]*?)```/g, (match, lang, code) => {
      return `<pre><code class="language-${lang}">${code.trim()}</code></pre>`;
    })
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\*([^*]+)\*/g, '<em>$1</em>')
    .replace(/^\> (.*$)/gim, '<blockquote>$1</blockquote>')
    .replace(/^\- (.*$)/gim, '<li>$1</li>')
    .replace(/(<li>[\s\S]*?<\/li>)/g, '<ul>$1</ul>')
    .replace(/<\/ul>\s*<ul>/g, '')
    .replace(/\n\n/g, '<br><br>');
}

async function loadData() {
  if (window.__SKILLS_DATA__) {
    allSkills = window.__SKILLS_DATA__;
    initUI();
    return;
  }
  try {
    const res = await fetch('assets/skills-data.json');
    allSkills = await res.json();
    initUI();
  } catch (err) {
    console.error('Failed to load skills:', err);
  }
}

function initUI() {
  document.getElementById('total-counter').textContent = allSkills.length;
  renderCategories();
  renderSkills();

  // Search
  const searchInput = document.getElementById('search-input');
  searchInput.addEventListener('input', (e) => {
    searchQuery = e.target.value.trim().toLowerCase();
    renderSkills();
  });

  // Modal
  const modal = document.getElementById('detail-modal');
  const closeBtn = document.getElementById('modal-close-btn');
  closeBtn.addEventListener('click', () => {
    if (isFullscreen) toggleFullscreen();
    modal.classList.remove('open');
  });
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      if (isFullscreen) toggleFullscreen();
      modal.classList.remove('open');
    }
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (isFullscreen) {
        toggleFullscreen();
      } else if (modal.classList.contains('open')) {
        modal.classList.remove('open');
      }
    }
  });

  // Setup pan & zoom listeners
  setupPanAndZoom();

  // Initialize Mermaid with Apple HIG palette
  if (window.mermaid) {
    window.mermaid.initialize({
      startOnLoad: false,
      theme: 'neutral',
      fontFamily: '-apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", sans-serif',
      themeVariables: {
        primaryColor: '#F5F5F7',
        primaryTextColor: '#1D1D1F',
        primaryBorderColor: '#D2D2D7',
        lineColor: '#86868B',
        secondaryColor: '#E8F2FF',
        tertiaryColor: '#FFFFFF',
        mainBkg: '#FFFFFF',
        nodeBorder: '#D2D2D7',
        clusterBkg: '#FAFAFC',
        clusterBorder: '#E5E5EA',
        fontSize: '13px'
      }
    });
  }
}

function setupPanAndZoom() {
  const viewport = document.getElementById('diagram-viewport');

  viewport.addEventListener('wheel', (e) => {
    e.preventDefault();
    const delta = e.deltaY > 0 ? -0.1 : 0.1;
    zoomLevel = Math.min(Math.max(0.35, zoomLevel + delta), 3.0);
    updateCanvasTransform();
  }, { passive: false });

  viewport.addEventListener('mousedown', (e) => {
    isPanning = true;
    startX = e.clientX - panX;
    startY = e.clientY - panY;
  });

  window.addEventListener('mousemove', (e) => {
    if (!isPanning) return;
    panX = e.clientX - startX;
    panY = e.clientY - startY;
    updateCanvasTransform();
  });

  window.addEventListener('mouseup', () => {
    isPanning = false;
  });
}

function updateCanvasTransform() {
  const canvas = document.getElementById('diagram-canvas');
  const indicator = document.getElementById('zoom-indicator');
  canvas.style.transform = `translate(${panX}px, ${panY}px) scale(${zoomLevel})`;
  indicator.textContent = `${Math.round(zoomLevel * 100)}%`;
}

function zoomIn() {
  zoomLevel = Math.min(3.0, zoomLevel + 0.2);
  updateCanvasTransform();
}

function zoomOut() {
  zoomLevel = Math.max(0.35, zoomLevel - 0.2);
  updateCanvasTransform();
}

function resetZoom() {
  zoomLevel = 1.0;
  panX = 0;
  panY = 0;
  updateCanvasTransform();
}

function toggleFullscreen() {
  const section = document.getElementById('diagram-section');
  isFullscreen = !isFullscreen;
  
  if (isFullscreen) {
    section.classList.add('fullscreen-mode');
    document.body.style.overflow = 'hidden';
    // Slightly boost initial zoom in fullscreen if needed
    zoomLevel = 1.15;
  } else {
    section.classList.remove('fullscreen-mode');
    document.body.style.overflow = '';
    zoomLevel = 1.0;
  }
  panX = 0;
  panY = 0;
  updateCanvasTransform();
}

function renderCategories() {
  const catMap = { all: { name: '全部技能', count: allSkills.length } };

  allSkills.forEach(s => {
    if (!catMap[s.categoryId]) {
      catMap[s.categoryId] = {
        name: s.category,
        count: 0
      };
    }
    catMap[s.categoryId].count++;
  });

  const menu = document.getElementById('sidebar-menu');
  menu.innerHTML = Object.entries(catMap).map(([id, item]) => {
    const iconSvg = SVG_ICONS[id] || SVG_ICONS.tools;
    return `
      <li>
        <button class="sidebar-item ${currentCategory === id ? 'active' : ''}" data-id="${id}">
          <span class="sidebar-btn-label">
            <span class="cat-svg-icon">${iconSvg}</span>
            <span>${item.name}</span>
          </span>
          <span class="sidebar-badge">${item.count}</span>
        </button>
      </li>
    `;
  }).join('');

  menu.querySelectorAll('.sidebar-item').forEach(btn => {
    btn.addEventListener('click', () => {
      menu.querySelectorAll('.sidebar-item').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentCategory = btn.dataset.id;
      renderSkills();
    });
  });
}

function renderSkills() {
  const grid = document.getElementById('cards-grid');
  const sectionTitle = document.getElementById('current-section-title');

  let filtered = allSkills.filter(s => {
    const matchesCat = (currentCategory === 'all' || s.categoryId === currentCategory);
    const matchesSearch = !searchQuery || 
      s.name.toLowerCase().includes(searchQuery) ||
      s.displayTitle.toLowerCase().includes(searchQuery) ||
      s.description.toLowerCase().includes(searchQuery) ||
      (s.triggers && s.triggers.some(t => t.toLowerCase().includes(searchQuery)));
    return matchesCat && matchesSearch;
  });

  const catNames = {
    all: '全部技能指南',
    'code-review': '代码品质与架构',
    pm: '产品规划与设计',
    'pm-lenny': 'Lenny 战略智库',
    visualization: '架构图谱与可视化',
    workflow: '自动化协作流',
    content: '内容与叙事工程',
    'ai-cli': '模型与 CLI 编排',
    tools: '工程效能工具'
  };

  sectionTitle.textContent = `${catNames[currentCategory] || '技能分类'} (${filtered.length})`;

  if (filtered.length === 0) {
    grid.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 4rem 1rem; color: #86868B;">
        <h3 style="font-weight: 500; margin-bottom: 0.5rem; color: #1D1D1F;">未找到符合条件的技能</h3>
        <p style="font-size: 0.9rem;">请尝试更换检索关键词或查看全部类别。</p>
      </div>`;
    return;
  }

  grid.innerHTML = filtered.map(s => {
    const triggers = (s.triggers || []).slice(0, 3).map(t => `<span class="trigger-tag">${t}</span>`).join('');
    const iconSvg = SVG_ICONS[s.categoryId] || SVG_ICONS.tools;
    return `
      <div class="skill-card" data-id="${s.id}">
        <div>
          <div class="card-tag">
            <span class="cat-svg-icon-sm">${iconSvg}</span>
            <span>${s.category}</span>
          </div>
          <h3 class="card-title">${s.displayTitle || s.name}</h3>
          <p class="card-desc">${s.description}</p>
        </div>
        <div class="card-footer">
          <div class="trigger-tags">${triggers}</div>
          <span class="card-action">教学详情 &rarr;</span>
        </div>
      </div>
    `;
  }).join('');

  grid.querySelectorAll('.skill-card').forEach(card => {
    card.addEventListener('click', () => {
      const skill = allSkills.find(s => s.id === card.dataset.id);
      if (skill) openSkillModal(skill);
    });
  });
}

function openSkillModal(skill) {
  const modal = document.getElementById('detail-modal');
  document.getElementById('modal-skill-title').textContent = skill.displayTitle || skill.name;
  document.getElementById('modal-skill-path').textContent = skill.path;
  document.getElementById('prompt-text-display').textContent = skill.samplePrompt;

  // Make sure not fullscreen when opening fresh
  if (isFullscreen) toggleFullscreen();
  resetZoom();

  // Render Mermaid diagram
  const canvas = document.getElementById('diagram-canvas');
  if (skill.mermaid && window.mermaid) {
    const id = 'mermaid-' + Math.random().toString(36).substring(2, 9);
    canvas.innerHTML = `<div class="mermaid" id="${id}">${skill.mermaid}</div>`;
    try {
      window.mermaid.run({ nodes: [document.getElementById(id)] });
    } catch (e) {
      console.warn("Client Mermaid render warning:", e);
      canvas.innerHTML = `
        <div class="mermaid-error-box">
          <p>当前拓扑已启用降级安全保护，原语结构正常：</p>
          <pre style="text-align:left; font-size:0.75rem; margin-top:0.5rem; background:#F5F5F7; padding:0.8rem; border-radius:8px;">${skill.mermaid}</pre>
        </div>`;
    }
  } else {
    canvas.innerHTML = `<div style="color:#86868B; font-size:0.85rem;">暂无逻辑流程图</div>`;
  }

  // Render markdown content
  document.getElementById('tutorial-markdown').innerHTML = renderSimpleMarkdown(skill.content);

  modal.classList.add('open');
}

function copyPromptCommand() {
  const text = document.getElementById('prompt-text-display').textContent;
  navigator.clipboard.writeText(text).then(() => {
    const btn = document.getElementById('copy-prompt-btn');
    const orig = btn.textContent;
    btn.textContent = '已拷贝';
    btn.style.background = '#34C759';
    setTimeout(() => {
      btn.textContent = orig;
      btn.style.background = '';
    }, 1500);
  });
}

window.addEventListener('DOMContentLoaded', loadData);
