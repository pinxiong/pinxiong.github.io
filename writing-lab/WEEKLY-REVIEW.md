# 每周写作改进复盘（执行手册）

> 定时任务只是触发器：**周一 20:00 主跑，周二 20:00 补跑**。真正的流程写在这个文件里。
> 改流程改这里，不要去改两个定时任务的提示词（否则两份会改歪）。

## 0. 为什么在晚上 20:00，不在早上

定时器只在**电脑开机且 WorkBuddy 在运行**时触发，关机或深度休眠期间不会补跑。
早上 09:00 这个点机器多半还没开，任务会直接消失；晚上 20:00 是 Pin 日常在电脑前的时间，
也是日报能稳定送达的时段。周二 20:00 是补跑位，所以周一没跑成也不会丢一周。

## 1. 幂等：先判断本周是否已经做过

看 `writing-lab/engagement/reports/` 里有没有本周（ISO 周）的 `*-weekly.html`，
或 `analysis-*.md` 的日期落在本周一之后。

- 已经出过 → 只回一行「本周复盘已于 <日期> 完成」，结束。**不重复发邮件。**
- 没出过 → 无论今天是周一还是周二补跑，都按下面完整执行。

## 2. 输入

| 内容 | 位置 |
|---|---|
| 采集脚本 | `writing-lab/engagement/scan.py` |
| 历史快照 | `writing-lab/engagement/data/history.jsonl`（ts / channel / slug / views / reactions / comments） |
| 最新快照 | `data/latest.json`、`data/comments/`（`pinxiongcn` 的跟帖算已回复） |
| 评论原文 | Dev.to `data/comments/<article-id>.json`；**Builder Center `data/comments/bc-<uc>-<id>.json`**（`scan.py` 已采公开接口，不再是 JS-only） |
| 选题库 | `writing-lab/engagement/topic-backlog.md` |
| 单篇反馈记录 | `writing-lab/feedback/*.md` |
| 规则变更台账 | `writing-lab/feedback/ledger.md` |
| 要改的写作规则 | `~/.workbuddy/skills/tech-article-writing/SKILL.md` 与 `references/` |

口径：只看 Dev.to 与 AWS Builder Center，不涉 Medium；只统计 2026-09-01 之后发布的文章；devto 与 bc 分列不相加。

## 3. 步骤

1. `python3 writing-lab/engagement/scan.py` 采集；Dev.to 不可达则用已有数据并注明截止时间。
2. 聚合 `history.jsonl`：每篇近 7 天与上一周的 views / reactions / comments 增量与累计；不足两周只列近 7 天并标注。
3. 生成图表：`.venv/bin/python report.py --weekly --date <今天>`；push `static/images/engagement` 与 `writing-lab/engagement`（`git add -f`），curl 确认图片 200 后再继续。
   **push 前先 `git pull --rebase`**：周一 21:30 还有流水线发布、日报两个任务会推同一个仓库，并发推送必然有一个被拒；被拒就 rebase 后重试一次，不要 force push。
4. 复核既有判断是否仍成立（首轮基线三条：边界/失败类评论率高、反直觉标题 reaction 率高、BC 推荐位是最大杠杆）。成立的保留，不成立的推翻并写依据。
5. **先处理反馈闭环，再改规则**：读本周 `feedback/` 记录里「出口」未执行的条目并执行；回看 `ledger.md` 标「待回看」的条目——预期效果成立改「已生效」，不成立就撤回并在台账追加撤回行。**这一步不能跳，否则规则只增不减。**
6. 列出仍未回复的评论（文章 + 评论者 + 链接），不起草回复。按 `tech-article-writing` §11 把评论分四类（致谢 / 复述 / 追问 / 纠错）并分渠道统计；**致谢只计入互动数，不进归因**。
7. 交付 A「写作规则修订」：每条写「规则 → 改成什么 → 依据哪条数据或评论」，并实际改文件；每处改动在 `ledger.md` 追加四要素（日期 / 类型 / 改了什么 / 依据 / 预期效果 / 回看结果=待回看）。约束：只改有本周证据的；不因单周波动推翻长期硬规则（句法、发布前清单、Dev.to 一段一行）；拿不准的列「待观察」。若某篇评论区全是致谢（零追问），按 §11 约束 5 读正文自己写下的 `does not cover`，确认已登记进 `topic-backlog.md`。
8. 交付 B「下一篇写作建议」：从 `topic-backlog.md` 与本周 feedback 选一条（注明来自哪条读者反馈、几人提过），给标题形式、开篇结构、要延续或改掉的一个写法、节奏结论。只给一个明确推荐。需要插队改 PLAN 时，写明插在哪、原编号如何顺延，PLAN 版本 +1。
9. 产出 `analysis-YYYY-MM-DD.md`（趋势表、规则修订清单与台账链接、下一篇建议）与 `reports/YYYY-MM-DD-weekly.html`（第一屏就是「本周改了哪些规则」和「下一篇写什么」，随后趋势图，最后未回复评论）。全部中文。
10. 发信（Agent Mail CLI，已授权固定动作，用 `--confirmed`，不再请求确认）：
    `agently-cli message +send --to pinxiongcn@foxmail.com --subject "每周写作改进复盘 · YYYY-MM-DD｜下一篇：<一句话主题>" --body-file reports/YYYY-MM-DD-weekly.html --confirmed`
    并把当天 PNG 逐张加 `--attachment`（相对 `engagement/` 的 `../../static/images/engagement/<日期>/<文件>.png`）。
    退出码 0 且输出含 `"ok": true` 才算成功；否则在摘要里注明失败原因，复盘照常交付。
11. 对话里给不超过 15 行中文摘要：第一行「下一篇写什么」，随后本周改了哪些规则文件与台账行，附趋势图链接。
12. 小样本（views < 50 或发布不足 48 小时）不下结论。除改规则文件、写 feedback 与台账、推图、发这一封邮件外，不做其他线上动作。

## 变更记录

| 日期 | 变更 |
|---|---|
| 2026-11-08 | 建立本文件；复盘时间 周一 09:00 → **周一 20:00**（避开开机前时段），新增周二 20:00 补跑位与 ISO 周幂等判断；把「先执行 feedback 出口、再改规则」列为不可跳过步骤 |
| 2026-11-10 | 输入表加入 BC 评论原文（`bc-<uc>-<id>.json`）；步骤 6 按 §11 分四类判读、致谢不进归因；步骤 7 要求零追问时核对正文 `does not cover` 已进 topic-backlog。依据 UC05 反馈记录 |
