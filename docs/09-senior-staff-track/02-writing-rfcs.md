# Writing RFCs

**Level:** L5+  
**Time:** 40 min to read + 60 min to write a draft RFC  
**Interview weight:** High — "tell me about a time you drove technical alignment" is in almost every Staff loop

---

## Quick Summary

An RFC (Request for Comments) is a written proposal that seeks input from stakeholders before a technical decision is made. Done well, it accelerates alignment, surfaces objections early, and creates a decision record. Done poorly, it creates busywork, gets ignored, or produces paralysis. This guide teaches you when to write one, how to structure it, and how to get it approved.

---

## What Is an RFC and When to Write One

### The Decision Spectrum

Not every technical decision needs an RFC. Staff engineers who write RFCs for everything become a bottleneck. Staff engineers who never write them make decisions in the dark.

| Decision Type | Right Artifact | Example |
|---------------|----------------|---------|
| Small, reversible, one team | Slack message or PR description | Change a config value |
| Medium, one team, lasting impact | Design doc in Confluence | Redesign internal data model |
| **Cross-team, lasting impact, irreversible** | **RFC** | Adopt a new auth standard |
| Org-wide architectural direction | Architecture Decision Record (ADR) | Choose microservices vs. monolith |
| Multi-year technical strategy | Strategy doc + roadmap | Platform migration |

Write an RFC when:
1. The decision affects more than one team's code, operations, or roadmap
2. You are proposing something that is difficult to undo (new protocol, data format, API contract)
3. You need buy-in from people who are not in your management chain
4. You want a record of why the decision was made, not just what was decided

Do NOT write an RFC when:
- The decision is internal to your team and easily reversible
- You have already decided and are going through the motions (this poisons the well — engineers learn that RFCs are theater)
- The decision is urgent and the RFC process would delay critical work

### RFC vs. Design Doc vs. Architecture Decision Record

**Design doc:** Explains how a specific system or feature will be built. Usually written by one team, reviewed by that team's tech lead. Answers: "How will we build X?"

**RFC:** Proposes a cross-cutting technical decision and solicits input. Answers: "Should we adopt X, and how should we standardize it?"

**Architecture Decision Record (ADR):** A lightweight, retrospective record of a decision already made. Often just a few paragraphs. Answers: "Why did we choose X over Y?"

---

## RFC Anatomy

A strong RFC has six sections. Each section has a specific job.

### Section 1: Problem Statement

**Job:** Make every reader agree that this problem exists and is worth solving.

Good problem statement:
> "Our three API gateways (checkout, identity, and inventory) each implement session token validation independently. This has caused three separate production incidents in the past six months when session format changes were applied inconsistently. It also means security patches must be applied in three places. We need a unified auth approach."

Bad problem statement (vague, no evidence):
> "Our authentication is not great and we should improve it."

The problem statement should be falsifiable. A reader should be able to look at it and say "yes, that is a real problem with evidence" or "no, I don't see the evidence for that." If it is not falsifiable, you have not written a problem statement — you have written an opinion.

### Section 2: Context and Background

**Job:** Give readers the information they need to evaluate your proposal without requiring them to be experts.

Include:
- How the current system works (briefly — link to existing docs)
- Why it was built this way originally (avoid sounding like you are blaming)
- Relevant constraints: team structure, existing dependencies, migration costs

This section is where many RFCs fail. The author knows the system deeply and skips context that non-expert readers need. Write for the skeptical PM or the new engineer, not for your co-author.

### Section 3: Proposal

**Job:** Describe your recommended solution in enough detail that an engineer could begin implementation.

Include:
- What you are proposing to change
- What the new system will look like (diagrams help)
- What teams or systems are affected
- Rough implementation timeline and ownership

This section should have a clear recommendation, not "here are some options." The alternatives belong in Section 4. If you cannot make a recommendation, you are not ready to write the RFC yet.

### Section 4: Alternatives Considered

**Job:** Show that you have done the intellectual work of evaluating options, and explain why you rejected the alternatives.

Bad alternative section:
> "We could also keep the current system." (No analysis — this is a strawman)
> "We could build our own solution." (Mentioned but not evaluated)

Good alternative section:
> **Option A: Keep status quo.** The current system works and most of the team knows it. However, it creates an O(n) maintenance burden as we add more services, and the recent incidents show the fragmentation cost is real. Rejected because the maintenance cost will compound.
>
> **Option B: Adopt SAML.** SAML is an established enterprise SSO standard. Our existing IdP (Okta) supports it. Rejected because SAML is XML-based and adds significant parsing overhead; our services are all internal, so the enterprise federation features do not provide value.
>
> **Option C (Recommended): Migrate to JWTs with a shared validation library.** See Proposal section.

