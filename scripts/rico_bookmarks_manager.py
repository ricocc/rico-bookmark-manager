#!/usr/bin/env python3
"""Rico Bookmarks Manager.

Standard-library CLI for browser-exported Netscape bookmark HTML files.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import copy
import hashlib
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import shutil
import sys
import time
from datetime import datetime
from urllib import request, error
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


TRACKING_PARAMS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "utm_id",
    "fbclid",
    "gclid",
    "yclid",
    "mc_cid",
    "mc_eid",
    "igshid",
    "spm",
}

THEME_IDS = ("kami", "ease", "minimal-mono", "retro-blue", "ui")

DOMAIN_RULES = {
    "openai.com": ("AI", "AI模型", "OpenAI / ChatGPT"),
    "chat.openai.com": ("AI", "AI工具", "ChatGPT"),
    "platform.openai.com": ("AI", "AI平台", "OpenAI API"),
    "anthropic.com": ("AI", "AI模型", "Anthropic / Claude"),
    "claude.ai": ("AI", "AI工具", "Claude"),
    "huggingface.co": ("AI", "AI平台", "Hugging Face"),
    "midjourney.com": ("AI", "AI绘画", "AI image generation"),
    "runwayml.com": ("AI", "AI视频", "AI video generation"),
    "suno.com": ("AI", "AI音频", "AI music generation"),
    "cursor.com": ("AI", "AI编程", "AI code editor"),
    "cursor.sh": ("AI", "AI编程", "AI code editor"),
    "react.dev": ("前端", "前端框架", "React documentation"),
    "vuejs.org": ("前端", "前端框架", "Vue documentation"),
    "nextjs.org": ("前端", "前端框架", "Next.js framework"),
    "vitejs.dev": ("前端", "构建工具", "Vite build tool"),
    "tailwindcss.com": ("前端", "CSS框架", "Tailwind CSS"),
    "ui.shadcn.com": ("前端", "UI组件库", "shadcn/ui"),
    "developer.mozilla.org": ("前端", "前端文档", "MDN Web Docs"),
    "figma.com": ("设计", "设计工具", "Figma"),
    "dribbble.com": ("设计", "设计灵感-web", "Design inspiration"),
    "behance.net": ("设计", "设计灵感-web", "Design portfolio"),
    "awwwards.com": ("设计", "设计灵感-web", "Website inspiration"),
    "mobbin.com": ("设计", "设计灵感-app", "App UI inspiration"),
    "coolors.co": ("设计", "配色工具", "Color palette tool"),
    "lucide.dev": ("设计", "图标资源", "Lucide icons"),
    "github.com": ("工具产品", "代码托管", "GitHub"),
    "gitlab.com": ("工具产品", "代码托管", "GitLab"),
    "vercel.com": ("工具产品", "部署工具", "Vercel"),
    "netlify.com": ("工具产品", "部署工具", "Netlify"),
    "cloudflare.com": ("工具产品", "CDN工具", "Cloudflare"),
    "notion.so": ("工具产品", "效率工具", "Notion"),
    "obsidian.md": ("工具产品", "知识管理", "Obsidian"),
    "medium.com": ("博客", "博客平台", "Medium"),
    "dev.to": ("博客", "博客平台", "DEV Community"),
    "hashnode.com": ("博客", "博客平台", "Hashnode"),
    "freecodecamp.org": ("学习教程", "编程学习", "freeCodeCamp"),
    "coursera.org": ("学习教程", "在线课程", "Coursera"),
    "udemy.com": ("学习教程", "在线课程", "Udemy"),
    "leetcode.com": ("学习教程", "算法学习", "LeetCode"),
    "producthunt.com": ("互联网", "产品发现", "Product Hunt"),
    "news.ycombinator.com": ("互联网", "科技媒体", "Hacker News"),
    "techcrunch.com": ("互联网", "科技媒体", "TechCrunch"),
    "36kr.com": ("互联网", "科技媒体", "36Kr"),
    "webflow.io": ("设计", "设计灵感-web", "Webflow 展示站点"),
    "tympanus.net": ("前端", "前端博客", "Codrops 前端教程"),
    "cosmos.so": ("设计", "设计灵感-web", "Cosmos 灵感库"),
    "are.na": ("设计", "设计灵感-web", "Are.na"),
    "read.cv": ("设计", "作品集", "Read.cv 设计师档案"),
    "cargo.site": ("设计", "作品集", "Cargo 作品集"),
    "vogue.it": ("设计", "品牌官网", "Vogue 品牌内容"),
    "rejouice.io": ("设计", "创意工作室", "Rejouice 创意代理商"),
    "thedigitalpanda.com": ("设计", "创意工作室", "The Digital Panda 创意工作室"),
    "worldcoin.org": ("互联网", "Web3与加密", "Worldcoin 加密项目"),
    "gumroad.com": ("互联网", "电商工具", "Gumroad 数字商品"),
    "cash.app": ("互联网", "支付工具", "Cash App"),
    "tilda.ws": ("工具产品", "建站工具", "Tilda 建站平台"),
    # --- Extensions for this dataset (exact domains, low false-positive) ---
    "zhuanlan.zhihu.com": ("博客", "技术博客", "知乎专栏"),
    "juejin.cn": ("前端", "前端博客", "掘金技术社区"),
    "uisdc.com": ("设计", "设计教程", "优设 设计教程"),
    "s.muz.li": ("设计", "设计灵感-web", "Muzli 设计灵感"),
    "zhihu.com": ("博客", "个人博客", "知乎"),
    "zcool.com.cn": ("设计", "作品集", "站酷 设计作品"),
    "cowtransfer.com": ("工具产品", "文件传输", "奶牛快传 文件传输"),
    "zapyatransfer.com": ("工具产品", "文件传输", "快牙 文件传输"),
    "smallpdf.com": ("工具产品", "效率工具", "Smallpdf PDF 工具"),
    "freeconvert.com": ("工具产品", "效率工具", "FreeConvert 文件转换"),
}

TAXONOMY = {
    "AI": {
        "AI工具": ["chatgpt", "claude", "kimi", "perplexity", "poe", "copilot", "jasper"],
        "AI模型": ["openai", "anthropic", "huggingface", "deepseek", "zhipu", "moonshot", "llm", "gpt"],
        "AI平台": ["dify", "coze", "replicate", "together", "modal", "wandb", "mlflow"],
        "AI基础设施": ["vector", "embedding", "pinecone", "weaviate", "qdrant", "milvus"],
        "AI框架": ["tensorflow", "pytorch", "keras", "onnx", "langchain", "llamaindex"],
        "AI编程": ["cursor", "copilot", "tabnine", "codeium", "windsurf", "aider", "cline"],
        "AI绘画": ["midjourney", "stable diffusion", "dall-e", "civitai", "comfyui", "leonardo"],
        "AI视频": ["runway", "pika", "sora", "kling", "heygen", "synthesia"],
        "AI音频": ["suno", "udio", "elevenlabs", "tts", "voice"],
        "AI教程": ["deeplearning.ai", "fast.ai", "karpathy", "machine learning course"],
    },
    "前端": {
        "前端框架": ["react", "vue", "angular", "svelte", "solid", "next.js", "nuxt", "astro"],
        "UI组件库": ["antd", "element", "chakra", "mantine", "radix", "shadcn", "bootstrap", "arco"],
        "构建工具": ["vite", "webpack", "rollup", "parcel", "esbuild", "babel", "turbopack"],
        "CSS工具": ["sass", "less", "postcss", "unocss", "css modules", "styled-components"],
        "CSS框架": ["tailwind", "bootstrap", "bulma"],
        "前端工具": ["eslint", "prettier", "storybook", "jest", "vitest", "playwright", "cypress"],
        "前端部署": ["vercel", "netlify", "cloudflare pages", "surge", "github pages"],
        "前端文档": ["developer.mozilla", "web.dev", "w3c", "whatwg"],
        "前端博客": ["css-tricks", "smashingmagazine", "alistapart"],
        "前端教程": ["javascript.info", "javascript30", "frontendmasters", "fullstackopen"],
        "前端语言": ["javascript", "typescript", "webassembly"],
    },
    "设计": {
        "设计工具": ["figma", "sketch", "canva", "framer", "webflow", "miro", "excalidraw", "spline", "tilda"],
        "设计灵感-web": ["dribbble", "behance", "awwwards", "siteinspire", "lapa", "land-book", "webflow", "showcase", "inspiration", "bestproductsites", "godly", "httpster"],
        "设计灵感-app": ["mobbin", "uisources", "scrnshts", "appshots"],
        "配色工具": ["coolors", "colorhunt", "palette", "gradient", "color.adobe"],
        "图标资源": ["heroicons", "feather", "tabler", "lucide", "iconify", "fontawesome", "iconfont"],
        "字体资源": ["google fonts", "fontpair", "typescale", "fontsquirrel", "typeface", "typography", "type foundry", "grilli", "gt america"],
        "设计素材": ["unsplash", "pexels", "pixabay", "undraw", "storyset"],
        "设计规范": ["material.io", "apple design", "human interface", "design system"],
        "设计教程": ["learnui", "designcode", "uxdesign"],
        "创意工作室": ["agency", "studio", "creative", "branding", "digital agency", "interactive design", "design agency", "production studio", "visual language", "visual design", "designs", "工作室", "创意"],
        "3D与交互": ["3d", "three.js", "threejs", "webgl", "webxr", "real-time", "realtime", "motion", "interactive", "immersive", "parallax", "animation"],
        "3D素材": ["blender", "c4d", "houdini", "cinema 4d", "三维素材", "三维", "贴图", "材质", "模型下载", "hdri", "mixamo", "cg教程", "cg网", "blender插件", "三维素材库"],
        "作品集": ["portfolio", "designer", "artist", "illustrator", "photographer", "freelance", "personal site", "作品集"],
        "品牌官网": ["official site", "official movie", "brand experience", "product site", "官网"],
    },
    "工具产品": {
        "效率工具": ["notion", "linear", "clickup", "asana", "trello", "slack", "todoist", "临时邮箱", "白嫖", "在线工具", "卡片生成", "图片压缩", "dll", "sticky", "pdf", "格式转换", "文件转换", "转换压缩", "电子书"],
        "内容生产": ["markdown", "公众号排版", "排版", "文字卡片", "mdnice", "doocs", "fireflycard", "md2wechat", "metatag", "screenshot", "微信编辑器", "公众号编辑器"],
        "下载工具": ["扒站", "去水印", "视频下载", "downloader", "磁力下载", "webcopier", "种子下载", "opengraph"],
        "文件传输": ["传文件", "文件传输", "快传", "跨平台文件", "文件分享", "大文件传输", "拷贝兔", "send large file", "airdrop"],
        "知识管理": ["obsidian", "logseq", "roam", "readwise", "pocket", "flomo", "yuque"],
        "开发工具": ["postman", "insomnia", "sentry", "swagger", "logrocket", "ci/cd", "pipeline", "code hosting", "open-source"],
        "部署工具": ["vercel", "netlify", "render", "railway", "fly.io", "heroku"],
        "云服务": ["aws", "azure", "google cloud", "digitalocean", "vultr", "linode"],
        "代码托管": ["github", "gitlab", "bitbucket", "gitea", "codeberg"],
        "数据库": ["postgres", "mysql", "mongodb", "redis", "sqlite", "neon", "planetscale"],
        "后端服务": ["supabase", "firebase", "appwrite", "strapi", "directus", "pocketbase"],
        "搜索工具": ["algolia", "meilisearch", "typesense", "duckduckgo"],
        "监控工具": ["grafana", "prometheus", "datadog", "newrelic", "sentry"],
        "容器工具": ["docker", "kubernetes", "podman"],
        "DevOps工具": ["terraform", "ansible", "jenkins", "github actions", "gitlab ci"],
        "安全工具": ["1password", "bitwarden", "proton", "vpn"],
        "浏览器": ["arc", "brave", "firefox", "vivaldi", "opera"],
        "建站工具": ["squarespace", "wix", "webflow", "framer", "wordpress", "carrd"],
        "包管理": ["npm", "pypi", "rubygems", "crates", "packagist"],
        "CDN工具": ["cloudflare", "fastly", "jsdelivr"],
        "域名服务": ["namecheap", "godaddy", "domains"],
    },
    "互联网": {
        "产品发现": ["producthunt", "betalist", "betapage"],
        "创业社区": ["indiehackers", "ycombinator"],
        "科技媒体": ["techcrunch", "theverge", "wired", "36kr", "sspai", "hacker news"],
        "技术媒体": ["infoq", "geekpark", "leiphone"],
        "SEO工具": ["moz", "ahrefs", "semrush", "screaming frog", "seo", "traffic"],
        "分析工具": ["amplitude", "mixpanel", "posthog", "plausible", "umami", "hotjar"],
        "营销工具": ["mailchimp", "hubspot", "convertkit", "出海", "推广运营", "google ads", "google analytics", "追踪", "ga小站"],
        "影视娱乐": ["电影", "影视", "动漫", "追剧", "磁力", "torrent", "1080p", "bt下载", "迅雷下载", "网盘资源", "高清mp4", "bt种子"],
        "电商工具": ["shopify", "woocommerce", "gumroad", "lemonsqueezy", "电商", "带货", "小店", "直播电商"],
        "支付工具": ["stripe", "paypal", "wise", "paddle", "支付", "payment"],
        "Web3与加密": ["web3", "crypto", "defi", "nft", "blockchain", "token", " dao", "ethereum", "bitcoin", "wallet", "smart contract", "yacht club", "coingecko", "opensea", "protocol", "metamask"],
    },
    "博客": {
        "博客平台": ["medium", "dev.to", "hashnode", "substack", "ghost", "wordpress", "gitbook"],
        "技术博客": ["css-tricks", "smashingmagazine", "alistapart", "web.dev/blog"],
        "个人博客": ["github.io", "gitlab.io", "vercel.app", "netlify.app", "pages.dev", ".me", ".blog"],
    },
    "学习教程": {
        "编程学习": ["freecodecamp", "codecademy", "pluralsight", "scrimba", "bootcamp", "coding"],
        "在线课程": ["coursera", "udemy", "edx", "udacity", "khanacademy"],
        "前端教程": ["frontendmasters", "javascript.info", "javascript30", "fullstackopen"],
        "算法学习": ["leetcode", "hackerrank", "codewars", "exercism", "codeforces"],
        "开发教程": ["roadmap.sh", "devhints", "tldr", "learngitbranching"],
        "设计教程": ["learnui", "designcode", "uxdesign"],
        "AI教程": ["deeplearning.ai", "fast.ai", "karpathy"],
    },
}


class BookmarkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.bookmarks = []
        self.folder_stack = []
        self.dl_stack = []
        self.pending_folder = None
        self.capture_h3 = False
        self.h3_text = []
        self.capture_a = False
        self.a_text = []
        self.a_attrs = {}

    def handle_starttag(self, tag, attrs):
        attrs = {k.lower(): v for k, v in attrs}
        if tag == "h3":
            self.capture_h3 = True
            self.h3_text = []
        elif tag == "dl":
            if self.pending_folder:
                self.folder_stack.append(self.pending_folder)
                self.dl_stack.append(True)
                self.pending_folder = None
            else:
                self.dl_stack.append(False)
        elif tag == "a":
            href = attrs.get("href", "")
            if href.startswith(("http://", "https://")):
                self.capture_a = True
                self.a_text = []
                self.a_attrs = attrs

    def handle_endtag(self, tag):
        if tag == "h3" and self.capture_h3:
            name = " ".join("".join(self.h3_text).split())
            self.pending_folder = name or None
            self.capture_h3 = False
        elif tag == "dl":
            if self.dl_stack:
                had_folder = self.dl_stack.pop()
                if had_folder and self.folder_stack:
                    self.folder_stack.pop()
        elif tag == "a" and self.capture_a:
            title = " ".join("".join(self.a_text).split())
            url = self.a_attrs.get("href", "")
            if url:
                add_date = self.a_attrs.get("add_date")
                self.bookmarks.append(
                    {
                        "title": title or url,
                        "url": url,
                        "add_date": add_date,
                        "source_folder_path": list(self.folder_stack),
                    }
                )
            self.capture_a = False
            self.a_attrs = {}

    def handle_data(self, data):
        if self.capture_h3:
            self.h3_text.append(data)
        if self.capture_a:
            self.a_text.append(data)


def now_iso():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def backup_file(path):
    path = Path(path)
    if path.exists():
        stamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup = path.with_name(f"{path.name}.bak-{stamp}")
        shutil.copy2(path, backup)
        return str(backup)
    return None


def get_domain(url):
    try:
        netloc = urlsplit(url).netloc.lower()
        if netloc.startswith("www."):
            netloc = netloc[4:]
        return netloc
    except Exception:
        return ""


def normalize_url(url):
    try:
        parts = urlsplit(url.strip())
        scheme = parts.scheme.lower()
        netloc = parts.netloc.lower()
        if netloc.startswith("www."):
            netloc = netloc[4:]
        path = re.sub(r"/+$", "", parts.path) or "/"
        query_pairs = [
            (k, v)
            for k, v in parse_qsl(parts.query, keep_blank_values=True)
            if k.lower() not in TRACKING_PARAMS and not k.lower().startswith("utm_")
        ]
        query = urlencode(query_pairs, doseq=True)
        return urlunsplit((scheme, netloc, path, query, ""))
    except Exception:
        return url.strip()


def stable_id(text):
    return hashlib.sha1(text.encode("utf-8", errors="ignore")).hexdigest()[:16]


def parse_bookmark_html(path):
    parser = BookmarkParser()
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    parser.feed(text)
    bookmarks = []
    for raw in parser.bookmarks:
        canonical = normalize_url(raw["url"])
        domain = get_domain(raw["url"])
        bookmarks.append(
            {
                "id": stable_id(canonical),
                "title": raw["title"],
                "url": raw["url"],
                "canonical_url": canonical,
                "final_url": "",
                "domain": domain,
                "source_folder_path": raw.get("source_folder_path", []),
                "source_category_path": raw.get("source_folder_path", []),
                "optimized_category_path": [],
                "category_path": [],
                "tags": [],
                "description": "",
                "http_status": None,
                "link_status": "unknown",
                "duplicate_group": None,
                "confidence": 0.0,
                "review_status": "kept",
                "add_date": raw.get("add_date"),
            }
        )
    return bookmarks


def match_domain(domain):
    for key, value in DOMAIN_RULES.items():
        if domain == key or domain.endswith("." + key) or key in domain:
            return value
    return None


TECHNIQUE_KEYWORDS = {
    "3d", "2d", "scroll", "webgl", "webxr", "three.js", "threejs",
    "motion", "animation", "interactive", "parallax", "immersive",
    "responsive", "minimal", "retro", "vintage", "brutalist",
    "glassmorphism", "neumorphism", "skeuomorphism",
    "illustration", "illus", "handwrite", "typography", "calligraphy",
    "photography", "photo", "cinematic", "video", "audio",
    "web3", "crypto", "nft", "defi", "blockchain",
    "ai", "ml", "generative", "procedural",
    "css", "svg", "canvas", "shader", "particle",
    "react", "vue", "angular", "svelte", "next.js", "nuxt",
    "tailwind", "sass", "figma", "framer", "webflow",
    "saas", "api", "sdk", "open-source", "no-code", "low-code",
}

DESIGN_NAME_TOKENS = {"design", "studio", "creative", "visual", "brand", "pixel", "graphics", "motion"}
DESIGN_TLDS = {"design", "studio", "gallery", "art", "photography", "designer", "creative"}


def split_title(title):
    """Split annotation prefix from title, returning (clean_title, style_tags).

    Non-destructive: the original title is preserved. ``clean_title`` strips
    annotation prefixes (technique lists, CJK notes before separators) so the
    card shows a readable name.  Extracted tokens are merged into tags.
    """
    if not title:
        return title, []

    # 1. CJK note before a separator: "CJK… - real title"
    m = re.match(
        r"^([一-鿿㐀-䶿　-〿＀-￯"
        r"⺀-⻿㇀-㇯㈀-㋿"
        r"a-zA-Z0-9 +/&]{2,30})\s*[-–—=]\s*(.+)$",
        title,
    )
    if m:
        prefix, rest = m.group(1).strip(), m.group(2).strip()
        if re.search(r"[一-鿿㐀-䶿]", prefix) and len(rest) >= 3:
            tokens = re.split(r"[+/、，,]+", prefix)
            tags = [t.strip().lower() for t in tokens if t.strip()]
            return rest, tags

    # 2. Technique-tag list: "3D+scroll+web3Title" or "scroll/illus/animation/Title"
    tokens = re.split(r"[+/]", title)
    if len(tokens) >= 2:
        tag_run = []
        rest_parts = []
        found_non_tag = False
        for tok in tokens:
            tok_s = tok.strip()
            if not found_non_tag and tok_s.lower() in TECHNIQUE_KEYWORDS:
                tag_run.append(tok_s.lower())
            else:
                found_non_tag = True
                rest_parts.append(tok)
        if tag_run and rest_parts:
            clean = "/".join(rest_parts).strip(" -–—")
            if clean and len(clean) >= 3:
                return clean, tag_run

    return title, []


FOLDER_HINTS = None


def _build_folder_hints():
    global FOLDER_HINTS
    if FOLDER_HINTS is not None:
        return FOLDER_HINTS
    FOLDER_HINTS = {}
    pairs = [
        (["设计优秀的网页", "设计灵感", "inspiration", "design", "设计", "设计资源"],
         ("设计", "设计灵感-web")),
        (["前端", "frontend", "fe", "前端开发", "前端收藏"],
         ("前端", "前端收藏")),
        (["ai", "人工智能", "chatgpt", "aigc", "llm", "大模型"],
         ("AI", "AI工具")),
        (["工具", "tools", "实用工具", "效率", "效率工具"],
         ("工具产品", "效率工具")),
        (["博客", "blog", "blogs", "博客收藏"],
         ("博客", "个人博客")),
        (["教程", "学习", "tutorial", "tutorials", "课程", "course"],
         ("学习教程", "编程学习")),
        (["web3", "crypto", "加密", "区块链", "blockchain"],
         ("互联网", "Web3与加密")),
        (["作品集", "portfolio", "设计师"],
         ("设计", "作品集")),
        (["3d", "three.js", "webgl", "3d交互"],
         ("设计", "3D与交互")),
        (["blender-教程", "blender插件", "材质节点", "素材网站", "模型网站"],
         ("设计", "3D素材")),
        (["品牌", "brand", "官网"],
         ("设计", "品牌官网")),
        (["创意", "agency", "studio", "工作室"],
         ("设计", "创意工作室")),
        (["电商", "shop", "ecommerce", "购物"],
         ("互联网", "电商工具")),
        (["支付", "payment", "pay"],
         ("互联网", "支付工具")),
        (["配色", "color", "色彩"],
         ("设计", "配色工具")),
        (["字体", "font", "typography"],
         ("设计", "字体资源")),
        (["图标", "icon", "icons"],
         ("设计", "图标资源")),
        (["优秀的个人博客", "cool person", "个人博客"],
         ("博客", "个人博客")),
        (["磁力相关", "电影资源", "磁力链"],
         ("互联网", "影视娱乐")),
        (["内容生产", "在线文字卡片制作"],
         ("工具产品", "内容生产")),
        (["数据抓取"],
         ("工具产品", "下载工具")),
        (["建站开发与追踪"],
         ("互联网", "营销工具")),
    ]
    for names, (cat, subcat) in pairs:
        for name in names:
            FOLDER_HINTS[name.lower()] = (cat, subcat)
    return FOLDER_HINTS


def folder_hint(source_path):
    """Map common user folder names to (category, subcategory) or None."""
    if not source_path:
        return None
    hints = _build_folder_hints()
    for folder in source_path:
        norm = folder.strip().lower()
        if norm in hints:
            return hints[norm]
    return None


def infer_category(bookmark):
    """Heuristic fallback that names a category when the static taxonomy does
    not match. The built-in taxonomy is only a reference; this lets the manager
    reason beyond it (creative studios, 3D, portfolios, web3, brand sites)
    instead of dropping everything ambiguous into 其他/待确认. Returns
    (category, subcategory, description, confidence) or None."""
    domain = (bookmark.get("domain") or "").lower()
    title = (bookmark.get("title") or "").lower()
    url = (bookmark.get("url") or "").lower()
    text = f"{title} {domain} {url}"
    parts = domain.split(".")
    name = parts[0] if parts else ""
    tld = parts[-1] if len(parts) > 1 else ""
    name_tokens = set(re.split(r"[^a-z0-9]+", name))

    if tld == "finance":
        return ("互联网", "Web3与加密", "Web3 / 加密项目", 0.6)
    if tld in DESIGN_TLDS or (name_tokens & DESIGN_NAME_TOKENS):
        return ("设计", "创意工作室", "设计相关站点", 0.55)
    if any(k in text for k in ("official site", "official movie", "brand", "experience", "welcome to", "product")):
        return ("设计", "品牌官网", "品牌 / 产品官网", 0.5)
    # Brand / product showcase: a short slug followed by a tagline separator
    # ("Brand | tagline", "Brand — tagline"). Flagged low-confidence for review.
    if re.search(r"^[A-Za-z0-9& .,'’]{2,40}\s(\||—|–|-|:)", title):
        return ("设计", "品牌官网", "品牌 / 产品官网", 0.45)
    return None


def classify_bookmark(bookmark, levels=2, mode="optimized"):
    source = bookmark.get("source_folder_path") or []
    if mode == "source":
        path = source[:levels] or ["其他"]
        confidence = 0.75 if source else 0.35
        description = ""
    else:
        title = bookmark.get("title", "")
        url = bookmark.get("url", "")
        domain = bookmark.get("domain", "")
        folder_text = " ".join(source)
        text = f"{title} {url} {domain} {folder_text}".lower()
        matched = match_domain(domain)
        if matched:
            cat, subcat, description = matched
            confidence = 0.95
        else:
            cat, subcat, description, confidence = "其他", "待确认", "", 0.35
            # 1. Try folder-based hints (common user folder names)
            folder_match = folder_hint(source)
            if folder_match:
                cat, subcat = folder_match
                confidence = 0.72
            # 2. Try taxonomy keyword matching
            for candidate_cat, subcats in TAXONOMY.items():
                for candidate_subcat, keywords in subcats.items():
                    if any(keyword.lower() in text for keyword in keywords):
                        cat = candidate_cat
                        subcat = candidate_subcat
                        description = ""
                        confidence = 0.78
                        break
                if confidence >= 0.78:
                    break
            # 3. Try heuristic inference
            if confidence < 0.78:
                inferred = infer_category(bookmark)
                if inferred:
                    cat, subcat, description, confidence = inferred
        path = [cat]
        if levels >= 2:
            path.append(subcat)
        if levels >= 3 and domain:
            path.append(domain)
        if mode == "hybrid" and source:
            bookmark["source_category_path"] = source
        bookmark["optimized_category_path"] = path
    bookmark["category_path"] = path
    bookmark["confidence"] = confidence
    bookmark["description"] = description

    # --- clean_title (display only, no tag extraction) ---
    clean, _ = split_title(bookmark.get("title", ""))
    bookmark["clean_title"] = clean if clean != bookmark.get("title") else ""

    # --- Tags: derive from website content, brand, and genuine technique keywords ---
    tags = []
    seen_lower = set()
    domain = bookmark.get("domain", "")
    title = (bookmark.get("title") or "").lower()
    url = (bookmark.get("url") or "").lower()

    def _add(tag):
        """Add tag if not already present (case-insensitive dedup)."""
        key = tag.lower()
        if key not in seen_lower:
            seen_lower.add(key)
            tags.append(tag)

    # 1. Brand tag from domain (skip generic/hosting domains)
    brand = _brand_tag(domain)
    if brand:
        _add(brand)

    # 2. Content nature tag from subcategory
    subcat = path[1] if len(path) >= 2 else ""
    if subcat and subcat not in ("待确认",):
        _add(subcat)

    # 3. Technique keywords found in title only (genuine, not annotation prefix)
    #    Scan title, not URL — URLs contain random substrings that cause false matches.
    for kw in TECHNIQUE_KEYWORDS:
        if len(kw) >= 2 and kw in title:
            # Short keywords (<=3 chars) require word boundary to avoid
            # false positives like "ai" matching "brain" or "hair".
            if len(kw) <= 3:
                if not re.search(r"(?<![a-z])" + re.escape(kw) + r"(?![a-z])", title):
                    continue
            _add(kw)
            if len(tags) >= 5:
                break

    bookmark["tags"] = tags[:5]
    if confidence < 0.5:
        bookmark["review_status"] = "low_confidence"
    return bookmark


# Domains too generic/ubiquitous to produce a useful brand tag.
_GENERIC_DOMAINS = {
    "github.com", "gitlab.com", "medium.com", "dev.to", "hashnode.com",
    "twitter.com", "x.com", "youtube.com", "instagram.com", "tiktok.com",
    "facebook.com", "linkedin.com", "reddit.com", "pinterest.com",
    "notion.so", "vercel.com", "netlify.com", "cloudflare.com",
    "google.com", "apple.com", "microsoft.com", "amazon.com",
    "wikipedia.org", "wordpress.com", "substack.com",
    "vercel.app", "netlify.app", "github.io", "pages.dev",
    "producthunt.com", "news.ycombinator.com",
}


_TLD_WORDS = {
    "com", "net", "org", "io", "co", "app", "dev", "me", "blog", "site",
    "design", "art", "studio", "gallery", "store", "shop", "online",
    "cn", "uk", "de", "fr", "jp", "kr", "ru", "it", "es", "nl", "br",
    "in", "au", "ca", "se", "no", "dk", "fi", "pl", "cz", "at", "ch",
}


def _brand_tag(domain):
    """Extract a meaningful brand name from a domain, or '' for generic hosts."""
    if not domain:
        return ""
    base = domain.lower().split(":")[0]
    if base in _GENERIC_DOMAINS or any(base.endswith("." + g) for g in _GENERIC_DOMAINS):
        return ""
    parts = base.split(".")
    if len(parts) >= 2:
        name = parts[-2]
        if len(name) >= 2 and name not in _TLD_WORDS:
            return name.capitalize()
    return ""


def domain_label(domain):
    if not domain:
        return ""
    parts = domain.split(".")
    if len(parts) >= 2:
        return parts[-2].capitalize()
    return domain.capitalize()


def assign_duplicates(bookmarks):
    groups = {}
    for bm in bookmarks:
        key = bm.get("canonical_url") or normalize_url(bm.get("url", ""))
        groups.setdefault(key, []).append(bm)
    duplicate_groups = []
    for key, items in groups.items():
        if len(items) > 1:
            gid = "dup-" + stable_id(key)
            duplicate_groups.append({"id": gid, "canonical_url": key, "count": len(items), "items": [i["id"] for i in items]})
            for item in items:
                item["duplicate_group"] = gid
                if item.get("review_status") == "kept":
                    item["review_status"] = "duplicate"
    return duplicate_groups


def build_structure(bookmarks):
    root = {"name": "ROOT", "count": 0, "children": {}}
    for bm in bookmarks:
        node = root
        node["count"] += 1
        for part in bm.get("source_folder_path") or ["未分类"]:
            children = node["children"]
            if part not in children:
                children[part] = {"name": part, "count": 0, "children": {}}
            node = children[part]
            node["count"] += 1
    return root


def distribution(bookmarks):
    cats = {}
    domains = {}
    statuses = {}
    reviews = {}
    tags = {}
    for bm in bookmarks:
        cat = "/".join(bm.get("category_path") or ["未分类"])
        cats[cat] = cats.get(cat, 0) + 1
        domains[bm.get("domain") or ""] = domains.get(bm.get("domain") or "", 0) + 1
        statuses[bm.get("link_status", "unknown")] = statuses.get(bm.get("link_status", "unknown"), 0) + 1
        reviews[bm.get("review_status", "kept")] = reviews.get(bm.get("review_status", "kept"), 0) + 1
        for tag in bm.get("tags", []):
            tags[tag] = tags.get(tag, 0) + 1
    return {
        "categories": sorted(cats.items(), key=lambda x: x[1], reverse=True),
        "domains": sorted(domains.items(), key=lambda x: x[1], reverse=True)[:50],
        "link_status": sorted(statuses.items(), key=lambda x: x[0]),
        "review_status": sorted(reviews.items(), key=lambda x: x[0]),
        "tags": sorted(tags.items(), key=lambda x: x[1], reverse=True)[:100],
    }


def suggestions(bookmarks, duplicate_groups):
    result = []
    total = len(bookmarks) or 1
    dist = distribution(bookmarks)
    other_count = sum(count for cat, count in dist["categories"] if cat.startswith("其他"))
    if other_count / total > 0.15:
        result.append(f"其他分类占比 {other_count / total:.1%}，建议抽样复核并扩展 taxonomy。")
    if duplicate_groups:
        result.append(f"发现 {len(duplicate_groups)} 组重复书签，建议在管理器的重复审查视图中确认保留项。")
    dead = sum(1 for bm in bookmarks if bm.get("link_status") in {"dead", "timeout", "error"})
    if dead:
        result.append(f"发现 {dead} 个疑似失效链接，建议先人工确认再删除。")
    large = [item for item in dist["categories"] if item[1] / total > 0.25]
    for cat, count in large[:3]:
        result.append(f"{cat} 包含 {count} 个书签，分类偏大，建议拆分二级分类。")
    if not result:
        result.append("结构整体可用；建议定期运行增量更新和死链检测。")
    return result


def check_one_url(url, timeout=8):
    headers = {"User-Agent": "RicoBookmarksManager/1.0"}
    for method in ("HEAD", "GET"):
        req = request.Request(url, headers=headers, method=method)
        try:
            with request.urlopen(req, timeout=timeout) as resp:
                status = getattr(resp, "status", None) or resp.getcode()
                final_url = resp.geturl()
                if 200 <= status < 400:
                    return {"http_status": status, "link_status": "redirected" if final_url != url else "alive", "final_url": final_url}
                return {"http_status": status, "link_status": "dead", "final_url": final_url}
        except error.HTTPError as exc:
            return {"http_status": exc.code, "link_status": "dead", "final_url": exc.geturl() or url}
        except Exception as exc:
            if method == "HEAD":
                continue
            name = exc.__class__.__name__.lower()
            if "timeout" in name or "timed" in str(exc).lower():
                return {"http_status": None, "link_status": "timeout", "final_url": url}
            return {"http_status": None, "link_status": "error", "final_url": url}
    return {"http_status": None, "link_status": "unknown", "final_url": url}


def check_links(bookmarks, concurrency=16, timeout=8):
    by_url = {}
    for bm in bookmarks:
        by_url.setdefault(bm["url"], []).append(bm)
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = {pool.submit(check_one_url, url, timeout): url for url in by_url}
        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            result = future.result()
            for bm in by_url[url]:
                bm.update(result)
                if result["link_status"] in {"dead", "timeout", "error"} and bm.get("review_status") == "kept":
                    bm["review_status"] = "dead_link"


def make_data(bookmarks, mode="optimized", levels=2, source_file=""):
    duplicate_groups = assign_duplicates(bookmarks)
    reports = {
        "structure": build_structure(bookmarks),
        "distribution": distribution(bookmarks),
        "duplicates": duplicate_groups,
        "suggestions": suggestions(bookmarks, duplicate_groups),
    }
    return {
        "generated_at": now_iso(),
        "source_file": source_file,
        "mode": mode,
        "levels": levels,
        "taxonomy": TAXONOMY,
        "bookmarks": bookmarks,
        "reports": reports,
    }


def load_data(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict) and "bookmarks" in data:
        return data
    bookmarks = []
    if isinstance(data, dict):
        for cat, items in data.items():
            if isinstance(items, list):
                for bm in items:
                    item = copy.deepcopy(bm)
                    path = item.get("category_path") or [item.get("primary_category") or cat]
                    item["category_path"] = path if isinstance(path, list) else [path]
                    item.setdefault("source_folder_path", item.get("folder_path", []))
                    item.setdefault("canonical_url", normalize_url(item.get("url", "")))
                    item.setdefault("id", stable_id(item["canonical_url"]))
                    item.setdefault("domain", get_domain(item.get("url", "")))
                    item.setdefault("tags", [])
                    item.setdefault("link_status", "unknown")
                    item.setdefault("review_status", "kept")
                    bookmarks.append(item)
    elif isinstance(data, list):
        bookmarks = data
    return make_data(bookmarks, source_file=str(path))


def write_json(path, data, dry_run=False):
    path = Path(path)
    ensure_dir(path.parent)
    if dry_run:
        return
    if path.exists():
        backup_file(path)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_reports(output, data):
    reports_dir = Path(output) / "reports"
    ensure_dir(reports_dir)
    bms = data["bookmarks"]
    dist = data["reports"]["distribution"]
    duplicates = data["reports"]["duplicates"]
    report_files = {
        "统计分布.md": render_distribution(dist, len(bms)),
        "重复书签.md": render_duplicates(duplicates, bms),
        "分类优化建议.md": "# 分类优化建议\n\n" + "\n".join(f"- {s}" for s in data["reports"]["suggestions"]) + "\n",
        "结构分析.md": render_structure(data["reports"]["structure"]),
        "死链检测.md": render_deadlinks(bms),
    }
    for name, content in report_files.items():
        (reports_dir / name).write_text(content, encoding="utf-8")


def render_distribution(dist, total):
    lines = [f"# 统计分布\n\n总计：{total} 个书签\n", "## 分类\n", "| 分类 | 数量 |", "| --- | ---: |"]
    lines += [f"| {cat} | {count} |" for cat, count in dist["categories"]]
    lines += ["\n## Top 域名\n", "| 域名 | 数量 |", "| --- | ---: |"]
    lines += [f"| {domain or 'unknown'} | {count} |" for domain, count in dist["domains"][:30]]
    lines += ["\n## 状态\n", "| 状态 | 数量 |", "| --- | ---: |"]
    lines += [f"| {status} | {count} |" for status, count in dist["link_status"]]
    return "\n".join(lines) + "\n"


def render_duplicates(groups, bookmarks):
    by_id = {bm["id"]: bm for bm in bookmarks}
    lines = ["# 重复书签\n"]
    if not groups:
        return "# 重复书签\n\n未发现重复书签。\n"
    for group in groups:
        lines.append(f"\n## {group['id']}（{group['count']}）\n")
        for item_id in group["items"]:
            bm = by_id.get(item_id)
            if bm:
                lines.append(f"- [{bm['title']}]({bm['url']}) - {'/'.join(bm.get('source_folder_path') or [])}")
    return "\n".join(lines) + "\n"


def render_deadlinks(bookmarks):
    dead = [bm for bm in bookmarks if bm.get("link_status") in {"dead", "timeout", "error"}]
    if not dead:
        return "# 死链检测\n\n未发现疑似失效链接，或尚未运行死链检测。\n"
    lines = ["# 死链检测\n"]
    for bm in dead:
        lines.append(f"- `{bm.get('link_status')}` [{bm['title']}]({bm['url']})")
    return "\n".join(lines) + "\n"


def display_description(bookmark):
    desc = (bookmark.get("description") or "").strip()
    if not desc or desc == "待确认资源":
        return ""
    path = bookmark.get("category_path") or []
    normalized = desc.replace(" · ", "/").replace(" / ", "/")
    path_text = "/".join(path)
    if normalized == path_text:
        return ""
    return desc


def render_structure(node, depth=0):
    if depth == 0:
        lines = ["# 结构分析\n"]
    else:
        lines = []
    for child in sorted(node.get("children", {}).values(), key=lambda x: x["count"], reverse=True):
        lines.append(f"{'  ' * depth}- {child['name']}（{child['count']}）")
        lines.append(render_structure(child, depth + 1).rstrip())
    return "\n".join(line for line in lines if line) + "\n"


def export_markdown(data, output):
    output = Path(output)
    ensure_dir(output / "categories")
    write_reports(output, data)
    bookmarks = data["bookmarks"]
    lines = [f"# 书签总览\n\n生成时间：{data.get('generated_at', now_iso())}\n\n总计：{len(bookmarks)} 个书签\n"]
    grouped = {}
    for bm in bookmarks:
        key = "/".join(bm.get("category_path") or ["其他"])
        grouped.setdefault(key, []).append(bm)
    for key, items in sorted(grouped.items(), key=lambda x: len(x[1]), reverse=True):
        lines.append(f"\n## {key}（{len(items)}）\n")
        for bm in items:
            clean_desc = display_description(bm)
            desc = f" — {clean_desc}" if clean_desc else ""
            lines.append(f"- [{bm['title']}]({bm['url']}){desc}")
    (output / "书签总览.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    top_groups = {}
    for bm in bookmarks:
        cat = (bm.get("category_path") or ["其他"])[0]
        top_groups.setdefault(cat, []).append(bm)
    for cat, items in top_groups.items():
        content = [f"# {cat}\n\n书签数量：{len(items)}\n"]
        subgroups = {}
        for bm in items:
            path = bm.get("category_path") or [cat, "其他"]
            sub = path[1] if len(path) > 1 else "其他"
            subgroups.setdefault(sub, []).append(bm)
        for sub, sub_items in sorted(subgroups.items(), key=lambda x: len(x[1]), reverse=True):
            content.append(f"\n## {sub}（{len(sub_items)}）\n")
            for bm in sub_items:
                content.append(f"- [{bm['title']}]({bm['url']})")
        safe = "".join(c for c in cat if c.isalnum() or c in " _-") or "其他"
        (output / "categories" / f"{safe}.md").write_text("\n".join(content) + "\n", encoding="utf-8")


def export_browser_html(data, output):
    output = Path(output)
    ensure_dir(output)
    now = int(time.time())
    lines = [
        "<!DOCTYPE NETSCAPE-Bookmark-file-1>",
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">',
        "<TITLE>Bookmarks</TITLE>",
        "<H1>Bookmarks</H1>",
        "<DL><p>",
        f'    <DT><H3 ADD_DATE="{now}" LAST_MODIFIED="{now}">Rico 书签</H3>',
        "    <DL><p>",
    ]
    tree = {}
    for bm in data["bookmarks"]:
        node = tree
        for part in bm.get("category_path") or ["其他"]:
            node = node.setdefault(part, {})
        node.setdefault("__items__", []).append(bm)
    emit_tree(lines, tree, 2, now)
    lines += ["    </DL><p>", "</DL><p>"]
    (output / "bookmarks_import.html").write_text("\n".join(lines), encoding="utf-8")


def emit_tree(lines, node, indent, now):
    pad = "    " * indent
    for name, child in sorted(node.items()):
        if name == "__items__":
            continue
        lines.append(f'{pad}<DT><H3 ADD_DATE="{now}" LAST_MODIFIED="{now}">{html.escape(name)}</H3>')
        lines.append(f"{pad}<DL><p>")
        emit_tree(lines, child, indent + 1, now)
        lines.append(f"{pad}</DL><p>")
    for bm in node.get("__items__", []):
        add_date = bm.get("add_date") or now
        lines.append(f'{pad}<DT><A HREF="{html.escape(bm["url"], quote=True)}" ADD_DATE="{add_date}">{html.escape(bm["title"])}</A>')


def theme_root():
    return Path(__file__).resolve().parents[1] / "assets" / "themes"


def list_themes():
    themes = []
    for theme_id in THEME_IDS:
        theme_path = theme_root() / theme_id / "theme.json"
        if theme_path.exists():
            theme = json.loads(theme_path.read_text(encoding="utf-8"))
            themes.append(theme)
    return themes


def load_theme(theme_id="ease"):
    if theme_id not in THEME_IDS:
        raise ValueError(f"Unknown theme '{theme_id}'. Choose one of: {', '.join(THEME_IDS)}")
    theme_path = theme_root() / theme_id / "theme.json"
    if not theme_path.exists():
        raise FileNotFoundError(f"Theme file not found: {theme_path}")
    theme = json.loads(theme_path.read_text(encoding="utf-8"))
    theme["source"] = str(theme_path)
    return theme


def parse_design(path):
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Design file not found: {p}")
    text = p.read_text(encoding="utf-8", errors="ignore")
    colors = list(dict.fromkeys(re.findall(r"#[0-9a-fA-F]{6}", text)))
    title = next((line.lstrip("# ").strip() for line in text.splitlines() if line.strip().startswith("#")), "Custom Design")
    fallback = load_theme("ease")
    custom = copy.deepcopy(fallback)
    custom["id"] = "custom"
    custom["name"] = title
    custom["description"] = "Custom DESIGN.md theme override"
    custom["source"] = str(p)
    custom["design_summary"] = text[:1200]
    if colors:
        palette = custom["colors"]
        palette["accent"] = colors[0]
        palette["accentStrong"] = colors[1] if len(colors) > 1 else colors[0]
        palette["accentSoft"] = colors[2] if len(colors) > 2 else palette.get("accentSoft", "#eef6ec")
        if len(colors) > 3:
            palette["bg"] = colors[3]
        if len(colors) > 4:
            palette["panel"] = colors[4]
    return custom


def resolve_theme(theme_id="ease", design=None):
    if design:
        return parse_design(design)
    return load_theme(theme_id or "ease")


def theme_css(theme):
    colors = theme.get("colors", {})
    radii = theme.get("radii", {})
    fonts = theme.get("fonts", {})
    variables = {
        "--bg": colors.get("bg", "#fffefc"),
        "--panel": colors.get("panel", "#ffffff"),
        "--panel-raised": colors.get("panelRaised", "#f7f7f7"),
        "--sidebar": colors.get("sidebar", colors.get("panel", "#ffffff")),
        "--overlay": colors.get("overlay", "rgba(0,0,0,.45)"),
        "--text": colors.get("text", "#161712"),
        "--muted": colors.get("muted", "#6e7568"),
        "--faint": colors.get("faint", "#9aa394"),
        "--inverse": colors.get("inverse", "#ffffff"),
        "--accent": colors.get("accent", "#0f3e17"),
        "--accent-strong": colors.get("accentStrong", colors.get("accent", "#0f3e17")),
        "--accent-soft": colors.get("accentSoft", "#eef6ec"),
        "--danger": colors.get("danger", "#a23d3d"),
        "--warning": colors.get("warning", "#8a6500"),
        "--success": colors.get("success", "#247346"),
        "--border": colors.get("border", "#dfe5dc"),
        "--shadow": colors.get("shadow", "none"),
        "--radius-sm": radii.get("sm", "7px"),
        "--radius-md": radii.get("md", "14px"),
        "--radius-pill": radii.get("pill", "999px"),
        "--font-ui": fonts.get("ui", "system-ui, sans-serif"),
        "--font-display": fonts.get("display", "Georgia, serif"),
        "--font-mono": fonts.get("mono", "monospace"),
    }
    for extra_key, extra_value in (theme.get("cssVars") or {}).items():
        if str(extra_key).startswith("--") and extra_value:
            variables[extra_key] = extra_value
    lines = [f":root {{", f"  color-scheme: {theme.get('mode', 'light')};"]
    for key, value in variables.items():
        lines.append(f"  {key}: {value};")
    lines.append("}")
    lines.append(f"html {{ background: var(--bg); }}")
    lines.append(f"body {{ background: var(--bg); }}")
    return "\n".join(lines) + "\n"


def resolve_theme_css(theme, theme_id="ease", design=None):
    if not design and theme_id in THEME_IDS:
        css_path = theme_root() / theme_id / "theme.css"
        if css_path.exists():
            return css_path.read_text(encoding="utf-8")
    return theme_css(theme)


def export_manager(data, output, design=None, theme="ease"):
    output = Path(output)
    ensure_dir(output)
    root = Path(__file__).resolve().parents[1]
    template = root / "assets" / "bookmark-manager-template"
    for name in ("index.html", "styles.css", "app.js", "logo.jpg"):
        shutil.copy2(template / name, output / name)
    selected_theme = resolve_theme(theme, design)
    (output / "theme.css").write_text(resolve_theme_css(selected_theme, theme, design), encoding="utf-8")
    meta = {"theme": selected_theme, "generated_at": now_iso()}
    data_js = "window.RICO_BOOKMARKS_DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
    data_js += "window.RICO_BOOKMARKS_META = " + json.dumps(meta, ensure_ascii=False, indent=2) + ";\n"
    (output / "data.js").write_text(data_js, encoding="utf-8")


def organize_from_input(input_path, mode="optimized", levels=2, check=False, no_network=False):
    bookmarks = parse_bookmark_html(input_path)
    for bm in bookmarks:
        classify_bookmark(bm, levels=levels, mode=mode)
    if check and not no_network:
        check_links(bookmarks)
    return make_data(bookmarks, mode=mode, levels=levels, source_file=str(input_path))


def write_data_bundle(data, output, dry_run=False):
    data_path = Path(output) / "data" / "bookmarks.json"
    write_json(data_path, data, dry_run=dry_run)
    if not dry_run:
        write_reports(output, data)
    return data_path


def command_analyze(args):
    data = organize_from_input(args.input, mode=args.mode, levels=args.levels, check=args.check_links, no_network=args.no_network)
    if args.output:
        write_data_bundle(data, args.output)
    print_summary(data)


def command_organize(args):
    data = organize_from_input(args.input, mode=args.mode, levels=args.levels, check=args.check_links, no_network=args.no_network)
    path = write_data_bundle(data, args.output)
    print(f"Wrote {path}")


def command_export_html(args):
    data = load_data(args.data)
    export_browser_html(data, args.output)
    print(f"Wrote {Path(args.output) / 'bookmarks_import.html'}")


def command_export_md(args):
    data = load_data(args.data)
    export_markdown(data, args.output)
    print(f"Wrote Markdown output in {args.output}")


def command_manager(args):
    data = load_data(args.data)
    export_manager(data, args.output, args.design, args.theme)
    print(f"Wrote manager in {args.output} using theme {args.theme if not args.design else 'custom design'}")


def command_themes(args):
    for theme in list_themes():
        print(f"{theme['id']}\t{theme.get('name', theme['id'])}\t{theme.get('mode', 'light')}\t{theme.get('description', '')}")


def command_update(args):
    existing = load_data(args.existing)
    new_data = organize_from_input(args.input, mode=args.mode, levels=args.levels, check=args.check_links, no_network=args.no_network)
    existing_by_url = {bm.get("canonical_url"): bm for bm in existing["bookmarks"]}
    added, changed, skipped = [], [], []
    for bm in new_data["bookmarks"]:
        key = bm.get("canonical_url")
        if key in existing_by_url:
            old = existing_by_url[key]
            if old.get("title") != bm.get("title"):
                changed.append({"existing": old, "incoming": bm})
            else:
                skipped.append(bm)
        else:
            added.append(bm)
            existing["bookmarks"].append(bm)
    existing["generated_at"] = now_iso()
    existing["reports"] = make_data(existing["bookmarks"], mode=args.mode, levels=args.levels)["reports"]
    ensure_dir(Path(args.output) / "reports")
    report = render_update_report(added, changed, skipped, args.dry_run)
    (Path(args.output) / "reports" / "增量更新.md").write_text(report, encoding="utf-8")
    if not args.dry_run:
        write_data_bundle(existing, args.output)
    print(report)


def render_update_report(added, changed, skipped, dry_run):
    lines = ["# 增量更新\n", f"模式：{'dry-run' if dry_run else 'write'}\n"]
    lines.append(f"- 新增：{len(added)}")
    lines.append(f"- 标题变化：{len(changed)}")
    lines.append(f"- 已存在跳过：{len(skipped)}")
    if added:
        lines.append("\n## 新增书签\n")
        for bm in added[:200]:
            lines.append(f"- [{bm['title']}]({bm['url']}) -> {'/'.join(bm.get('category_path') or [])}")
    if changed:
        lines.append("\n## 标题变化\n")
        for item in changed[:200]:
            lines.append(f"- {item['existing'].get('title')} -> {item['incoming'].get('title')}")
    return "\n".join(lines) + "\n"


def command_all(args):
    data = organize_from_input(args.input, mode=args.mode, levels=args.levels, check=args.check_links, no_network=args.no_network)
    write_data_bundle(data, args.output)
    export_markdown(data, args.output)
    export_browser_html(data, args.output)
    export_manager(data, Path(args.output) / "site", args.design, args.theme)
    print_summary(data)
    print(f"Wrote complete output in {args.output}")


def print_summary(data):
    bms = data["bookmarks"]
    print(f"Bookmarks: {len(bms)}")
    print(f"Mode: {data.get('mode')} / levels: {data.get('levels')}")
    print(f"Duplicate groups: {len(data['reports']['duplicates'])}")
    print("Top categories:")
    for cat, count in data["reports"]["distribution"]["categories"][:10]:
        print(f"  {cat}: {count}")


def add_common(parser):
    parser.add_argument("--mode", choices=["source", "optimized", "hybrid"], default="optimized")
    parser.add_argument("--levels", type=int, choices=[1, 2, 3], default=2)
    parser.add_argument("--check-links", action="store_true")
    parser.add_argument("--no-network", action="store_true")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Rico browser bookmark manager")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("analyze")
    p.add_argument("--input", required=True)
    p.add_argument("--output")
    add_common(p)
    p.set_defaults(func=command_analyze)

    p = sub.add_parser("organize")
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    add_common(p)
    p.set_defaults(func=command_organize)

    p = sub.add_parser("export-html")
    p.add_argument("--data", required=True)
    p.add_argument("--output", required=True)
    p.set_defaults(func=command_export_html)

    p = sub.add_parser("export-md")
    p.add_argument("--data", required=True)
    p.add_argument("--output", required=True)
    p.set_defaults(func=command_export_md)

    p = sub.add_parser("manager")
    p.add_argument("--data", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--design")
    p.add_argument("--theme", choices=THEME_IDS, default="ease")
    p.set_defaults(func=command_manager)

    p = sub.add_parser("themes")
    p.set_defaults(func=command_themes)

    p = sub.add_parser("update")
    p.add_argument("--input", required=True)
    p.add_argument("--existing", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--dry-run", action="store_true")
    add_common(p)
    p.set_defaults(func=command_update)

    p = sub.add_parser("all")
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--design")
    p.add_argument("--theme", choices=THEME_IDS, default="ease")
    add_common(p)
    p.set_defaults(func=command_all)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
