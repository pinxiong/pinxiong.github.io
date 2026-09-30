# GitHub Pages 完整搭建手册

> 目标：搭建一个以 Git 仓库为"单一真相源"的个人英文技术博客，自动部署到 GitHub Pages。
> 环境：macOS（zsh）。全程约 30-45 分钟。
> 最终效果：本地写 Markdown → `git push` → 约 1 分钟后线上自动更新。

---

## 第 0 步：选型（先看懂再动手）

| 方案 | 优点 | 缺点 | 结论 |
|---|---|---|---|
| **Hugo + PaperMod**（本手册采用） | 单二进制、构建极快、主题成熟、文档全 | 模板语法是 Go template，定制需学习 | ✅ 写作为主、追求稳定的首选 |
| Astro | 现代化、组件化、可扩展交互 | 依赖 Node 生态，配置项多 | 想做复杂交互站点再选 |
| Jekyll | GitHub 原生支持，零 CI 配置 | Ruby 环境麻烦，构建慢，主题老旧 | 不推荐新站使用 |

**为什么选 Hugo**：你的核心诉求是"内容沉淀 + 长期维护"，Hugo 的单文件、无依赖、秒级构建最适合十年尺度的维护。

---

## 第 1 步：准备环境

### 1.1 安装 Hugo

```bash
brew install hugo
```

**验证**：

```bash
hugo version
```

应输出类似 `hugo v0.13x.x+extended darwin/arm64`。有版本号即成功。

**失败修复**：
- 提示 `brew: command not found` → 先装 Homebrew：`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- 版本太旧（< v0.120）→ `brew upgrade hugo`

### 1.2 确认 Git 与 GitHub 账号

```bash
git --version
git config --global user.name   # 应显示你的名字
git config --global user.email  # 应显示你的 GitHub 邮箱
```

**验证**：能输出用户名和邮箱即可。没有的话：

```bash
git config --global user.name "YourName"
git config --global user.email "you@example.com"
```

### 1.3 确认 GitHub 推送权限

```bash
ssh -T git@github.com
```

**验证**：看到 `Hi <username>! You've successfully authenticated` 即成功。

**失败修复**：提示 `Permission denied` → 说明本机还没配 SSH key，执行：

```bash
ssh-keygen -t ed25519 -C "you@example.com"   # 一路回车
cat ~/.ssh/id_ed25519.pub                     # 复制输出的全部内容
```

然后打开 GitHub → Settings → SSH and GPG keys → New SSH key，粘贴保存，重新执行 `ssh -T git@github.com` 验证。

---

## 第 2 步：创建 GitHub 仓库

### 2.1 在 GitHub 网页上操作

1. 打开 https://github.com/new
2. Repository name 填：`<你的用户名>.github.io`（**必须 exactly 等于你的用户名**，这是个人主页的特殊命名，例如用户名为 `pinxiong` 就填 `pinxiong.github.io`）
3. 选 **Public**（GitHub Pages 免费版要求公开）
4. **不要**勾选 README / .gitignore / License（保持空仓库，稍后本地推送）
5. 点 Create repository

**验证**：仓库创建成功，页面显示 "Quick setup" 和仓库地址 `git@github.com:<username>/<username>.github.io.git`。

**失败修复**：如果名字填错了 → 仓库 Settings → Rename 改成正确名字，URL 才会是根域名。

---

## 第 3 步：本地初始化 Hugo 站点

### 3.1 生成站点骨架

```bash
cd ~/projects          # 换成你习惯放代码的目录
hugo new site my-blog
cd my-blog
git init
```

**验证**：`ls` 应看到 `archetypes  assets  content  data  hugo.toml  layouts  static  themes` 等目录。

### 3.2 添加 PaperMod 主题（git submodule 方式）

```bash
git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
```

**验证**：`ls themes/PaperMod` 能看到主题文件（layouts、assets 等）。

**失败修复**：
- 克隆超时 → 网络问题，重试或换网络环境
- `themes/PaperMod` 目录是空的 → submodule 没拉下来，执行 `git submodule update --init --recursive`

### 3.3 配置 hugo.toml

把 `hugo.toml` 整个替换为以下内容（把 `yourusername` 和站点信息改成你的）：

