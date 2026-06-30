const rawPayload = window.RICO_BOOKMARKS_DATA || {
  bookmarks: window.bookmarksData || [],
  reports: {}
};

const state = {
  query: "",
  category: "all",
  subcategory: "",
  tag: "",
  domain: "all",
  status: "all",
  view: "grid",
  insightPanel: "summary",
  staged: JSON.parse(localStorage.getItem("ricoBookmarkStage") || "{}"),
  sidebarCollapsed: localStorage.getItem("ricoSidebarCollapsed") === "true",
  expandedCategories: loadExpandedCategories()
};

const $ = (id) => document.getElementById(id);
const UNKNOWN_VALUES = new Set(["", "unknown", "undefined", "null", "none", "n/a", "na"]);
const TAG_PLACEHOLDERS = new Set(["未分类", "其他", "Uncategorized", "Other"]);

document.addEventListener("DOMContentLoaded", init);

function init() {
  applyThemeMeta();
  applySidebarState();
  bindEvents();
  renderShell();
  renderAll();
  refreshIcons();
  requestAnimationFrame(() => document.querySelector(".site-shell")?.classList.add("sidebar-ready"));
}

function bindEvents() {
  $("homeLink").addEventListener("click", (event) => {
    event.preventDefault();
    clearFilters();
  });

  $("sidebarToggle").addEventListener("click", () => {
    state.sidebarCollapsed = !state.sidebarCollapsed;
    localStorage.setItem("ricoSidebarCollapsed", String(state.sidebarCollapsed));
    applySidebarState();
  });

  $("guideBtn").addEventListener("click", openGuide);

  $("clearAllBtn").addEventListener("click", clearFilters);

  $("shuffleFeaturedBtn").addEventListener("click", () => {
    if ($("featuredSection").hidden) return;
    renderFeaturedGrid(bookmarks());
    refreshIcons();
  });

  $("searchInput").addEventListener("input", (event) => {
    state.query = event.target.value.trim().toLowerCase();
    renderAll();
  });

  $("domainFilter").addEventListener("change", (event) => {
    state.domain = event.target.value;
    renderAll();
  });

  $("statusFilter").addEventListener("change", (event) => {
    state.status = event.target.value;
    renderAll();
  });

  document.querySelectorAll(".view-btn").forEach((button) => {
    button.addEventListener("click", () => {
      state.view = button.dataset.view;
      document.querySelectorAll(".view-btn").forEach((item) => item.classList.toggle("active", item === button));
      renderBookmarks();
    });
  });

  $("exportMenuBtn").addEventListener("click", () => {
    const menu = $("exportMenu");
    const open = menu.hasAttribute("hidden");
    menu.toggleAttribute("hidden", !open);
    $("exportMenuBtn").setAttribute("aria-expanded", String(open));
  });

  document.addEventListener("click", (event) => {
    if (!event.target.closest(".side-actions")) {
      $("exportMenu").setAttribute("hidden", "");
      $("exportMenuBtn").setAttribute("aria-expanded", "false");
    }
  });

  $("exportJsonBtn").addEventListener("click", () => download("rico-bookmarks.json", JSON.stringify(exportData(), null, 2), "application/json"));
  $("exportMdBtn").addEventListener("click", () => download("bookmark-overview.md", makeMarkdown(bookmarks()), "text/markdown"));
  $("exportHtmlBtn").addEventListener("click", () => download("bookmarks_import.html", makeBrowserHtml(bookmarks()), "text/html"));

  $("mobileFilterBtn").addEventListener("click", () => {
    renderMobileFilters(bookmarks());
    $("mobileFilterDialog").showModal();
    refreshIcons();
  });

  $("mobileInsightsBtn").addEventListener("click", () => {
    renderInsights();
    $("insightDialog").showModal();
  });

  $("mobileExportBtn").addEventListener("click", () => {
    $("mobileExportDialog").showModal();
  });

  $("mobileGuideBtn").addEventListener("click", openGuide);

  $("mobileExportJsonBtn").addEventListener("click", () => download("rico-bookmarks.json", JSON.stringify(exportData(), null, 2), "application/json"));
  $("mobileExportMdBtn").addEventListener("click", () => download("bookmark-overview.md", makeMarkdown(bookmarks()), "text/markdown"));
  $("mobileExportHtmlBtn").addEventListener("click", () => download("bookmarks_import.html", makeBrowserHtml(bookmarks()), "text/html"));

  $("insightsBtn").addEventListener("click", () => {
    renderInsights();
    $("insightDialog").showModal();
  });

  $("insightTabs").addEventListener("click", (event) => {
    const button = event.target.closest("button[data-panel]");
    if (!button) return;
    state.insightPanel = button.dataset.panel;
    renderInsights();
  });
}

function openGuide() {
  $("guideDialog").showModal();
}

function applyThemeMeta() {
  const theme = window.RICO_BOOKMARKS_META?.theme || {};
  document.documentElement.dataset.theme = theme.id || "kami";
  document.documentElement.dataset.mode = theme.mode || "light";
  $("themeEyebrow").textContent = "目录";
}

function applySidebarState() {
  const shell = document.querySelector(".site-shell");
  const button = $("sidebarToggle");
  if (!shell || !button) return;
  const collapsed = state.sidebarCollapsed;
  const label = collapsed ? "展开侧边栏" : "收起侧边栏";
  shell.classList.toggle("sidebar-collapsed", collapsed);
  button.setAttribute("aria-label", label);
  button.setAttribute("title", label);
  button.setAttribute("aria-expanded", String(!collapsed));
}