### Section 5: Risks and Mitigations

**Job:** Name the things that could go wrong and what you will do about each one.

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Teams do not migrate on schedule | Medium | Medium | Deprecation timeline with tracking dashboard |
| JWT secret rotation breaks active sessions | Low | High | Support both old and new tokens during 2-week transition window |
| Library introduces new bugs | Low | High | 100% unit test coverage + canary deployment before full rollout |
| Security team rejects JWT approach | Low | High | Pre-align with security team before publishing RFC (already done) |

### Section 6: Appendix

**Job:** Supporting material that is useful but would interrupt the flow of the main document.

Include: detailed data, benchmark results, migration scripts, API specs, links to related discussions.

---

## Full Annotated Sample RFC: Migrate Auth from Session Tokens to JWTs

---

**RFC-0047: Unified JWT Authentication for Internal Services**  
**Author:** [Your name]  
**Status:** Draft  
**Created:** 2026-05-20  
**Review deadline:** 2026-06-03  
**Stakeholders:** Platform team, Identity team, Checkout team, Inventory team, Security

---

### Problem Statement

Our platform currently has three separate session token validation implementations (checkout-api, identity-service, inventory-service). In the past six months, this fragmentation caused:

- **2026-02-14 incident (P1, 47 min):** Session format updated in identity-service was not propagated to checkout-api. 12% of checkout attempts failed.
- **2026-04-03 incident (P2, 22 min):** Security patch for token replay attack applied in identity-service; checkout-api remained vulnerable for 11 days.
- **Ongoing:** Security team estimates 3 engineer-days per quarter spent on redundant token management work across teams.

> [ANNOTATION: Good — specific incidents with dates and impact. Not vague.]

We need a single, authoritative token format and validation library that all internal services can use.

---

### Context

Our current session tokens are opaque 64-character random strings stored in Redis. On each request, the calling service must make a synchronous call to identity-service to validate the token and retrieve user metadata. This architecture was designed in 2021 when we had two services; we now have nine.

> [ANNOTATION: Explains the original design decision without blame. "Designed in 2021 when we had two services" is factual, not a criticism.]

The current flow:
```
Client → Service → identity-service (token lookup) → Redis → return user object
```

Each service validation call adds ~8ms of latency (measured P50). For services that validate on every request, this is a fixed per-request cost.

---

### Proposal

Adopt JSON Web Tokens (JWTs) as the standard token format for all internal service authentication.

**Key changes:**
1. identity-service will issue JWTs on login; JWTs will be signed with an RSA-256 private key managed by identity-service
2. All services will validate JWTs locally using a shared Go library (`internal/auth`) without a network call
3. The JWT payload will include: `user_id`, `email`, `roles[]`, `issued_at`, `expires_at`
4. Token expiry: 1 hour for access tokens, 30 days for refresh tokens (matches current session lifetime)
5. Migration window: 12 weeks; all services must adopt by 2026-08-01

**New flow:**
```
Client → Service → local JWT validation (no network call) → proceed
                                 ↓ (if token invalid)
                         Return 401, client refreshes token
```

**Performance improvement:** Eliminates 8ms network call per request. At 50K req/s across all services, this saves ~400ms of cumulative latency per second across the platform.

> [ANNOTATION: Quantified the performance benefit. Numbers make proposals concrete and easier to evaluate.]

---

### Alternatives Considered

**Option A: Shared Redis-backed session tokens (status quo + centralization)**  
Centralize the Redis validation into a single library while keeping opaque tokens. Eliminates code duplication but preserves the network call overhead. Rejected: solves the consistency problem but not the latency or availability problem. If Redis is unavailable, authentication fails platform-wide.

> [ANNOTATION: Specific rejection reason, not just "we don't want this."]

**Option B: mTLS (mutual TLS) for service-to-service authentication**  
Each service gets a certificate; services authenticate each other via TLS handshake. Strong security model. Rejected: mTLS solves service-to-service auth, not user-to-service auth. Our problem is user session tokens, not service identity. mTLS is a complementary concern, not a substitute.

**Option C: SAML SSO**  
Enterprise standard. Rejected: SAML is XML-based and designed for browser-based federation. Our services are internal APIs called by backend clients. SAML overhead and complexity is not appropriate for this use case.

---

### Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Teams don't migrate by deadline | Medium | Medium | Bi-weekly migration status in platform meeting; deprecation warning logs in old flow starting week 8 |
| JWT secret key compromise | Low | Critical | RSA keys stored in Vault; rotation procedure documented; 1-hour token expiry limits blast radius |
| Clock skew between services causes premature expiry | Low | Medium | JWTs use server-issued timestamps; clients do not set expiry; 5-minute skew tolerance in validation library |
| Service that can't easily migrate | Unknown | Medium | Identify outliers in week 1; assess on a case-by-case basis |

> [ANNOTATION: The "unknown" likelihood for the last row is honest. Pretending you have perfect knowledge undermines credibility.]

---

### Migration Plan

**Weeks 1-2:** Ship `internal/auth` library (Go). Write integration tests. Security review.  
**Weeks 3-4:** Migrate identity-service to issue JWTs. Run in dual-mode (issue JWT + old token for same login).  
**Weeks 5-10:** Teams migrate services. identity-service validates both formats during transition.  
**Week 11:** Stop issuing old tokens. Old tokens expire within 24h (current session TTL).  
**Week 12:** Remove old token validation code from identity-service.

---

### Appendix

- [JWT spec (RFC 7519)](https://datatracker.ietf.org/doc/html/rfc7519)
- Internal/auth library draft PR (link intentionally omitted)
- Security team pre-approval email thread (link intentionally omitted)
- Benchmark results: JWT vs. Redis validation latency (link intentionally omitted)

---

## How to Drive the Review Process

Writing a good RFC is half the work. Getting it approved requires managing the social process.

**Before you publish:**
- Pre-align with your most important stakeholders 1:1 before the RFC goes public. If the security team lead is going to object, you want to know before the RFC is live, not after. Use these 1:1s to gather objections and either address them in the RFC or understand them well enough to respond during review.
- Identify the minimum set of approvals you need. For a cross-team RFC, this is usually: one technical approver per affected team + one approver from the platform or architecture team.

**Review period:**
- 2 weeks is standard for most RFCs. Less than 1 week signals you do not really want input. More than 3 weeks signals low urgency and the RFC will get deprioritized.
- Set an explicit review deadline in the RFC header.

**Handling disagreement:**
- Separate disagreement about *what* from disagreement about *whether*. "I think Redis is actually fine for this use case" (what) is different from "I think we should not standardize auth at all" (whether). The first is addressable. The second requires a separate conversation about problem framing.
- When someone raises an objection, resist the urge to immediately argue. Instead, ask: "Can you say more about the failure mode you are worried about?" Often the objection is more specific than the initial statement, and the specific version is either something you can address or something you had not considered.
- If you cannot get to consensus, escalate to a tech lead or architecture council. The goal of an RFC is not unanimous agreement — it is alignment. Document the objections and explain the decision-making process.

**After approval:**
- Update the RFC status to "Accepted" and add a decision summary at the top
- Send a summary to all stakeholders, not just the reviewers
- Create the implementation tracking tickets and link them from the RFC

---

## Signs Your RFC Will Be Rejected

- **No clear recommendation:** "Here are three options" without a recommendation puts the decision burden on reviewers. They will ask you to decide.
- **Strawman alternatives:** An alternative that is obviously bad and included only to make your proposal look good. Readers notice this and it damages your credibility.
- **Missing stakeholders:** If an affected team discovers the RFC via the company Slack after it is "approved," you have a political problem that will slow or block implementation.
- **Vague problem statement:** If the problem could be solved multiple ways and the RFC only addresses one, reviewers will wonder if you explored the space.
- **No migration plan:** "We will figure it out" is not a migration plan. The most common RFC objection is "this sounds expensive to migrate to."

---

## Interview Scenario

**"Tell me about a time you drove alignment on a technical decision."**

Use this structure, anchored in an RFC story:

1. **Situation:** Set up the problem. What was the technical mess and why was it a problem?
2. **Stakeholders:** Who had to agree and why was it hard? (Different incentives, history of failed attempts, competing priorities)
3. **Your approach:** How did you structure the proposal? Who did you pre-align with and why?
4. **Friction:** What objection or disagreement came up? (If none, it was not a hard alignment problem)
5. **Resolution:** How did you reach agreement? Was it full consensus or a decision you made with documented tradeoffs?
6. **Outcome:** What happened after the decision? What did you learn?

If you cannot fill in step 4, find a different story. An alignment story without friction is an easy story, and easy stories do not demonstrate L5+ behavior.

---

*Next:* [Technical Strategy](03-technical-strategy.md) — how to drive 6-month and 2-year technical direction
