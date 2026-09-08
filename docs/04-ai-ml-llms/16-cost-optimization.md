# Cost Optimization for ML — Reducing Spend Without Sacrificing Quality

**Level:** L5-L5+
**Status:** draft
**Audience:** ML platform engineer preparing an L5 cost/performance design review.
**Prerequisites:** token accounting, inference serving, caching, batching, and basic financial modeling.
**Sequence:** Batch 3A, 4/5
**Terra gate:** open
**Time to read:** ~20 min

Practical strategies for 10-100× cost reduction: model compression, inference optimization, caching, and infrastructure right-sizing.

## Learning objectives

- Convert request volume, token counts, price, utilization, and cache hits into a unit cost.
- Compare routing, caching, quantization, batching, and distillation without assuming their savings multiply perfectly.
- Design budgets, quotas, attribution, and alerts that preserve quality and privacy.
- Explain when a cheaper path is unsafe because it increases latency, stale answers, or quality failures.

## What it is

ML cost optimization is the controlled reduction of cost per useful outcome. For
LLM workloads, separate input tokens, output tokens, embedding/index work,
GPU-hours, storage, network, observability, and engineering operations. A low
invoice is not an optimization if retries, poor answers, or latency violations
move cost elsewhere.

## Why it matters

Token demand and model choice can change faster than fixed infrastructure. A
design needs a denominator such as cost per successful grounded answer or cost
per classified document, not only monthly spend. Attribute usage by product,
tenant, model version, and experiment so an aggregate reduction does not hide a
regression for a protected workload.

## Mental model

```text
traffic -> policy/router -> cache or model -> tokens + latency + quality
             |                 |                    |
          quota/budget       hit/miss             unit-cost ledger
```

Optimize the largest measured term first, then re-measure quality and tail
latency. Savings from routing and caching overlap: a cache hit may avoid model
tokens, while routing changes the cost of misses. Do not multiply headline
percentages without measuring their joint distribution.

## Worked example

Assume 100,000 requests/day, 400 input tokens, 250 output tokens, a 30% exact
cache hit rate, and a provider price of $0.15 per million input tokens and $0.60
per million output tokens. Misses are 70,000 requests, so daily model cost is
`70,000 × (400×0.15 + 250×0.60) / 1,000,000 = $13.65`, before cache storage,
embedding, retries, and observability. Report the assumptions and verify prices
and model versions at decision time.

## Advantages and limitations

| Technique | Benefit | Trade-off |
|---|---|---|
| Exact caching | Near-zero model cost for repeats | Staleness and invalidation; low hit rate for unique prompts |
| Semantic caching | More hits for paraphrases | Similarity mistakes and embedding cost |
| Smaller-model routing | Lower average cost | Classifier errors and quality variance |
| Quantization | Lower GPU memory/cost | Calibration and quality regressions |
| Batching | Better utilization | Queue latency and fairness complexity |

## Topic-specific visual

```mermaid
flowchart LR
  R[Request] --> Q[Quota and attribution]
  Q --> C{Cache hit?}
  C -->|yes| H[Return versioned result]
  C -->|no| S[Complexity router]
  S --> M[Model tier]
  M --> L[Usage ledger: tokens, latency, quality]
  L --> B[Budget and alerting]
```

The ledger receives both cache misses and hits. This makes it possible to
measure cost per useful outcome and prevents a cache from hiding stale-answer or
quality failures.

## Failure modes and operations

Watch cost/request, tokens/request, cache hit rate, retry rate, model mix,
GPU utilization, queue latency, quality slices, and budget burn. Add per-tenant
quotas and an explicit degraded mode. Cache keys must include model/prompt/data
versions and authorization scope; never trade tenant isolation for hit rate.
For price changes or provider outages, retain a versioned fallback policy and
recompute the unit economics rather than silently changing quality.

---

## ⚖️ Cost Optimization Strategies Trade-offs

| Strategy | Cost Reduction | Quality Impact | Implementation Effort | Latency Impact |
|----------|----------------|----------------|----------------------|----------------|
| **Model distillation** | 5-20× | -5 to -20% | High | 5-20× faster |
| **Quantization (INT8)** | 2-4× | <1% loss | Low | 2-4× faster |
| **Quantization (INT4)** | 4-8× | 1-5% loss | Low | 4-8× faster |
| **Prompt caching** | 50-90% | 0% | Low | <1ms cached |
| **Semantic caching** | 20-60% | 0% | Medium | <1ms cached |
| **Smaller model routing** | 3-10× | -10 to -30% | Medium | 3-10× faster |
| **Batching** | 2-4× | 0% | Low | Adds queue latency |
| **Speculative decoding** | 2-3× | 0% | High | 2-3× faster |

