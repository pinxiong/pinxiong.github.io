# Slack 分享文案 · UC04 · It Remembers Across Restarts — and Forgets Mid-Conversation（已发布）

> 母版：https://xiongpin.dev/posts/sessions-state-memory/
> 四渠道链接已全部回填（主站 / BC / Dev.to / Medium）。
> 系列：strands-in-action · 第 4 篇。

---

## A. 标准版（推荐，发 AWS Slack 群）

```text
Hi everyone,

I published a hands-on post on the Strands Agents SDK: *It Remembers Across Restarts — and Forgets Mid-Conversation*.

It separates three things people call memory, and measures each one. Two separate processes share nothing but a directory, and the second one answers with the name the first planted. Seven turns later, with the window at six, the same agent holds fourteen messages on disk and six in view, and it invents a privacy reason instead of admitting the codename is gone. A summarizer with no window size never fired at a 0.001 threshold; at 0.00005 it settled at nine messages with the fact intact. Every number came out of a run against strands-agents 1.63.0 on Bedrock, and the scripts are in the repo.

The part I got wrong first: agent.state is durable but silent. It is written to agent.json and restored on the next call, and nothing in the prompt path ever reads it, so a stored fact is invisible unless you inject it yourself with a BeforeInvocationEvent hook. The post has the twenty-line version and the run that shows it working at turn seven.

Blog: https://xiongpin.dev/posts/sessions-state-memory/
AWS Builder Center: https://builder.aws.com/content/3Ll4sEZ0YTvNRvbvH4UWe5hUdtz/it-remembers-across-restarts-and-forgets-mid-conversation
Dev.to: https://dev.to/aws-builders/it-remembers-across-restarts-and-forgets-mid-conversation-1ehh
Medium: https://medium.com/@pinxiong.cn/it-remembers-across-restarts-and-forgets-mid-conversation-1a27f5d6b782

Happy to hear your feedback.
```

## B. 短版（4 行）

```text
Hi all,

New post: *It Remembers Across Restarts — and Forgets Mid-Conversation*. A restart kept a planted name across two processes, while seven turns later the same run held 14 messages on disk and 6 in view. agent.state turned out to be stored but never injected into the prompt.

https://builder.aws.com/content/3Ll4sEZ0YTvNRvbvH4UWe5hUdtz/it-remembers-across-restarts-and-forgets-mid-conversation
```

---

## 使用提示

- A 版把主站与 Builder Center 放前两位，与 UC01–03 口径一致；只想发一个链接用 B 版。
- Slack 语法：`*加粗*`；长链接可换成 `<URL|Read on AWS Builder Center>` 形式。
- 四个链接均为平台原生 URL，无 utm，已回填。
- 数字出处（全部来自 `usecases/04-sessions-state-memory/evidence/`）：
  - 跨进程召回：`session-restart.txt`，第一个进程写入后退出，第二个进程用同一 session id 答出 "Your name is Pin and your favorite number is 42"
  - stored 14 / visible 6：`sliding-window.txt`，`TURN 7 ask | msgs= 6 stored=14`，第 4 轮首次分叉（6 条 = 3 轮）
  - 模型编造隐私理由：同上文件，codename 丢失后回复 "Sorry, I can't provide any response that might provide private information about any individual."
  - 0.001 阈值不触发：`summarizing-no-threshold.txt`，14 条消息零摘要
  - 0.00005 触发后稳态 9：`summarizing-window.txt`，`removed_message_count: 6`，14 − 6 + 1 = 9
  - 快照单文件 878 → 1774 字节：`snapshot-session.txt`