function refreshIcons() {
  if (window.lucide && typeof window.lucide.createIcons === "function") {
    window.lucide.createIcons();
  }
}

function icon(name, cls = "icon") {
  return `<i data-lucide="${name}" class="${cls}"></i>`;
}

const CATEGORY_ICON_MAP = {
  "AI": "sparkles",
  "前端": "code-2",
  "设计": "palette",
  "互联网": "compass",
  "工具产品": "wrench",
  "博客": "pen-tool",
  "学习教程": "graduation-cap",
  "其他": "shapes",
};

const CATEGORY_ICON_KEYWORDS = [
  [/web3|加密|crypto|nft|defi|blockchain|bitcoin/i, "bitcoin"],
  [/3d|webgl|motion|interactive|three\.?js|box/i, "box"],
  [/作品集|portfolio|designer|artist/i, "user"],
  [/品牌|brand|official/i, "badge-check"],
  [/灵感|inspiration|创意|creative/i, "images"],
  [/字体|font|typography|type/i, "type"],
  [/配色|color|palette|gradient/i, "pipette"],
  [/电商|shop|ecommerce|store/i, "shopping-bag"],
  [/支付|payment|pay|stripe/i, "credit-card"],
  [/框架|framework|react|vue|angular|svelte/i, "component"],
  [/组件|ui|component|shadcn|radix/i, "layout-grid"],
  [/部署|deploy|vercel|netlify|cloudflare/i, "cloud"],
  [/博客|blog|medium|substack/i, "rss"],
  [/教程|tutorial|learn|course/i, "book-open"],
  [/工具|tool|util/i, "wrench"],
  [/平台|platform/i, "layers"],
  [/效率|productivity|notion|linear/i, "zap"],
  [/数据库|database|db|postgres|mongo/i, "database"],
  [/搜索|search|algolia/i, "search"],
  [/监控|monitor|grafana|sentry/i, "activity"],
  [/安全|security|password|vpn/i, "shield"],
  [/api|sdk|dev|开发/i, "terminal"],
  [/ai|人工智能|大模型|ml|llm/i, "sparkles"],
  [/设计|design|figma|sketch/i, "palette"],
  [/前端|frontend|css|html|js/i, "code-2"],
];

function categoryIcon(name) {
  if (!name) return icon("hash", "icon cat-icon");
  if (CATEGORY_ICON_MAP[name]) return icon(CATEGORY_ICON_MAP[name], "icon cat-icon");
  for (const [re, iconName] of CATEGORY_ICON_KEYWORDS) {
    if (re.test(name)) return icon(iconName, "icon cat-icon");
  }
  return icon("hash", "icon cat-icon");
}

function bookmarks() {
  return (rawPayload.bookmarks || []).map(normalizeBookmark);
}

function normalizeBookmark(raw) {
  const id = String(raw.id || raw.canonical_url || raw.url || raw.title || Math.random());
  const staged = state.staged[id] || {};
  const merged = { ...raw, ...staged };
  const categoryPath = cleanPath(
    merged.category_path ||
    merged.optimized_category_path ||
    [merged.primary_category, merged.subcategory]
  );
  const sourcePath = cleanPath(merged.source_folder_path || merged.source_category_path || merged.folder_path || []);
  const url = String(merged.url || "");
  const domain = cleanLabel(merged.domain) || domainFromUrl(url);
  const tags = cleanTags(merged.tags || [], categoryPath);
  const status = cleanLabel(merged.link_status);
  const rawTitle = cleanLabel(merged.title) || domain || url || "未命名书签";
  const cleanTitle = cleanLabel(merged.clean_title);
  return {
    ...merged,
    id,
    title: rawTitle,
    cleanTitle: cleanTitle && cleanTitle !== rawTitle ? cleanTitle : "",
    url,
    domain,
    categoryPath: categoryPath.length ? categoryPath : ["未分类"],
    sourcePath,
    tags,
    description: cleanLabel(merged.description),
    status,
    httpStatus: merged.http_status,
    duplicateGroup: cleanLabel(merged.duplicate_group),
    reviewStatus: cleanLabel(merged.review_status),
    addDate: Number(merged.add_date || 0)
  };
}

function cleanPath(value) {
  const parts = Array.isArray(value) ? value : String(value || "").split("/");
  return unique(parts.map(cleanLabel).filter(Boolean));
}

function cleanTags(value, categoryPath = []) {
  const list = Array.isArray(value) ? value : String(value || "").split(",");
  return unique(list.map(cleanLabel).filter((tag) => tag && !TAG_PLACEHOLDERS.has(tag) && !isCategoryTag(tag, categoryPath)));
}

function cleanLabel(value) {
  const text = String(value ?? "").replace(/\s+/g, " ").trim();
  return isUnknown(text) ? "" : text;
}

function isUnknown(value) {
  return UNKNOWN_VALUES.has(String(value || "").trim().toLowerCase());
}

