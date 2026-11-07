# New comments discovered at 2026-11-07T20:57:37+08:00

### Dev.to · It Remembers Across Restarts — and Forgets Mid-Conversation
- url: https://dev.to/aws-builders/it-remembers-across-restarts-and-forgets-mid-conversation-1ehh
- author: Reid Marlow (@reidmarlow)
- at: 2026-11-07T02:19:45Z
- depth: 0

The separation between disk session storage and the prompt's active message window is where a lot of agent architectures leak tokens.

When teams realize their sliding window pruned turn-one context, the instinctive reaction is usually to bump the window size or wire up an LLM summarizer. Bumping the window balloons input token costs and TTFT on turn twenty. An LLM summarizer burns latency and eventually drops precision on specific parameters.

What works reliably is treating conversation history as strictly ephemeral context, while pulling invariants out into agent.state and injecting them into a fixed system manifest header on every invocation. If a user preference, working directory, or target schema lives in structured state and gets injected above the message list, you can keep the sliding window at five or six messages without the agent losing the thread.

### Dev.to · It Remembers Across Restarts — and Forgets Mid-Conversation
- url: https://dev.to/aws-builders/it-remembers-across-restarts-and-forgets-mid-conversation-1ehh
- author: Alex Shev (@alexshev)
- at: 2026-11-07T02:34:06Z
- depth: 0

Separating durable session storage from in-window context is valuable because the remedies are different. A restart test can pass while a long conversation still loses the task’s active constraints. I’d add a contract test that plants a decision-critical fact at several depths and verifies both retrieval and the agent’s behavior, not only whether the text reappears.

### Dev.to · The Limits That Don't Limit
- url: https://dev.to/aws-builders/the-limits-that-dont-limit-2o4j
- author: Pierre-Laurent Medori (@pierrelaurentmedori)
- at: 2026-11-06T09:06:18Z
- depth: 0

The deadline section caught my eye, we once took a reasoning model's silence for a dead job. So I tried it with a stub model on 1.63.0.

With your 20-second tool the run comes back cancelled, but the tool finished anyway and its result is in agent.messages. If that tool charges a card, better check before retrying. Swapping time.sleep(20) for tool_context.cancel_signal.wait(20) gets you out at 5 s with nothing done.Also, the limits restart on every top-level call, so a retry wrapper gets a fresh budget each time unless you pass result.invocation_context.

Do you keep one context across retries of a job, or cap the attempts in the queue?

### Dev.to · The Limits That Don't Limit
- url: https://dev.to/aws-builders/the-limits-that-dont-limit-2o4j
- author: Pierre-Laurent Medori (@pierrelaurentmedori)
- at: 2026-11-07T10:23:57Z
- depth: 2

Thanks a lot for rerunning all of it, you went much further than I did. The split between resuming and a new attempt is the answer I was missing.

### Dev.to · The Limits That Don't Limit
- url: https://dev.to/aws-builders/the-limits-that-dont-limit-2o4j
- author: Kent Bodrov (@innokentyb)
- at: 2026-11-06T14:07:04Z
- depth: 0

The cross-retry boundary also seems important when several workers can act on the same job: a per-invocation hook won’t by itself prevent two concurrent attempts from each spending the remaining quota. Would you put the reservation in a shared, atomic job-level store and reconcile it with the external side effect before releasing it?

### Dev.to · How to red-team an AI support bot before launch: a 30-scenario harness
- url: https://dev.to/pinxiongcn/i-red-teamed-my-own-support-bot-with-30-scenarios-it-failed-7-heres-the-harness-39e7
- author: xcl (@lin7c)
- at: 2026-11-02T13:44:24Z
- depth: 0

The distinction between asserting on the reply string and asserting on side effects is the key shift, and scenario 22 makes it concrete: requires_ticket plus routed_to for disputes catches a polite answer that otherwise scores well on tone and accuracy. One weakness sits in the must_not_say check using re.search over the joined replies. A prohibited phrase inside a negation — stating that a full refund is not available — would fail that check, while a paraphrase that commits to reimbursement without those exact words would pass it. How should the harness separate prohibited commitments from legitimate explanations of a policy boundary? A related timing question: tickets_for runs right after the final turn, so an asynchronously created ticket could produce a false failure unless polling with a short deadline happens before the routing check is declared failed.

### Dev.to · How to red-team an AI support bot before launch: a 30-scenario harness
- url: https://dev.to/pinxiongcn/i-red-teamed-my-own-support-bot-with-30-scenarios-it-failed-7-heres-the-harness-39e7
- author: Reid Marlow (@reidmarlow)
- at: 2026-11-02T14:16:23Z
- depth: 0

