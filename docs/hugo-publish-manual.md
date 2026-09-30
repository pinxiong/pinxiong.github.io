# Hugo 发布手册（xiongpin.dev）

> 目标：用 Hugo 管理站点，**push 到 master 即自动发布**，无需本地构建产物。
> 现状：**已全流程上线并验证**（Hugo 0.152.1 + PaperMod v8.0，GitHub Actions 自动部署，线上 <https://xiongpin.dev> 已是 Hugo 版本）。
> 你的仓库：`/Users/pinxiong/Documents/Important/pinxiong.github.io`
> 线上地址：https://xiongpin.dev

---

## 一、已经帮你做完的事

| 项目 | 状态 |
|---|---|
| 仓库从 Jekyll 迁移到 Hugo | ✅ 已推送并上线 |
| PaperMod v8.0 主题 | ✅ 已内嵌到 `themes/PaperMod`（可直接改，无需网络拉取） |
| 四段式文章模板 | ✅ `archetypes/posts.md`（Problem / Diagnosis / Fix / Lessons） |
| GitHub Actions 自动部署 | ✅ 已跑绿（`.github/workflows/hugo.yml`） |
| Pages 构建方式 | ✅ 已自动切换为 **GitHub Actions**（无需手工设置） |
| 自定义域名保护 | ✅ `static/CNAME` = `xiongpin.dev`（每次部署都不会丢域名） |
| 发布脚本 | ✅ `scripts/new-post.sh` + `scripts/publish.sh` |
| 本地 Hugo | ✅ 已升级到 0.152.1（旧版备份在 `/usr/local/bin/hugo-0.107.bak`） |
| 线上验收 | ✅ 首页/文章/归档/搜索/RSS/sitemap/robots 全部 200，www 301 → apex |

**现在没有任何待办的网页操作**——你只需要开始写。

---

## 二、仓库结构（你只需要关心 3 个目录）

```
pinxiong.github.io/
├── config.yaml                      ← 站点配置（标题/描述/菜单/社交链接）
├── content/
│   ├── posts/                       ← 文章放这里（*.md）
│   │   └── hello-and-why-this-site-exists.md
│   ├── about.md                     ← About 页
│   ├── archives.md                  ← 归档页
│   └── search.md                    ← 搜索页
├── static/
│   └── CNAME                        ← 域名文件（勿删）
├── archetypes/posts.md              ← 新文章模板（四段式骨架）
├── scripts/
│   ├── new-post.sh                  ← 新建文章（自动套模板 + 生成文件名）
│   └── publish.sh                   ← 一键发布（翻转草稿 + 提交 + 推送）
├── themes/PaperMod/                 ← 主题（已内嵌并修复）
├── README.md                        ← 仓库内速查说明
└── .github/workflows/hugo.yml       ← 自动部署流程
```

---

## 三、Pages 构建方式（已自动完成，无需操作）

首轮部署时，CI 里的 `actions/configure-pages` 带 `enablement: true`，已经自动把 Pages 切成 **GitHub Actions** 构建，所以这一步**你不用做**（线上已是 Hugo 版本即为证据）。

只在部署报错时手动确认一次：

1. 仓库页面 → **Settings**（仓库的 Settings，不是账号的）
2. 左侧菜单 → **Pages**
3. **Build and deployment → Source** 应为 **`GitHub Actions`**
4. 不要动 **Custom domain**（应仍是 `xiongpin.dev`，并勾选 Enforce HTTPS）

---

## 四、首次发布（已完成 ✅）

首轮推送 `bddf52e → cf9696c` 触发构建，**build 成功、deploy 成功**，线上已从 Jekyll 切到 Hugo。

首轮曾失败一次，报错为：

```
Error: Ensure GITHUB_TOKEN has permission "id-token: write".
```

**原因**：Pages 站点是在同一轮里刚被 `configure-pages` 启用的，部署作业拿不到 OIDC 令牌。
**修复**：把权限声明下沉到 job 级（`deploy` job 显式声明 `pages: write` + `id-token: write`），并把 `deploy-pages` 升到 `v5`。第二次推送即通过。

**验收命令**（现在随时可跑）：

```bash
curl -s https://xiongpin.dev | grep -o "<title>[^<]*</title>"
# 期望：<title>Xiong Pin</title>
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
draft: false              # 必须改成 false 才会发布
summary: "一句话摘要，会显示在列表页和社交卡片上"
tags: ["aws", "networking"]
categories: ["Engineering"]
ShowToc: true             # 显示右侧目录（长文建议开）
TocOpen: false
---
```

可选进阶字段：

```yaml
canonicalURL: "https://dev.to/your-post"   # 反向：如果你先在别处首发
cover:
  image: "/images/cover.png"               # 封面图，放 static/images/
  alt: "描述"
```

---

## 七、SEO 与分发的关键点（和你之前的策略对齐）