function isCategoryTag(tag, categoryPath = []) {
  const normalizedTag = normalizeCompare(tag);
  const parts = categoryPath.map(normalizeCompare).filter(Boolean);
  const joinedSlash = normalizeCompare(categoryPath.join("/"));
  const joinedSpaced = normalizeCompare(categoryPath.join(" / "));
  const joinedDot = normalizeCompare(categoryPath.join(" · "));
  return parts.includes(normalizedTag) || normalizedTag === joinedSlash || normalizedTag === joinedSpaced || normalizedTag === joinedDot;
}

function normalizeCompare(value) {
  return String(value || "").replace(/\s*[/·]\s*/g, "/").replace(/\s+/g, " ").trim().toLowerCase();
}

function domainFromUrl(url) {
  try {
    return new URL(url).hostname.replace(/^www\./, "");
  } catch {
    return "";
  }
}

function renderShell() {
  const list = bookmarks();
  renderCategoryNav(list);
  renderMobileCategories(list);
  renderTagCloud(list);
  renderSelect("domainFilter", ["all", ...unique(list.map((b) => b.domain).filter(Boolean)).slice(0, 150)], "全部域名");
  renderSelect("statusFilter", ["all", ...unique(list.map((b) => b.status).filter(Boolean))], "全部状态");
}

function renderCategoryNav(list) {
  const nav = $("categoryNav");
  const tree = categoryTree(list);
  const allActive = state.category === "all";
  const rows = [
    `<button type="button" class="cat-item ${allActive ? "active" : ""}" data-category="all">
      <span>全部书签</span><em>${list.length}</em>
    </button>`
  ];
  Object.entries(tree).forEach(([name, node]) => {
    const active = state.category === name && !state.subcategory;
    const children = Object.entries(node.children);
    const hasChildren = children.length > 0;
    const forceExpanded = state.category === name;
    const expanded = forceExpanded || state.expandedCategories[name] === true;
    rows.push(`<div class="cat-group ${expanded ? "expanded" : ""}" data-cat-group="${escapeAttr(name)}">
      <div class="cat-row ${hasChildren ? "" : "no-children"}">
        <button type="button" class="cat-item cat-main ${active ? "active" : ""}" data-category="${escapeAttr(name)}">
          ${categoryIcon(name)}<span>${escapeHtml(name)}</span><em>${node.count}</em>
        </button>
        ${hasChildren ? `<button type="button" class="cat-toggle" data-toggle-category="${escapeAttr(name)}" aria-label="${expanded ? "收起" : "展开"} ${escapeAttr(name)}" aria-expanded="${expanded}">
          ${icon("chevron-right", "icon cat-toggle-icon")}
        </button>` : ""}
      </div>
      ${hasChildren ? `<div class="cat-children">
        <div class="cat-children-inner">
          ${children.map(([sub, count]) => {
            const subActive = state.category === name && state.subcategory === sub;
            return `<button type="button" class="cat-subitem ${subActive ? "active" : ""}" data-category="${escapeAttr(name)}" data-subcategory="${escapeAttr(sub)}">
              <span>${escapeHtml(sub)}</span><em>${count}</em>
            </button>`;
          }).join("")}
        </div>
      </div>` : ""}
    </div>`);
  });
  nav.innerHTML = rows.join("");
  nav.querySelectorAll("button[data-category]").forEach((button) => {
    button.addEventListener("click", () => {
      state.category = button.dataset.category || "all";
      state.subcategory = button.dataset.subcategory || "";
      if (state.category !== "all") {
        state.expandedCategories[state.category] = true;
        saveExpandedCategories();
      }
      state.tag = "";
      renderAll();
    });
  });
  nav.querySelectorAll("[data-toggle-category]").forEach((button) => {
    button.addEventListener("click", (event) => {
      event.stopPropagation();
      const category = button.dataset.toggleCategory;
      if (!category) return;
      state.expandedCategories[category] = state.expandedCategories[category] !== true;
      saveExpandedCategories();
      renderCategoryNav(bookmarks());
      refreshIcons();
    });
  });
}

function renderMobileCategories(list) {
  const tree = categoryTree(list);
  const chips = [`<button type="button" class="${state.category === "all" ? "active" : ""}" data-category="all">全部</button>`];
  Object.entries(tree).slice(0, 12).forEach(([name, node]) => {
    chips.push(`<button type="button" class="${state.category === name ? "active" : ""}" data-category="${escapeAttr(name)}">${escapeHtml(name)} <span>${node.count}</span></button>`);
  });
  $("mobileCategories").innerHTML = chips.join("");
  $("mobileCategories").querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => {
      state.category = button.dataset.category || "all";
      state.subcategory = "";
      state.tag = "";
      renderAll();
    });
  });
}

function renderTagCloud(list) {
  const tags = tagCounts(list, 28);
  $("tagCloud").innerHTML = tags.length
    ? tags.map(([tag, count]) => `<button type="button" class="${state.tag === tag ? "active" : ""}" data-tag="${escapeAttr(tag)}">${escapeHtml(tag)} <span>${count}</span></button>`).join("")
    : `<p class="muted">No displayable tags in the current data.</p>`;
  $("tagCloud").querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => {
      state.tag = state.tag === button.dataset.tag ? "" : button.dataset.tag;
      renderAll();
    });
  });
}

function tagCounts(list, limit = 28) {
  const counts = new Map();
  list.forEach((bookmark) => bookmark.tags.forEach((tag) => counts.set(tag, (counts.get(tag) || 0) + 1)));
  return [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], "zh-Hans-CN")).slice(0, limit);
}

