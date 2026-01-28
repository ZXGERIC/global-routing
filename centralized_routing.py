"""
Idea 1: Centralized Routing
All 40 domain agents are sub-agents of a single root coordinator.
The root agent routes directly to the appropriate domain agent.
"""

import time
from google.adk.agents import LlmAgent
from domains import DOMAINS

# Import model configuration
MODEL = "gemini-2.0-flash"  # or "gemini-2.5-flash"

def create_centralized_system():
    """
    Creates a centralized routing system where all 40 domains
    are sub-agents of a single root coordinator.
    """

    # Create 40 domain agents
    domain_agents = []
    domain_descriptions = []

    for domain in DOMAINS:
        agent = LlmAgent(
            name=f"{domain['name']}_agent",
            model=MODEL,
            instruction=f"""You are the {domain['name'].title()} agent.

Your description: {domain['description']}

You handle queries related to: {', '.join(domain['keywords'])}

When you receive a query, acknowledge it and indicate you are the {domain['name']} agent handling this request.
Keep your response brief and focused on confirming you've routed correctly.""",
            description=f"{domain['name']}: {domain['description']}",
        )
        domain_agents.append(agent)
        domain_descriptions.append(f"- {domain['name']}: {domain['description']}")

    # Create the root coordinator with all 40 agents as sub-agents
    routing_instruction = f"""You are the central routing coordinator. Your job is to route user queries to the appropriate domain agent.

Available domain agents:
{chr(10).join(domain_descriptions)}

IMPORTANT: Analyze the user's query carefully and route to the MOST appropriate domain agent.
- Consider the user's intent and keywords
- If a query could fit multiple domains, choose the PRIMARY intent
- Be decisive - pick ONE agent

After routing, respond with: [ROUTED_TO: agent_name]"""

    root_coordinator = LlmAgent(
        name="central_coordinator",
        model=MODEL,
        instruction=routing_instruction,
        sub_agents=domain_agents,
    )

    return root_coordinator, domain_agents


def query_centralized(coordinator, query: str) -> dict:
    """
    Query the centralized routing system and return metrics.
    """
    start_time = time.time()

    # Run the query through the coordinator
    response = coordinator.run(query)

    end_time = time.time()
    latency = end_time - start_time

    # Parse the response to extract which agent was routed to
    routed_to = "unknown"
    if "[ROUTED_TO:" in response:
        start_idx = response.find("[ROUTED_TO:") + len("[ROUTED_TO:")
        end_idx = response.find("]", start_idx)
        routed_to = response[start_idx:end_idx].strip()

    return {
        "response": response,
        "routed_to": routed_to,
        "latency": latency,
        "query": query
    }


def main():
    """Test the centralized routing system."""
    print("=" * 60)
    print("CENTRALIZED ROUTING SYSTEM (Idea 1)")
    print("=" * 60)
    print(f"\nCreating system with {len(DOMAINS)} domain agents...\n")

    coordinator, domain_agents = create_centralized_system()

    print(f"Root coordinator: {coordinator.name}")
    print(f"Sub-agents: {len(domain_agents)}")
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
        result = query_centralized(coordinator, query)
        print(f"\nQuery: {query}")
        print(f"Routed to: {result['routed_to']}")
        print(f"Latency: {result['latency']:.2f}s")


if __name__ == "__main__":
    main()
