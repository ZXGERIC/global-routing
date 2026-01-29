#!/usr/bin/env python3
"""
Routing Experiment: Centralized vs Distributed vs Direct

Compares three routing approaches:
- Idea 1: Centralized routing (Root → 40 Domain Agents)
- Idea 2: Distributed routing (Root → 40 Domains → Sub-Agents)
- Idea 3: Direct routing (Root → 148 Sub-Agents, no domain layer)
"""

import argparse
import asyncio
import csv
import logging
import os
import statistics
import time
from datetime import datetime
from typing import Dict, List

# Set up logging (log file will be created with timestamp later)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)


def setup_timestamped_logging():
    """Create a timestamped log file for this experiment run."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"experiment_{timestamp}.log"
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(file_handler)
    return log_filename

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configure environment before importing ADK
os.environ.setdefault('GOOGLE_GENAI_USE_VERTEXAI', 'false')
# ADK looks for GOOGLE_API_KEY, but user might have GOOGLE_GENAI_API_KEY
if not os.environ.get('GOOGLE_API_KEY') and os.environ.get('GOOGLE_GENAI_API_KEY'):
    os.environ['GOOGLE_API_KEY'] = os.environ['GOOGLE_GENAI_API_KEY']

from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.adk.events.event import Event
from google.genai import types as genai_types
from domains import DOMAINS, SUB_AGENTS

MODEL = "gemini-2.5-flash"

# Test queries covering different domains
TEST_QUERIES = [
    # Travel
    ("I need to book a flight to Tokyo", "travel"),
    ("Find me a hotel in Paris", "travel"),
    ("Rent a car for next week", "travel"),
    ("Plan a vacation to Hawaii", "travel"),

    # Finance
    ("Check my bank balance", "finance"),
    ("I want to invest in stocks", "finance"),
    ("Report an expense", "finance"),
    ("Show my financial report", "finance"),

    # HR
    ("Request time off for next week", "hr"),
    ("Check my benefits", "hr"),
    ("When do I get paid?", "hr"),
    ("Enroll in training program", "hr"),

    # IT Support
    ("Reset my password", "it_support"),
    ("My VPN is not working", "it_support"),
    ("Install new software", "it_support"),
    ("Connect to WiFi", "it_support"),

    # Customer Service
    ("Where is my order?", "customer_service"),
    ("I want to return this item", "customer_service"),
    ("File a complaint", "customer_service"),
    ("Product information", "customer_service"),

    # Sales
    ("I want to buy your product", "sales"),
    ("What's the price?", "sales"),
    ("Request a quote", "sales"),
    ("Schedule a demo", "sales"),

    # Marketing
    ("Create a marketing campaign", "marketing"),
    ("Post on social media", "marketing"),
    ("Show marketing analytics", "marketing"),
    ("Review brand guidelines", "marketing"),

    # Legal
    ("Review this contract", "legal"),
    ("Compliance question", "legal"),
    ("IP registration", "legal"),
    ("Legal advice needed", "legal"),

    # Engineering
    ("Review my code", "engineering"),
    ("Deploy to production", "engineering"),
    ("Fix this bug", "engineering"),
    ("API documentation", "engineering"),

    # Operations
    ("Check inventory levels", "operations"),
    ("Track shipment", "operations"),
    ("Vendor management", "operations"),
    ("Optimize processes", "operations"),

    # More domains for comprehensive testing
    ("Project status update", "project_management"),
    ("Design a new feature", "design"),
    ("Send company announcement", "communications"),
    ("Book a meeting room", "facilities"),
    ("Generate sales report", "data_analytics"),
    ("Report security incident", "security"),
    ("Enroll in training", "learning_development"),
    ("Carbon footprint report", "sustainability"),
    ("Quality testing request", "quality_assurance"),
    ("Risk assessment", "risk_management"),
    ("Pay my bill", "billing"),
    ("Plan an event", "events"),
    ("Write a blog post", "content"),
    ("Market research", "research"),
    ("Tax planning", "tax"),
    ("Investor information", "investor_relations"),
    ("M&A opportunity", "corporate_development"),
    ("Employee engagement", "workplace"),
    ("Revenue forecast", "revenue_operations"),
]


def create_centralized_system():
    """Create centralized routing: 1 root -> 40 domain agents."""
    domain_agents = []
    domain_list = []

    for domain in DOMAINS:
        # Enhanced description with examples
        examples = domain.get("sample_queries", [])[:3]
        examples_str = "".join([f'\n      - "{q}"' for q in examples])

        full_description = f"""{domain['description']}

Keywords: {', '.join(domain['keywords'])}{examples_str}"""

        agent = LlmAgent(
            name=f"{domain['name']}_agent",
            model=MODEL,
            instruction=f"""You are the {domain['name'].title()} agent.

{full_description}

Acknowledge you are handling this request as the {domain['name']} agent.
Start your response with: [ROUTED_TO: {domain['name']}_agent]""",
            description=full_description,
        )
        domain_agents.append(agent)
        domain_list.append(f"- **{domain['name']}**: {domain['description'][:80]}...")

    # Improved routing instruction
    routing_instruction = f"""You are the central routing coordinator. Your ONLY job is to route queries to domain agents.

