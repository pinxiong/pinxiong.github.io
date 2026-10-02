---
title: "AI Coding in Practice: Refactoring a Zero-Docs Microservice"
date: 2026-09-30T21:00:00+08:00
draft: false
summary: "A two-year-old Java microservice with zero documentation, rebuilt in 13 steps with spec-driven AI coding."
tags: ["ai-coding", "spec-driven", "agent", "legacy-refactoring", "ai"]
categories: ["Engineering"]
showTableOfContents: true
images: ["/images/ai-coding-in-practice-zero-docs-microservice/cover.png"]
cover:
image: "/images/ai-coding-in-practice-zero-docs-microservice/cover.png"
alt: "Cover art: 13 steps, 0 docs - a spec-driven AI coding field report with coding time cut from one week to 4 hours, a 90% first-pass rate and zero production incidents"
---

Most backend teams have a service that runs in production and plays a pivotal role in the business. However, nobody knows the full picture of how it behaves. We also have a service like this. It is a digital-key microservice acting as a piece of infrastructure that lets the mobile device lock and unlock a car. It has already run for two years, but has zero documentation. Until recently, the only complete description of how this service behaved was carried in the heads of a few engineers, some of whom moved to other projects.

This article is a field report showing how we used AI coding to refactor this service. The idea of how to refactor it comes from Kiro's design philosophy. We designed 13 steps to make the refactoring process successful. You can benefit from what we learned: what we did well, what we didn't and the results we achieved. The short version: coding time dropped from one week to 4 hours, work we scoped for two people over a month was finished by one person in two weeks, and 90% of the functions passed their first test. One thing we want to emphasize is that it's not a demo, but a real service running in production with zero tolerance for incidents.

## The problem: a service nobody dared to touch

This service spans three ends: the mobile device (Apple, Xiaomi and Huawei), the vehicle (TSP, module and RKE) and the cloud (API, PKI and certificates). Its three communication paths are:

- The mobile device connects to the vehicle over **BLE**, **NFC** and **UWB**.
- The mobile device connects to the cloud over **HTTPS**.
- The vehicle connects to the cloud over **MQTT**.

Every unlock, every permission grant and every key lifecycle event goes through these three ends.

![Three-end coordination: the mobile device, the vehicle and the cloud, connected over BLE/NFC/UWB, HTTPS and MQTT](/images/ai-coding-in-practice-zero-docs-microservice/three-ends.svg)

Three properties made it dangerous to touch:

- **It's production-critical.** A failed key exchange means a customer is left standing next to a car that won't open, under a zero-tolerance SLA.
- **It has zero documentation.** There are no records of two years of change requests, urgent bugfixes and performance optimization. The only documentation is the code itself and the memory that lives in engineers' heads.
- **Knowledge is leaving.** The core engineers who programmed it have moved to other projects. Every question about "why this code is this way" had a half-day turnaround.

The cost showed up in the worst place: debugging. Tracing a cross-end problem (an inconsistent status issue that can only be reproduced when the mobile device, the vehicle and the cloud interact in a specific order) took more than two weeks. Not because the fix was hard, but because understanding the system was hard: there was no call-chain map, no flowcharts, no database schema design docs.

At the same time, business changes are queued up for this service, including internationalization, a batch of new product features and a migration of the service onto our company foundation framework. In practice, that migration consists of replacing Redis with Redisson and externalizing runtime configuration to Nacos. Every requirement means several weeks of learning the code logic before we can change anything. The only solution is spec-driven AI coding — letting AI understand the service first, splitting a requirement into several small specs and then writing code.

## Why AI coding — and why not just let it loose

Why did we choose AI coding here? The decision came down to four observations:

- **The code is the only source of truth — and AI can read it fast.** The code repository is the only trustworthy description of the system, with zero documentation. A person can read only a few hundred lines of code an hour. However, AI can read the whole code repository in minutes. "Zero documentation" is a fatal issue for a human but not for AI — the precondition is that AI's understanding of the source code must be confirmed by a human.
- **Most of the work is mechanical, not creative.** Things like "migrating the service to the company foundation framework", "documenting the call chain" and "generating test cases" are repetitive and well-defined tasks once we have a precise description of the existing behavior.
- **The bottleneck is comprehension, not typing speed.** AI writes code far faster than the team can keep up. The real question, though, was not the model. It was a disciplined workflow: turning "understanding the code, then writing code to meet business requirements" into artifacts a human can review.
- **AI tool cost is covered by the company.** We can use the internal AI coding environment, including its tokens and support. The only real investment was process design.

