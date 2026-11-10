# New comments discovered at 2026-11-10T21:31:09+08:00

### Builder Center · When "Not Found" Doesn't Mean "Never Happened"
- url: https://builder.aws.com/content/3Ls8Su63RbuSKR3yys1j9t6US1p
- author: Purva Jain (@purvajain30)
- at: 2026-11-10T11:31:30+00:00

👍

### Builder Center · When "Not Found" Doesn't Mean "Never Happened"
- url: https://builder.aws.com/content/3Ls8Su63RbuSKR3yys1j9t6US1p
- author: Benjamin Kincses (@dextheking)
- at: 2026-11-10T09:48:35+00:00

The fence and the witness were run separately. What breaks if you run both at once? If the fence rejects the late commit and the witness still holds the slot in outcome\_unknown, does the retry wait for a terminal state that never arrives, or does the fence rejection count as terminal?

### Builder Center · When "Not Found" Doesn't Mean "Never Happened"
- url: https://builder.aws.com/content/3Ls8Su63RbuSKR3yys1j9t6US1p
- author: Saurabh Arup Mukherjee (@muks04)
- at: 2026-11-10T08:35:57+00:00

Interesting One!

### Builder Center · When "Not Found" Doesn't Mean "Never Happened"
- url: https://builder.aws.com/content/3Ls8Su63RbuSKR3yys1j9t6US1p
- author: Mohammed Mudasser (@muddu)
- at: 2026-11-10T06:06:15+00:00

Nice

### Builder Center · When "Not Found" Doesn't Mean "Never Happened"
- url: https://builder.aws.com/content/3Ls8Su63RbuSKR3yys1j9t6US1p
- author: Muhammad Talha Khan (@muhammadtalhakhan06)
- at: 2026-11-10T05:23:12+00:00

Really Interesting!

### Builder Center · When "Not Found" Doesn't Mean "Never Happened"
- url: https://builder.aws.com/content/3Ls8Su63RbuSKR3yys1j9t6US1p
- author: Robin kumar (@robinkumar)
- at: 2026-11-10T02:42:40+00:00

Interesting engineering problem. Lease expiration should not be treated as proof that an operation never completed. A worker may lose its lease while an earlier operation is still in flight, creating opportunities for duplicate writes or stale commits.

I would address this using idempotency keys, fencing tokens, and conditional writes to prevent outdated workers from modifying newer state. Reconciliation should also verify the actual operation state before retrying.

The key takeaway is that distributed systems must distinguish between failure to observe completion and actual failure of the operation. Designing for delayed execution and duplicate delivery is essential for consistency.

### Builder Center · When "Not Found" Doesn't Mean "Never Happened"
- url: https://builder.aws.com/content/3Ls8Su63RbuSKR3yys1j9t6US1p
- author: Rutuja Gophane (@rutujaa07)
- at: 2026-11-10T02:39:03+00:00

Great
