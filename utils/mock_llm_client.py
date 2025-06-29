import json
import time
import random
from typing import Dict, Any, Optional, List
from datetime import datetime

class MockLLMClient:
    """
    Mock LLM client for offline testing of the agentic workflow.
    Simulates responses without making actual API calls.
    """
    
    def __init__(self, client_type: str = "mock"):
        self.client_type = client_type
        self.call_count = 0
        self.response_templates = self._load_response_templates()
        
    def _load_response_templates(self) -> Dict[str, Any]:
        return {
            "analysis": {
                "methylation": {
                    "response": "Based on the methylation analysis of user {user_id}, I found several key insights:\n\n1. **Methylation Status**: The user shows {methylation_level} methylation levels in key genes.\n2. **Health Implications**: This pattern suggests {health_implication}.\n3. **Recommendations**: Consider {recommendation}.\n\nOverall assessment: {overall_assessment}",
                    "parameters": {"max_tokens": 500, "temperature": 0.3}
                },
                "metagenomics": {
                    "response": "Gut microbiome analysis for user {user_id} reveals:\n\n1. **Diversity Index**: {diversity_score} (optimal range: 3.0-4.5)\n2. **Key Species**: {key_species}\n3. **Dysbiosis Indicators**: {dysbiosis_indicators}\n4. **Metabolic Pathways**: {metabolic_pathways}\n\nRecommendations: {recommendations}",
                    "parameters": {"max_tokens": 600, "temperature": 0.2}
                }
            },
            "summary": {
                "response": "**Executive Summary for {user_id}**\n\n**Key Findings**:\n{key_findings}\n\n**Risk Assessment**:\n{risk_assessment}\n\n**Priority Actions**:\n{priority_actions}\n\n**Next Steps**:\n{next_steps}",
                "parameters": {"max_tokens": 400, "temperature": 0.2}
            },
            "recommendation": {
                "response": "**Personalized Recommendations for {user_id}**\n\n**Lifestyle Changes**:\n{lifestyle_changes}\n\n**Dietary Recommendations**:\n{dietary_recommendations}\n\n**Supplementation**:\n{supplementation}\n\n**Monitoring**:\n{monitoring}\n\n**Follow-up**:\n{follow_up}",
                "parameters": {"max_tokens": 500, "temperature": 0.3}
            }
        }
    
    def generate_response(self, prompt: str, agent_type: str, domain: str = None, **kwargs) -> Dict[str, Any]:
        self.call_count += 1
        time.sleep(random.uniform(0.1, 0.5))
        
        template = self._get_response_template(agent_type, domain)
        mock_data = self._generate_mock_data(agent_type, domain, **kwargs)
        
        try:
            response_text = template["response"].format(**mock_data)
        except KeyError as e:
            response_text = f"Mock response for {agent_type} agent in {domain} domain. Error in template: {e}"
        
        response = {
            "id": f"mock_response_{self.call_count}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": f"mock-{self.client_type}-model",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response_text
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": len(prompt.split()),
                "completion_tokens": len(response_text.split()),
                "total_tokens": len(prompt.split()) + len(response_text.split())
            }
        }
        
        return response
    
    def _get_response_template(self, agent_type: str, domain: str = None) -> Dict[str, Any]:
        if agent_type in self.response_templates:
            if domain and domain in self.response_templates[agent_type]:
                return self.response_templates[agent_type][domain]
            elif "response" in self.response_templates[agent_type]:
                return self.response_templates[agent_type]
        
        return {
            "response": f"Mock response for {agent_type} agent{f' in {domain} domain' if domain else ''}.",
            "parameters": {"max_tokens": 300, "temperature": 0.3}
        }
    
    def _generate_mock_data(self, agent_type: str, domain: str = None, **kwargs) -> Dict[str, Any]:
        base_data = {
            "user_id": kwargs.get("user_id", "user_001"),
            "timestamp": datetime.now().isoformat(),
            "analysis_date": datetime.now().strftime("%Y-%m-%d")
        }
        
        if domain == "methylation":
            base_data.update({
                "methylation_level": random.choice(["high", "moderate", "low"]),
                "health_implication": "potential impact on gene regulation",
                "recommendation": "lifestyle modifications and targeted supplementation",
                "overall_assessment": "normal methylation patterns with some areas of interest"
            })
        elif domain == "metagenomics":
            base_data.update({
                "diversity_score": round(random.uniform(2.5, 4.8), 2),
                "key_species": "Bifidobacterium, Lactobacillus, Akkermansia",
                "dysbiosis_indicators": "slight reduction in beneficial bacteria",
                "metabolic_pathways": "short-chain fatty acid production pathways",
                "recommendations": "increase fiber intake and consider probiotics"
            })
        
        if agent_type == "summary":
            base_data.update({
                "key_findings": "comprehensive analysis reveals normal patterns",
                "risk_assessment": "low to moderate risk profile",
                "priority_actions": "maintain current lifestyle, monitor trends",
                "next_steps": "follow-up in 6 months recommended"
            })
        elif agent_type == "recommendation":
            base_data.update({
                "lifestyle_changes": "regular exercise and stress management",
                "dietary_recommendations": "balanced diet with increased fiber",
                "supplementation": "vitamin D and omega-3 fatty acids",
                "monitoring": "quarterly biomarker tracking",
                "follow_up": "schedule follow-up consultation"
            })
        
        return base_data
    
    def get_usage_stats(self) -> Dict[str, Any]:
        return {
            "total_calls": self.call_count,
            "client_type": self.client_type,
            "average_response_time": "0.3 seconds (simulated)",
            "success_rate": "100% (mock client)"
        }
    
    def reset_stats(self) -> None:
        self.call_count = 0
