# New comments discovered at 2026-11-09T20:19:21+08:00

### Builder Center · It Remembers Across Restarts — and Forgets Mid-Conversation
- url: https://builder.aws.com/content/3Ll4sEZ0YTvNRvbvH4UWe5hUdtz
- comment count 11 -> 13
- comment text is JS-only: read it in a real browser before replying.

### Dev.to · The Limits That Don't Limit
- url: https://dev.to/aws-builders/the-limits-that-dont-limit-2o4j
- author: Kent Bodrov (@innokentyb)
- at: 2026-11-09T11:16:11Z
- depth: 5

That unresolved queue needs an owner and a decision deadline, not just a TTL. For a launch review I would want someone accountable for the scope, a forced timeout with an external read-back, a recovery owner, and an explicit stop condition. How do you decide when an unresolved item needs human intervention rather than another reconciliation attempt?

### Dev.to · The Limits That Don't Limit
- url: https://dev.to/aws-builders/the-limits-that-dont-limit-2o4j
- author: Gonzalo Gjuka (@gonzalogjuka)
- at: 2026-11-08T14:39:26Z
- depth: 2

Yes, and that part the API gets right. The limit comes back as HTTP 400: LimitExceeded for Oracle's limit on the tenancy, QuotaExceeded for an admin's quota on the compartment. Oracle's API error table marks both "Retry: No". Host capacity comes back as a 500 with the message "Out of host capacity.", and 500s sit in the retry-with-backoff class. A retry policy can split on status: never retry the 400s, loop on that 500. My loop also matches the message, not just the status, so any other 500 shows up in the log instead of passing for capacity.
