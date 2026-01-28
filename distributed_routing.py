"""
Idea 2: Distributed Routing (No Categories)
Root agent routes directly to domain agents, and each domain agent routes to its own sub-agents.
Routing logic is distributed across the hierarchy.
"""

import time
from google.adk.agents import LlmAgent
from domains import DOMAINS, SUB_AGENTS

# Import model configuration
MODEL = "gemini-2.0-flash"  # or "gemini-2.5-flash"


def create_distributed_system():
    """
    Creates a distributed routing system where:
    1. Root agent routes directly to domain agents
    2. Each domain agent routes to its own sub-agents
    """

    # Create domain agents
    domain_agent_map = {}  # Maps domain name -> agent instance
    domain_descriptions = []

    for domain in DOMAINS:
        # Create sub-agents for this domain
        sub_agents = []
        sub_agent_descriptions = []

        for sub_name in domain.get("sub_agents", []):
            sub_desc = SUB_AGENTS.get(sub_name, f"Handles {sub_name} tasks")
            sub_agent = LlmAgent(
                name=f"{domain['name']}_{sub_name}",
                model=MODEL,
                instruction=f"""You are the {sub_name.title()} sub-agent within the {domain['name']} domain.

Your description: {sub_desc}

Acknowledge you are the {domain['name']}/{sub_name} sub-agent handling this request.
Start your response with: [ROUTED_TO: {domain['name']}_{sub_name}]
Keep your response brief.""",
                description=f"{sub_name}: {sub_desc}",
            )
            sub_agents.append(sub_agent)
            sub_agent_descriptions.append(f"- {sub_name}: {sub_desc}")

        # Store sub-agents
        if sub_agents:
            routing_instruction = f"""You are the {domain['name'].title()} domain agent.

Your description: {domain['description']}
Your keywords: {', '.join(domain['keywords'])}

You route queries to your specialized sub-agents:
{chr(10).join(sub_agent_descriptions)}

Route to the most appropriate sub-agent and delegate immediately.
After routing, indicate with: [ROUTED_TO: {domain['name']}]"""
        else:
            routing_instruction = f"""You are the {domain['name'].title()} domain agent.

Your description: {domain['description']}
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

    # Create the root coordinator that routes directly to domain agents
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

    return root_coordinator, {
        'domain_agents': domain_agent_map,
    }


def query_distributed(coordinator, query: str) -> dict:
    """
    Query the distributed routing system and return metrics.
    """
    start_time = time.time()

    # Run the query through the distributed system
    response = coordinator.run(query)

    end_time = time.time()
    latency = end_time - start_time

    # Parse the response
    routed_to = []
    temp_response = response
    while "[ROUTED_TO:" in temp_response:
        start_idx = temp_response.find("[ROUTED_TO:") + len("[ROUTED_TO:")
        end_idx = temp_response.find("]", start_idx)
        agent = temp_response[start_idx:end_idx].strip()
        routed_to.append(agent)
        temp_response = temp_response[end_idx + 1:]

    if "[HANDLED_BY:" in response:
        start_idx = response.find("[HANDLED_BY:") + len("[HANDLED_BY:")
        end_idx = response.find("]", start_idx)
        routed_to.append(response[start_idx:end_idx].strip())

    return {
        "response": response,
        "routing_path": routed_to,
        "hop_count": len(routed_to),
        "latency": latency,
        "query": query
    }


def main():
    """Test the distributed routing system."""
    print("=" * 60)
    print("DISTRIBUTED ROUTING SYSTEM (Idea 2 - No Categories)")
    print("=" * 60)
    print("\nCreating distributed system with:")
    print("  - 1 Root coordinator")
    print(f"  - {len(DOMAINS)} Domain agents")
    print("  - Sub-agents within each domain\n")

    coordinator, system = create_distributed_system()

    print(f"Root coordinator: {coordinator.name}")
    print(f"Domain agents: {len(system['domain_agents'])}")
    print("\n" + "=" * 60)

    # Test queries
    test_queries = [
        "I need to book a flight to Tokyo",
        "Check my bank balance",
        "Reset my password",
        "Where is my order?",
        "Request time off for next week",
        "Create a marketing campaign",
        "Review this contract",
        "Plan a vacation to Hawaii",
    ]

    print("\nTest Queries:")
    print("-" * 60)

    for query in test_queries:
        result = query_distributed(coordinator, query)
        print(f"\nQuery: {query}")
        print(f"Routing path: {' -> '.join(result['routing_path'])}")
        print(f"Hops: {result['hop_count']}")
        print(f"Latency: {result['latency']:.2f}s")


if __name__ == "__main__":
    main()