**CRITICAL RULES:**
1. You MUST ALWAYS delegate to a domain agent - never answer queries yourself
2. Read ALL available agents before deciding
3. When in doubt, choose the closest match

**Available Domain Agents (40 total):**
{chr(10).join(domain_list)}

**ROUTING HINTS FOR AMBIGUOUS CASES:**
- "expense", "payment", "spending", "report cost" → finance_agent
- "when do I get paid", "paycheck", "salary inquiry" → hr_agent
- "training", "enroll in course", "enroll in program" → hr_agent
- "travel", "flight", "hotel", "vacation", "trip" → travel_agent
- "order", "return", "refund", "delivery" → customer_service_agent

Now route the query and DELEGATE immediately."""

    root_coordinator = LlmAgent(
        name="central_coordinator",
        model=MODEL,
        instruction=routing_instruction,
        sub_agents=domain_agents,
    )

    return root_coordinator, domain_agents


def create_distributed_system():
    """Create distributed routing: root -> 40 domains -> sub-agents (no categories)."""
    # Create domain agents
    domain_agent_map = {}
    domain_descriptions = []

    for domain in DOMAINS:
        sub_agents = []
        for sub_name in domain.get("sub_agents", []):
            sub_desc = SUB_AGENTS.get(sub_name, f"Handles {sub_name}")
            sub_agent = LlmAgent(
                name=f"{domain['name']}_{sub_name}",
                model=MODEL,
                instruction=f"""You are the {sub_name} sub-agent.
Description: {sub_desc}
Start your response with: [ROUTED_TO: {domain['name']}_{sub_name}]""",
                description=f"{sub_name}: {sub_desc}",
            )
            sub_agents.append(sub_agent)

        if sub_agents:
            sub_list = ", ".join(domain['sub_agents'])
            routing_instruction = f"""You are the {domain['name']} domain agent.
Description: {domain['description']}
Your keywords: {', '.join(domain['keywords'])}
Your sub-agents: {sub_list}

Route to the most appropriate sub-agent and delegate immediately.
After routing, indicate with: [ROUTED_TO: {domain['name']}]"""
        else:
            routing_instruction = f"""You are the {domain['name']} domain agent.
Description: {domain['description']}
Your keywords: {', '.join(domain['keywords'])}
Handle this request directly.
Start your response with: [ROUTED_TO: {domain['name']}]"""

        domain_agent = LlmAgent(
            name=f"{domain['name']}_domain",
            model=MODEL,
            instruction=routing_instruction,
            sub_agents=sub_agents,
        )
        domain_agent_map[domain['name']] = domain_agent
        domain_descriptions.append(f"- {domain['name']}: {domain['description']}")

    # Root coordinator routes directly to domain agents
    root_instruction = f"""You are the root coordinator for distributed routing.

Route user queries to the appropriate domain agent.

Available domain agents (40 total):
{chr(10).join(domain_descriptions)}

IMPORTANT: Analyze the query and route to the MOST appropriate domain agent.
Be decisive - pick ONE domain and delegate immediately."""

    root_coordinator = LlmAgent(
        name="distributed_coordinator",
        model=MODEL,
        instruction=root_instruction,
        sub_agents=list(domain_agent_map.values()),
    )

    return root_coordinator, {'domain_agents': domain_agent_map}


def create_direct_system():
    """Create direct routing (Idea 3): Root -> All 148 sub-agents directly (no domain agents)."""
    # Create all sub-agents directly under root
    sub_agents_list = []
    sub_agent_descriptions = []

    for domain in DOMAINS:
        domain_name = domain['name']

        # For domains without sub-agents, create a domain agent as a "sub-agent"
        sub_names = domain.get("sub_agents", [])

        if not sub_names:
            # Domain without sub-agents - create domain-level agent
            full_description = f"""{domain['description']}

Keywords: {', '.join(domain['keywords'])}"""

            agent = LlmAgent(
                name=f"{domain_name}",
                model=MODEL,
                instruction=f"""You are the {domain_name.title()} agent.

{full_description}

Acknowledge you are handling this request as the {domain_name} agent.
Start your response with: [ROUTED_TO: {domain_name}]""",
                description=full_description,
            )
            sub_agents_list.append(agent)
            sub_agent_descriptions.append(f"- **{domain_name}**: {domain['description']}")

        else:
            # Create individual sub-agents
            for sub_name in sub_names:
                sub_desc = SUB_AGENTS.get(sub_name, f"Handles {sub_name}")

                # Include domain context in sub-agent description
                full_description = f"""{sub_desc}

Parent domain: {domain_name}
Domain keywords: {', '.join(domain['keywords'])}"""

                agent = LlmAgent(
                    name=f"{domain_name}_{sub_name}",
                    model=MODEL,
                    instruction=f"""You are the {sub_name} agent.

{full_description}

Acknowledge you are handling this request.
Start your response with: [ROUTED_TO: {domain_name}_{sub_name}]""",
                    description=full_description,
                )
                sub_agents_list.append(agent)
                sub_agent_descriptions.append(f"- **{domain_name}_{sub_name}**: {sub_desc}")

    # Root coordinator routes directly to all sub-agents
    total_agents = len(sub_agents_list)
    routing_instruction = f"""You are the direct routing coordinator. Your ONLY job is to route queries to specialized agents.