```toml
baseURL = "https://yourusername.github.io/"
languageCode = "en-us"
title = "Your Name"
theme = "PaperMod"
paginate = 10

[params]
  description = "Long-term builder. Cloud, open source, and AI engineering notes."
  defaultTheme = "auto"        # auto / light / dark
  ShowReadingTime = true
  ShowShareButtons = false
  ShowPostNavLinks = true
  ShowBreadCrumbs = true
  ShowCodeCopyButtons = true

  [params.homeInfoParams]
    Title = "Hi, I'm Your Name"
    Content = "Apache Dubbo Committer · AWS Community Builder · Writing about cloud, open source, and AI engineering."

[[menu.main]]
  name = "Posts"
  url = "/posts/"
  weight = 1
[[menu.main]]
  name = "About"
  url = "/about/"
  weight = 2
[[menu.main]]
  name = "Archives"
  url = "/archives/"
  weight = 3
[[menu.main]]
  name = "Search"
  url = "/search/"
  weight = 4

[outputs]
  home = ["HTML", "RSS", "JSON"]   # JSON 是 PaperMod 搜索功能所需
```

**注意**：`baseURL` 必须和你的 GitHub Pages 地址完全一致（含结尾 `/`），这是线上样式和链接正确的关键，也是全站 canonical 链接的来源。

---

## 第 4 步：创建必备页面与第一篇文章

### 4.1 About 页

```bash
hugo new content about.md
```

编辑 `content/about.md`：

```markdown
---
title: "About"
layout: "about"
url: "/about/"
summary: "about"
---

(Your English bio here.)
```

### 4.2 Archives 页与 Search 页（PaperMod 标配）

```bash
mkdir -p content
cat > content/archives.md << 'EOF'
---
title: "Archives"
layout: "archives"
url: "/archives/"
summary: "archives"
---
EOF

cat > content/search.md << 'EOF'
---
title: "Search"
layout: "search"
url: "/search/"
summary: "search"
placeholder: "Search posts..."
---
EOF
```

### 4.3 第一篇文章

```bash
hugo new content posts/my-first-post.md
```

编辑 `content/posts/my-first-post.md`，**重点：把 `draft: true` 改成 `draft: false`**，否则不会发布：

```markdown
---
title: "My First Post"
date: 2026-09-29T22:00:00+08:00
draft: false
tags: ["meta"]
summary: "Why I started this site."
---

Your content here.
```

**写作模板建议**（四段式复盘结构，直接当 archetype 用）：

```markdown
---
title: ""
date: {{ .Date }}
draft: true
tags: []
summary: ""
---

## Problem
## Analysis
## Method
## Lessons
```

把上面这段覆盖写入 `archetypes/default.md`，以后 `hugo new content` 生成的每篇文章自动带四段式骨架。

---

## 第 5 步：本地预览验证

```bash
hugo server -D
```

**验证**：
1. 打开 http://localhost:1313 → 能看到首页、你的站点标题和简介
2. 点 Posts → 能看到第一篇文章，点进去内容完整
3. 点 Search → 搜索框能搜到文章关键词
4. 页面样式正常（有 PaperMod 的简洁排版，不是裸 HTML）

**失败修复**：
- 页面裸奔无样式 → 检查 `hugo.toml` 里 `theme = "PaperMod"` 拼写、以及 `themes/PaperMod` 非空
- 文章不出现 → 检查 `draft: false`；检查 `date` 不是未来时间（未来日期的文章默认不发布）
- 端口被占用 → `hugo server -D -p 1314`

预览确认无误后 `Ctrl+C` 停止。

---

## 第 6 步：配置 GitHub Actions 自动部署

### 6.1 创建部署工作流

```bash
mkdir -p .github/workflows
cat > .github/workflows/hugo.yaml << 'EOF'
name: Deploy Hugo site to Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: true

defaults:
  run:
    shell: bash

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      HUGO_VERSION: 0.148.2
    steps:
      - name: Install Hugo CLI
        run: |
          wget -O ${{ runner.temp }}/hugo.deb https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb \
          && sudo dpkg -i ${{ runner.temp }}/hugo.deb

      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v5

      - name: Build with Hugo
        env:
          HUGO_CACHEDIR: ${{ runner.temp }}/hugo_cache
          HUGO_ENVIRONMENT: production
        run: |
          hugo \
            --minify \
            --baseURL "${{ steps.pages.outputs.base_url }}/"

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
EOF
```

> 关键点：`submodules: recursive` 确保 CI 拉取主题；`--baseURL` 由 GitHub 自动注入，避免环境不一致。

### 6.2 提交并推送

```bash
git add -A
git commit -m "Initial Hugo site with PaperMod"
git branch -M main
git remote add origin git@github.com:yourusername/yourusername.github.io.git
git push -u origin main
```

（把 `yourusername` 两处都替换为你的 GitHub 用户名）

### 6.3 开启 Pages 的 Actions 部署源

推送后，到 GitHub 网页操作：

1. 打开仓库 → **Settings → Pages**
2. Source 选择 **GitHub Actions**（不是 Deploy from a branch）
3. 保存

