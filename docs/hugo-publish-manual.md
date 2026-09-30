# Hugo 发布手册（xiongpin.dev）

> 目标：用 Hugo 管理站点，**push 到 master 即自动发布**，无需本地构建产物。
> 现状：**已全流程上线并验证**（Hugo 0.165.0 + Blowfish v3.8.0，Medium 风格阅读排版，GitHub Actions 自动部署，线上 <https://xiongpin.dev> 已是 Hugo 版本）。
> 你的仓库：`/Users/pinxiong/Documents/Important/pinxiong.github.io`
> 线上地址：https://xiongpin.dev

---

## 一、已经帮你做完的事

| 项目 | 状态 |
|---|---|
| 仓库从 Jekyll 迁移到 Hugo | ✅ 已推送并上线 |
| 主题由 PaperMod 换成 **Blowfish v3.8.0** | ✅ 已内嵌到 `themes/blowfish`（原始上游版本，未改动，可直接替换） |
| Medium 风格阅读排版 | ✅ `assets/css/custom.css`（衬线正文 + ~672px 版心 + 安静的代码块） |
| 四段式文章模板 | ✅ `archetypes/posts.md`（Problem / Context / Diagnosis / Fix / Lessons） |
| GitHub Actions 自动部署 | ✅ 已跑绿（`.github/workflows/hugo.yml`） |
| Pages 构建方式 | ✅ 已自动切换为 **GitHub Actions**（无需手工设置） |
| 自定义域名保护 | ✅ `static/CNAME` = `xiongpin.dev`（每次部署都不会丢域名） |
| 发布脚本 | ✅ `scripts/new-post.sh` + `scripts/publish.sh` |
| 本地 Hugo | ✅ 已升级到 0.165.0（旧版备份在 `/usr/local/bin/hugo-0.152.1.bak`） |
| 线上验收 | ✅ 首页/文章列表/搜索/标签/RSS/sitemap/robots 全部 200，www 301 → apex |

**现在没有任何待办的网页操作**——你只需要开始写。

---

## 二、仓库结构（你只需要关心 3 个目录）

```
pinxiong.github.io/
├── config/_default/                 ← 站点配置（按 Blowfish 约定的拆分布局）
│   ├── hugo.toml                    ←   baseURL / 分类法 / 输出格式 / Hugo 最低版本
│   ├── params.toml                  ←   主题参数（配色/首页/文章页/列表页）
│   ├── languages.en.toml            ←   标题/描述/作者资料/社交链接
│   ├── menus.en.toml                ←   顶部菜单（Posts、About）
│   └── markup.toml                  ←   goldmark + 代码高亮设置
├── content/
│   ├── _index.md                    ← 首页简介（显示在 profile 头部下方）
│   ├── posts/                       ← 文章放这里（*.md）
│   │   ├── _index.md                ← 文章列表页（按年份分组）
│   │   └── hello-and-why-this-site-exists.md
│   └── about.md                     ← About 页
├── assets/css/custom.css            ← 站点排版（最后加载，覆盖主题默认样式）
├── static/
│   └── CNAME                        ← 域名文件（勿删），另有一份在仓库根目录
├── archetypes/posts.md              ← 新文章模板（四段式骨架）
├── scripts/
│   ├── new-post.sh                  ← 新建文章（自动套模板 + 生成文件名）
│   ├── publish.sh                   ← 一键发布（翻转草稿 + 提交 + 推送）
│   └── install-hugo.sh              ← 新机器装 Hugo（版本与 CI 对齐）
├── themes/blowfish/                 ← 主题（原始上游内嵌，版本见 BLOWFISH_VERSION）
├── .devcontainer/                   ← Codespaces / Dev Container 定义
├── README.md                        ← 仓库内速查说明
└── .github/workflows/hugo.yml       ← 自动部署流程
```

> **没有** `content/archives.md` 和 `content/search.md` 了。Blowfish 的搜索是顶栏那个放大镜
> （Fuse.js 读 `index.json`），文章列表 `/posts/` 本身按年份分组，就等于归档页。

