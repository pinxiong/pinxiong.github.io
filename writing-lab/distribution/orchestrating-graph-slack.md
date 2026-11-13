# Slack 分享文案 · UC07 · Orchestrating Agents: The Graph Is Yours, the Judgment Isn't

> 母版：`usecases/07-graph/article.md`（canonical 只用于各平台 Import / canonical 设置，**不进 Slack 文案**）。
> 状态：**在制品，尚未发布**。BC / Dev.to 链接发布后回填；Medium 为 `<MEDIUM_URL>` 占位，手动 Import 后回填。
> 按 Pin 2026-11-10 口径：**Slack 不放 Blog 主站链接**。
> 系列：strands-in-action · 第 7 篇。

---

## A. 标准版（推荐，发 AWS Slack 群）

```text
Hi everyone,

New post in the Strands Agents series: *Orchestrating Agents: The Graph Is Yours, the Judgment Isn't*.

A Strands graph takes the routing decision away from the model: an edge fires when a Python predicate returns True. I ran the same task as the previous swarm post on a graph, and the sharp edges showed up in the traces. The predicate was evaluated three times per fork while the model-call counters never moved, because it only reads text the model already wrote. A join with two parents ran twice, started before the slower parent finished, and saw only the first parent's output. With no cap set, a cycle warns that it is unbounded; with a cap of six it stops as FAILED after exactly six node executions. Two same-batch nodes really overlapped in wall-clock time, which the swarm never did. And the pruning described in the source did not match either failure I injected: a raising tool left the node COMPLETED, while a hook cancellation aborted the whole graph. Every number came out of a run against strands-agents 1.63.0, and the scripts and raw evidence are in the repo.

AWS Builder Center: https://builder.aws.com/content/<BC_ID>/orchestrating-agents-the-graph-is-yours-the-judgment-isnt
Dev.to: https://dev.to/aws-builders/orchestrating-agents-the-graph-is-yours-the-judgment-isnt-16dk
Medium: <MEDIUM_URL>

Happy to hear your feedback.
```

## B. 短版（4 行）

```text
Hi all,

New post: *Orchestrating Agents: The Graph Is Yours, the Judgment Isn't*. Routing is a Python predicate, not a model call, but a join ran twice and the documented pruning did not happen. The edges are yours; the words your predicate reads are not.

https://builder.aws.com/content/<BC_ID>/orchestrating-agents-the-graph-is-yours-the-judgment-isnt
```

## C. 全渠道短版（一句话 + 三条链接）

```text
New post: *Orchestrating Agents: The Graph Is Yours, the Judgment Isn't*. A predicate, not a judge. A join that ran twice. A cycle with no default limit.

AWS Builder Center: https://builder.aws.com/content/<BC_ID>/orchestrating-agents-the-graph-is-yours-the-judgment-isnt
Dev.to: https://dev.to/aws-builders/orchestrating-agents-the-graph-is-yours-the-judgment-isnt-16dk
Medium: <MEDIUM_URL>
```

---

## 使用提示

- A 版以 Builder Center 开头，链接块只放 **BC / Dev.to / Medium 三条**；主站 Blog 按 Pin 口径不进 Slack，canonical 仍指回主站，读者从平台文内链接回流即可。只想发一个链接用 B 版；想一次贴全三条链接但不要长段落，用 C 版。
- 发布后把 `https://builder.aws.com/content/<BC_ID>/orchestrating-agents-the-graph-is-yours-the-judgment-isnt` / `https://dev.to/aws-builders/orchestrating-agents-the-graph-is-yours-the-judgment-isnt-16dk` 换成真实链接，手动 Import 完成后把 `<MEDIUM_URL>` 换成 Medium 真实 URL；同时回填 Medium 手册顶部表格、`PIPELINE_STATE.md` 台账、`usecases/07-graph/publish/README.md`。

## 数字出处（逐条指向 `usecases/07-graph/evidence/`）

| 文案里的数字 | 证据文件 |
|---|---|
| 谓词求值 3 次、模型调用快照不变 | `graph-trace-condition.txt/.json` |
| join 跑 2 次、先于慢父完成、只见首个父节点 | `graph-fanin-or.txt/.json` |
| 上限 6 → 6 次执行后 FAILED；不设限 warning | `graph-limits-capped.txt/.json`、`graph-limits-unbounded.txt/.json` |
| 同批节点 wall-clock 重叠 | `graph-parallel-overlap.txt/.json` |
| raise 节点 COMPLETED / cancel 整图 abort | `graph-failure-raise.txt/.json`、`graph-failure-cancel.txt/.json` |
