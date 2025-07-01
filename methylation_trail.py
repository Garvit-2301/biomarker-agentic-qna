import dspy
from agents.demo_agent import DemoAgent

# Configure your real LLM
lm = dspy.LM(
    model="meta-llama/Llama-3-8b-chat-hf",
    api_key="tgp_v1_xaeOuQ7mmffFW8s-eyDp1RB3HbUSRyU-XWzhsf2nino",
    api_base="https://api.together.xyz/",
    custom_llm_provider="together_ai"
)
dspy.configure(lm=lm)

# Example run for methylation analysis
#agent = DemoAgent(domain="methylation", agent_type="analysis", user_id="test_user_001")
#result = agent.process()

#print(f"Success: {result['success']}")
#print(f"Response: {result['response'][:500]}...")
domains = ["methylation", "metagenomics", "proteomics", "transcriptomics", "whole_exome", "whole_genome"]
agent_types = ["analysis", "summary", "recommendation"]

for domain in domains:
    for agent_type in agent_types:
        agent = DemoAgent(domain=domain, agent_type=agent_type, user_id="test_user_001")
        result = agent.process()
        print(f"{domain} - {agent_type}: {'✓' if result['success'] else '✗'}")
        print(f"Response: {result['response'][:300]}...\n")
