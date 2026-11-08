# New comments discovered at 2026-11-08T21:30:48+08:00

### Builder Center · It Remembers Across Restarts — and Forgets Mid-Conversation
- url: https://builder.aws.com/content/3Ll4sEZ0YTvNRvbvH4UWe5hUdtz
- comment count 4 -> 11
- comment text is JS-only: read it in a real browser before replying.

### Dev.to · The Limits That Don't Limit
- url: https://dev.to/aws-builders/the-limits-that-dont-limit-2o4j
- author: Kent Bodrov (@innokentyb)
- at: 2026-11-08T11:10:44Z
- depth: 2

Thanks for tracing that to the actual process boundary. One edge case is the reservation TTL expiring while the external effect is still unknown: another worker could acquire capacity before reconciliation finishes. I’d keep an explicit unresolved state and reconcile it before freeing the budget. Would you scope the idempotency key to the logical effect across retries, while keeping a separate ID for each execution attempt?

### Builder Center · The Limits That Don't Limit
- url: https://builder.aws.com/content/3Li5l8UlIgThJpfAkefMsa0hok5
- comment count 5 -> 9
- comment text is JS-only: read it in a real browser before replying.