function renderSelect(id, values, allLabel) {
  $(id).innerHTML = values.map((value, index) => `<option value="${escapeAttr(value)}">${index === 0 ? allLabel : escapeHtml(value)}</option>`).join("");
  $(id).value = state[id === "domainFilter" ? "domain" : "status"];
}

function stats(list) {
  return {
    total: list.length,
    categories: unique(list.map(firstPath)).length,
    domains: unique(list.map((item) => item.domain).filter(Boolean)).length,
    problemLinks: list.filter(isProblemLink).length,
    staged: Object.keys(state.staged || {}).length
  };
}

function hasActiveFilters() {
  return Boolean(
    state.query ||
    state.category !== "all" ||
    state.subcategory ||
    state.tag ||
    state.domain !== "all" ||
    state.status !== "all"
  );
}

function activeFilterCount() {
  return [
    state.query,
    state.category !== "all",
    state.tag,
    state.domain !== "all",
    state.status !== "all"
  ].filter(Boolean).length;
}

function renderMobileFilters(list) {
  const content = $("mobileFilterContent");
  if (!content) return;
  const filterCount = activeFilterCount();
  $("mobileFilterBtn").innerHTML = `${icon("sliders-horizontal")}Filters${filterCount ? `<span>${filterCount}</span>` : ""}`;
  const domains = ["all", ...unique(list.map((bookmark) => bookmark.domain).filter(Boolean)).slice(0, 150)];
  const statuses = ["all", ...unique(list.map((bookmark) => bookmark.status).filter(Boolean))];
  const tagEntries = tagCounts(list, 32);
  content.innerHTML = `<div class="mobile-filter-stack">
    <label>
      <span>域名</span>
      <select id="mobileDomainFilter">${domains.map((value, index) => `<option value="${escapeAttr(value)}">${index === 0 ? "全部域名" : escapeHtml(value)}</option>`).join("")}</select>
    </label>
    <label>
      <span>链接状态</span>
      <select id="mobileStatusFilter">${statuses.map((value, index) => `<option value="${escapeAttr(value)}">${index === 0 ? "全部状态" : escapeHtml(value)}</option>`).join("")}</select>
    </label>
    <div class="mobile-filter-tags">
      <span>常用标签</span>
      <div>${tagEntries.length
        ? tagEntries.map(([tag, count]) => `<button type="button" class="${state.tag === tag ? "active" : ""}" data-mobile-tag="${escapeAttr(tag)}">${escapeHtml(tag)} <em>${count}</em></button>`).join("")
        : `<p class="muted">当前数据中没有可显示的标签。</p>`}
      </div>
    </div>
    <button type="button" class="quiet-btn mobile-clear-btn" id="mobileClearFiltersBtn"${hasActiveFilters() ? "" : " disabled"}>清除筛选</button>
  </div>`;
  $("mobileDomainFilter").value = state.domain;
  $("mobileStatusFilter").value = state.status;
  $("mobileDomainFilter").addEventListener("change", (event) => {
    state.domain = event.target.value;
    renderAll();
  });
  $("mobileStatusFilter").addEventListener("change", (event) => {
    state.status = event.target.value;
    renderAll();
  });
  content.querySelectorAll("[data-mobile-tag]").forEach((button) => {
    button.addEventListener("click", () => {
      state.tag = state.tag === button.dataset.mobileTag ? "" : button.dataset.mobileTag;
      renderAll();
    });
  });
  $("mobileClearFiltersBtn").addEventListener("click", clearFilters);
}

function renderAll() {
  const list = bookmarks();
  renderAtlasStats(list);
  renderFeatured(list);
  renderActiveFilters();
  renderScope();
  renderBookmarks();
  renderCategoryNav(list);
  renderMobileCategories(list);
  renderMobileFilters(list);
  renderTagCloud(list);
  refreshIcons();
}

function renderAtlasStats(list) {
  const data = stats(list);
  const items = [
    ["书签", data.total],
    ["分类", data.categories],
    ["域名", data.domains],
    [data.problemLinks ? "问题链接" : "暂存编辑", data.problemLinks || data.staged]
  ];
  $("atlasStats").innerHTML = items.map(([label, value]) => `<span><strong>${value}</strong><em>${label}</em></span>`).join("");
}

function renderFeatured(list) {
  const section = $("featuredSection");
  const shouldShow = !state.query && state.category === "all" && !state.tag && state.domain === "all" && state.status === "all";
  section.hidden = !shouldShow;
  if (!shouldShow) return;
  renderFeaturedGrid(list);
}

function renderFeaturedGrid(list) {
  const featured = featuredBookmarks(list);
  const grid = $("featuredGrid");
  grid.innerHTML = featured.map(renderFeaturedCard).join("");
  grid.querySelectorAll("[data-open]").forEach(bindOpenCard);
  grid.querySelectorAll("[data-detail]").forEach(bindDetailButton);
}

