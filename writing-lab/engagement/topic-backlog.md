# 选题库（读者反馈驱动）

用途：下一篇文章从这里选，不从脑子里选。每条都要能指回一条真实读者反馈。
规则：同一主题被多人提到就追加 +1；写成文章后把条目移到文末「已成文」。
每周一复盘从这里选一条给出明确推荐。

## 待写

- [2026-11-10] **cancel-on-death 与 per-attempt id：崩溃的 attempt 与慢的 attempt 能否区分** —— UC05 正文自认边界："Cancelling the id on death is a separate mechanism, and this experiment does not cover it." 正文已指出「所有 worker 共用一个永久 identity 时，crashed 与 slow 不可区分」，但没有实验。适合做「一次 identity 设计错了会怎样」的对照实验。
- [2026-11-10] **落盘 session 的安全边界：明文 JSON 该怎么放** —— UC04 Builder Center dextheking（11-09 17:51）："The session files sit on disk as plain JSON and anyone with disk access can read the full transcript. Where do you put that directory in a deployed agent, and do you encrypt it or wipe it, or is local disk the wrong place once real user data flows through it?" 这是 UC04 评论里唯一指向部署安全而非记忆机制的缺口，尚未回复。此前因「BC 评论正文抓不到」被漏掉，本次补采原文后登记。

- [2026-11-09] **unresolved 队列的治理五项：scope owner / decision deadline / forced timeout + external read-back / recovery owner / 何时停止自动 reconciliation 转人工** —— UC03《The Limits That Don't Limit》Kent Bodrov 18:30 追问。UC05 正文 17:00 已定稿，未覆盖这五项；周复盘（20:20）曾建议补节后再发，用户拍板按原计划 11-09 21:30 发布，本轮不补进正文。转为发布后的反馈出口：在评论回复里正面回答，并作为下一篇候选素材。

- [2026-11-07] **manifest 注入的 token 与 TTFT 成本实测** —— UC04《It Remembers Across Restarts》Reid Marlow。他主张每轮注入固定 manifest；我回复里承认「这部分没测过，不能算免费」。这是一个公开承认过的实证缺口，补上就是一篇完整的实测文：注入 vs 加大窗口 vs 摘要器，三者的 token 与延迟对照。
- [2026-11-07] **多 worker 并发下的配额预留与副作用对账** —— UC03《The Limits That Don't Limit》Kent Bodrov。单次调用的限额管不住两个并发 attempt 各花一份剩余配额；他问的是 shared atomic job-level store + 释放前对账。这是 UC03 的直接续集，且需要真实并发实验。
- [2026-11-07] **重试与超时下的幂等键：重复工单断言** —— red-team 篇 Reid Marlow。`len(found) > 0` 放行重复写入，改成 `len(found) == 1` 并校验幂等键才能抓到。主题可扩成「副作用断言」专篇。
- [2026-11-07] **prohibited-phrase 检查的否定句误判** —— red-team 篇 xcl。`must_not_say` 用正则会把「不提供全额退款」误判为违规，又放过没用到原词的承诺。如何区分「解释政策边界」与「做出承诺」。
- [2026-11-07] **spec 漂移：tribal knowledge 变成 artifact 之后** —— AI Coding 篇 ai_adam（越南语，尚未回复）。代码继续前进而 spec 没跟上时会发生什么，怎么发现。
- [2026-11-08] **配额、实际容量与服务端等待：客户端限制管不到的一层** —— UC03《The Limits That Don't Limit》Gonzalo Gjuka。OCI 配额可用但主机容量不足、客户端重试设置无法缩短首次服务端等待的实例，把文章的「限额只约束它计数的东西」扩展到了云资源供给，适合做一次跨系统对照实测。

## 已成文 / 已闭环

- [2026-11-10] **两半合起来跑：fence + authoritative 状态机同时启用** —— UC05 正文自认边界："I verified each half separately, not the combination."；BC 读者 Benjamin Kincses 11-10 追问组合下「fence 拒绝 late commit 而 witness 仍 hold outcome_unknown」会不会等一个永不到来的终态。已产出 `outreach/uc05-comments/probe_fence_witness.py`（10 ms 轮询 janitor + 3.2 s 上限，6 组 × 5 次真实时钟）与 `evidence/fence-witness-combined.txt`：无竞争写者时 fence 拒绝 0 次、等价于 witness 单跑；注入绕过 reservation 的写者后，article 的 has_effect 优先顺序不读 A 终态故不卡（但早释放 5/5），终态集合含 fenced 则 2.41 s 正常结算，仅含 committed 则 capacity_released=0/5、queued_job_started=0/5、timed_out=5/5，即 capacity 泄漏而非 retry 卡死。回复稿 `reply-benjamin-combined-bc.md` 经两个独立 agent 复审全项 PASS。来源：`feedback/2026-11-10-uc05-feedback.md` 出口 B + BC 评论 `3LuVoa3aEnI6ODVdrEJvGgaa56h`。若扩成文章素材已齐。

- [2026-11-08] 预留配额的崩溃边界：outcome_unknown 与 unused 分离、按外部幂等键对账后才归还容量 —— UC03 Mayank Raj。已产出 `outreach/uc03-comments/reservation_crash.py` 与三种情形证据（naive 重复写 + 容量误归还；reconcile 不重复；崩溃于副作用前不泄漏配额），回复经独立 agent 两轮验证 PASS。若扩成文章素材已齐。

- [2026-11-07] Agent 记忆的契约测试（多深度植入 + 检索与行为双断言）—— UC04 Alex Shev。已产出 `outreach/uc04-comments/contract_test.py` 与 7 组单进程 + 3 组跨进程证据，并在 Dev.to/Medium 回复中公布。若扩成独立文章，素材已齐。
- [2026-11-07] state 需自行注入 prompt（BeforeInvocationEvent + manifest）—— UC04 Reid Marlow。已写入 UC04 正文「State does not inject itself」一节并同步四渠道。
- [2026-11-07] reasoning 模型沉默被误判为死任务、取消后的副作用与重试预算 —— UC03 Pierre-Laurent Medori。已补进 UC03 正文（协作式取消、quota 进程级作用域、limits 重置脚注）。