### LLM API Cost Reference (2026)

```
Model               Input ($/1M tokens)   Output ($/1M tokens)   Context
─────────────────────────────────────────────────────────────────────────
GPT-4o              $2.50                 $10.00                 128K
GPT-4o-mini         $0.15                 $0.60                  128K
Claude-3-Haiku      $0.25                 $1.25                  200K
Claude-3-Sonnet     $3.00                 $15.00                 200K
Llama-3-70B (self)  ~$0.10                ~$0.10                  8K
Llama-3-8B (self)   ~$0.01               ~$0.01                   8K

Routing strategy: Use small model for 80% of queries, large for 20%
Cost: 0.8 × $0.01 + 0.2 × $0.10 = $0.028 vs. $0.10 (all large) = 3.6× savings
```

---

## 🏗️ Architecture Patterns

### Pattern 1: Model Cascade / Routing

```
Request
  │
  ▼
Complexity Classifier (fast, cheap)
  │
  ├── Simple query (80%)  → Small model (8B)    $0.01/1K tokens
  │
  ├── Medium query (15%)  → Medium model (70B)  $0.10/1K tokens
  │
  └── Complex query (5%)  → Large model (API)   $3.00/1K tokens

Classifier: Keywords, query length, topic, user tier
Fallback: If small model confidence < threshold, escalate to next tier
```

### Pattern 2: Multi-Level Caching

```
Request
  │
  ▼
Exact Cache (Redis, TTL=1h)
  ├── HIT  → Return instantly (<1ms)
  │
  └── MISS
        │
        ▼
Semantic Cache (embedding similarity > 0.95)
  ├── HIT  → Return similar response (<10ms)
  │
  └── MISS
        │
        ▼
Prefix Cache (KV cache for system prompt)
  ├── HIT  → Skip system prompt encoding (~50% savings)
  │
  └── MISS
        │
        ▼
Full LLM Inference
```

### Pattern 3: Quantization Ladder

```
Model Precision    Memory    Speed    Quality
─────────────────────────────────────────────
FP32               100%      1×       Baseline
BF16/FP16          50%       1-2×     ~0% loss
INT8               25%       2-3×     <1% loss
INT4 (GPTQ, AWQ)   12.5%     4-5×     1-5% loss
INT2               6.25%     6-8×     >10% loss (avoid)

Recommendation: INT8 for most use cases, INT4 for memory-constrained
Calibration: Run 128-256 representative samples to find optimal quantization scale
```

---

## 📊 Cost Optimization Implementation