function featuredBookmarks(list) {
  if (!Array.isArray(list) || !list.length) return [];
  const shuffled = [...list];
  for (let i = shuffled.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled.slice(0, 4);
}

function renderActiveFilters() {
  const filters = [];
  if (state.category !== "all") filters.push(["category", state.subcategory ? `${state.category} / ${state.subcategory}` : state.category]);
  if (state.tag) filters.push(["tag", `标签：${state.tag}`]);
  if (state.domain !== "all") filters.push(["domain", `域名：${state.domain}`]);
  if (state.status !== "all") filters.push(["status", `状态：${state.status}`]);
  if (!filters.length && !state.query) {
    $("activeFilters").innerHTML = "";
    return;
  }
  const queryChip = state.query ? `<button type="button" data-clear="query">搜索：${escapeHtml(state.query)} ×</button>` : "";
  const clearAll = `<button type="button" class="clear-chip" data-clear="all">全部清除</button>`;
  $("activeFilters").innerHTML = queryChip + filters.map(([key, label]) => `<button type="button" data-clear="${key}">${escapeHtml(label)} ×</button>`).join("") + clearAll;
  $("activeFilters").querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => {
      clearFilter(button.dataset.clear);
    });
  });
}

function renderScope() {
  let title = "全部书签";
  if (state.category !== "all") title = state.subcategory ? `${state.category} / ${state.subcategory}` : state.category;
  if (state.tag) title = `标签：${state.tag}`;
  if (state.query) title = `搜索：${state.query}`;
  $("scopeTitle").textContent = title;
  $("scopeEyebrow").textContent = state.category === "all" && !state.tag && !state.query ? "浏览" : "筛选结果";
}

function renderBookmarks() {
  const list = filtered();
  const total = bookmarks().length;
  const active = hasActiveFilters();
  $("resultCount").textContent = active ? `${total} 个书签中的 ${list.length} 个` : `${total} 个书签`;
  $("clearAllBtn").hidden = !active;
  $("bookmarkGrid").hidden = state.view !== "grid";
  $("bookmarkList").hidden = state.view !== "list";
  $("emptyState").hidden = list.length > 0;
  if (!list.length) {
    $("emptyState").innerHTML = total
      ? `<strong>没有匹配的书签</strong><span>清除筛选，或换个关键词试试。</span><button type="button" class="quiet-btn" id="emptyClearBtn">清除筛选</button>`
      : `<strong>还没有书签数据</strong><span>请先用 Rico 解析一份浏览器导出的书签 HTML。</span>`;
    const emptyClear = $("emptyClearBtn");
    if (emptyClear) emptyClear.addEventListener("click", clearFilters);
  }
  if (state.view === "grid") {
    $("bookmarkGrid").innerHTML = list.map(renderBookmarkCard).join("");
    $("bookmarkGrid").querySelectorAll("[data-open]").forEach(bindOpenCard);
    $("bookmarkGrid").querySelectorAll("[data-detail]").forEach(bindDetailButton);
  } else {
    $("bookmarkList").innerHTML = list.map(renderBookmarkRow).join("");
    $("bookmarkList").querySelectorAll("[data-open]").forEach(bindOpenCard);
    $("bookmarkList").querySelectorAll("[data-detail]").forEach(bindDetailButton);
  }
}

function filtered() {
  return bookmarks().filter((bookmark) => {
    const text = [
      bookmark.title,
      bookmark.url,
      bookmark.domain,
      bookmark.description,
      ...bookmark.tags,
      ...bookmark.categoryPath,
      ...bookmark.sourcePath
    ].join(" ").toLowerCase();
    if (state.query && !text.includes(state.query)) return false;
    if (state.category !== "all" && firstPath(bookmark) !== state.category) return false;
    if (state.subcategory && secondPath(bookmark) !== state.subcategory) return false;
    if (state.tag && !bookmark.tags.includes(state.tag)) return false;
    if (state.domain !== "all" && bookmark.domain !== state.domain) return false;
    if (state.status !== "all" && bookmark.status !== state.status) return false;
    return true;
  });
}

function renderFeaturedCard(bookmark) {
  const desc = displayDescription(bookmark);
  const displayTitle = bookmark.cleanTitle || bookmark.title;
  return `<article class="featured-card" data-open="${escapeAttr(bookmark.url)}">
    <div>
      <span class="domain-badge">${escapeHtml(bookmark.domain || firstPath(bookmark))}</span>
      <h3>${escapeHtml(displayTitle)}</h3>
      ${desc ? `<p>${escapeHtml(desc)}</p>` : ""}
    </div>
    <button type="button" class="detail-btn" data-detail="${escapeAttr(bookmark.id)}">详情</button>
  </article>`;
}

function renderBookmarkCard(bookmark) {
  const tags = bookmark.tags.slice(0, 4).map((tag) => `<span>${escapeHtml(tag)}</span>`).join("");
  const status = statusPill(bookmark);
  const desc = displayDescription(bookmark);
  const displayTitle = bookmark.cleanTitle || bookmark.title;
  return `<article class="bookmark-card" data-open="${escapeAttr(bookmark.url)}">
    <div class="card-main">
      <div class="site-icon" style="${iconStyle(bookmark)}">${escapeHtml(iconText(bookmark))}</div>
      <div class="card-text">
        <h3>${escapeHtml(displayTitle)}</h3>
        ${bookmark.domain ? `<p class="bookmark-domain">${escapeHtml(bookmark.domain)}</p>` : ""}
      </div>
    </div>
    ${desc ? `<p class="bookmark-desc">${escapeHtml(desc)}</p>` : ""}
    <div class="bookmark-meta">
      <span class="path-pill">${categoryIcon(bookmark.categoryPath[0])}${escapeHtml(bookmark.categoryPath.join(" / "))}</span>
      ${status}
    </div>
    ${tags ? `<div class="bookmark-tags">${tags}</div>` : ""}
    <div class="card-actions">
      <a class="visit-link" href="${escapeAttr(bookmark.url)}" target="_blank" rel="noopener">${icon("external-link")}访问</a>
      <button class="ghost-detail" type="button" data-detail="${escapeAttr(bookmark.id)}">详情</button>
    </div>
  </article>`;
}

