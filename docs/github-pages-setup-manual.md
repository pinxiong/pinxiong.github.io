# GitHub Pages 完整搭建手册

> 目标：搭建一个以 Git 仓库为"单一真相源"的个人英文技术博客，自动部署到 GitHub Pages。
> 环境：macOS（zsh）。全程约 30-45 分钟。
> 最终效果：本地写 Markdown → `git push` → 约 1 分钟后线上自动更新。

> **⚠️ 时效说明（2026-09 更新）**
> 本手册记录的是**从零搭建**的过程，其中主题部分最早用的是 PaperMod。仓库现在实际使用
> **Blowfish v3.8.0 + Hugo 0.165.0**，且主题是**内嵌（vendored）**而非 git submodule，
> 站点配置也拆到了 `config/_default/` 下。
> 下面第 3 步、第 4.2 步、第 6 步中与主题/配置相关的段落已同步改为 Blowfish 的做法；
> 日常发布与排错请以 **[`hugo-publish-manual.md`](./hugo-publish-manual.md)** 为准。

---

## 第 0 步：选型（先看懂再动手）

| 方案 | 优点 | 缺点 | 结论 |
|---|---|---|---|
| **Hugo + Blowfish**（本手册采用） | 单二进制、构建极快、主题活跃维护、自带搜索/深色模式/代码复制 | 模板语法是 Go template，定制需学习 | ✅ 写作为主、追求长期稳定的首选 |
| Hugo + PaperMod | 极简、上手最快 | 上游 2024-11 后基本停更，新 Hugo 需打补丁 | 仅作参考，不推荐新站 |
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

应输出类似 `hugo v0.165.0+extended darwin/arm64`。有版本号即成功。

> **版本要求**：Blowfish v3.8 用到 `site.Language.Locale`，需要 **Hugo ≥ 0.162**。
> 本仓库把版本钉在 **0.165.0**（CI 与本地一致），新机器直接用仓库自带的
> `./scripts/install-hugo.sh` 安装最省事——它读的就是 CI 里那个版本号，且无需 sudo。

**失败修复**：
- 提示 `brew: command not found` → 先装 Homebrew：`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- 版本太旧（< v0.162）→ `brew upgrade hugo`，或改用 `./scripts/install-hugo.sh`

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

### 3.2 添加 Blowfish 主题（内嵌 / vendored 方式）

本项目**不用 git submodule**，而是把主题源码直接提交进仓库，好处是：`git clone` 即可构建、不依赖 Go 工具链、CI 不必拉 submodule、历史可回滚。

```bash
# 下载指定版本（示例为 v3.8.0）并解压
curl -L -o /tmp/blowfish.tar.gz \
  https://github.com/nunocoracao/blowfish/archive/refs/tags/v3.8.0.tar.gz
mkdir -p themes
tar -xzf /tmp/blowfish.tar.gz -C /tmp
cp -R /tmp/blowfish-3.8.0 themes/blowfish
echo "v3.8.0" > themes/blowfish/BLOWFISH_VERSION
rm -rf themes/blowfish/.git themes/blowfish/exampleSite
```

**验证**：`ls themes/blowfish` 能看到 `layouts`、`assets`、`i18n`、`static` 等目录，且 `themes/blowfish/BLOWFISH_VERSION` 内容为 `v3.8.0`。

**失败修复**：
- 下载超时 → 换网络，或用镜像前缀 `https://gh-proxy.com/https://github.com/...`
- 构建时提示找不到主题 → 确认目录名与 `config/_default/hugo.toml` 里 `theme = "blowfish"` 一致

> Blowfish 的编译后 CSS（Tailwind）已经**随主题提交**，所以 CI 里不需要 Node/npm 构建步骤。

### 3.3 站点配置（拆到 `config/_default/`）

Blowfish 推荐按功能拆分配置。把原来的 `hugo.toml` 拆成 5 个文件：

```
config/_default/
├── hugo.toml          # baseURL / 分类法 / 输出格式 / Hugo 最低版本
├── params.toml        # 主题参数（配色 / 首页 / 文章页 / 列表页）
├── languages.en.toml  # 标题 / 描述 / 作者资料 / 社交链接
├── menus.en.toml      # 顶部菜单
└── markup.toml        # goldmark + 代码高亮
```

`hugo.toml` 关键内容：

```toml
baseURL = "https://yourusername.github.io/"
title = "Your Name"
theme = "blowfish"
defaultContentLanguage = "en"
paginate = 10

[taxonomies]
  tag = "tags"
  category = "categories"
  author = "authors"
  series = "series"

[outputs]
  home = ["HTML", "RSS", "JSON"]   # JSON 供主题内置搜索（Fuse.js）使用

[module]
  [module.hugoVersion]
    extended = true
    min = "0.165.0"
```

