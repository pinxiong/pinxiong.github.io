# Medium 发布手册 · UC07 · Orchestrating Agents: The Graph Is Yours, the Judgment Isn't

> 系列：strands-in-action 第 7 篇 ｜ 状态：**主站 / Dev.to / Builder Center 已于 2026-11-13 22:04（GMT+8）发布；Medium 待手动 Import**
> 日期：2026-11-13（开写当档预置，22:17 回填全部线上链接；标题、副标题、封面、正文核对项均按本篇实测填写）

**线上地址**

| 渠道 | 链接 |
|---|---|
| 主站（canonical） | https://xiongpin.dev/posts/orchestrating-graph/ |
| AWS Builder Center | https://builder.aws.com/content/3M3UfdK6svKCg1nD2c3m1x9OnqZ/orchestrating-agents-the-graph-is-yours-the-judgment-isnt |
| Dev.to | https://dev.to/aws-builders/orchestrating-agents-the-graph-is-yours-the-judgment-isnt-16dk |
| Medium | <MEDIUM_URL>（手动 Import 后回填） |

Medium 只能手动操作，约 5 分钟。按下面 7 步走。

---

## 第 1 步：Import（从 canonical 导入）

打开 <https://medium.com/p/import> → 粘贴上方表格里的主站 canonical URL `https://xiongpin.dev/posts/orchestrating-graph/` → Import。

导入结果一定是一篇 draft，不会自动发布。Import 会带过来标题、正文和 12 个代码块（8 个 Python 源码块 + 2 个 text + 2 个 bash），**但 subtitle 永远是空的，必须手填**。

---

## 第 2 步：Title 与 Subtitle（本手册重点）

**Title（导入后应已是这个，核对即可）**

```text
Orchestrating Agents: The Graph Is Yours, the Judgment Isn't
```

**Subtitle：手填，从下面 4 个里选一个（字符数已逐条数过，全部 ≤ 140 上限）**

| 选项 | 字符数 | 副标题 |
|---|---|---|
| **① 推荐** | **137** | `Routing is a Python predicate, not a model call. A join ran twice. The documented pruning never happened. Every number came out of a run.` |
| ② 讲机制 | 126 | `The edges are yours, but the predicate reads text a model wrote. A join fires on the first parent. Verified on strands 1.63.0.` |
| ③ 讲失败 | 128 | `A tool that raises did not fail the node. A hook cancellation aborted the whole graph. Neither run matched the source docstring.` |
| ④ 最紧凑 | 79 | `A predicate, not a judge. A join that ran twice. A cycle with no default limit.` |

---

## 第 3 步：Byline 首行

```text
By Pin Xiong · Strands in Action, post 7 · Verified on strands-agents 1.63.0
```

## 第 4 步：封面图

用 `pinxiong.github.io/static/images/orchestrating-graph/cover-medium.png`，尺寸 **1400×788（16:9）**，深蓝系列基准由 `strands-in-action/tools/build_covers.py --slug orchestrating-graph` 生成，不要手搓配色。同目录 `cover-medium.svg` 为源文件。

- 未 Import 的文章：直接在编辑器插入这张新图即可。
- 已发布故事需要换图时：进编辑页替换**正文第一张图** → Save and publish。Medium 没有 API，这一步只能人工，核验脚本对 Medium 只报 `MANUAL`，不要默认当成 PASS。

## 第 5 步：标签（5 个，与前三篇同口径）

```text
AWS, Amazon Bedrock, Multi-Agent Systems, Python, AI Agents
```

## 第 6 步：正文核对清单（逐项过）

1. **正文无配图**（本篇只有封面，正文里没有机制图，不要额外插图）。
2. **12 个代码块**：8 个 Python（SDK 源码逐字摘录：`209-224 / 1021-1038 / 1285-1325 / 161-180 / 491-504 / 999-1010 / 1066-1072 / 1225-1226`）、2 个 text（ASCII 图 / writer 输入）、2 个 bash（Try it yourself）。全部要有等宽字体和灰底；源码块首行是 `# strands/multiagent/graph.py:NNN -- verbatim, strands-agents 1.63.0`。
3. **源码块第一行代码必须 0 缩进**，只保留相对层级。Import 有时会整体右移，逐块检查。
4. **ASCII 图块**（`A (fast, batch 1) ---> B (slow, batch 2)` 那一段）保持等宽，别被拆成多段。
5. **引用行**：开头的 `> Verified on 2026-11-13 against strands-agents 1.63.0 ...` 应显示为引用样式（左侧竖线）。
6. 全文搜一遍 `](` 和 `![`，确认没有 Markdown 残留符号。
7. `Try it yourself` 首屏的 `git clone https://github.com/pinxiong/strands-in-action.git` + `cd strands-in-action/usecases/07-graph` 必须完整保留，别当成草稿尾巴删掉。

## 第 7 步：Advanced settings → Publish

1. Advanced settings 里把 **canonical / original source** 勾上并指回 `https://xiongpin.dev/posts/orchestrating-graph/`，不要让 Medium 自己当 canonical。
2. 打开线上文章，确认标题下方显示的是你选的 subtitle、封面是 16:9 深蓝那张、canonical 指回 xiongpin.dev。
3. 把 Medium URL 回填三处：本文件顶部表格、`orchestrating-graph-slack.md` 的 A 版与 C 版 `<MEDIUM_URL>` 占位、`strands-in-action/PIPELINE_STATE.md` 的 UC07 D+0 台账 Medium 行。

---

**数字出处**（Slack 文案与正文共用，均指向 `usecases/07-graph/evidence/`）

| 数字 | 证据文件 |
|---|---|
| 3 次谓词求值、模型调用快照 `{2,2,0,0}`、5145 tokens | `graph-trace-condition.txt/.json` |
| `A, join, B, join`、join 跑 2 次、1365 tokens | `graph-fanin-or.txt/.json` |
| 5109 tokens、9863 ms、writer 输入拼串 | `graph-trace-linear.txt/.json` |
| `overlap_pairs=[('right','left')]`、2046 tokens / 5493 ms | `graph-parallel-overlap.txt/.json` |
| unbounded warning、6 次执行 FAILED、644 tokens | `graph-limits-unbounded.txt/.json`、`graph-limits-capped.txt/.json` |
| raise 四节点全跑、cancel 整图 abort | `graph-failure-raise.txt/.json`、`graph-failure-cancel.txt/.json` |