**CRITICAL RULES:**
1. You MUST ALWAYS delegate to a specialized agent - never answer queries yourself
2. Read ALL available agents before deciding
3. When in doubt, choose the closest match

**Available Specialized Agents ({total_agents} total):**
{chr(10).join(sub_agent_descriptions)}

**ROUTING HINTS FOR AMBIGUOUS CASES:**
- "expense", "payment", "spending", "report cost" → finance_expenses
- "when do I get paid", "paycheck", "salary inquiry" → hr_payroll
- "training", "enroll in course", "enroll in program" → hr (learning_development also acceptable)
- "travel", "flight", "hotel", "vacation", "trip" → travel_* (specific sub-agent)
- "order", "return", "refund", "delivery" → customer_service_* (specific sub-agent)

Now route the query and DELEGATE immediately."""

    root_coordinator = LlmAgent(
        name="direct_coordinator",
        model=MODEL,
        instruction=routing_instruction,
        sub_agents=sub_agents_list,
    )

    return root_coordinator, {'sub_agents': sub_agents_list}


async def run_query_async(agent, query: str, mode: str, run_num: int = 1) -> Dict:
    """Run a query and return metrics using ADK's InMemoryRunner."""
    logging.info(f"Run {run_num} - {mode}: Executing query: '{query[:50]}...'")
    runner = InMemoryRunner(agent=agent, app_name=f"routing_experiment_{mode}")

    start_time = time.time()
    events = await runner.run_debug(
        query,
        user_id="test_user",
        session_id=f"test_session_{mode}",
        quiet=True
    )
    latency = time.time() - start_time
    logging.info(f"Run {run_num} - {mode}: Query completed in {latency:.2f}s")

    # Extract response and routing info
    response_text = ""
    routing_path = []

    for event in events:
        # Get content from events
        if hasattr(event, 'content') and event.content and hasattr(event.content, 'parts') and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, 'text') and part.text:
                    response_text += part.text + "\n"

        # Check agent author to track routing path
        if hasattr(event, 'author') and event.author not in ['user', 'test_user']:
            routing_path.append(event.author)

    # Extract routing markers from response
    import re
    routed_to = "unknown"
    pattern = r'\[ROUTED_TO:\s*([^\]]+)\]|\[HANDLED_BY:\s*([^\]]+)\]'
    matches = re.findall(pattern, response_text)
    for match in matches:
        routed = match[0] if match[0] else match[1]
        if routed:
            routed_to = routed.strip()

    # If no marker found, use the last agent in the path (excluding coordinator)
    if routed_to == "unknown" and routing_path:
        # Filter out coordinators and get the last domain agent
        domain_agents = [a for a in routing_path if "coordinator" not in a.lower() and "category" not in a.lower()]
        if domain_agents:
            routed_to = domain_agents[-1]
        elif routing_path:
            routed_to = routing_path[-1]

    logging.info(f"Run {run_num} - {mode}: Routed to '{routed_to}', hops: {len(set(routing_path))}")

    return {
        "query": query,
        "response": response_text[:500],  # Truncate for display
        "routed_to": routed_to,
        "routing_path": routing_path,
        "hop_count": len(set(routing_path)),  # Unique agents in path
        "latency": latency,
        "mode": mode
    }


def is_correct_routing(routed_to: str, expected_domain: str) -> bool:
    """Check if routing was correct."""
    # Extract domain name from agent name
    if f"{expected_domain}_" in routed_to or routed_to.startswith(expected_domain):
        return True
    return False


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_results(results: List[Dict], mode: str, verbose: bool = True):
    """Print query results."""
    if not verbose:
        return

    print(f"\n{mode.upper()} RESULTS:")
    print("-" * 70)

    correct = 0
    total_lat = 0

    for r in results:
        expected = r.get('expected', 'unknown')
        is_correct = is_correct_routing(r['routed_to'], expected)
        if is_correct:
            correct += 1

        status = "✓" if is_correct else "✗"
        print(f"{status} Query: {r['query'][:50]}...")
        print(f"  → Routed to: {r['routed_to']}")
        print(f"  → Hops: {r['hop_count']}")
        print(f"  → Latency: {r['latency']:.2f}s")
        print(f"  → Expected: {expected}")
        print()
        total_lat += r['latency']

    accuracy = (correct / len(results)) * 100
    avg_lat = total_lat / len(results)

    print("-" * 70)
    print(f"Accuracy: {accuracy:.1f}% ({correct}/{len(results)} correct)")
    print(f"Average Latency: {avg_lat:.2f}s")
    print(f"Average Hops: {sum(r['hop_count'] for r in results) / len(results):.1f}")


def calculate_run_metrics(results: List[Dict], mode: str = "", run_num: int = 1) -> Dict:
    """Calculate metrics for a single run."""
    correct = sum(1 for r in results if is_correct_routing(r['routed_to'], r['expected']))
    total = len(results)
    accuracy = (correct / total * 100) if total > 0 else 0
    avg_latency = sum(r['latency'] for r in results) / total if total > 0 else 0
    avg_hops = sum(r['hop_count'] for r in results) / total if total > 0 else 0

    logging.info(f"Run {run_num} - {mode}: Metrics - Accuracy: {accuracy:.1f}% ({correct}/{total}), "
                 f"Avg Latency: {avg_latency:.2f}s, Avg Hops: {avg_hops:.1f}")

    return {
        "accuracy": accuracy,
        "avg_latency": avg_latency,
        "avg_hops": avg_hops,
        "correct": correct,
        "total": total
    }