One failure mode that bites once you assert on helpdesk side effects is ticket duplication during network retries. When a tool call times out at the HTTP boundary, agent harnesses frequently retry without a unique idempotency key tied to the session and turn. In tickets_for(), checking len(found) &gt; 0 passes even if a flaky webhook spawned three duplicate tickets for the same dispute. Changing that assertion to len(found) == 1 and verifying the idempotency key on the ticket payload catches duplicate write bugs that prompt evals never see.

### Dev.to · How to red-team an AI support bot before launch: a 30-scenario harness
- url: https://dev.to/pinxiongcn/i-red-teamed-my-own-support-bot-with-30-scenarios-it-failed-7-heres-the-harness-39e7
- author: Alex Shev (@alexshev)
- at: 2026-11-02T15:35:20Z
- depth: 0

Thirty scenarios are most valuable when the failures are classified by boundary: instruction injection, unsafe tool use, privacy leakage, unsupported claims, and bad escalation. Keep the adversarial prompt, tool trace, expected stop condition, and a regression label together so a fix does not merely improve one demo path.

### Dev.to · Two specialists, one orchestrator, one catalog
- url: https://dev.to/aws-builders/two-specialists-one-orchestrator-one-catalog-10g8
- author: tercel (@tercelyi)
- at: 2026-11-02T06:29:22Z
- depth: 0

That “115.0 seconds past every synchronous read timeout” line is the kicker. It means your deep-scan flow is definitively in “this must be async” territory: any SDK or HTTP client with the usual 30–60s ceiling will hit its own wall before the work is done, even though the backend is still happily grinding away.

That directly implies one thing: protocol choice becomes a product decision, not an infra detail. If a team insists on blocking message/send semantics for work that looks like your 5-pass, 75–115s scan, they’re basically choosing failure modes and retry storms up front.

Things I’d be curious to measure next, given your data:


For the 95.0s orchestrated review: how much of that is A2A versus AG-UI overhead versus discovery (ListAgentRuntimes + GetAgentCard)?

With ten microVM-backed sessions: what’s the cold-start vs warm path latency distribution, and does the X-Amzn-Bedrock-AgentCore-Runtime-Session-Id pattern introduce any hot-spotting?

On the MCP side pinned to m7g.large / c7g.large: is tool latency meaningfully different from the serverless default at low QPS, or is this mostly about predictable CPU/MEM envelopes?


Also, your registry + RAM setup quietly answers a nasty org problem: “Who owns what agent/tool?” The fact that “payment processing” semantically hits billing suggests you could start tracking drift: when team naming diverges too far from how requesters describe tasks, does search relevance degrade?

### Dev.to · Stopping an Agent From Overreaching: Policy in Enforce Mode
- url: https://dev.to/aws-builders/stopping-an-agent-from-overreaching-policy-in-enforce-mode-4dgf
- author: 1487022216-art (@1487022216art)
- at: 2026-10-24T10:15:39Z
- depth: 0

“Prompt 里的规则是建议，网关上的策略才是门”——这个 takeaway 抓住了本质。LOG_ONLY 先记录三拒一准、再翻转到 ENFORCE 的做法很聪明：等于把策略当灰度发布，先拿到真实的拒绝样本再硬拦截，而不是一上来就把整条对话打断。Default deny 配 ceiling 的组合也很关键，只写 allow 不配 fall-through forbid 会留下缺口。一个想追问的点：ENFORCE 拒绝后，agent 会不会换个说法再试——连续被拒是否会产生“绕路”行为？如果这部分有观测数据会很有价值。

If you are new to Muse, my invite code is F9KUI3 - redeem within 48 hours of joining in Settings &gt; Redeem token (mobile) or Settings &gt; General &gt; Usage &gt; Redeem invite code (web). Disclosure: this is my referral code, exact reward is whatever your own redemption page shows, I am not stating a specific token amount.

### Dev.to · Stopping an Agent From Overreaching: Policy in Enforce Mode
- url: https://dev.to/aws-builders/stopping-an-agent-from-overreaching-policy-in-enforce-mode-4dgf
- author: Odinaka Robert Nnamani (@robertpaschal)
- at: 2026-10-25T00:41:40Z
- depth: 0

The LOG_ONLY step is the part I would copy first. I have seen too many controls go straight to enforce and then get blamed for the first blocked workflow, which is how a good gate gets removed. Recording three denials while nothing breaks gives you real evidence to show the team, and it also exposes the missing permits before they take down a whole conversation. I also like that the ceiling lives on the gateway, not in the prompt: a rule that only the model reads is not a rule when the caller changes.

### Dev.to · Stopping an Agent From Overreaching: Policy in Enforce Mode
- url: https://dev.to/aws-builders/stopping-an-agent-from-overreaching-policy-in-enforce-mode-4dgf
- author: Odinaka Robert Nnamani (@robertpaschal)
- at: 2026-11-02T11:43:01Z
- depth: 2

missing-permission path is exactly where it pays off. finding it in a check beats finding it in prod.

