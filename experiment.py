#!/usr/bin/env python3
"""
Routing Experiment: Centralized vs Distributed

Compares two routing approaches:
- Idea 1: Centralized routing (one root, 40 direct sub-agents)
- Idea 2: Distributed routing (root -> categories -> domains -> sub-agents)
"""

import argparse
import asyncio
import os
import time
from typing import Dict, List

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

MODEL = "gemini-2.0-flash"

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


async def run_query_async(agent, query: str, mode: str) -> Dict:
    """Run a query and return metrics using ADK's InMemoryRunner."""
    runner = InMemoryRunner(agent=agent, app_name=f"routing_experiment_{mode}")

    start_time = time.time()
    events = await runner.run_debug(
        query,
        user_id="test_user",
        session_id=f"test_session_{mode}",
        quiet=True
    )
    latency = time.time() - start_time

    # Extract response and routing info
    response_text = ""
    routing_path = []

    for event in events:
        # Get content from events
        if hasattr(event, 'content') and event.content:
            if hasattr(event.content, 'parts'):
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


def print_results(results: List[Dict], mode: str):
    """Print query results."""
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


async def run_centralized(queries_to_run):
    """Run centralized routing tests."""
    print_header("CENTRALIZED ROUTING (Idea 1)")
    print(f"Architecture: Root → 40 Domain Agents")
    print(f"Queries: {len(queries_to_run)}")

    coordinator, _ = create_centralized_system()
    centralized_results = []

    for query, expected in queries_to_run:
        result = await run_query_async(coordinator, query, "centralized")
        result['expected'] = expected
        centralized_results.append(result)
        print(f"  Tested: {query[:40]}...")

    print_results(centralized_results, "Centralized")
    return centralized_results


async def run_distributed(queries_to_run):
    """Run distributed routing tests."""
    print_header("DISTRIBUTED ROUTING (Idea 2 - No Categories)")
    print(f"Architecture: Root → 40 Domains → Sub-agents")
    print(f"Queries: {len(queries_to_run)}")

    coordinator, _ = create_distributed_system()
    distributed_results = []

    for query, expected in queries_to_run:
        result = await run_query_async(coordinator, query, "distributed")
        result['expected'] = expected
        distributed_results.append(result)
        print(f"  Tested: {query[:40]}...")

    print_results(distributed_results, "Distributed")
    return distributed_results


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
    parser.add_argument("--mode", choices=["centralized", "distributed", "compare", "quick"],
                       default="quick", help="Which mode to run")
    parser.add_argument("--queries", type=int, default=10,
                       help="Number of test queries to run")
    args = parser.parse_args()

    # Select queries
    queries_to_run = TEST_QUERIES[:args.queries]

    if args.mode in ["centralized", "compare", "quick"]:
        centralized_results = await run_centralized(queries_to_run)

    if args.mode in ["distributed", "compare", "quick"]:
        distributed_results = await run_distributed(queries_to_run)

    if args.mode in ["compare", "quick"]:
        print_header("COMPARISON SUMMARY")

        centralized_correct = sum(1 for r in centralized_results if is_correct_routing(r['routed_to'], r['expected']))
        distributed_correct = sum(1 for r in distributed_results if is_correct_routing(r['routed_to'], r['expected']))

        centralized_avg_lat = sum(r['latency'] for r in centralized_results) / len(centralized_results)
        distributed_avg_lat = sum(r['latency'] for r in distributed_results) / len(distributed_results)

        centralized_avg_hops = sum(r['hop_count'] for r in centralized_results) / len(centralized_results)
        distributed_avg_hops = sum(r['hop_count'] for r in distributed_results) / len(distributed_results)

        print(f"\n{'Metric':<25} {'Centralized':<20} {'Distributed':<20} {'Winner'}")
        print("-" * 70)

        cen_acc = centralized_correct / len(centralized_results) * 100
        dist_acc = distributed_correct / len(distributed_results) * 100
        acc_diff = abs(cen_acc - dist_acc)
        acc_winner = "Tie" if acc_diff < 5 else ("Centralized" if cen_acc > dist_acc else "Distributed")
        print(f"{'Accuracy':<25} {cen_acc:.1f}%{' ':<14} {dist_acc:.1f}%{' ':<14} {acc_winner}")

        lat_winner = "Centralized" if centralized_avg_lat < distributed_avg_lat else "Distributed"
        print(f"{'Avg Latency':<25} {centralized_avg_lat:.2f}s{' ':<13} {distributed_avg_lat:.2f}s{' ':<13} {lat_winner}")

        hops_winner = "Centralized" if centralized_avg_hops < distributed_avg_hops else "Distributed"
        print(f"{'Avg Hops':<25} {centralized_avg_hops:.1f}{' ':<14} {distributed_avg_hops:.1f}{' ':<14} {hops_winner}")

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


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
