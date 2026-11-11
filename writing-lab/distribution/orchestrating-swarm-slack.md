# Slack 分享文案 · UC06 · Orchestrating Agents: Nobody Decides Who Goes Next

> 母版：主站 `content/posts/orchestrating-swarm.md`（canonical 只用于各平台 Import / canonical 设置，**不进 Slack 文案**）。
> BC / Dev.to 链接已于 2026-11-11 发布当档回填；Medium 为 `<MEDIUM_URL>` 占位，手动 Import 后回填。
> 按 Pin 2026-11-10 口径：**Slack 不放 Blog 主站链接**。
> 系列：strands-in-action · 第 6 篇。

---

## A. 标准版（推荐，发 AWS Slack 群）

```text
Hi everyone,

New post in the Strands Agents series: *Orchestrating Agents: Nobody Decides Who Goes Next*.

A Strands swarm has no scheduler, no route table and no orchestrator queue. Routing is a model's tool call, evaluated at every hop, and the swarm ends when the last node stops talking. That design has sharp edges, and I ran them all: the same task spent 8857 tokens to deliver eight words, then 8605 tokens to deliver six, and both runs reported "completed", because "completed" only means nobody asked for help. A handoff dies with the node that requested it, and the timeout report says zero tokens. A tool that always raises did not stop the swarm; the next node ran and saved its draft eleven times. max_handoffs and max_iterations turn out to read the same counter. Every number came out of a run against strands-agents 1.63.0, and the scripts are in the repo.

AWS Builder Center: https://builder.aws.com/content/3Lxn0RS1k0tiClcigN1xz5c0hH9
Dev.to: https://dev.to/aws-builders/orchestrating-agents-nobody-decides-who-goes-next-2cg4
Medium: <MEDIUM_URL>

Happy to hear your feedback.
```

## B. 短版（4 行）

```text
Hi all,

New post: *Orchestrating Agents: Nobody Decides Who Goes Next*. 8857 tokens bought eight words; 8605 bought six; both runs said "completed". In a swarm, completion only means nobody asked for help. Routing is a model's tool call, not a plan.

https://builder.aws.com/content/3Lxn0RS1k0tiClcigN1xz5c0hH9
```

## C. 全渠道短版（一句话 + 三条链接）

```text
New post: *Orchestrating Agents: Nobody Decides Who Goes Next*. 8857 tokens bought eight words; 8605 bought six; both runs said "completed". In a Strands swarm, routing is a model's tool call and completion means nobody asked for help.

AWS Builder Center: https://builder.aws.com/content/3Lxn0RS1k0tiClcigN1xz5c0hH9
Dev.to: https://dev.to/aws-builders/orchestrating-agents-nobody-decides-who-goes-next-2cg4
Medium: <MEDIUM_URL>
```

---

## 使用提示

- A 版以 Builder Center 开头，链接块只放 **BC / Dev.to / Medium 三条**；主站 Blog 按 Pin 口径不进 Slack，canonical 仍指回主站，读者从平台文内链接回流即可。只想发一个链接用 B 版；想一次贴全三条链接但不要长段落，用 C 版。要主推 Medium，把 B 版的 BC 链接换成 Medium 链接即可。
- Slack 语法：`*加粗*`；长链接可换成 `<URL|Read on AWS Builder Center>` 形式。
- 这是第 6 篇，不是终篇；下一篇是 graph orchestration（自画节点与边），可带一句 "next up is the graph"。
- BC / Dev.to 链接已于 2026-11-11 发布当档回填（A/B/C 三版均生效）；Medium Import 后回填 `<MEDIUM_URL>`。分享时若 Medium 带 `?postPublishedType=initial` 查询串，去掉再发。
- 数字出处（全部来自 `strands-in-action/usecases/06-swarm/evidence/`）：
  - 8857 tokens / 八词 deliverable、8605 tokens / 六词 deliverable —— `swarm-trace.txt`（happy 两次运行；`node_history: researcher -> calculator -> writer`）
  - 沉默即完成（718 tokens、writer never ran）—— 同上，silent 模式
  - handoff 随节点死亡、失败报 0 tokens（4.012s 超时）—— `swarm-failure.txt`，timeout 模式
  - `max_handoffs` / `max_iterations` 同一计数器（3 轮同停点、不同 reason 字符串）—— `swarm-limits.txt`
  - 坏工具不停止 swarm（`node_history: calculator -> writer`、`save_draft` 调 11 次、22371 tokens）—— `swarm-failure.txt`，toolerror 模式
- 人工取消节点（BeforeNodeCallEvent）与 session 拒绝构造在正文 "Where a human can stand" 一节，数据同在 `swarm-failure.txt`。
- 别把 "swarm 节点无并行" 说成 SDK 缺陷：单进程 await 一个节点流是设计使然，正文 "What surprised me" 一节有原话。
