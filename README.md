# Routing Experiment: Centralized vs Distributed

This experiment compares two routing approaches using Google ADK.

## The Two Approaches

### Idea 1: Centralized Routing
```
Root Coordinator → 40 Domain Agents
```
- One root agent routes directly to 40 domain agents
- All routing logic in one place
- Simpler architecture, faster routing

### Idea 2: Distributed Routing (No Categories)
```
Root Coordinator → 40 Domain Agents → Sub-Agents
```
- Root agent routes directly to 40 domain agents
- Each domain agent routes to its own specialized sub-agents
- More granular routing (e.g., `it_support_network`, `finance_banking`)
- Routing logic distributed across domains

**Note**: We initially tested with 5 category agents, but removed them because they created ambiguity and reduced accuracy from 95% → 65%.

## Experiment Results (20 queries)

| Metric | Centralized (Idea 1) | Distributed (Idea 2) | Winner |
|--------|---------------------|---------------------|--------|
| **Accuracy** | 100% (20/20) | 95% (19/20) | Centralized |
| **Avg Latency** | 1.94s | 2.20s | Centralized |
| **Avg Hops** | 2.0 | 2.9 | Centralized |

### Key Findings

1. **Prompt engineering matters more than architecture**
   - Adding example queries and routing hints improved centralized from 85% → 100%
   - Removing categories improved distributed from 65% → 95%

2. **Forced delegation prevents "no route" errors**
   - "MUST ALWAYS delegate" instruction prevents coordinator from answering directly

3. **Routing hints resolve ambiguous cases**
   - Explicit rules: "training" → hr, "expense" → finance

## Setup

1. Install dependencies:
```bash
pip3 install google-adk python-dotenv --break-system-packages
```

2. Set up your Google API key in `.env`:
```bash
GOOGLE_GENAI_USE_VERTEXAI=false
GOOGLE_API_KEY=your-api-key-here
```

Get your API key from: https://aistudio.google.com/app/apikey

## Running the Experiment

```bash
# Quick comparison (default 20 queries)
python3 experiment.py --mode quick

# Custom number of queries
python3 experiment.py --mode compare --queries 30

# Run only centralized
python3 experiment.py --mode centralized --queries 20

# Run only distributed
python3 experiment.py --mode distributed --queries 20
```

## Project Structure

```
global-routing/
├── domains.py                # 40 domain configurations with sub-agents
├── centralized_routing.py    # Idea 1: Centralized routing
├── distributed_routing.py    # Idea 2: Distributed routing (no categories)
├── improved_centralized.py  # Enhanced centralized version
├── experiment.py             # Main comparison script
├── analyze_errors.py         # Error analysis helper
├── .env                      # API configuration
└── README.md                 # This file
```

## How Correctness is Determined

1. **Test queries** have expected domains:
   ```python
   ("Reset my password", "it_support"),
   ("Check my bank balance", "finance"),
   ```

2. **System routes** the query to an agent

3. **Correctness check** compares routed agent vs expected:
   ```python
   def is_correct_routing(routed_to: str, expected_domain: str):
       return expected_domain in routed_to
   ```

## When to Use Each Approach

| Use Case | Recommended |
|----------|-------------|
| Most applications | **Centralized** (simple, fast, 100% accurate) |
| Need sub-agent granularity | **Distributed** (`it_support_network` vs `it_support`) |
| Multiple teams own domains | **Distributed** (each team maintains their routing) |
| Ambiguous domain boundaries | **Centralized** (routing hints resolve confusion) |