### Dev.to · Stopping an Agent From Overreaching: Policy in Enforce Mode
- url: https://dev.to/aws-builders/stopping-an-agent-from-overreaching-policy-in-enforce-mode-4dgf
- author: Yusef Syed (@yusef_syed_e5513cf2360a92)
- at: 2026-10-28T19:37:38Z
- depth: 0

The LOG_ONLY run is the part I'd keep: the log said DENY and RF-2774152577 still went out, so a decision log isn't the outcome.

One gap the ceiling can't see is that it's per call. Nothing in the Cedar condition stops six 500s on SO-2214 after the 3000 is denied; each one is ALLOW. A cheap check after every test run: sum the refunds per order in the backend and compare that to the limit you meant. Did you try a split request under ENFORCE?

### Dev.to · Reaching Real Systems Without Holding Credentials: Gateway and Identity
- url: https://dev.to/aws-builders/reaching-real-systems-without-holding-credentials-gateway-and-identity-3p6a
- author: Gautam K (@gautamtalksdev)
- at: 2026-10-22T18:21:26Z
- depth: 0

The detail I liked most is the order service echoing which token it saw. That turns the outbound hop into something you can check instead of something you trust.

Question on the write path: the orders credential is scoped to orders.read, but createTicket writes rows, and the gate in front of it is the same inbound JWT the reads use. If you turned the Policy engine on, would you treat the ticketing target differently from the two read targets, or keep one rule for the whole gateway?

### Dev.to · Reaching Real Systems Without Holding Credentials: Gateway and Identity
- url: https://dev.to/aws-builders/reaching-real-systems-without-holding-credentials-gateway-and-identity-3p6a
- author: Gautam K (@gautamtalksdev)
- at: 2026-11-02T22:58:07Z
- depth: 2

The default deny detail is the useful part, thank you. It means turning the engine on is itself a change that can take tools offline, so I would ship the permits first and attach the engine second. The 44 to 56 ms number is helpful too, that is cheap for a gate on the one tool that writes.

### Dev.to · Reaching Real Systems Without Holding Credentials: Gateway and Identity
- url: https://dev.to/aws-builders/reaching-real-systems-without-holding-credentials-gateway-and-identity-3p6a
- author: Gautam K (@gautamtalksdev)
- at: 2026-11-03T17:00:55Z
- depth: 4

That's a better order than mine, thanks. Log only first means the three DENYs show you exactly which permits are missing before anything can go dark. I'll correct my mental model: permits first is only required when the first attach is already in enforce.

### Dev.to · AI Coding in Practice: Refactoring a Zero-Docs Microservice
- url: https://dev.to/aws-builders/ai-coding-in-practice-refactoring-a-zero-docs-microservice-1kkg
- author: Oleksandr (@alexcodebytes)
- at: 2026-10-08T09:28:04Z
- depth: 0

Refactoring a production microservice that unlocks cars with zero documentation sounds like an absolute nightmare scenario. Cutting down scoped work from 2 months to 2 weeks using AI is an insane efficiency boost, but keeping that 90% pass rate on production infrastructure is the real win here.

### Dev.to · AI Coding in Practice: Refactoring a Zero-Docs Microservice
- url: https://dev.to/aws-builders/ai-coding-in-practice-refactoring-a-zero-docs-microservice-1kkg
- author: Oleksandr (@alexcodebytes)
- at: 2026-10-09T16:09:20Z
- depth: 2

Anytime!

### Dev.to · AI Coding in Practice: Refactoring a Zero-Docs Microservice
- url: https://dev.to/aws-builders/ai-coding-in-practice-refactoring-a-zero-docs-microservice-1kkg
- author: ai_adam (@ai_adam)
- at: 2026-10-10T11:01:55Z
- depth: 0

Spec-driven approach ở đây thú vị chỗ nó biến "tribal knowledge" thành artifact có thể version-control và review. 13 steps nghe nhiều nhưng thực tế là chia nhỏ để LLM không bị context overflow — mỗi step một contract rõ ràng (input/output schema, error cases, performance budget).

90% first-pass ấn tượng, nhưng mình muốn hỏi thêm: team bạn handle flaky test/integration test như thế nào khi LLM sinh mock? Và "zero incidents" có tính cả canary deploy hay chỉ staging?

Điểm mạnh nhất bài viết là công khai quy trình chứ không chỉ khoe metric — giúp team khác replicate được thay vì chỉ ngưỡng mộ PS: the tool I meant is on labagent .tech

### Dev.to · How to build EKS with Terraform
- url: https://dev.to/aws-builders/how-to-build-eks-with-terraform-54pl
- author: swapnilgangrade01 (@swapnilgangrade01)
- at: 2022-04-27T14:42:09Z
- depth: 0

Can you put the code in github and please share the link. It will be really helpful
