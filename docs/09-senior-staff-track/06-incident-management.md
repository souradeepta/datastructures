# Incident Management

**Level:** L5+  
**Time:** 40 min to read + 60 min to write a practice post-mortem  
**Interview weight:** Medium-high — "tell me about a production incident you managed" appears in most senior loops

---

## Quick Summary

Production incidents are where Staff engineers earn their pay. Anyone can write code that works in development. L5+ engineers are expected to stay calm under pressure, make clear decisions with incomplete information, communicate clearly to multiple audiences simultaneously, and then extract learning from the incident afterward. This guide teaches the structure for doing all of that.

---

## Incident Command Structure

Large or high-severity incidents benefit from explicit role assignment. The worst incidents are the ones where 8 engineers are all trying to fix the same thing, nobody is communicating to stakeholders, and decisions get made by whoever speaks loudest.

### The Four Roles

**Incident Commander (IC)**
- Owns the incident from detection to resolution
- Makes the final call on all escalation and mitigation decisions
- Does not do deep technical debugging — delegates that
- Communicates with non-technical stakeholders (leadership, support, comms)
- Keeps the incident channel focused and productive

**Communications Lead**
- Writes all external status page updates
- Drafts executive summaries for leadership
- Coordinates with Customer Success and Support on customer messaging
- Ensures the incident channel does not get flooded with status questions ("what is happening?") that distract the tech leads

**Technical Lead (Tech Lead)**
- Owns the investigation: diagnosis, hypothesis formation, mitigation
- Delegates specific investigation tasks to engineers
- Reports findings to the IC with recommended actions
- Does NOT independently decide to apply risky changes — gets IC sign-off

**Scribe**
- Takes timestamped notes throughout the incident
- Records: what was tried, what was found, who made decisions and when
- Does not need to be technical — junior engineer, TPM, or EM works well
- Output becomes the timeline section of the post-mortem

### Role Assignment in Practice

For a P1 (critical) incident involving > 2 engineers, explicit role assignment should happen within the first 5-10 minutes. The person who calls the incident does not automatically become the IC — assign the most experienced available person.

For P2-P3 incidents (significant but not critical), one person often covers IC + Technical Lead. The communications lead and scribe roles may not be needed for smaller incidents.

---

## The Incident Response Timeline

```
DETECT → TRIAGE → MITIGATE → RESOLVE → REVIEW
   |         |          |          |         |
[alert,   [scope,    [stop the   [full     [post-
customer  severity,  bleeding]  recovery] mortem]
report,   owner
anomaly]  assignment]
```

### Phase 1: Detect

Incidents surface from three places:
- Automated alerts (preferred — the earlier, the smaller)
- Customer reports / support tickets
- Engineer discovers anomaly during development

The quality of your alerting determines the quality of your detect time. If you are regularly finding out about incidents from customer reports before your alerts fire, you have an observability problem that is a pre-incident fix.

**First 2 minutes:** Acknowledge the alert. Post in the incident channel: "Investigating [alert name]. [Your name] is looking." This prevents 3 other engineers from independently starting to look at the same thing.

### Phase 2: Triage

Answer three questions as fast as possible:

1. **What is broken?** (Customer-visible impact: can users check out? Is data being lost? What percentage of requests are affected?)
2. **How severe is it?** (P1: all users, core flow. P2: significant percentage of users, degraded experience. P3: minor impact, has workaround.)
3. **Who should be involved?** (Call in the right people. Do not page the database team for an application-level bug. Do not try to fix a database failure without the database team.)

Time box triage: if you have not answered all three questions in 10 minutes, escalate. You are probably missing information or have the wrong people on the call.

### Phase 3: Mitigate

Mitigation means stopping the customer impact as fast as possible. Mitigation is not the same as root cause fix.

Common fast mitigations:
- **Rollback:** Revert the last deployment. This is almost always the right first instinct if there is a recent deploy.
- **Feature flag:** Turn off the feature that is causing the issue.
- **Traffic shed:** Route traffic away from a broken region or instance.
- **Circuit breaker:** Stop calling a broken downstream dependency; return cached or degraded results instead.

Do not try to fix the root cause under incident pressure unless the fix is trivially simple. Introducing a code change during an active incident when you are stressed and moving fast is a high-risk move. Mitigate first, fix properly afterward.

**Decision-making discipline:** The IC makes the call on risky mitigations. If the Tech Lead wants to apply a database migration during an active incident to fix the root cause, the IC decides whether the risk is worth it. The answer is usually: no, mitigate first.

### Phase 4: Resolve

The incident is resolved when the customer impact is fully ended, not just when mitigation is in place. Mitigation and resolution are different:

- **Mitigated:** "We rolled back the deploy. Error rate is dropping."
- **Resolved:** "Error rate is back to baseline. All affected requests have recovered. No remaining customer impact."

Before closing the incident, do a brief debrief: "Is there anything still broken that we might have missed?" and "Do we need to take any immediate action before the post-mortem?" (Data backfills, customer notifications, immediate monitoring changes.)

### Phase 5: Review (Post-Mortem)

