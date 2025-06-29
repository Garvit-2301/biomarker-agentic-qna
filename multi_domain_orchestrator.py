from typing import Dict, Any
from utils.llm_factory import LLMFactory
from utils.user_data_loader import UserDataLoader
from agents.common.domain_classifier import DomainClassifierAgent
from agents.common.intent_classifier import IntentClassifierAgent
from agents.common.explainer import ExplainerAgent
from agents.common.compare import CompareAgent

# Import domain-specific agents
from agents.methylation.insight_builder import MethylationInsightBuilderAgent
from agents.methylation.recommendation import MethylationRecommendationAgent
from agents.metagenomics.insight_builder import MetagenomicsInsightBuilderAgent
from agents.whole_exome.insight_builder import WholeExomeInsightBuilderAgent
from agents.proteomics.insight_builder import ProteomicsInsightBuilderAgent
from agents.transcriptomics.insight_builder import TranscriptomicsInsightBuilderAgent
from agents.whole_genome.insight_builder import WholeGenomeInsightBuilderAgent

class MultiDomainOrchestrator:
    def __init__(self, llm_client_type: str = "openai", **llm_kwargs) -> None:
        """
        Initialize the multi-domain orchestrator
        
        Args:
            llm_client_type: Type of LLM client ("openai" or "llama3")
            **llm_kwargs: Additional arguments for the LLM client
        """
        self.llm = LLMFactory.create_client(llm_client_type, **llm_kwargs)
        self.llm_client_type = llm_client_type
        self.user_loader = UserDataLoader()
        
        # Initialize classifiers
        self.domain_classifier = DomainClassifierAgent(self.llm)
        self.intent_classifier = IntentClassifierAgent(self.llm)
        
        # Initialize common agents
        self.common_agents = {
            "Explain_Score": ExplainerAgent(self.llm),
            "Compare": CompareAgent(self.llm),
        }
        
        # Initialize domain-specific agents
        self.domain_agents = {
            "methylation": {
                "Insight": MethylationInsightBuilderAgent(self.llm),
                "Recommendation": MethylationRecommendationAgent(self.llm),
            },
            "metagenomics": {
                "Insight": MetagenomicsInsightBuilderAgent(self.llm),
            },
            "whole_exome": {
                "Insight": WholeExomeInsightBuilderAgent(self.llm),
            },
            "proteomics": {
                "Insight": ProteomicsInsightBuilderAgent(self.llm),
            },
            "transcriptomics": {
                "Insight": TranscriptomicsInsightBuilderAgent(self.llm),
            },
            "whole_genome": {
                "Insight": WholeGenomeInsightBuilderAgent(self.llm),
            },
        }

    def handle_user_query(self, user_id: str, user_query: str, *, 
                         demographics: Dict[str, Any] = None, 
                         baseline: Dict[str, Any] = None) -> str:
        """
        Handle query for a specific user by determining domain and intent
        """
        # First, classify the domain
        domain = self.domain_classifier.run(user_query, {})
        
        # Load user's report data for the specific domain
        user_report = self.user_loader.load_user_report(user_id, domain)
        if user_report is None:
            available_domains = self.user_loader.get_available_domains(user_id)
            return f"Error: No {domain} data found for user {user_id}. Available domains: {', '.join(available_domains)}"
        
        # Create context with user data and domain
        ctx: Dict[str, Any] = {
            "report": user_report,
            "demographics": demographics or {},
            "baseline": baseline or {},
            "user_id": user_id,
            "domain": domain,
            "full_user_data": user_report
        }
        
        # Handle "what is" queries
        if user_query.lower().startswith("what is"):
            ctx["term"] = user_query.split("what is", 1)[1].strip(" ?")
        
        # Classify intent
        intent = self.intent_classifier.run(user_query, ctx)
        
        # Route to appropriate agent
        if intent in ["Explain_Score", "Compare"]:
            # Use common agents
            agent = self.common_agents.get(intent)
        elif domain in self.domain_agents and intent in self.domain_agents[domain]:
            # Use domain-specific agent
            agent = self.domain_agents[domain][intent]
        else:
            # Fallback to domain-specific insight agent
            agent = self.domain_agents[domain]["Insight"] if domain in self.domain_agents else None
        
        if agent is None:
            return f"Error: No agent available for domain '{domain}' and intent '{intent}'"
        
        return agent.run(user_query, ctx)

    def get_available_users(self) -> list:
        """
        Get list of available users
        """
        return self.user_loader.get_available_users()
    
    def get_available_domains(self, user_id: str) -> list:
        """
        Get list of available domains for a specific user
        """
        return self.user_loader.get_available_domains(user_id)
    
    def get_llm_info(self) -> Dict[str, Any]:
        """
        Get information about the current LLM client
        """
        return {
            "client_type": self.llm_client_type,
            "model": getattr(self.llm, 'model', 'unknown'),
            "connection_status": self.llm.test_connection() if hasattr(self.llm, 'test_connection') else "unknown"
        }

if __name__ == '__main__':
    # Sample demographics and baseline data
    demographics = {"age": 35, "sex": "F"}
    baseline = {"mean_health_score": 0.12}
    
    # Initialize orchestrator
    qa = MultiDomainOrchestrator("openai", model="gpt-4")
    
    # Show available users
    print("Available users:", qa.get_available_users())
    print("LLM Info:", qa.get_llm_info())
    print("\n" + "="*50)
    
    # Test different domain queries
    test_queries = [
        ("user_001", "Can you explain my methylation report?"),
        ("user_001", "What is CpG methylation?"),
        ("user_001", "How do my microbiome results compare to others?"),
        ("user_001", "Explain my whole exome sequencing results"),
    ]
    
    for user_id, query in test_queries:
        print(f"\n{'='*20} USER: {user_id} {'='*20}")
        print(f"Query: {query}")
        print("-" * 60)
        
        try:
            response = qa.handle_user_query(user_id, query,
                                          demographics=demographics, baseline=baseline)
            print(response)
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n" + "="*60) 