# New comments discovered at 2026-11-11T21:31:02+08:00

### Dev.to · Testing async side effects in an LLM agent harness: tickets, retries, and exactly-once
- url: https://dev.to/pinxiongcn/testing-async-side-effects-in-an-llm-agent-harness-tickets-retries-and-exactly-once-5c93
- author: 于侃 (@aiapikey)
- at: 2026-11-10T13:32:19Z
- depth: 0

The false-red half is the cheap lesson; "a passing test can be a lie" is where I would spend the effort, because that half is invisible.

The way to make it visible is a negative control per assertion: point the harness at a deliberately broken worker - one that never commits, one that commits twice - and require the test to fail in both. An assertion that stays green against a broken side effect is not measuring routing, it is measuring the absence of a crash. Twenty lines of setup, and it upgrades every scenario in the suite at once.

The same trick catches the duplicate hole: if a worker that writes twice does not turn any assertion red, then nothing in the suite actually covers exactly-once.

Worth adding to the fix list, since it is the only item that checks the tests themselves.

### Builder Center · When "Not Found" Doesn't Mean "Never Happened"
- url: https://builder.aws.com/content/3Ls8Su63RbuSKR3yys1j9t6US1p
- author: David Sebastian Barrera Gaona (@sebasgao)
- at: 2026-11-11T03:10:37+00:00

Thanks so much

### Builder Center · When "Not Found" Doesn't Mean "Never Happened"
- url: https://builder.aws.com/content/3Ls8Su63RbuSKR3yys1j9t6US1p
- author: astronomad (@astronomad)
- at: 2026-11-10T23:09:35+00:00

Thanks for sharing.

### Builder Center · When "Not Found" Doesn't Mean "Never Happened"
- url: https://builder.aws.com/content/3Ls8Su63RbuSKR3yys1j9t6US1p
- author: Farooq Butt (@farooq91)
- at: 2026-11-10T20:34:11+00:00

enojyed the read

### Dev.to · The Limits That Don't Limit
- url: https://dev.to/aws-builders/the-limits-that-dont-limit-2o4j
- author: Gonzalo Gjuka (@gonzalogjuka)
- at: 2026-11-10T16:43:14Z
- depth: 6

Fair question, and the honest answer is that I do not have that refusal yet. Access is by request, so nobody has reached a buy decision I can quote. What I have are the refusals from threads, and they came in three shapes. "Most tools still ask for one big credential up front": they wanted a key per provider they could revoke on its own, and we do not have that, it is one read-only credential per provider per org. "Can it run in CI?": no, the pre-flight only runs in the app, there is no API. "Does it check quotas?": no, and I said so. Nobody said the problem was not real. They said the thing I had was one layer short of where their pain lived.

On the identity point, you caught a real gap. Our inventory is reduced to counts per region from whichever credential the org connected, and the check never prints which tenancy or account those counts came from. Connect the wrong account and the list is honest and useless. Putting the identity in the output is the fix, and it is cheap.