The post-mortem is not optional at P1 and not optional at P2 in most engineering orgs. See the Post-Mortem section below.

---

## During the Incident: Decision-Making Under Pressure

### The 3-Minute Rule

If the team has been discussing a mitigation for more than 3 minutes without deciding, the IC should force a decision: "We have been discussing this for 3 minutes. What is the risk if we apply [option A]? What is the risk if we do not? I am going to call it in 60 seconds."

Incident channels can become paralyzed by the same caution that makes good engineers slow to merge PRs in normal times. During an active incident, the cost of inaction (continued customer impact) usually exceeds the cost of a slightly imperfect mitigation.

### When to Escalate

Escalate to the next level of leadership when:
- The incident is likely to exceed your SLA / failure budget
- You need resources you do not have (additional engineers, vendor support, infrastructure changes)
- There is customer data loss or security exposure
- You have been in active incident mode for > 1 hour without clear mitigation

Escalation is not failure. Waiting too long to escalate because you do not want to "bother" the VP is the failure.

### Runbook Discipline

A runbook is a documented procedure for diagnosing and mitigating a known failure mode. Good runbooks:
- Are linked from the alert that fires
- Include specific commands to run, not just "check the database"
- Are tested quarterly (run the runbook in a staging environment to verify it still works)
- Are updated after every incident where they were used

During an incident, follow the runbook first. If the runbook does not resolve the issue, deviate — but document that you deviated and why. This becomes a post-mortem action item: update the runbook.

---

## Full Post-Mortem Template

```markdown
# Post-Mortem: [Incident Name]

**Severity:** P1 / P2 / P3
**Date:** [YYYY-MM-DD]
**Duration:** [Start time] → [End time] ([total duration])
**On-call responders:** [Names]
**Incident Commander:** [Name]
**Affected service(s):** [List]
**Customer impact:** [Describe in plain language: "12% of checkout attempts failed for 45 minutes"]

---

## Executive Summary
[3-4 sentences. What happened, what the impact was, and what the immediate fix was.
Written for a non-technical audience.]

---

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 14:23 | Automated alert: checkout error rate exceeds 5% threshold |
| 14:24 | @engineer1 acknowledged alert, started investigation |
| 14:27 | Identified that error rate was 12%, concentrated in EU region |
| 14:31 | Paged DB team lead — suspected database issue |
| 14:38 | DB team confirmed: primary database node in EU was unhealthy; reads were being routed to a replica that was 4 minutes behind |
| 14:42 | Decision: force failover to secondary primary in EU. IC sign-off obtained |
| 14:45 | Failover initiated |
| 14:52 | Error rate back to < 0.1%. Incident mitigated |
| 15:10 | Root cause investigation confirmed: EU primary ran out of disk space due to WAL buildup |
| 15:30 | Disk space remediated. WAL configuration corrected |
| 15:35 | Incident resolved |

---

## Root Cause

[Describe the technical root cause in specific terms. Avoid "human error" as a root cause — human error is a symptom of a system that makes errors easy.]

The EU database primary ran out of disk space due to accumulation of Write-Ahead Log (WAL) segments. WAL archiving was configured to archive to S3, but the S3 IAM policy had expired (certificate rotation 2026-02-01). Archiving had been silently failing for 15 days, during which WAL segments accumulated locally. When disk reached 100%, the primary became unhealthy and Postgres stopped accepting writes.

---

## Contributing Factors

[List the conditions that made this incident possible or worse. Each contributing factor is a potential action item.]

1. S3 IAM certificate rotation happened without a corresponding update to the database archiving configuration
2. WAL archiving failures were not alerting — they were logged at WARN level only
3. Disk utilization alerting threshold was set at 90% but never fired because disk went from 70% to 100% rapidly once archiving started failing
4. The EU primary disk was smaller than the US primary due to a provisioning discrepancy from 2024

---

## What Went Well

- Alert detection was fast (23 seconds from threshold breach to page)
- DB team responded within 7 minutes of being paged
- IC made the failover decision quickly; no analysis paralysis
- Runbook for DB failover was accurate and followed correctly

---

## What Went Poorly

- WAL archiving silently failing for 15 days without any alert
- The connection between IAM certificate rotation and database configuration was not documented
- First 10 minutes of investigation were spent on application logs before escalating to the DB team

---

## Action Items

| Action | Owner | Due | Priority |
|--------|-------|-----|----------|
| Add alert: WAL archiving failure logs at ERROR level | DB team | 2026-06-10 | P1 |
| Add alert: WAL archiving lag > 5 minutes | DB team | 2026-06-10 | P1 |
| Add disk utilization trend alert (rate of change, not just threshold) | Infra team | 2026-06-17 | P1 |
| Document IAM certificate rotation runbook to include DB archiving config check | DB team | 2026-06-24 | P2 |
| Normalize EU and US database disk sizes | Infra team | 2026-07-01 | P2 |
| Add WAL archiving status to weekly infrastructure health review | Infra EM | 2026-06-10 | P2 |

---

## Appendix

- [PagerDuty incident link]
- [Datadog dashboard showing error rate spike]
- [Slack incident channel transcript]
- [DB failover runbook]
```