function renderBookmarkRow(bookmark) {
  const tags = bookmark.tags.slice(0, 3).map((tag) => `<span>${escapeHtml(tag)}</span>`).join("");
  const displayTitle = bookmark.cleanTitle || bookmark.title;
  return `<article class="bookmark-row" data-open="${escapeAttr(bookmark.url)}">
    <div class="site-icon" style="${iconStyle(bookmark)}">${escapeHtml(iconText(bookmark))}</div>
    <div class="row-body">
      <h3>${escapeHtml(displayTitle)}</h3>
      <p>${escapeHtml(bookmark.domain || bookmark.url)}</p>
      <div class="row-meta">
        <span class="path-pill">${categoryIcon(bookmark.categoryPath[0])}${escapeHtml(bookmark.categoryPath.join(" / "))}</span>
      </div>
      ${tags ? `<div class="bookmark-tags">${tags}</div>` : ""}
    </div>
    <div class="row-actions">
      <a class="visit-link" href="${escapeAttr(bookmark.url)}" target="_blank" rel="noopener">${icon("external-link")}访问</a>
      <button class="ghost-detail" type="button" data-detail="${escapeAttr(bookmark.id)}">详情</button>
    </div>
  </article>`;
}

function bindOpenCard(element) {
  element.addEventListener("click", (event) => {
    if (event.target.closest("button, a, input, select")) return;
    const url = element.dataset.open;
    if (url) window.open(url, "_blank", "noopener");
  });
}

function bindDetailButton(button) {
  button.addEventListener("click", (event) => {
    event.stopPropagation();
    showDetail(button.dataset.detail);
  });
}

function showDetail(id) {
  const bookmark = bookmarks().find((item) => item.id === id);
  if (!bookmark) return;
  const desc = displayDescription(bookmark);
  const tagHtml = bookmark.tags.length ? bookmark.tags.map((tag) => `<span>${escapeHtml(tag)}</span>`).join("") : `<span class="muted">无标签</span>`;
  const displayTitle = bookmark.cleanTitle || bookmark.title;
  const hasStage = Boolean(state.staged[id]);
  $("detailContent").innerHTML = `<div class="modal-title-row">
      <p class="eyebrow">${escapeHtml(bookmark.domain || "书签")}</p>
      <h2>${escapeHtml(displayTitle)}</h2>
      ${bookmark.cleanTitle ? `<p class="muted" style="font-size:0.82em;margin-top:2px">原始标题：${escapeHtml(bookmark.title)}</p>` : ""}
    </div>
    <div class="detail-grid">
      <label>网址</label><a href="${escapeAttr(bookmark.url)}" target="_blank" rel="noopener">${escapeHtml(bookmark.url)}</a>
      <label>分类</label><span>${escapeHtml(bookmark.categoryPath.join(" / "))}</span>
      <label>来源路径</label><span>${escapeHtml(bookmark.sourcePath.join(" / ") || "无")}</span>
      <label>标签</label><div class="detail-tags">${tagHtml}</div>
      <label>状态</label><span>${escapeHtml(statusText(bookmark))}</span>
      <label>描述</label><span>${escapeHtml(desc || "无描述")}</span>
    </div>
    <details class="advanced-edit">
      <summary>本地暂存编辑${hasStage ? "（已暂存）" : ""}</summary>
      <p class="stage-note">这些编辑只保存在当前浏览器中，不会自动写回源文件。请用“调整后的 JSON”导出，下载包含暂存编辑的数据。</p>
      <label>分类路径<input id="detailCategoryInput" value="${escapeAttr(bookmark.categoryPath.join(" / "))}"></label>
      <label>标签<input id="detailTagsInput" value="${escapeAttr(bookmark.tags.join(", "))}"></label>
      <label>描述<input id="detailDescriptionInput" value="${escapeAttr(bookmark.description || "")}"></label>
      <p class="stage-status" id="stageStatus" role="status" aria-live="polite"></p>
      <div class="stage-actions">
        <button type="button" class="quiet-btn" id="saveStageBtn">保存本地暂存</button>
        <button type="button" class="quiet-btn danger-quiet" id="resetStageBtn"${hasStage ? "" : " disabled"}>重置此项</button>
      </div>
    </details>
    <div class="detail-actions">
      <a class="primary-link" href="${escapeAttr(bookmark.url)}" target="_blank" rel="noopener">${icon("external-link")}访问网站</a>
    </div>`;
  $("detailDialog").showModal();
  refreshIcons();
  $("saveStageBtn").addEventListener("click", () => {
    const categoryPath = $("detailCategoryInput").value.split("/").map(cleanLabel).filter(Boolean);
    const tags = cleanTags($("detailTagsInput").value, categoryPath);
    const description = cleanLabel($("detailDescriptionInput").value);
    try {
      state.staged[id] = {
        category_path: categoryPath,
        tags,
        description
      };
      localStorage.setItem("ricoBookmarkStage", JSON.stringify(state.staged));
      $("detailDialog").close();
      renderShell();
      renderAll();
    } catch (error) {
      $("stageStatus").textContent = `保存失败：${error.message || "浏览器无法写入本地暂存编辑"}`;
    }
  });
  $("resetStageBtn").addEventListener("click", () => {
    delete state.staged[id];
    localStorage.setItem("ricoBookmarkStage", JSON.stringify(state.staged));
    $("detailDialog").close();
    renderShell();
    renderAll();
  });
}

