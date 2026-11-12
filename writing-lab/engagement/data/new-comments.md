# New comments discovered at 2026-11-12T21:30:41+08:00

### Dev.to · Orchestrating Agents: Nobody Decides Who Goes Next
- url: https://dev.to/aws-builders/orchestrating-agents-nobody-decides-who-goes-next-2cg4
- author: Omid (@justcallmeomid)
- at: 2026-11-11T14:36:27Z
- depth: 0

"Completed means no node asked for help" is the line I'd put at the top of every multi-agent doc. I hit the same thing from the other side: an agent's own "tests pass" only meant something once the tests ran in a step the agent doesn't control, so the acceptance check sat outside the model's turn. Your six-word vs eight-word runs show why that matters even when the status says completed: the status measures whether anyone asked for more work, not the deliverable.

For your graph piece, one data point on what fixed edges buy: in my setup the order of steps is a YAML file the runtime follows, not a model's tool call, and a separate judge, not the agent that wrote the fix, decides whether another repair round is worth running. Disclosure: I build Kraft SDLC (write-up: dev.to/justcallmeomid/i-stopped-ba...)

### Dev.to · Orchestrating Agents: Nobody Decides Who Goes Next
- url: https://dev.to/aws-builders/orchestrating-agents-nobody-decides-who-goes-next-2cg4
- author: Adem İşler (@ademisler)
- at: 2026-11-11T15:56:03Z
- depth: 0

the six-word vs no-deliverable runs both returning completed is the key failure mode here. i'd put a deterministic gate after the swarm: check the saved brief exists, validate the expected token total and cost, and record timed-out turns separately. model-led routing is useful; treating silence as success isn't.

### Builder Center · When "Not Found" Doesn't Mean "Never Happened"
- url: https://builder.aws.com/content/3Ls8Su63RbuSKR3yys1j9t6US1p
- author: Maicon (@akablame)
- at: 2026-11-11T16:20:25+00:00

Thanks!
