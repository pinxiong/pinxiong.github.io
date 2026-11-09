# 反馈记录 · UC03 → 插队 UC05

> 这是本闭环的第一个真实案例：**读者反馈直接改写了系列计划**。
> 记录时点：2026-11-08（UC03 发布 D+2）。

## 1. 触发

读者 **Mayank Raj** 在 Builder Center 的 UC03《The Limits That Don't Limit》下连问三轮，问题逐层收紧：

1. 单次调用的限额管不住两个并发 attempt 各花一份剩余配额 —— 需要 shared atomic job-level store；
2. 请求已提交但响应丢失时，你怎么知道"没找到"等于"没发生过"；
3. 崩溃发生在副作用之前之后，容量归还是不是都安全。

这三问的共同点：**它们问的不是文章里某个词，而是文章结论的边界**。UC03 的论点是"限额只约束它计数的东西"，但没有回答"那计数之外靠什么"。

## 2. 做了什么

- 两个确定性探针：`outreach/uc03-comments/reservation_crash.py`、`reservation_delayed_commit.py`。
- 结果（naive 写法）：重复写 1 次 + 容量误归还；延迟提交场景 duplicate_writes=1。
- 回复稿经**两个独立 agent**（一个做实验、一个只读证据复核）两轮验证后 PASS，才发布。

## 3. 归因

- **不是"没讲清"，是"没讲完"**：读者已经接受 UC03 的结论，开始问下一层。
- 这类缺口无法靠加一节补救 —— 它需要 reservation 状态机、幂等键、目的地围栏、延迟提交，是一篇独立文章的体量。
- 而且 UC03 的读者已经在这条线上：他们不会去翻系列目录，只会在评论区继续问。

## 4. 出口：B 系列选题（插队）

| 动作 | 内容 |
|---|---|
| 新增 | **UC05《When "Not Found" Doesn't Mean "Never Happened"》** |
| 拆分 | 原 UC05「多智能体四选一」拆成 UC06 Swarm / UC07 Graph / UC08 Workflow / UC09 A2A，各一篇深挖 |
| 新增 | UC10 同进程混搭、UC11 跨进程混搭 |
| 顺延 | 原 UC06 Guardrails → UC12，原 UC07 Evals → UC13，原 UC08 Deploy → UC14 |
| 规模 | 8 篇 + A0 → **14 篇 + A0** |
| 代价 | 系列战线拉长约一倍；节奏改为每 2–3 天一篇来消化 |

**为什么值这个代价**：这不是读者的个人偏好，是 UC03 结论的必要延伸。不补，等于把文章停在"发现问题"；补了，读者拿到的是可执行的状态机。

## 5. 对写作规则的连带影响

- 以后写"边界类"文章（limits / guardrails / quotas），**结论必须写到"边界之外靠什么"**，否则读者一定会追问到那一层。这条等 UC05 发布后回看是否要写进 `tech-article-writing`。

## 6. 下篇开写时必须记住的一条

> **判断反馈是"澄清"还是"缺口"：澄清改正文，缺口改计划。**

## 7. 周复盘回看（2026-11-09，D+3）

### 数据窗口

历史快照从 2026-11-07 20:57 到 2026-11-09 20:19，不足两周，不做上一周对比。此窗口内：

- Dev.to：views 62 → 85（+23），reactions 22 → 22（+0），comments 6 → 15（+9）。
- Builder Center：likes 20 → 20（+0），comments 4 → 9（+5）。
- Dev.to 累计 85 views / 15 comments，评论数为每百次阅读 17.6 条；评论包含作者回复，只用于和首轮基线的同口径比较。

### 新读者反馈（保留原文）

Kent Bodrov（Dev.to，2026-11-09）：

> That unresolved queue needs an owner and a decision deadline, not just a TTL. For a launch review I would want someone accountable for the scope, a forced timeout with an external read-back, a recovery owner, and an explicit stop condition. How do you decide when an unresolved item needs human intervention rather than another reconciliation attempt?

Gonzalo Gjuka（Dev.to，2026-11-08）：

> Yes, and that part the API gets right. The limit comes back as HTTP 400: LimitExceeded for Oracle's limit on the tenancy, QuotaExceeded for an admin's quota on the compartment. Oracle's API error table marks both "Retry: No". Host capacity comes back as a 500 with the message "Out of host capacity.", and 500s sit in the retry-with-backoff class. A retry policy can split on status: never retry the 400s, loop on that 500. My loop also matches the message, not just the status, so any other 500 shows up in the log instead of passing for capacity.

### 出口核验

| 出口 | 本次结论 | 是否已执行 |
|---|---|---|
| B 系列选题 | UC05 已在 `strands-in-action/PLAN.md` v3 插入，下一篇仍是 UC05，不再次插队；Kent 的新问题归入本篇必须回答的「unresolved 队列如何退出」 | 已执行 |
| A 写作规则 | 「边界类文章必须写到边界之外靠什么」继续待回看；UC05 尚未发布，没有发布后证据，本周不提前写成硬规则 | 已执行（明确不改） |
| C 发布策略 | 本周没有新增可支持改窗口的证据，继续沿用 21:30–22:30（GMT+8） | 已执行（明确不改） |

UC05 完稿时必须补答：unresolved item 的 scope owner、decision deadline、forced timeout + external read-back、recovery owner，以及何时停止自动 reconciliation 并转人工。Gonzalo 的 OCI 例子只作为跨系统对照线索；未独立复现前不写成自己的实测结论。
