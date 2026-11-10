# 写作规则变更台账

> 每条规则改动都要能追到一次真实反馈或一次实测数据。查不到来源的规则，下次复盘可以删。
> 改动后 2–3 篇回看「预期效果」，不成立就撤回并在本表加一行撤回记录。

| 日期 | 类型 | 改了什么 | 依据（读者原话 / 数据 / 文件） | 预期效果 | 回看结果 |
|---|---|---|---|---|---|
| 2026-11-07 | 写作规则 | UC04 增写「State does not inject itself」一节：state 不自动进 prompt，必须经 `BeforeInvocationEvent` 注入 | Reid Marlow（Dev.to / BC）："treating conversation history as strictly ephemeral context, while pulling invariants out into agent.state" —— 读者把这点当成默认行为，说明正文漏了机制层 | 后续记忆类文章的读者不再问同一点 | 待回看（UC05 发布后） |
| 2026-11-07 | 写作规则 | 评论回复一律「一个 agent 做实验 + 另一个独立 agent 只读证据复核」，全 PASS 才算准确 | Pin（2026-11-07）："做实验是一个 agent 然后去验证的又是另外一个 agent…如果没有验证，只是做了个实验，然后贴了一个报告，这种我觉得不叫准确无误" | 回复里不再出现「我跑了所以是这样」的越界结论 | 已生效，固化在 `comment-reply-verification` skill |
| 2026-11-08 | 写作规则 | 破折号（em dash）相关规则全部关闭，工具层 `IGNORE_DASH_RULES = True` | Pin（2026-10-01 政策）：本机输入法打不出该字符，属输入通道问题 | 评审不再重复报假阳性 | 已生效 |
| 2026-11-08 | 系列选题 | 插入 UC05《When "Not Found" Doesn't Mean "Never Happened"》；原 UC05 多智能体四选一拆成 UC06–UC09，新增 UC10/UC11 混搭；原 06–08 顺延为 UC12–UC14，系列 8 篇 → 14 篇 | Mayank Raj（BC，UC03 三连问）：预留配额的并发争用、延迟提交、崩溃边界；探针 `outreach/uc03-comments/reservation_crash.py` 与 `reservation_delayed_commit.py` 已验证 | 补齐 UC03 结论的边界，读者不必再自行推导 | 待回看（UC05 发布后） |
| 2026-11-08 | 发布策略 | 发布窗口 20:00–23:00 收窄为 **21:30–22:30（GMT+8）**，周二/三/四优先，周六日不发 | `engagement/data/comments/` 22 条读者评论按 UTC 小时分布，UTC 13–16 为单一峰值；历史 21:35/22:03 发布的篇目即时阅读 88/60，16:58/19:43 仅 15/4 | 下一篇首日 Dev.to 阅读高于近三篇中位数 | 待回看（UC05 发布后 48h） |
| 2026-11-08 | 发布策略 | 开写时间 09:00 → 10:30，并改为 10:30 / 14:30 / 21:30 三个触发点、幂等补跑 | Pin（2026-11-08）：早上 9 点电脑可能没开机、网络不通，定时器根本不会触发 | 不再出现「当天没开写」的空转日 | 待回看（连续 5 个工作日） |
| 2026-11-10 | 写作规则（**试行**） | §4 新增结构自检四件套：命名状态 / 判别实验 / 显式边界 / 复跑命令；明确「零追问不等于写透」 | 跨篇评论结构：UC03、UC04 的追问全部落在未命名、未实验的边界（Mayank、Reid、Alex、Kent）；UC05 用四件套后，唯一具体评论点名复述 `outcome_unknown` 与 idempotency（`feedback/2026-11-10-uc05-feedback.md`） | 后续篇目的「边界型追问」减少，读者能复述具体机制名而非泛泛称赞 | 待回看（UC06/UC07，2–3 篇后决定是否升级为硬规则或撤回） |
| 2026-11-10 | 写作规则（方法论） | §11 新增约束 4：评论分四类（致谢/复述/追问/纠错）、分渠道统计，致谢只计入互动数不进归因 | UC05 的 4 条 BC 评论中 3 条为纯致谢、1 条复述、0 追问；UC04 的 7 条中 4 条为致谢/推广；Dev.to 同期以技术追问为主 | 反馈记录不再把点赞与致谢写成「内容被读者接住」 | 待回看（下一次 D+2 记录） |
| 2026-11-10 | 写作规则（方法论） | §11 新增约束 5：零追问时把正文自己写下的 `does not cover` 登记进 topic-backlog，反馈输入 = 读者追问 + 作者自认边界 | UC05 正文两处自认边界（"Cancelling the id on death ... this experiment does not cover it"、"I verified each half separately, not the combination"）无任何读者接住；若只等评论，下一篇没有原料 | 每篇发布后 topic-backlog 至少新增 1 条来自正文的候选，闭环不因致谢型评论区空转 | 待回看（UC06 开写时检查是否真的读了该条目） |