In other words, the hardest part was never which LLM to pick, but the design of the full workflow: making a probabilistic code generator trusted in a zero-tolerance system.

In the end, we surveyed AI coding products on the market and found that **Kiro's design philosophy** came closest to meeting our needs. We read Kiro's official docs closely before refactoring, and then we designed the solution around our own service, not around the tool's defaults.

### Kiro's design philosophy

Kiro's design philosophy is built on three pillars: distilling proven engineering patterns, respecting developer conventions and maximizing AI capabilities. Those pillars show up as four core capabilities:

- **Specs**: The Specs feature defines three stages crossing requirements (requirements.md), design (design.md) and tasks (tasks.md), with human approval between them. "Prompt" is your wish, but "Spec" is your contract.
- **Steering**: The project's basic rules are written once and are loaded into every interaction, including the product's knowledge, technical specifications and the project's structure. In contrast to AGENTS.md, Kiro supports inclusion modes where agents can run according to a specific mode including always, fileMatch, manual and auto.
- **Hooks**: Hooks let you define an event mechanism to build a workflow automatically. All behaviors that happen in a session are defined as different event types that can trigger actions you define in advance.
- **Custom Agents**: Custom agents are open for developers to design the agent's behavior to meet your needs. What you can set up for your agent includes pre-approving specific tools, limiting tool access, providing relevant context and configuring tool behavior.

In short, three ideas from those capabilities shaped our process: the quality of your context sets the ceiling of AI output; restrictions limit what AI is allowed to do; and different agents serve different purposes.

## The process: 13 steps across four phases

The full flow consists of 13 steps divided into 4 phases. In the diagram below, steps marked with an asterisk are each checked by a separate agent, and every step ends with human review.

![The 13-step process across four phases](/images/ai-coding-in-practice-zero-docs-microservice/process.svg)

### Phase 1 — Understand (Steps 1–3)

**Step 1: Generate tech docs.** AI read the whole codebase and produced architectural docs, per-flow documents and module maps. This was the moment that tribal memory was written down: the system had its own records that didn't depend on anyone.

**Step 2: Generate test cases.** Based on the docs from Step 1, AI generated test cases for APIs and the coverage reached 98%. Why did this step come before any refactoring? Because tests must pin down the current and verified behavior, not AI's intention. As a result, every later refactor had a fixed baseline to be verified against, not an opinion.

**Step 3: Deep code distillation.** AI sorted out the call chain per business scenario, the distribution of error codes, core data structures and the Redis key inventory. This step can turn a **two-week investigation into a four-hour one**.

### Phase 2 — Define (Step 4)

**Step 4: Code standards + harness engineering.** We set up the coding standards, module boundaries, the documentation structure (**specs**, **plans**, **architecture** and **guides**) and the AI coding workflow itself before AI wrote code. This step limited AI's behavior by telling it what, when and how to do it.

### Phase 3 — Refactor & verify (Steps 5–10)

**Step 5: AI refactor.** AI wrote code based on the foundation framework and executed against the specs and standards. The agent never decided when it was done; the Phase 2 contract did.

**Steps 6–8: Three independent verifications.** A consistency-check agent compared the new code against the distilled docs ("does the implementation still match the documented behavior?"). A regression agent ran the Step-2 test suite against the new code. A code-diff agent reviewed the full diff for anything that changed unintentionally. Each check ran in its own agent with fresh context. All three passed through human review before the next phase opened.

**Steps 9–10: Write it back down.** The changes, the optimizations and the known TODOs were documented as part of the work. Everything flowed into the knowledge base. Which is why the refactor is *durable*: the next AI session — or the next engineer — starts from living docs, not from zero.

![Docs structure: specs, plans, architecture, guides](/images/ai-coding-in-practice-zero-docs-microservice/docs-structure.png)