`params.toml` 至少保留这些（其余走主题默认）：

```toml
colorScheme = "blowfish"        # 克制的蓝色强调色
defaultAppearance = "light"
autoSwitchAppearance = true     # 跟随系统，同时保留读者手动切换
enableSearch = true
enableCodeCopy = true
mainSections = ["posts"]

[header]
  layout = "basic"

[homepage]
  layout = "profile"            # 头像 + 简介 + 最近文章
  showRecent = true

[article]
  showAuthor = true
  showAuthorBottom = true
  showTableOfContents = true    # 文章目录
  showRelatedContent = true
  sharingLinks = ["linkedin", "x-twitter", "email"]

[list]
  groupByYear = true            # 文章列表按年份分组
```

`languages.en.toml` 负责站点标题、描述、作者资料和社交链接（`[params.author]` + `[[params.author.links]]`）。

**注意**：`baseURL` 必须和你的 GitHub Pages 地址完全一致（含结尾 `/`），这是线上样式和链接正确的关键，也是全站 canonical 链接的来源。绑了自定义域名后改成 `https://yourname.dev/`。

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

### 4.2 Archives 页与 Search 页（Blowfish 不需要单独建）

Blowfish 的搜索是**顶栏那个放大镜**（Fuse.js 读首页生成的 `index.json`），没有独立的 `/search/` 页面；文章列表 `/posts/` 本身按年份分组，就等于归档页。

所以**不要**再创建 `content/archives.md` / `content/search.md`——如果建了，站点会出现两个多余的、样式不匹配的页面。只需保证：

1. `config/_default/params.toml` 里 `enableSearch = true`（默认已开）；
2. `hugo.toml` 的 `[outputs] home` 里含 `"JSON"`（搜索索引来源）。

（如果你的仓库是从旧 PaperMod 版本迁过来的，把这两个 .md 文件删掉即可。）

### 4.3 第一篇文章

```bash
hugo new posts/my-first-post.md
```

编辑 `content/posts/my-first-post.md`，**重点：把 `draft: true` 改成 `draft: false`**，否则不会发布：

```markdown
---
title: "My First Post"
date: 2026-09-29T22:00:00+08:00
draft: false
tags: ["meta"]
summary: "Why I started this site."
showTableOfContents: true
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
## Context
## Diagnosis
## Fix
## Lessons
```

把上面这段覆盖写入 `archetypes/posts.md`（按 section 名匹配，这样 `hugo new posts/xxx.md` 才会自动套用；放在 `archetypes/default.md` 只对普通页面生效）。以后新建的每篇文章都会自带四段式骨架。

---

## 第 5 步：本地预览验证

```bash
hugo server -D
```

**验证**：
1. 打开 http://localhost:1313 → 能看到首页（profile 版式，含头像/简介/最近文章）
2. 点 Posts → 能看到第一篇文章，点进去内容完整
3. 点顶栏放大镜 → 能搜到文章关键词
4. 页面样式正常（Blowfish 的简洁排版 + 你的 Medium 风格正文，不是裸 HTML）
5. 页脚或顶栏切换明暗主题 → 深色模式生效

**失败修复**：
- 页面裸奔无样式 → 检查 `config/_default/hugo.toml` 里 `theme = "blowfish"` 拼写、以及 `themes/blowfish` 非空
- 搜索无结果 → 确认 `[outputs] home` 含 `"JSON"`，且 `enableSearch = true`
- 构建报 `can't evaluate field Locale` → Hugo 版本低于 0.162，升级到 0.165.0
- 文章不出现 → 检查 `draft: false`；检查 `date` 不是未来时间（未来日期的文章默认不发布）
- 端口被占用 → `hugo server -D -p 1314`

预览确认无误后 `Ctrl+C` 停止。

---

## 第 6 步：配置 GitHub Actions 自动部署

### 6.1 创建部署工作流

```bash
mkdir -p .github/workflows
cat > .github/workflows/hugo.yml << 'EOF'
name: Deploy Hugo site to Pages

on:
  push:
    branches: ["master"]
  workflow_dispatch:

permissions:
  contents: read

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
      HUGO_VERSION: 0.165.0          # 与本地 install-hugo.sh 保持一致
    steps:
      - name: Install Hugo CLI
        run: |
          wget -O ${{ runner.temp }}/hugo.deb https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb \
          && sudo dpkg -i ${{ runner.temp }}/hugo.deb

      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0              # 主题已内嵌，无需 submodules

      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v5
        with:
          enablement: true            # 首次自动把 Pages 切到 GitHub Actions

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
    permissions:                     # 权限下沉到 job 级，避免首次部署的 OIDC 竞态
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v5
EOF
```