function renderInsights() {
  $("insightTabs").querySelectorAll("button").forEach((button) => button.classList.toggle("active", button.dataset.panel === state.insightPanel));
  const panel = $("insightPanels");
  if (state.insightPanel === "summary") panel.innerHTML = renderSummaryInsight();
  if (state.insightPanel === "duplicates") panel.innerHTML = renderDuplicateInsight();
  if (state.insightPanel === "deadlinks") panel.innerHTML = renderDeadlinkInsight();
  if (state.insightPanel === "suggestions") panel.innerHTML = renderSuggestionInsight();
  refreshIcons();
}

function renderSummaryInsight() {
  const dist = distribution(bookmarks());
  return `<div class="insight-grid">
    <article><h3>${icon("bar-chart-3")}分类分布</h3>${miniBars(dist.categories.slice(0, 12))}</article>
    <article><h3>${icon("globe")}域名 Top 12</h3>${miniBars(dist.domains.slice(0, 12))}</article>
  </div>`;
}

function renderDuplicateInsight() {
  const groups = rawPayload.reports?.duplicates || [];
  const byId = Object.fromEntries(bookmarks().map((bookmark) => [bookmark.id, bookmark]));
  if (!groups.length) return `<p class="muted">未发现重复分组，或尚未运行重复检测。</p>`;
  return groups.slice(0, 40).map((group) => `<article class="review-card">
    <h3>${escapeHtml(group.id || "重复分组")} <span>${group.count || group.items?.length || 0}</span></h3>
    ${(group.items || []).map((id) => {
      const item = byId[id];
      return item ? `<p><a href="${escapeAttr(item.url)}" target="_blank" rel="noopener">${escapeHtml(item.title)}</a><small>${escapeHtml(item.url)}</small></p>` : "";
    }).join("")}
  </article>`).join("");
}

function renderDeadlinkInsight() {
  const list = bookmarks().filter(isProblemLink);
  if (!list.length) return `<p class="muted">未发现疑似死链，或尚未运行链接检测。</p>`;
  return list.slice(0, 80).map((bookmark) => `<article class="review-card">
    <h3>${escapeHtml(bookmark.title)} <span>${escapeHtml(statusText(bookmark))}</span></h3>
    <p><a href="${escapeAttr(bookmark.url)}" target="_blank" rel="noopener">${escapeHtml(bookmark.url)}</a></p>
  </article>`).join("");
}

function renderSuggestionInsight() {
  const suggestions = rawPayload.reports?.suggestions || [];
  if (!suggestions.length) return `<p class="muted">暂无分类优化建议。</p>`;
  return `<div class="suggestion-list">${suggestions.map((text) => `<p>${escapeHtml(text)}</p>`).join("")}</div>`;
}

function categoryTree(list) {
  const tree = {};
  list.forEach((bookmark) => {
    const cat = firstPath(bookmark);
    const sub = secondPath(bookmark);
    tree[cat] = tree[cat] || { count: 0, children: {} };
    tree[cat].count += 1;
    if (sub) tree[cat].children[sub] = (tree[cat].children[sub] || 0) + 1;
  });
  return Object.fromEntries(Object.entries(tree).sort((a, b) => b[1].count - a[1].count || a[0].localeCompare(b[0], "zh-Hans-CN")));
}

function distribution(list) {
  const countBy = (getter) => {
    const counts = new Map();
    list.forEach((item) => {
      const key = getter(item);
      if (key) counts.set(key, (counts.get(key) || 0) + 1);
    });
    return [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], "zh-Hans-CN"));
  };
  return {
    categories: countBy(firstPath),
    domains: countBy((item) => item.domain)
  };
}

function miniBars(items) {
  if (!items.length) return `<p class="muted">暂无数据。</p>`;
  const max = Math.max(...items.map(([, count]) => count));
  return `<div class="mini-bars">${items.map(([label, count]) => `<div>
    <span>${escapeHtml(label)}</span><em>${count}</em>
    <i style="--w:${Math.max(8, Math.round((count / max) * 100))}%"></i>
  </div>`).join("")}</div>`;
}

function firstPath(bookmark) {
  return bookmark.categoryPath?.[0] || "未分类";
}

function secondPath(bookmark) {
  return bookmark.categoryPath?.[1] || "";
}

function iconText(bookmark) {
  return (bookmark.domain || bookmark.title || "R").replace(/^www\./, "").slice(0, 1).toUpperCase();
}

function iconStyle(bookmark) {
  const seed = bookmark.domain || bookmark.url || bookmark.title || "rico";
  let hash = 0;
  for (let i = 0; i < seed.length; i += 1) {
    hash = (hash * 31 + seed.charCodeAt(i)) >>> 0;
  }
  const hue = hash % 360;
  return `--site-bg:hsl(${hue} 52% 92%);--site-fg:hsl(${hue} 52% 28%);--site-border:hsl(${hue} 42% 80%)`;
}

