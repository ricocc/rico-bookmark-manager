# Rico Bookmarks Manager

把杂乱的浏览器书签导出文件，变成一个干净、可搜索的本地导航站——同时附带结构化数据、Markdown 总览和审阅报告。既是  skill，也是一套零依赖、只用 Python 标准库的 CLI。

English documentation: [README.md](README.md)

![ease 主题](screenshot/ease.jpeg)

## 效果预览

生成的导航站内置 5 个主题——`ease`、`kami`、`minimal-mono`、`retro-blue`、`ui`：

| | | |
| :---: | :---: | :---: |
| ![ease 主题](screenshot/ease.jpeg)<br>`ease`（默认） | ![kami 主题](screenshot/kami.jpeg)<br>`kami` | ![minimal-mono 主题](screenshot/mono.jpeg)<br>`minimal-mono` |
| ![retro-blue 主题](screenshot/retro.jpeg)<br>`retro-blue` | ![ui 主题](screenshot/ui.jpeg)<br>`ui` | |

## 能做什么

- 把浏览器书签导出文件解析成结构化 `bookmarks.json`。
- 分析文件夹结构、分类分布、重复链接和低置信度项目。
- 按 `source`（原始）、`optimized`（优化）或 `hybrid`（混合）模式整理书签。
- 在启用网络检查时检测死链。
- 用新的书签导出和旧数据做增量更新。
- 导出 Markdown 总览和浏览器可导入的 HTML（可再导回浏览器）。
- 生成本地静态导航站，支持搜索、筛选、报告、导出、主题和本地暂存编辑。

## 安装

按以下三种方式之一安装为 Claude Code skill。**仓库根目录就是 skill 本身**，因此可以直接放进 skills 目录。

```bash
# 方式一：npx 一键安装（推荐）
npx skills add https://github.com/ricocc/rico-bookmark-manager.git

# 方式二：git clone 到 Claude Code 的 skills 目录
git clone https://github.com/ricocc/rico-bookmark-manager.git ~/.claude/skills/rico-bookmark-manager

# 方式三：下载 ZIP 解压到 skills 目录
#   macOS/Linux: ~/.claude/skills/rico-bookmark-manager/
#   Windows:     %USERPROFILE%\.claude\skills\rico-bookmark-manager\
```

安装后的目录结构：

```text
~/.claude/skills/rico-bookmark-manager/
├── SKILL.md
├── scripts/rico_bookmarks_manager.py
├── assets/
└── references/
```

### 验证安装

重启 Claude Code 或重新加载 skills 后，在对话里输入：

```text
/rico-bookmark-manager
```

或者直接说一句 “rico，整理我的书签”。如果 skill 被激活，说明安装成功。

## 在 AI 中使用（推荐）

装好之后，**最自然的用法是在对话里用自然语言让 AI 调用**，不需要记命令。两种方式：

```text
# 方式 A：斜杠显式调用
/rico-bookmark-manager 帮我整理 bookmarks.html，并生成导航站

# 方式 B：对话中自然触发
rico，帮我整理书签
```

常见场景（你说一句 → 背后会发生什么）：

| 你可以这样说 | 会发生什么 |
| --- | --- |
| “rico，整理我的书签并生成导航站” | 解析你的书签 HTML，分类整理，生成本地导航站。 |
| “帮我对浏览器书签去重、检查死链” | 找出重复项和失效链接，产出审阅报告。 |
| “换成 retro-blue 主题重新生成导航站” | 用指定主题重建站点。 |
| “把这份新导出的书签增量合并进来，先预览” | 以 `--dry-run` 预览增量更新，保留已有分类。 |
| “整理好后导出成能导回浏览器的文件” | 生成 `bookmarks_import.html`，可直接导回浏览器（见下）。 |
| “我想存个书签” | 不触发（没有明确的管理动作）。 |

