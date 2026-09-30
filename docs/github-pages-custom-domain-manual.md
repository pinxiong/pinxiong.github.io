# GitHub Pages 绑定自有域名完整手册

> 目标：把 `yourusername.github.io` 绑定到你自己申请的域名（如 `yourname.dev`），全站 HTTPS。
> 前提：GitHub Pages 站点已能通过 `yourusername.github.io` 正常访问（见《GitHub Pages 完整搭建手册》前 6 步）。
> 全程约 20 分钟操作 + DNS 生效等待（5 分钟～24 小时，通常 1 小时内）。

---

## 第 0 步：先理解两个概念（30 秒）

- **根域名（apex domain）**：`yourname.dev`，不带任何前缀。GitHub Pages 要求用 **4 条 A 记录**指向它的服务器。
- **子域名**：`www.yourname.dev`、`blog.yourname.dev`。用 **1 条 CNAME 记录**指向 `yourusername.github.io`。

最佳实践：**根域名和 www 都配上**，GitHub 会自动把其中一个 301 跳转到另一个，权重集中到一个地址。

---

## 第 1 步：购买域名（已有域名可跳过）

| 注册商 | 价格（.dev） | 适合你的理由 | 注意 |
|---|---|---|---|
| **AWS Route 53**（推荐，已有 AWS 账号时） | $12/年，续费同价 | 免外币信用卡、账单与现有 AWS 合并、控制台熟悉 | DNS 托管另收 $0.50/月/Hosted Zone + 微量查询费 |
| **Cloudflare** | ~$10-12/年，续费同价（成本价） | DNS 免费且生效极快、自带免费 CDN、送域名邮箱转发 | 需外币卡/PayPal |
| Porkbun | 首年 ~$9-11.5，续费 ~$13 | 首年便宜、界面友好 | 需外币卡/PayPal |
| 腾讯云 DNSPod / 阿里云万网 | **不支持 .dev** | 仅适合 .com/.cn 等后缀（.com 约 ¥75-78/年） | 国内注册商受工信部清单限制，.dev 不在其列；注册需实名认证 |

**重要说明**：
- 域名在国内注册 ≠ 需要备案。备案针对的是"服务器在中国大陆"，GitHub Pages 服务器在境外，**无需备案**。
- 想注册 `.dev` 只能走国际注册商（Route 53 / Cloudflare / Porkbun / Namecheap 等）；国内注册商清单里都没有该后缀（已核实腾讯云官方文档，2026-04 更新）。
- 注册信息建议用拼音/英文填写，邮箱填常用邮箱（找回和转移都靠它）。

**后缀建议**：技术博客首选 `.dev`（技术感强；.dev 在浏览器 HSTS 预加载列表中，强制 HTTPS，正好符合需求）、`.com`（通用）、`.me`（个人感）。避免冷门后缀（部分邮箱和防火墙会误判）。

**验证**：注册商控制台里能看到域名状态为"正常/Active"（Route 53 中为 Registered domains 列表出现该域名）。

---

## 第 2 步：配置 DNS 记录（按你的注册商选一节）

### 方案 B：AWS Route 53（.dev 推荐路径）

> 前提：已在 Route 53 注册域名（Console → Route 53 → Registered domains → Register domain）。注册完成后 AWS 会自动为该域名创建一个 Hosted Zone。

1. 打开 **Route 53 → Hosted zones**，点击你的域名（如 `yourname.dev`）
2. 点 **Create record**，添加以下记录（Simple routing，Record type 逐条选择）：

| Record name | Record type | Value |
|---|---|---|
| （留空，即根域名） | A | `185.199.108.153` `185.199.109.153` `185.199.110.153` `185.199.111.153`（4 个 IP 填在同一条记录的 Value 里，每行一个） |
| `www` | CNAME | `yourusername.github.io` |

3. TTL 保持默认 300，点 **Create records**
4. Hosted Zone 费用：$0.50/月 + 查询费（个人博客量级每月不到 $0.10），账单与 AWS 合并

> **注意**：Route 53 的 A 记录不要把 Record type 错选成 "A – Routes traffic to an IPv4 address **and some AWS resources**" 里的 Alias 开关——保持 **Alias 关闭**，Value 直接填 4 个 GitHub IP 即可。

### 方案 C：Cloudflare

1. 登录 Cloudflare → 选择你的域名 → 左侧 **DNS → Records**
2. 点 **Add record**，依次添加 5 条记录：

| 类型 | Name | 内容 | Proxy 状态 |
|---|---|---|---|
| A | `@` | `185.199.108.153` | **DNS only（灰色云）** |
| A | `@` | `185.199.109.153` | DNS only |
| A | `@` | `185.199.110.153` | DNS only |
| A | `@` | `185.199.111.153` | DNS only |
| CNAME | `www` | `yourusername.github.io` | DNS only |

3. 保存

> **初期务必用灰色云（DNS only）**。橙色云代理模式下 GitHub 的证书签发病例多，等 HTTPS 完全跑通后再考虑开代理。

### 方案 D：腾讯云 DNSPod

1. 登录 DNSPod 控制台 → 我的域名 → 点你的域名 → **记录管理 → 添加记录**
2. 添加 5 条：

| 主机记录 | 记录类型 | 记录值 |
|---|---|---|
| `@` | A | `185.199.108.153` |
| `@` | A | `185.199.109.153` |
| `@` | A | `185.199.110.153` |
| `@` | A | `185.199.111.153` |
| `www` | CNAME | `yourusername.github.io.`（结尾的点可省） |

3. TTL 保持默认 600 即可

### 方案 E：阿里云万网