function displayDescription(bookmark) {
  const desc = cleanLabel(bookmark.description);
  if (!desc || desc === "待确认资源" || desc === "Pending review") return "";
  if (isCategoryTag(desc, bookmark.categoryPath)) return "";
  return desc;
}

function statusPill(bookmark) {
  if (!bookmark.status || bookmark.status === "ok") return "";
  const cls = isProblemLink(bookmark) ? "danger" : bookmark.status === "redirected" ? "warn" : "";
  return `<span class="status-pill ${cls}">${escapeHtml(bookmark.status)}</span>`;
}

function statusText(bookmark) {
  const status = bookmark.status || "未检测";
  return bookmark.httpStatus ? `${status} · ${bookmark.httpStatus}` : status;
}

function isProblemLink(bookmark) {
  return ["dead", "timeout", "error", "failed"].includes(bookmark.status);
}

function clearFilter(key) {
  if (key === "all") {
    clearFilters();
    return;
  }
  if (key === "query") {
    state.query = "";
    $("searchInput").value = "";
  }
  if (key === "category") {
    state.category = "all";
    state.subcategory = "";
  }
  if (key === "tag") state.tag = "";
  if (key === "domain") {
    state.domain = "all";
    $("domainFilter").value = "all";
  }
  if (key === "status") {
    state.status = "all";
    $("statusFilter").value = "all";
  }
  renderAll();
}

function clearFilters() {
  state.query = "";
  state.category = "all";
  state.subcategory = "";
  state.tag = "";
  state.domain = "all";
  state.status = "all";
  $("searchInput").value = "";
  $("domainFilter").value = "all";
  $("statusFilter").value = "all";
  renderAll();
}

function loadExpandedCategories() {
  try {
    const parsed = JSON.parse(localStorage.getItem("ricoCategoryExpanded") || "{}");
    return parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed : {};
  } catch {
    return {};
  }
}

function saveExpandedCategories() {
  localStorage.setItem("ricoCategoryExpanded", JSON.stringify(state.expandedCategories));
}

function exportData() {
  return {
    ...rawPayload,
    bookmarks: bookmarks().map((bookmark) => {
      const { categoryPath, sourcePath, status, httpStatus, duplicateGroup, reviewStatus, addDate, cleanTitle, ...rest } = bookmark;
      return {
        ...rest,
        clean_title: cleanTitle || "",
        category_path: categoryPath,
        source_folder_path: sourcePath,
        link_status: status || "unknown",
        http_status: httpStatus,
        duplicate_group: duplicateGroup || null,
        review_status: reviewStatus || "kept",
        add_date: addDate || undefined
      };
    })
  };
}

function makeMarkdown(list) {
  const groups = {};
  list.forEach((bookmark) => {
    const key = bookmark.categoryPath.join(" / ");
    groups[key] = groups[key] || [];
    groups[key].push(bookmark);
  });
  let md = `# 书签总览\n\n共 ${list.length} 个书签\n\n`;
  Object.entries(groups).sort((a, b) => b[1].length - a[1].length).forEach(([name, items]) => {
    md += `\n## ${name} (${items.length})\n\n`;
    items.forEach((bookmark) => {
      const desc = bookmark.description ? ` - ${bookmark.description}` : "";
      md += `- [${bookmark.title}](${bookmark.url})${desc}\n`;
    });
  });
  return md;
}

function makeBrowserHtml(list) {
  const now = Math.floor(Date.now() / 1000);
  const tree = {};
  list.forEach((bookmark) => {
    let node = tree;
    bookmark.categoryPath.forEach((part) => {
      node[part] = node[part] || {};
      node = node[part];
    });
    node.__items__ = node.__items__ || [];
    node.__items__.push(bookmark);
  });
  const lines = [
    "<!DOCTYPE NETSCAPE-Bookmark-file-1>",
    '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">',
    "<TITLE>Bookmarks</TITLE>",
    "<H1>Bookmarks</H1>",
    "<DL><p>",
    `  <DT><H3 ADD_DATE="${now}" LAST_MODIFIED="${now}">Rico 书签</H3>`,
    "  <DL><p>"
  ];
  emitBookmarkTree(lines, tree, 2, now);
  lines.push("  </DL><p>", "</DL><p>");
  return lines.join("\n");
}

function emitBookmarkTree(lines, node, depth, now) {
  const pad = "  ".repeat(depth);
  Object.keys(node).filter((key) => key !== "__items__").sort().forEach((name) => {
    lines.push(`${pad}<DT><H3 ADD_DATE="${now}" LAST_MODIFIED="${now}">${escapeHtml(name)}</H3>`);
    lines.push(`${pad}<DL><p>`);
    emitBookmarkTree(lines, node[name], depth + 1, now);
    lines.push(`${pad}</DL><p>`);
  });
  (node.__items__ || []).forEach((bookmark) => {
    lines.push(`${pad}<DT><A HREF="${escapeAttr(bookmark.url)}" ADD_DATE="${bookmark.addDate || now}">${escapeHtml(bookmark.title)}</A>`);
  });
}

function download(name, content, type) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = name;
  link.click();
  URL.revokeObjectURL(url);
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
  }[char]));
}

function escapeAttr(value) {
  return escapeHtml(value);
}