def print_multi_run_table(centralized_runs: List[Dict], distributed_runs: List[Dict], direct_runs: List[Dict] = None):
    """Print a table comparing all runs with statistics."""
    print("\n" + "=" * 130)
    print("  MULTI-RUN COMPARISON TABLE")
    print("=" * 130)

    # Header
    if direct_runs:
        header = f"{'Run':<6} {'Cent Acc':<12} {'Cent Lat':<10} {'Cent Hop':<10} {'Dist Acc':<12} {'Dist Lat':<10} {'Dist Hop':<10} {'Direct Acc':<12} {'Direct Lat':<10} {'Direct Hop':<10}"
        print(header)
        print("-" * 130)
    else:
        header = f"{'Run':<6} {'Cent Accuracy':<15} {'Cent Latency':<15} {'Cent Hops':<12} {'Dist Accuracy':<15} {'Dist Latency':<15} {'Dist Hops':<12}"
        print(header)
        print("-" * 100)

    # Data rows
    for i in range(len(centralized_runs)):
        c = centralized_runs[i]
        d = distributed_runs[i]
        if direct_runs and i < len(direct_runs):
            dr = direct_runs[i]
            row = (f"{i+1:<6} "
                   f"{c['accuracy']:.0f}%{' ':<6} "
                   f"{c['avg_latency']:.2f}s{' ':<4} "
                   f"{c['avg_hops']:.1f}{' ':<6} "
                   f"{d['accuracy']:.0f}%{' ':<6} "
                   f"{d['avg_latency']:.2f}s{' ':<4} "
                   f"{d['avg_hops']:.1f}{' ':<6} "
                   f"{dr['accuracy']:.0f}%{' ':<6} "
                   f"{dr['avg_latency']:.2f}s{' ':<4} "
                   f"{dr['avg_hops']:.1f}")
            print(row)
        else:
            row = (f"{i+1:<6} "
                   f"{c['accuracy']:.1f}% ({c['correct']}/{c['total']}){' ':<4} "
                   f"{c['avg_latency']:.2f}s{' ':<8} "
                   f"{c['avg_hops']:.1f}{' ':<7} "
                   f"{d['accuracy']:.1f}% ({d['correct']}/{d['total']}){' ':<4} "
                   f"{d['avg_latency']:.2f}s{' ':<8} "
                   f"{d['avg_hops']:.1f}")
            print(row)

    if direct_runs:
        print("-" * 130)
    else:
        print("-" * 100)

    # Statistics rows
    cen_accs = [r['accuracy'] for r in centralized_runs]
    cen_lats = [r['avg_latency'] for r in centralized_runs]
    cen_hops = [r['avg_hops'] for r in centralized_runs]

    dist_accs = [r['accuracy'] for r in distributed_runs]
    dist_lats = [r['avg_latency'] for r in distributed_runs]
    dist_hops = [r['avg_hops'] for r in distributed_runs]

    def format_stats(values):
        if not values:
            return "N/A"
        return f"avg:{statistics.mean(values):.1f} min:{min(values):.1f} max:{max(values):.1f}"

    def format_lat_stats(values):
        if not values:
            return "N/A"
        return f"avg:{statistics.mean(values):.2f} min:{min(values):.2f} max:{max(values):.2f}"

    if direct_runs:
        dir_accs = [r['accuracy'] for r in direct_runs]
        dir_lats = [r['avg_latency'] for r in direct_runs]
        dir_hops = [r['avg_hops'] for r in direct_runs]

        print(f"\n{'STATISTICS':<8} {'Centralized':<30} {'Distributed':<30} {'Direct':<30}")
        print("-" * 130)

        print(f"{'Accuracy':<8} {format_stats(cen_accs):<30} {format_stats(dist_accs):<30} {format_stats(dir_accs):<30}")
        print(f"{'Latency':<8} {format_lat_stats(cen_lats):<30} {format_lat_stats(dist_lats):<30} {format_lat_stats(dir_lats):<30}")
        print(f"{'Hops':<8} {format_stats(cen_hops):<30} {format_stats(dist_hops):<30} {format_stats(dir_hops):<30}")

        # Overall winner
        print("-" * 130)
        avg_cen_acc = statistics.mean(cen_accs)
        avg_dist_acc = statistics.mean(dist_accs)
        avg_dir_acc = statistics.mean(dir_accs)
        avg_cen_lat = statistics.mean(cen_lats)
        avg_dist_lat = statistics.mean(dist_lats)
        avg_dir_lat = statistics.mean(dir_lats)

        best_acc = max(avg_cen_acc, avg_dist_acc, avg_dir_acc)
        acc_winner = "Centralized" if best_acc == avg_cen_acc else ("Direct" if best_acc == avg_dir_acc else "Distributed")

        best_lat = min(avg_cen_lat, avg_dist_lat, avg_dir_lat)
        lat_winner = "Centralized" if best_lat == avg_cen_lat else ("Direct" if best_lat == avg_dir_lat else "Distributed")

        print(f"\nOVERALL WINNER (averaged over {len(centralized_runs)} runs):")
        print(f"  Accuracy: {acc_winner} ({avg_cen_acc:.1f}% vs {avg_dist_acc:.1f}% vs {avg_dir_acc:.1f}%)")
        print(f"  Latency: {lat_winner} ({avg_cen_lat:.2f}s vs {avg_dist_lat:.2f}s vs {avg_dir_lat:.2f}s)")
        print("=" * 130 + "\n")
    else:
        print(f"\n{'STATISTICS':<6} {'Centralized':<42} {'Distributed':<42}")
        print("-" * 100)

        print(f"{'Accuracy':<6} {format_stats(cen_accs):<42} {format_stats(dist_accs):<42}")
        print(f"{'Latency':<6} {format_lat_stats(cen_lats):<42} {format_lat_stats(dist_lats):<42}")
        print(f"{'Hops':<6} {format_stats(cen_hops):<42} {format_stats(dist_hops):<42}")

        # Overall winner
        print("-" * 100)
        avg_cen_acc = statistics.mean(cen_accs)
        avg_dist_acc = statistics.mean(dist_accs)
        avg_cen_lat = statistics.mean(cen_lats)
        avg_dist_lat = statistics.mean(dist_lats)

        acc_winner = "Centralized" if avg_cen_acc > avg_dist_acc else ("Distributed" if avg_dist_acc > avg_cen_acc else "Tie")
        lat_winner = "Centralized" if avg_cen_lat < avg_dist_lat else "Distributed"

        print(f"\nOVERALL WINNER (averaged over {len(centralized_runs)} runs):")
        print(f"  Accuracy: {acc_winner} ({avg_cen_acc:.1f}% vs {avg_dist_acc:.1f}%)")
        print(f"  Latency: {lat_winner} ({avg_cen_lat:.2f}s vs {avg_dist_lat:.2f}s)")
        print("=" * 100 + "\n")