```python
import time
import math
import hashlib
from typing import Optional, Callable, List
from collections import OrderedDict

# ── Exact Response Cache ──────────────────────────────────────────────────────

class ExactCache:
    """LRU cache for exact prompt→response pairs."""

    def __init__(self, max_size: int = 10000, ttl_sec: float = 3600):
        self.max_size = max_size
        self.ttl_sec = ttl_sec
        self._cache: OrderedDict = OrderedDict()
        self._timestamps: dict = {}
        self.hits = 0
        self.misses = 0

    def _key(self, prompt: str, model: str = "default") -> str:
        return hashlib.sha256(f"{model}:{prompt}".encode()).hexdigest()

    def get(self, prompt: str, model: str = "default") -> Optional[str]:
        key = self._key(prompt, model)
        if key in self._cache:
            if time.time() - self._timestamps[key] < self.ttl_sec:
                self._cache.move_to_end(key)  # LRU update
                self.hits += 1
                return self._cache[key]
            else:
                del self._cache[key]
                del self._timestamps[key]
        self.misses += 1
        return None

    def set(self, prompt: str, response: str, model: str = "default"):
        key = self._key(prompt, model)
        if len(self._cache) >= self.max_size:
            oldest = next(iter(self._cache))
            del self._cache[oldest]
            del self._timestamps[oldest]
        self._cache[key] = response
        self._timestamps[key] = time.time()

    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / max(total, 1)

    def estimated_savings(self, cost_per_call: float = 0.01) -> float:
        return self.hits * cost_per_call


# ── Semantic Cache (Embedding Similarity) ──────────────────────────────────────

class SemanticCache:
    """Cache responses by semantic similarity of prompts."""

    def __init__(self, similarity_threshold: float = 0.95, max_size: int = 1000):
        self.threshold = similarity_threshold
        self.max_size = max_size
        self._entries: list = []   # [(embedding, response, prompt)]
        self.hits = 0
        self.misses = 0

    def _embed(self, text: str) -> List[float]:
        """Simulated embedding (real: call embedding API or local model)."""
        # Hash-based pseudo-embedding for demo
        words = text.lower().split()
        vec = [0.0] * 8
        for word in words:
            h = hash(word)
            for i in range(8):
                vec[i] += ((h >> i) & 1) * 2 - 1
        norm = math.sqrt(sum(x**2 for x in vec)) or 1
        return [x / norm for x in vec]

    def _cosine_sim(self, a: List[float], b: List[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x**2 for x in a))
        norm_b = math.sqrt(sum(x**2 for x in b))
        return dot / max(norm_a * norm_b, 1e-9)

    def get(self, prompt: str) -> Optional[str]:
        emb = self._embed(prompt)
        for entry_emb, response, _ in self._entries:
            if self._cosine_sim(emb, entry_emb) >= self.threshold:
                self.hits += 1
                return response
        self.misses += 1
        return None

    def set(self, prompt: str, response: str):
        emb = self._embed(prompt)
        if len(self._entries) >= self.max_size:
            self._entries.pop(0)
        self._entries.append((emb, response, prompt))


# ── Model Router ──────────────────────────────────────────────────────────────

class ModelRouter:
    """Route queries to appropriate model tier based on complexity."""

    MODELS = {
        "small":  {"cost_per_1k": 0.01, "latency_ms": 200,  "quality": 0.7},
        "medium": {"cost_per_1k": 0.10, "latency_ms": 500,  "quality": 0.85},
        "large":  {"cost_per_1k": 3.00, "latency_ms": 2000, "quality": 0.95},
    }

    SMALL_INDICATORS = [
        "what is", "define", "translate", "summarize in one sentence",
        "yes or no", "how many", "when was",
    ]
    LARGE_INDICATORS = [
        "analyze", "compare and contrast", "write a detailed", "explain step by step",
        "debug this", "review this code", "design a system",
    ]

    def route(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        word_count = len(prompt.split())

        if any(ind in prompt_lower for ind in self.SMALL_INDICATORS) and word_count < 30:
            return "small"
        if any(ind in prompt_lower for ind in self.LARGE_INDICATORS) or word_count > 200:
            return "large"
        return "medium"

    def estimate_cost(self, prompt: str, response: str, model: str) -> float:
        tokens = (len(prompt.split()) + len(response.split())) * 1.3  # rough token estimate
        return tokens / 1000 * self.MODELS[model]["cost_per_1k"]


# Demo
print("=== Caching Demo ===")
cache = ExactCache(max_size=100, ttl_sec=3600)
prompts = ["What is Python?", "What is Python?", "Tell me about AI", "What is Python?"]

for prompt in prompts:
    result = cache.get(prompt)
    if result is None:
        # Simulate LLM call
        result = f"Response to: {prompt}"
        cache.set(prompt, result)
        print(f"  MISS → Generated response for: '{prompt[:30]}'")
    else:
        print(f"  HIT  → Cached response for: '{prompt[:30]}'")

print(f"Hit rate: {cache.hit_rate():.1%}, Saved ~${cache.estimated_savings():.2f}")

print("\n=== Model Routing ===")
router = ModelRouter()
test_prompts = [
    "What is machine learning?",
    "Analyze the trade-offs between BERT and GPT architectures in detail",
    "Translate 'hello' to French",
]
for p in test_prompts:
    tier = router.route(p)
    model_info = router.MODELS[tier]
    print(f"  [{tier:6}] {p[:50]}")
    print(f"          Cost: ${model_info['cost_per_1k']}/1K, Latency: {model_info['latency_ms']}ms")
```

---

## ❓ Interview Q&A

**Q1: How would you reduce inference costs by 10× without significant quality loss?**