---

## 三、Pages 构建方式（已自动完成，无需操作）

首轮部署时，CI 里的 `actions/configure-pages` 带 `enablement: true`，已经自动把 Pages 切成 **GitHub Actions** 构建，所以这一步**你不用做**（线上已是 Hugo 版本即为证据）。

只在部署报错时手动确认一次：

1. 仓库页面 → **Settings**（仓库的 Settings，不是账号的）
2. 左侧菜单 → **Pages**
3. **Build and deployment → Source** 应为 **`GitHub Actions`**
4. 不要动 **Custom domain**（应仍是 `xiongpin.dev`，并勾选 Enforce HTTPS）

---

## 四、发布历史（存档，供排查时对照）

**首轮上线**：推送 `bddf52e → cf9696c` 触发构建，build 成功、deploy 成功，线上从 Jekyll 切到 Hugo。

首轮曾失败一次，报错为：

```
Error: Ensure GITHUB_TOKEN has permission "id-token: write".
```

**原因**：Pages 站点是在同一轮里刚被 `configure-pages` 启用的，部署作业拿不到 OIDC 令牌。
**修复**：把权限声明下沉到 job 级（`deploy` job 显式声明 `pages: write` + `id-token: write`），并把 `deploy-pages` 升到 `v5`。第二次推送即通过。

**主题迁移**：由 PaperMod v8.0 换成 Blowfish v3.8.0。Blowfish v3.8 用到 `site.Language.Locale`（Hugo ≥ 0.162 才有），因此把 Hugo 从 0.152.1 升到 0.165.0（CI、本地、`install-hugo.sh` 三处同步）。PaperMod 时代打的三个主题补丁（`opengraph.html` / `twitter_cards.html` / `schema_json.html`）随主题一起删除，不再需要。

**验收命令**（现在随时可跑）：

```bash
curl -s https://xiongpin.dev | grep -o "<title>[^<]*</title>"
# 期望：<title>Pin Xiong</title>
```

---

## 五、日常写作流程（两条命令）

### 1. 新建文章

```bash
cd /Users/pinxiong/Documents/Important/pinxiong.github.io
./scripts/new-post.sh "How I Cut EC2 Cold Start by 40%"
```

它会用标题生成文件名（`how-i-cut-ec2-cold-start-by-40.md`），自动套用四段式模板（Problem → Context → Diagnosis → Fix → Lessons），并默认 `draft: true`（草稿，推送也不会发布）。

### 2. 写作 + 本地预览

```bash
hugo server -D
# 打开 http://localhost:1313 实时预览（-D 表示包含草稿）
```

边写边看，保存后浏览器自动刷新。**预览时不要加 `--baseURL`**，否则 canonical 会变成 localhost。

写完后把 `summary`（列表页摘要）和 `tags` 填上——这两项影响列表页展示和社交卡片。

### 3. 发布（一条命令）

```bash
./scripts/publish.sh content/posts/how-i-cut-ec2-cold-start-by-40.md
```

它做三件事：把 `draft: true` 改成 `false` → 提交 → 推送到 master。推送即发布，Actions 自动构建，约 1 分钟线上可见。

脚本还有两道保护：

- 若 front matter 被改坏（比如 `draft` 那行格式异常），会**拒绝提交**并提示你先 `head -10` 检查；
- 若有其他文章仍是草稿，会列出来提醒你"这些不会发布"。

> 也可以不用脚本，手工三步等价：改 `draft: false` → `git add -A && git commit -m "..."` → `git push origin master`。
> **不要**提交 `public/`（已在 `.gitignore` 中忽略），构建由 CI 完成。

---

## 六、文章 front matter 说明

