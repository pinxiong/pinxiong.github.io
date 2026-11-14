---
title: "The End of Tech Debt Is AI"
subtitle: "Rebuilding an undocumented microservice into a knowledge base"
date: 2026-10-17
event: "AWS Community Day Shenzhen 2026"
eventUrl: "https://2026-autumn.awscommunityday.cn/speakers"
brochureUrl: "https://mp.weixin.qq.com/s/t_rL67xd40TrCb_qsPqlRw"
location: "Shenzhen, China"
role: "Speaker"
track: "Spark Bridge · 星火桥"
talkTime: "14:30–15:00"
cover: "/images/speaking/aws-community-day-2026/talk-stage-01.jpg"
tags: ["AI Coding", "Microservices", "Knowledge Base", "Java"]
summary: "A production microservice with no documentation, no tolerance for failure, and two years of accumulated tech debt — rebuilt by AI agents in 13 steps, with the git history to prove it."
showTableOfContents: false
showAuthor: false
showRelatedContent: false
showDate: false
---

<div class="talk-hero">
  <img src="/images/speaking/aws-community-day-2026/talk-stage-01.jpg" alt="Pin Xiong presenting at AWS Community Day Shenzhen 2026">
</div>

<div class="talk-facts">
  <div><span>Event</span><a href="https://2026-autumn.awscommunityday.cn/speakers" target="_blank" rel="noopener">AWS Community Day Shenzhen 2026</a></div>
  <div><span>Date</span>17 October 2026</div>
  <div><span>Track</span>Spark Bridge · 星火桥</div>
  <div><span>Slot</span>14:30–15:00</div>
</div>

<div class="talk-links">
  <a href="https://mp.weixin.qq.com/s/t_rL67xd40TrCb_qsPqlRw" target="_blank" rel="noopener">Event guide · 活动宣传册 ↗</a>
  <a href="https://2026-autumn.awscommunityday.cn/speakers" target="_blank" rel="noopener">Speakers page ↗</a>
</div>

Most teams treat a legacy service as a black box they are afraid to touch. This talk is the opposite: a two-year-old Java/Spring Boot microservice, running in production across three ends — mobile app, vehicle, and cloud — with **no documentation at all** and **zero tolerance for downtime**, taken apart and rebuilt with AI agents.

The original Chinese title was 技术债的尽头是 AI：一个微服务从零文档到知识库的重构之路. The English version keeps the part that matters: the debt was never the code. It was the missing knowledge.

## What the talk covers

- How to build system comprehension in a codebase nobody documented, using AI agents as readers before using them as writers.
- A 13-step flow borrowed from Kiro's design philosophy — understand, define, rebuild, deploy — with the actual git commits and knowledge-base layout shown on screen.
- The "athlete and referee" pattern: separate agents for producing changes and for judging them, so the model that writes the code never grades its own homework.
- Which steps should stay manual. The honest answer is not "let the agent do everything."

## The numbers, as presented

| Measure | Planned | Actual |
| --- | --- | --- |
| Coding | 1 week | 4 hours |
| Integration testing | 1 week | 2 days |
| First integration pass | — | 20 minutes, 90% of features verified |
| Bugs found | — | 2, both human error |
| Pitfalls documented | — | 5 |

The talk deliberately keeps the failures in. A report that only shows the wins is marketing, not engineering.

## The conclusion I actually wanted to land

**Process, not the model, is where the safety comes from.** The 13 steps would work with Kiro, with Qoder, or with a plain chat window. The harness is the asset; the model is swappable. That is also why the same flow is reusable on the next legacy service instead of being a one-off story.

## Photos from the session

Three frames, three distances: the room, the talk, and the table.

<div class="talk-photos">
  <figure class="talk-photos-wide">
    <img src="/images/speaking/aws-community-day-2026/group-photo-01.jpg" alt="Speakers, volunteers and attendees of AWS Community Day Shenzhen 2026 gathered in the auditorium, holding the User Group 上海 and User Group 深圳 banners">
    <figcaption>The room. Around 600 developers in the hall, with the Shanghai and Shenzhen User Group banners up front.</figcaption>
  </figure>
  <figure>
    <img src="/images/speaking/aws-community-day-2026/talk-stage-02.jpg" alt="Running the refactoring demo from the podium laptop during the session">
    <figcaption>The talk. Running the 13-step refactor live from the podium laptop.</figcaption>
  </figure>
  <figure>
    <img src="/images/speaking/aws-community-day-2026/portrait-namecard.jpg" alt="At the speaker table before the session, name card on the desk">
    <figcaption>The table. At the speaker desk before the session — <span class="nowrap">熊聘</span> on the card.</figcaption>
  </figure>
</div>

## Slides and recording

Slides are being cleaned up for publication. If you want the deck or the 13-step checklist before then, email me at [pinxiong.cn@gmail.com](mailto:pinxiong.cn@gmail.com) and I will send it over.

The written version of this talk is a series on the blog: start with [AI Coding in practice: rebuilding a zero-docs microservice](/posts/ai-coding-in-practice-zero-docs-microservice/).