def save_results_to_csv(
    centralized_runs: List[Dict],
    distributed_runs: List[Dict],
    direct_runs: List[Dict] = None,
    queries: List[tuple] = None,
    output_path: str = None
):
    """Save experiment results to a CSV file."""
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"experiment_results_{timestamp}.csv"

    logging.info(f"Saving results to CSV: {output_path}")

    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write header with metadata
        writer.writerow(['Routing Experiment Results'])
        writer.writerow([f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'])
        if queries:
            writer.writerow([f'Total Queries: {len(queries)}'])
        writer.writerow([f'Total Runs: {len(centralized_runs)}'])
        writer.writerow([])

        # Determine if we have direct runs
        has_direct = direct_runs is not None and len(direct_runs) > 0

        # Write per-run summary table
        writer.writerow(['RUN SUMMARY'])
        if has_direct:
            writer.writerow(['Run', 'Cent Acc', 'Cent Lat', 'Cent Hop',
                            'Dist Acc', 'Dist Lat', 'Dist Hop',
                            'Direct Acc', 'Direct Lat', 'Direct Hop'])
            for i, ((c, d), dr) in enumerate(zip(zip(centralized_runs, distributed_runs), direct_runs), 1):
                writer.writerow([
                    i,
                    f"{c['accuracy']:.0f}%",
                    f"{c['avg_latency']:.2f}",
                    f"{c['avg_hops']:.1f}",
                    f"{d['accuracy']:.0f}%",
                    f"{d['avg_latency']:.2f}",
                    f"{d['avg_hops']:.1f}",
                    f"{dr['accuracy']:.0f}%",
                    f"{dr['avg_latency']:.2f}",
                    f"{dr['avg_hops']:.1f}"
                ])
        else:
            writer.writerow(['Run', 'Cent Accuracy', 'Cent Latency (s)', 'Cent Hops',
                            'Dist Accuracy', 'Dist Latency (s)', 'Dist Hops'])
            for i, (c, d) in enumerate(zip(centralized_runs, distributed_runs), 1):
                writer.writerow([
                    i,
                    f"{c['accuracy']:.1f}% ({c['correct']}/{c['total']})",
                    f"{c['avg_latency']:.2f}",
                    f"{c['avg_hops']:.1f}",
                    f"{d['accuracy']:.1f}% ({d['correct']}/{d['total']})",
                    f"{d['avg_latency']:.2f}",
                    f"{d['avg_hops']:.1f}"
                ])

        # Write statistics
        writer.writerow([])
        writer.writerow(['STATISTICS'])

        cen_accs = [r['accuracy'] for r in centralized_runs]
        cen_lats = [r['avg_latency'] for r in centralized_runs]
        cen_hops = [r['avg_hops'] for r in centralized_runs]

        dist_accs = [r['accuracy'] for r in distributed_runs]
        dist_lats = [r['avg_latency'] for r in distributed_runs]
        dist_hops = [r['avg_hops'] for r in distributed_runs]

        if has_direct:
            dir_accs = [r['accuracy'] for r in direct_runs]
            dir_lats = [r['avg_latency'] for r in direct_runs]
            dir_hops = [r['avg_hops'] for r in direct_runs]

            writer.writerow(['Metric', 'Cent Avg', 'Cent Min', 'Cent Max',
                            'Dist Avg', 'Dist Min', 'Dist Max',
                            'Direct Avg', 'Direct Min', 'Direct Max'])

            writer.writerow([
                'Accuracy (%)',
                f"{statistics.mean(cen_accs):.1f}",
                f"{min(cen_accs):.1f}",
                f"{max(cen_accs):.1f}",
                f"{statistics.mean(dist_accs):.1f}",
                f"{min(dist_accs):.1f}",
                f"{max(dist_accs):.1f}",
                f"{statistics.mean(dir_accs):.1f}",
                f"{min(dir_accs):.1f}",
                f"{max(dir_accs):.1f}"
            ])

            writer.writerow([
                'Latency (s)',
                f"{statistics.mean(cen_lats):.2f}",
                f"{min(cen_lats):.2f}",
                f"{max(cen_lats):.2f}",
                f"{statistics.mean(dist_lats):.2f}",
                f"{min(dist_lats):.2f}",
                f"{max(dist_lats):.2f}",
                f"{statistics.mean(dir_lats):.2f}",
                f"{min(dir_lats):.2f}",
                f"{max(dir_lats):.2f}"
            ])

            writer.writerow([
                'Hops',
                f"{statistics.mean(cen_hops):.1f}",
                f"{min(cen_hops):.1f}",
                f"{max(cen_hops):.1f}",
                f"{statistics.mean(dist_hops):.1f}",
                f"{min(dist_hops):.1f}",
                f"{max(dist_hops):.1f}",
                f"{statistics.mean(dir_hops):.1f}",
                f"{min(dir_hops):.1f}",
                f"{max(dir_hops):.1f}"
            ])
        else:
            writer.writerow(['Metric', 'Centralized Avg', 'Centralized Min', 'Centralized Max',
                            'Distributed Avg', 'Distributed Min', 'Distributed Max'])

            writer.writerow([
                'Accuracy (%)',
                f"{statistics.mean(cen_accs):.1f}",
                f"{min(cen_accs):.1f}",
                f"{max(cen_accs):.1f}",
                f"{statistics.mean(dist_accs):.1f}",
                f"{min(dist_accs):.1f}",
                f"{max(dist_accs):.1f}"
            ])

            writer.writerow([
                'Latency (s)',
                f"{statistics.mean(cen_lats):.2f}",
                f"{min(cen_lats):.2f}",
                f"{max(cen_lats):.2f}",
                f"{statistics.mean(dist_lats):.2f}",
                f"{min(dist_lats):.2f}",
                f"{max(dist_lats):.2f}"
            ])

            writer.writerow([
                'Hops',
                f"{statistics.mean(cen_hops):.1f}",
                f"{min(cen_hops):.1f}",
                f"{max(cen_hops):.1f}",
                f"{statistics.mean(dist_hops):.1f}",
                f"{min(dist_hops):.1f}",
                f"{max(dist_hops):.1f}"
            ])

        # Write test queries
        if queries:
            writer.writerow([])
            writer.writerow(['TEST QUERIES'])
            writer.writerow(['Index', 'Query', 'Expected Domain'])

            for i, (query, expected) in enumerate(queries, 1):
                writer.writerow([i, query, expected])

    logging.info(f"Results saved to {output_path}")
    print(f"\nResults saved to: {output_path}")

    return output_path


async def run_centralized(queries_to_run, verbose: bool = True, run_num: int = 1):
    """Run centralized routing tests."""
    mode = "centralized"
    logging.info(f"Run {run_num} - {mode.upper()}: Starting with {len(queries_to_run)} queries")

    if verbose:
        print_header("CENTRALIZED ROUTING (Idea 1)")
        print(f"Architecture: Root → 40 Domain Agents")
        print(f"Queries: {len(queries_to_run)}")

    coordinator, _ = create_centralized_system()
    centralized_results = []

    for i, (query, expected) in enumerate(queries_to_run, 1):
        result = await run_query_async(coordinator, query, mode, run_num)
        result['expected'] = expected
        centralized_results.append(result)
        if verbose:
            print(f"  [{i}/{len(queries_to_run)}] Tested: {query[:40]}...")

    print_results(centralized_results, "Centralized", verbose=verbose)
    logging.info(f"Run {run_num} - {mode.upper()}: Completed")
    return centralized_results


async def run_distributed(queries_to_run, verbose: bool = True, run_num: int = 1):
    """Run distributed routing tests."""
    mode = "distributed"
    logging.info(f"Run {run_num} - {mode.upper()}: Starting with {len(queries_to_run)} queries")

    if verbose:
        print_header("DISTRIBUTED ROUTING (Idea 2 - No Categories)")
        print(f"Architecture: Root → 40 Domains → Sub-agents")
        print(f"Queries: {len(queries_to_run)}")

    coordinator, _ = create_distributed_system()
    distributed_results = []

    for i, (query, expected) in enumerate(queries_to_run, 1):
        result = await run_query_async(coordinator, query, mode, run_num)
        result['expected'] = expected
        distributed_results.append(result)
        if verbose:
            print(f"  [{i}/{len(queries_to_run)}] Tested: {query[:40]}...")

    print_results(distributed_results, "Distributed", verbose=verbose)
    logging.info(f"Run {run_num} - {mode.upper()}: Completed")
    return distributed_results


async def run_direct(queries_to_run, verbose: bool = True, run_num: int = 1):
    """Run direct routing tests (Idea 3: Root → All sub-agents)."""
    mode = "direct"
    logging.info(f"Run {run_num} - {mode.upper()}: Starting with {len(queries_to_run)} queries")

    if verbose:
        print_header("DIRECT ROUTING (Idea 3 - Root → Sub-Agents)")
        print(f"Architecture: Root → 148 Sub-Agents (no domain layer)")
        print(f"Queries: {len(queries_to_run)}")

    coordinator, _ = create_direct_system()
    direct_results = []

    for i, (query, expected) in enumerate(queries_to_run, 1):
        result = await run_query_async(coordinator, query, mode, run_num)
        result['expected'] = expected
        direct_results.append(result)
        if verbose:
            print(f"  [{i}/{len(queries_to_run)}] Tested: {query[:40]}...")

    print_results(direct_results, "Direct", verbose=verbose)
    logging.info(f"Run {run_num} - {mode.upper()}: Completed")
    return direct_results


async def run_comparison(queries_to_run):
    """Run both and compare."""
    centralized_results = await run_centralized(queries_to_run)
    distributed_results = await run_distributed(queries_to_run)

    print_header("COMPARISON SUMMARY")

    centralized_correct = sum(1 for r in centralized_results if is_correct_routing(r['routed_to'], r['expected']))
    distributed_correct = sum(1 for r in distributed_results if is_correct_routing(r['routed_to'], r['expected']))

    centralized_avg_lat = sum(r['latency'] for r in centralized_results) / len(centralized_results)
    distributed_avg_lat = sum(r['latency'] for r in distributed_results) / len(distributed_results)

    centralized_avg_hops = sum(r['hop_count'] for r in centralized_results) / len(centralized_results)
    distributed_avg_hops = sum(r['hop_count'] for r in distributed_results) / len(distributed_results)

    print(f"\n{'Metric':<25} {'Centralized':<20} {'Distributed':<20} {'Winner'}")
    print("-" * 70)

    # Accuracy
    cen_acc = centralized_correct / len(centralized_results) * 100
    dist_acc = distributed_correct / len(distributed_results) * 100
    acc_diff = abs(cen_acc - dist_acc)
    acc_winner = "Tie" if acc_diff < 5 else ("Centralized" if cen_acc > dist_acc else "Distributed")
    print(f"{'Accuracy':<25} {cen_acc:.1f}%{' ':<14} {dist_acc:.1f}%{' ':<14} {acc_winner}")

    # Latency
    lat_winner = "Centralized" if centralized_avg_lat < distributed_avg_lat else "Distributed"
    print(f"{'Avg Latency':<25} {centralized_avg_lat:.2f}s{' ':<13} {distributed_avg_lat:.2f}s{' ':<13} {lat_winner}")

    # Hops
    hops_winner = "Centralized" if centralized_avg_hops < distributed_avg_hops else "Distributed"
    print(f"{'Avg Hops':<25} {centralized_avg_hops:.1f}{' ':<14} {distributed_avg_hops:.1f}{' ':<14} {hops_winner}")

    # Architecture
    print(f"\n{'Architecture':<25} {'1-2 hops':<20} {'2-3 hops':<20}")
    print(f"{'Routing Logic':<25} {'Centralized (40 opts)':<20} {'Distributed (5-10 opts)':<20}")
    print(f"{'Maintenance':<25} {'Single routing file':<20} {'Multiple files':<20}")

    print("\n" + "=" * 70)
    print("RECOMMENDATION:")
    if dist_acc >= cen_acc:
        winner = "Distributed routing (Idea 2)"
        reason = "Better or equal accuracy with distributed architecture"
    else:
        winner = "Centralized routing (Idea 1)"
        reason = "Better accuracy despite simpler architecture"
    print(f"  → {winner}")
    print(f"  → {reason}")
    print("=" * 70 + "\n")


async def main_async():
    parser = argparse.ArgumentParser(description="Routing Experiment: Centralized vs Distributed")
    parser.add_argument("--mode", choices=["centralized", "distributed", "direct", "compare", "quick"],
                       default="quick", help="Which mode to run")
    parser.add_argument("--queries", type=int, default=10,
                       help="Number of test queries to run")
    parser.add_argument("--runs", type=int, default=1,
                       help="Number of times to run the experiment (for statistical significance)")
    parser.add_argument("--output", type=str, default=None,
                       help="Path to save CSV results (default: experiment_results_TIMESTAMP.csv)")
    args = parser.parse_args()

    # Set up timestamped log file for this run
    log_filename = setup_timestamped_logging()

    logging.info(f"Starting experiment: mode={args.mode}, queries={args.queries}, runs={args.runs}, output={args.output}")
    logging.info(f"Log file: {log_filename}")

    # Select queries
    queries_to_run = TEST_QUERIES[:args.queries]

    # Storage for multi-run metrics
    centralized_run_metrics = []
    distributed_run_metrics = []
    direct_run_metrics = []

    for run_num in range(args.runs):
        current_run = run_num + 1
        if args.runs > 1:
            print(f"\n{'=' * 70}")
            print(f"  RUN {current_run} of {args.runs}")
            print('=' * 70)

        verbose = (args.runs == 1)  # Only show detailed output for single run

        if args.mode in ["centralized", "compare", "quick"]:
            centralized_results = await run_centralized(queries_to_run, verbose=verbose, run_num=current_run)
            centralized_run_metrics.append(calculate_run_metrics(centralized_results, "centralized", current_run))

        if args.mode in ["distributed", "compare", "quick"]:
            distributed_results = await run_distributed(queries_to_run, verbose=verbose, run_num=current_run)
            distributed_run_metrics.append(calculate_run_metrics(distributed_results, "distributed", current_run))

        if args.mode in ["direct", "compare", "quick"]:
            direct_results = await run_direct(queries_to_run, verbose=verbose, run_num=current_run)
            direct_run_metrics.append(calculate_run_metrics(direct_results, "direct", current_run))

    # Print multi-run table if multiple runs
    if args.runs > 1 and args.mode in ["compare", "quick"]:
        print_multi_run_table(centralized_run_metrics, distributed_run_metrics, direct_run_metrics)
        # Save to CSV
        save_results_to_csv(centralized_run_metrics, distributed_run_metrics, direct_run_metrics, queries_to_run, args.output)

    # Print single-run comparison for single run mode
    if args.runs == 1 and args.mode in ["compare", "quick"]:
        print_header("COMPARISON SUMMARY")

        centralized_correct = sum(1 for r in centralized_results if is_correct_routing(r['routed_to'], r['expected']))
        distributed_correct = sum(1 for r in distributed_results if is_correct_routing(r['routed_to'], r['expected']))
        direct_correct = sum(1 for r in direct_results if is_correct_routing(r['routed_to'], r['expected']))

        centralized_avg_lat = sum(r['latency'] for r in centralized_results) / len(centralized_results)
        distributed_avg_lat = sum(r['latency'] for r in distributed_results) / len(distributed_results)
        direct_avg_lat = sum(r['latency'] for r in direct_results) / len(direct_results)

        centralized_avg_hops = sum(r['hop_count'] for r in centralized_results) / len(centralized_results)
        distributed_avg_hops = sum(r['hop_count'] for r in distributed_results) / len(distributed_results)
        direct_avg_hops = sum(r['hop_count'] for r in direct_results) / len(direct_results)

        print(f"\n{'Metric':<25} {'Centralized':<18} {'Distributed':<18} {'Direct':<18} {'Winner'}")
        print("-" * 100)

        cen_acc = centralized_correct / len(centralized_results) * 100
        dist_acc = distributed_correct / len(distributed_results) * 100
        dir_acc = direct_correct / len(direct_results) * 100
        best_acc = max(cen_acc, dist_acc, dir_acc)
        acc_winner = "Tie" if (max(cen_acc, dist_acc, dir_acc) - min(cen_acc, dist_acc, dir_acc)) < 5 else (
            "Centralized" if best_acc == cen_acc else ("Direct" if best_acc == dir_acc else "Distributed"))
        print(f"{'Accuracy':<25} {cen_acc:.1f}%{' ':<12} {dist_acc:.1f}%{' ':<12} {dir_acc:.1f}%{' ':<12} {acc_winner}")

        best_lat = min(centralized_avg_lat, distributed_avg_lat, direct_avg_lat)
        lat_winner = "Centralized" if best_lat == centralized_avg_lat else ("Direct" if best_lat == direct_avg_lat else "Distributed")
        print(f"{'Avg Latency':<25} {centralized_avg_lat:.2f}s{' ':<11} {distributed_avg_lat:.2f}s{' ':<11} {direct_avg_lat:.2f}s{' ':<11} {lat_winner}")

        best_hops = min(centralized_avg_hops, distributed_avg_hops, direct_avg_hops)
        hops_winner = "Centralized" if best_hops == centralized_avg_hops else ("Direct" if best_hops == direct_avg_hops else "Distributed")
        print(f"{'Avg Hops':<25} {centralized_avg_hops:.1f}{' ':<12} {distributed_avg_hops:.1f}{' ':<12} {direct_avg_hops:.1f}{' ':<12} {hops_winner}")

        print(f"\n{'Architecture':<25} {'Root → 40':<18} {'Root → 40 → Sub':<18} {'Root → 148':<18}")
        print(f"{'Routing Logic':<25} {'Centralized':<18} {'Distributed':<18} {'Direct':<18}")

        print("\n" + "=" * 100)
        print("RECOMMENDATION:")
        best_acc_val = max(cen_acc, dist_acc, dir_acc)
        if best_acc_val == dir_acc:
            winner = "Direct routing (Idea 3)"
            reason = "Best accuracy with direct sub-agent access"
        elif best_acc_val == dist_acc:
            winner = "Distributed routing (Idea 2)"
            reason = "Better or equal accuracy with distributed architecture"
        else:
            winner = "Centralized routing (Idea 1)"
            reason = "Better accuracy despite simpler architecture"
        print(f"  → {winner}")
        print(f"  → {reason}")
        print("=" * 100 + "\n")

        # Save to CSV for single run too
        save_results_to_csv(centralized_run_metrics, distributed_run_metrics, direct_run_metrics, queries_to_run, args.output)

    logging.info("Experiment completed successfully")


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