```yaml
---
title: "Your post title"
date: 2026-10-01T09:00:00+08:00
draft: false                        # 必须改成 false 才会发布
summary: "一句话摘要，会显示在列表页和社交卡片上"
tags: ["aws", "networking"]
categories: ["Engineering"]         # 当前文章页不展示分类，可留作内部分组
series: []                          # 系列名，同系列的文章会互相链接
showTableOfContents: true           # 显示目录（长文建议开）
---
```

可选进阶字段：

```yaml
canonicalURL: "https://dev.to/your-post"   # 反向：如果你先在别处首发
externalUrl: "https://..."                 # 该条跳转到外部而不在站内渲染
showRelatedContent: false                  # 单篇关闭"相关文章"
showAuthor: false                          # 单篇隐藏作者块
cover:
  image: "images/cover.png"                # 封面图，放 static/images/ 或资源页包
  alt: "描述"
  caption: "图注"
```

> 旧 PaperMod 的 `ShowToc` / `TocOpen` 已废弃，统一用 Blowfish 的 `showTableOfContents`。

### 插入视频（视频材料场景）

Blowfish 自带两个 shortcode，直接写在正文里：

```markdown
{{</* youtubeLite id="dQw4w9WgXcQ" */>}}     <!-- 点封面才加载的 YouTube 嵌入，很快 -->
{{</* video src="clip.mp4" */>}}              <!-- 自托管视频，文件放 static/ -->
```

`youtubeLite` 只在读者点击时才拉起 YouTube iframe，避免开屏就把第三方脚本拖进来。

---

## 七、主题与排版（想改外观时看这里）

