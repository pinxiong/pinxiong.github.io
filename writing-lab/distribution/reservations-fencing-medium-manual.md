# Medium 发布手册 · UC05 · When "Not Found" Doesn't Mean "Never Happened"

> 系列：strands-in-action 第 5 篇 ｜ 状态：**四渠道全部上线**（主站 / Builder Center / Dev.to 于 2026-11-09 21:30 窗口发布；Medium 于 2026-11-10 手动 Import 完成）
> 日期：2026-11-10（Medium URL 当日回填）

**线上地址**

| 渠道 | 链接 |
|---|---|
| 主站（canonical） | https://xiongpin.dev/posts/reservations-fencing/ |
| AWS Builder Center | https://builder.aws.com/content/3Ls8Su63RbuSKR3yys1j9t6US1p/when-not-found-doesnt-mean-never-happened |
| Dev.to | https://dev.to/aws-builders/when-not-found-doesnt-mean-never-happened-2eie |
| Medium | https://medium.com/@pinxiong.cn/when-not-found-doesnt-mean-never-happened-1bc3e54bd912 |

Medium 只能手动操作，约 5 分钟。按下面 7 步走。

---

## 第 1 步：Import（从 canonical 导入）

打开 <https://medium.com/p/import> → 粘贴 `https://xiongpin.dev/posts/reservations-fencing/` → Import。

导入结果一定是一篇 draft，不会自动发布。Import 会带过来标题、正文、1 张正文图和 16 个代码块，**但 subtitle 永远是空的，必须手填**。

---

## 第 2 步：Title 与 Subtitle（本手册重点）

**Title（导入后应已是这个，核对即可）**

```text
When "Not Found" Doesn't Mean "Never Happened"
```

**Subtitle：手填，从下面 4 个里选一个（字符数已逐条数过，全部 ≤ 140 上限）**

| 选项 | 字符数 | 副标题 |
|---|---|---|
| **① 推荐** | **136** | `The janitor released capacity at 1.003s. The retry committed at 1.407s. The old attempt landed at 2.405s. Five runs, five double writes.` |
| ② 讲语义 | 131 | `A lease expiry proves only that a worker stopped reporting. In five real-clock runs, "not found" turned into two writes every time.` |
| ③ 讲修复 | 131 | `Splitting "expired" into "confirmed existing" and "outcome_unknown" stopped every duplicate write. Here are the runs that show why.` |
| ④ 最紧凑 | 69 | `Five runs. Five duplicate writes. One missing state: outcome_unknown.` |

**为什么推荐 ①**

- **三个时间戳直接排出因果**：1.003s 释放容量 → 1.407s 重试提交 → 2.405s 旧 attempt 才落地。读者不用读正文就知道「查不到」为什么会变成两次写；这是全文最硬的一组实测数字。
- **结尾给出次数**（five runs, five double writes），把反差坐实成可复现的结果，而不是一个假设的竞态。
- **不重复标题原话**，也不含 `outcome_unknown` 这类内部术语，Medium 列表页读者无需前置知识。
- 136 字符贴着 140 上限，移动端一般不截断；若你担心被截，改用 ④（69 字符）。

② 把结论前置，适合想强调「lease 到底证明了什么」的读者，但没有具体时间线，冲击力弱一点。③ 直接剧透解法（`outcome_unknown`），会把「先看到失败、再找状态」的阅读张力抹掉；只在你想吸引已经踩过坑的工程师时用。④ 最安全、最不容易截断，但数字太干，少了那 2.4 秒的荒谬感。

**操作**：在 Medium 编辑器里，标题下方灰色的 "Write a subtitle..." 处粘贴所选文本（切勿粘成正文段落，否则不会样式化为副标题）。

---

## 第 3 步：Byline 首行

正文第一行（Import 一般不会自动加，需手写）：

```text
Originally published at https://xiongpin.dev/posts/reservations-fencing/ on 2026-11-09.
```

把 `https://xiongpin.dev/posts/reservations-fencing/` 选中做成超链接，指向自身。

---

## 第 4 步：封面图

上传：`pinxiong.github.io/static/images/reservations-fencing/cover-medium.png`（**1400×788，16:9**，源 SVG 同目录 `cover-medium.svg`）。

上传后在 Medium 的 "Change thumbnail" 里确认显示的是整张图、三行标题文字没被裁掉。

> **注意**：BC 线上 2026-11-09 上传的是当时的 1400×735（1.90:1）版本，已在平台上正常显示、不会自动更新。本地 `cover-medium.png` 已于 2026-11-10 重做成 16:9；**Medium 用这个新文件即可，不必回 BC 重传**。

---

## 第 5 步：标签（5 个，与前两篇同口径）

```text
AI · Agents · AWS · Strands · Software Engineering
```

Medium 最多 5 个，按上面顺序填，前两个权重最高。

---

## 第 6 步：正文核对清单（逐项过）

1. **正文图只有 1 张**：`race-timeline.png`（延迟提交竞态时间线，位于 "The retry that arrives too early" 一节）。这张图是全文唯一的配图，缺了就说明 Import 没抓全，回主站对应位置重新复制。别按 UC03/UC04 的习惯去找 6–7 张图，本篇确实只有一张。
2. **16 个代码块**：Python 与终端输出块都要有等宽字体和灰底；被 Import 拍平成段落的，全选那段 → 工具栏 `</>` 重新设为 code block。特别检查 `SUMMARY trials=5 duplicate_writes_total=5 ...` 那几行，别被拆成多段。
3. **状态机 ASCII 图**（`reserved ──expiry──▶ outcome_unknown`）：这是纯文本块，应保持等宽对齐，不能被转成普通段落。
4. **引用行**：开头的 `> Verified on 2026-11-09 against strands-agents 1.63.0 ...` 应显示为引用样式（左侧竖线）。
5. 全文搜一遍 `](` 和 `![`，确认没有 Markdown 残留符号（Import 偶尔漏转）。
6. 结尾的系列预告（"the series now moves to orchestration"）和 article 01 链接必须保留，不要当成草稿尾巴删掉。

---

## 第 7 步：Advanced settings → Publish

点右上 `Publish` 前，先开 `Advanced settings`：

- [ ] **"This story was originally published elsewhere"** 勾上
- [ ] Canonical 链接填 **`https://xiongpin.dev/posts/reservations-fencing/`**（带结尾斜杠，与上表完全一致）
- [ ] 留空 canonical = 把 SEO 让给 Medium，停下先修

然后 Publish。发布后做两件事：

1. 打开线上文章，确认标题下方显示的是你选的 subtitle、封面是 16:9 那张、canonical 指回 xiongpin.dev；
2. 把 Medium URL 回填到本文件顶部表格、`reservations-fencing-slack.md` 的 `<MEDIUM_URL>` 占位，以及 `strands-in-action/PIPELINE_STATE.md` 的 Medium 台账行。

**本篇执行结果（2026-11-10）**：Medium URL 由 Pin 提供，已回填本表、`reservations-fencing-slack.md`（A 版与 C 版）、`PIPELINE_STATE.md` 的 Medium 台账行及 `usecases/05-reservations-fencing/publish/README.md`。`medium.com` 在本机网络不可达，未做页面抓取核验；subtitle / 封面 / canonical 三项请以 Medium 线上页面为准确认一次。
