"""
Centralized Routing Errors Analysis
Current: 85% accuracy (17/20 correct)
Goal: Improve to match distributed's 95%
"""

ERRORS = [
    ("Report an expense", "coordinator", "finance", "Coordinator didn't delegate"),
    ("When do I get paid?", "coordinator", "hr", "Ambiguous: payroll vs finance"),
    ("Enroll in training program", "learning_development", "hr", "L&D is valid, but HR owns it"),
]

print("=" * 60)
print("CENTRALIZED ROUTING ERROR ANALYSIS")
print("=" * 60)

for query, routed, expected, reason in ERRORS:
    print(f"\nQuery: '{query}'")
    print(f"  Routed to: {routed}")
    print(f"  Expected: {expected}")
    print(f"  Issue: {reason}")

print("\n" + "=" * 60)
print("POTENTIAL IMPROVEMENTS:")
print("=" * 60)
print("""
1. BETTER AGENT DESCRIPTIONS
   - Add explicit "handles queries like..." examples
   - Clarify boundaries between overlapping domains

2. IMPROVED ROUTING INSTRUCTION
   - Force delegation (never answer as coordinator)
   - Priority rules for ambiguous cases

3. KEYWORD HINTS
   - Add explicit keywords to agent descriptions
   - Use synonyms and related terms

4. DOMAIN OWNERSHIP CLARIFICATION
   - Training → HR owns, L&D executes
   - Payroll → HR owns
""")