The commit history tells the same story from the other side: design documents first, implementation second.

![Commit history: design and implementation tracked in docs](/images/ai-coding-in-practice-zero-docs-microservice/commit-history.png)

### Phase 4 — Deploy (Steps 11–13)

**Step 11: Deploy & integration.** In contrast to a typical migration, the first full run in the new environment took **20 minutes** — the framework migration was already validated by the Phase 3 gates, so integration was confirmation, not discovery.

**Step 12: Grayscale plan.** The rollout plan was written as a spec and approved by a human gate *before* execution: which traffic slices, in which order, with which abort criteria.

**Step 13: Grayscale release.** We executed the plan. **Zero production incidents.**

## What worked well

![Results: coding time per task from one week to 4 hours (10x faster); one person in two weeks instead of two people in a month; 90% first-pass rate on 98% API coverage](/images/ai-coding-in-practice-zero-docs-microservice/metrics.svg)

- **10x coding productivity increase.** The rewrite cut coding time per task from one week to 4 hours, because the distilled documents and the Step 2 test suite gave AI a clear contract to code against. The saved hours did not disappear; they moved to review, which is where the bottleneck now sits.
- **4x fewer person-months.** We scoped the migration for 2 people over 1 month; 1 person finished it in 2 weeks. The gain came from the documentation phase, not from faster typing.
- **90% first-pass rate.** The Step 2 suite covered 98% of the API surface; 90% of the functions then passed the first 20-minute test. Only two bugs were found throughout the entire process; both were caused by humans. That told us where to invest next: better specs, not a better model.

### How we measured

These numbers come from one service, one team and one release, so read them as a field report, not as a controlled experiment.

- **The comparison is task to task, not run to run.** Before means the same class of change done the old way: reading the code and asking the engineers who wrote it. After means the same change done through the 13-step workflow. The two figures were tracked by the team, by hand. No timers were involved.
- **Coding time excludes review.** Review is not inside the 4 hours, and it is now our bottleneck. The end-to-end saving is real, but smaller than 10x.
- **The test suite was generated from the Step 1 docs.** A behavior the docs describe wrongly is therefore a behavior the suite cannot catch. That is why the critical-path specs were approved by humans against business intent, not only distilled from the code.
- **Tokens were free.** We ran on an internal AI coding environment. Token cost is covered centrally by the company, so it is not part of these results.

## What didn't work

- **Small changes need a full cycle.** Even a tiny change requires running a full workflow.
- **Authorization interruptions.** Executing a long task needs multiple authorization confirmations, which interrupt the work rhythm.
- **Review fatigue.** AI produced output far faster than we could review it.
- **Player vs. referee conflict.** The same agent wrote the code and reviewed its own work, so quality degraded. As a result, production and verification must be executed by two separate agents.
- **Doc-dependent bug analysis.** AI analyzed the bug according to the documentation first instead of the code.

These pain points are process issues, not AI capability limits. Better workflows solve most of them.

## Key takeaways

### Foundational principles

1. **Code without docs is tech debt.** Documentation is the requirement, the unfinished task. Code is merely the result. As a result, the debt stays invisible until something breaks.
2. **Process > AI code generation.** The workflow and standards you design matter more than letting AI write code.
3. **Best model for docs, cheaper for code.** Use the strongest model for documentation generation. In contrast, a standard model is sufficient for code writing.
4. **Review docs > review code.** Reviewing documentation catches more issues than reviewing code. Documentation exposes hidden bugs, because the code is written from the docs.

### Practical wisdom & mindset

1. **Don't rush to manual analysis.** When bugs appear, let AI analyze first: output full call chains as docs, read the docs rather than the code, then let AI fix. This works as long as the docs are sound; the doc caveat from the previous section still applies.
2. **Your taste sets the ceiling.** AI generates code at the level of your code taste. Better code taste means higher AI output quality.
3. **Attitude determines outcomes.** Positive people find ways to help AI succeed. Neutral or negative people spend time finding faults.
4. **Unreasonable becomes reasonable.** After refactoring, previously unreasonable product demands suddenly become feasible. Better harness engineering unlocks new possibilities.

**The model is a component; the process is the product.**