---

## Annotated Sample Post-Mortem: Database Primary Failure

**Incident:** EU database primary went unhealthy, causing 45 minutes of 12% checkout failure rate.

### What made this a good post-mortem:

**1. The timeline is timestamped and specific.**
Bad timeline: "The database went down and we fixed it."
Good timeline: Each step has a time, an actor, and an observation. An engineer who was not on call can reconstruct exactly what happened.

**2. The root cause is specific and traceable.**
Bad root cause: "Database configuration issue caused the failure."
Good root cause: "S3 IAM certificate rotation on 2026-02-01 caused WAL archiving to silently fail for 15 days, resulting in disk exhaustion."

Note that "certificate rotation" is not a human error — it is a system design flaw (archiving failures did not alert). A bad post-mortem would say "operator failed to update the IAM policy." A good post-mortem says "the system had no mechanism to detect the archiving failure."

**3. Contributing factors are separate from root cause.**
The root cause is one thing. Contributing factors are the system conditions that made the incident worse or made the root cause possible. Separating them produces more actionable action items.

**4. Action items are specific, owned, and time-bound.**
Bad action item: "Fix alerting."
Good action item: "Add alert: WAL archiving failure logs at ERROR level. Owner: DB team. Due: 2026-06-10."

**5. "What went well" is not empty.**
Post-mortems that only list what went wrong produce demoralized teams. Acknowledging what worked (fast alert, accurate runbook) reinforces behaviors you want to repeat.

### What a bad post-mortem looks like:

- "Root cause: human error — engineer did not update the IAM policy." (Blame, not system analysis)
- "Resolution: fixed the database." (Not specific enough to prevent recurrence)
- No contributing factors section (misses the structural issues)
- Action items: "Be more careful with certificate rotation." (Not actionable)
- No timeline (cannot reconstruct what happened)

---

## Blameless Culture: Why "Human Error" Is Never the Root Cause

The concept of blameless post-mortems comes from the insight that complex systems have many failure modes, and humans operate within those systems. When a human makes a mistake, the question to ask is not "why did this person make a mistake?" but "what about the system made this mistake easy to make and hard to detect?"

If your engineer ran a delete query on the wrong database, "human error" is not the root cause. The root causes are:

- Why could the engineer access the production database directly?
- Why was there no confirmation prompt for destructive operations?
- Why was there no read-only access policy that required elevated permissions for writes?
- Why did the system not have point-in-time recovery enabled so the mistake was recoverable?

Each of those is a system design failure. The human was operating within a system that made the mistake easy. Blame-based post-mortems do not fix systems — they make engineers afraid to admit mistakes, which makes future incidents harder to detect and harder to diagnose.

A blameless post-mortem is not blame-less in the sense that nobody was responsible. It is blame-less in the sense that the question is "how do we design the system so this cannot happen again?" not "who did this and how do we prevent them from doing it again?"

---

## Interview Scenario

**"Tell me about a production incident you managed."**

The interviewer is evaluating several things:
- Did you stay calm and organized under pressure?
- Did you communicate clearly to multiple audiences?
- Did you make decisions without perfect information?
- Did you extract learning and drive systemic change afterward?

**Model answer:**

"In late 2025, we had a P1 incident on our payment service. It was 11 PM on a Friday. Our fraud detection model started returning errors for 15% of transactions, and our payment flow was hard-failing instead of falling back to a lower-confidence check.

I took the IC role since I was the most senior person awake. First thing I did was assign explicit roles: I had one engineer on technical investigation, one on customer communication (we had customers reporting declined cards on Twitter), and I asked a PM to join as a non-technical observer so they could give me real-time customer sentiment.

The technical investigation took 8 minutes to identify: the fraud detection service was returning HTTP 503 because it was hitting a memory limit. The underlying cause was a model we had deployed 6 hours earlier that had a much larger working set.

I had two options: roll back the model (30-minute process with data validation steps) or increase the memory limit temporarily and route around the errors. I chose the memory increase because it was faster — 5 minutes to apply — and I wanted to stop the customer impact before we spent 30 minutes on a clean rollback. We applied the memory increase, the 503s stopped, and then I rolled back the model properly over the next 40 minutes while the service was healthy.

The post-mortem found three systemic gaps: our deploy pipeline for ML models did not validate memory requirements against the production resource limits before deploying; our payment service did not have a fallback mode for fraud service failures; and the on-call handoff at 10 PM had not flagged the model deployment as a recent change.

We fixed all three. The ML model deploy pipeline now gates on a memory smoke test. The payment service now has a fallback tier. And our incident handoff template now includes 'recent deployments in the last 4 hours.'"

**Why this answer is strong:** Specific timeline and decisions. Explicit role assignment. Two options evaluated with reasoning. Both short-term mitigation and long-term fix are separated. Post-mortem action items are specific and systemic, not blame-based. The answer demonstrates IC behavior, not just "I debugged a thing."

---

*Related:* [Database Monitoring](../02-databases/24-database-monitoring.md) — reliability measurement and alerting practices