需要可复现、可脚本化的批处理时，见下方 [命令行用法（进阶）](#命令行用法进阶)。

## 快速开始

**第一步**：从浏览器把书签导出为 HTML 文件。

**第二步**：运行完整流程：

```bash
python scripts/rico_bookmarks_manager.py all \
  --input bookmarks.html \
  --output rico-bookmarks
```

**第三步**：在浏览器打开 `rico-bookmarks/site/index.html`，即可搜索、筛选、查看详情、暂存调整、查看报告和导出。

这一步会生成：

```text
rico-bookmarks/
├── site/                    # 本地静态书签导航站
├── data/bookmarks.json      # 结构化书签数据
├── reports/*.md             # 重复、死链、建议、分布报告
├── categories/*.md          # 按分类生成的 Markdown
├── 书签总览.md              # Markdown 总览
└── bookmarks_import.html    # 浏览器可导入 HTML
```

### 导回浏览器

整理后的分类会被还原成浏览器里的书签**文件夹层级**。`all` 已自动生成 `bookmarks_import.html`（也可单独运行 `export-html` 生成），导回方式：

- **Chrome / Edge**：书签管理器 → 右上角菜单 → 导入书签 → 选择该 HTML。
- **Firefox**：书签管理器（书签库）→ 导入和备份 → 从 HTML 导入书签。

> 提醒：浏览器导入是**新增**而非替换——它会作为一个新文件夹加入，不会删除你原有的书签。若想要干净替换，请先手动删除旧书签，或在测试 profile 里验证。

## 命令行用法（进阶）

需要可复现、可脚本化或调试时，直接用 CLI：

```bash
# 分析结构和重复项（不整理文件）
python scripts/rico_bookmarks_manager.py analyze \
  --input bookmarks.html \
  --output rico-bookmarks

# 使用混合模式和三级分类整理
python scripts/rico_bookmarks_manager.py organize \
  --input bookmarks.html \
  --output rico-bookmarks \
  --mode hybrid \
  --levels 3

# 从已有数据只重建导航站
python scripts/rico_bookmarks_manager.py manager \
  --data rico-bookmarks/data/bookmarks.json \
  --output rico-bookmarks/site

# 使用指定主题生成导航站
python scripts/rico_bookmarks_manager.py manager \
  --data rico-bookmarks/data/bookmarks.json \
  --theme retro-blue \
  --output rico-bookmarks/site

# 从已有数据生成可导回浏览器的 HTML
python scripts/rico_bookmarks_manager.py export-html \
  --data rico-bookmarks/data/bookmarks.json \
  --output rico-bookmarks

# 预览增量更新（不写入）
python scripts/rico_bookmarks_manager.py update \
  --input new_bookmarks.html \
  --existing rico-bookmarks/data/bookmarks.json \
  --output rico-bookmarks \
  --dry-run

# 查看内置主题
python scripts/rico_bookmarks_manager.py themes
```

## 主题

用 `--theme` 选择导航站外观（默认 `ease`）：

| 主题 | 说明 |
| --- | --- |
| `ease` | 默认主题。纸感目录风格，矿物蓝强调色和安静界面。 |
| `kami` | 暖色画布、象牙纸面、墨蓝强调色、serif 层级。 |
| `minimal-mono` | 深色黑白灰界面，暖灰底色。 |
| `retro-blue` | 暖纸面、编辑感蓝色标题和克制金色点缀。 |
| `ui` | 单色 Swiss 风格，强调边框和组件结构。 |

内置主题位于 `assets/themes/<theme-id>/`（含 `theme.json`、`theme.css`、`DESIGN.md`）。生成时优先复制 `theme.css`，缺失则从 `theme.json` 生成。自定义 `--design DESIGN.md` 会在构建时生成 `theme.css`。

`kami` 主题基于 Kami 的公开设计语言（[官网](https://kami.tw93.fun/index-zh.html)、[仓库](https://github.com/tw93/kami)）：暖色画布、象牙纸面、墨蓝强调色、serif 层级和轻微 ring 阴影。

## 导航站

生成的静态站点包含：

- 全局搜索：标题、URL、域名、描述、标签、来源路径、分类路径。
- 分类、二级分类、标签、域名和链接状态筛选。
- 卡片和列表两种视图。
- 书签卡片，支持访问和详情。
- 详情弹窗，包含 URL、来源文件夹、分类、标签、状态、描述和本地暂存调整。
- 指南弹窗，说明页面如何使用。
- 报告弹窗，包含统计、重复、死链和建议。
- JSON、Markdown 和浏览器导入 HTML 导出。

详情里的调整保存在当前浏览器的 `localStorage`，属于本地暂存，不会直接写入 `bookmarks.json` 或浏览器 profile。站内 JSON 导出会包含这些暂存的分类、标签和描述调整，你可以再主动替换源数据。

## CLI 参考

```bash
python scripts/rico_bookmarks_manager.py <command> [options]
```

| 命令 | 用途 |
| --- | --- |
| `analyze` | 解析书签 HTML，输出结构、重复、分布和建议。 |
| `organize` | 解析并按 `source`、`optimized` 或 `hybrid` 分类。 |
| `export-html` | 从已有 `bookmarks.json` 生成浏览器可导入 HTML。 |
| `export-md` | 从已有数据生成总览、分类文件和报告。 |
| `manager` | 从已有数据生成本地静态导航站。 |
| `update` | 把新的书签 HTML 增量合并到已有 `bookmarks.json`。 |
| `all` | 执行整理 + Markdown 导出 + 浏览器 HTML 导出 + 导航站生成。 |
| `themes` | 查看内置导航站主题。 |

| 参数 | 用于 | 说明 |
| --- | --- | --- |
| `--input bookmarks.html` | `analyze`, `organize`, `update`, `all` | 书签 HTML 输入，通常来自浏览器导出。 |
| `--output rico-bookmarks` | 多数命令 | 输出目录。 |
| `--data path/to/bookmarks.json` | `manager`, `export-md`, `export-html` | 已有结构化书签数据。 |
| `--existing path/to/bookmarks.json` | `update` | 用于增量更新的旧数据。 |
| `--mode source\|optimized\|hybrid` | `analyze`, `organize`, `all`, `update` | 分类策略。 |
| `--levels 1\|2\|3` | `analyze`, `organize`, `all`, `update` | 最大分类层级。 |
| `--check-links` | `analyze`, `organize`, `all` | 执行网络链接检测。 |
| `--no-network` | `analyze`, `organize`, `all` | 跳过网络检测。 |
| `--dry-run` | `update` | 预览增量更新，不写入数据文件。 |
| `--theme kami\|ease\|minimal-mono\|retro-blue\|ui` | `manager`, `all` | 内置导航站主题，默认 `ease`。 |
| `--design DESIGN.md` | `manager`, `all` | 使用自定义设计参考生成主题。 |

## 增量更新

增量更新需要一个新的书签 HTML 导出，加上一个已有的 `bookmarks.json`：

```bash
python scripts/rico_bookmarks_manager.py update \
  --input new_bookmarks.html \
  --existing rico-bookmarks/data/bookmarks.json \
  --output rico-bookmarks \
  --dry-run
```

更新流程按标准化 URL 匹配旧书签，保留已有人工审阅字段，只分类新增项目，并写出 `reports/增量更新.md`。检查行为时先使用 `--dry-run`。

## 环境要求

- Python 3.8+
- 不需要第三方 Python 依赖
- 一个书签输入来源，通常是浏览器导出的 Netscape HTML
- Node.js 只用于开发时可选的 JavaScript 语法检查

## 给 AI/Agent

把这个 skill 当作通用执行契约，而不是某个 agent 产品的专属集成——任何能读文件、跑 Python、写输出的运行时都能执行。

**如何触发。** 作为 skill，它在以下情况激活：(1) 说 `rico` 加书签请求；或 (2) 表达明确具体的书签管理任务（整理、去重、查死链、导出、增量更新、生成导航站）。只是模糊地随口提一句“书签”不会触发。具体台词见上方 [在 AI 中使用](#在-ai-中使用推荐)。

**执行流程。** 理解目标 → 确认或请求输入来源 → 选择最低风险路径 → 运行 CLI → 说明读取了什么、写入了什么、是否访问了浏览器数据。

**输入来源**，从最安全到能力最强：

| 层级 | 输入来源 | 适用场景 |
| --- | --- | --- |
| Level 1 | 浏览器导出的 `bookmarks.html` | 默认、最稳定，适合完整整理、分析和增量更新。 |
| Level 2 | 已有 `bookmarks.json` | 重建导航站、导出 Markdown/HTML，或合并新的导出文件。 |
| Level 3 | Agent 生成的中间文件 | Agent 获得用户授权且环境允许，安全地把浏览器数据导出成标准输入文件。 |
| Level 4 | 浏览器自动化或当前标签页采集 | 属于 Agent 外部能力，不是固定 CLI 接口；必须有明确用户意图和授权。 |

CLI 的公开接口是文件型的（`--input`、`--data`、`--existing`）。如果通过 profile 访问或自动化获取了浏览器数据，先转换成上述文件之一再调用 CLI。不确定时，优先让用户提供浏览器导出的 HTML。不要直接修改浏览器 profile 文件。

## 安全说明

- 不自动删除书签。
- 不直接修改 Chrome、Edge、Firefox 或其他浏览器 profile 文件。
- 如果 Agent 可以访问浏览器数据，先获得用户授权，并生成中间输入文件。
- 增量更新写入前先使用 `--dry-run`。
- 更新时保留人工编辑过的分类。
- 导航站详情编辑默认只是本地暂存，除非用户主动导出并替换源数据。

## 项目结构

```text
rico-bookmark-manager/
├── SKILL.md
├── scripts/
│   └── rico_bookmarks_manager.py
├── assets/
│   ├── bookmark-manager-template/
│   └── themes/
├── references/
│   ├── cli.md
│   ├── design-md.md
│   ├── link-checking.md
│   ├── manager-spec.md
│   ├── schema.md
│   ├── taxonomy.md
│   └── workflow.md
└──agents/
```

---

## 我的其他开源项目

- **Rico Skills** - 我的 skill 系列：[https://github.com/ricocc/rico-skills](https://github.com/ricocc/rico-skills)
- **SaaS Template** - 开源：[https://github.com/ricocc/ricoui-saas-template](https://github.com/ricocc/ricoui-saas-template)
- **Portfolio Template** - 开源：[https://github.com/ricocc/ricoui-portfolio](https://github.com/ricocc/ricoui-portfolio)
- **Blog Template** - 开源：[https://github.com/ricocc/public-portfolio-site](https://github.com/ricocc/public-portfolio-site)

## 关于作者

我是 Rico <a href="https://x.com/ricouii" target="_blank">X (@ricouii)</a>，网页/UI 设计师，热衷于做些有趣和创意的作品。拥有 UI/UX 设计工作经验，目前专注于网页设计和视觉落地，以及开发项目探索。

可以添加我的微信，交个朋友：

<img src="https://ricoui.com/assets/wechat.png" alt="ricocc-wechat" width="280" height="auto" style="display:inline-block;margin:12px;">

我平时在博客 <a href="https://ricoui.com/" target="_blank">Rico's Blog</a> 更新内容。也可以关注我的小红书 [@Rico的设计漫想](https://www.xiaohongshu.com/user/profile/5f2b6903000000000101f51f)。

## 💜 支持作者

如果觉得有所帮助的话，一点点支持，感谢！

<img src="https://ricoui.com/assets/wechat-qr.jpg" alt="ricocc-wechat" width="280" height="auto" style="display:inline-block;margin:12px;">


---

⭐ 如果这个工具帮你整理好了书签，欢迎点一个 Star。
