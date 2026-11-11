# Medium 发布手册 · UC06 · Orchestrating Agents: Nobody Decides Who Goes Next

> 系列：strands-in-action 第 6 篇 ｜ 状态：**主站 / Dev.to / BC 已于 2026-11-11 21:30 窗口发布（21:36 / 21:37 / ≈21:50 GMT+8）；Medium 待手动 Import**
> 日期：2026-11-11（发布当档产出，Medium URL 待回填）

**线上地址**

| 渠道 | 链接 |
|---|---|
| 主站（canonical） | https://xiongpin.dev/posts/orchestrating-swarm/ |
| AWS Builder Center | https://builder.aws.com/content/3Lxn0RS1k0tiClcigN1xz5c0hH9 |
| Dev.to | https://dev.to/aws-builders/orchestrating-agents-nobody-decides-who-goes-next-2cg4 |
| Medium | <MEDIUM_URL>（手动 Import 后回填） |

Medium 只能手动操作，约 5 分钟。按下面 7 步走。

---

## 第 1 步：Import（从 canonical 导入）

打开 <https://medium.com/p/import> → 粘贴 `https://xiongpin.dev/posts/orchestrating-swarm/` → Import。

导入结果一定是一篇 draft，不会自动发布。Import 会带过来标题、正文、1 张正文图和 16 个代码块，**但 subtitle 永远是空的，必须手填**。

---

## 第 2 步：Title 与 Subtitle（本手册重点）

**Title（导入后应已是这个，核对即可）**

```text
Orchestrating Agents: Nobody Decides Who Goes Next
```

**Subtitle：手填，从下面 4 个里选一个（字符数已逐条数过，全部 ≤ 140 上限）**

| 选项 | 字符数 | 副标题 |
|---|---|---|
| **① 推荐** | **138** | `The swarm spent 8857 tokens and delivered eight words. The next run spent 8605 and delivered six. "Completed" means nobody asked for help.` |
| ② 讲机制 | 139 | `No scheduler, no route table. Routing is a model's tool call, and the swarm ends when the last node goes quiet. Verified on strands 1.63.0.` |
| ③ 讲失败 | 136 | `A handoff dies with the node that requested it. A broken tool does not stop the swarm. The runs that show why, on strands-agents 1.63.0.` |
| ④ 最紧凑 | 66 | `8857 tokens. Eight words. "Completed" means nobody asked for help.` |

**为什么推荐 ①**

- **两个 token 总数 + 两个字数**直接坐实「同一个任务、两次运行、两种产出」：8857→八个词、8605→六个词，这是全文最反直觉的一组实测数字，不用读正文就能感到失控感。
- 结尾把 `completed` 的真实语义一句戳破（nobody asked for help），与标题的「没人决定」互为印证，读者带着这个定义进正文。
- 不含 SDK 内部术语（handoff / node / swarm 之外无行话），Medium 列表页读者无需前置知识。
- 138 字符贴着 140 上限，移动端一般不截断；若担心截断，改用 ④（66 字符）。

② 把机制讲得最完整（路由 = 模型的 tool call、终止 = 沉默），适合想吸引「正在选型多智能体框架」的读者，但没有数字，冲击力弱一点。③ 剧透了两个失败结论，会削弱正文中「completion by silence」的发现感；只在你想吸引已经踩过 swarm 坑的工程师时用。④ 最安全、最不容易截断，但少了「第二跑只有六个词」的荒谬感。

**操作**：在 Medium 编辑器里，标题下方灰色的 "Write a subtitle..." 处粘贴所选文本（切勿粘成正文段落，否则不会样式化为副标题）。

---

## 第 3 步：Byline 首行

正文第一行（Import 一般不会自动加，需手写）：

```text
Originally published at https://xiongpin.dev/posts/orchestrating-swarm/ on 2026-11-11.
```

把 `https://xiongpin.dev/posts/orchestrating-swarm/` 选中做成超链接，指向自身。

---

## 第 4 步：封面图

上传：`pinxiong.github.io/static/images/orchestrating-swarm/cover-medium.png`（**1400×788，16:9**，源 SVG 同目录 `cover-medium.svg`，viewBox 直接就是 `0 0 1400 788`，无需再校尺寸，上传后目视整图未裁即可）。

> **2026-11-11 封面风格统一**：本篇与 UC05 的封面已从白底细线排版改回 UC01–UC04 的深蓝渐变基准（`#0b2547 → #14407c`，右侧机制图三件套）。Medium 还没 Import，用当前这个新文件即可。主站 / Dev.to 已同步新图；**BC 线上头图是上传到平台资产库的旧白底 `cove.webp`，不会自动更新**，需要在 BC 后台单独重传同一个 `cover-medium.png`。

---

## 第 5 步：标签（5 个，与前三篇同口径）

```text
AI · Agents · AWS · Strands · Software Engineering
```

Medium 最多 5 个，按上面顺序填，前两个权重最高。

---

## 第 6 步：正文核对清单（逐项过）

1. **正文图只有 1 张**：`swarm-handoff-loop.png`（handoff 循环机制图，位于开头 "Three agents share one task" 段落之后）。这张图是全文唯一配图，缺了就说明 Import 没抓全，回主站对应位置重新复制。别按 UC03/UC04 的习惯去找多张图，本篇确实只有一张。
2. **16 个代码块**：5 个 Python（SDK 源码逐字摘录，首行 `# strands/multiagent/swarm.py:NNN -- ...`）、9 个 text（运行 trace / 上下文块）、2 个 bash（Try it yourself）。全部要有等宽字体和灰底；被 Import 拍平成段落的，全选那段 → 工具栏 `</>` 重新设为 code block。特别检查 `node_history : researcher -> calculator -> writer` 那几行 trace，别被拆成多段。
3. **无 ASCII 状态机图**（UC05 有、本篇没有）。看起来像图的 `Context: / Handoff Message: / User Request:` 块是普通 text 代码块，保持等宽即可。
4. **引用行**：开头的 `> Verified on 2026-11-11 against strands-agents 1.63.0 ...` 应显示为引用样式（左侧竖线）。
5. 全文搜一遍 `](` 和 `![`，确认没有 Markdown 残留符号（Import 偶尔漏转）。
6. 结尾的系列预告（"The next piece in the series keeps the same task..."）和 article 05 链接必须保留，不要当成草稿尾巴删掉。

---

## 第 7 步：Advanced settings → Publish

点右上 `Publish` 前，先开 `Advanced settings`：

- [ ] **"This story was originally published elsewhere"** 勾上
- [ ] Canonical 链接填 **`https://xiongpin.dev/posts/orchestrating-swarm/`**（带结尾斜杠，与上表完全一致）
- [ ] 留空 canonical = 把 SEO 让给 Medium，停下先修

然后 Publish。发布后做两件事：

1. 打开线上文章，确认标题下方显示的是你选的 subtitle、封面是 16:9 那张、canonical 指回 xiongpin.dev；
2. 把 Medium URL 回填到本文件顶部表格、`orchestrating-swarm-slack.md` 的 `<MEDIUM_URL>` 占位，以及 `strands-in-action/PIPELINE_STATE.md` 的 Medium 台账行。
