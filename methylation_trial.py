import dspy 
from agents.demo_agent import DemoAgent

lm = dspy.LM(model="meta-llama/Llama-3-8b-chat-hf", api_key="tgp_v1_xaeOuQ7mmff-FW8s-eyDp1RB3HbUSRyU-XWzhsf2nino", api_base="https://api.together.xyz/", custom_llm_provider="together_ai")
dspy.configure(lm=lm)

#Methylation agent
for domain in domains:
  for agent_type in agent_types:
    agent = DemoAgent(domain=domain,
                      agent_type=agent_type,
                      user_id="user-123")
    result = agent.process()
    print(f"{domain} - {agent_type}:{'yes" if result['success'] else 'no'}")
    print(f"Response: {result['reponse'][:300]}...\n")
