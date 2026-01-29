# Routing Experiment: Centralized vs Distributed

This experiment compares two routing approaches using Google ADK for multi-agent systems with 40 domains.

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

## Latest Experiment Results (20 queries, 2 runs)

| Metric | Centralized (Idea 1) | Distributed (Idea 2) | Winner |
|--------|---------------------|---------------------|--------|
| **Accuracy** | 97.5% (avg: 95-100%) | 95.0% (consistent) | Centralized |
| **Avg Latency** | 2.60s | 3.54s | Centralized |
| **Avg Hops** | 2.0 | 2.9 | Centralized |

**Centralized wins:** 27% faster latency with better accuracy.

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
# Quick comparison (default 10 queries, 1 run)
python3 experiment.py

# Custom queries and multiple runs for statistics
python3 experiment.py --queries 20 --runs 3

# Run only centralized
python3 experiment.py --mode centralized --queries 20

# Run only distributed
python3 experiment.py --mode distributed --queries 20

# Save results to custom CSV file
python3 experiment.py --queries 20 --runs 3 --output my_results.csv
```

### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--mode` | `quick`, `compare`, `centralized`, `distributed` | `quick` |
| `--queries` | Number of test queries to run | `10` |
| `--runs` | Number of times to run (for statistics) | `1` |
| `--output` | Custom CSV output path | `experiment_results_TIMESTAMP.csv` |

## Project Structure

```
global-routing/
├── domains.py       # 40 domain configurations with keywords, examples, sub-agents
├── experiment.py     # Main experiment script with both routing implementations
├── .env              # API configuration (not in git)
├── .gitignore        # Excludes .env, *.log, *.csv
└── README.md         # This file
```

**Generated files:**
- `experiment_TIMESTAMP.log` - Timestamped log for each run
- `experiment_results_TIMESTAMP.csv` - CSV results export

## Output Files

### CSV Results
Each experiment run generates a CSV file containing:
- Run summary with accuracy, latency, and hops per run
- Statistics (avg/min/max) across all runs
- Complete list of test queries

### Log Files
Each experiment creates a timestamped log file with:
- Per-query execution logs
- Routing results (which agent, hops, latency)
- Run completion metrics

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
| Most applications | **Centralized** (simple, fast, accurate) |
| Need sub-agent granularity | **Distributed** (`it_support_network` vs `it_support`) |
| Multiple teams own domains | **Distributed** (each team maintains their routing) |
| Ambiguous domain boundaries | **Centralized** (routing hints resolve confusion) |
| Best performance | **Centralized** (fewer hops, lower latency) |
