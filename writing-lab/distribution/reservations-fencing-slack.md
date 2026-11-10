# Slack 分享文案 · UC05 · When "Not Found" Doesn't Mean "Never Happened"（四渠道全部上线）

> 母版：https://xiongpin.dev/posts/reservations-fencing/
> 四渠道链接已全部回填（主站 / BC / Dev.to / Medium，Medium 于 2026-11-10 回填）。
> 系列：strands-in-action · 第 5 篇。

---

## A. 标准版（推荐，发 AWS Slack 群）

```text
Hi everyone,

I published a hands-on post on the Strands Agents SDK: *When "Not Found" Doesn't Mean "Never Happened"*.

A lease expiry proves only that a worker stopped reporting. In five real-clock runs, a naive reconciler wrote the same ticket twice every time, and handed the capacity back while the effect already existed. The delayed-commit race is the part that surprised me: the janitor released capacity at 1.003s, the retry committed at 1.407s, and the old attempt, still alive, committed at 2.405s. A put-if-absent fence stopped every duplicate write but still released capacity early and burned a wasted retry. Keeping the reservation in outcome_unknown until the destination reported a terminal state gave zero duplicates, zero early releases and zero retries. Every number came out of a run against strands-agents 1.63.0, and the scripts are in the repo.

Blog: https://xiongpin.dev/posts/reservations-fencing/
AWS Builder Center: https://builder.aws.com/content/3Ls8Su63RbuSKR3yys1j9t6US1p/when-not-found-doesnt-mean-never-happened
Dev.to: https://dev.to/aws-builders/when-not-found-doesnt-mean-never-happened-2eie
Medium: https://medium.com/@pinxiong.cn/when-not-found-doesnt-mean-never-happened-1bc3e54bd912

Happy to hear your feedback.
```

## B. 短版（4 行）

```text
Hi all,

New post: *When "Not Found" Doesn't Mean "Never Happened"*. Five real-clock runs, five duplicate writes. A lease expiry tells you a worker stopped reporting, not that nothing happened; the fix is to hold the reservation in outcome_unknown until the destination answers.

https://builder.aws.com/content/3Ls8Su63RbuSKR3yys1j9t6US1p/when-not-found-doesnt-mean-never-happened
```

## C. 全渠道短版（一句话 + 四条链接）

```text
New post: *When "Not Found" Doesn't Mean "Never Happened"*. Five real-clock runs, five duplicate writes. A lease expiry tells you a worker stopped reporting, not that nothing happened; hold the reservation in outcome_unknown until the destination reports a terminal state.

Blog: https://xiongpin.dev/posts/reservations-fencing/
AWS Builder Center: https://builder.aws.com/content/3Ls8Su63RbuSKR3yys1j9t6US1p/when-not-found-doesnt-mean-never-happened
Dev.to: https://dev.to/aws-builders/when-not-found-doesnt-mean-never-happened-2eie
Medium: https://medium.com/@pinxiong.cn/when-not-found-doesnt-mean-never-happened-1bc3e54bd912
```

---

## 使用提示

- A 版把主站与 Builder Center 放前两位，四渠道顺序与 UC04 一致；只想发一个链接用 B 版；想一次贴全四条链接但不要长段落，用 C 版。要主推 Medium，把 B 版的 BC 链接换成 Medium 链接即可。
- Slack 语法：`*加粗*`；长链接可换成 `<URL|Read on AWS Builder Center>` 形式。
- 这是第 5 篇，不是终篇，不要写 "the last post"；结尾预告的是多智能体编排，可以带一句 "next up is orchestration"。
- 四个链接均为平台原生 URL，无 utm，已全部回填；分享时若 Medium 带 `?postPublishedType=initial` 查询串，去掉再发。
- 链接可达性：主站 / Dev.to / BC 于 2026-11-10 复核为 HTTP 200；`medium.com` 在本机网络不可达，Medium URL 由 Pin 提供，未做页面抓取核验。
- 数字出处（全部来自 `strands-in-action/usecases/05-reservations-fencing/evidence/`）：
  - 5/5 重复写、容量误归还 —— `lease-crash-boundary.txt`，`SUMMARY trials=5 duplicate_writes_total=5 capacity_returned_while_effect_exists=5/5`
  - 1.003s / 1.407s / 2.405s 时间线 —— `delayed-commit-race.txt`，naive 模式 `SUMMARY trials=5 duplicate_writes_total=5 early_capacity_release=5/5`
  - fence 模式 0 重复但 5/5 提前释放 —— 同上，fenced 模式 `duplicate_writes_total=0 early_capacity_release=5/5`
  - authoritative 0 / 0 / 0 —— 同上，`duplicate_writes_total=0 early_capacity_release=0/5 retry_started=0/5`
  - 12 workers / 2 slots / 1.0s lease / 继承者等 1.002s —— `slot-contention.txt`
  - SDK 侧：单实例串行 `ConcurrencyException`、同 `idempotency_token` 进程内去重、双实例各拿 453-token 预算 —— `concurrent-limits.txt`
- 别把 `outcome_unknown` 写成 SDK 提供的状态：它是本篇实验里自己加进 reservation 状态机的，正文 "Two states, not one" 一节有说明。
