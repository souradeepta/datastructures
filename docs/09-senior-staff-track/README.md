# Senior / Staff Engineer Interview Track

**Level:** L5+  
**Audience:** Engineers interviewing for Senior (L5), Staff (L6), and Principal (L7) roles  
**Why this exists:** Nearly every interview prep resource stops at L4. Cracking the Coding Interview teaches arrays and trees. System Design Interview books cover LRU caches and URL shorteners. None of them tell you what actually changes when you move up a level.

---

## Who This Track Is For

You are interviewing for a role where:

- The interviewer expects **you** to define the scope, not just solve a given problem
- "How do you influence teams you don't manage?" is a real evaluation axis
- System design questions come with an implicit follow-up: "Now tell me about the org design, failure budget, and migration path"
- Behavioral questions are assessed against leadership principles, not just STAR format
- You are expected to have opinions on technical strategy, not just implementation

If you are preparing for L4 or below, the `docs/01-interview-frameworks/` section covers what you need. This track assumes you already pass coding and basic system design interviews — the bottleneck at L5+ is everything else.

---

## Why This Content Is Rare and Valuable

Most prep content is written by people who recently passed L4 interviews and want to share what worked. That creates a massive selection bias: the internet is full of "how to answer LeetCode medium" and almost nothing on "how to present a technical strategy to skip-level leadership."

The skills evaluated at L5+ are also harder to practice. You can grind 300 LeetCode problems. You cannot grind "write an RFC that drives cross-team alignment" because those skills live in actual work contexts. This track is an attempt to extract the implicit knowledge that strong staff engineers carry and make it legible.

What you will find here:

- **Concrete frameworks** with named steps, not generic advice like "think about trade-offs"
- **Worked examples** that go end-to-end: the vague prompt, the scoping process, the written artifact, the review conversation
- **Failure modes** — what gets candidates rejected at L5+, not just what gets them hired
- **Model answers** for the 10 behavioral scenarios that appear in every staff interview loop

---

## Prerequisites

Before starting this track, you should be able to:

1. Solve medium-difficulty LeetCode problems in 30 minutes (not the focus here, but table stakes)
2. Design a basic web service: load balancer, application servers, database, cache (covered in `docs/03-system-design/`)
3. Explain CAP theorem, eventual consistency, and the trade-offs between SQL and NoSQL (`docs/02-databases/`)
4. Write a coherent STAR story for a behavioral question (`docs/01-interview-frameworks/`)

This track layers on top of those foundations.

---

## How to Use This Track

**Recommended reading order:** Sequential. Each guide builds on the previous one. The first three guides (system design playbook, RFCs, technical strategy) establish the core L5+ mental models. The remaining guides apply those models to specific situations.

**Time estimate:** 2-3 hours per guide if you do the exercises. 45 minutes if you read through without writing anything. Do the exercises — the writing forces clarity that reading alone does not.

**Before your interview:** Read the guide for whatever axis your loop is heaviest on. If you know you have a "leadership and influence" interview, go straight to `05-cross-team-influence.md`. If you have a system design interview, start with `01-staff-system-design-playbook.md`.

---

## Table of Contents

| # | Guide | Level | Description |
|---|-------|-------|-------------|
| 01 | [Staff System Design Playbook](01-staff-system-design-playbook.md) | L5+ | How the L5+ system design interview differs from L4; capacity planning math; failure budget framework; multi-region checklist |
| 02 | [Writing RFCs](02-writing-rfcs.md) | L5+ | Full RFC anatomy; annotated sample RFC; how to drive review and handle disagreement |
| 03 | [Technical Strategy](03-technical-strategy.md) | L5+-L6+ | How to drive 6-month and 2-year technical direction; consensus without authority; decision-making under uncertainty |
| 04 | [Ambiguity and Scoping](04-ambiguity-and-scoping.md) | L5+ | Defining the problem before solving it; scoping rubric; reversibility matrix |
| 05 | [Cross-Team Influence](05-cross-team-influence.md) | L5+-L6+ | Leading without authority; the 4 influence levers; presenting to leadership; negotiating MVAs |
| 06 | [Incident Management](06-incident-management.md) | L5+ | Incident command structure; decision-making under pressure; blameless post-mortems |
| 07 | [Bar Raiser Interviews at Amazon](07-bar-raiser-amazon.md) | L5+ | Senior-level behavioral signals and bar-raiser preparation |
| 08 | [Staff Interviews at Google and Meta](08-staff-google-meta.md) | L5+-L6+ | Role expectations and interview patterns across two companies |
| 09 | [Behavioral Interviews at Scale](09-behavioral-at-scale.md) | L5+-L6+ | Leadership narratives for broad organizational impact |
| 10 | [Mentorship and Technical Leadership](10-mentorship-and-tech-leadership.md) | L5+-L6+ | Growing engineers and leading technical direction |
| 11 | [Compensation and Negotiation](11-compensation-and-negotiation.md) | L5+-L6+ | Evaluating and negotiating senior engineering offers |

---

## A Note on Level Labels

**L5+** means the content is primarily relevant to Senior Engineer (L5 at Google/Meta/Amazon/Microsoft) candidates. Most of the scenarios assume you are a tech lead or the most senior individual contributor on a team.

**L5+-L6+** means the content is relevant at Senior but becomes a primary evaluation axis at Staff. If you are interviewing for a Staff role, the L5+-L6+ guides are where your loop will focus most of its time.

---

## Key Insight

The jump from L4 to L5+ is not about knowing more technology. It is about operating at a higher level of abstraction: you are responsible for the *right problems to solve*, not just for solving problems correctly. Every guide in this track is, in some sense, about that shift.

---

*Last updated: 2026-05-28*