**验证**：
1. 仓库 → Actions 标签页 → 能看到 "Deploy Hugo site to Pages" 工作流在运行，约 1-2 分钟变绿
2. 打开 `https://yourusername.github.io/` → 看到和本地预览一样的站点

**失败修复**：
- Actions 报错 `theme not found` / 网站无样式 → 工作流里 `submodules: recursive` 缺失，或本地 submodule 未正确提交；执行 `git submodule update --init --recursive` 后重新提交 `.gitmodules`
- Actions 红色失败 → 点进去看日志，最常见是 Hugo 版本与主题不兼容：把 `HUGO_VERSION` 改为本地 `hugo version` 显示的版本号
- 站点 404 → 确认仓库名 exactly 是 `用户名.github.io`；确认 Settings → Pages 的 Source 是 GitHub Actions；首次部署等 1-3 分钟
- 样式丢失/链接全错 → `baseURL` 配置不对，检查 hugo.toml 结尾是否有 `/`

---

## 第 7 步：绑定自定义域名（可选，建议做）

自定义域名（如 `yourname.dev`）让 SEO 权重真正沉淀在"你的"域名上，且即使将来迁离 GitHub Pages 也不受影响。

### 7.1 购买域名

在 Cloudflare / Namecheap / GoDaddy 购买（推荐 Cloudflare，价格透明、DNS 快）。

### 7.2 配置 DNS

在域名服务商处添加：

- 根域名：4 条 A 记录，分别指向
  - `185.199.108.153` / `185.199.109.153` / `185.199.110.153` / `185.199.111.153`
- www：1 条 CNAME 记录，指向 `yourusername.github.io`

### 7.3 仓库侧配置

1. 在站点 `static/` 目录创建 `CNAME` 文件，内容只有一行你的域名：`yourname.dev`
2. 仓库 Settings → Pages → Custom domain 填 `yourname.dev`，保存
3. DNS 生效后（几分钟到几小时）勾选 **Enforce HTTPS**
4. 同时把 `hugo.toml` 的 `baseURL` 改为 `https://yourname.dev/`，提交推送

**验证**：`curl -I https://yourname.dev` 返回 200，浏览器访问正常且带锁标志。

**失败修复**：DNS 超过 24 小时未生效 → 用 `dig yourname.dev` 检查记录是否生效；确认没有冲突的 AAAA 记录。

---

## 第 8 步：日常写作工作流（每天只用这三行）

```bash
hugo new content posts/$(date +%Y-%m-%d)-my-topic.md   # 1. 新建（自带四段式骨架）
# ... 写 Markdown，写完把 draft 改为 false ...
git add -A && git commit -m "Add post: my-topic" && git push   # 2. 推送
# 3. 约 1 分钟后线上自动更新，Actions 标签页可看部署状态
```

**配套习惯（与你的资产策略对应）**：
- 文章写完先在仓库定稿 → GitHub Pages 是正式版（canonical 源头）
- 复制全文到 Dev.to / Medium 时设置 canonical 指回本站
- 每季度 `git tag v2026-Q3` 打一个季度标签，方便做元复盘

---

## 第 9 步：可选增强（后续按需添加）

| 增强 | 做法 | 何时做 |
|---|---|---|
| 评论系统 | Giscus（基于 GitHub Discussions，零成本，数据在自己仓库） | 有稳定读者后 |
| 访问统计 | Cloudflare Web Analytics（免费、无 Cookie、轻量） | 自定义域名后 |
| 订阅入口 | 页面嵌入 Substack/Beehiiv 订阅表单 | Newsletter 开通后 |
| 站内搜索 | PaperMod 已自带（本手册已配置） | — |
| 多语言预留 | Hugo 原生支持多语言，将来想加中文只需加 `content/` 下按语言分目录 | 需要时再开 |

---

## 故障速查表

| 症状 | 最可能原因 | 修复 |
|---|---|---|
| 本地预览正常，线上 404 | Pages Source 未设为 GitHub Actions | Settings → Pages → Source 改 GitHub Actions |
| 线上页面裸奔无样式 | CI 没拉 submodule | 工作流 checkout 加 `submodules: recursive` |
| 文章本地有线上没有 | `draft: true` 或日期在未来 | 改 draft: false，修正 date |
| 链接/图片全 404 | baseURL 错误 | 检查 hugo.toml 的 baseURL 与结尾 `/` |
| Actions 红色 | Hugo 版本与主题不兼容 | HUGO_VERSION 对齐本地版本 |
| 自定义域名不生效 | DNS 未生效或记录错误 | `dig yourname.dev` 排查 |