**主题是原封不动内嵌的上游版本。** `themes/blowfish/` 就是 [nunocoracao/blowfish](https://github.com/nunocoracao/blowfish) 的原始拷贝，版本号写在 `themes/blowfish/BLOWFISH_VERSION`（当前 `v3.8.0`）。用内嵌而不是 submodule/module，好处是 `git clone` 直接能构建、不需要 Go 工具链；升级就是整个文件夹换掉。

**站点外观全部在 `assets/css/custom.css`。** Blowfish 会把它拼在自己编译好的 CSS **之后**，所以里面的规则天然覆盖主题，不用改主题文件。Medium 风格的来源就在这里：

- 正文用衬线字体（`charter` → `Bitstream Charter` → `Georgia` 栈），约 21px，行高 1.62；
- 版心约 672px（`42rem`），接近 Medium 的阅读宽度；
- 标题保持无衬线，与正文拉开对比；
- 代码块只保留**一层**外框：边框画在 `.highlight-wrapper` 上，`.highlight` 和 `pre` 的边框/圆角全部清零。Blowfish 是三层嵌套（`wrapper > highlight > pre`），框超过一层就会画出重影边框和空缝。

**更新主题的推荐方式**（保持可回滚）：

```bash
cd /Users/pinxiong/Documents/Important/pinxiong.github.io
cp -R themes/blowfish /tmp/blowfish-backup      # 先备份当前可用版本
# 下载新版解压到 /tmp，用新目录替换 themes/blowfish（保留 BLOWFISH_VERSION）
hugo server -D                                  # 本地验证没问题再提交
```

> 如果新版本改了 CSS 类名，`custom.css` 里的选择器需要跟着调——所以务必本地预览过再推。

---

## 八、SEO 与分发的关键点（和你之前的策略对齐）

| 项目 | 当前状态 | 说明 |
|---|---|---|
| canonical 链接 | ✅ 自动指向 `https://xiongpin.dev/...` | 分发到 Dev.to / Medium 的副本设 canonical 指回这里，权重记在你域名下 |
| sitemap.xml | ✅ 自动生成 | 提交到 Google Search Console 可加速收录 |
| robots.txt | ✅ 允许抓取并声明 sitemap | 无需改动 |
| RSS feed | ✅ `https://xiongpin.dev/index.xml` | 订阅与自动分发都用它 |
| 社交分享卡片 | ✅ OpenGraph/Twitter Card 已启用 | 分享到 LinkedIn/X 时自动带标题和摘要，可分享渠道配在 `params.toml` 的 `sharingLinks` |

后续建议（不急）：

1. 建 Google Search Console，提交 `https://xiongpin.dev/sitemap.xml`
2. 加 favicon：把图标放进 `static/`，文件名用 `favicon.ico`、`favicon-32x32.png`
3. 加统计：在 `config/_default/params.toml` 里补 Blowfish 的 `[analytics]` 配置块（支持 Fathom / Plausible / Umami / Google Analytics）
4. 中文文章若要做，加 `languages.zh.toml` + `menus.zh.toml` 即可开多语言

---

## 九、故障速查表

| 现象 | 原因 | 修复 |
|---|---|---|
| Actions 报 `Pages site is not configured to use GitHub Actions` | Source 不是 GitHub Actions | 做第三节的确认，然后 Re-run |
| Actions 报 `Ensure GITHUB_TOKEN has permission "id-token: write"` | 首次启用 Pages 与部署同轮的竞态；或权限没下沉到 job 级 | 现在工作流已在 `deploy` job 显式声明权限，直接 **Re-run all jobs** 即可通过 |
| 构建报 `can't evaluate field Locale in type *langs.Language` | Hugo 版本低于 0.162，满足不了 Blowfish v3.8 | 确认 `hugo version` ≥ 0.165.0；CI 里改 `.github/workflows/hugo.yml` 的 `HUGO_VERSION`，本地跑 `./scripts/install-hugo.sh` |
| `publish.sh` 报 `Front matter looks broken` | `draft` 那行的格式被改坏（例如 `draft: falsesummary: ""`，行尾换行被吃掉） | `head -10 content/posts/xxx.md` 检查，手工恢复 `---` 包裹与逐行键值，再重跑 |
| 线上源码里 grep 不到 `canonical="..."` | HTML 被压缩，属性引号被去掉，属**正常现象** | 用宽松写法验证：`curl -s https://xiongpin.dev \| grep -oE '<link rel=canonical[^>]*>'` |
| 代码块出现双层边框/中间空缝 | 边框同时画在了 `pre` / `.highlight` / `.highlight-wrapper` 上 | 只留 `.highlight-wrapper` 一层框，另外两层 `border: none`（见 `custom.css`） |
| 页面看起来是裸露 HTML，没有主题样式 | `themes/blowfish` 为空，或缺 `assets/css/custom.css` | 确认 `themes/blowfish/layouts` 存在且 `config/_default/hugo.toml` 里 `theme = "blowfish"` |
| 本地 `hugo` 报需求版本过高 | 用到旧版 Hugo | `hugo version` 应为 0.165.0；若不对，跑 `./scripts/install-hugo.sh` |
| 页面 404，但 `pinxiong.github.io` 能开 | CNAME 丢失或 Pages 源设错 | 确认 `static/CNAME` 内容为 `xiongpin.dev`，且 Source = GitHub Actions |
| 推送后网站没变化 | Actions 未触发或失败 | 看 Actions 标签页；`git push --force` 不是解决办法 |
| 文章推送了但线上没有 | 该文章仍是 `draft: true` | 改成 `false` 再推；`publish.sh` 会列出所有未发布草稿 |
| `git commit` 报 `index.lock: File exists` | VS Code 的 Git 集成正在刷新（会短暂占用） | 等 3 秒重试；仍失败则删除该锁文件（0 字节才可删） |
| `hugo server` 报端口占用 | 1313 被上次的进程占用 | `pkill -f "hugo server"` 后重试，或换端口 `-p 1314` |

---

## 十、一句话回顾

**写**：`./scripts/new-post.sh "标题"` → 编辑 → `hugo server -D` 预览
**发**：`./scripts/publish.sh content/posts/xxx.md` → 自动翻转草稿并推送 → 约 1 分钟线上可见
**改外观**：只动 `assets/css/custom.css`，别改 `themes/blowfish`
**沉淀**：所有 Markdown 源文件在你的 Git 仓库里，域名权重、RSS、sitemap 全部归你，平台只是分发管道