> 关键点：主题**内嵌**在仓库里，所以**不需要** `submodules: recursive`；`--baseURL` 由 GitHub 自动注入，避免环境不一致；`deploy` job 单独声明 `pages: write` + `id-token: write`，这是首轮部署不报 `id-token` 错误的关键。

### 6.2 提交并推送

```bash
git add -A
git commit -m "Initial Hugo site with Blowfish"
git branch -M master
git remote add origin git@github.com:yourusername/yourusername.github.io.git
git push -u origin master
```

（把 `yourusername` 两处都替换为你的 GitHub 用户名；分支名用 `master` 还是 `main` 都行，只要和 `.github/workflows/hugo.yml` 里的 `branches` 一致）

### 6.3 开启 Pages 的 Actions 部署源

推送后，到 GitHub 网页操作：

1. 打开仓库 → **Settings → Pages**
2. Source 选择 **GitHub Actions**（不是 Deploy from a branch）
3. 保存

**验证**：
1. 仓库 → Actions 标签页 → 能看到 "Deploy Hugo site to Pages" 工作流在运行，约 1-2 分钟变绿
2. 打开 `https://yourusername.github.io/` → 看到和本地预览一样的站点

**失败修复**：
- Actions 报错 `theme not found` / 网站无样式 → 确认 `themes/blowfish` 已提交进仓库（不是 submodule、也不该被 `.gitignore` 忽略）
- Actions 报 `Ensure GITHUB_TOKEN has permission "id-token: write"` → `deploy` job 缺权限声明，按 6.1 补上 `pages: write` + `id-token: write` 后 Re-run
- Actions 红色失败 → 点进去看日志，最常见是 Hugo 版本与主题不兼容：把 `HUGO_VERSION` 改为本地 `hugo version` 显示的版本号（Blowfish v3.8 需 ≥ 0.162）
- 站点 404 → 确认仓库名 exactly 是 `用户名.github.io`；确认 Settings → Pages 的 Source 是 GitHub Actions；首次部署等 1-3 分钟
- 样式丢失/链接全错 → `baseURL` 配置不对，检查 `config/_default/hugo.toml` 结尾是否有 `/`

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
4. 同时把 `config/_default/hugo.toml` 的 `baseURL` 改为 `https://yourname.dev/`，提交推送

**验证**：`curl -I https://yourname.dev` 返回 200，浏览器访问正常且带锁标志。

**失败修复**：DNS 超过 24 小时未生效 → 用 `dig yourname.dev` 检查记录是否生效；确认没有冲突的 AAAA 记录。

---

## 第 8 步：日常写作工作流

本仓库已封装成两个脚本（比手工敲命令更快，且自带防呆检查）：

```bash
./scripts/new-post.sh "My Topic"        # 1. 新建（自动套四段式骨架，文件名自动生成，draft: true）
hugo server -D                          # 2. 本地预览 http://localhost:1313
./scripts/publish.sh content/posts/my-topic.md   # 3. 翻转草稿 → 提交 → 推送
```

不用脚本时的手工等价写法：

```bash
hugo new posts/my-topic.md              # 新建
# ... 写 Markdown，写完把 draft 改为 false ...
git add -A && git commit -m "Add post: my-topic" && git push   # 推送
# 约 1 分钟后线上自动更新，Actions 标签页可看部署状态
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
| 站内搜索 | Blowfish 已自带（顶栏放大镜，Fuse.js） | — |
| 多语言预留 | Hugo 原生支持多语言，加 `languages.zh.toml` + `menus.zh.toml` 即可 | 需要时再开 |

---

## 故障速查表

| 症状 | 最可能原因 | 修复 |
|---|---|---|
| 本地预览正常，线上 404 | Pages Source 未设为 GitHub Actions | Settings → Pages → Source 改 GitHub Actions |
| 线上页面裸奔无样式 | `themes/blowfish` 没提交进仓库 | 确认主题目录已 `git add`，且不在 `.gitignore` 里 |
| 构建报 `can't evaluate field Locale` | Hugo 版本低于 0.162 | `HUGO_VERSION` 与本地都升到 0.165.0 |
| 文章本地有线上没有 | `draft: true` 或日期在未来 | 改 draft: false，修正 date |
| 链接/图片全 404 | baseURL 错误 | 检查 `config/_default/hugo.toml` 的 baseURL 与结尾 `/` |
| Actions 红色 | Hugo 版本与主题不兼容 | HUGO_VERSION 对齐本地版本 |
| 自定义域名不生效 | DNS 未生效或记录错误 | `dig yourname.dev` 排查 |