| 项目 | 当前状态 | 说明 |
|---|---|---|
| canonical 链接 | ✅ 自动指向 `https://xiongpin.dev/...` | 分发到 Dev.to / Medium 的副本设 canonical 指回这里，权重记在你域名下 |
| sitemap.xml | ✅ 自动生成 | 提交到 Google Search Console 可加速收录 |
| robots.txt | ✅ 允许抓取并声明 sitemap | 无需改动 |
| RSS feed | ✅ `https://xiongpin.dev/index.xml` | 订阅与自动分发都用它 |
| 社交分享卡片 | ✅ OpenGraph/Twitter Card 已启用 | 分享到 LinkedIn/X 时自动带标题和摘要 |

后续建议（不急）：
1. 建 Google Search Console，提交 `https://xiongpin.dev/sitemap.xml`
2. 加 favicon：把图标放进 `static/`，命名 `favicon.ico`、`favicon-32x32.png`（配置已预留）
3. 加统计：PaperMod 支持 Google Analytics（在 `config.yaml` 加 `services.googleAnalytics.ID`）

---

## 八、故障速查表

| 现象 | 原因 | 修复 |
|---|---|---|
| Actions 报 `Pages site is not configured to use GitHub Actions` | Source 不是 GitHub Actions | 做第三节的确认，然后 Re-run |
| Actions 报 `Ensure GITHUB_TOKEN has permission "id-token: write"` | 首次启用 Pages 与部署同轮的竞态；或权限没下沉到 job 级 | 现在工作流已在 `deploy` job 显式声明权限，直接 **Re-run all jobs** 即可通过 |
| `publish.sh` 报 `Front matter looks broken` | `draft` 那行的格式被改坏（例如 `draft: falsesummary: ""`，行尾换行被吃掉） | `head -10 content/posts/xxx.md` 检查，手工恢复 `---` 包裹与逐行键值，再重跑 |
| 线上源码里 grep 不到 `canonical="..."` | HTML 被压缩，属性引号被去掉，属**正常现象** | 用宽松写法验证：`curl -s https://xiongpin.dev \| grep -oE '<link rel=canonical[^>]*>'` |
| Actions 报 `partial "partials/.../_funcs/..." not found` | 主题被更新，补丁丢失 | 见第九节：重新打补丁 |
| Actions 报 `.Site.Social was deprecated...` | `config.yaml` 里的 `params.social` 被删了 | 恢复该配置块 |
| 本地 `hugo` 报 `v0.112.4 or greater is required` | 用到了旧版 Hugo | `hugo version` 应为 0.152.1；若不对，用 `/usr/local/bin/hugo-0.107.bak` 之外的正确版本 |
| 页面 404，但 `pinxiong.github.io` 能开 | CNAME 丢失或 Pages 源设错 | 确认 `static/CNAME` 内容为 `xiongpin.dev`，且 Source = GitHub Actions |
| 推送后网站没变化 | Actions 未触发或失败 | 看 Actions 标签页；`git push --force` 不是解决办法 |
| 文章推送了但线上没有 | 该文章仍是 `draft: true` | 改成 `false` 再推；`publish.sh` 会列出所有未发布草稿 |
| `git commit` 报 `index.lock: File exists` | VS Code 的 Git 集成正在刷新（会短暂占用） | 等 3 秒重试；仍失败则删除该锁文件（0 字节才可删） |
| `hugo server` 报端口占用 | 1313 被上次的进程占用 | `pkill -f "hugo server"` 后重试，或换端口 `-p 1314` |

---

## 九、关于主题补丁（重要，将来更新主题时会用到）

PaperMod v8.0 有三处调用在新版 Hugo 里已失效，我已经修好并保存在仓库里。**如果将来你要更新主题，这三处需要重新打补丁**：

1. `themes/PaperMod/layouts/partials/templates/opengraph.html`
2. `themes/PaperMod/layouts/partials/templates/twitter_cards.html`
3. `themes/PaperMod/layouts/partials/templates/schema_json.html`

把其中的 `partial "partials/templates/_funcs/get-page-images"` 改成 `partial "templates/_funcs/get-page-images"`（去掉多余前缀）。
另外 `config.yaml` 里的 `params.social` 块不要删，它让主题跳过已被 Hugo 移除的旧代码路径。

**更新主题的推荐方式**（保持可回滚）：

```bash
cd /Users/pinxiong/Documents/Important/pinxiong.github.io
cp -R themes/PaperMod /tmp/PaperMod-backup     # 先备份当前可用版本
# 下载新版到 /tmp，替换 themes/PaperMod，然后重新打上面三处补丁
hugo server -D                                  # 本地验证没问题再提交
```

---

## 十、一句话回顾

**写**：`./scripts/new-post.sh "标题"` → 编辑 → `hugo server -D` 预览
**发**：`./scripts/publish.sh content/posts/xxx.md` → 自动翻转草稿并推送 → 约 1 分钟线上可见
**沉淀**：所有 Markdown 源文件在你的 Git 仓库里，域名权重、RSS、sitemap 全部归你，平台只是分发管道
