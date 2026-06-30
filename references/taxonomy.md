# Default Rico Taxonomy

The default taxonomy starts from the user's current bookmark export and can be extended during each run.

## 一级分类

- AI
- 前端
- 设计
- 互联网
- 工具产品
- 博客
- 学习教程
- 其他

## 二级分类

### AI
AI工具, AI模型, AI平台, AI基础设施, AI框架, AI编程, AI绘画, AI视频, AI音频, AI教程, AI论文, AI文档, AI博客, AI媒体, AI其他

### 前端
前端框架, UI组件库, 构建工具, CSS工具, CSS框架, 前端工具, 前端部署, 前端文档, 前端博客, 前端教程, 前端语言, 前端其他

### 设计
设计工具, 设计灵感-web, 设计灵感-app, 配色工具, 图标资源, 字体资源, 设计素材, 设计规范, 设计教程, 创意工作室, 3D与交互, 作品集, 品牌官网, 设计博客, 设计其他

### 工具产品
效率工具, 知识管理, 开发工具, 部署工具, 云服务, 代码托管, 数据库, 后端服务, 搜索工具, 监控工具, 容器工具, DevOps工具, 安全工具, 浏览器, 建站工具, 包管理, CDN工具, 域名服务, 工具产品其他

### 互联网
产品发现, 创业社区, 科技媒体, 技术媒体, SEO工具, 分析工具, 营销工具, 电商工具, 支付工具, Web3与加密, 互联网其他

### 博客
博客平台, 技术博客, 个人博客, 博客其他

### 学习教程
编程学习, 在线课程, 前端教程, 算法学习, 开发教程, 设计教程, AI教程, 学习教程其他

### 其他
待确认, 低置信度, 未归类资源, 其他其他

## Matching Priority

1. Exact domain rules.
2. Strong keyword rules in title, URL, domain, and source folder.
3. Source folder hints.
4. Heuristic inference (`infer_category`) that names a category for content the static taxonomy misses — creative studios, 3D/interactive, portfolios, Web3, brand/product showcase sites. Inferred items carry lower confidence and the weakest inferences are flagged `low_confidence` for review.
5. Fallback to `其他/待确认` only when nothing fits.

## The built-in taxonomy is only a reference

The default categories above are a starting point, not a ceiling. When a real export is dominated by a domain the taxonomy doesn't cover (for example creative agencies, 3D sites, portfolios, Web3 projects, or a niche industry), do not silently dump those bookmarks into `其他/待确认`. Instead:

- Inspect the preflight analysis (`reports/统计分布.md`) to see what is falling into `其他`.
- Name appropriate categories yourself and extend the run: add matching `DOMAIN_RULES`, `TAXONOMY` keywords, or signals in `infer_category` (`scripts/rico_bookmarks_manager.py`) so the content lands in a meaningful bucket.
- Prefer specific, lower-risk signals (exact domains, TLDs, unambiguous title keywords) over very broad ones to avoid false positives.
- Keep genuinely ambiguous items in `其他/待确认` rather than inventing a misleading category — a smaller, honest `其他` is better than a noisy guess.