1. 登录阿里云控制台 → 域名 → 解析设置 → **添加记录**
2. 记录内容与方案 D 完全相同（4 条 A + 1 条 CNAME）

> **方案 D / E 说明**：国内注册商无法注册 `.dev`，这两节仅在你使用 `.com`/`.cn` 等后缀时适用。

### 验证 DNS 已配好

```bash
dig yourname.dev +noall +answer -t A
# 应返回 4 条 A 记录，IP 为 185.199.108-111.153

dig www.yourname.dev +noall +answer -t CNAME
# 应返回 CNAME 指向 yourusername.github.io
```

**失败修复**：
- `dig` 查不到记录 → 刚配完等 5-10 分钟再查；还不行检查注册商控制台是否保存成功
- 查到旧 IP → 本地 DNS 缓存，`sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder` 后重查
- **如果存在 AAAA (IPv6) 记录且不是 GitHub 的 IP → 必须删掉**，这是自定义域名最常见的坑：浏览器优先走 IPv6 会连到错误服务器

---

## 第 3 步：仓库侧添加 CNAME 文件（关键，漏了会被部署覆盖）

在 Hugo 站点根目录执行：

```bash
echo "yourname.dev" > static/CNAME
git add static/CNAME
git commit -m "Add custom domain CNAME"
git push
```

**为什么是 `static/` 目录**：Hugo 构建时会把 `static/` 里的文件原样复制到站点根目录，这样每次部署都会带上 CNAME。如果只在 GitHub 网页上填域名而不加这个文件，**某些部署方式会清掉域名设置**，加了这个文件则双保险。

**验证**：推送后等 Actions 变绿，访问 `https://yourusername.github.io/CNAME` 能看到你的域名文本。

---

## 第 4 步：GitHub 侧绑定域名

1. 打开仓库 → **Settings → Pages**
2. **Custom domain** 输入框填：`yourname.dev` → 点 **Save**
3. GitHub 会自动做 DNS check：
   - ✅ 绿色提示 "DNS check successful" → 继续
   - ⚠️ 黄色/红色提示 → DNS 还没生效，等 10-60 分钟回来重试（点 Check again）
4. DNS check 通过后，勾选 **Enforce HTTPS**

> GitHub 会自动为你的域名签发免费证书（Let's Encrypt），签发需要几分钟到几小时。**证书签发完成前 "Enforce HTTPS" 是灰色不可勾选的，属正常现象，耐心等。**

**验证**：
```bash
curl -I https://yourname.dev
```
返回 `HTTP/2 200` 且浏览器访问带锁标志即成功。

**失败修复**：
- DNS check 一直失败 → 回到第 2 步用 `dig` 确认 4 条 A 记录都在；检查 Cloudflare 是否开了橙色云代理（先关掉）
- HTTPS 勾选项超过 24 小时仍灰色 → 在 Custom domain 框里删掉域名、Save、重新填入、Save，触发重新签发
- 浏览器提示证书错误 → 证书还在签发中，等 1 小时；超过 24 小时按上一条处理

---

## 第 5 步：更新 Hugo 配置（让 canonical 指向新域名）

编辑 `hugo.toml`：

```toml
baseURL = "https://yourname.dev/"
```

```bash
git add hugo.toml
git commit -m "Update baseURL to custom domain"
git push
```

**这一步的意义**：全站的 canonical 链接、sitemap、RSS 里的地址都会变成你的域名——**搜索引擎权重从此沉淀在你自己的域名上**，这正是整个资产策略的核心。

**验证**：等部署完成后，打开 `https://yourname.dev` 任意一篇文章，右键"查看网页源代码"，搜索 `canonical`，应看到：

```html
<link rel="canonical" href="https://yourname.dev/posts/xxx/">
```

---

## 第 6 步：整体验收清单

逐项打勾：

- [ ] `https://yourname.dev` 正常打开，带 HTTPS 锁
- [ ] `https://www.yourname.dev` 自动跳转到 `https://yourname.dev`（或反向，取决于 GitHub 配置）
- [ ] `https://yourusername.github.io` 自动跳转到你的自定义域名
- [ ] 文章页源码里 canonical 是自定义域名
- [ ] `https://yourname.dev/sitemap.xml` 可访问，URL 均为自定义域名
- [ ] `https://yourname.dev/index.xml`（RSS）可访问

全部通过 → 域名绑定完成。

---

## 故障速查表

| 症状 | 原因 | 修复 |
|---|---|---|
| 浏览器打不开，GitHub 提示 DNS check failed | DNS 未生效或记录错误 | `dig` 验证 4 条 A 记录；Cloudflare 关代理 |
| 部分访客打不开，部分能开 | 存在指向别处的 AAAA 记录 | 删除多余 AAAA 记录 |
| `ERR_CERT_*` 证书错误 | 证书签发中 | 等 1-24 小时；超时则删域名重填触发重签 |
| 网站开了但样式/链接错乱 | baseURL 没改成新域名 | 改 hugo.toml 第 5 步并推送 |
| www 能开、根域名不能开（或反之） | 只配了一种记录 | 4 条 A 和 CNAME 都要配 |
| 一段时间后域名设置消失 | 只填了网页设置，没加 CNAME 文件 | 补第 3 步的 `static/CNAME` |

---

## 后续可选：域名邮箱

有了自己的域名，可以顺便获得 `you@yourname.dev` 邮箱（放在 GitHub 主页和 LinkedIn 上非常专业）：

- **Cloudflare Email Routing**：免费，把域名邮箱转发到你的 Gmail/QQ 邮箱，5 分钟配好
- 发送端用 Gmail 的"添加其他电子邮件地址"功能配合 SMTP 即可
