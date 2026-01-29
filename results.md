# Routing Experiment Results

**Generated:** 2026-01-29 09:03:09
**Total Queries:** 20
**Total Runs:** 2

---

## The Three Approaches

| Approach | Architecture | Description |
|----------|--------------|-------------|
| **Idea 1: Centralized** | Root → 40 Domain Agents | Simple, fast routing |
| **Idea 2: Distributed** | Root → 40 Domains → Sub-Agents | Granular routing |
| **Idea 3: Direct** | Root → 148 Sub-Agents | Direct access, no domain layer |

---

## Run Summary

| Run | Cent Acc | Cent Lat (s) | Cent Hop | Dist Acc | Dist Lat (s) | Dist Hop | Direct Acc | Direct Lat (s) | Direct Hop |
|-----|----------|--------------|----------|----------|--------------|----------|------------|----------------|------------|
| 1   | 95%      | 2.77         | 2.0      | 95%      | 3.87         | 2.9      | 90%        | 5.10           | 2.1        |
| 2   | 95%      | 3.09         | 2.0      | 95%      | 4.15         | 3.0      | 95%        | 4.24           | 2.1        |

---

## Statistics

| Metric       | Cent Avg | Cent Min | Cent Max | Dist Avg | Dist Min | Dist Max | Direct Avg | Direct Min | Direct Max |
|--------------|----------|----------|----------|----------|----------|----------|------------|------------|------------|
| Accuracy (%) | 95.0     | 95.0     | 95.0     | 95.0     | 95.0     | 95.0     | 92.5       | 90.0       | 95.0       |
| Latency (s)  | 2.93     | 2.77     | 3.09     | 4.01     | 3.87     | 4.15     | 4.67       | 4.24       | 5.10       |
| Hops         | 2.0      | 2.0      | 2.0      | 2.9      | 2.9      | 3.0      | 2.1        | 2.1        | 2.1        |

---

## Overall Winner

| Metric | Winner | Details |
|--------|--------|---------|
| **Accuracy** | Centralized / Distributed | 95.0% vs 92.5% (Direct) |
| **Latency** | **Centralized** | 2.93s (37% faster than Direct) |
| **Hops** | **Centralized** | 2.0 hops (simplest path) |

---

## Key Findings

1. **Centralized routing (Idea 1) wins overall**
   - Best latency with 95% accuracy
   - Consistent 2.0 hop path
   - 37% faster than Direct routing

2. **Direct routing (Idea 3) underperformed**
   - Lowest accuracy (92.5% avg, dropped to 90% in run 1)
   - Slowest latency (4.67s avg)
   - 148 routing options may overwhelm the LLM

3. **Distributed routing (Idea 2) - Middle ground**
   - Same accuracy as Centralized (95%)
   - Higher latency due to extra hop (2.9 vs 2.0)

4. **The "Sweet Spot" is ~40 routing options**
   - Centralized (40 agents) performs best
   - Direct (148 agents) shows diminishing returns
   - More choices = more cognitive load = slower/less accurate

---

## Test Queries

| # | Query | Expected Domain |
|---|-------|-----------------|
| 1  | I need to book a flight to Tokyo | travel |
| 2  | Find me a hotel in Paris | travel |
| 3  | Rent a car for next week | travel |
| 4  | Plan a vacation to Hawaii | travel |
| 5  | Check my bank balance | finance |
| 6  | I want to invest in stocks | finance |
| 7  | Report an expense | finance |
| 8  | Show my financial report | finance |
| 9  | Request time off for next week | hr |
| 10 | Check my benefits | hr |
| 11 | When do I get paid? | hr |
| 12 | Enroll in training program | hr |
| 13 | Reset my password | it_support |
| 14 | My VPN is not working | it_support |
| 15 | Install new software | it_support |
| 16 | Connect to WiFi | it_support |
| 17 | Where is my order? | customer_service |
| 18 | I want to return this item | customer_service |
| 19 | File a complaint | customer_service |
| 20 | Product information | customer_service |

---

## Recommendation

**Use Centralized Routing (Idea 1)** for this multi-agent system:

- Best accuracy (95%)
- Fastest latency (2.93s avg)
- Simplest architecture (2 hops)
- Consistent performance across runs

The experiment shows that more routing options (148 agents in Direct) doesn't improve performance - it actually degrades it. The optimal design balances granularity with cognitive load on the routing LLM.