A: Layered approach achieving 10-30× total:
1. **Caching (2-5× reduction)**: Exact cache for repeated queries (FAQ, system prompts); semantic cache for near-duplicate prompts. Typical hit rate: 30-70% for production traffic
2. **Quantization (2-4× reduction)**: INT8 inference via TensorRT or llama.cpp; <1% quality loss on most tasks
3. **Model routing (3-10× reduction)**: Small model for 80% simple queries, large model only for complex. Classify query complexity with a 3-class classifier (100M params, <1ms)
4. **Batching (1.5-3× reduction)**: Group requests into batches of 8-32; amortize KV cache overhead; trade queue latency for throughput

Combined: 2× (cache) × 2× (quantization) × 2× (routing) × 1.5× (batching) = ~12× savings

**Q2: What are the trade-offs of using a smaller model vs. a larger API model?**

A:
- **Smaller self-hosted model**: Lower cost at scale (>1M QPS), private (no data sent to third party), controllable latency, but needs GPU infrastructure, ops burden, may need domain fine-tuning
- **Larger API model**: Higher quality out-of-box, zero ops, latest capabilities, but higher cost, vendor dependency, data privacy concerns, variable latency

Decision framework: < 100K QPM → API (ops cost dominates); > 1M QPM → self-hosted (compute cost dominates); PII data → self-hosted (compliance); experimental → API (no infra investment)

**Q3: How does speculative decoding reduce latency without changing model quality?**

A: Standard decoding: large model generates 1 token/step (serial, slow). Speculative decoding: small draft model generates K tokens in parallel; large target model verifies all K in one pass.

If all K tokens accepted: K tokens for the price of 1 verification pass (~3-4× speedup). If token i rejected: discard tokens i+1..K, re-sample token i from target. No quality loss (mathematically equivalent to pure target model output). Requires: draft model ~10× smaller than target.

**Q4: Design a cost monitoring system for LLM API usage.**

A: Track per-request and aggregate metrics:
1. **Per-request**: prompt_tokens, completion_tokens, model_id, user_id, latency_ms
2. **Aggregated (hourly)**: cost_by_model, cost_by_user, tokens_by_endpoint, cache_hit_rate
3. **Alerts**: Daily budget threshold, sudden cost spike (3σ above baseline), per-user quota exceeded
4. **Attribution**: Tag requests with feature_name, experiment_id for cost-by-feature breakdown

Implementation: Wrap LLM calls in middleware → emit events to Kafka → Flink aggregation → store in TimescaleDB → Grafana dashboard

---

## 🧪 Practical Exercises

### Exercise 1: Cost Calculator (Easy)

```python
def estimate_monthly_cost(
    queries_per_day: int,
    avg_input_tokens: int,
    avg_output_tokens: int,
    model: str = "gpt-4o-mini",
    cache_hit_rate: float = 0.3,
) -> dict:
    pricing = {
        "gpt-4o":      {"input": 2.50,  "output": 10.00},
        "gpt-4o-mini": {"input": 0.15,  "output": 0.60},
        "claude-haiku":{"input": 0.25,  "output": 1.25},
    }
    p = pricing.get(model, pricing["gpt-4o-mini"])
    
    effective_queries = queries_per_day * (1 - cache_hit_rate)
    daily_cost = (
        effective_queries * avg_input_tokens / 1e6 * p["input"] +
        effective_queries * avg_output_tokens / 1e6 * p["output"]
    )
    monthly_cost = daily_cost * 30
    cache_savings = daily_cost * 30 * cache_hit_rate / (1 - cache_hit_rate + 1e-9)
    
    return {
        "daily_cost": f"${daily_cost:.2f}",
        "monthly_cost": f"${monthly_cost:.2f}",
        "monthly_with_cache": f"${monthly_cost:.2f} (after {cache_hit_rate:.0%} cache)",
        "cache_savings": f"${cache_savings:.2f}/month",
        "model": model,
    }


configs = [
    (10000, 200, 500, "gpt-4o", 0.3),
    (10000, 200, 500, "gpt-4o-mini", 0.3),
    (100000, 150, 300, "claude-haiku", 0.5),
]
for qpd, inp, out, model, hit_rate in configs:
    result = estimate_monthly_cost(qpd, inp, out, model, hit_rate)
    print(f"{model}: {result['monthly_cost']}/month (savings: {result['cache_savings']})")
